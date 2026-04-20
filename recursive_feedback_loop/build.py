"""Build mode -- AI builds a project by feeding its own progress back.

Give it a project idea. The AI designs, builds, tests, and iterates.
Each iteration the AI sees what it produced last time, what files exist
in the project, and continues building however it wants.

When the AI wants to explore alternatives, it can trigger possibilities
by including [EXPLORE: question] in its output. The loop detects this,
runs ai_possibilities, and feeds the branches back as context.

Architecture:
  Iteration 0: seed prompt -> Hermes (tools) -> design + start building
  Iteration N: project state + last output + explore results -> Hermes -> continue
  Between iterations: detect [EXPLORE] triggers, run possibilities if found

Different from RFL:
  - No compaction. Each iteration gets: seed + project state + last output.
  - No prescriptive synthesis. The AI decides what to do next.
  - Possibilities integration for creative branching.

Different from evolve:
  - Uses Hermes subprocess (has tools -- reads/writes files).
  - Reads actual project state between iterations.
  - The AI builds a real project, not just refined text.
"""

import json
import os
import re
import subprocess
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


CONTINUE_TEMPLATE = """You are autonomously building a project. Here's your context:

ORIGINAL GOAL:
{seed}

IMPORTANT: Create all files under {workdir}/ using ABSOLUTE paths.
Use the terminal tool (mkdir, cat >, etc.) with full paths like {workdir}/src/main.rs.
Do NOT use relative paths -- they may resolve to the wrong directory.

PROJECT STATE:
{project_state}

YOUR PREVIOUS ITERATION (iteration {prev_iteration}):
{prev_summary}
{explore_context}
RAW OUTPUT FROM LAST ITERATION (for reference, may be truncated):
{prev_output}

Continue building. You have full creative control. Read files, write files,
run commands. Decide what to do next based on what you've built so far.
If you're stuck or want to explore alternatives, include this line in your output:
[EXPLORE: your question here]
The system will explore alternatives and feed them back to you.
If you think the project is complete, say [DONE] on its own line."""

EXPLORE_INJECT_TEMPLATE = """

EXPLORATION RESULTS (alternatives the system found):
{explore_results}
Consider these alternatives and pick the best path forward, or ignore them
if you have a better idea. You're in control."""


@dataclass
class BuildConfig:
    seed_prompt: str
    workdir: str = "."               # where Hermes runs (project dir)
    iterations: int = 8
    hermes_binary: str = "hermes"
    hermes_model: Optional[str] = None
    hermes_provider: Optional[str] = None
    retry_provider: Optional[str] = None  # fallback provider on timeout
    retry_model: Optional[str] = None     # fallback model on timeout
    iteration_timeout: int = 900     # seconds per iteration
    explore_enabled: bool = True     # enable [EXPLORE] triggers
    explore_depth: int = 1           # possibilities exploration depth
    explore_max_branches: int = 5
    output_dir: str = ""
    save_snapshots: bool = True


@dataclass
class BuildTurn:
    iteration: int
    prompt: str
    output: str
    explored: bool = False
    explore_question: str = ""
    explore_branches: list = field(default_factory=list)
    elapsed_seconds: float = 0.0
    hermes_exit_code: int = 0


@dataclass
class BuildState:
    id: str = ""
    config: BuildConfig = None
    turns: list = field(default_factory=list)
    final_output: str = ""
    project_path: str = ""
    output_dir: str = ""

    def elapsed(self) -> float:
        return sum(t.elapsed_seconds for t in self.turns)


class BuildRunner:
    """Run an autonomous build loop."""

    def __init__(self, config: BuildConfig):
        self.config = config
        self.state = BuildState(
            id=uuid.uuid4().hex[:8],
            config=config,
            project_path=str(Path(config.workdir).resolve()),
        )
        self._stop = False

    def stop(self):
        self._stop = True

    def run(self) -> BuildState:
        """Run the build loop."""
        self.state.output_dir = self._resolve_output_dir()
        Path(self.state.output_dir).mkdir(parents=True, exist_ok=True)

        prev_output = ""
        explore_context = ""

        for i in range(self.config.iterations):
            if self._stop:
                break

            # Build the prompt for this iteration
            # NOTE: Hermes file tools (patch, write_file) resolve paths relative
            # to its auto-detected project root, NOT the subprocess cwd. So we
            # must use absolute paths in all file instructions.
            abs_workdir = str(Path(self.config.workdir).resolve())
            if i == 0:
                prompt = (
                    f"IMPORTANT: Create ALL files under {abs_workdir}/ using ABSOLUTE paths.\n"
                    f"Use the terminal tool with commands like: mkdir -p {abs_workdir}/src && cat > {abs_workdir}/src/main.rs << 'EOF'\n"
                    f"Do NOT use relative paths -- they may resolve to the wrong directory.\n\n"
                    f"{self.config.seed_prompt}"
                )
            else:
                project_state = self._gather_project_state()
                prev_summary = self._extract_build_summary(prev_output, i - 1)
                prompt = CONTINUE_TEMPLATE.format(
                    seed=self.config.seed_prompt[:2000],
                    workdir=abs_workdir,
                    project_state=project_state,
                    prev_iteration=i - 1,
                    prev_summary=prev_summary,
                    prev_output=prev_output[:3000],
                    explore_context=explore_context,
                )

            # Run Hermes
            turn = self._run_hermes(i, prompt)
            self.state.turns.append(turn)
            prev_output = turn.output

            # Save snapshot
            if self.config.save_snapshots:
                self._save_snapshot(i, turn)

            # Check for [DONE] on its own line in the AI's actual response.
            # Must be at start of a line, not inside the prompt template text.
            import re
            if re.search(r'^\s*\[DONE\]\s*$', turn.output, re.MULTILINE):
                print(f"  AI declared project done at iteration {i}")
                break

            # Check for [EXPLORE] triggers
            explore_context = ""
            if self.config.explore_enabled:
                question = self._detect_explore_trigger(turn.output)
                if question:
                    print(f"  AI wants to explore: {question[:80]}")
                    branches = self._run_possibilities(question)
                    if branches:
                        branch_text = "\n".join(
                            f"  - {b.get('title', '?')}: {b.get('description', '')[:120]}"
                            for b in branches
                        )
                        explore_context = EXPLORE_INJECT_TEMPLATE.format(
                            explore_results=branch_text
                        )
                        turn.explored = True
                        turn.explore_question = question
                        turn.explore_branches = branches

            # Print progress
            print(f"  Iter {i}: {len(turn.output)} chars, {turn.elapsed_seconds:.0f}s"
                  f"{' [EXPLORED]' if turn.explored else ''}"
                  f"{' [DONE]' if '[DONE]' in turn.output else ''}")

        self.state.final_output = prev_output
        self._save_final()
        return self.state

    def _run_hermes(self, iteration: int, prompt: str) -> BuildTurn:
        """Spawn Hermes subprocess with the prompt. Retries with fallback provider on timeout."""
        start = time.time()

        # NOTE: Do NOT use -Q (quiet mode). It installs a signal handler that
        # crashes when Hermes' skill auto-loader spawns threads. The -Q mode
        # kills the process with KeyboardInterrupt during skill matching for
        # common words like "build", "explorer", "browser". Output is cleaned
        # by _clean_output() which strips ANSI codes and UI artifacts.
        cmd = [self.config.hermes_binary, "chat", "-q", prompt, "-t", ""]
        if self.config.hermes_model:
            cmd.extend(["-m", self.config.hermes_model])
        if self.config.hermes_provider:
            cmd.extend(["--provider", self.config.hermes_provider])

        # Save prompt for debugging
        prompt_file = Path(self.state.output_dir) / f"prompt_{iteration}.txt"
        prompt_file.write_text(prompt)

        output, exit_code = self._exec_hermes(cmd, start)

        # If failed with no meaningful output, try fallback provider.
        # Covers: timeout (-1), API errors (1, 2), crashes, etc.
        # Also retry on very short output (<200 chars) which usually means session
        # recovery grabbed content from the wrong concurrent process.
        if exit_code != 0 and len(output.strip()) < 200 and self.config.retry_provider:
            print(f"  Primary provider failed (exit={exit_code}), retrying with {self.config.retry_provider}...")
            retry_cmd = [self.config.hermes_binary, "chat", "-q", prompt, "-t", ""]
            if self.config.retry_model:
                retry_cmd.extend(["-m", self.config.retry_model])
            retry_cmd.extend(["--provider", self.config.retry_provider])
            output, exit_code = self._exec_hermes(retry_cmd, start)

        # Clean Hermes output (deduplicate boxed + final)
        output = self._clean_output(output)

        elapsed = time.time() - start
        return BuildTurn(
            iteration=iteration,
            prompt=prompt[:500],  # save first 500 chars of prompt
            output=output,
            elapsed_seconds=elapsed,
            hermes_exit_code=exit_code,
        )

    def _exec_hermes(self, cmd: list, run_start: float) -> tuple:
        """Execute a Hermes command. Returns (output, exit_code)."""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.config.iteration_timeout,
                cwd=self.config.workdir,
            )
            output = result.stdout or ""
            exit_code = result.returncode
        except subprocess.TimeoutExpired:
            output = ""
            exit_code = -1
            # Try to recover output from Hermes session DB
            recovered = self._recover_session_output(run_start)
            if recovered:
                print(f"  [RECOVERED {len(recovered)} chars from session DB]")
                output = recovered
        except Exception as e:
            output = f"Error running Hermes: {e}"
            exit_code = -1

        return output, exit_code

    def _recover_session_output(self, started_before: float) -> str:
        """Recover assistant output from Hermes session DB after a timeout.
        
        When Hermes times out, it often has done real work (tool calls, file writes)
        but never finishes its text response. The session DB has all the messages.
        
        Strategy: find sessions started in a narrow window after our subprocess,
        then validate that the session's content is relevant to our project by
        checking if any assistant messages reference our working directory.
        This avoids picking up sessions from concurrent Hermes processes (cron, etc).
        """
        db_path = Path.home() / ".hermes" / "state.db"
        if not db_path.exists():
            return ""
        
        try:
            import sqlite3
            conn = sqlite3.connect(str(db_path))
            conn.row_factory = sqlite3.Row
            
            # Find candidate sessions started within 10s of our subprocess launch.
            # Take the most recent ones -- we'll validate relevance.
            rows = conn.execute(
                "SELECT id, started_at FROM sessions WHERE started_at >= ? - 5 AND started_at <= ? + 120 ORDER BY started_at DESC LIMIT 5",
                (started_before, started_before)
            ).fetchall()
            
            if not rows:
                conn.close()
                return ""
            
            # Get our project path for relevance checking
            proj_path = str(Path(self.config.workdir).resolve())
            proj_name = Path(self.config.workdir).name
            
            # Try each candidate session, newest first
            for session_row in rows:
                session_id = session_row["id"]
                
                # Get the last assistant message with content
                msg_rows = conn.execute(
                    "SELECT content FROM messages WHERE session_id = ? AND role = 'assistant' AND content IS NOT NULL AND content != '' ORDER BY timestamp DESC LIMIT 1",
                    (session_id,)
                ).fetchall()
                
                if not msg_rows or not msg_rows[0]["content"]:
                    continue
                
                content = msg_rows[0]["content"]
                
                # Validate relevance: content mentions our project dir or path
                content_lower = content.lower()
                if proj_name.lower() in content_lower or proj_path in content:
                    conn.close()
                    return content
                
                # Also check tool call messages for our working directory
                tool_rows = conn.execute(
                    "SELECT content FROM messages WHERE session_id = ? AND role = 'tool' AND content IS NOT NULL ORDER BY timestamp DESC LIMIT 5",
                    (session_id,)
                ).fetchall()
                for tr in tool_rows:
                    if proj_path in tr["content"]:
                        conn.close()
                        return content
            
            conn.close()
            return ""
        except Exception:
            return ""

    def _clean_output(self, text: str) -> str:
        """Clean Hermes output -- strip UI artifacts, deduplicate."""
        if not text:
            return ""

        # Remove ANSI escape codes
        text = re.sub(r'\x1b\[[0-9;]*m', '', text)

        # Strip Hermes UI artifacts (box drawing, tool progress)
        lines = text.split("\n")
        cleaned = []
        for line in lines:
            stripped = line.strip()
            if any(p in stripped for p in ["preparing", "┊"]):
                continue
            if stripped.startswith("╭─") or stripped.startswith("╰─"):
                continue
            if stripped and all(c in "╭╮╰╯│─┃┆┊║═" for c in stripped):
                continue
            cleaned.append(line)
        text = "\n".join(cleaned).strip()

        # Hermes dedup: if second half matches first half
        mid = len(text) // 2
        if mid > 100:
            first = text[:mid].strip()
            second = text[mid:].strip()
            overlap = min(200, len(first), len(second))
            if overlap > 50:
                if first[:overlap].replace(" ", "") == second[:overlap].replace(" ", ""):
                    return first

        return text

    def _gather_project_state(self) -> str:
        """Gather current project state for context injection."""
        lines = []
        proj = Path(self.config.workdir)

        # File listing
        files = []
        for root, dirs, filenames in os.walk(proj):
            dirs[:] = [d for d in dirs
                       if d not in {'.git', '__pycache__', 'node_modules', '.venv',
                                    'venv', 'dist', 'build', 'target', '.mypy_cache'}
                       and not d.startswith('rfl_') and not d.startswith('evolve_')]
            for fn in filenames:
                fp = Path(root) / fn
                rel = fp.relative_to(proj)
                files.append((str(rel), fp.stat().st_size))

        if files:
            files.sort(key=lambda x: x[0])
            lines.append(f"Files ({len(files)} total):")
            for path, size in files[:40]:
                lines.append(f"  {path} ({size} bytes)")
            if len(files) > 40:
                lines.append(f"  ... and {len(files) - 40} more")

        # Git log (recent commits)
        try:
            result = subprocess.run(
                ["git", "log", "--oneline", "-5"],
                capture_output=True, text=True, timeout=5,
                cwd=self.config.workdir,
            )
            if result.returncode == 0 and result.stdout.strip():
                lines.append("\nRecent commits:")
                for line in result.stdout.strip().splitlines()[:5]:
                    lines.append(f"  {line}")
        except Exception:
            pass

        # Git diff (uncommitted changes)
        try:
            result = subprocess.run(
                ["git", "diff", "--stat"],
                capture_output=True, text=True, timeout=5,
                cwd=self.config.workdir,
            )
            if result.returncode == 0 and result.stdout.strip():
                lines.append("\nUncommitted changes:")
                lines.append(result.stdout.strip()[:500])
        except Exception:
            pass

        return "\n".join(lines) if lines else "(empty project)"

    def _extract_build_summary(self, output: str, iteration: int) -> str:
        """Extract structured summary from iteration output.
        
        Instead of sending raw output[:6000], pull out the dense signal:
        what files were touched, what tests passed/failed, what was decided,
        and what the AI planned to do next.
        """
        if not output:
            return "(no output from previous iteration)"
        
        parts = []
        parts.append(f"[Iteration {iteration} summary]")
        
        # 1. Extract file operations from output text
        import re
        file_ops = []
        for m in re.finditer(
            r'(?:wrote|created|modified|saved|updated|wrote to|write_file|patch)\s+[`"\']?([^\s`"\',\)]+\.\w+)',
            output, re.IGNORECASE
        ):
            path = m.group(1).strip()
            if path and len(path) < 120 and not any(p in path for p in ['target/', '.git/']):
                file_ops.append(path)
        
        if file_ops:
            seen = set()
            unique = []
            for f in file_ops:
                base = f.split('/')[-1]
                if base not in seen:
                    seen.add(base)
                    unique.append(f)
            parts.append(f"Files touched: {', '.join(unique[:15])}")
        
        # 2. Extract test results
        test_patterns = [
            r'(\d+)\s*(?:/| of | out of )\s*(\d+)\s*(?:tests?|passed|passing)',
            r'test result:.*?(\d+)\s*passed.*?(\d+)\s*failed',
            r'(\d+) passed.*?(\d+) failed',
        ]
        for pat in test_patterns:
            m = re.search(pat, output, re.IGNORECASE)
            if m:
                parts.append(f"Tests: {m.group(0).strip()}")
                break
        
        # 3. Extract build/compile results
        if re.search(r'error\[E\d+\]|error:', output):
            errors = re.findall(r'error(?:\[E\d+\])?:\s*(.+)', output)
            if errors:
                parts.append(f"Build errors: {'; '.join(e.strip()[:80] for e in errors[:3])}")
        elif re.search(r'Compil|Build.*success|Finished', output, re.IGNORECASE):
            parts.append("Build: compiled successfully")
        
        # 4. Key decisions and next intent from commentary
        commentary_lines = []
        for line in output.split('\n'):
            stripped = line.strip()
            if not stripped or stripped.startswith(('┊', '╭', '╰', '│', '●', '---')):
                continue
            if any(p in stripped.lower() for p in ['preparing', 'terminal...', 'review diff']):
                continue
            if len(stripped) > 20:
                commentary_lines.append(stripped)
        
        if commentary_lines:
            first_chunk = ' '.join(commentary_lines[:5])
            if len(first_chunk) > 500:
                first_chunk = first_chunk[:497] + '...'
            parts.append(f"Decisions: {first_chunk}")
            
            last_chunk = ' '.join(commentary_lines[-4:])
            if len(last_chunk) > 500:
                last_chunk = last_chunk[:497] + '...'
            if last_chunk != first_chunk:
                parts.append(f"Next intent: {last_chunk}")
        
        # 5. Git diff summary
        try:
            result = subprocess.run(
                ['git', 'diff', '--stat'],
                capture_output=True, text=True, timeout=5,
                cwd=self.config.workdir,
            )
            if result.returncode == 0 and result.stdout.strip():
                summary_line = [l for l in result.stdout.strip().splitlines() if 'changed' in l]
                if summary_line:
                    parts.append(f"Changes: {summary_line[0].strip()}")
        except Exception:
            pass
        
        summary = '\n'.join(parts)
        if len(summary) > 3000:
            summary = summary[:2997] + '...'
        
        return summary

    def _detect_explore_trigger(self, output: str) -> str:
        """Check if the AI output contains an [EXPLORE: question] trigger."""
        m = re.search(r'\[EXPLORE:\s*(.+?)\]', output)
        if m:
            return m.group(1).strip()
        return ""

    def _run_possibilities(self, question: str) -> list[dict]:
        """Run ai_possibilities to explore the AI's question."""
        try:
            from possibilities.llm import LLMClient
            from possibilities.prompts import BRANCH_PROMPT, get_depth_guidance
            from possibilities.llm import parse_json_response
        except ImportError:
            print("  [possibilities not available, skipping explore]")
            return []

        try:
            client = LLMClient(model=None, temperature=0.9, complexity="fast")
            prompt = BRANCH_PROMPT.format(
                project_context=f"Project at {self.config.workdir}. AI is autonomously building it.",
                seed_question=question,
                depth=0,
                depth_guidance=get_depth_guidance(0),
                n_min=3,
                n_max=self.config.explore_max_branches,
            )
            raw = client.generate(prompt)
            branches = parse_json_response(raw)
            return branches if isinstance(branches, list) else []
        except Exception as e:
            print(f"  [explore failed: {e}]")
            return []

    def _resolve_output_dir(self) -> str:
        if self.config.output_dir:
            return self.config.output_dir
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        return str(Path.cwd() / f"build_{timestamp}")

    def _save_snapshot(self, iteration: int, turn: BuildTurn):
        snap_dir = Path(self.state.output_dir) / "snapshots"
        snap_dir.mkdir(parents=True, exist_ok=True)
        data = {
            "iteration": turn.iteration,
            "explored": turn.explored,
            "explore_question": turn.explore_question,
            "elapsed": turn.elapsed_seconds,
            "hermes_exit_code": turn.hermes_exit_code,
            "output": turn.output,
        }
        if turn.explore_branches:
            data["explore_branches"] = turn.explore_branches
        path = snap_dir / f"iter_{iteration:03d}.json"
        path.write_text(json.dumps(data, indent=2))

    def _save_final(self):
        out = Path(self.state.output_dir)

        # conversation.md
        lines = [f"# Build Run {self.state.id}", ""]
        lines.append(f"Seed: {self.config.seed_prompt[:200]}")
        lines.append(f"Workdir: {self.config.workdir}")
        lines.append(f"Iterations: {len(self.state.turns)}")
        lines.append(f"Time: {self.state.elapsed():.1f}s")
        explored = sum(1 for t in self.state.turns if t.explored)
        if explored:
            lines.append(f"Explored: {explored} iterations")
        lines.append("")

        for turn in self.state.turns:
            lines.append(f"## Iteration {turn.iteration}")
            if turn.explored:
                lines.append(f"*Explored: {turn.explore_question}*")
            lines.append(f"Time: {turn.elapsed_seconds:.1f}s | Exit: {turn.hermes_exit_code}")
            lines.append("")
            lines.append(turn.output)
            lines.append("")
            lines.append("---")
            lines.append("")

        (out / "conversation.md").write_text("\n".join(lines))

        # build_log.jsonl
        with open(out / "build_log.jsonl", "w") as f:
            for turn in self.state.turns:
                entry = {
                    "iteration": turn.iteration,
                    "elapsed": turn.elapsed_seconds,
                    "output_len": len(turn.output),
                    "explored": turn.explored,
                    "explore_question": turn.explore_question,
                    "hermes_exit_code": turn.hermes_exit_code,
                }
                f.write(json.dumps(entry) + "\n")

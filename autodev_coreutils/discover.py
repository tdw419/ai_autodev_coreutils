"""discover -- Find new work by scanning projects, RAG, and codebases.

Scans three sources to discover what needs doing:
  1. ~/zion/projects/ -- find projects with dirty git, incomplete roadmaps, stale work
  2. RAG knowledge base -- search for pending ideas, unfinished features, known gaps
  3. Specific codebases (e.g. Geometry OS) -- check roadmap completeness, open issues

Output: A prioritized list of work items written to .autodev/discovered.md
        and optionally fed into the roadmap/flow pipeline.

Usage:
    autodev-discover                    # scan everything
    autodev-discover --source projects  # only scan ~/zion/projects/
    autodev-discover --source rag       # only search RAG knowledge base
    autodev-discover --source geo       # only check Geometry OS
    autodev-discover --update-roadmap   # write findings into existing roadmap
    autodev-discover --into-flow        # run full flow on best finding
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

try:
    from model_choice import generate as llm_generate
except ImportError:
    llm_generate = None

from .contract import (
    make_parser, find_project, ensure_autodev_dir,
    write_state, write_spec, output, error, EXIT_FAILURE,
)


PROJECTS_DIR = Path(os.environ.get("ZION_PROJECTS", os.path.expanduser("~/zion/projects")))
RAG_DB = Path(os.environ.get("RAG_DB", os.path.expanduser("~/zion/projects/rag/rag/rag.db")))
GEO_OS_DIR = PROJECTS_DIR / "geometry_os" / "geometry_os"


# --- Source 1: Project Scanner ---

def scan_projects(projects_dir: Path = PROJECTS_DIR) -> list[dict]:
    """Scan ~/zion/projects/ for work signals.

    Signals: dirty git, stale commits (no activity in 7+ days with dirty tree),
    ROADMAP.md with incomplete phases, missing AI_GUIDE.md on active projects.
    """
    findings = []

    if not projects_dir.exists():
        return findings

    for project_dir in sorted(projects_dir.iterdir()):
        if not project_dir.is_dir():
            continue
        if project_dir.name.startswith("_") or project_dir.name.startswith("."):
            continue

        info = {
            "project": project_dir.name,
            "path": str(project_dir),
            "signals": [],
            "priority": 0,
        }

        git_dir = project_dir / ".git"
        has_git = git_dir.exists()

        # Signal: dirty working tree
        if has_git:
            try:
                result = subprocess.run(
                    ["git", "status", "--short"],
                    capture_output=True, text=True, timeout=5,
                    cwd=str(project_dir),
                )
                dirty_lines = [l for l in result.stdout.strip().split("\n") if l.strip()]
                if dirty_lines:
                    info["signals"].append(f"dirty git ({len(dirty_lines)} files)")
                    info["priority"] += 2
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass

        # Signal: has ROADMAP.md (worth investigating)
        roadmap = _find_file(project_dir, "ROADMAP.md")
        if roadmap:
            incomplete = _count_incomplete_phases(roadmap)
            if incomplete > 0:
                info["signals"].append(f"roadmap: {incomplete} incomplete phases")
                info["priority"] += 5
            info["roadmap"] = str(roadmap)

        # Signal: recent activity (commits in last 3 days)
        if has_git:
            try:
                result = subprocess.run(
                    ["git", "log", "-1", "--format=%ct"],
                    capture_output=True, text=True, timeout=5,
                    cwd=str(project_dir),
                )
                if result.returncode == 0 and result.stdout.strip():
                    last_ts = int(result.stdout.strip())
                    age_days = (datetime.now().timestamp() - last_ts) / 86400
                    if age_days < 3:
                        info["signals"].append(f"active ({age_days:.1f} days ago)")
                        info["priority"] += 3
                    info["last_commit_days"] = round(age_days, 1)
            except (subprocess.TimeoutExpired, FileNotFoundError, ValueError):
                pass

        # Signal: has NORTH_STAR.md (strategic project)
        if (project_dir / "NORTH_STAR.md").exists():
            info["has_north_star"] = True
            info["priority"] += 1

        # Signal: has AI_GUIDE.md (AI-ready project)
        if (project_dir / "AI_GUIDE.md").exists():
            info["has_ai_guide"] = True
            info["priority"] += 1

        if info["signals"]:
            findings.append(info)

    # Sort by priority descending
    findings.sort(key=lambda x: x["priority"], reverse=True)
    return findings


def _find_file(project_dir: Path, name: str) -> Optional[Path]:
    """Find a file in project root or docs/ subdir."""
    for loc in [project_dir / name, project_dir / "docs" / name]:
        if loc.exists():
            return loc
    return None


def _count_incomplete_phases(roadmap_path: Path) -> int:
    """Count phases that are not COMPLETE/DONE in a roadmap.

    Only counts status rows like: | phase-N Description | STATUS | X/Y |
    Ignores dependency edge rows like: | phase-N | phase-M | soft | ... |
    """
    try:
        text = roadmap_path.read_text()
        lines = text.split("\n")
        incomplete = 0
        for line in lines:
            # Status rows: | phase-N Description | STATUS | X/Y |
            # Must have "phase-" in first cell AND a status in 2nd cell
            if "| phase-" not in line and "| phase " not in line:
                continue
            # Skip dependency edges (3rd column is soft/hard/informs)
            cells = [c.strip() for c in line.split("|")]
            if len(cells) >= 4:
                third = cells[3] if len(cells) > 3 else ""
                if third in ("soft", "hard", "informs", "optional", "required"):
                    continue  # dependency edge, not status row
            # Now check if it's a status row that isn't complete
            if "COMPLETE" not in line and "DONE" not in line:
                incomplete += 1
        return incomplete
    except Exception:
        return 0


# --- Source 2: RAG Knowledge Base ---

def search_rag(query: str, limit: int = 5, db_path: Path = RAG_DB) -> list[dict]:
    """Search the RAG knowledge base for work-related content.

    Calls the RAG query CLI or falls back to direct SQLite + embeddings.
    """
    findings = []

    # Try the MCP-style query tool first (faster, no model loading)
    if db_path.exists():
        try:
            results = _rag_sqlite_search(query, limit, db_path)
            findings.extend(results)
        except Exception:
            pass

    # If we have LLM access, enrich the findings
    if findings and llm_generate:
        try:
            summaries = "\n".join(
                f"[{i+1}] {f.get('concept', 'unknown')}: {f.get('preview', '')[:200]}"
                for i, f in enumerate(findings[:10])
            )
            prompt = f"""Given these research findings, extract actionable work items.
For each item, state: what to do, which project, and why it matters.

Findings:
{summaries}

Output JSON array: [{{"task": "...", "project": "...", "reason": "...", "priority": 1-5}}]
Only output the JSON array, no markdown fences."""

            resp = llm_generate(prompt, complexity="fast")
            items = _parse_json_list(resp)
            for item in items[:5]:
                item["source"] = "rag"
                findings.append(item)
        except Exception:
            pass

    return findings


def _rag_sqlite_search(query_text: str, limit: int, db_path: Path) -> list[dict]:
    """Direct SQLite search against the RAG database.

    Searches both the concept (filename) and explanation (content) fields.
    Handles JSON-encoded content in explanation column.
    """
    import sqlite3

    results = []
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    try:
        # Split query into keywords for broader matching
        keywords = query_text.split()
        conditions = []
        params = []
        for kw in keywords[:5]:  # limit to 5 keywords
            conditions.append("(explanation LIKE ? OR concept LIKE ?)")
            params.extend([f"%{kw}%", f"%{kw}%"])

        where = " OR ".join(conditions)

        rows = conn.execute(
            f"""SELECT concept, domain, explanation, quality_score
               FROM knowledge_vectors
               WHERE {where}
               ORDER BY quality_score DESC
               LIMIT ?""",
            params + [limit],
        ).fetchall()

        for row in rows:
            explanation = row["explanation"]
            try:
                data = json.loads(explanation)
                content = data.get("content", explanation)[:300]
            except (json.JSONDecodeError, TypeError):
                content = explanation[:300]

            results.append({
                "concept": row["concept"],
                "domain": row["domain"],
                "quality": row["quality_score"],
                "preview": content.replace("\n", " "),
                "source": "rag",
            })
    finally:
        conn.close()

    return results


# --- Source 3: Geometry OS Scanner ---

def scan_geo_os(geo_dir: Path = GEO_OS_DIR) -> list[dict]:
    """Check Geometry OS for pending work.

    Looks at: roadmap completeness, test results, open issues, recent changes.
    """
    findings = []

    if not geo_dir.exists():
        return findings

    info = {
        "project": "geometry_os",
        "path": str(geo_dir),
        "signals": [],
        "priority": 0,
    }

    # Check roadmap
    roadmap = _find_file(geo_dir, "ROADMAP.md")
    if roadmap:
        text = roadmap.read_text()
        incomplete = _count_incomplete_phases(roadmap)
        if incomplete > 0:
            info["signals"].append(f"roadmap: {incomplete} incomplete phases")
            info["priority"] += 5
        else:
            info["signals"].append("roadmap: all phases complete (self-heal eligible)")
            info["priority"] += 3

    # Check for test failures
    try:
        result = subprocess.run(
            ["cargo", "test", "--quiet", "--", "--quiet"],
            capture_output=True, text=True, timeout=120,
            cwd=str(geo_dir),
        )
        if result.returncode != 0:
            failed_lines = [l for l in result.stdout.split("\n") if "FAILED" in l or "failures" in l]
            info["signals"].append(f"test failures: {len(failed_lines)} issues")
            info["priority"] += 4
        else:
            # Count passing tests
            passed = result.stdout.count("test result: ok")
            info["signals"].append(f"tests passing")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Check git status
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            capture_output=True, text=True, timeout=5,
            cwd=str(geo_dir),
        )
        dirty = [l for l in result.stdout.strip().split("\n") if l.strip()]
        if dirty:
            info["signals"].append(f"dirty git ({len(dirty)} files)")
            info["priority"] += 2
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Check for recent changes
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ct"],
            capture_output=True, text=True, timeout=5,
            cwd=str(geo_dir),
        )
        if result.returncode == 0 and result.stdout.strip():
            last_ts = int(result.stdout.strip())
            age_days = (datetime.now().timestamp() - last_ts) / 86400
            info["last_commit_days"] = round(age_days, 1)
    except (subprocess.TimeoutExpired, FileNotFoundError, ValueError):
        pass

    # Search RAG for Geometry OS specific work
    geo_rag = search_rag("geometry os feature gap incomplete pending", limit=3)
    if geo_rag:
        info["rag_hints"] = [
            r.get("concept", "") or r.get("preview", "")[:100]
            for r in geo_rag[:3]
        ]
        info["priority"] += 2

    if info["signals"]:
        findings.append(info)

    return findings


# --- Aggregation ---

def discover_all(
    sources: list[str] = None,
    projects_dir: Path = PROJECTS_DIR,
    geo_dir: Path = GEO_OS_DIR,
) -> list[dict]:
    """Run all discovery sources and return prioritized findings."""
    if sources is None:
        sources = ["projects", "rag", "geo"]

    all_findings = []

    if "projects" in sources:
        all_findings.extend(scan_projects(projects_dir))

    if "geo" in sources:
        all_findings.extend(scan_geo_os(geo_dir))

    if "rag" in sources:
        # Use broad queries to find work across the knowledge base
        for query in [
            "pending work incomplete feature gap",
            "next feature to build roadmap",
            "bug fix error failure",
        ]:
            rag_results = search_rag(query, limit=3)
            for r in rag_results:
                r["discovery_source"] = "rag"
                all_findings.append(r)

    # Sort by priority
    all_findings.sort(key=lambda x: x.get("priority", 0), reverse=True)

    # Deduplicate by project/concept + reason
    seen = set()
    unique = []
    for f in all_findings:
        key = (f.get("project", f.get("concept", "")),
               f.get("reason", f.get("preview", ""))[:100])
        if key not in seen:
            seen.add(key)
            unique.append(f)

    return unique


def format_discovery(findings: list[dict]) -> str:
    """Format findings as human-readable markdown."""
    lines = [
        f"# Autodev Discovery Report",
        f"",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Findings: {len(findings)}",
        f"",
    ]

    for i, f in enumerate(findings[:20], 1):
        proj = f.get("project", f.get("concept", "unknown"))
        priority = f.get("priority", 0)
        signals = f.get("signals", [])

        lines.append(f"## {i}. {proj} (priority: {priority})")

        if f.get("path"):
            lines.append(f"- Path: {f['path']}")

        for sig in signals:
            lines.append(f"- {sig}")

        if f.get("roadmap"):
            lines.append(f"- Roadmap: {f['roadmap']}")

        if f.get("rag_hints"):
            lines.append(f"- RAG hints: {'; '.join(f['rag_hints'])}")

        if f.get("reason"):
            lines.append(f"- Why: {f['reason']}")

        if f.get("preview"):
            lines.append(f"- Preview: {f['preview'][:200]}")

        lines.append("")

    return "\n".join(lines)


def _parse_json_list(text: str) -> list[dict]:
    """Parse a JSON array from LLM output."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(l for l in lines if not l.strip().startswith("```"))

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        import re
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match:
            return json.loads(match.group())
        return []


def main(argv=None):
    parser = make_parser("discover", "Find new work by scanning projects, RAG, and codebases")
    parser.add_argument(
        "--source", "-s",
        choices=["projects", "rag", "geo", "all"],
        default="all",
        help="Which source(s) to scan (default: all)",
    )
    parser.add_argument(
        "--limit", "-n", type=int, default=20,
        help="Max findings to report (default: 20)",
    )
    parser.add_argument(
        "--update-roadmap", action="store_true",
        help="Write top findings into .autodev/roadmap.yaml",
    )
    parser.add_argument(
        "--into-flow", action="store_true",
        help="Run autodev flow on the best finding",
    )
    parser.add_argument(
        "--projects-dir",
        default=str(PROJECTS_DIR),
        help=f"Projects directory (default: {PROJECTS_DIR})",
    )

    args = parser.parse_args(argv)
    project = find_project(args.workdir)
    ad = ensure_autodev_dir(project)

    sources = ["projects", "rag", "geo"] if args.source == "all" else [args.source]

    if not args.quiet:
        if args.json_output:
            pass  # skip header in json mode
        else:
            output(f"Autodev Discovery")
            output(f"  Sources: {', '.join(sources)}")
            output(f"  Projects: {args.projects_dir}")
            output("")

    # Run discovery
    findings = discover_all(
        sources=sources,
        projects_dir=Path(args.projects_dir),
    )
    findings = findings[:args.limit]

    if not findings:
        if args.json_output:
            output({"findings": [], "count": 0}, json_mode=True)
        elif not args.quiet:
            output("No work found. Everything looks complete.")
        write_state(project, "discover", {"findings": [], "status": "empty"})
        return 0

    # Write report
    report = format_discovery(findings)
    report_path = write_spec(project, "discovered", report)

    # Write state
    write_state(project, "discover", {
        "findings_count": len(findings),
        "sources": sources,
        "top_projects": [f.get("project", "unknown") for f in findings[:5]],
    })

    if args.json_output:
        output({"findings": findings, "count": len(findings)}, json_mode=True)
    elif not args.quiet:
        output(report)

    # Update roadmap if requested
    if args.update_roadmap and findings:
        _update_roadmap(findings, project)

    # Run flow if requested
    if args.into_flow and findings:
        best = findings[0]
        proj_name = best.get("project", "")
        proj_path = best.get("path", "")
        if proj_path and Path(proj_path).exists():
            from .flow import main_flow
            output(f"\nRunning flow on: {proj_name}")
            return main_flow(
                question=f"What should we work on next for {proj_name}?",
                project_path=proj_path,
                json_mode=args.json_output,
                quiet=args.quiet,
            )

    return 0


def _update_roadmap(findings: list[dict], project: Path):
    """Write top findings into the project's roadmap."""
    try:
        from .adapters import write_roadmap_from_findings
        write_roadmap_from_findings(findings, project)
        if not True:  # quiet check would go here
            output("  Updated roadmap with top findings")
    except Exception as e:
        output(f"  WARNING: Could not update roadmap: {e}")

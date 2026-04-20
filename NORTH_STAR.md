# Autodev Coreutils -- NORTH STAR

## What This Is

Linux coreutils (ls, cat, grep, sed, awk...) share one contract:
they read text from stdin/files, write text to stdout, and exit 0 or 1.
That single contract enables infinite composition via pipes.

**Autodev coreutils is the same idea for AI development automation.**

A set of small CLI tools that share a common data contract,
composable via pipes and the filesystem, that together form the
building blocks of autonomous AI software development.

## The Contract

Every coreutil:
1. Reads a **project directory** (default: `.`)
2. Reads/writes **markdown specs** as the universal interchange format
3. Writes a **status document** to `.autodev/` in the project dir
4. Exits **0** on success, **non-zero** on failure
5. Accepts `--json` flag for machine-readable output
6. Accepts `--quiet` flag for piped composition (errors only)

The filesystem IS the pipe. Markdown IS the format. The `.autodev/`
directory IS the state.

## What's In vs Out

### IN (the coreutils)

These are small, single-purpose tools that do one thing well:

| Tool | Analogy | Purpose | Status |
|------|---------|---------|--------|
| `possibilities` | `ls` | Explore the space of what could be built | EXISTS (installed CLI) |
| `roadmap` | `mkdir -p` | Structure a plan into phases/milestones | EXISTS (installed CLI) |
| `task-split` | `split` | Break one spec into N parallel work items | NEW |
| `context-pack` | `tar` | Bundle exactly the files an agent needs | NEW |
| `diff-apply` | `patch` | Apply a natural-language change description | NEW |
| `verify` | `test` | Verify an agent's claims against files/git | NEW |
| `snapshot` | `checkpoint` | Capture workflow state for resume | NEW |
| `watchdog` | `watch` | Monitor a running agent, intervene on stall | NEW |

### ALSO IN (existing tools to integrate)

| Tool | Role | Status |
|------|------|--------|
| `rfl` | The engine (while/do/done loop) | EXISTS (installed CLI) |
| `model-choice` | Provider selection (env var) | EXISTS (installed CLI) |
| `carry-forward` | Bouncer/gate for session loops | EXISTS (Hermes skill) |
| `keep-or-revert` | Atomic git commit/rollback | EXISTS (Hermes skill) |
| `learnings` | Accumulate knowledge across runs | EXISTS (Hermes skill) |
| `strategist` | Prioritize next work from data | EXISTS (Hermes skill) |

### OUT (different layer)

These are services/daemons, not utilities:
- ai_daemon (systemd layer)
- paperclip (task queue -- more like Redis than a coreutil)
- AIPM dashboard (monitoring)
- Hermes itself (the shell, not a tool)

## Composition Test

```bash
# The dream: pipe everything together
possibilities explore "What should GeoOS do next?" -w ./geo \
  | roadmap build - \
  | task-split --parallel 3 \
  | xargs -I{} sh -c 'context-pack {} | rfl run --from-file -'
```

Today the tools don't share this contract. The project is:
1. Define the contract
2. Write thin wrappers/adapters for existing tools
3. Build the new tools that fill gaps
4. Test that composition actually works

## Design Principles

1. **Filesystem is the API.** No daemon, no server, no database (for coreutils).
2. **Markdown is the format.** Specs, plans, outcomes -- all human-readable markdown.
   JSON only when explicitly requested (`--json`).
3. **One tool, one job.** If a tool does two things, split it.
4. **Exit codes matter.** 0 = success, 1 = failure, 2 = bad args, 3 = timeout.
5. **Composable by default.** Every tool should work alone AND in a pipeline.
6. **No external deps beyond Python stdlib + model_choice.** These need to be portable.

## Target User

Not humans directly (though they can use them). The primary consumer
is OTHER AI agents and automation scripts. If a tool needs a human
to interpret its output, it's not a coreutil.

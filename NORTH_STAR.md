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
| `possibilities` | `ls` | Explore the space of what could be built | PEER DEP (installed from ~/zion/projects/ai_possibilities) |
| `roadmap` | `mkdir -p` | Structure a plan into phases/milestones | PEER DEP (installed from ~/zion/projects/roadmap_builder) |
| `rfl` | `while/do/done` | Iterative self-feeding refinement loop | PEER DEP (installed from ~/zion/projects/recursive_feedback_loop) |
| `model-choice` | `env` | LLM provider selection (shared infra) | PEER DEP (installed from ~/zion/projects/model_choice) |
| `task-split` | `split` | Break one spec into N parallel work items | BUILT-IN |
| `context-pack` | `tar` | Bundle exactly the files an agent needs | BUILT-IN |
| `verify` | `test` | Verify an agent's claims against files/git | BUILT-IN |
| `snapshot` | `checkpoint` | Capture workflow state for resume | BUILT-IN |
|| `watchdog` | `watch` | Monitor a running agent, intervene on stall | BUILT-IN |
|| `decide` | `test` | Pick between options using evidence and LLM judgment | BUILT-IN |
|| `discover` | `find` | Find new work by scanning projects, RAG, codebases | BUILT-IN |

### WHY NOT COPY PEER DEPS IN

These projects have their own repos, tests, release cycles, and development
history. Copying them into coreutils would mean:
- Two copies to maintain, immediately drift
- Breaks their independent iteration
- Bloats this project with code that isn't ours

Instead: coreutils depends on them as peer packages (editable installs),
uses their CLI interfaces, and provides adapters to bridge their formats.
Like Linux -- grep doesn't ship inside sed.

### ALSO IN (pipe adapters + pipeline)

| Component | Purpose | Status |
|-----------|---------|--------|
| `adapters.py` | Bridge between tool formats (possibilities:roadmap, etc) | BUILT-IN |
| `flow.py` | One-shot pipeline: explore->roadmap->split->pack->seed | BUILT-IN |
| `autodev pipe` | CLI for running individual adapters | BUILT-IN |
| `autodev flow` | CLI for running full pipeline | BUILT-IN |

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

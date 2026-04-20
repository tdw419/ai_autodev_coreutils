# Autodev Coreutils -- Usage Guide

This is a set of CLI tools for AI development automation. Think of them like
Linux coreutils (`ls`, `cat`, `grep`, `sort`) but for building software with AI.

One install (`pip install -e .`) gives you every command below.

## The Shared Contract

Every tool follows these rules:

- `-w DIR` or `--workdir DIR` -- which project to operate on (default: `.`)
- `--json` -- machine-readable output (for piping between tools or AI parsing)
- `-q` or `--quiet` -- suppress output, only show errors
- Exit code 0 = success, non-zero = failure
- State goes in `.autodev/` inside the project directory

If you're an AI agent: use `--json` to get structured data you can parse.
Use `-q` when chaining tools so only the final output matters.

---

## The Tools

### 1. `possibilities` -- Explore what to build

Expands a question into a branching tree of possibilities, scored by
"fertility" (how many doors each idea opens). Use this when you don't
know what direction to go.

```bash
# Explore ideas for a project
possibilities explore "What should we build next?" -w ./myproject

# Use fast/cheap model, limit scope
possibilities explore "How to improve error handling?" -w . -c fast --max-nodes 25

# Save tree for later
possibilities explore "..." -w . -o tree.json

# Continue an existing exploration
possibilities resume tree.json -d 4

# Merge multiple exploration trees
possibilities merge tree1.json tree2.json -o merged.json

# Find which ideas keep coming up across branches
possibilities converge tree.json

# Escalate thin branches with stronger models
possibilities escalate tree.json -w .
```

Key flags:
- `-c fast|balanced|thorough|auto` -- model complexity (default: balanced)
- `--max-nodes 25` -- cap tree size (use `fast` + 25 to avoid timeouts)
- `-d N` -- max depth (default: 3)
- `--decay 0.7` -- fertility decay factor
- `-o file.json` -- save tree

Output: Renders a text tree + ranked paths to stdout. Saves JSON tree with `-o`.

### 2. `roadmap` -- Structure a plan

Takes a YAML spec and renders it as a structured roadmap with phases,
deliverables, and tasks.

```bash
# Create a starter roadmap
roadmap init "My Project" -o roadmap.yaml

# Build/render a roadmap
roadmap build roadmap.yaml                    # markdown to stdout
roadmap build roadmap.yaml -f json            # JSON to stdout
roadmap build roadmap.yaml -f yaml -o out.yaml  # YAML to file

# Validate a roadmap
roadmap validate roadmap.yaml

# Show the next actionable task
roadmap next-task roadmap.yaml
```

### 3. `rfl` -- Iterative refinement loop

Runs an AI conversation that feeds its own output back as input. Each
iteration builds on the last. Use this for deep work on a single thread:
audits, bug hunts, feature implementation, code review.

```bash
# Start a loop from a prompt
rfl run "Audit the error handling in src/"

# Start from a file
rfl run --from-file seed_prompt.txt

# Use a template
rfl run --template audit -w /path/to/project -p description="My project"

# List available templates
rfl templates

# Show running instances
rfl list

# Replay a previous run
rfl replay /path/to/run/output
```

Key flags for `rfl run`:
- `-n 5` -- max iterations (default: 10)
- `-b 8000` -- max context tokens per iteration
- `--mode oneshot|session` -- fresh process per iteration vs persistent tmux
- `--strategy sliding_window|rolling_summary|hierarchical` -- compaction
- `--retry-provider gemini` -- which provider to retry on failure
- `--build` -- build mode: structured summaries replace raw output

### 4. `model-choice` -- LLM provider routing

Selects the right LLM for a query based on complexity, cost, and availability.
Other tools use this internally. You can also call it directly.

```bash
# Simple query
model-choice "Explain this function"

# Force complexity tier
model-choice -c fast "What does this code do?"
model-choice -c thorough "Design an architecture for..."

# Use a specific model
model-choice -m anthropic/claude-sonnet-4 "Write tests"

# JSON output
model-choice -j "Explain this error"

# List available models
model-choice --list

# Check rate limits
model-choice --rate-limits
```

### 5. `autodev-task-split` -- Break work into parallel items

Takes a spec or plan and uses an LLM to decompose it into N independently
executable work items.

```bash
# Split a file into 3 tasks
autodev-task-split spec.md -n 3

# Split from a saved spec
autodev-task-split --from-spec plan -n 5

# Pipe from stdin
echo "# Fix all the bugs" | autodev-task-split -n 3 --json

# Include extra context files
autodev-task-split spec.md -n 3 --context-files src/main.py src/utils.py
```

Output: Writes `.autodev/tasks/task_000.md`, `task_001.md`, etc.
Each task has: title, description, files to touch, complexity estimate, dependencies.

### 6. `autodev-context-pack` -- Bundle only relevant files

Reads a task spec, figures out which files in the project are relevant,
and copies just those files to a minimal directory. Saves tokens when
feeding code to an agent.

```bash
# Pack context for a specific task
autodev-context-pack --task 0

# Pack for an ad-hoc spec
autodev-context-pack --spec "Fix the parser error handling"

# Pack from a task file
autodev-context-pack .autodev/tasks/task_000.md

# Custom output location
autodev-context-pack --task 2 -o /tmp/packed/
```

Output: Copies files to `.autodev/pack/` (or `-o` location), preserving directory structure.

### 7. `autodev-verify` -- Check if work actually happened

Takes an agent's "I did X" claim and verifies it against the actual codebase.
Runs tests. Checks git diffs. Uses LLM to assess evidence.

```bash
# Verify a specific claim
autodev-verify --claim "Added error handling to parser.py"

# Just run tests (no LLM)
autodev-verify --test-only

# Specify test command
autodev-verify --test "cargo test" --test-only

# Check a specific git diff
autodev-verify --diff HEAD~2 --claim "Fixed the race condition"
```

Output: PASS or FAIL with evidence. Exit code 0 = pass, 1 = fail.

### 8. `autodev-snapshot` -- Save and restore state

Captures the full `.autodev/` state so you can resume later or rollback.

```bash
# Save a snapshot
autodev-snapshot --tag "before-refactor"

# List all snapshots
autodev-snapshot --list

# Restore a snapshot
autodev-snapshot --restore before-refactor
```

### 9. `autodev-watchdog` -- Monitor a running process

Watches a running agent or command. Kills on timeout, detects stalls,
auto-restarts on failure.

```bash
# Run a command with watchdog
autodev-watchdog --command "rfl run --from-file seed.txt" --timeout 600

# Monitor an existing PID
autodev-watchdog --pid 12345 --timeout 300

# With auto-restart
autodev-watchdog --command "..." --timeout 300 --max-restarts 3
```

---

## The Meta Command: `autodev`

`autodev` is the orchestrator that ties everything together.

```bash
# See all available tools and what's installed
autodev list

# Initialize .autodev/ in a project
autodev init

# Show current project state
autodev status

# Convert between tool formats
autodev pipe possibilities:roadmap tree.json -o roadmap.yaml
autodev pipe roadmap:tasks roadmap.yaml -o spec.md
autodev pipe tasks:rfl-seeds .autodev/tasks/

# Full pipeline: question -> explore -> roadmap -> split -> seeds
autodev flow --question "What should we build next?"
autodev flow --from-tree tree.json
autodev flow --from-roadmap roadmap.yaml -n 5
```

---

## Composing Tools Together

The tools are designed to chain. The filesystem is the pipe, markdown is
the format, `.autodev/` is the state.

### Pattern 1: Explore then execute

```bash
# Explore what to build
possibilities explore "What's the biggest risk?" -w . -o .autodev/tree.json

# Convert top ideas into a roadmap
autodev pipe possibilities:roadmap .autodev/tree.json -o .autodev/roadmap.yaml

# Split roadmap into parallel tasks
autodev-task-split .autodev/roadmap.yaml -n 3 --json

# Generate RFL seeds for each task
autodev pipe tasks:rfl-seeds .autodev/tasks/

# Run each task through RFL
rfl run --from-file .autodev/tasks/seed_task_000.txt -w .
rfl run --from-file .autodev/tasks/seed_task_001.txt -w .
rfl run --from-file .autodev/tasks/seed_task_002.txt -w .
```

### Pattern 2: Snapshot, work, verify

```bash
# Save state before risky changes
autodev-snapshot --tag "before-refactor"

# Run the work
rfl run --template feature -w . -p feature_name="new auth"

# Verify the agent actually did what it said
autodev-verify --claim "Implemented new auth system" --test "python3 -m pytest"

# If it broke, restore
autodev-snapshot --restore before-refactor
```

### Pattern 3: Quick audit

```bash
# One-liner: audit any project
rfl run --template audit -w /path/to/project -p description="the authentication module"
```

---

## The `.autodev/` Directory

When you run `autodev init`, this structure is created:

```
.autodev/
  tasks/                    # task-split output (task_000.md, task_001.md, ...)
  snapshots/                # snapshot archives (snap_<tag>.tar.gz)
  pack/                     # context-pack output (minimal file bundles)
  seed_task_*.txt           # RFL seed prompts (generated by tasks:rfl-seeds)
  possibility_tree.json     # raw exploration tree from possibilities
  roadmap.yaml              # generated or converted roadmap
  *_state.json              # per-tool state files (auto-managed)
```

This directory IS the shared state between tools. Every tool reads from and
writes to it. You can check it into git for team sharing, or gitignore it
for solo projects.

---

## For AI Agents

If you're an AI agent reading this, here's what you need to know:

1. **Always use `--json`** when you plan to parse the output programmatically.
   Every tool supports it.

2. **Always use `-q`** when you're chaining tools and only care about the
   final result. Suppresses intermediate output.

3. **Check exit codes.** 0 = worked, anything else = failed. Don't parse
   output on non-zero exits.

4. **The `.autodev/` directory is your workspace.** Read state files to
   understand what previous tools have done. Write state files to communicate
   with the next tool in the chain.

5. **Start with `autodev init`** on any new project. Creates the directory
   structure everything else expects.

6. **For expensive operations** (possibilities explore, RFL runs), prefer
   `-c fast --max-nodes 25` to avoid timeouts. You can always escalate depth
   later with `possibilities resume`.

7. **Verify your own work** with `autodev-verify`. Don't just claim you did
   something -- run the tests and check the diff.

8. **The pipe adapters bridge tool formats:**
   - `possibilities:roadmap` -- tree JSON -> roadmap YAML
   - `roadmap:tasks` -- roadmap YAML -> markdown spec for task-split
   - `tasks:rfl-seeds` -- task markdown files -> RFL --from-file prompts

9. **model-choice is the LLM layer.** If it's misconfigured, everything that
   uses LLMs will fail. Check with `model-choice --list` first if things
   aren't working.

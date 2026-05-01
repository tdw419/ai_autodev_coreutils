# Hermes Agent Orchestration

Apply patterns from OpenAI Symphony, Harness Engineering, Gas Town, and Archon to the Hermes agent ecosystem. Synthesize research into wiki, map concepts to existing infrastructure, and implement concrete improvements.

**Progress:** 6/16 phases complete, 0 in progress

**Deliverables:** 24/63 complete

**Tasks:** 24/63 complete

## Scope Summary

| Phase | Status | Deliverables | LOC Target | Tests |
|-------|--------|-------------|-----------|-------|
| phase-1 Wiki Synthesis from Symphony Research | COMPLETE | 8/8 | 530 | - |
| phase-2 Map Symphony Patterns to Hermes Infrastructure | COMPLETE | 2/2 | 740 | - |
| phase-3 Close High-Value Gaps with Existing Tools | COMPLETE | 3/3 | 890 | - |
| phase-4 Build Lightweight Symphony-Style Orchestrator | COMPLETE | 4/4 | 1,160 | - |
| phase-5 Archon-Style Deterministic DAG for Hermes | COMPLETE | 4/4 | 1,570 | - |
| phase-6 Gas Town-Style Role Specialization | COMPLETE | 3/3 | 1,780 | - |
| phase-7 Testing and Hardening | PLANNED | 0/4 | 550 | 30 |
| phase-8 Execution History and Observability | PLANNED | 0/4 | 310 | 5 |
| phase-9 Inferential Sensor (LLM-as-Judge Post-Review) | PLANNED | 0/4 | 340 | 5 |
| phase-10 Automated Garbage Collection and Remediation | PLANNED | 0/4 | 350 | 15 |
| phase-11 Workspace Lifecycle Management | PLANNED | 0/4 | 200 | 5 |
| phase-12 Agent-Legible Self-Documentation | PLANNED | 0/3 | 420 | - |
| phase-13 Pull Request Automation | PLANNED | 0/4 | 330 | 10 |
| phase-14 Agent Health Monitoring (Deacon Pattern) | PLANNED | 0/4 | 260 | 10 |
| phase-15 Safety Policies and Approval Gates | PLANNED | 0/4 | 360 | 15 |
| phase-16 Multi-Repo Orchestration | PLANNED | 0/4 | 320 | 10 |

## Dependencies

| From | To | Type | Reason |
|------|----|------|--------|
| phase-1 | phase-2 | informs | Wiki pages from phase 1 provide the reference material for the mapping |
| phase-2 | phase-3 | informs | Gap analysis from phase 2 determines which quick wins to prioritize |
| phase-3 | phase-4 | soft | Quick wins from phase 3 (test gating, AI_GUIDE improvements) make the orchestrator more effective, but not strictly required |
| phase-4 | phase-5 | soft | DAG executor enhances the orchestrator but can also run standalone for manual use |
| phase-5 | phase-6 | soft | Role specialization builds on the DAG executor from phase 5 |
| phase-6 | phase-7 | soft | Tests should cover all the systems built in phases 1-6 |
| phase-7 | phase-8 | soft | Tests should be green before adding observability to avoid logging test noise |
| phase-8 | phase-9 | soft | Review results should be logged to the execution history from phase 8 |
| phase-9 | phase-10 | soft | LLM review sensor from phase 9 can be used to validate auto-fix quality |
| phase-8 | phase-11 | soft | Workspace lifecycle events should be logged to the execution history from phase 8 |
| phase-7 | phase-12 | soft | Documentation should reflect the final tested state of the code, not intermediate versions |
| phase-8 | phase-13 | soft | PR creation events should be logged to the execution history from phase 8 |
| phase-11 | phase-14 | soft | Workspace lifecycle from phase 11 provides the state tracking that health monitoring depends on |
| phase-7 | phase-15 | soft | Approval logic should be tested before deployment |
| phase-8 | phase-15 | soft | Approval events should be logged to the execution history from phase 8 |
| phase-4 | phase-16 | soft | Multi-repo support extends the base orchestrator from phase 4 |
| phase-13 | phase-16 | soft | PR creation from phase 13 should work across multiple repos |
| phase-14 | phase-16 | soft | Health monitoring from phase 14 should cover workers across all repos |
| phase-15 | phase-16 | soft | Approval policies from phase 15 may vary per repo |

## [x] phase-1: Wiki Synthesis from Symphony Research (COMPLETE)

**Goal:** Extract and synthesize all key concepts from the OpenAI Symphony doc into persistent wiki pages

The research doc at ~/zion/docs/research/ covers 6 major concepts that have no wiki
representation yet: Symphony, Harness Engineering, Gas Town, Archon, Ralph Wiggum
pattern, and agent.md spec. Create focused wiki pages for each, cross-referenced
with existing pages. Update the tag taxonomy in SCHEMA.md to include new tags.


### Deliverables

- [x] **Update wiki tag taxonomy** -- Add orchestration, harness-engineering, codex, openai, workflow-dag to SCHEMA.md tag taxonomy
  - [x] `p1.d1.t1` Add orchestration-related tags to SCHEMA.md
    > Add tags: orchestration, harness-engineering, codex, openai, workflow-dag, agent-md under appropriate taxonomy sections
    _Files: ~/wiki/SCHEMA.md_
  - [x] New tags added to SCHEMA.md under appropriate section
    _Validation: grep for each tag in SCHEMA.md_
  _~20 LOC_
- [x] **Symphony wiki page** -- Create concepts/openai-symphony.md covering the orchestration spec, architecture, config params, and issue-tracker-as-control-plane pattern
  - [x] `p1.d2.t1` Create concepts/openai-symphony.md
    > Write wiki page covering Symphony spec mechanics, architecture table, config params, Elixir implementation notes, and 500% PR increase claim
    _Files: ~/wiki/concepts/openai-symphony.md_
  - [x] Page exists with proper frontmatter and 2+ wikilinks
    _Validation: read_file and check links_
  - [x] Covers polling daemon, workspace manager, workflow loader, agent runner, status surface
    _Validation: read page content_
  _~80 LOC_
- [x] **Harness Engineering wiki page** -- Create concepts/harness-engineering.md covering the three-layer hierarchy (inner/outer/orchestrator), dark factory model, application legibility
  - [x] `p1.d3.t1` Create concepts/harness-engineering.md
    > Write wiki page covering the three-layer harness hierarchy, dark factory model (1M LOC, 0% review), application legibility principles, and structural invariants
    _Files: ~/wiki/concepts/harness-engineering.md_
  - [x] Page covers all three harness layers with tooling examples
    _Validation: read page content_
  - [x] Links to Symphony and existing hermes-related pages
    _Validation: check wikilinks_
  _~100 LOC_
- [x] **Gas Town wiki page** -- Create concepts/gas-town.md covering the swarm coordination architecture, Beads state management, and specialized agent roles
  - [x] `p1.d4.t1` Create concepts/gas-town.md
    > Write wiki page covering Gas Town architecture, Beads/Dolt state mgmt, agent role taxonomy, GUPP principle, and Kubernetes comparison
    _Files: ~/wiki/concepts/gas-town.md_
  - [x] Page covers all 6 agent roles (Mayor, Polecat, Deacon, Refinery, Witness, Dog)
    _Validation: read page content_
  _~90 LOC_
- [x] **Archon wiki page** -- Create concepts/archon-deterministic-workflows.md covering YAML DAG pipelines and deterministic vs probabilistic node types
  - [x] `p1.d5.t1` Create concepts/archon-deterministic-workflows.md
    > Write wiki page covering Archon's YAML DAG approach, node types table, harness-vs-brain debate, and CI/CD-style pipeline for agents
    _Files: ~/wiki/concepts/archon-deterministic-workflows.md_
  - [x] Page covers all 4 node types (AI, Bash, Loop, Dependency)
    _Validation: read page content_
  _~70 LOC_
- [x] **Ralph Wiggum pattern wiki page** -- Create concepts/ralph-wiggum-pattern.md covering context management, smart zone, and persistence artifacts
  - [x] `p1.d6.t1` Create concepts/ralph-wiggum-pattern.md
    > Write wiki page covering the Ralph Wiggum loop pattern, context window decay, smart zone concept, git/filesystem persistence, and comparison table
    _Files: ~/wiki/concepts/ralph-wiggum-pattern.md_
  - [x] Page covers context decay problem, fresh-per-iteration solution, stop hooks
    _Validation: read page content_
  _~70 LOC_
- [x] **agent.md spec wiki page** -- Create concepts/agent-md-specification.md covering structure, AAIF adoption, and effective implementation patterns
  - [x] `p1.d7.t1` Create concepts/agent-md-specification.md
    > Write wiki page covering agent.md structure (4 key sections), AAIF adoption, 2500-repo analysis findings
    _Files: ~/wiki/concepts/agent-md-specification.md_
  - [x] Page covers tech stack definition, executable commands, code examples, three-tier boundaries
    _Validation: read page content_
  _~70 LOC_
- [x] **Update wiki index and log** -- Add all new pages to index.md, fix stale ralph-loop entry, append log entry
  - [x] `p1.d8.t1` Update index.md and log.md
    > Add all 6 concept pages to index.md, fix stale ralph-loop entry, append bulk ingest log entry
    _Files: ~/wiki/index.md, ~/wiki/log.md_
  - [x] All 6 new pages appear in index.md under correct section
    _Validation: grep index.md for each page_
  - [x] Stale claude-code-ralph-loop-explained entry removed or fixed
    _Validation: grep index.md_
  _~30 LOC_

### Technical Notes

Use wiki_ingest MCP tool to pull source material from RAG. Track synthesis with wiki_track. Each page must have 2+ wikilinks to other wiki pages.

### Risks

- Some concepts may already have partial coverage in existing pages -- search before creating

## [x] phase-2: Map Symphony Patterns to Hermes Infrastructure (COMPLETE)

**Goal:** Create a comparison document mapping each Symphony/Gas Town/Harness concept to what Hermes already has, identifying gaps

Several patterns from the research doc already exist in Hermes in different forms.
This phase creates a structured mapping and identifies specific gaps to close.


### Deliverables

- [x] **Hermes vs Symphony comparison wiki page** -- Create comparisons/hermes-vs-symphony.md mapping each pattern to Hermes equivalents
  - [x] `p2.d1.t1` Create comparisons/hermes-vs-symphony.md
    > Map these patterns to Hermes equivalents:
    > 1. Issue tracker as control plane -> GitHub Issues skill + Paperclip
    > 2. Workspace isolation -> delegate_task workdir isolation
    > 3. WORKFLOW.md policy engine -> AGENT.md / AI_GUIDE.md
    > 4. Agent runner (Codex) -> delegate_task + acp_command=claude
    > 5. Ralph Wiggum loop -> RFL with carry-forward
    > 6. Outer Harness (guides) -> skills system + AGENT.md
    > 7. Outer Harness (sensors) -> keep-or-revert, code-review skill
    > 8. Orchestrator layer -> cron scheduler + continuous-roadmap-worker
    > 9. Deterministic DAG (Archon) -> no equivalent (GAP)
    > 10. Specialized agent roles (Gas Town) -> partial via delegate-dispatch (GAP)
    > 11. Garbage Collection Loops -> no equivalent (GAP)
    > 12. agent.md spec -> partial via AI_GUIDE.md convention (GAP)
    _Files: ~/wiki/comparisons/hermes-vs-symphony.md_
  - [x] Covers at least 8 pattern mappings with gap analysis
    _Validation: read page, count mappings_
  - [x] Each mapping identifies: Hermes equivalent, maturity level, specific gaps
    _Validation: check table format_
  _~150 LOC_
- [x] **Gap priority ranking** -- Rank identified gaps by implementation effort vs value, produce actionable recommendations
  - [x] `p2.d2.t1` Add gap priority ranking to comparison page (depends: p2.d1.t1)
    > After the mapping table, add a ranked list of gaps with effort/value assessment and specific recommendation for each
    _Files: ~/wiki/comparisons/hermes-vs-symphony.md_
  - [x] Each gap has: description, effort (low/med/high), value (low/med/high), recommendation
    _Validation: read comparison page gap section_
  _~60 LOC_

### Technical Notes

The comparisons/ directory currently has 0 pages -- this will be the first. Make it good as a template.

### Risks

- Some Hermes equivalents may be undocumented -- need to check skills and session history

## [x] phase-3: Close High-Value Gaps with Existing Tools (COMPLETE)

**Goal:** Implement the highest-value gaps identified in phase 2 using existing Hermes infrastructure

Based on the gap analysis, implement quick wins that leverage what's already built.
Focus on: agent.md improvements, garbage collection loops, and outer harness sensors.


### Deliverables

- [x] **AI_GUIDE.md template upgrade** -- Update the ai-guide skill to incorporate agent.md best practices from the research (three-tier boundaries, executable commands, code examples)
  - [x] `p3.d1.t1` Patch ai-guide skill with agent.md best practices
    > Add agent.md spec's 4 key sections as recommended additions to AI_GUIDE.md template: tech stack definition, executable commands, code examples, three-tier boundaries
    _Files: ~/.hermes/skills/software-development/ai-guide/SKILL.md_
  - [x] ai-guide skill includes agent.md structure recommendations
    _Validation: read skill content_
  - [x] Three-tier boundaries (Always/Ask First/Never) included as template section
    _Validation: grep skill for 'three-tier' or 'boundaries'_
  _~40 LOC_
- [x] **Convention garbage collection cron job** -- Create a weekly cron job that scans project codebases for deviations from documented conventions and opens issues or creates tasks
  - [x] `p3.d2.t1` Create garbage collection cron job
    > Create a weekly cron job that reads AI_GUIDE.md from target projects, scans code for convention violations (naming patterns, file structure, missing tests), and reports findings. Start with geometry-os as the target project.
  - [x] Cron job exists and runs weekly
    _Validation: cronjob list_
  - [x] Checks at least 3 convention types (naming, structure, test patterns)
    _Validation: read cron prompt_
  _~30 LOC_
- [x] **Outer harness sensor: automated test gating for delegate_task** -- Create a wrapper pattern/skill that automatically runs tests after delegate_task completion and re-runs on failure (deterministic sensor)
  - [x] `p3.d3.t1` Create delegate-test-gate skill
    > Create a skill that wraps delegate_task with: (1) run task, (2) run tests, (3) if tests fail, re-delegate with test output as context, (4) repeat up to N times. Pattern from outer harness deterministic sensors.
    _Files: ~/.hermes/skills/.archive/delegate-test-gate/SKILL.md_
  - [x] Skill or documented pattern exists for test-after-delegate
    _Validation: skill_view or read skill file_
  - [x] Includes retry-with-context on test failure
    _Validation: read skill content_
  _~80 LOC_

### Technical Notes

These are low-risk changes to existing infrastructure. No new services needed.

### Risks

- Garbage collection cron needs careful scoping to avoid noisy reports

## [x] phase-4: Build Lightweight Symphony-Style Orchestrator (COMPLETE)

**Goal:** Build a Hermes-native orchestrator that uses GitHub Issues as a control plane to drive autonomous coding agents

This is the main build phase. Create an orchestrator that polls GitHub Issues for
tasks, spawns delegate_task workers in isolated workdirs, and manages status
lifecycle. Modeled on Symphony but using Hermes's existing cron + delegate_task
infrastructure instead of Elixir/Codex.


### Deliverables

- [x] **Orchestrator core: issue poller** -- Script that polls GitHub Issues (repo TBD) for issues with specific labels (e.g. 'agent-ready'), returns structured task list
  - [x] `p4.d1.t1` Create issue poller script
    > Python script using gh CLI to poll GitHub Issues. Filter by label 'agent-ready'. Return JSON with issue number, title, body, labels. Skip issues already assigned or closed.
    _Files: ~/zion/projects/agent-orchestration/poller.py_
  - [x] Polls GitHub Issues API via gh CLI
    _Validation: run script, check output_
  - [x] Filters by label, excludes in-progress/completed
    _Validation: test with labeled issues_
  _~80 LOC_
- [x] **Orchestrator core: worker spawner** -- Script that takes an issue from the poller and spawns a delegate_task worker with appropriate context, workdir, and skills
  - [x] `p4.d2.t1` Create worker spawner script (depends: p4.d1.t1)
    > Python script that receives an issue, creates workdir at ~/zion/projects/agent-orchestration/workspaces/ISSUE-NUM, builds prompt from issue title+body+AI_GUIDE.md, calls delegate_task with appropriate toolsets
    _Files: ~/zion/projects/agent-orchestration/spawner.py_
  - [x] Spawns delegate_task with issue context as prompt
    _Validation: test with a real issue_
  - [x] Creates isolated workdir per issue
    _Validation: check workdir creation_
  - [x] Uses acp_command=claude for reasoning tasks
    _Validation: check delegate_task params_
  _~100 LOC_
- [x] **Orchestrator cron integration** -- Wire poller + spawner into a Hermes cron job that runs on a schedule, with concurrency limits
  - [x] `p4.d3.t1` Create orchestrator cron job (depends: p4.d1.t1, p4.d2.t1)
    > Create Hermes cron job that runs the orchestrator loop: poll issues -> filter ready -> spawn workers (up to N concurrent) -> update issue status. Include config for repo, labels, max_concurrent, polling interval.
  - [x] Cron job runs orchestrator on schedule
    _Validation: cronjob list_
  - [x] Respects max_concurrent limit (configurable)
    _Validation: check cron prompt for limit_
  _~40 LOC_
- [x] **Orchestrator status dashboard** -- Simple status command showing active workers, recent completions, queue depth
  - [x] `p4.d4.t1` Create orchestrator status command (depends: p4.d3.t1)
    > CLI command (or script) that reads workspace state and reports: active workers (by issue number), completed issues, failed issues, queue depth. Output as simple terminal table.
    _Files: ~/zion/projects/agent-orchestration/status.sh_
  - [x] Can run from terminal to see orchestrator state
    _Validation: run status command_
  _~50 LOC_

### Technical Notes

Uses gh CLI for GitHub, delegate_task for workers, cron for scheduling. No Elixir, no Codex -- pure Hermes stack. Workspace isolation via delegate_task workdir param. Consider reusing delegate-dispatch skill patterns.

### Risks

- GitHub API rate limits on frequent polling
- delegate_task sessions are synchronous within a turn -- need to handle long-running tasks via background processes or chained cron
- Issue state management race conditions with multiple workers

## [x] phase-5: Archon-Style Deterministic DAG for Hermes (COMPLETE)

**Goal:** Implement a YAML-based DAG runner that forces delegate_task workers through a defined pipeline (plan, implement, test, review, PR)

Archon uses YAML DAGs to make agent workflows deterministic. This phase brings that
pattern to Hermes: define a pipeline as a YAML DAG, execute nodes sequentially,
with AI nodes using delegate_task and bash nodes running tests/lint/git.


### Deliverables

- [x] **DAG YAML schema and parser** -- Define schema for workflow YAML (nodes, edges, node types) and write parser
  - [x] `p5.d1.t1` Create DAG schema and parser
    > Python module with Pydantic/dataclass models for DAG nodes (AI, Bash, Loop, Dependency) and edges. YAML parser that validates the DAG is acyclic. Include a default 'standard-pipeline.yaml' for plan->implement->test->review.
    _Files: ~/zion/projects/agent-orchestration/dag.py_
  - [x] Schema supports AI, Bash, Loop, Dependency node types
    _Validation: parse example YAML_
  _~120 LOC_
- [x] **DAG executor** -- Execute DAG nodes: AI nodes via delegate_task, Bash nodes via terminal, Loop nodes with retry logic
  - [x] `p5.d2.t1` Create DAG executor (depends: p5.d1.t1)
    > Python executor that walks the DAG topologically. AI nodes: build prompt from node config + context, call delegate_task. Bash nodes: run shell command, check exit code. Loop nodes: repeat child until condition met. Dependency nodes: just enforce order. Output results per node.
    _Files: ~/zion/projects/agent-orchestration/executor.py_
  - [x] Executes a simple 3-node pipeline end-to-end
    _Validation: run with example YAML_
  - [x] Stops on Bash node failure (deterministic gate)
    _Validation: test with failing test node_
  _~150 LOC_
- [x] **Standard pipeline template** -- Default workflow YAML for the standard dev pipeline: plan, implement, lint, test, review, commit
  - [x] `p5.d3.t1` Create standard-pipeline.yaml (depends: p5.d1.t1)
    > YAML file defining: AI(plan) -> AI(implement) -> Bash(lint) -> Bash(test) -> Loop(fix-on-failure, max=3) -> AI(review) -> Bash(git commit). Include prompts and shell commands for each node.
    _Files: ~/zion/projects/agent-orchestration/pipelines/standard-pipeline.yaml_
  - [x] Template covers full dev lifecycle with gates
    _Validation: read YAML, trace through nodes_
  _~60 LOC_
- [x] **Integrate DAG with orchestrator (phase 4)** -- Wire DAG executor into the orchestrator so each issue goes through the pipeline
  - [x] `p5.d4.t1` Integrate DAG executor into orchestrator (depends: p4.d3.t1, p5.d2.t1)
    > Modify the orchestrator spawner to use DAG executor with the standard pipeline instead of a single delegate_task call. Each issue becomes a DAG execution.
    _Files: ~/zion/projects/agent-orchestration/spawner.py_
  - [x] Orchestrator spawns DAG executor instead of raw delegate_task
    _Validation: check orchestrator cron prompt_
  _~40 LOC_

### Technical Notes

Keep it simple -- no Phoenix dashboard, no Dolt database. Just YAML + Python + Hermes tools. The DAG runner is a library, not a service.

### Risks

- DAG complexity can grow unbounded -- cap at 10 nodes per pipeline
- Error propagation across nodes needs clear semantics

## [x] phase-6: Gas Town-Style Role Specialization (COMPLETE)

**Goal:** Implement role-based agent specialization where different workers have different prompts, toolsets, and responsibilities

Gas Town assigns specialized roles (Mayor, Polecat, Deacon, etc.) to agents.
This phase brings role specialization to Hermes: define role profiles as skills
or prompt templates, and let the orchestrator assign roles to workers based on
task type.


### Deliverables

- [x] **Role profile system** -- Define agent roles as YAML profiles with prompts, toolsets, and capabilities
  - [x] `p6.d1.t1` Create role profile YAMLs
    > Create roles/ directory with YAML profiles for: implementer (code writing, full tools), reviewer (read-only + suggestions), tester (run tests, report), coordinator (triage, assign, no code changes). Each has: name, description, system_prompt additions, allowed_toolsets, max_turns.
    _Files: ~/zion/projects/agent-orchestration/roles/_
  - [x] At least 4 roles defined (implementer, reviewer, tester, coordinator)
    _Validation: read role YAML files_
  _~100 LOC_
- [x] **Role-aware orchestrator** -- Update orchestrator to match issues to roles based on labels or heuristics
  - [x] `p6.d2.t1` Add role matching to orchestrator (depends: p4.d3.t1, p6.d1.t1)
    > Update spawner.py to select role profile based on issue labels or title heuristics. Pass role-specific prompt additions and toolsets to delegate_task.
    _Files: ~/zion/projects/agent-orchestration/spawner.py_
  - [x] Issues with 'bug' label get tester role, 'feature' gets implementer, etc.
    _Validation: test with labeled issues_
  _~60 LOC_
- [x] **Multi-role pipeline** -- Create a pipeline where different roles handle different stages (implementer writes code, tester validates, reviewer approves)
  - [x] `p6.d3.t1` Create multi-role pipeline YAML (depends: p5.d3.t1, p6.d1.t1)
    > Create a pipeline YAML where: AI(plan, role=coordinator) -> AI(implement, role=implementer) -> Bash(test) -> Loop(fix, role=implementer) -> AI(review, role=reviewer) -> Bash(commit). Requires role field on AI nodes.
    _Files: ~/zion/projects/agent-orchestration/pipelines/team-pipeline.yaml_
  - [x] Pipeline YAML uses different roles for different nodes
    _Validation: read pipeline YAML_
  _~50 LOC_

### Technical Notes

Roles are prompt+toolset profiles, not separate processes. Same delegate_task infrastructure, different configuration. This is the 'Outer Harness' concept -- role profiles ARE guides.

### Risks

- Role matching heuristics may be too simplistic
- Over-specialization can reduce flexibility for novel tasks

## [ ] phase-7: Testing and Hardening (PLANNED)

**Goal:** Add comprehensive tests for the orchestrator system and harden edge cases

The orchestrator, DAG executor, poller, spawner, and role system have no tests. This phase adds unit tests for each module, an integration test that exercises a full pipeline end-to-end, and fixes any bugs discovered during testing. This is a prerequisite for relying on the orchestrator in production.

### Deliverables

- [ ] **Unit tests for DAG parser and executor** -- Test node parsing, topological sort, cycle detection, and all 4 node type executors
  - [ ] `p7.d1.t1` Create test_dag.py with comprehensive unit tests
    > Expand existing test_dag.py (or replace) with tests for: parse_node, parse_pipeline, cycle detection, topological order, entry_nodes, pipeline_to_dict, edge cases (empty pipeline, missing deps, invalid node types, loop children validation)
    _Files: ~/zion/projects/agent-orchestration/test_dag.py_
  - [ ] Test file exists with 10+ test cases covering dag.py
    _Validation: python3 -m pytest test_dag.py -v_
  - [ ] Test file exists with 10+ test cases covering executor.py
    _Validation: python3 -m pytest test_executor.py -v_
  _~150 LOC_
- [ ] **Unit tests for poller, spawner, roles, orchestrator** -- Test each module core functions with mocked gh CLI and filesystem
  - [ ] `p7.d2.t1` Create test_orchestrator_modules.py
    > Mock gh CLI for poller tests. Mock filesystem for spawner tests. Test role matching heuristics. Test orchestrator run_loop with mocked poller/spawner. Cover edge cases: empty issues, max concurrent, no repo configured.
    _Files: ~/zion/projects/agent-orchestration/test_orchestrator_modules.py_
  - [ ] Test file covers poller.py, spawner.py, roles.py with mocked subprocess calls
    _Validation: python3 -m pytest test_orchestrator_modules.py -v_
  _~200 LOC_
- [ ] **End-to-end integration test** -- Test a full pipeline execution from YAML parse through all node types
  - [ ] `p7.d3.t1` Create test_integration.py (depends: p7.d1.t1, p7.d2.t1)
    > Create a test pipeline YAML with all 4 node types. Execute it with the DAGExecutor. Verify: correct execution order, bash node output capture, loop node iteration count, failure propagation, context templating, dry-run mode.
    _Files: ~/zion/projects/agent-orchestration/test_integration.py_
  - [ ] Integration test runs a pipeline YAML through the full executor
    _Validation: python3 -m pytest test_integration.py -v_
  _~120 LOC_
- [ ] **Fix bugs found during testing** -- Address any issues discovered by the test suite
  - [ ] `p7.d4.t1` Fix bugs discovered by test suite (depends: p7.d1.t1, p7.d2.t1, p7.d3.t1)
    > Run the full test suite. Fix any failures in dag.py, executor.py, spawner.py, roles.py, or orchestrator.py. Common areas to check: loop executor variable scoping, template rendering edge cases, role matching fallbacks.
    _Files: ~/zion/projects/agent-orchestration/dag.py, ~/zion/projects/agent-orchestration/executor.py, ~/zion/projects/agent-orchestration/spawner.py, ~/zion/projects/agent-orchestration/roles.py_
  - [ ] All tests pass after fixes
    _Validation: python3 -m pytest -v (all green)_
  _~80 LOC_

### Technical Notes

Use pytest with subprocess mocking for gh CLI. Use tmp_path fixture for filesystem tests. No external dependencies needed beyond pytest.

### Risks

- The executor AI node preparation may be hard to unit test since it outputs delegate_task params rather than executing
- Loop executor has a known variable scoping issue (iteration variable in except clause)

## [ ] phase-8: Execution History and Observability (PLANNED)

**Goal:** Add persistent execution logging so past orchestrator runs can be inspected, debugged, and analyzed

The current system has no execution history. When a pipeline runs, results are printed to stdout and lost. This phase adds a JSON-based execution log that records every pipeline run, every node execution, and every orchestrator loop iteration. Includes a CLI to query past runs. This addresses gap #7 from the comparison page (observability) and is essential for production use.

### Deliverables

- [ ] **Execution log storage** -- JSON-based log that records every pipeline run with timestamps, node results, and context
  - [ ] `p8.d1.t1` Add execution logging to DAGExecutor
    > Create execution_log.py module that creates ~/.orchestrator/logs/ directory, writes one JSON file per run (named by timestamp), stores pipeline name, all node results, duration, context, and final status. Integrate into executor.py run() method.
    _Files: ~/zion/projects/agent-orchestration/execution_log.py, ~/zion/projects/agent-orchestration/executor.py_
  - [ ] Executor writes results to a persistent log file after each run
    _Validation: run executor, check log file exists and contains run data_
  _~100 LOC_
- [ ] **Orchestrator loop logging** -- Log each orchestrator loop iteration (poll results, spawn decisions, worker state)
  - [ ] `p8.d2.t1` Add loop logging to orchestrator.py (depends: p8.d1.t1)
    > Append each run_loop() summary to ~/.orchestrator/logs/loops/YYYY-MM-DD.jsonl (one JSON line per iteration). Include: timestamp, polled count, spawned issues, active workers, skipped reasons.
    _Files: ~/zion/projects/agent-orchestration/orchestrator.py_
  - [ ] Orchestrator appends loop summaries to a daily log file
    _Validation: run orchestrator, check daily log file_
  _~50 LOC_
- [ ] **History query CLI** -- CLI command to list and inspect past execution runs
  - [ ] `p8.d3.t1` Create orch_history.py CLI (depends: p8.d1.t1)
    > Python CLI with subcommands: list (show recent runs with status, pipeline name, duration), show RUN_ID (display full node-by-node results), failed (show only failed runs), stats (summary statistics). Output as formatted terminal table or JSON.
    _Files: ~/zion/projects/agent-orchestration/orch_history.py_
  - [ ] Can list past runs and show details of a specific run
    _Validation: python3 orch_history.py list && python3 orch_history.py show RUN_ID_
  _~120 LOC_
- [ ] **Update status.sh to show recent history** -- Enhance the status dashboard with last N runs summary
  - [ ] `p8.d4.t1` Update status.sh with history section (depends: p8.d3.t1)
    > Add a "Recent Runs" section to status.sh that calls orch_history.py list --last 5 and displays it. Keep the existing worker status section.
    _Files: ~/zion/projects/agent-orchestration/status.sh_
  - [ ] status.sh shows recent execution history alongside worker status
    _Validation: run status.sh, check for history section_
  _~40 LOC_

### Technical Notes

Use JSON Lines format for loop logs (append-friendly). Use one JSON file per pipeline run (easy to inspect). Log directory: ~/.orchestrator/logs/.

### Risks

- Log files could grow large over time -- need rotation or pruning
- Sensitive data in prompts/issue bodies may end up in logs

## [ ] phase-9: Inferential Sensor (LLM-as-Judge Post-Review) (PLANNED)

**Goal:** Implement an LLM-based code review sensor that runs after pipeline completion to assess code quality

The final high-value gap from the comparison page: inferential sensors. After a pipeline completes (code written, tests passing), an LLM-as-judge reviews the git diff for quality, security issues, and adherence to project conventions. This mirrors the Outer Harness inferential sensor pattern from Harness Engineering. The review runs as an optional pipeline node or standalone command.

### Deliverables

- [ ] **LLM review sensor module** -- Python module that runs an LLM review on a git diff and outputs structured feedback
  - [ ] `p9.d1.t1` Create review_sensor.py
    > Create a Python module that reads a git diff, constructs a review prompt with project context (AI_GUIDE.md if available), calls an LLM via delegate_task or subprocess, parses the review response into structured JSON (summary, issues list with severity, verdict: approve/request_changes/block). Include configurable review criteria (security, performance, readability, convention adherence).
    _Files: ~/zion/projects/agent-orchestration/review_sensor.py_
  - [ ] Module can review a git diff and output structured JSON with verdict
    _Validation: python3 review_sensor.py --diff <(git diff)_
  _~150 LOC_
- [ ] **Review sensor as pipeline node type** -- Add REVIEW node type to the DAG executor that runs the LLM review sensor
  - [ ] `p9.d2.t1` Add REVIEW node type to DAG (depends: p9.d1.t1)
    > Add NodeType.REVIEW to dag.py. The review node takes: diff_source (git diff command or file path), review_criteria (list), and threshold (minimum score to pass). Executor calls review_sensor.run_review(). If verdict is block, node fails (stopping the pipeline).
    _Files: ~/zion/projects/agent-orchestration/dag.py, ~/zion/projects/agent-orchestration/executor.py_
  - [ ] Pipeline YAML can include a review node that runs LLM-as-judge
    _Validation: create pipeline with review node, execute it_
  _~80 LOC_
- [ ] **Review pipeline template** -- Pipeline YAML that adds an LLM review gate before the final commit
  - [ ] `p9.d3.t1` Create review-pipeline.yaml (depends: p9.d2.t1)
    > Create pipelines/review-pipeline.yaml based on standard-pipeline.yaml but with a REVIEW node inserted between review (AI) and commit (bash). The review node runs the LLM sensor on the git diff. If blocked, pipeline stops before commit.
    _Files: ~/zion/projects/agent-orchestration/pipelines/review-pipeline.yaml_
  - [ ] Pipeline template exists with review node before commit
    _Validation: read YAML, trace through nodes_
  _~60 LOC_
- [ ] **Review sensor configuration** -- YAML config for review criteria, model selection, and thresholds
  - [ ] `p9.d4.t1` Create review_config.yaml
    > Create review_config.yaml with: default_criteria (security, readability, performance, convention), model (claude-sonnet), max_tokens, threshold_score (0-100), custom_rules (project-specific review rules), and examples of good/bad patterns.
    _Files: ~/zion/projects/agent-orchestration/review_config.yaml_
  - [ ] review_config.yaml exists with sensible defaults
    _Validation: read YAML file_
  _~50 LOC_

### Technical Notes

The review sensor should work both as a pipeline node and as a standalone CLI tool. Use the same delegate_task infrastructure for the LLM call. The review prompt should be structured for reliable JSON output.

### Risks

- LLM-as-judge can be inconsistent -- the structured prompt and criteria need careful design
- Token cost per review -- should be configurable and possibly skippable for simple changes
- Review may produce false positives -- need a way to override or whitelist

## [ ] phase-10: Automated Garbage Collection and Remediation (PLANNED)

**Goal:** Upgrade the convention-scanning cron from phase 3 into an automated remediation system that can fix convention drift, not just report it

The research doc describes "Garbage Collection Loops" as weekly background tasks that scan for deviations from "golden principles" and open targeted refactoring PRs. Phase 3 created a reporting-only cron. This phase upgrades it to a two-mode system: report mode (safe, default) and auto-fix mode (optional, gated by confidence threshold). The system reads AI_GUIDE.md conventions, scans code, and either reports or fixes issues. This is the "self-correcting codebase" concept from the research applied concretely.

### Deliverables

- [ ] **Convention scanner library** -- Reusable Python module that reads AI_GUIDE.md and scans a codebase for convention violations
  - [ ] `p10.d1.t1` Create gc_scanner.py module
    > Python module that: (1) parses AI_GUIDE.md for convention rules, (2) walks a codebase tree, (3) detects violations (naming patterns, file placement, missing tests, import style, deprecated APIs), (4) outputs structured JSON report with file:line:violation:severity. Support --guide flag and --rules flag for custom rule sets.
    _Files: ~/zion/projects/agent-orchestration/gc_scanner.py_
  - [ ] Module can parse AI_GUIDE.md sections and extract rules
    _Validation: python3 gc_scanner.py --guide AI_GUIDE.md --scan ._
  - [ ] Detects at least 5 violation types (naming, structure, imports, missing files, deprecated patterns)
    _Validation: run scanner on test fixtures_
  _~150 LOC_
- [ ] **Auto-fix engine** -- Module that applies automated fixes for high-confidence violations detected by the scanner
  - [ ] `p10.d2.t1` Create gc_autofix.py module (depends: p10.d1.t1)
    > Python module that takes scanner output and applies fixes: rename files/functions to match naming conventions, sort/organize imports, add missing __init__.py, generate test stubs for untested modules. Only apply fixes with confidence >= threshold (default 0.9). Generate a git commit per fix batch with descriptive message. Support --dry-run flag.
    _Files: ~/zion/projects/agent-orchestration/gc_autofix.py_
  - [ ] Can fix at least 3 violation types automatically (naming, imports, missing boilerplate)
    _Validation: run auto-fix on test fixtures, verify corrections_
  _~120 LOC_
- [ ] **GC integration with orchestrator** -- Add GC as a scheduled pipeline that the orchestrator can run on target repos
  - [ ] `p10.d3.t1` Create gc-pipeline.yaml (depends: p10.d1.t1, p10.d2.t1)
    > Create pipelines/gc-pipeline.yaml: Bash(scan) -> AI(triage findings) -> Loop(auto-fix, max=5) -> Bash(commit fixes). The triage node uses an AI to review scan results and decide which are safe to fix. Auto-fix only runs on approved items.
    _Files: ~/zion/projects/agent-orchestration/pipelines/gc-pipeline.yaml_
  - [ ] GC pipeline YAML exists that runs scan -> report -> optional auto-fix
    _Validation: read pipeline YAML_
  _~60 LOC_
- [ ] **Upgrade existing GC cron** -- Update the phase 3 garbage collection cron to use the new scanner instead of ad-hoc checks
  - [ ] `p10.d4.t1` Upgrade GC cron to use scanner module (depends: p10.d1.t1)
    > Update the existing convention-gc cron job prompt to call gc_scanner.py with the target project's AI_GUIDE.md. Keep the weekly schedule. Add optional auto-fix mode gated by a flag.
  - [ ] Cron prompt references gc_scanner.py instead of manual grep/find commands
    _Validation: read cron prompt_
  _~20 LOC_

### Technical Notes

The scanner should be project-agnostic -- it reads AI_GUIDE.md for rules rather than hardcoding conventions. Auto-fix should be conservative: only fix things that are mechanically verifiable (naming, imports, structure), never touch logic.

### Risks

- Auto-fix could introduce subtle bugs if confidence threshold is too low
- Different projects have wildly different conventions -- parser needs to be flexible

## [ ] phase-11: Workspace Lifecycle Management (PLANNED)

**Goal:** Implement workspace cleanup, archival, and the "Dog" role pattern for maintaining orchestrator hygiene

The orchestrator creates isolated workspaces per issue (~/zion/projects/agent-orchestration/workspaces/ISSUE-NUM) but never cleans them up. Over time, disk fills with stale workspaces. Gas Town's "Dog" role handles town-level maintenance and cleanup. This phase implements workspace lifecycle: active -> completed -> archived -> pruned, with configurable retention policies. Also adds the Dog role to the role system for general maintenance tasks.

### Deliverables

- [ ] **Workspace state machine** -- Track workspace lifecycle states and enforce retention policies
  - [ ] `p11.d1.t1` Add workspace state tracking to spawner.py
    > When spawner creates a workspace, write a .workspace.json metadata file with: issue_number, created_at, status (active), role, pipeline. When orchestrator marks an issue complete, update status to completed. Add archive() and prune() functions that move completed workspaces to an archive dir and delete old archives respectively.
    _Files: ~/zion/projects/agent-orchestration/spawner.py, ~/zion/projects/agent-orchestration/workspace_manager.py_
  - [ ] Workspaces have defined states (active, completed, archived, pruned)
    _Validation: check workspace metadata files_
  _~100 LOC_
- [ ] **Dog role profile** -- Add a maintenance role that handles cleanup, health checks, and housekeeping
  - [ ] `p11.d2.t1` Create Dog role profile
    > Create roles/dog.yaml: name=dog, description="Maintenance and cleanup agent", system_prompt focuses on hygiene tasks (archive old workspaces, check disk usage, verify orchestrator health, clean logs), allowed_toolsets=[bash, filesystem], max_turns=5 (short tasks). Include maintenance-specific prompts for common cleanup operations.
    _Files: ~/zion/projects/agent-orchestration/roles/dog.yaml_
  - [ ] Dog role YAML exists with maintenance-focused prompts and toolsets
    _Validation: read roles/dog.yaml_
  _~40 LOC_
- [ ] **Cleanup cron job** -- Scheduled job that archives completed workspaces and prunes old archives
  - [ ] `p11.d3.t1` Create workspace cleanup cron (depends: p11.d1.t1)
    > Create a daily cron that calls workspace_manager.py cleanup --archive-after 7 --prune-after 30. Archives completed workspaces older than 7 days, deletes archives older than 30 days. Reports stats (archived N, pruned N, freed X MB).
    _Files: ~/zion/projects/agent-orchestration/workspace_manager.py_
  - [ ] Cron job runs daily and archives workspaces older than N days
    _Validation: cronjob list_
  _~30 LOC_
- [ ] **Update status.sh with workspace hygiene** -- Show workspace states and disk usage in the status dashboard
  - [ ] `p11.d4.t1` Add workspace section to status.sh (depends: p11.d1.t1)
    > Add a "Workspaces" section to status.sh: active N, completed N, archived N, total disk usage. Call workspace_manager.py stats to get the data.
    _Files: ~/zion/projects/agent-orchestration/status.sh_
  - [ ] status.sh shows workspace counts by state and total disk usage
    _Validation: run status.sh_
  _~30 LOC_

### Technical Notes

Archive = move to ~/.orchestrator/archives/ with timestamp. Prune = delete archived dirs older than threshold. Keep it simple -- no database, just filesystem state + JSON metadata.

### Risks

- Accidentally pruning active workspaces -- need strict age + status checks before deletion
- Archived workspaces may contain useful context for similar future issues -- consider keeping a summary

## [ ] phase-12: Agent-Legible Self-Documentation (PLANNED)

**Goal:** Make the orchestrator project itself follow agent.md best practices, enabling the orchestrator to be maintained and extended by autonomous agents

The research emphasizes "Agent-Legible Software" -- code, tests, docs, and infrastructure all optimized for high-speed autonomous iteration. The orchestrator project has working code but no AI_GUIDE.md, no inline architecture docs, and no structured conventions. This phase makes the orchestrator project "eat its own dog food": create an AI_GUIDE.md that describes the orchestrator's architecture, add docstrings and type hints to all modules, create a CONTRIBUTING.md for agents, and ensure the project can be safely modified by autonomous workers following the same patterns it orchestrates.

### Deliverables

- [ ] **AI_GUIDE.md for orchestrator project** -- Create a comprehensive agent.md/AI_GUIDE.md that enables autonomous agents to work on the orchestrator codebase
  - [ ] `p12.d1.t1` Create AI_GUIDE.md for orchestrator
    > Create ~/zion/projects/agent-orchestration/AI_GUIDE.md following the agent.md spec from the research: (1) Tech Stack: Python 3, YAML, bash, gh CLI, (2) Executable Commands: python3 -m pytest, python3 dag.py --validate, python3 executor.py --pipeline, (3) Code Examples: how to add a new node type, how to add a new role, how to create a pipeline, (4) Three-Tier Boundaries: Always (run tests before commit, use type hints), Ask First (modify YAML schema, change public APIs), Never (delete existing pipelines, modify poller auth).
    _Files: ~/zion/projects/agent-orchestration/AI_GUIDE.md_
  - [ ] AI_GUIDE.md exists with tech stack, commands, architecture overview, and three-tier boundaries
    _Validation: read AI_GUIDE.md_
  _~100 LOC_
- [ ] **Module documentation pass** -- Add docstrings, type hints, and architecture comments to all Python modules
  - [ ] `p12.d2.t1` Add docstrings and type hints to all modules
    > Add comprehensive docstrings to: dag.py (node types, pipeline parsing, validation), executor.py (execution flow, context handling, node executors), poller.py (API interaction, filtering), spawner.py (workspace setup, role assignment), roles.py (role loading, matching), orchestrator.py (main loop, state management). Add type hints to all function signatures. Add module-level docstrings explaining each file's purpose.
    _Files: ~/zion/projects/agent-orchestration/dag.py, ~/zion/projects/agent-orchestration/executor.py, ~/zion/projects/agent-orchestration/poller.py, ~/zion/projects/agent-orchestration/spawner.py, ~/zion/projects/agent-orchestration/roles.py, ~/zion/projects/agent-orchestration/orchestrator.py_
  - [ ] All public functions have docstrings and type annotations
    _Validation: python3 -c "import ast; ..." or manual review_
  _~200 LOC_
- [ ] **Architecture decision record** -- Create an ADR or design doc explaining the orchestrator architecture for future agents
  - [ ] `p12.d3.t1` Create ARCHITECTURE.md (depends: p12.d1.t1)
    > Create ~/zion/projects/agent-orchestration/ARCHITECTURE.md with: (1) ASCII system diagram showing poller -> spawner -> executor -> DAG flow, (2) Data flow description (GitHub Issues -> poller JSON -> spawner workdir -> executor pipeline -> results), (3) Key design decisions (why YAML DAGs, why role profiles, why filesystem-based state), (4) Extension points (how to add node types, roles, pipelines), (5) Comparison to Symphony/Gas Town architecture.
    _Files: ~/zion/projects/agent-orchestration/ARCHITECTURE.md_
  - [ ] ARCHITECTURE.md exists with system diagram, data flow, and design decisions
    _Validation: read ARCHITECTURE.md_
  _~120 LOC_

### Technical Notes

This is a meta-phase -- the orchestrator documenting itself so agents can maintain it. Follow the agent.md spec format exactly since this is the reference implementation for the Hermes ecosystem.

### Risks

- Documentation may drift from code if not kept in sync -- consider adding a doc-check to the test suite

## [ ] phase-13: Pull Request Automation (PLANNED)

**Goal:** Complete the issue-to-PR lifecycle by auto-creating pull requests after successful pipeline execution

Symphony's end-to-end flow is: issue -> workspace -> agent work -> PR. The orchestrator currently stops at "workspace with commits" -- no PR is ever created. This phase closes that gap by adding PR creation after successful pipelines, with metadata linking the PR back to the issue, the role, and the pipeline used. This transforms the orchestrator from a "workspace factory" into a true autonomous development pipeline that mirrors the 500% PR increase reported by OpenAI teams using Symphony.


### Deliverables

- [ ] **PR creator module** -- Python module that creates GitHub PRs after successful pipeline execution with orchestrator metadata
  - [ ] `p13.d1.t1` Create pr_creator.py module
    > Python module that: (1) reads workspace metadata (issue number, role, pipeline, duration from meta.json), (2) creates a feature branch from workspace changes, (3) pushes to remote, (4) creates a GitHub PR via gh CLI with structured body (issue link, role used, pipeline name, duration, test results), (5) labels the PR and links it to the issue. Include --draft flag for draft PRs.
    _Files: ~/zion/projects/agent-orchestration/pr_creator.py_
  - [ ] Module can create a PR from a workspace branch with structured body
    _Validation: python3 pr_creator.py --workspace workspaces/42 --repo owner/repo_
  _~150 LOC_
- [ ] **PR integration with executor pipeline** -- Add a PR step to the standard and team pipelines that runs after successful commit
  - [ ] `p13.d2.t1` Add PR step to pipeline templates (depends: p13.d1.t1)
    > Add a conditional bash node to standard-pipeline.yaml and team-pipeline.yaml that calls pr_creator.py after commit. The step should be gated by a pipeline env var (CREATE_PR=true) so it can be toggled. Include the PR body template as a pipeline env variable.
    _Files: ~/zion/projects/agent-orchestration/pipelines/standard-pipeline.yaml, ~/zion/projects/agent-orchestration/pipelines/team-pipeline.yaml_
  - [ ] Pipeline YAMLs include an optional PR creation step after commit
    _Validation: read pipeline YAML, trace nodes_
  _~60 LOC_
- [ ] **PR lifecycle management** -- Track PR status and auto-close/update when the source issue changes state
  - [ ] `p13.d3.t1` Add PR tracking to workspace metadata (depends: p13.d1.t1)
    > After PR creation, update workspace meta.json with: pr_number, pr_url, pr_state, created_at. Add a function to pr_creator.py that checks PR status (open/merged/closed) and can close a PR when the source issue is closed. Update orchestrator.py run_loop() to check for completed workspaces with open PRs and post a summary comment on the issue.
    _Files: ~/zion/projects/agent-orchestration/pr_creator.py, ~/zion/projects/agent-orchestration/orchestrator.py_
  - [ ] PR metadata stored in workspace includes PR number and URL
    _Validation: check workspace meta.json after PR creation_
  _~80 LOC_
- [ ] **Configurable PR settings** -- YAML config for PR behavior (draft mode, labels, reviewers, branch naming)
  - [ ] `p13.d4.t1` Create pr_config.yaml
    > Create pr_config.yaml with: draft (bool, default false), auto_label (bool, default true), labels (list, e.g. ["auto-generated", "agent"]), reviewers (list, optional), branch_prefix (string, e.g. "orch/"), pr_body_template (multiline string with {{issue_url}}, {{role}}, {{pipeline}}, {{duration}} placeholders), close_on_issue_close (bool, default true).
    _Files: ~/zion/projects/agent-orchestration/pr_config.yaml_
  - [ ] pr_config.yaml exists with sensible defaults
    _Validation: read YAML file_
  _~40 LOC_

### Technical Notes

Uses gh CLI for all GitHub operations (PR create, issue link, label). No GitHub API tokens needed -- relies on gh auth. PR body should be structured for both human and machine readability. Consider adding a "Generated by Hermes Orchestrator" footer.

### Risks

- PRs created by agents may not meet human review standards -- consider always starting in draft mode
- Branch naming collisions if multiple workers create PRs for the same issue
- Pushing to remote requires write access -- need to handle auth errors gracefully

## [ ] phase-14: Agent Health Monitoring (Deacon Pattern) (PLANNED)

**Goal:** Implement the Gas Town Deacon pattern -- a health supervision daemon that monitors running workers, detects stuck agents, and manages resource usage

Gas Town's Deacon role is a "daemon beacon; central health supervisor" that monitors the health of all running agents. Currently the orchestrator can spawn workers but has no way to detect if a worker is stuck, consuming excessive resources, or has silently failed. This phase adds health monitoring: periodic checks on workspace activity, disk usage tracking, timeout detection, and auto-recovery or escalation for unhealthy workers. This is essential for running the orchestrator in production where workers may run for hours.


### Deliverables

- [ ] **Health check module** -- Python module that checks the health of active worker workspaces
  - [ ] `p14.d1.t1` Create health_check.py module
    > Python module that: (1) scans all workspaces with status "in-progress", (2) checks last file modification time (stuck detection), (3) measures disk usage per workspace, (4) checks for zombie processes (optional, via ps), (5) reports health as JSON with per-worker status (healthy, stale, oversized, unknown). Configurable thresholds: stale_after_minutes (default 30), max_disk_mb (default 500). Support --watch flag for continuous monitoring.
    _Files: ~/zion/projects/agent-orchestration/health_check.py_
  - [ ] Module can scan all active workspaces and report health status per worker
    _Validation: python3 health_check.py --all_
  - [ ] Detects stuck workers (no file changes in N minutes)
    _Validation: create a stale workspace, run health check_
  _~120 LOC_
- [ ] **Auto-recovery for stuck workers** -- Automatically detect and handle stuck workers (timeout, escalation, or restart)
  - [ ] `p14.d2.t1` Add auto-recovery logic to health_check.py (depends: p14.d1.t1)
    > Add to health_check.py: (1) when a worker is stale beyond threshold, update its meta.json status to "failed", (2) post a comment on the GitHub issue explaining the timeout, (3) optionally archive the workspace, (4) log the recovery event. Support --auto-recover flag and --escalate flag (create a new issue for human review). Recovery modes: mark-failed (default), archive, retry (re-spawn with reduced max_turns).
    _Files: ~/zion/projects/agent-orchestration/health_check.py_
  - [ ] Stuck workers are detected and marked as failed after timeout
    _Validation: simulate stuck worker, verify detection_
  _~80 LOC_
- [ ] **Health monitoring cron job** -- Scheduled cron job that runs health checks and auto-recovers unhealthy workers
  - [ ] `p14.d3.t1` Create health monitoring cron job (depends: p14.d2.t1)
    > Create a Hermes cron job that runs health_check.py --auto-recover every 15 minutes. Include config for thresholds, notification on failure, and escalation. The cron prompt should read health_config.yaml for settings.
  - [ ] Cron job runs health checks every 15 minutes
    _Validation: cronjob list_
  _~20 LOC_
- [ ] **Health dashboard in status.sh** -- Show worker health status alongside the existing status dashboard
  - [ ] `p14.d4.t1` Add health section to status.sh (depends: p14.d1.t1)
    > Add a "Worker Health" section to status.sh that calls health_check.py and displays: per-worker status (healthy/stale/oversized), disk usage, last activity time, time since spawn. Use color coding if terminal supports it (green=healthy, yellow=stale, red=failed).
    _Files: ~/zion/projects/agent-orchestration/status.sh_
  - [ ] status.sh shows health status per active worker
    _Validation: run status.sh, check for health section_
  _~40 LOC_

### Technical Notes

Health checks are filesystem-based (no need for process monitoring). Stuck detection uses file modification timestamps. Disk usage via du -sb. The Deacon pattern is complementary to the Dog pattern (phase 11): Dog cleans up completed workspaces, Deacon monitors active ones.

### Risks

- Stuck detection threshold is tricky -- too short and you kill slow workers, too long and stuck workers waste resources
- Auto-recovery could lose work if a worker was actually making progress on a long task
- File modification time may not accurately reflect agent activity (agent might be "thinking")

## [ ] phase-15: Safety Policies and Approval Gates (PLANNED)

**Goal:** Add configurable safety policies modeled on Symphony's approval_policy to control when human approval is required before agent actions proceed

Symphony supports three approval modes: untrusted (every action requires approval), on-failure (only failed actions require approval), and never (fully autonomous). The current Hermes orchestrator runs in "never" mode exclusively -- no human checkpoints exist. This is fine for trusted pipelines but risky for production repos, sensitive changes, or new team members. This phase adds configurable approval gates at the pipeline level, node level, and orchestrator level, enabling a spectrum from fully autonomous to fully supervised operation. This is the "Outer Harness" safety layer from Harness Engineering applied to the Hermes orchestrator.


### Deliverables

- [ ] **Approval policy engine** -- Configurable approval modes that gate pipeline execution at defined checkpoints
  - [ ] `p15.d1.t1` Create approval.py module
    > Python module implementing approval policies: (1) ApprovalMode enum (untrusted, on-failure, never), (2) check_approval() function that takes mode, node result, and policy config, returns (approved: bool, reason: str), (3) untrusted mode: every AI node requires approval before proceeding, (4) on-failure mode: only failed bash/test nodes require approval before retry, (5) never mode: no approval needed (current behavior). Include approval_context that captures what needs approval (diff, test output, prompt).
    _Files: ~/zion/projects/agent-orchestration/approval.py_
  - [ ] Support for untrusted, on-failure, and never approval modes
    _Validation: configure each mode, verify behavior_
  _~100 LOC_
- [ ] **APPROVAL node type for DAG** -- Add an APPROVAL node type that pauses pipeline execution until human approval
  - [ ] `p15.d2.t1` Add APPROVAL node type to DAG executor (depends: p15.d1.t1)
    > Add NodeType.APPROVAL to dag.py. The approval node takes: prompt (what the human is approving), timeout (how long to wait before failing), and on_timeout (fail or skip). In executor.py: when an approval node is reached, write a pending approval file to the workspace, post a GitHub comment requesting approval, and poll for an approval file or comment. If approval is granted, continue. If timeout, apply on_timeout behavior. Support --auto-approve flag to bypass for CI.
    _Files: ~/zion/projects/agent-orchestration/dag.py, ~/zion/projects/agent-orchestration/executor.py_
  - [ ] Pipeline YAML can include approval nodes that block until approved
    _Validation: create pipeline with approval node, execute it_
  _~120 LOC_
- [ ] **Approval-safe pipeline template** -- Pipeline YAML that includes approval gates at critical checkpoints
  - [ ] `p15.d3.t1` Create safe-pipeline.yaml with approval gates (depends: p15.d2.t1)
    > Create pipelines/safe-pipeline.yaml based on standard-pipeline.yaml but with APPROVAL nodes inserted: (1) after implement (approve code changes before testing), (2) after review (approve before commit). The approval nodes include context about what changed (file list, diff summary) so the approver can make an informed decision. Include a --mode flag that switches between untrusted and on-failure by changing which approval nodes are active.
    _Files: ~/zion/projects/agent-orchestration/pipelines/safe-pipeline.yaml_
  - [ ] Pipeline template has approval nodes before commit and PR creation
    _Validation: read pipeline YAML_
  _~80 LOC_
- [ ] **Approval audit trail** -- Log all approval decisions with who approved, when, and why
  - [ ] `p15.d4.t1` Add approval logging to approval.py (depends: p15.d1.t1, p8.d1.t1)
    > Append approval events to ~/.orchestrator/logs/approvals.jsonl. Each entry: timestamp, pipeline, node_id, issue_number, decision (approved/rejected/timeout), approver (auto or github_username), reason, context_snapshot (files changed, test results). Add a CLI subcommand to approval.py: audit (show recent approvals), stats (approval rate, average wait time).
    _Files: ~/zion/projects/agent-orchestration/approval.py_
  - [ ] Approval events are logged with timestamp, approver, decision, and context
    _Validation: check log files after approval_
  _~60 LOC_

### Technical Notes

Approval is filesystem-based for simplicity: pending approvals are JSON files in the workspace. For GitHub integration, approvals can be triggered by comments with "/approve" or "/reject" on the issue. The APPROVAL node type is the key innovation -- it makes safety a first-class concept in the DAG, not an external wrapper.

### Risks

- Approval nodes can stall pipelines indefinitely if no one approves -- need timeout and escalation
- Different approval modes for different repos/tasks adds configuration complexity
- Human approval defeats the purpose of autonomous orchestration -- needs to be optional and off by default

## [ ] phase-16: Multi-Repo Orchestration (PLANNED)

**Goal:** Extend the orchestrator to manage tasks across multiple GitHub repositories with per-repo configuration

Symphony and Gas Town both manage multiple repositories simultaneously. The current Hermes orchestrator is hardcoded to a single repo (ORCH_REPO). This phase extends it to support multiple repos with per-repo configuration: different pipelines, roles, AI_GUIDE.md files, approval policies, and cost budgets. Workspaces are organized by repo. The orchestrator polls all configured repos and routes tasks to the appropriate worker configuration. This is the scaling phase that transforms the orchestrator from a single-project tool into a fleet manager.


### Deliverables

- [ ] **Multi-repo configuration** -- Extend orchestrator.yaml to support multiple repos with per-repo settings
  - [ ] `p16.d1.t1` Extend orchestrator.yaml for multi-repo support
    > Redesign orchestrator.yaml to support: repos (list of repo configs), each with: name, url, labels, pipeline, roles_dir, ai_guide_path, approval_mode, max_concurrent, budget_daily. Keep backward compatibility: if "repo" (singular) is set, treat as single-repo mode. Add a validate_config() function to orchestrator.py that checks all repo configs are valid and accessible.
    _Files: ~/zion/projects/agent-orchestration/orchestrator.yaml, ~/zion/projects/agent-orchestration/orchestrator.py_
  - [ ] Config supports repos as a list with per-repo pipeline, roles, labels, and policies
    _Validation: read config YAML_
  _~80 LOC_
- [ ] **Per-repo workspace organization** -- Organize workspaces by repo to avoid collisions and enable repo-specific cleanup
  - [ ] `p16.d2.t1` Update spawner.py for per-repo workspace layout (depends: p16.d1.t1)
    > Change workspace path from workspaces/{issue_number} to workspaces/{repo_name}/{issue_number}. Update spawner.py spawn_worker() to accept repo_name parameter. Update orchestrator.py to pass repo_name when spawning. Update status.sh, health_check.py, and workspace_manager.py to handle the new layout. Add a migration function that moves existing workspaces to the new layout.
    _Files: ~/zion/projects/agent-orchestration/spawner.py, ~/zion/projects/agent-orchestration/orchestrator.py, ~/zion/projects/agent-orchestration/status.sh_
  - [ ] Workspaces are organized as workspaces/{repo_name}/{issue_number}
    _Validation: spawn a worker, check workspace path_
  _~60 LOC_
- [ ] **Multi-repo poller** -- Poll all configured repos and aggregate results into a unified task queue
  - [ ] `p16.d3.t1` Add multi-repo polling to orchestrator.py (depends: p16.d1.t1)
    > Update orchestrator.py run_loop() to iterate over all configured repos, poll each, and aggregate results. Apply per-repo max_concurrent limits. Report per-repo stats in the summary output. Handle repo-specific errors gracefully (one repo failing shouldn't block others). Add --repo flag to filter to a single repo for debugging.
    _Files: ~/zion/projects/agent-orchestration/orchestrator.py_
  - [ ] Single orchestrator loop polls all repos and reports per-repo task counts
    _Validation: run orchestrator with multi-repo config_
  _~80 LOC_
- [ ] **Per-repo cost tracking** -- Track estimated costs per repo and alert when approaching budget limits
  - [ ] `p16.d4.t1` Add cost tracking to orchestrator (depends: p16.d1.t1)
    > Create cost_tracker.py module: (1) estimate token usage per pipeline execution based on node types and turns (AI nodes cost ~10K tokens/turn, bash nodes are free), (2) accumulate daily costs per repo, (3) compare against per-repo budget_daily limit, (4) alert (print warning) when approaching 80% of budget, (5) stop spawning workers when budget is exceeded. Store daily costs in ~/.orchestrator/costs/{repo}/{date}.json. CLI: python3 cost_tracker.py report --period week.
    _Files: ~/zion/projects/agent-orchestration/cost_tracker.py_
  - [ ] Cost report shows per-repo estimated spend with daily totals
    _Validation: run cost report command_
  _~100 LOC_

### Technical Notes

Multi-repo is primarily a configuration and routing change, not a fundamental architecture change. The poller already accepts a repo parameter. The spawner already supports per-task configuration. The main work is in the orchestrator loop (iterate over repos) and workspace layout (add repo prefix). Backward compatibility is important: single-repo mode must continue to work with no config changes.

### Risks

- More repos means more GitHub API calls -- need to respect rate limits across all repos
- Per-repo configuration drift -- different repos may need different orchestrator versions
- Cost tracking is estimates only -- actual token usage depends on the LLM provider and model
- Workspace migration from flat layout to repo-prefixed layout could break existing workspaces

## Global Risks

- Symphony/Gas Town/Archon are all rapidly evolving -- this roadmap may need updates as those projects change
- delegate_task sessions are synchronous and bounded by parent turn -- long-running orchestrator tasks need careful design (background terminals or chained cron)
- GitHub Issues as control plane requires a public or accessible repo -- private repo token management adds complexity
- Token costs for autonomous loops can escalate quickly (Symphony team uses 1B tokens/day) -- need cost awareness in the orchestrator

## Conventions

- Python scripts use python3 (no bare python command on this system)
- GitHub API via gh CLI, not raw curl
- All new code goes to ~/zion/projects/agent-orchestration/
- Skills go to ~/.hermes/skills/ following existing category structure
- Wiki pages follow SCHEMA.md conventions (frontmatter, wikilinks, tag taxonomy)

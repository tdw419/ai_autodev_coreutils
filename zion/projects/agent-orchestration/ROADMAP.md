# Hermes Agent Orchestration

Apply patterns from OpenAI Symphony, Harness Engineering, Gas Town, and Archon to the Hermes agent ecosystem. Synthesize research into wiki, map concepts to existing infrastructure, and implement concrete improvements.

**Progress:** 16/41 phases complete, 0 in progress

**Deliverables:** 65/163 complete

**Tasks:** 64/163 complete

## Scope Summary

| Phase | Status | Deliverables | LOC Target | Tests |
|-------|--------|-------------|-----------|-------|
| phase-1 Wiki Synthesis from Symphony Research | COMPLETE | 8/8 | 530 | - |
| phase-2 Map Symphony Patterns to Hermes Infrastructure | COMPLETE | 2/2 | 740 | - |
| phase-3 Close High-Value Gaps with Existing Tools | COMPLETE | 3/3 | 890 | - |
| phase-4 Build Lightweight Symphony-Style Orchestrator | COMPLETE | 4/4 | 1,160 | - |
| phase-5 Archon-Style Deterministic DAG for Hermes | COMPLETE | 4/4 | 1,570 | - |
| phase-6 Gas Town-Style Role Specialization | COMPLETE | 3/3 | 1,780 | - |
| phase-7 Testing and Hardening | COMPLETE | 4/4 | 550 | 30 |
| phase-8 Execution History and Observability | COMPLETE | 4/4 | 310 | 5 |
| phase-9 Inferential Sensor (LLM-as-Judge Post-Review) | COMPLETE | 4/4 | 340 | 5 |
| phase-10 Automated Garbage Collection and Remediation | COMPLETE | 4/4 | 350 | 15 |
| phase-11 Workspace Lifecycle Management | COMPLETE | 4/4 | 200 | 5 |
| phase-12 Agent-Legible Self-Documentation | COMPLETE | 3/3 | 420 | - |
| phase-13 Pull Request Automation | COMPLETE | 4/4 | 330 | 10 |
| phase-14 Agent Health Monitoring (Deacon Pattern) | COMPLETE | 4/4 | 260 | 10 |
| phase-15 Safety Policies and Approval Gates | COMPLETE | 4/4 | 360 | 15 |
| phase-16 Multi-Repo Orchestration | COMPLETE | 4/4 | 320 | 10 |
| phase-17 Structural Invariants Engine | PLANNED | 2/4 | 390 | 10 |
| phase-18 Agent Self-Debugging and Trace Tools | PLANNED | 0/4 | 320 | 5 |
| phase-19 Continuous Self-Improvement Loop | PLANNED | 0/4 | 380 | 5 |
| phase-20 Context Window Optimization (Smart Zone) | PLANNED | 0/4 | 300 | 5 |
| phase-21 Merge Queue and Conflict Prevention (Refinery Pattern) | PLANNED | 0/4 | 410 | 10 |
| phase-22 Config Hot-Reload and Live Tuning | PLANNED | 0/4 | 270 | 5 |
| phase-23 End-to-End Integration and Real-World Validation | PLANNED | 0/4 | 550 | 15 |
| phase-24 Project Onboarding Bootstrap | PLANNED | 0/4 | 400 | 10 |
| phase-25 Orchestrator Resilience and State Recovery | PLANNED | 0/4 | 380 | 10 |
| phase-26 Work Item Decomposition (Mayor Pattern) | PLANNED | 0/4 | 400 | 10 |
| phase-27 Live Terminal Dashboard (Witness Pattern) | PLANNED | 0/4 | 380 | 5 |
| phase-28 Speculative Execution and Parallel Exploration | PLANNED | 0/4 | 400 | 10 |
| phase-29 Agent Strategy A/B Testing and Analytics | PLANNED | 0/4 | 350 | 10 |
| phase-30 Inter-Agent Communication and Shared State (Beads Pattern) | PLANNED | 0/4 | 380 | 15 |
| phase-31 Self-Verifying Agent Toolkit | PLANNED | 0/4 | 370 | 10 |
| phase-32 Token Cost Tracking and Budget Enforcement | PLANNED | 0/4 | 370 | 10 |
| phase-33 Application Legibility Toolkit | PLANNED | 0/4 | 420 | 10 |
| phase-34 Agent-Generated Tooling | PLANNED | 0/4 | 400 | 10 |
| phase-35 Dark Factory Mode (Full Autonomous Operation) | PLANNED | 0/4 | 410 | 10 |
| phase-36 Dynamic Policy Engine (WORKFLOW.md Loader) | PLANNED | 0/4 | 410 | 12 |
| phase-37 Event-Driven Trigger Mode | PLANNED | 0/4 | 430 | 12 |
| phase-38 Cross-Project Knowledge Transfer | PLANNED | 0/4 | 360 | 12 |
| phase-39 Browser-Based UI Verification (Chrome DevTools Protocol) | PLANNED | 0/4 | 410 | 8 |
| phase-40 Multi-Model Agent Backend Abstraction | PLANNED | 0/4 | 460 | 10 |
| phase-41 Intelligent Scheduling and Priority Queuing (GUPP Enforcement) | PLANNED | 0/4 | 470 | 10 |

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
| phase-20 | phase-21 | soft | Context budgeting ensures merge conflict reports fit in AI node prompts |
| phase-20 | phase-9 | soft | Context budgeting ensures review prompts don't exceed smart zone limits |
| phase-22 | phase-21 | soft | Config hot-reload allows merge queue settings to be tuned without restart |
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
| phase-10 | phase-17 | soft | Structural invariants complement convention scanning from phase 10 -- invariants check architecture, conventions check style |
| phase-5 | phase-17 | soft | Invariant checker runs as a pipeline gate in the DAG executor from phase 5 |
| phase-8 | phase-18 | informs | Trace tools read from the execution logs created by phase 8 |
| phase-7 | phase-18 | soft | Tests should be green before adding debug tooling to avoid noisy traces |
| phase-5 | phase-18 | soft | Debug context injection modifies the executor from phase 5 |
| phase-8 | phase-19 | informs | Self-improvement reads from the execution logs created by phase 8 |
| phase-9 | phase-19 | soft | LLM review results from phase 9 provide additional signal for improvement analysis |
| phase-10 | phase-19 | soft | GC findings from phase 10 can feed into the improvement analysis |
| phase-17 | phase-19 | soft | Invariant violations from phase 17 can be tracked as improvement signals |
| phase-18 | phase-19 | soft | Failure correlation from phase 18 feeds into the pattern analyzer |
| phase-5 | phase-20 | soft | Context budgeting modifies the executor AI node prompt construction from phase 5 |
| phase-8 | phase-20 | soft | Context budget stats are stored in execution logs from phase 8 |
| phase-13 | phase-21 | soft | Merge queue manages PRs created by the PR automation from phase 13 |
| phase-14 | phase-21 | soft | Health monitoring from phase 14 should cover merge queue operations |
| phase-4 | phase-22 | soft | Config hot-reload modifies the orchestrator loop from phase 4 |
| phase-6 | phase-22 | soft | Role profile hot-reload requires the role system from phase 6 |
| phase-19 | phase-22 | soft | Self-improvement auto-tuning benefits from hot-reload to apply changes immediately |
| phase-13 | phase-23 | soft | PR automation from phase 13 is needed for the full issue-to-PR lifecycle test |
| phase-14 | phase-23 | soft | Health monitoring from phase 14 should be included in the integration chain |
| phase-12 | phase-24 | soft | Agent-legible self-documentation from phase 12 defines the AI_GUIDE.md format that onboarding generates |
| phase-4 | phase-24 | soft | Onboarding generates orchestrator config compatible with the orchestrator from phase 4 |
| phase-11 | phase-25 | soft | Workspace lifecycle from phase 11 provides the state tracking that resilience builds on |
| phase-8 | phase-25 | soft | Execution history from phase 8 should record checkpoint and recovery events |
| phase-23 | phase-25 | soft | Integration validation from phase 23 ensures resilience works with the full system |
| phase-4 | phase-26 | soft | Decomposition extends the orchestrator poller-spawner loop from phase 4 |
| phase-6 | phase-26 | soft | Sub-issues may benefit from different role assignments based on sub-task type |
| phase-13 | phase-26 | soft | Sub-issue PRs should link back to parent issue for end-to-end traceability |
| phase-8 | phase-27 | soft | Dashboard reads execution history from phase 8 for the recent panel |
| phase-14 | phase-27 | soft | Health check data from phase 14 feeds the system panel |
| phase-25 | phase-27 | soft | Pipeline checkpoints from phase 25 enable DAG progress visualization |
| phase-6 | phase-28 | soft | Role specialization from phase 6 provides the different agent profiles for each strategy |
| phase-16 | phase-28 | soft | Per-repo cost tracking from phase 16 is needed to budget speculative execution |
| phase-19 | phase-28 | soft | Self-improvement data from phase 19 helps identify which strategies perform best over time |
| phase-11 | phase-28 | soft | Workspace lifecycle from phase 11 handles archival of non-winning speculative workspaces |
| phase-8 | phase-29 | informs | Analytics reads execution logs created by phase 8 |
| phase-19 | phase-29 | soft | Self-improvement analysis from phase 19 can incorporate A/B testing data |
| phase-27 | phase-29 | soft | Dashboard from phase 27 provides the visualization surface for analytics |
| phase-28 | phase-29 | soft | Speculative execution from phase 28 generates the A/B comparison data |
| phase-4 | phase-30 | soft | Shared state extends the orchestrator''s worker management from phase 4 |
| phase-21 | phase-30 | soft | Merge queue from phase 21 handles post-completion conflicts; shared state handles pre-completion coordination |
| phase-14 | phase-30 | soft | Health monitoring from phase 14 can use shared state to detect stale workers |
| phase-16 | phase-30 | soft | Multi-repo orchestration from phase 16 needs cross-repo coordination |
| phase-5 | phase-31 | soft | VERIFY node type extends the DAG executor from phase 5 |
| phase-7 | phase-31 | soft | Verification tests should be covered by the test suite from phase 7 |
| phase-8 | phase-32 | soft | Cost data should be stored alongside execution logs from phase 8 |
| phase-22 | phase-32 | soft | Budget limits should be configurable via hot-reload from phase 22 |
| phase-28 | phase-32 | soft | Speculative execution from phase 28 multiplies costs -- budget enforcement is critical |
| phase-10 | phase-33 | soft | Legibility checks complement convention scanning from phase 10 GC |
| phase-17 | phase-33 | soft | Structural invariants from phase 17 and architecture linting from phase 33 are complementary -- invariants check rules, legibility checks understandability |
| phase-24 | phase-33 | soft | Project onboarding from phase 24 benefits from architecture analysis |
| phase-5 | phase-34 | soft | GENERATED_TOOL node type extends the DAG executor from phase 5 |
| phase-10 | phase-34 | soft | GC findings from phase 10 can inform what custom tools to generate |
| phase-19 | phase-34 | soft | Self-improvement analysis from phase 19 can identify which generated tools are most effective |
| phase-33 | phase-34 | soft | Legibility analysis from phase 33 identifies patterns that need custom tooling |
| phase-9 | phase-35 | soft | Inferential sensor from phase 9 provides the LLM review signal for confidence scoring |
| phase-15 | phase-35 | soft | Safety policies from phase 15 define the approval gates that confidence scoring replaces or augments |
| phase-17 | phase-35 | soft | Structural invariants from phase 17 provide the architecture compliance signal |
| phase-23 | phase-35 | soft | E2E validation from phase 23 should validate the dark factory pipeline |
| phase-31 | phase-35 | soft | Self-verification toolkit from phase 31 provides the verification gates |
| phase-32 | phase-35 | soft | Cost tracking from phase 32 provides the cost efficiency signal |
| phase-33 | phase-35 | soft | Legibility scoring from phase 33 provides the codebase quality signal |
| phase-34 | phase-35 | soft | Agent-generated tooling from phase 34 provides custom validation signals |
| phase-4 | phase-36 | soft | Policy engine extends the orchestrator loop from phase 4 |
| phase-5 | phase-36 | soft | Pipeline selection from policy overrides the DAG executor from phase 5 |
| phase-6 | phase-36 | soft | Role profiles from phase 6 can be overridden by per-label policy |
| phase-12 | phase-36 | soft | Agent-legible documentation from phase 12 is enhanced by dynamic policy loading |
| phase-24 | phase-36 | soft | Onboarding bootstrap from phase 24 can generate initial workflow policies |
| phase-4 | phase-37 | soft | Event triggers extend the orchestrator loop from phase 4 |
| phase-25 | phase-37 | soft | Resilience from phase 25 should handle webhook server crashes |
| phase-8 | phase-38 | soft | Knowledge extraction reads execution logs from phase 8 |
| phase-16 | phase-38 | soft | Multi-repo orchestration from phase 16 provides the cross-project context where knowledge transfer is most valuable |
| phase-20 | phase-38 | soft | Context optimization from phase 20 should account for knowledge injection in context window management |
| phase-30 | phase-38 | soft | Inter-agent communication from phase 30 provides the notification channel for knowledge sharing |
| phase-5 | phase-39 | soft | BROWSER node type extends the DAG executor from phase 5 |
| phase-7 | phase-39 | hard | Tests should cover browser verification before production use |
| phase-31 | phase-39 | soft | Self-verification toolkit from phase 31 provides the verification framework that browser nodes extend |
| phase-5 | phase-40 | soft | Backend abstraction modifies the executor AI node execution from phase 5 |
| phase-6 | phase-40 | soft | Role profiles from phase 6 inform per-role backend routing rules |
| phase-32 | phase-40 | soft | Cost tracking from phase 32 provides the cost data that backend routing optimizes |
| phase-29 | phase-40 | soft | A/B testing analytics from phase 29 can compare backend performance |
| phase-4 | phase-41 | soft | Priority queue modifies the orchestrator poller-spawner loop from phase 4 |
| phase-6 | phase-41 | soft | Role specialization from phase 6 affects which issues get which workers |
| phase-14 | phase-41 | soft | Health monitoring from phase 14 should track scheduling latency |
| phase-37 | phase-41 | soft | Webhook triggers from phase 37 should jump the priority queue |

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

## [x] phase-7: Testing and Hardening (COMPLETE)

**Goal:** Add comprehensive tests for the orchestrator system and harden edge cases

The orchestrator, DAG executor, poller, spawner, and role system have no tests. This phase adds unit tests for each module, an integration test that exercises a full pipeline end-to-end, and fixes any bugs discovered during testing. This is a prerequisite for relying on the orchestrator in production.

### Deliverables

- [x] **Unit tests for DAG parser and executor** -- Test node parsing, topological sort, cycle detection, and all 4 node type executors
  - [x] `p7.d1.t1` Create test_dag.py with comprehensive unit tests
    > Expand existing test_dag.py (or replace) with tests for: parse_node, parse_pipeline, cycle detection, topological order, entry_nodes, pipeline_to_dict, edge cases (empty pipeline, missing deps, invalid node types, loop children validation)
    _Files: ~/zion/projects/agent-orchestration/test_dag.py_
  - [x] Test file exists with 10+ test cases covering dag.py
    _Validation: python3 -m pytest test_dag.py -v_
  - [x] Test file exists with 10+ test cases covering executor.py
    _Validation: python3 -m pytest test_executor.py -v_
  _~150 LOC_
- [x] **Unit tests for poller, spawner, roles, orchestrator** -- Test each module core functions with mocked gh CLI and filesystem
  - [x] `p7.d2.t1` Create test_orchestrator_modules.py
    > Mock gh CLI for poller tests. Mock filesystem for spawner tests. Test role matching heuristics. Test orchestrator run_loop with mocked poller/spawner. Cover edge cases: empty issues, max concurrent, no repo configured.
    _Files: ~/zion/projects/agent-orchestration/test_orchestrator_modules.py_
  - [x] Test file covers poller.py, spawner.py, roles.py with mocked subprocess calls
    _Validation: python3 -m pytest test_orchestrator_modules.py -v_
  _~200 LOC_
- [x] **End-to-end integration test** -- Test a full pipeline execution from YAML parse through all node types
  - [x] `p7.d3.t1` Create test_integration.py (depends: p7.d1.t1, p7.d2.t1)
    > Create a test pipeline YAML with all 4 node types. Execute it with the DAGExecutor. Verify: correct execution order, bash node output capture, loop node iteration count, failure propagation, context templating, dry-run mode.
    _Files: ~/zion/projects/agent-orchestration/test_integration.py_
  - [x] Integration test runs a pipeline YAML through the full executor
    _Validation: python3 -m pytest test_integration.py -v_
  _~120 LOC_
- [x] **Fix bugs found during testing** -- Address any issues discovered by the test suite
  - [x] `p7.d4.t1` Fix bugs discovered by test suite (depends: p7.d1.t1, p7.d2.t1, p7.d3.t1)
    > Run the full test suite. Fix any failures in dag.py, executor.py, spawner.py, roles.py, or orchestrator.py. Common areas to check: loop executor variable scoping, template rendering edge cases, role matching fallbacks.
    _Files: ~/zion/projects/agent-orchestration/dag.py, ~/zion/projects/agent-orchestration/executor.py, ~/zion/projects/agent-orchestration/spawner.py, ~/zion/projects/agent-orchestration/roles.py_
  - [x] All tests pass after fixes
    _Validation: python3 -m pytest -v (all green)_
  _~80 LOC_

### Technical Notes

Use pytest with subprocess mocking for gh CLI. Use tmp_path fixture for filesystem tests. No external dependencies needed beyond pytest.

### Risks

- The executor AI node preparation may be hard to unit test since it outputs delegate_task params rather than executing
- Loop executor has a known variable scoping issue (iteration variable in except clause)

## [x] phase-8: Execution History and Observability (COMPLETE)

**Goal:** Add persistent execution logging so past orchestrator runs can be inspected, debugged, and analyzed

The current system has no execution history. When a pipeline runs, results are printed to stdout and lost. This phase adds a JSON-based execution log that records every pipeline run, every node execution, and every orchestrator loop iteration. Includes a CLI to query past runs. This addresses gap #7 from the comparison page (observability) and is essential for production use.

### Deliverables

- [x] **Execution log storage** -- JSON-based log that records every pipeline run with timestamps, node results, and context
  - [x] `p8.d1.t1` Add execution logging to DAGExecutor
    > Create execution_log.py module that creates ~/.orchestrator/logs/ directory, writes one JSON file per run (named by timestamp), stores pipeline name, all node results, duration, context, and final status. Integrate into executor.py run() method.
    _Files: ~/zion/projects/agent-orchestration/execution_log.py, ~/zion/projects/agent-orchestration/executor.py_
  - [x] Executor writes results to a persistent log file after each run
    _Validation: run executor, check log file exists and contains run data_
  _~100 LOC_
- [x] **Orchestrator loop logging** -- Log each orchestrator loop iteration (poll results, spawn decisions, worker state)
  - [x] `p8.d2.t1` Add loop logging to orchestrator.py (depends: p8.d1.t1)
    > Append each run_loop() summary to ~/.orchestrator/logs/loops/YYYY-MM-DD.jsonl (one JSON line per iteration). Include: timestamp, polled count, spawned issues, active workers, skipped reasons.
    _Files: ~/zion/projects/agent-orchestration/orchestrator.py_
  - [x] Orchestrator appends loop summaries to a daily log file
    _Validation: run orchestrator, check daily log file_
  _~50 LOC_
- [x] **History query CLI** -- CLI command to list and inspect past execution runs
  - [x] `p8.d3.t1` Create orch_history.py CLI (depends: p8.d1.t1)
    > Python CLI with subcommands: list (show recent runs with status, pipeline name, duration), show RUN_ID (display full node-by-node results), failed (show only failed runs), stats (summary statistics). Output as formatted terminal table or JSON.
    _Files: ~/zion/projects/agent-orchestration/orch_history.py_
  - [x] Can list past runs and show details of a specific run
    _Validation: python3 orch_history.py list && python3 orch_history.py show RUN_ID_
  _~120 LOC_
- [x] **Update status.sh to show recent history** -- Enhance the status dashboard with last N runs summary
  - [x] `p8.d4.t1` Update status.sh with history section (depends: p8.d3.t1)
    > Add a "Recent Runs" section to status.sh that calls orch_history.py list --last 5 and displays it. Keep the existing worker status section.
    _Files: ~/zion/projects/agent-orchestration/status.sh_
  - [x] status.sh shows recent execution history alongside worker status
    _Validation: run status.sh, check for history section_
  _~40 LOC_

### Technical Notes

Use JSON Lines format for loop logs (append-friendly). Use one JSON file per pipeline run (easy to inspect). Log directory: ~/.orchestrator/logs/.

### Risks

- Log files could grow large over time -- need rotation or pruning
- Sensitive data in prompts/issue bodies may end up in logs

## [x] phase-9: Inferential Sensor (LLM-as-Judge Post-Review) (COMPLETE)

**Goal:** Implement an LLM-based code review sensor that runs after pipeline completion to assess code quality

The final high-value gap from the comparison page: inferential sensors. After a pipeline completes (code written, tests passing), an LLM-as-judge reviews the git diff for quality, security issues, and adherence to project conventions. This mirrors the Outer Harness inferential sensor pattern from Harness Engineering. The review runs as an optional pipeline node or standalone command.

### Deliverables

- [x] **LLM review sensor module** -- Python module that runs an LLM review on a git diff and outputs structured feedback
  - [x] `p9.d1.t1` Create review_sensor.py
    > Create a Python module that reads a git diff, constructs a review prompt with project context (AI_GUIDE.md if available), calls an LLM via delegate_task or subprocess, parses the review response into structured JSON (summary, issues list with severity, verdict: approve/request_changes/block). Include configurable review criteria (security, performance, readability, convention adherence).
    _Files: ~/zion/projects/agent-orchestration/review_sensor.py_
  - [x] Module can review a git diff and output structured JSON with verdict
    _Validation: python3 review_sensor.py --diff <(git diff)_
  _~150 LOC_
- [x] **Review sensor as pipeline node type** -- Add REVIEW node type to the DAG executor that runs the LLM review sensor
  - [x] `p9.d2.t1` Add REVIEW node type to DAG (depends: p9.d1.t1)
    > Add NodeType.REVIEW to dag.py. The review node takes: diff_source (git diff command or file path), review_criteria (list), and threshold (minimum score to pass). Executor calls review_sensor.run_review(). If verdict is block, node fails (stopping the pipeline).
    _Files: ~/zion/projects/agent-orchestration/dag.py, ~/zion/projects/agent-orchestration/executor.py_
  - [x] Pipeline YAML can include a review node that runs LLM-as-judge
    _Validation: create pipeline with review node, execute it_
  _~80 LOC_
- [x] **Review pipeline template** -- Pipeline YAML that adds an LLM review gate before the final commit
  - [x] `p9.d3.t1` Create review-pipeline.yaml (depends: p9.d2.t1)
    > Create pipelines/review-pipeline.yaml based on standard-pipeline.yaml but with a REVIEW node inserted between review (AI) and commit (bash). The review node runs the LLM sensor on the git diff. If blocked, pipeline stops before commit.
    _Files: ~/zion/projects/agent-orchestration/pipelines/review-pipeline.yaml_
  - [x] Pipeline template exists with review node before commit
    _Validation: read YAML, trace through nodes_
  _~60 LOC_
- [x] **Review sensor configuration** -- YAML config for review criteria, model selection, and thresholds
  - [x] `p9.d4.t1` Create review_config.yaml
    > Create review_config.yaml with: default_criteria (security, readability, performance, convention), model (claude-sonnet), max_tokens, threshold_score (0-100), custom_rules (project-specific review rules), and examples of good/bad patterns.
    _Files: ~/zion/projects/agent-orchestration/review_config.yaml_
  - [x] review_config.yaml exists with sensible defaults
    _Validation: read YAML file_
  _~50 LOC_

### Technical Notes

The review sensor should work both as a pipeline node and as a standalone CLI tool. Use the same delegate_task infrastructure for the LLM call. The review prompt should be structured for reliable JSON output.

### Risks

- LLM-as-judge can be inconsistent -- the structured prompt and criteria need careful design
- Token cost per review -- should be configurable and possibly skippable for simple changes
- Review may produce false positives -- need a way to override or whitelist

## [x] phase-10: Automated Garbage Collection and Remediation (COMPLETE)

**Goal:** Upgrade the convention-scanning cron from phase 3 into an automated remediation system that can fix convention drift, not just report it

The research doc describes "Garbage Collection Loops" as weekly background tasks that scan for deviations from "golden principles" and open targeted refactoring PRs. Phase 3 created a reporting-only cron. This phase upgrades it to a two-mode system: report mode (safe, default) and auto-fix mode (optional, gated by confidence threshold). The system reads AI_GUIDE.md conventions, scans code, and either reports or fixes issues. This is the "self-correcting codebase" concept from the research applied concretely.

### Deliverables

- [x] **Convention scanner library** -- Reusable Python module that reads AI_GUIDE.md and scans a codebase for convention violations
  - [x] `p10.d1.t1` Create gc_scanner.py module
    > Python module that: (1) parses AI_GUIDE.md for convention rules, (2) walks a codebase tree, (3) detects violations (naming patterns, file placement, missing tests, import style, deprecated APIs), (4) outputs structured JSON report with file:line:violation:severity. Support --guide flag and --rules flag for custom rule sets.
    _Files: ~/zion/projects/agent-orchestration/gc_scanner.py_
  - [x] Module can parse AI_GUIDE.md sections and extract rules
    _Validation: python3 gc_scanner.py --guide AI_GUIDE.md --scan ._
  - [x] Detects at least 5 violation types (naming, structure, imports, missing files, deprecated patterns)
    _Validation: run scanner on test fixtures_
  _~150 LOC_
- [x] **Auto-fix engine** -- Module that applies automated fixes for high-confidence violations detected by the scanner
  - [x] `p10.d2.t1` Create gc_autofix.py module (depends: p10.d1.t1)
    > Python module that takes scanner output and applies fixes: rename files/functions to match naming conventions, sort/organize imports, add missing __init__.py, generate test stubs for untested modules. Only apply fixes with confidence >= threshold (default 0.9). Generate a git commit per fix batch with descriptive message. Support --dry-run flag.
    _Files: ~/zion/projects/agent-orchestration/gc_autofix.py_
  - [x] Can fix at least 3 violation types automatically (naming, imports, missing boilerplate)
    _Validation: run auto-fix on test fixtures, verify corrections_
  _~120 LOC_
- [x] **GC integration with orchestrator** -- Add GC as a scheduled pipeline that the orchestrator can run on target repos
  - [x] `p10.d3.t1` Create gc-pipeline.yaml (depends: p10.d1.t1, p10.d2.t1)
    > Create pipelines/gc-pipeline.yaml: Bash(scan) -> AI(triage findings) -> Loop(auto-fix, max=5) -> Bash(commit fixes). The triage node uses an AI to review scan results and decide which are safe to fix. Auto-fix only runs on approved items.
    _Files: ~/zion/projects/agent-orchestration/pipelines/gc-pipeline.yaml_
  - [x] GC pipeline YAML exists that runs scan -> report -> optional auto-fix
    _Validation: read pipeline YAML_
  _~60 LOC_
- [x] **Upgrade existing GC cron** -- Update the phase 3 garbage collection cron to use the new scanner instead of ad-hoc checks
  - [x] `p10.d4.t1` Upgrade GC cron to use scanner module (depends: p10.d1.t1)
    > Update the existing convention-gc cron job prompt to call gc_scanner.py with the target project's AI_GUIDE.md. Keep the weekly schedule. Add optional auto-fix mode gated by a flag.
  - [x] Cron prompt references gc_scanner.py instead of manual grep/find commands
    _Validation: read cron prompt_
  _~20 LOC_

### Technical Notes

The scanner should be project-agnostic -- it reads AI_GUIDE.md for rules rather than hardcoding conventions. Auto-fix should be conservative: only fix things that are mechanically verifiable (naming, imports, structure), never touch logic.

### Risks

- Auto-fix could introduce subtle bugs if confidence threshold is too low
- Different projects have wildly different conventions -- parser needs to be flexible

## [x] phase-11: Workspace Lifecycle Management (COMPLETE)

**Goal:** Implement workspace cleanup, archival, and the "Dog" role pattern for maintaining orchestrator hygiene

The orchestrator creates isolated workspaces per issue (~/zion/projects/agent-orchestration/workspaces/ISSUE-NUM) but never cleans them up. Over time, disk fills with stale workspaces. Gas Town's "Dog" role handles town-level maintenance and cleanup. This phase implements workspace lifecycle: active -> completed -> archived -> pruned, with configurable retention policies. Also adds the Dog role to the role system for general maintenance tasks.

### Deliverables

- [x] **Workspace state machine** -- Track workspace lifecycle states and enforce retention policies
  - [x] `p11.d1.t1` Add workspace state tracking to spawner.py
    > When spawner creates a workspace, write a .workspace.json metadata file with: issue_number, created_at, status (active), role, pipeline. When orchestrator marks an issue complete, update status to completed. Add archive() and prune() functions that move completed workspaces to an archive dir and delete old archives respectively.
    _Files: ~/zion/projects/agent-orchestration/spawner.py, ~/zion/projects/agent-orchestration/workspace_manager.py_
  - [x] Workspaces have defined states (active, completed, archived, pruned)
    _Validation: check workspace metadata files_
  _~100 LOC_
- [x] **Dog role profile** -- Add a maintenance role that handles cleanup, health checks, and housekeeping
  - [x] `p11.d2.t1` Create Dog role profile
    > Create roles/dog.yaml: name=dog, description="Maintenance and cleanup agent", system_prompt focuses on hygiene tasks (archive old workspaces, check disk usage, verify orchestrator health, clean logs), allowed_toolsets=[bash, filesystem], max_turns=5 (short tasks). Include maintenance-specific prompts for common cleanup operations.
    _Files: ~/zion/projects/agent-orchestration/roles/dog.yaml_
  - [x] Dog role YAML exists with maintenance-focused prompts and toolsets
    _Validation: read roles/dog.yaml_
  _~40 LOC_
- [x] **Cleanup cron job** -- Scheduled job that archives completed workspaces and prunes old archives
  - [x] `p11.d3.t1` Create workspace cleanup cron (depends: p11.d1.t1)
    > Create a daily cron that calls workspace_manager.py cleanup --archive-after 7 --prune-after 30. Archives completed workspaces older than 7 days, deletes archives older than 30 days. Reports stats (archived N, pruned N, freed X MB).
    _Files: ~/zion/projects/agent-orchestration/workspace_manager.py_
  - [x] Cron job runs daily and archives workspaces older than N days
    _Validation: cronjob list_
  _~30 LOC_
- [x] **Update status.sh with workspace hygiene** -- Show workspace states and disk usage in the status dashboard
  - [x] `p11.d4.t1` Add workspace section to status.sh (depends: p11.d1.t1)
    > Add a "Workspaces" section to status.sh: active N, completed N, archived N, total disk usage. Call workspace_manager.py stats to get the data.
    _Files: ~/zion/projects/agent-orchestration/status.sh_
  - [x] status.sh shows workspace counts by state and total disk usage
    _Validation: run status.sh_
  _~30 LOC_

### Technical Notes

Archive = move to ~/.orchestrator/archives/ with timestamp. Prune = delete archived dirs older than threshold. Keep it simple -- no database, just filesystem state + JSON metadata.

### Risks

- Accidentally pruning active workspaces -- need strict age + status checks before deletion
- Archived workspaces may contain useful context for similar future issues -- consider keeping a summary

## [x] phase-12: Agent-Legible Self-Documentation (COMPLETE)

**Goal:** Make the orchestrator project itself follow agent.md best practices, enabling the orchestrator to be maintained and extended by autonomous agents

The research emphasizes "Agent-Legible Software" -- code, tests, docs, and infrastructure all optimized for high-speed autonomous iteration. The orchestrator project has working code but no AI_GUIDE.md, no inline architecture docs, and no structured conventions. This phase makes the orchestrator project "eat its own dog food": create an AI_GUIDE.md that describes the orchestrator's architecture, add docstrings and type hints to all modules, create a CONTRIBUTING.md for agents, and ensure the project can be safely modified by autonomous workers following the same patterns it orchestrates.

### Deliverables

- [x] **AI_GUIDE.md for orchestrator project** -- Create a comprehensive agent.md/AI_GUIDE.md that enables autonomous agents to work on the orchestrator codebase
  - [x] `p12.d1.t1` Create AI_GUIDE.md for orchestrator
    > Create ~/zion/projects/agent-orchestration/AI_GUIDE.md following the agent.md spec from the research: (1) Tech Stack: Python 3, YAML, bash, gh CLI, (2) Executable Commands: python3 -m pytest, python3 dag.py --validate, python3 executor.py --pipeline, (3) Code Examples: how to add a new node type, how to add a new role, how to create a pipeline, (4) Three-Tier Boundaries: Always (run tests before commit, use type hints), Ask First (modify YAML schema, change public APIs), Never (delete existing pipelines, modify poller auth).
    _Files: ~/zion/projects/agent-orchestration/AI_GUIDE.md_
  - [x] AI_GUIDE.md exists with tech stack, commands, architecture overview, and three-tier boundaries
    _Validation: read AI_GUIDE.md_
  _~100 LOC_
- [x] **Module documentation pass** -- Add docstrings, type hints, and architecture comments to all Python modules
  - [x] `p12.d2.t1` Add docstrings and type hints to all modules
    > Add comprehensive docstrings to: dag.py (node types, pipeline parsing, validation), executor.py (execution flow, context handling, node executors), poller.py (API interaction, filtering), spawner.py (workspace setup, role assignment), roles.py (role loading, matching), orchestrator.py (main loop, state management). Add type hints to all function signatures. Add module-level docstrings explaining each file's purpose.
    _Files: ~/zion/projects/agent-orchestration/dag.py, ~/zion/projects/agent-orchestration/executor.py, ~/zion/projects/agent-orchestration/poller.py, ~/zion/projects/agent-orchestration/spawner.py, ~/zion/projects/agent-orchestration/roles.py, ~/zion/projects/agent-orchestration/orchestrator.py_
  - [x] All public functions have docstrings and type annotations
    _Validation: python3 -c "import ast; ..." or manual review_
  _~200 LOC_
- [x] **Architecture decision record** -- Create an ADR or design doc explaining the orchestrator architecture for future agents
  - [x] `p12.d3.t1` Create ARCHITECTURE.md (depends: p12.d1.t1)
    > Create ~/zion/projects/agent-orchestration/ARCHITECTURE.md with: (1) ASCII system diagram showing poller -> spawner -> executor -> DAG flow, (2) Data flow description (GitHub Issues -> poller JSON -> spawner workdir -> executor pipeline -> results), (3) Key design decisions (why YAML DAGs, why role profiles, why filesystem-based state), (4) Extension points (how to add node types, roles, pipelines), (5) Comparison to Symphony/Gas Town architecture.
    _Files: ~/zion/projects/agent-orchestration/ARCHITECTURE.md_
  - [x] ARCHITECTURE.md exists with system diagram, data flow, and design decisions
    _Validation: read ARCHITECTURE.md_
  _~120 LOC_

### Technical Notes

This is a meta-phase -- the orchestrator documenting itself so agents can maintain it. Follow the agent.md spec format exactly since this is the reference implementation for the Hermes ecosystem.

### Risks

- Documentation may drift from code if not kept in sync -- consider adding a doc-check to the test suite

## [x] phase-13: Pull Request Automation (COMPLETE)

**Goal:** Complete the issue-to-PR lifecycle by auto-creating pull requests after successful pipeline execution

Symphony's end-to-end flow is: issue -> workspace -> agent work -> PR. The orchestrator currently stops at "workspace with commits" -- no PR is ever created. This phase closes that gap by adding PR creation after successful pipelines, with metadata linking the PR back to the issue, the role, and the pipeline used. This transforms the orchestrator from a "workspace factory" into a true autonomous development pipeline that mirrors the 500% PR increase reported by OpenAI teams using Symphony.


### Deliverables

- [x] **PR creator module** -- Python module that creates GitHub PRs after successful pipeline execution with orchestrator metadata
  - [x] `p13.d1.t1` Create pr_creator.py module
    > Python module that: (1) reads workspace metadata (issue number, role, pipeline, duration from meta.json), (2) creates a feature branch from workspace changes, (3) pushes to remote, (4) creates a GitHub PR via gh CLI with structured body (issue link, role used, pipeline name, duration, test results), (5) labels the PR and links it to the issue. Include --draft flag for draft PRs.
    _Files: ~/zion/projects/agent-orchestration/pr_creator.py_
  - [x] Module can create a PR from a workspace branch with structured body
    _Validation: python3 pr_creator.py --workspace workspaces/42 --repo owner/repo_
  _~150 LOC_
- [x] **PR integration with executor pipeline** -- Add a PR step to the standard and team pipelines that runs after successful commit
  - [x] `p13.d2.t1` Add PR step to pipeline templates (depends: p13.d1.t1)
    > Add a conditional bash node to standard-pipeline.yaml and team-pipeline.yaml that calls pr_creator.py after commit. The step should be gated by a pipeline env var (CREATE_PR=true) so it can be toggled. Include the PR body template as a pipeline env variable.
    _Files: ~/zion/projects/agent-orchestration/pipelines/standard-pipeline.yaml, ~/zion/projects/agent-orchestration/pipelines/team-pipeline.yaml_
  - [x] Pipeline YAMLs include an optional PR creation step after commit
    _Validation: read pipeline YAML, trace nodes_
  _~60 LOC_
- [x] **PR lifecycle management** -- Track PR status and auto-close/update when the source issue changes state
  - [x] `p13.d3.t1` Add PR tracking to workspace metadata (depends: p13.d1.t1)
    > After PR creation, update workspace meta.json with: pr_number, pr_url, pr_state, created_at. Add a function to pr_creator.py that checks PR status (open/merged/closed) and can close a PR when the source issue is closed. Update orchestrator.py run_loop() to check for completed workspaces with open PRs and post a summary comment on the issue.
    _Files: ~/zion/projects/agent-orchestration/pr_creator.py, ~/zion/projects/agent-orchestration/orchestrator.py_
  - [x] PR metadata stored in workspace includes PR number and URL
    _Validation: check workspace meta.json after PR creation_
  _~80 LOC_
- [x] **Configurable PR settings** -- YAML config for PR behavior (draft mode, labels, reviewers, branch naming)
  - [x] `p13.d4.t1` Create pr_config.yaml
    > Create pr_config.yaml with: draft (bool, default false), auto_label (bool, default true), labels (list, e.g. ["auto-generated", "agent"]), reviewers (list, optional), branch_prefix (string, e.g. "orch/"), pr_body_template (multiline string with {{issue_url}}, {{role}}, {{pipeline}}, {{duration}} placeholders), close_on_issue_close (bool, default true).
    _Files: ~/zion/projects/agent-orchestration/pr_config.yaml_
  - [x] pr_config.yaml exists with sensible defaults
    _Validation: read YAML file_
  _~40 LOC_

### Technical Notes

Uses gh CLI for all GitHub operations (PR create, issue link, label). No GitHub API tokens needed -- relies on gh auth. PR body should be structured for both human and machine readability. Consider adding a "Generated by Hermes Orchestrator" footer.

### Risks

- PRs created by agents may not meet human review standards -- consider always starting in draft mode
- Branch naming collisions if multiple workers create PRs for the same issue
- Pushing to remote requires write access -- need to handle auth errors gracefully

## [x] phase-14: Agent Health Monitoring (Deacon Pattern) (COMPLETE)

**Goal:** Implement the Gas Town Deacon pattern -- a health supervision daemon that monitors running workers, detects stuck agents, and manages resource usage

Gas Town's Deacon role is a "daemon beacon; central health supervisor" that monitors the health of all running agents. Currently the orchestrator can spawn workers but has no way to detect if a worker is stuck, consuming excessive resources, or has silently failed. This phase adds health monitoring: periodic checks on workspace activity, disk usage tracking, timeout detection, and auto-recovery or escalation for unhealthy workers. This is essential for running the orchestrator in production where workers may run for hours.


### Deliverables

- [x] **Health check module** -- Python module that checks the health of active worker workspaces
  - [x] `p14.d1.t1` Create health_check.py module
    > Python module that: (1) scans all workspaces with status "in-progress", (2) checks last file modification time (stuck detection), (3) measures disk usage per workspace, (4) checks for zombie processes (optional, via ps), (5) reports health as JSON with per-worker status (healthy, stale, oversized, unknown). Configurable thresholds: stale_after_minutes (default 30), max_disk_mb (default 500). Support --watch flag for continuous monitoring.
    _Files: ~/zion/projects/agent-orchestration/health_check.py_
  - [x] Module can scan all active workspaces and report health status per worker
    _Validation: python3 health_check.py --all_
  - [x] Detects stuck workers (no file changes in N minutes)
    _Validation: create a stale workspace, run health check_
  _~120 LOC_
- [x] **Auto-recovery for stuck workers** -- Automatically detect and handle stuck workers (timeout, escalation, or restart)
  - [x] `p14.d2.t1` Add auto-recovery logic to health_check.py (depends: p14.d1.t1)
    > Add to health_check.py: (1) when a worker is stale beyond threshold, update its meta.json status to "failed", (2) post a comment on the GitHub issue explaining the timeout, (3) optionally archive the workspace, (4) log the recovery event. Support --auto-recover flag and --escalate flag (create a new issue for human review). Recovery modes: mark-failed (default), archive, retry (re-spawn with reduced max_turns).
    _Files: ~/zion/projects/agent-orchestration/health_check.py_
  - [x] Stuck workers are detected and marked as failed after timeout
    _Validation: simulate stuck worker, verify detection_
  _~80 LOC_
- [x] **Health monitoring cron job** -- Scheduled cron job that runs health checks and auto-recovers unhealthy workers
  - [x] `p14.d3.t1` Create health monitoring cron job (depends: p14.d2.t1)
    > Create a Hermes cron job that runs health_check.py --auto-recover every 15 minutes. Include config for thresholds, notification on failure, and escalation. The cron prompt should read health_config.yaml for settings.
  - [x] Cron job runs health checks every 15 minutes
    _Validation: cronjob list_
  _~20 LOC_
- [x] **Health dashboard in status.sh** -- Show worker health status alongside the existing status dashboard
  - [x] `p14.d4.t1` Add health section to status.sh (depends: p14.d1.t1)
    > Add a "Worker Health" section to status.sh that calls health_check.py and displays: per-worker status (healthy/stale/oversized), disk usage, last activity time, time since spawn. Use color coding if terminal supports it (green=healthy, yellow=stale, red=failed).
    _Files: ~/zion/projects/agent-orchestration/status.sh_
  - [x] status.sh shows health status per active worker
    _Validation: run status.sh, check for health section_
  _~40 LOC_

### Technical Notes

Health checks are filesystem-based (no need for process monitoring). Stuck detection uses file modification timestamps. Disk usage via du -sb. The Deacon pattern is complementary to the Dog pattern (phase 11): Dog cleans up completed workspaces, Deacon monitors active ones.

### Risks

- Stuck detection threshold is tricky -- too short and you kill slow workers, too long and stuck workers waste resources
- Auto-recovery could lose work if a worker was actually making progress on a long task
- File modification time may not accurately reflect agent activity (agent might be "thinking")

## [x] phase-15: Safety Policies and Approval Gates (COMPLETE)

**Goal:** Add configurable safety policies modeled on Symphony's approval_policy to control when human approval is required before agent actions proceed

Symphony supports three approval modes: untrusted (every action requires approval), on-failure (only failed actions require approval), and never (fully autonomous). The current Hermes orchestrator runs in "never" mode exclusively -- no human checkpoints exist. This is fine for trusted pipelines but risky for production repos, sensitive changes, or new team members. This phase adds configurable approval gates at the pipeline level, node level, and orchestrator level, enabling a spectrum from fully autonomous to fully supervised operation. This is the "Outer Harness" safety layer from Harness Engineering applied to the Hermes orchestrator.


### Deliverables

- [x] **Approval policy engine** -- Configurable approval modes that gate pipeline execution at defined checkpoints
  - [x] `p15.d1.t1` Create approval.py module
    > Python module implementing approval policies: (1) ApprovalMode enum (untrusted, on-failure, never), (2) check_approval() function that takes mode, node result, and policy config, returns (approved: bool, reason: str), (3) untrusted mode: every AI node requires approval before proceeding, (4) on-failure mode: only failed bash/test nodes require approval before retry, (5) never mode: no approval needed (current behavior). Include approval_context that captures what needs approval (diff, test output, prompt).
    _Files: ~/zion/projects/agent-orchestration/approval.py_
  - [x] Support for untrusted, on-failure, and never approval modes
    _Validation: configure each mode, verify behavior_
  _~100 LOC_
- [x] **APPROVAL node type for DAG** -- Add an APPROVAL node type that pauses pipeline execution until human approval
  - [x] `p15.d2.t1` Add APPROVAL node type to DAG executor (depends: p15.d1.t1)
    > Add NodeType.APPROVAL to dag.py. The approval node takes: prompt (what the human is approving), timeout (how long to wait before failing), and on_timeout (fail or skip). In executor.py: when an approval node is reached, write a pending approval file to the workspace, post a GitHub comment requesting approval, and poll for an approval file or comment. If approval is granted, continue. If timeout, apply on_timeout behavior. Support --auto-approve flag to bypass for CI.
    _Files: ~/zion/projects/agent-orchestration/dag.py, ~/zion/projects/agent-orchestration/executor.py_
  - [x] Pipeline YAML can include approval nodes that block until approved
    _Validation: create pipeline with approval node, execute it_
  _~120 LOC_
- [x] **Approval-safe pipeline template** -- Pipeline YAML that includes approval gates at critical checkpoints
  - [x] `p15.d3.t1` Create safe-pipeline.yaml with approval gates (depends: p15.d2.t1)
    > Create pipelines/safe-pipeline.yaml based on standard-pipeline.yaml but with APPROVAL nodes inserted: (1) after implement (approve code changes before testing), (2) after review (approve before commit). The approval nodes include context about what changed (file list, diff summary) so the approver can make an informed decision. Include a --mode flag that switches between untrusted and on-failure by changing which approval nodes are active.
    _Files: ~/zion/projects/agent-orchestration/pipelines/safe-pipeline.yaml_
  - [x] Pipeline template has approval nodes before commit and PR creation
    _Validation: read pipeline YAML_
  _~80 LOC_
- [x] **Approval audit trail** -- Log all approval decisions with who approved, when, and why
  - [x] `p15.d4.t1` Add approval logging to approval.py (depends: p15.d1.t1, p8.d1.t1)
    > Append approval events to ~/.orchestrator/logs/approvals.jsonl. Each entry: timestamp, pipeline, node_id, issue_number, decision (approved/rejected/timeout), approver (auto or github_username), reason, context_snapshot (files changed, test results). Add a CLI subcommand to approval.py: audit (show recent approvals), stats (approval rate, average wait time).
    _Files: ~/zion/projects/agent-orchestration/approval.py_
  - [x] Approval events are logged with timestamp, approver, decision, and context
    _Validation: check log files after approval_
  _~60 LOC_

### Technical Notes

Approval is filesystem-based for simplicity: pending approvals are JSON files in the workspace. For GitHub integration, approvals can be triggered by comments with "/approve" or "/reject" on the issue. The APPROVAL node type is the key innovation -- it makes safety a first-class concept in the DAG, not an external wrapper.

### Risks

- Approval nodes can stall pipelines indefinitely if no one approves -- need timeout and escalation
- Different approval modes for different repos/tasks adds configuration complexity
- Human approval defeats the purpose of autonomous orchestration -- needs to be optional and off by default

## [x] phase-16: Multi-Repo Orchestration (COMPLETE)

**Goal:** Extend the orchestrator to manage tasks across multiple GitHub repositories with per-repo configuration

Symphony and Gas Town both manage multiple repositories simultaneously. The current Hermes orchestrator is hardcoded to a single repo (ORCH_REPO). This phase extends it to support multiple repos with per-repo configuration: different pipelines, roles, AI_GUIDE.md files, approval policies, and cost budgets. Workspaces are organized by repo. The orchestrator polls all configured repos and routes tasks to the appropriate worker configuration. This is the scaling phase that transforms the orchestrator from a single-project tool into a fleet manager.


### Deliverables

- [x] **Multi-repo configuration** -- Extend orchestrator.yaml to support multiple repos with per-repo settings
  - [x] `p16.d1.t1` Extend orchestrator.yaml for multi-repo support
    > Redesign orchestrator.yaml to support: repos (list of repo configs), each with: name, url, labels, pipeline, roles_dir, ai_guide_path, approval_mode, max_concurrent, budget_daily. Keep backward compatibility: if "repo" (singular) is set, treat as single-repo mode. Add a validate_config() function to orchestrator.py that checks all repo configs are valid and accessible.
    _Files: ~/zion/projects/agent-orchestration/orchestrator.yaml, ~/zion/projects/agent-orchestration/orchestrator.py_
  - [x] Config supports repos as a list with per-repo pipeline, roles, labels, and policies
    _Validation: read config YAML_
  _~80 LOC_
- [x] **Per-repo workspace organization** -- Organize workspaces by repo to avoid collisions and enable repo-specific cleanup
  - [x] `p16.d2.t1` Update spawner.py for per-repo workspace layout (depends: p16.d1.t1)
    > Change workspace path from workspaces/{issue_number} to workspaces/{repo_name}/{issue_number}. Update spawner.py spawn_worker() to accept repo_name parameter. Update orchestrator.py to pass repo_name when spawning. Update status.sh, health_check.py, and workspace_manager.py to handle the new layout. Add a migration function that moves existing workspaces to the new layout.
    _Files: ~/zion/projects/agent-orchestration/spawner.py, ~/zion/projects/agent-orchestration/orchestrator.py, ~/zion/projects/agent-orchestration/status.sh_
  - [x] Workspaces are organized as workspaces/{repo_name}/{issue_number}
    _Validation: spawn a worker, check workspace path_
  _~60 LOC_
- [x] **Multi-repo poller** -- Poll all configured repos and aggregate results into a unified task queue
  - [x] `p16.d3.t1` Add multi-repo polling to orchestrator.py (depends: p16.d1.t1)
    > Update orchestrator.py run_loop() to iterate over all configured repos, poll each, and aggregate results. Apply per-repo max_concurrent limits. Report per-repo stats in the summary output. Handle repo-specific errors gracefully (one repo failing shouldn't block others). Add --repo flag to filter to a single repo for debugging.
    _Files: ~/zion/projects/agent-orchestration/orchestrator.py_
  - [x] Single orchestrator loop polls all repos and reports per-repo task counts
    _Validation: run orchestrator with multi-repo config_
  _~80 LOC_
- [x] **Per-repo cost tracking** -- Track estimated costs per repo and alert when approaching budget limits
  - [x] `p16.d4.t1` Add cost tracking to orchestrator (depends: p16.d1.t1)
    > Create cost_tracker.py module: (1) estimate token usage per pipeline execution based on node types and turns (AI nodes cost ~10K tokens/turn, bash nodes are free), (2) accumulate daily costs per repo, (3) compare against per-repo budget_daily limit, (4) alert (print warning) when approaching 80% of budget, (5) stop spawning workers when budget is exceeded. Store daily costs in ~/.orchestrator/costs/{repo}/{date}.json. CLI: python3 cost_tracker.py report --period week.
    _Files: ~/zion/projects/agent-orchestration/cost_tracker.py_
  - [x] Cost report shows per-repo estimated spend with daily totals
    _Validation: run cost report command_
  _~100 LOC_

### Technical Notes

Multi-repo is primarily a configuration and routing change, not a fundamental architecture change. The poller already accepts a repo parameter. The spawner already supports per-task configuration. The main work is in the orchestrator loop (iterate over repos) and workspace layout (add repo prefix). Backward compatibility is important: single-repo mode must continue to work with no config changes.

### Risks

- More repos means more GitHub API calls -- need to respect rate limits across all repos
- Per-repo configuration drift -- different repos may need different orchestrator versions
- Cost tracking is estimates only -- actual token usage depends on the LLM provider and model
- Workspace migration from flat layout to repo-prefixed layout could break existing workspaces

## [ ] phase-17: Structural Invariants Engine (PLANNED)

**Goal:** Build custom structural tests that enforce architectural constraints (layering, dependency direction, module boundaries) beyond code style

The Harness Engineering research emphasizes "Rigid Architecture" as a key pillar: enforcing a strict layering model that limits the agent's search space. Phase 10's convention scanner handles naming and style conventions. This phase goes deeper: enforcing architectural rules like "no UI code importing from database layer," "service modules must depend on repo interfaces not implementations," and "all public APIs must have type annotations." These invariants are mechanically checked and can be run as pipeline gates, catching architectural drift before it accumulates.

### Deliverables

- [x] **Architecture invariant checker** -- Python module that reads an invariants.yaml config and checks a codebase for architectural violations
  - [x] `p17.d1.t1` Create invariant_checker.py module
    > Python module that: (1) reads invariants.yaml defining project-specific architectural rules, (2) uses AST parsing to check import statements against forbidden_imports rules, (3) verifies layer_order (e.g., types -> config -> repo -> service), (4) checks dependency_direction (higher layers cannot import from lower), (5) detects circular dependencies via import graph, (6) outputs structured JSON report with file:line:violation:severity. Support --fix flag for auto-fixable violations (reorder imports).
    _Files: ~/zion/projects/agent-orchestration/invariant_checker.py_
  - [x] Module parses invariants.yaml with rule definitions (forbidden_imports, required_interfaces, layer_order, dependency_direction)
    _Validation: read config and checker code_
  - [x] Checker detects at least 4 violation types (forbidden imports, layer violations, missing type annotations, circular dependencies)
    _Validation: run checker on test fixtures with known violations_
  _~150 LOC_
- [x] **Invariants configuration schema** -- YAML schema for defining project-specific architectural invariants with sensible defaults
  - [ ] `p17.d2.t1` Create invariants.yaml schema and example config (depends: p17.d1.t1)
    > Define invariants.yaml schema with sections: layers (ordered list of module layers), forbidden_imports (regex patterns), dependency_rules (source_layer -> allowed_target_layers), required_annotations (functions/classes that need type hints), circular_limit (max allowed cycle length, 0 = none). Create example-invariants.yaml for a typical layered project (models/repo/service/api).
    _Files: ~/zion/projects/agent-orchestration/invariants.yaml_
  - [x] invariants.yaml schema supports forbidden_imports, layer_order, dependency_direction, required_annotations, circular_dependency_limit
    _Validation: read YAML schema_
  - [x] Example invariants.yaml provided for a typical layered project
    _Validation: read example config_
  _~80 LOC_
- [ ] **Integrate invariant checker into pipelines** -- Add invariant checking as a gate in the standard and team pipelines
  - [ ] `p17.d3.t1` Add invariant check to pipeline templates (depends: p17.d1.t1, p5.d3.t1)
    > Add a Bash node to standard-pipeline.yaml and team-pipeline.yaml that runs invariant_checker.py with the project's invariants.yaml. Place it after the implement node and before tests, so architectural violations are caught early. Gate the pipeline on failure (stop before tests if invariants fail).
    _Files: ~/zion/projects/agent-orchestration/pipelines/standard-pipeline.yaml, ~/zion/projects/agent-orchestration/pipelines/team-pipeline.yaml_
  - [ ] standard-pipeline.yaml and team-pipeline.yaml include an invariant check node after implementation
    _Validation: read pipeline YAML_
  _~40 LOC_
- [ ] **Tests for invariant checker** -- Unit tests covering all violation types and edge cases
  - [ ] `p17.d4.t1` Create test_invariant_checker.py (depends: p17.d1.t1)
    > Create test fixtures (sample Python files with intentional violations) and test cases: valid project passes all checks, forbidden import detected, layer violation detected, circular dependency detected, missing type annotation detected, empty project returns clean report, invalid config handled gracefully, --fix flag corrects reorderable violations.
    _Files: ~/zion/projects/agent-orchestration/test_invariant_checker.py_
  - [ ] Test file with 10+ test cases covering AST parsing, layer enforcement, cycle detection
    _Validation: python3 -m pytest test_invariant_checker.py -v_
  _~120 LOC_

### Technical Notes

Use Python AST module for import analysis -- no external dependencies. Layer enforcement uses a simple graph traversal. Circular dependency detection uses Tarjan's algorithm. Keep rules project-agnostic via YAML config.

### Risks

- AST-based analysis may miss dynamic imports or conditional imports
- Defining good architectural invariants requires domain knowledge of the target project
- Overly strict invariants can slow down development if not tuned carefully

## [ ] phase-18: Agent Self-Debugging and Trace Tools (PLANNED)

**Goal:** Give agents the ability to read their own execution traces, inspect logs, and debug failures during pipeline execution

Phase 8 adds execution history for humans to review after runs. The Harness Engineering research emphasizes "Application Legibility" -- agents should have local access to logs, metrics, and traces so they can reason about code they just wrote. This phase builds tools that make execution traces agent-readable, letting an AI node in a pipeline inspect its own (or a previous run's) output, understand what failed, and adjust its approach. This is the difference between "a human reviews the log" and "the agent reviews its own trace and self-corrects."

### Deliverables

- [ ] **Agent-readable trace formatter** -- Module that converts execution logs into a concise, agent-optimized format suitable for inclusion in prompts
  - [ ] `p18.d1.t1` Create trace_formatter.py module (depends: p8.d1.t1)
    > Python module that: (1) reads a pipeline run from execution_log.py, (2) extracts key information per node (status, duration, error message, output summary), (3) formats as compact text for prompt injection (<2000 tokens), (4) supports --format compact|detailed|diff modes, (5) highlights failure chain (which nodes failed and why), (6) includes context about what files were touched. The compact format is designed to be prepended to an AI node's prompt so the agent can understand previous failures.
    _Files: ~/zion/projects/agent-orchestration/trace_formatter.py_
  - [ ] Can format a pipeline run trace into a compact summary (node status, error messages, key outputs) under 2000 tokens
    _Validation: python3 trace_formatter.py --run RUN_ID --compact_
  - [ ] Supports multiple output formats: compact (for prompts), detailed (for debugging), diff-focused (shows what changed at each node)
    _Validation: run with different format flags_
  _~120 LOC_
- [ ] **Debug context builder for executor** -- Enhance the DAG executor to build debug context for AI nodes when previous runs failed
  - [ ] `p18.d2.t1` Add debug context to executor AI nodes (depends: p18.d1.t1, p5.d2.t1)
    > Modify executor.py to: (1) when an AI node runs after a previous failure in the same pipeline execution, automatically call trace_formatter to build a debug context, (2) inject the debug context into the AI node's prompt as a "Previous attempt failed:" section, (3) include the specific error message and which node failed, (4) for Loop nodes, include iteration count and failure history. This enables AI nodes to learn from their own failures within a single pipeline run.
    _Files: ~/zion/projects/agent-orchestration/executor.py_
  - [ ] Executor automatically builds a debug context string when retrying a failed pipeline
    _Validation: execute pipeline with failure, check retry prompt includes trace_
  _~60 LOC_
- [ ] **Cross-run failure correlation** -- Analyze multiple pipeline runs to find recurring failure patterns
  - [ ] `p18.d3.t1` Add failure correlation to trace_formatter (depends: p18.d1.t1)
    > Add --correlate flag to trace_formatter.py that: (1) reads the last N pipeline runs, (2) groups failures by node_id and failure_type, (3) identifies recurring patterns (same node failing in >50% of runs), (4) outputs a summary: "Node 'test' failed in 8/10 recent runs. Common error: ImportError. Suggested fix: check dependencies." This enables the orchestrator or a human to spot systemic issues.
    _Files: ~/zion/projects/agent-orchestration/trace_formatter.py_
  - [ ] Can identify that a specific node type or pipeline step fails repeatedly across runs
    _Validation: python3 trace_formatter.py --correlate --last 20_
  _~80 LOC_
- [ ] **Self-debug pipeline template** -- Pipeline YAML that uses trace tools to enable agents to debug and fix their own failures
  - [ ] `p18.d4.t1` Create debug-pipeline.yaml (depends: p18.d2.t1, p5.d3.t1)
    > Create pipelines/debug-pipeline.yaml: AI(implement) -> Bash(test) -> AI(debug, reads trace from failed run, analyzes failure) -> Loop(fix, max=3, includes trace context in each iteration) -> Bash(test). The debug node uses trace_formatter to get the failure context, then formulates a targeted fix. The loop retries with increasing trace history so the agent can see what it already tried.
    _Files: ~/zion/projects/agent-orchestration/pipelines/debug-pipeline.yaml_
  - [ ] Pipeline includes a debug node that reads previous failure traces and formulates a fix strategy
    _Validation: read pipeline YAML, trace through nodes_
  _~60 LOC_

### Technical Notes

The key insight is that traces should be compact enough to fit in an AI prompt without blowing the context window. The compact format targets <2000 tokens. Detailed format is for human debugging. Diff format shows what files changed at each step.

### Risks

- Trace context in prompts adds tokens -- need to be careful about context window budget
- Over-debugging can make pipelines slower without adding value for simple failures
- Trace format needs to be stable across executor versions to avoid breaking correlation

## [ ] phase-19: Continuous Self-Improvement Loop (PLANNED)

**Goal:** Analyze execution history to identify recurring failure patterns, auto-tune pipeline parameters, and improve the orchestrator's own harness

The research's end vision is a "self-correcting codebase" where the system analyzes its own execution history and improves its harness. Phase 10 handles code-level garbage collection. This phase closes the meta-loop: the orchestrator analyzes its own pipeline execution data to identify which nodes fail most, which pipelines have the lowest success rate, and which parameters need tuning. It then generates actionable improvement suggestions or automatically adjusts parameters. This transforms the orchestrator from a static executor into a system that gets better at its job over time.

### Deliverables

- [ ] **Failure pattern analyzer** -- Module that analyzes execution logs to identify recurring failure patterns and bottlenecks
  - [ ] `p19.d1.t1` Create self_improve.py analyzer module (depends: p8.d1.t1)
    > Python module that: (1) reads all pipeline runs from execution_log.py, (2) computes per-node failure rates, (3) identifies failure sequences (which nodes fail after which), (4) detects bottlenecks (slowest nodes, most retried loops), (5) identifies pipeline-level patterns (which pipelines have lowest success rate), (6) outputs structured JSON report with findings and suggested actions. Support --period flag for time-windowed analysis.
    _Files: ~/zion/projects/agent-orchestration/self_improve.py_
  - [ ] Can identify top 5 failing nodes across all runs with failure rates
    _Validation: python3 self_improve.py --analyze --last 50_
  - [ ] Detects patterns like "test node fails 60% of the time after implement node" or "loop node always hits max iterations"
    _Validation: run analysis on synthetic history_
  _~150 LOC_
- [ ] **Parameter auto-tuner** -- Automatically adjust pipeline parameters (loop max, timeout, retry count) based on historical performance
  - [ ] `p19.d2.t1` Add parameter tuning to self_improve.py (depends: p19.d1.t1)
    > Add --tune mode to self_improve.py: (1) analyze loop nodes to determine if max_iterations is too low (most loops hit the limit) or too high (loops almost never reach it), (2) analyze timeout values for bash nodes (are tests timing out?), (3) suggest adjusted values with confidence scores, (4) support --apply flag to write suggested values back to pipeline YAML files, (5) keep a tuning history log to track changes over time.
    _Files: ~/zion/projects/agent-orchestration/self_improve.py_
  - [ ] Can suggest parameter adjustments based on failure patterns (e.g., "loop max 3 is insufficient, 80% of loops hit the limit")
    _Validation: python3 self_improve.py --tune_
  _~100 LOC_
- [ ] **Weekly self-review cron** -- Cron job that runs the analyzer weekly and generates an improvement report
  - [ ] `p19.d3.t1` Create weekly self-review cron (depends: p19.d1.t1)
    > Create a weekly Hermes cron that runs self_improve.py --analyze --period week and outputs a summary report. The report includes: top failure patterns, pipeline success rates, parameter tuning suggestions, and a "health score" for the orchestrator. Optionally creates GitHub Issues for high-priority findings. Keep the report in ~/.orchestrator/reports/ for historical comparison.
  - [ ] Cron job runs weekly and outputs a structured improvement report
    _Validation: cronjob list_
  _~30 LOC_
- [ ] **Improvement action executor** -- Module that can automatically apply low-risk improvements suggested by the analyzer
  - [ ] `p19.d4.t1` Add improvement executor to self_improve.py (depends: p19.d2.t1, p13.d1.t1)
    > Add --apply mode with --auto flag: (1) apply parameter tuning (safe, mechanical changes to pipeline YAML), (2) for structural improvements (new test cases, missing invariants), create a draft GitHub Issue with the suggestion, (3) log all applied changes with before/after values, (4) support --dry-run to preview changes. Only auto-apply changes with confidence >= 0.9.
    _Files: ~/zion/projects/agent-orchestration/self_improve.py_
  - [ ] Can apply parameter tuning suggestions and create issues for structural improvements
    _Validation: python3 self_improve.py --apply --auto_
  _~100 LOC_

### Technical Notes

The self-improvement loop is the most "meta" phase -- the system improving itself. Start with read-only analysis (phase 19.d1), then add parameter tuning (19.d2), then automated action (19.d4). Each step requires more trust. Keep the improvement report human-readable so Jericho can review what the system wants to change.

### Risks

- Auto-tuning could make things worse if the analysis is wrong -- need human review for structural changes
- The improvement loop could get stuck in a cycle (change parameters -> different failures -> change back)
- Analysis quality depends on having enough execution history -- needs a minimum of 20-30 runs to be meaningful

## [ ] phase-20: Context Window Optimization (Smart Zone) (PLANNED)

**Goal:** Implement context budget management for AI nodes so agents stay in the 'smart zone' and avoid reasoning decay

The Ralph Wiggum pattern from the research emphasizes that AI models exhibit reasoning quality decay after reaching 30-60% of their context window. The current DAG executor constructs prompts for AI nodes without any awareness of context budget -- a large issue body + AI_GUIDE.md + pipeline context could easily exceed the optimal range. This phase adds a context_budget module that: (1) estimates token count for prompt components, (2) prioritizes which context to include when budget is tight, (3) truncates or summarizes context that exceeds budget, (4) tracks actual context usage per AI node run for tuning. This ensures agents always operate in the "smart zone" for maximum reasoning quality, directly applying the research's key insight about context management.

### Deliverables

- [ ] **Context budget estimator** -- Python module that estimates token counts for prompt components and manages context budgets
  - [ ] `p20.d1.t1` Create context_budget.py module
    > Python module that: (1) estimates token count using tiktoken or a simple word*1.3 heuristic, (2) accepts a list of prompt components with priorities (issue_body=high, ai_guide=medium, previous_context=low), (3) when total exceeds budget, truncates lowest-priority components first, (4) supports summarize mode that extracts key points from truncated sections, (5) logs actual vs estimated token usage per run. Default budget: 80% of model context window (leaving 20% for response).
    _Files: ~/zion/projects/agent-orchestration/context_budget.py_
  - [ ] Module can estimate token count for a string with reasonable accuracy (within 10%)
    _Validation: python3 context_budget.py --estimate --text "test string"_
  - [ ] Supports configurable budget with per-component priority weights
    _Validation: test with different budget limits and priorities_
  _~120 LOC_
- [ ] **Budget-aware prompt builder in executor** -- Update the DAG executor to use context budgeting when constructing AI node prompts
  - [ ] `p20.d2.t1` Integrate context_budget into executor AI node builder (depends: p20.d1.t1)
    > Modify executor.py build_ai_prompt() to: (1) pass prompt components (issue body, AI_GUIDE.md, role prompt, pipeline context, previous results) to context_budget.fit_to_budget(), (2) include budget stats (estimated_tokens, budget, truncation_applied) in the execution log, (3) support a --budget flag on the executor CLI to override default budget, (4) warn in logs when more than 30% of context is truncated.
    _Files: ~/zion/projects/agent-orchestration/executor.py_
  - [ ] AI node prompts are constructed with budget awareness
    _Validation: run executor with large issue body, check prompt is truncated appropriately_
  - [ ] Budget usage is logged per AI node execution
    _Validation: check execution log for budget fields_
  _~60 LOC_
- [ ] **Context budget configuration** -- YAML config for per-pipeline and per-role context budgets
  - [ ] `p20.d3.t1` Create context_config.yaml (depends: p20.d1.t1)
    > Create context_config.yaml with: default_budget_tokens (80000 for claude models), per_role_overrides (reviewer gets more context, coordinator gets less), per_pipeline_overrides (review-pipeline gets more budget for diff context), component_priorities (ordered list of prompt components with priority weights), summarize_threshold (at what truncation level to switch from truncation to summarization).
    _Files: ~/zion/projects/agent-orchestration/context_config.yaml_
  - [ ] context_config.yaml exists with per-role and per-pipeline budget overrides
    _Validation: read YAML file_
  _~40 LOC_
- [ ] **Context usage analytics** -- Track and report context window usage patterns across pipeline runs
  - [ ] `p20.d4.t1` Add context usage analytics to context_budget.py (depends: p20.d1.t1, p8.d1.t1)
    > Add --stats mode to context_budget.py that: (1) reads execution logs for budget fields, (2) computes average context usage per node type, per role, per pipeline, (3) identifies nodes that frequently hit budget limits (sign of oversized prompts), (4) suggests budget adjustments based on usage patterns. Output as table or JSON.
    _Files: ~/zion/projects/agent-orchestration/context_budget.py_
  - [ ] Can report average context usage per node type and role
    _Validation: python3 context_budget.py --stats --last 20_
  _~80 LOC_

### Technical Notes

Token estimation can use a simple heuristic (chars / 3.5) to avoid external dependencies, or tiktoken if available. The "smart zone" concept means keeping prompt under 60% of model context window. Truncation should preserve the most informative parts: issue title + first paragraph, AI_GUIDE commands section, role system prompt.

### Risks

- Token estimation is inherently imprecise -- different models have different tokenizers
- Over-aggressive truncation could remove critical context that the agent needs
- Budget tuning requires experimentation with real workloads

## [ ] phase-21: Merge Queue and Conflict Prevention (Refinery Pattern) (PLANNED)

**Goal:** Implement Gas Town''s Refinery pattern to manage concurrent agent PRs and prevent merge conflicts

Gas Town's Refinery role "manages merge queues to prevent collisions" -- when multiple agents work on the same codebase simultaneously, their PRs can conflict. The current orchestrator can spawn multiple workers but has no merge coordination. This phase adds a merge queue system that: (1) sequences PR merges to avoid conflicts, (2) detects potential conflicts before agents start work, (3) rebases branches when the base has moved, (4) provides merge order recommendations. This is essential for running the orchestrator at scale with concurrent workers, directly implementing the Refinery pattern from the research.

### Deliverables

- [ ] **Conflict detector** -- Python module that predicts merge conflicts between workspace branches and the main branch
  - [ ] `p21.d1.t1` Create conflict_detector.py module
    > Python module that: (1) runs git diff on workspace branch vs main, (2) for each changed file, checks if main branch has concurrent changes (git log --oneline main..HEAD), (3) uses git merge-tree --write-tree to dry-run merge and detect conflicts, (4) outputs conflict report as JSON with: workspace, branch, conflict_files, conflict_type (content vs structural), severity, suggested_action (rebase, wait, or proceed). Support --batch flag to check all workspaces.
    _Files: ~/zion/projects/agent-orchestration/conflict_detector.py_
  - [ ] Module can check if workspace changes would conflict with main branch
    _Validation: create conflicting changes, run detector_
  - [ ] Reports conflict probability and affected files
    _Validation: check output includes file list and confidence score_
  _~120 LOC_
- [ ] **Merge queue manager** -- Ordered queue that sequences PR merges to minimize conflicts
  - [ ] `p21.d2.t1` Create merge_queue.py module (depends: p21.d1.t1)
    > Python module implementing a priority merge queue: (1) PRs are added to a JSON-backed queue file (~/.orchestrator/merge-queue.jsonl), (2) queue is ordered by: no-conflict PRs first, then by fewest conflicts, then by oldest, (3) supports enqueue, dequeue, reorder, and status commands, (4) before merging, runs conflict_detector to verify merge is still safe, (5) if new conflict detected, moves PR to "needs-rebase" state. CLI: python3 merge_queue.py enqueue --pr 42, dequeue, status, reorder.
    _Files: ~/zion/projects/agent-orchestration/merge_queue.py_
  - [ ] Can enqueue multiple PRs and determine safe merge order
    _Validation: enqueue 3 PRs with overlapping files, verify order minimizes conflicts_
  - [ ] Queue state persists across orchestrator restarts
    _Validation: check queue file exists and is valid after restart_
  _~150 LOC_
- [ ] **Auto-rebase on conflict** -- Automatically rebase workspace branches when main branch has advanced
  - [ ] `p21.d3.t1` Add auto-rebase to merge_queue.py (depends: p21.d2.t1)
    > Add rebase function to merge_queue.py: (1) when a PR is next in queue but has conflicts, attempt git rebase main, (2) if rebase succeeds, re-run tests (configurable), (3) if tests pass, mark as ready to merge, (4) if rebase fails, mark as "needs-manual-intervention" and post a comment on the PR explaining the conflict. Support --auto-rebase flag and --test-after-rebase flag.
    _Files: ~/zion/projects/agent-orchestration/merge_queue.py_
  - [ ] Can rebase a workspace branch onto latest main
    _Validation: create diverged branch, run rebase, verify clean merge_
  - [ ] Rebase failure triggers workspace notification
    _Validation: simulate unresolvable conflict, check notification_
  _~80 LOC_
- [ ] **Merge coordination in orchestrator loop** -- Integrate merge queue into the orchestrator main loop
  - [ ] `p21.d4.t1` Add merge queue check to orchestrator.py (depends: p21.d2.t1, p4.d3.t1)
    > Modify orchestrator.py run_loop() to: (1) before spawning new workers, check if any workspaces have pending PRs in the merge queue, (2) skip spawning workers for issues that would conflict with pending merges, (3) after successful pipeline completion, auto-enqueue the PR in the merge queue, (4) report merge queue status in the loop summary. This ensures the orchestrator is conflict-aware when scheduling work.
    _Files: ~/zion/projects/agent-orchestration/orchestrator.py_
  - [ ] Orchestrator checks merge queue before spawning new workers
    _Validation: run orchestrator with pending queue, verify new workers wait_
  _~60 LOC_

### Technical Notes

The merge queue is file-backed (JSON Lines) for simplicity, no external service needed. Git merge-tree --write-tree is available in git 2.36+ for dry-run merge detection. The Refinery pattern is about preventing collisions, not resolving them -- the goal is to sequence merges so conflicts are rare, not to auto-resolve complex merge conflicts.

### Risks

- Auto-rebase can introduce subtle bugs if the rebase changes semantics
- Merge queue ordering is NP-hard in the general case -- heuristic ordering is good enough
- Concurrent orchestrator instances could race on the queue file -- need file locking

## [ ] phase-22: Config Hot-Reload and Live Tuning (PLANNED)

**Goal:** Enable the orchestrator to pick up config changes without restart, supporting live parameter tuning

Symphony's Elixir implementation features hot code reloading, allowing system updates without interrupting active agent sessions. The Hermes orchestrator reads its config (orchestrator.yaml, role profiles, pipeline YAMLs) once at startup. If you change max_concurrent or swap a pipeline template, you must restart the cron job. This phase adds file-watching that detects config changes and reloads them on the fly. Combined with the self-improvement loop (phase 19) and context budgeting (phase 20), this enables the orchestrator to be tuned in real-time -- adjust parameters, swap pipelines, modify role prompts -- all without interrupting running workers. This is a small but critical operational improvement that makes the orchestrator production-ready for continuous operation.

### Deliverables

- [ ] **Config watcher module** -- Python module that watches config files for changes and triggers reload
  - [ ] `p22.d1.t1` Create config_watcher.py module
    > Python module that: (1) watches specified config files using filesystem modification time (polling every 5s, no inotify dependency), (2) on change, reloads the config and validates it, (3) calls registered callbacks for each config type (on_orchestrator_config_change, on_role_change, on_pipeline_change), (4) logs all config reloads with before/after diff, (5) supports --watch flag for standalone operation and programmatic API for integration. Use file hashing to avoid spurious reloads.
    _Files: ~/zion/projects/agent-orchestration/config_watcher.py_
  - [ ] Module detects changes to YAML config files within 5 seconds
    _Validation: modify config file, check reload is triggered_
  - [ ] Supports watching orchestrator.yaml, role profiles, and pipeline YAMLs
    _Validation: modify each type, verify detection_
  _~100 LOC_
- [ ] **Hot-reload integration in orchestrator** -- Integrate config watcher into the orchestrator main loop
  - [ ] `p22.d2.t1` Integrate config_watcher into orchestrator.py (depends: p22.d1.t1)
    > Modify orchestrator.py to: (1) instantiate config_watcher at startup with callbacks for each config type, (2) on orchestrator.yaml change: reload max_concurrent, repo, labels, pipeline path, (3) on role YAML change: reload affected role profile (roles.py already loads from disk, just need cache invalidation), (4) on pipeline YAML change: next execution uses updated pipeline, (5) add --no-watch flag to disable hot-reload for debugging. Log all reloads to execution history.
    _Files: ~/zion/projects/agent-orchestration/orchestrator.py_
  - [ ] Orchestrator picks up config changes mid-loop without restart
    _Validation: change max_concurrent while orchestrator is running, verify new limit applies_
  - [ ] Role profile changes are picked up for new workers
    _Validation: modify a role YAML, spawn new worker, verify new prompts used_
  _~60 LOC_
- [ ] **Config change audit trail** -- Log all config changes with diffs and timestamps for debugging
  - [ ] `p22.d3.t1` Add config audit logging (depends: p22.d1.t1)
    > Append config change events to ~/.orchestrator/logs/config-changes.jsonl. Each entry: timestamp, config_type (orchestrator/role/pipeline), file_path, change_type (modified/added/deleted), diff_summary (what changed in human-readable form), reloaded_successfully (bool). Add a CLI subcommand to config_watcher.py: audit (show recent changes), rollback (restore previous config version if backed up).
    _Files: ~/zion/projects/agent-orchestration/config_watcher.py_
  - [ ] All config changes are logged with before/after values
    _Validation: change config, check audit log_
  _~50 LOC_
- [ ] **Live tuning CLI** -- CLI command to inspect and modify orchestrator config at runtime
  - [ ] `p22.d4.t1` Add live tuning CLI to config_watcher.py (depends: p22.d2.t1)
    > Add CLI subcommands to config_watcher.py: get KEY (show current value), set KEY VALUE (modify config and trigger reload), reset (restore defaults), validate (check config health). The set command writes the change to the YAML file and triggers the watcher callback. Support --dry-run to preview changes without applying. This enables operators to tune the orchestrator from the command line without editing files.
    _Files: ~/zion/projects/agent-orchestration/config_watcher.py_
  - [ ] Can view current config and modify parameters without editing files
    _Validation: python3 config_watcher.py get max_concurrent && python3 config_watcher.py set max_concurrent 5_
  _~60 LOC_

### Technical Notes

Polling-based file watching (every 5s) is sufficient and avoids platform-specific dependencies (inotify, FSEvents, ReadDirectoryChangesW). File hashing (SHA256 of first 4KB) is fast enough for small YAML configs. The orchestrator's cron-based execution model means "hot reload" really means "pick up changes on next loop iteration" -- no need for true in-process hot reload.

### Risks

- Bad config changes could break the orchestrator mid-operation -- need validation before applying
- Race condition if config file is being written while being read -- use atomic file reads
- Config drift between what''s on disk and what''s in memory if validation rejects a change

## [ ] phase-23: End-to-End Integration and Real-World Validation (PLANNED)

**Goal:** Validate the complete orchestrator system works end-to-end on a real project, measure throughput, and fix integration issues

Phases 1-22 build individual components (poller, spawner, executor, DAG, roles, logging, health, PR creation, etc.) but none validates the full lifecycle: issue filed -> polled -> workspace created -> pipeline executed -> tests pass -> PR created -> issue linked -> workspace archived. This phase runs the full system against a real GitHub repo, measures the time from issue to PR, identifies and fixes integration bugs, and establishes baseline metrics. This is the "smoke test" that proves the orchestrator delivers on the 500% PR increase claim from the Symphony research.

### Deliverables

- [ ] **Integration test suite for full lifecycle** -- Automated test that exercises the complete orchestrator flow from issue creation to PR
  - [ ] `p23.d1.t1` Create test_e2e_lifecycle.py
    > End-to-end test using a test GitHub repo: (1) create a test issue with agent-ready label via gh CLI, (2) run orchestrator one loop iteration, (3) verify workspace was created with correct structure, (4) verify pipeline YAML was loaded, (5) check execution log was written, (6) verify workspace metadata exists. Use fixtures and mocking for parts that need GitHub access. Include cleanup that removes test issues and workspaces after the test.
    _Files: ~/zion/projects/agent-orchestration/test_e2e_lifecycle.py_
  - [ ] Test creates an issue, waits for poller, verifies workspace creation, pipeline execution, and final state
    _Validation: python3 -m pytest test_e2e_lifecycle.py -v_
  _~200 LOC_
- [ ] **Component integration stress test** -- Test that all modules work together correctly when chained (poller -> spawner -> executor -> logger -> health)
  - [ ] `p23.d2.t1` Create test_integration_chain.py
    > Integration test that chains all modules: (1) mock poller returns a test issue, (2) spawner creates workspace and returns path, (3) executor runs a pipeline in that workspace, (4) execution_log records the run, (5) health_check can scan the workspace, (6) workspace_manager can archive it. Verify data flows correctly between modules. Catch any interface mismatches (wrong parameter names, missing fields, incompatible types).
    _Files: ~/zion/projects/agent-orchestration/test_integration_chain.py_
  - [ ] Can run a full pipeline through the executor with real (mocked) poller and spawner
    _Validation: python3 -m pytest test_integration_chain.py -v_
  _~150 LOC_
- [ ] **Fix integration issues discovered during testing** -- Address any bugs, interface mismatches, or missing error handling found during e2e testing
  - [ ] `p23.d3.t1` Fix integration bugs from e2e testing (depends: p23.d1.t1, p23.d2.t1)
    > Run the full integration test suite. Fix any failures. Common integration issues to check: workspace path inconsistencies between spawner and health_check, execution log schema mismatches, role loading failures when roles/ dir is empty, config fallback behavior when orchestrator.yaml is missing, poller error handling when gh auth fails.
    _Files: ~/zion/projects/agent-orchestration/poller.py, ~/zion/projects/agent-orchestration/spawner.py, ~/zion/projects/agent-orchestration/executor.py, ~/zion/projects/agent-orchestration/orchestrator.py, ~/zion/projects/agent-orchestration/health_check.py_
  - [ ] All integration tests pass after fixes
    _Validation: python3 -m pytest test_e2e_lifecycle.py test_integration_chain.py -v_
  _~100 LOC_
- [ ] **Baseline metrics collection** -- Measure and record baseline performance metrics for the orchestrator
  - [ ] `p23.d4.t1` Create metrics.py baseline collector
    > Create metrics.py that reads execution logs and computes: (1) average pipeline duration, (2) pipeline success rate (% that complete without failure), (3) per-node-type average duration, (4) time from issue creation to workspace creation, (5) loop retry rates. Output as JSON for historical comparison. This establishes the baseline before optimization phases (19, 20) can improve on it.
    _Files: ~/zion/projects/agent-orchestration/metrics.py_
  - [ ] Metrics script reports time-to-PR, pipeline success rate, and resource usage
    _Validation: python3 metrics.py --baseline_
  _~100 LOC_

### Technical Notes

This is the "does it actually work?" phase. Focus on real integration, not unit tests (those were done in phase 7). Use a dedicated test repo to avoid polluting real projects. The baseline metrics are crucial for measuring improvement in later phases.

### Risks

- Integration tests may require GitHub auth -- need to handle missing credentials gracefully
- Timing-based tests may be flaky -- use generous timeouts
- Test cleanup may fail if workspaces are in use -- add force cleanup

## [ ] phase-24: Project Onboarding Bootstrap (PLANNED)

**Goal:** Create a quick-start tool that onboards new GitHub repos to the orchestrator in under 5 minutes

Symphony reads WORKFLOW.md from each project automatically. The Hermes orchestrator currently requires manual configuration: creating orchestrator.yaml, setting up AI_GUIDE.md, adding agent-ready labels, configuring the cron job. This phase creates a bootstrap CLI that automates all of this. Run "python3 onboard.py owner/repo" and it: detects the project type (Python/Node/Go), generates an appropriate AI_GUIDE.md, creates a minimal orchestrator config, adds the agent-ready label to the repo, and outputs the cron job command to copy-paste. This directly applies the agent.md spec pattern from the research: making projects agent-legible with minimal human effort.

### Deliverables

- [ ] **Project type detector** -- Analyze a repo to detect its language, framework, build system, and test runner
  - [ ] `p24.d1.t1` Create project detector module
    > Python module that analyzes a local repo clone: (1) check for language markers (setup.py, pyproject.toml, package.json, go.mod, Cargo.toml), (2) detect framework (Django, FastAPI, Express, React, etc.) from dependencies, (3) find test runner (pytest, jest, go test, cargo test), (4) locate build commands, (5) check for existing AI_GUIDE.md or AGENT.md. Output as structured dict. Use gh CLI to get repo metadata (language, topics) as additional signal.
    _Files: ~/zion/projects/agent-orchestration/onboard.py_
  - [ ] Can detect at least 5 project types (Python/pip, Python/poetry, Node/npm, Go, Rust)
    _Validation: python3 onboard.py --detect ~/zion/projects/some-repo_
  _~120 LOC_
- [ ] **AI_GUIDE.md generator** -- Generate a project-specific AI_GUIDE.md based on detected project type and conventions
  - [ ] `p24.d2.t1` Add AI_GUIDE.md generation to onboard.py
    > Add --guide mode to onboard.py: (1) use project detector output to select appropriate template, (2) fill in tech stack section with detected versions (python --version, node --version), (3) generate executable commands section based on detected build/test/lint tools, (4) add three-tier boundaries with sensible defaults for the project type, (5) scan existing code for naming patterns and include them as conventions. Output to stdout or write to file with --write flag.
    _Files: ~/zion/projects/agent-orchestration/onboard.py_
  - [ ] Generates a valid AI_GUIDE.md with tech stack, commands, and three-tier boundaries
    _Validation: python3 onboard.py --guide ~/zion/projects/some-repo_
  _~100 LOC_
- [ ] **Full onboarding CLI** -- One-command onboarding that configures everything needed for a new repo
  - [ ] `p24.d3.t1` Implement full onboarding flow
    > Implement the full onboard.py flow: (1) clone or verify repo exists locally, (2) run project detection, (3) generate AI_GUIDE.md and write to repo root, (4) create minimal orchestrator.yaml entry for the repo, (5) use gh CLI to add "agent-ready" label to the repo, (6) detect test commands and validate they work, (7) output a ready-to-use cron job command. Support --dry-run to preview changes without applying them. Support --pipeline flag to select which pipeline template to use.
    _Files: ~/zion/projects/agent-orchestration/onboard.py_
  - [ ] Single command sets up: orchestrator config, AI_GUIDE.md, GitHub label, and outputs cron command
    _Validation: python3 onboard.py owner/repo --full_
  _~100 LOC_
- [ ] **Onboarding validation test** -- Test the onboarding flow on a real repo and verify the generated config works
  - [ ] `p24.d4.t1` Create test_onboard.py
    > Test the onboarding flow: (1) test project detection on fixture repos (Python, Node, Go), (2) test AI_GUIDE.md generation includes correct commands, (3) test dry-run mode makes no changes, (4) test full onboarding on a test repo creates valid config, (5) test error handling for unsupported project types, missing gh auth, empty repos.
    _Files: ~/zion/projects/agent-orchestration/test_onboard.py_
  - [ ] Can onboard a test repo and the generated config produces a valid orchestrator setup
    _Validation: python3 -m pytest test_onboard.py -v_
  _~80 LOC_

### Technical Notes

The onboarding tool is the "first impression" of the orchestrator for new projects. Keep it simple and opinionated. A good default AI_GUIDE.md is worth more than a perfect one that requires manual editing. Support the most common project types (Python, Node, Go) well rather than trying to handle every edge case.

### Risks

- Project detection may be inaccurate for polyglot repos -- let users override detected settings
- Generated AI_GUIDE.md may include wrong commands -- validation step is critical
- GitHub label creation requires write access -- need clear error messaging

## [ ] phase-25: Orchestrator Resilience and State Recovery (PLANNED)

**Goal:** Make the orchestrator fault-tolerant with crash recovery, partial state handling, and graceful degradation

The research highlights Elixir/BEAM's excellence in "managing long-running, concurrent, and fault-tolerant processes" as a deliberate architectural choice for Symphony. The Hermes orchestrator currently has no crash recovery: if the cron agent crashes mid-pipeline, the workspace is left in an indeterminate state, the issue is never updated, and no one knows the worker failed. This phase adds resilience: (1) workspace state is checkpointed after each node, (2) crashed pipelines can be resumed from the last checkpoint, (3) orphaned workspaces (from crashed orchestrator instances) are detected and cleaned up, (4) the orchestrator handles its own failures gracefully. This transforms the orchestrator from a "best-effort" tool into a reliable system that can run 24/7 without human intervention.

### Deliverables

- [ ] **Pipeline checkpoint system** -- Save pipeline execution state after each node so crashed pipelines can be resumed
  - [ ] `p25.d1.t1` Add checkpoint support to executor.py
    > Modify executor.py to: (1) after each node completes, write a checkpoint to workspace/.orchestrator/checkpoint.json with: completed_nodes list, node_results, context state, pipeline_hash, (2) on startup, check for existing checkpoint and offer --resume mode that skips already-completed nodes, (3) validate checkpoint integrity (pipeline_hash must match current pipeline to prevent stale checkpoints), (4) clean up checkpoint on successful completion. Add --resume flag to executor CLI.
    _Files: ~/zion/projects/agent-orchestration/executor.py_
  - [ ] After each node completes, execution state is persisted to a checkpoint file
    _Validation: run pipeline, check checkpoint files exist after each node_
  - [ ] A crashed pipeline can be resumed from the last successful checkpoint
    _Validation: kill executor mid-pipeline, restart with --resume flag, verify it skips completed nodes_
  _~120 LOC_
- [ ] **Orphaned workspace detector** -- Detect and handle workspaces left behind by crashed orchestrator instances
  - [ ] `p25.d2.t1` Add orphan detection to workspace_manager.py
    > Add detect_orphans() function to workspace_manager.py: (1) find all workspaces with status "in-progress" or "active", (2) check if the orchestrator process that created them is still running (via PID stored in meta.json, if available), (3) check if the workspace has recent file activity (any changes in the last N minutes), (4) classify orphans as: recoverable (has checkpoint, can resume), stale (no recent activity, needs attention), or zombie (process dead, no checkpoint, needs manual review). Add --detect-orphans CLI flag.
    _Files: ~/zion/projects/agent-orchestration/workspace_manager.py_
  - [ ] Can identify workspaces with in-progress status but no active orchestrator process
    _Validation: create a stale workspace, run detector, verify it is flagged_
  _~80 LOC_
- [ ] **Graceful shutdown handler** -- Handle SIGTERM/SIGINT by saving state and cleaning up before exit
  - [ ] `p25.d3.t1` Add signal handlers to orchestrator.py
    > Add signal handlers to orchestrator.py: (1) on SIGTERM/SIGINT, finish current node (don't kill mid-execution), (2) update workspace meta.json status to "interrupted", (3) write a checkpoint so the pipeline can be resumed, (4) log the interruption event, (5) add a --graceful-timeout flag (default 30s) that forces exit if current node doesn't finish in time. This ensures the orchestrator can be safely stopped and restarted.
    _Files: ~/zion/projects/agent-orchestration/orchestrator.py_
  - [ ] Orchestrator saves state and updates workspace metadata when interrupted
    _Validation: send SIGTERM to running orchestrator, check workspace state is clean_
  _~60 LOC_
- [ ] **Resilience integration tests** -- Test crash recovery, orphan detection, and graceful shutdown scenarios
  - [ ] `p25.d4.t1` Create test_resilience.py
    > Create resilience tests: (1) run pipeline, kill process after node 2, verify --resume skips completed nodes and finishes, (2) create workspace with stale metadata, run orphan detector, verify classification, (3) send SIGTERM to orchestrator mid-loop, verify workspace is marked interrupted and checkpoint exists, (4) test double-crash scenario (resume, crash again, resume again). Use subprocess and signal modules for process management.
    _Files: ~/zion/projects/agent-orchestration/test_resilience.py_
  - [ ] Tests cover: kill mid-pipeline + resume, orphan detection, signal handling
    _Validation: python3 -m pytest test_resilience.py -v_
  _~120 LOC_

### Technical Notes

Checkpoints are simple JSON files in the workspace -- no database needed. The key insight is that pipeline execution is deterministic (same DAG, same order), so we only need to track which nodes are done, not the full state. Resilience is about making the orchestrator safe to run unattended, which is essential for the "Dark Factory" model from the research.

### Risks

- Checkpoint files could become corrupted if the crash happens mid-write -- use atomic writes (write to temp file, then rename)
- Resume could produce different results if external state changed between runs (e.g., main branch advanced)
- Signal handling in Python is tricky -- need to test on both foreground and background processes

## [ ] phase-26: Work Item Decomposition (Mayor Pattern) (PLANNED)

**Goal:** Enable the orchestrator to break down large or complex issues into smaller, independently executable sub-tasks

Gas Town's Mayor role acts as a concierge that distributes work, often decomposing complex tasks into sub-tasks for specialized workers. The current orchestrator treats each issue as a single unit of work -- a large feature request or refactoring issue gets assigned to one worker that must handle everything. This phase adds issue decomposition: an AI-powered analysis step that breaks complex issues into sub-tasks, creates sub-issues on GitHub, and orchestrates them through the pipeline. This directly implements the Mayor pattern and enables the "speculative ticket filing" workflow described in the research where engineers file high-level intent and the system decomposes into executable units.


### Deliverables

- [ ] **Issue complexity analyzer** -- Python module that analyzes an issue and determines if it needs decomposition
  - [ ] `p26.d1.t1` Create decomposer.py complexity analyzer
    > Python module that: (1) reads an issue's title, body, labels, and comments via gh CLI, (2) estimates complexity based on heuristics (body length, mentions of multiple files/components, keywords like "refactor", "migration", "redesign"), (3) uses a lightweight LLM call (via delegate_task) to assess if the issue spans multiple concerns, (4) outputs a classification: simple (pass through as-is) or complex (needs decomposition) with a confidence score. Threshold configurable in orchestrator.yaml.
    _Files: ~/zion/projects/agent-orchestration/decomposer.py_
  - [ ] Can classify issues as simple (single task) or complex (needs decomposition)
    _Validation: python3 decomposer.py --analyze ISSUE_NUM_
  _~120 LOC_
- [ ] **Sub-issue generator** -- AI-powered decomposition of complex issues into independently executable sub-tasks
  - [ ] `p26.d2.t1` Implement sub-issue generation
    > Add --decompose mode to decomposer.py: (1) call an LLM with the issue body and project context (AI_GUIDE.md, file tree), (2) prompt the LLM to produce sub-tasks with: title, body, affected files, dependencies between sub-tasks, estimated complexity, (3) validate sub-tasks are independently executable (no circular dependencies), (4) create sub-issues on GitHub via gh CLI with parent/child linking, (5) label sub-issues as agent-ready and link back to parent. Include --dry-run to preview decomposition without creating issues.
    _Files: ~/zion/projects/agent-orchestration/decomposer.py_
  - [ ] Can break a complex issue into 2-6 sub-issues with clear scope boundaries
    _Validation: python3 decomposer.py --decompose ISSUE_NUM --max-parts 6_
  _~150 LOC_
- [ ] **Decomposition integration with orchestrator** -- Wire decomposition into the orchestrator loop so complex issues are auto-decomposed before worker assignment
  - [ ] `p26.d3.t1` Integrate decomposer into orchestrator loop
    > Modify orchestrator.py run_loop() to: (1) after polling, run complexity analysis on each new issue, (2) for simple issues, proceed to spawner as before, (3) for complex issues, run decomposition, create sub-issues, label parent as "decomposed", (4) on next loop iteration, poll sub-issues as normal tasks, (5) when all sub-issues are complete, auto-close parent issue with summary comment. Add decompose_threshold and auto_decompose config options to orchestrator.yaml.
    _Files: ~/zion/projects/agent-orchestration/orchestrator.py_
  - [ ] Orchestrator automatically decomposes complex issues before spawning workers
    _Validation: create a complex test issue, run orchestrator, verify sub-issues created_
  _~80 LOC_
- [ ] **Decomposition pipeline template** -- Pipeline YAML that includes a decomposition step for complex tasks
  - [ ] `p26.d4.t1` Create decompose-pipeline.yaml
    > Create pipelines/decompose-pipeline.yaml: AI(analyze complexity) -> CONDITIONAL(simple: AI(implement) -> Bash(test) -> Bash(commit), complex: AI(decompose) -> Bash(create sub-issues) -> END). Requires a CONDITIONAL node type or equivalent branching logic. If CONDITIONAL is too complex, create two separate pipeline templates and let the orchestrator select based on complexity analysis.
    _Files: ~/zion/projects/agent-orchestration/pipelines/decompose-pipeline.yaml_
  - [ ] Pipeline template exists with a decomposition-aware flow
    _Validation: read pipeline YAML_
  _~50 LOC_

### Technical Notes

Decomposition quality depends on the LLM prompt. Start conservative: only decompose issues with high confidence scores. The sub-issue creation via gh CLI is the key mechanism -- it mirrors how Gas Town's Mayor distributes work. Keep sub-issues small enough to complete in a single pipeline run.

### Risks

- LLM decomposition may produce overlapping or poorly scoped sub-tasks -- need validation
- Sub-issue creation rate could hit GitHub API limits for large batches
- Parent issue tracking gets complex if sub-issues are reassigned or closed manually

## [ ] phase-27: Live Terminal Dashboard (Witness Pattern) (PLANNED)

**Goal:** Build a real-time terminal dashboard that displays orchestrator state, worker activity, and pipeline progress

Gas Town's Witness role provides "observation and logging" as a first-class concern. Symphony's reference implementation includes a Phoenix live dashboard. The current orchestrator has status.sh (static snapshot) and orch_history.py (post-hoc queries) but no live view. This phase builds a terminal-based dashboard using rich/textual that auto-refreshes and shows: active workers with real-time progress, pipeline execution state, queue depth, recent completions/failures, and system health. This is the "Status Surface" component from the Symphony architecture, making the orchestrator's state visible at a glance without running CLI commands.


### Deliverables

- [ ] **Dashboard framework** -- Terminal dashboard with auto-refreshing panels for orchestrator state
  - [ ] `p27.d1.t1` Create dashboard.py with rich/textual layout
    > Python script using the rich library (already commonly available) that renders a terminal dashboard with panels: (1) Workers panel -- list of active workspaces with status, role, elapsed time, (2) Queue panel -- pending issues count, labels breakdown, (3) Recent panel -- last 10 completed/failed pipeline runs with status indicators, (4) System panel -- disk usage, log sizes, uptime. Auto-refresh every 5 seconds. Use rich.layout.Table and rich.live.Live for rendering. Fall back to plain text if rich is not installed.
    _Files: ~/zion/projects/agent-orchestration/dashboard.py_
  - [ ] Dashboard renders in terminal with multiple panels showing live data
    _Validation: python3 dashboard.py_
  _~150 LOC_
- [ ] **Real-time workspace monitoring** -- Watch workspace filesystem for changes and update dashboard in real-time
  - [ ] `p27.d2.t1` Add filesystem watcher to dashboard
    > Add filesystem monitoring to dashboard.py: (1) watch workspace directories for file changes (creation, modification, deletion), (2) display last N file events per workspace, (3) compute "activity score" based on recent file operations, (4) highlight inactive workers (no file changes in N minutes) in yellow/red. Use simple polling (os.scandir + mtime) rather than inotify for cross-platform compatibility.
    _Files: ~/zion/projects/agent-orchestration/dashboard.py_
  - [ ] Dashboard shows live file modification timestamps per active workspace
    _Validation: create files in workspace, observe dashboard update_
  _~80 LOC_
- [ ] **Pipeline execution visualization** -- Show active pipeline DAGs with node-by-node progress highlighting
  - [ ] `p27.d3.t1` Add DAG visualization to dashboard
    > Add pipeline visualization to dashboard.py: (1) read checkpoint files from active workspaces, (2) render the pipeline DAG as an ASCII tree showing node names with status icons (checkmark for completed, spinner for active, dot for pending, X for failed), (3) show current node duration and total pipeline elapsed time, (4) allow selecting a workspace to view its pipeline detail.
    _Files: ~/zion/projects/agent-orchestration/dashboard.py_
  - [ ] Dashboard renders the current pipeline DAG with completed/active/pending nodes
    _Validation: run a pipeline, observe dashboard shows DAG progress_
  _~100 LOC_
- [ ] **Dashboard launcher and cron integration** -- Easy launch command and optional integration with orchestrator cron
  - [ ] `p27.d4.t1` Add dashboard CLI and update status.sh
    > Add CLI arguments to dashboard.py: --watch (auto-refresh interval), --focus (specific workspace or panel), --export (save snapshot as text). Update status.sh to mention the dashboard as an alternative to the static status view. Add a note to the orchestrator cron prompt that the dashboard can be run in a separate terminal to monitor orchestrator activity.
    _Files: ~/zion/projects/agent-orchestration/dashboard.py, ~/zion/projects/agent-orchestration/status.sh_
  - [ ] Single command launches the dashboard; can be run alongside orchestrator
    _Validation: python3 dashboard.py starts and updates_
  _~50 LOC_

### Technical Notes

Use rich (pip install rich) for terminal rendering -- it's lightweight, widely available, and produces beautiful output. If rich is not installed, fall back to plain-text tables. The dashboard is read-only -- it never modifies orchestrator state. Keep refresh interval configurable to balance responsiveness with resource usage.

### Risks

- rich library may not be installed -- need graceful fallback to plain text
- Terminal rendering may be slow with many workspaces -- need pagination or filtering
- Dashboard could consume noticeable CPU if refresh interval is too aggressive

## [ ] phase-28: Speculative Execution and Parallel Exploration (PLANNED)

**Goal:** Enable the orchestrator to run multiple solution strategies in parallel and select the best outcome

The Harness Engineering research describes running "100 parallel Ralph Wiggum loops to explore different architectural approaches, only keeping the one that passes the most rigorous quality gates." The current orchestrator assigns one worker per issue with one pipeline. This phase adds speculative execution: for complex issues, spawn multiple workers with different strategies (different roles, different prompts, different pipeline templates), run them in parallel, evaluate outcomes against quality gates, and keep the best result. This transforms the orchestrator from a single-path executor into a multi-strategy optimizer, directly applying the "code is disposable" philosophy from the Dark Factory model.


### Deliverables

- [ ] **Strategy definition system** -- Define multiple solution strategies per issue type that the orchestrator can execute in parallel
  - [ ] `p28.d1.t1` Create strategy YAML schema and loader
    > Define strategies/ directory with YAML files. Each strategy specifies: name, applicable_labels (which issue types it handles), role_override (different role than default), prompt_additions (extra context for this strategy), pipeline (which pipeline template to use), weight (priority for resource allocation), quality_threshold (minimum score to be considered). Create a strategies.py loader that matches issues to applicable strategies. Default strategies: conservative (implementer + standard pipeline), aggressive (implementer + team pipeline), exploratory (coordinator plan first, then implement).
    _Files: ~/zion/projects/agent-orchestration/strategies/, ~/zion/projects/agent-orchestration/strategies.py_
  - [ ] Can define 2+ strategies for a given issue type with different roles, prompts, and pipelines
    _Validation: read strategy YAML configs_
  _~120 LOC_
- [ ] **Parallel execution manager** -- Spawn and manage multiple workers for the same issue using different strategies
  - [ ] `p28.d2.t1` Add speculative execution to orchestrator
    > Add --speculative mode to orchestrator.py: (1) for a given issue, create N workspaces (one per strategy), (2) spawn workers in parallel using existing concurrency limits, (3) each worker runs its strategy's pipeline independently, (4) track speculative runs in workspace metadata (strategy_name, parent_issue, is_speculative=true), (5) report speculative run status alongside normal runs. Add max_speculative config option (default 3) to prevent resource exhaustion.
    _Files: ~/zion/projects/agent-orchestration/orchestrator.py, ~/zion/projects/agent-orchestration/spawner.py_
  - [ ] Can spawn N workers for the same issue, each with a different strategy
    _Validation: python3 orchestrator.py --speculative ISSUE_NUM --strategies conservative,aggressive_
  _~100 LOC_
- [ ] **Outcome evaluator** -- Evaluate completed speculative runs against quality gates and select the best outcome
  - [ ] `p28.d3.t1` Create outcome evaluator module
    > Create evaluator.py module: (1) read execution logs from all speculative runs for an issue, (2) compute quality score per run based on: test pass rate, lint violations, code coverage delta, execution time, pipeline completion (did all nodes succeed), (3) weight factors configurable in strategies.yaml, (4) output ranked list of runs with scores, (5) select winner and mark its workspace as the primary result, (6) archive non-winning workspaces. Add --compare flag to compare two specific runs.
    _Files: ~/zion/projects/agent-orchestration/evaluator.py_
  - [ ] Can compare multiple completed runs and select the one with the highest quality score
    _Validation: run two strategies, verify evaluator picks the better one_
  _~120 LOC_
- [ ] **Speculative pipeline template** -- Pipeline YAML that orchestrates parallel strategy execution and evaluation
  - [ ] `p28.d4.t1` Create speculative-pipeline.yaml
    > Create pipelines/speculative-pipeline.yaml documenting the speculative flow. Since true parallel execution requires orchestrator-level coordination (not pipeline-level), this is a meta-pipeline template that the orchestrator uses as a blueprint: (1) select applicable strategies, (2) spawn parallel workers, (3) wait for all to complete, (4) run evaluator, (5) commit winner, (6) archive losers, (7) post summary to issue. Include cost estimate per speculative run.
    _Files: ~/zion/projects/agent-orchestration/pipelines/speculative-pipeline.yaml_
  - [ ] Pipeline template exists for the full speculative flow (decompose -> parallel execute -> evaluate -> commit)
    _Validation: read pipeline YAML_
  _~60 LOC_

### Technical Notes

Speculative execution is resource-intensive. Default to off. Only enable for issues labeled "explore" or when explicitly requested. The evaluator should be deterministic (test results, lint) not inferential (LLM review) to avoid adding cost. Consider a "tournament mode" that runs strategies head-to-head on the same issue and tracks win rates over time.

### Risks

- Speculative execution multiplies token costs -- need strict budgeting and opt-in
- Workspace proliferation -- N strategies per issue means N workspaces to manage
- Evaluator may pick the wrong winner if quality metrics don''t capture the right signals
- Not all issues benefit from exploration -- simple bugs should use the standard path

## [ ] phase-29: Agent Strategy A/B Testing and Analytics (PLANNED)

**Goal:** Track the performance of different agent strategies, roles, and pipeline configurations over time to optimize orchestrator effectiveness

The Dark Factory model treats code as disposable and experiments with approaches. The research mentions that "when an agent failed, the team analyzed the environment for missing capabilities rather than refining prompts." The current orchestrator has no mechanism to compare different configurations or track which strategies lead to successful outcomes. This phase adds experiment tracking: label pipeline runs with their configuration (role, pipeline, prompt version, model), compute success metrics per configuration, and provide statistical analysis to identify which configurations perform best for different issue types. This enables data-driven optimization of the orchestrator's harness, moving from "guess and check" to "measure and improve."


### Deliverables

- [ ] **Experiment tracking schema** -- Extend execution logs to capture configuration metadata for each run
  - [ ] `p29.d1.t1` Extend execution_log.py with config tracking
    > Modify execution_log.py to: (1) accept config_metadata parameter with role, pipeline_name, strategy, model, prompt_version, orchestrator_version, (2) compute a config_hash (SHA256 of key config fields) for grouping, (3) store config_metadata alongside execution results, (4) add config_metadata to the run JSON output. Backward compatible -- if metadata is missing, use defaults.
    _Files: ~/zion/projects/agent-orchestration/execution_log.py_
  - [ ] Execution logs include role, pipeline, strategy, and config hash for each run
    _Validation: run a pipeline, check execution log includes config metadata_
  _~60 LOC_
- [ ] **Performance analytics engine** -- Compute per-configuration success rates, average durations, and quality scores
  - [ ] `p29.d2.t1` Create analytics.py module
    > Create analytics.py that: (1) reads execution logs with config metadata, (2) groups runs by config_hash, role, pipeline, strategy, issue_type, (3) computes per-group metrics: success_rate, avg_duration, avg_test_pass_rate, total_runs, (4) identifies statistical significance (is strategy A significantly better than strategy B?), (5) outputs as formatted table or JSON. Support --by flag to group by different dimensions, --period for time windowing, --top N to show best/worst performers.
    _Files: ~/zion/projects/agent-orchestration/analytics.py_
  - [ ] Can report success rate and average duration grouped by role, pipeline, and strategy
    _Validation: python3 analytics.py --by-role --period week_
  _~150 LOC_
- [ ] **Configuration recommendation engine** -- Suggest optimal role/pipeline/strategy combinations based on historical performance for each issue type
  - [ ] `p29.d3.t1` Add recommendation engine to analytics.py
    > Add --recommend mode to analytics.py: (1) for a given issue type (determined by labels or title keywords), look up historical performance of all configurations, (2) rank configurations by success_rate * (1 / avg_duration) -- balancing quality and speed, (3) require minimum N runs (default 5) before making a recommendation, (4) output recommendation with confidence level and supporting data, (5) if no sufficient data, recommend the default configuration. This feeds into the orchestrator's strategy selection in phase 28.
    _Files: ~/zion/projects/agent-orchestration/analytics.py_
  - [ ] Can recommend the best configuration for a given issue type based on historical data
    _Validation: python3 analytics.py --recommend --issue-type bug_
  _~80 LOC_
- [ ] **Analytics dashboard integration** -- Add analytics panels to the live dashboard from phase 27
  - [ ] `p29.d4.t1` Add analytics panel to dashboard.py
    > Add an "Analytics" panel to dashboard.py from phase 27: (1) show per-role success rate for last 50 runs, (2) show per-pipeline success rate, (3) show top 3 performing configurations, (4) show trend indicator (improving/declining) compared to previous period. Panel updates on each refresh cycle by calling analytics.py.
    _Files: ~/zion/projects/agent-orchestration/dashboard.py_
  - [ ] Dashboard shows per-role success rates and recent performance trends
    _Validation: run dashboard, check analytics panel renders_
  _~60 LOC_

### Technical Notes

A/B testing requires a sufficient volume of runs to be meaningful. The recommendation engine should be conservative -- only recommend when there's enough data (minimum 5 runs per configuration per issue type). Use simple statistical tests (proportion z-test for success rates) rather than complex ML. The analytics module should be fast enough to run on every dashboard refresh.

### Risks

- Low run volume makes statistics unreliable -- need clear confidence indicators
- Issue type classification may be noisy (labels are often inconsistent)
- Recommendations could lead to configuration lock-in if one strategy dominates early
- Analytics queries could be slow on large log histories -- need indexing or aggregation

## [ ] phase-30: Inter-Agent Communication and Shared State (Beads Pattern) (PLANNED)

**Goal:** Implement lightweight shared state between concurrent workers so agents can coordinate on related tasks

Gas Town's Beads database enables agents to share state -- when one worker modifies a file that another worker depends on, the system coordinates. The current orchestrator runs workers in complete isolation with no awareness of each other. This phase adds a lightweight coordination layer: a shared state file that tracks which files each worker is modifying, a notification mechanism so workers can learn about related changes, and conflict-aware scheduling that prevents workers from stepping on each other. This is a simpler alternative to Gas Town's full Dolt-based Beads system, using filesystem-based coordination instead of a version-controlled SQL database. This enables the "pull-based" work distribution pattern where workers can react to each other's progress rather than operating in silos.


### Deliverables

- [ ] **Shared state registry** -- File-backed registry that tracks which files are being modified by which workers
  - [ ] `p30.d1.t1` Create shared_state.py module
    > Create shared_state.py: (1) maintain a JSON-backed registry at ~/.orchestrator/state/shared-state.json, (2) register(worker_id, files_list) -- claim files for a worker, (3) unregister(worker_id) -- release all claimed files, (4) query(file_path) -- check if a file is locked and by whom, (5) query_conflicts(worker_id, files_list) -- check if any of the proposed files conflict with existing locks, (6) auto-expire locks after configurable timeout (default 2 hours) to handle crashed workers. Use file locking (fcntl.flock) for concurrent access safety.
    _Files: ~/zion/projects/agent-orchestration/shared_state.py_
  - [ ] Workers can register and unregister file locks; other workers can query active locks
    _Validation: python3 shared_state.py register --worker 42 --files src/main.py_
  _~120 LOC_
- [ ] **Conflict-aware scheduling** -- Modify orchestrator to check shared state before spawning workers and skip file-conflicting tasks
  - [ ] `p30.d2.t1` Add conflict checking to orchestrator spawner
    > Modify orchestrator.py and spawner.py: (1) before spawning a worker, estimate which files the issue will touch (parse issue body for file mentions, check issue labels for component hints), (2) call shared_state.query_conflicts() to check for active locks, (3) if conflicts found, skip this issue and log "deferred due to file conflict with worker N", (4) on next loop iteration, re-check deferred issues. Add conflict_strategy config: skip (default), queue (wait until clear), warn (proceed but log warning).
    _Files: ~/zion/projects/agent-orchestration/orchestrator.py, ~/zion/projects/agent-orchestration/spawner.py_
  - [ ] Orchestrator delays spawning a worker if its target files conflict with an active worker
    _Validation: create two issues touching the same file, verify second is delayed_
  _~80 LOC_
- [ ] **Worker notification channel** -- Simple notification mechanism so workers can learn about related changes from other workers
  - [ ] `p30.d3.t1` Add notification channel to shared_state.py
    > Extend shared_state.py with notifications: (1) post_notification(worker_id, message, related_files) -- write a notification to ~/.orchestrator/state/notifications.jsonl, (2) get_notifications(since_timestamp, related_files) -- retrieve notifications relevant to a worker, (3) auto-clean notifications older than 24 hours. In executor.py, when an AI node starts, check for notifications about files in its workspace and include them in the prompt as "Related changes by other workers: ..." This enables agents to be aware of concurrent activity.
    _Files: ~/zion/projects/agent-orchestration/shared_state.py, ~/zion/projects/agent-orchestration/executor.py_
  - [ ] Worker A can post a notification that Worker B reads when it starts
    _Validation: post notification, start worker, verify it reads the notification_
  _~80 LOC_
- [ ] **Integration tests for coordination** -- Test concurrent worker coordination, conflict detection, and notification delivery
  - [ ] `p30.d4.t1` Create test_shared_state.py
    > Create test_shared_state.py: (1) test register/unregister with concurrent access (multiple threads), (2) test conflict detection with overlapping file sets, (3) test lock expiration after timeout, (4) test notification post/retrieve lifecycle, (5) test file locking safety under concurrent writes, (6) test orchestrator conflict-aware scheduling with mocked workers. Use threading for concurrency tests.
    _Files: ~/zion/projects/agent-orchestration/test_shared_state.py_
  - [ ] Tests verify that concurrent workers coordinate correctly and conflicts are detected
    _Validation: python3 -m pytest test_shared_state.py -v_
  _~100 LOC_

### Technical Notes

This is a deliberately simple implementation of Beads -- filesystem-based rather than database-backed. The shared state JSON file is the coordination point. File locking (fcntl.flock on Linux) ensures safe concurrent access. For production scale, this could be upgraded to SQLite or Dolt, but JSON files are sufficient for the Hermes orchestrator's expected workload (10-20 concurrent workers).

### Risks

- File locking may not work on all filesystems (NFS, FUSE) -- document limitations
- File conflict estimation from issue body is imprecise -- workers may touch more files than expected
- Notification delivery adds latency to AI node startup
- Shared state file could become a bottleneck with many workers -- consider sharding

## [ ] phase-31: Self-Verifying Agent Toolkit (PLANNED)

**Goal:** Enable agents to verify their own work through automated UI testing, CLI output validation, and integration checks -- the 'agents drive application-level tools' pattern from Symphony

The Symphony research emphasizes that agents should be able to "drive application-level tools, such as Chrome DevTools or CLI scripts, to verify their own work before submitting a pull request." Currently, our pipeline relies on bash nodes running tests and linters, but agents cannot perform higher-order verification like checking UI output, API responses, or end-to-end behavior. This phase adds a verification toolkit that provides reusable verification primitives agents can call to self-validate their changes before pipeline completion.

### Deliverables

- [ ] **Verification primitives library** -- Python module with reusable verification functions for common self-check patterns
  - [ ] `p31.d1.t1` Create verify.py module
    > Create verify.py with verification primitives: (1) assert_file_exists(path, pattern), (2) assert_output_contains(cmd, expected), (3) assert_api_responds(url, status, body_contains), (4) assert_command_succeeds(cmd, timeout), (5) assert_config_valid(yaml_path, schema), (6) assert_no_regression(baseline_path, current_output). Each returns structured JSON result. Add --baseline flag to capture expected outputs for regression testing.
    _Files: ~/zion/projects/agent-orchestration/verify.py_
  - [ ] Module provides at least 6 verification primitives (file exists, output contains, API responds, command succeeds, config valid, no regressions)
    _Validation: python3 verify.py --list_
  _~150 LOC_
- [ ] **VERIFY node type for DAG executor** -- Add a VERIFY node type that runs verification primitives from the pipeline
  - [ ] `p31.d2.t1` Add VERIFY node type to DAG (depends: p31.d1.t1)
    > Add NodeType.VERIFY to dag.py. The verify node takes: checks (list of verification primitives with args), baseline_dir (directory for baseline files), and on_fail (stop/warn/continue). Executor calls verify.run_checks(). Each check result is logged. If any check fails and on_fail=stop, the node fails (stopping the pipeline).
    _Files: ~/zion/projects/agent-orchestration/dag.py, ~/zion/projects/agent-orchestration/executor.py_
  - [ ] Pipeline YAML can include VERIFY nodes that run verification checks
    _Validation: create pipeline with verify node, execute it_
  _~80 LOC_
- [ ] **Self-verification pipeline template** -- Pipeline YAML that adds verification gates before the commit step
  - [ ] `p31.d3.t1` Create verify-pipeline.yaml (depends: p31.d2.t1)
    > Create pipelines/verify-pipeline.yaml based on standard-pipeline.yaml but with VERIFY nodes after implementation and after tests: AI(implement) -> VERIFY(output structure) -> Bash(test) -> VERIFY(test results) -> AI(review) -> VERIFY(no regressions) -> Bash(commit). Verification gates ensure agents self-validate before committing.
    _Files: ~/zion/projects/agent-orchestration/pipelines/verify-pipeline.yaml_
  - [ ] Pipeline template exists with VERIFY nodes before commit
    _Validation: read YAML, trace through nodes_
  _~60 LOC_
- [ ] **Baseline management CLI** -- CLI to capture, update, and compare verification baselines
  - [ ] `p31.d4.t1` Add baseline management to verify.py (depends: p31.d1.t1)
    > Add baseline subcommands to verify.py: capture (save current output as baseline), compare (run checks against baselines), update (update baselines with new expected values), diff (show differences between current and baseline). Baselines stored as JSON files in a configurable directory. Include --auto-update flag for non-interactive baseline refresh.
    _Files: ~/zion/projects/agent-orchestration/verify.py_
  - [ ] Can capture baselines, compare against them, and update them
    _Validation: python3 verify.py --baseline capture --dir baselines/_
  _~80 LOC_

### Technical Notes

Verification primitives are the "self-verifying agent" concept from Symphony. They differ from bash test nodes in that they are structured assertions with baseline tracking, not raw shell commands. This makes them composable and agent-readable.

### Risks

- Baselines can become stale if the project evolves -- need a refresh strategy
- Some verifications (API responses, UI) may be flaky in CI environments
- Over-verification can slow down pipelines -- keep verification fast and focused

## [ ] phase-32: Token Cost Tracking and Budget Enforcement (PLANNED)

**Goal:** Add cost visibility and token budget enforcement to the orchestrator so autonomous operation doesn''t escalate costs unexpectedly

The Harness Engineering research highlights extreme token consumption: "over one billion output tokens per day" at $2,000-3,000 daily. The Symphony config includes agent.max_turns and agent.max_concurrent to control costs. Our orchestrator has no cost tracking -- we don't know how many tokens each pipeline run consumes, and there's no way to set a budget ceiling. This phase adds token estimation, cost tracking per pipeline run, configurable budget limits, and alerts when spending approaches thresholds. Essential for running the orchestrator autonomously without financial surprises.

### Deliverables

- [ ] **Token cost estimator** -- Module that estimates token usage and cost for pipeline runs based on model, context size, and node count
  - [ ] `p32.d1.t1` Create cost_tracker.py module
    > Create cost_tracker.py: (1) estimate_tokens(prompt, model) -- rough token count based on character length and model tokenizer, (2) estimate_cost(tokens, model) -- lookup table for per-token costs (claude-sonnet, claude-opus, gpt-4, etc.), (3) record_usage(run_id, node_id, model, input_tokens, output_tokens) -- persist to ~/.orchestrator/logs/costs/, (4) get_run_cost(run_id) -- sum costs for a pipeline run, (5) get_daily_cost(date) -- aggregate daily spending. Include a model_pricing.yaml config with current model prices.
    _Files: ~/zion/projects/agent-orchestration/cost_tracker.py, ~/zion/projects/agent-orchestration/model_pricing.yaml_
  - [ ] Can estimate token cost for a pipeline before execution
    _Validation: python3 cost_tracker.py --estimate --pipeline pipelines/standard-pipeline.yaml_
  _~150 LOC_
- [ ] **Cost tracking integration with executor** -- Record token usage after each AI node execution in the pipeline
  - [ ] `p32.d2.t1` Add cost tracking to executor AI nodes (depends: p32.d1.t1)
    > After each AI node execution in executor.py, estimate token usage from the prompt size and output size. Record the usage via cost_tracker.record_usage(). Include the cost in the NodeResult output. Add total_cost to the execution log run summary.
    _Files: ~/zion/projects/agent-orchestration/executor.py_
  - [ ] Executor records estimated token usage for each AI node
    _Validation: run pipeline, check cost logs_
  _~60 LOC_
- [ ] **Budget enforcement** -- Configurable budget limits that prevent pipelines from exceeding cost thresholds
  - [ ] `p32.d3.t1` Add budget enforcement to executor (depends: p32.d1.t1, p32.d2.t1)
    > Add budget enforcement to DAGExecutor: (1) check budget before each AI node execution, (2) if remaining budget < estimated node cost, skip or fail the node, (3) support per-run budget (--budget 5.00) and daily budget (cost_tracker.get_remaining_daily_budget()), (4) log budget exceeded events. Add budget field to pipeline YAML env vars.
    _Files: ~/zion/projects/agent-orchestration/executor.py, ~/zion/projects/agent-orchestration/cost_tracker.py_
  - [ ] Pipeline stops when budget limit is reached
    _Validation: set low budget, run pipeline, verify it stops_
  _~80 LOC_
- [ ] **Cost reporting in status and history** -- Show cost data in status.sh and orch_history.py
  - [ ] `p32.d4.t1` Add cost section to status.sh and orch_history.py (depends: p32.d1.t1)
    > Add a "Costs" section to status.sh showing: today's spend, this week's spend, remaining daily budget, most expensive runs. Update orch_history.py show command to include cost per run. Add orch_history.py cost subcommand for cost analytics (daily, weekly, per-pipeline, per-role).
    _Files: ~/zion/projects/agent-orchestration/status.sh, ~/zion/projects/agent-orchestration/orch_history.py_
  - [ ] status.sh shows daily cost and remaining budget
    _Validation: run status.sh, check for cost section_
  _~80 LOC_

### Technical Notes

Token estimation is inherently approximate since we don't have access to actual tokenizer counts from the LLM provider. Use character-based heuristics (1 token ~ 4 chars for English) as a reasonable estimate. Model pricing should be updated periodically as providers change prices.

### Risks

- Token estimation accuracy varies by model and content type
- Budget enforcement based on estimates may be too aggressive or too lenient
- Model pricing changes frequently -- need a way to update without code changes
- Daily budget may not account for shared infrastructure costs

## [ ] phase-33: Application Legibility Toolkit (PLANNED)

**Goal:** Build automated tools that make codebases directly understandable and verifiable by agents -- the "Application Legibility" principle from Harness Engineering

The Harness Engineering research emphasizes "Application Legibility" -- making software directly understandable and verifiable by the agent. This includes: integrated observability (local access to logs/metrics/traces), rigid architecture enforcement (strict layering limits agent search space), and constraints enforced mechanically via structural tests. Phase 17 covers structural invariants but focuses on checking existing code. This phase goes further: it provides tools that help agents UNDERSTAND a codebase quickly (architecture maps, dependency graphs, entry point discovery) and tools that help projects BECOME more legible (architecture linter, module boundary checker).

### Deliverables

- [ ] **Codebase comprehension module** -- Module that generates agent-readable summaries of a codebase''s architecture and structure
  - [ ] `p33.d1.t1` Create legibility.py module
    > Create legibility.py: (1) analyze_architecture(project_dir) -- scan directory structure, detect layers (types, config, repo, service), identify entry points, map dependencies, output as structured JSON, (2) generate_architecture_doc(project_dir) -- create a markdown architecture overview suitable for AI_GUIDE.md, (3) find_entry_points(project_dir) -- detect main files, API routes, CLI entry points, (4) map_dependencies(project_dir) -- build an import dependency graph, detect circular dependencies, identify unused modules. Output agent-readable summaries that help autonomous agents quickly understand a new codebase.
    _Files: ~/zion/projects/agent-orchestration/legibility.py_
  - [ ] Module can analyze a codebase and output an architecture summary
    _Validation: python3 legibility.py --analyze /path/to/project_
  _~180 LOC_
- [ ] **Architecture linter** -- Linter that enforces architectural rules (layer boundaries, dependency direction, module isolation)
  - [ ] `p33.d2.t1` Add architecture linting to legibility.py (depends: p33.d1.t1)
    > Add linting rules to legibility.py: (1) layer_boundary_check -- ensure modules in "service" layer don't import from "types" layer directly (configurable layer rules), (2) dependency_direction_check -- enforce allowed import directions, (3) module_isolation_check -- detect circular imports and unintended cross-module dependencies, (4) entry_point_check -- verify entry points follow project conventions. Rules configured via arch_rules.yaml. Output violations as structured JSON with file:line:rule:severity format compatible with the GC scanner.
    _Files: ~/zion/projects/agent-orchestration/legibility.py, ~/zion/projects/agent-orchestration/arch_rules.yaml_
  - [ ] Linter can check at least 4 architectural rules
    _Validation: python3 legibility.py --lint /path/to/project_
  _~120 LOC_
- [ ] **Legibility scoring** -- Quantitative score measuring how agent-legible a codebase is
  - [ ] `p33.d3.t1` Add legibility scoring to legibility.py (depends: p33.d1.t1, p33.d2.t1)
    > Add scoring to legibility.py: (1) architecture_score -- how well-organized the directory structure is, (2) documentation_score -- presence of AI_GUIDE.md, README, docstrings, (3) test_score -- test coverage estimate, (4) convention_score -- naming consistency, import style, (5) overall score as weighted average. Track scores over time in ~/.orchestrator/logs/legibility/ to detect drift. Include --compare flag to compare current score against a baseline.
    _Files: ~/zion/projects/agent-orchestration/legibility.py_
  - [ ] Module outputs a legibility score (0-100) with breakdown by category
    _Validation: python3 legibility.py --score /path/to/project_
  _~80 LOC_
- [ ] **Integration with GC and onboarding** -- Wire legibility checks into the GC scanner and project onboarding bootstrap
  - [ ] `p33.d4.t1` Integrate legibility into GC and onboarding (depends: p33.d1.t1, p33.d2.t1, p33.d3.t1)
    > Add a legibility check to gc-pipeline.yaml as a Bash node that runs legibility.py --lint and --score. If score drops below threshold, flag for remediation. Update the project onboarding bootstrap (phase 24) to run legibility.py --analyze and include the architecture summary in the generated AI_GUIDE.md. This closes the loop: onboarding creates legible projects, GC ensures they stay legible.
    _Files: ~/zion/projects/agent-orchestration/pipelines/gc-pipeline.yaml_
  - [ ] GC pipeline includes legibility score check, onboarding generates architecture doc
    _Validation: read pipeline YAML, check onboarding prompt_
  _~40 LOC_

### Technical Notes

Application legibility is the key insight from Harness Engineering: "code is free, but attention is scarce." Making codebases legible reduces the attention (tokens) agents need to understand them, directly reducing costs. The scoring system creates a measurable proxy for "how easy is this codebase for an AI to work with?"

### Risks

- Architecture analysis may be slow for large codebases -- need caching
- Layer detection heuristics may not match all project structures
- Legibility score could be gamed (e.g., adding docstrings without content) -- need quality weighting

## [ ] phase-34: Agent-Generated Tooling (PLANNED)

**Goal:** Enable the orchestrator to generate its own quality tools (linters, tests, validators) as part of the development pipeline -- the "structural tests and custom linters often generated by agents" pattern from Harness Engineering

The Harness Engineering research notes that "structural tests and custom linters (often generated by agents)" enforce application legibility mechanically. This is a powerful meta-pattern: agents not only write code but also create the tools that verify code quality. Currently, our orchestrator runs pre-defined pipelines with fixed test/lint commands. This phase adds the ability for the orchestrator to: (1) detect when a project needs custom validation rules, (2) generate linters/tests/checks for those rules, (3) integrate the generated tools into subsequent pipeline runs. This creates a self-improving quality loop where the harness gets better as the codebase grows.

### Deliverables

- [ ] **Tool generation module** -- Module that generates custom linters, tests, and validators from project patterns
  - [ ] `p34.d1.t1` Create tool_gen.py module
    > Create tool_gen.py: (1) detect_patterns(project_dir) -- analyze codebase for recurring patterns (naming conventions, error handling patterns, import styles, API patterns), (2) generate_linter(patterns) -- create a Python linter script that checks for pattern adherence, (3) generate_tests(project_dir) -- generate test stubs for untested modules based on function signatures and docstrings, (4) generate_validator(schema) -- create a validation script from a JSON/YAML schema. Output generated tools to a tools/ directory in the project. Include --dry-run to preview without writing.
    _Files: ~/zion/projects/agent-orchestration/tool_gen.py_
  - [ ] Module can analyze a project and generate a custom linter
    _Validation: python3 tool_gen.py --analyze /path/to/project --generate linter_
  _~180 LOC_
- [ ] **Generated tool integration with pipelines** -- Pipeline node type that runs agent-generated tools alongside standard checks
  - [ ] `p34.d2.t1` Add GENERATED_TOOL node type to DAG (depends: p34.d1.t1)
    > Add NodeType.GENERATED_TOOL to dag.py. The generated_tool node takes: tool_path (path to generated linter/test/validator), args (command-line arguments), and auto_generate (bool, if true run tool_gen.py before executing). Executor runs the generated tool as a bash subprocess with configurable timeout. If auto_generate=true, first runs tool_gen.py to ensure the tool is up-to-date with current project patterns.
    _Files: ~/zion/projects/agent-orchestration/dag.py, ~/zion/projects/agent-orchestration/executor.py_
  - [ ] Pipeline YAML can include GENERATED_TOOL nodes
    _Validation: create pipeline with generated tool node, execute it_
  _~80 LOC_
- [ ] **Self-improving quality loop** -- Pipeline that generates tools, runs them, and updates the toolset based on findings
  - [ ] `p34.d3.t1` Create self-improving pipeline YAML (depends: p34.d2.t1)
    > Create pipelines/self-improve-pipeline.yaml: AI(analyze patterns) -> Bash(generate linter) -> Bash(run generated linter) -> AI(review findings, update rules) -> Bash(generate updated linter) -> Bash(run updated linter) -> Bash(commit tools). This pipeline creates a feedback loop where quality tools evolve with the codebase.
    _Files: ~/zion/projects/agent-orchestration/pipelines/self-improve-pipeline.yaml_
  - [ ] Pipeline YAML exists that generates and runs custom tools
    _Validation: read pipeline YAML_
  _~60 LOC_
- [ ] **Tool registry and versioning** -- Track generated tools, their version, and effectiveness over time
  - [ ] `p34.d4.t1` Add tool registry to tool_gen.py (depends: p34.d1.t1)
    > Add a tool registry to tool_gen.py stored in ~/.orchestrator/tools/registry.json. Track: tool name, project, generated_at, version, pattern_count (number of patterns detected), effectiveness (violation count trend), last_run, last_updated. Support --registry list, --registry update, --registry retire (mark old tools as deprecated). Include a version suffix on generated tools (linter_v1.py, linter_v2.py) to track evolution.
    _Files: ~/zion/projects/agent-orchestration/tool_gen.py_
  - [ ] Generated tools are tracked in a registry with version history
    _Validation: python3 tool_gen.py --registry list_
  _~80 LOC_

### Technical Notes

Agent-generated tooling is the "harness builds the harness" concept. The key insight is that agents are better at detecting patterns in code than humans writing static rules. By generating linters from observed patterns, the tools stay in sync with the codebase evolution. Generated tools should be treated as disposable -- they can be regenerated at any time from the current codebase state.

### Risks

- Generated linters may be too strict or too lenient -- need human review for critical rules
- Tool regeneration could break existing pipelines if the interface changes
- Generated tools may have bugs themselves -- need to test the tools
- Auto-generation on every pipeline run could be slow -- cache and only regenerate when patterns change

## [ ] phase-35: Dark Factory Mode (Full Autonomous Operation) (PLANNED)

**Goal:** Enable fully autonomous "dark factory" operation where the orchestrator manages a codebase with zero human code review, using the complete harness (sensors, gates, budgets, verification) to ensure quality

The Harness Engineering research describes the "Dark Factory" model: "a small team built an internal software product with zero manually-written code" and "moved toward a Dark Factory model where no human reviewed the code before it was merged into the main branch." This is the endgame of the orchestrator: combining all previous phases into a mode where the orchestrator can autonomously develop a codebase end-to-end. Phases 1-34 build individual capabilities; this phase integrates them into a cohesive autonomous operation mode with confidence scoring, progressive trust escalation, and emergency stops. This is NOT about removing humans from the loop entirely -- it is about giving humans the option to operate in "review only" mode instead of "approve every change" mode.

### Deliverables

- [ ] **Confidence scoring engine** -- Module that computes a composite confidence score for each pipeline run based on all available signals
  - [ ] `p35.d1.t1` Create confidence.py module
    > Create confidence.py: (1) evaluate_run(run_id) -- compute composite confidence from: test pass rate (phase 7), review sensor score (phase 9), structural invariant compliance (phase 17), legibility score (phase 33), cost efficiency (phase 32), historical success rate for similar tasks. (2) weighted_score(signals) -- configurable weights for each signal, (3) trust_level(score) -- map score to trust tier: auto-merge (95+), draft-PR (80+), human-review (60+), block (<60). Store confidence history for trend analysis.
    _Files: ~/zion/projects/agent-orchestration/confidence.py, ~/zion/projects/agent-orchestration/confidence_config.yaml_
  - [ ] Module outputs a confidence score (0-100) with breakdown by signal
    _Validation: python3 confidence.py --evaluate --run RUN_ID_
  _~150 LOC_
- [ ] **Progressive trust escalation** -- System that gradually increases autonomy as the orchestrator demonstrates reliability
  - [ ] `p35.d2.t1` Add trust escalation to confidence.py (depends: p35.d1.t1)
    > Add trust escalation logic: (1) track rolling success rate (last N runs), (2) escalate trust tier after sustained high confidence (e.g., 10 consecutive auto-merge quality runs -> upgrade from draft-PR to auto-merge), (3) de-escalate on failures (any blocked run -> drop one tier), (4) trust_levels.yaml stores current trust level per repo/pipeline. Include --trust-status and --trust-reset commands. Trust escalation is the mechanism that enables the Dark Factory: start conservative, earn autonomy through consistent quality.
    _Files: ~/zion/projects/agent-orchestration/confidence.py_
  - [ ] Trust level increases after consecutive successful runs
    _Validation: simulate 10 successful runs, check trust level escalation_
  _~100 LOC_
- [ ] **Dark factory mode pipeline** -- End-to-end autonomous pipeline that combines all quality gates into a single self-governing workflow
  - [ ] `p35.d3.t1` Create dark-factory-pipeline.yaml (depends: p35.d1.t1, p35.d2.t1)
    > Create pipelines/dark-factory-pipeline.yaml: AI(plan) -> AI(implement) -> VERIFY(output) -> Bash(test) -> REVIEW(LLM judge) -> VERIFY(no regression) -> BASH(structural invariants) -> BASH(architecture lint) -> AI(confidence evaluate) -> CONDITIONAL(auto-merge OR draft-PR OR human-review based on confidence score). This is the complete Dark Factory pipeline combining phases 5, 9, 17, 31, 32, 33, and 35.
    _Files: ~/zion/projects/agent-orchestration/pipelines/dark-factory-pipeline.yaml_
  - [ ] Pipeline exists that runs the full autonomous workflow with confidence-gated decisions
    _Validation: read pipeline YAML_
  _~80 LOC_
- [ ] **Emergency stop and human override** -- Mechanism for humans to immediately halt autonomous operation and take manual control
  - [ ] `p35.d4.t1` Add emergency stop to orchestrator (depends: p35.d1.t1)
    > Add emergency stop mechanism: (1) confidence.py --emergency-stop creates a kill file (~/.orchestrator/EMERGENCY_STOP), (2) orchestrator.py checks for kill file before each loop iteration, (3) if kill file exists, stop spawning new workers and gracefully shut down active ones, (4) --emergency-resume removes the kill file, (5) --status shows emergency stop state. This is the safety valve for Dark Factory mode -- humans can always pull the plug.
    _Files: ~/zion/projects/agent-orchestration/confidence.py, ~/zion/projects/agent-orchestration/orchestrator.py_
  - [ ] Can immediately stop all active workers and prevent new spawns
    _Validation: python3 confidence.py --emergency-stop_
  _~80 LOC_

### Technical Notes

Dark Factory Mode is the culmination of the entire roadmap. It does not mean "no humans ever" -- it means "humans review outcomes, not process." The confidence scoring engine is the key innovation: it aggregates all quality signals into a single number that determines the level of autonomy. Progressive trust escalation means the system starts conservative and earns autonomy. The emergency stop ensures humans always have the final say.

### Risks

- Confidence scoring weights may be wrong for specific projects -- need per-project tuning
- Progressive trust escalation could be too slow or too fast -- need configurable rates
- Emergency stop must be truly immediate -- cannot wait for the next cron cycle
- Dark factory mode should only be enabled for projects with comprehensive test coverage
- Legal/compliance requirements may prevent fully autonomous merges in some organizations

## [ ] phase-36: Dynamic Policy Engine (WORKFLOW.md Loader) (PLANNED)

**Goal:** Create a runtime policy loader that dynamically configures agent behavior per-project from structured workflow definitions

Symphony's Workflow Loader "parses WORKFLOW.md for prompt templates and runtime settings," acting as a Policy Engine that shapes agent behavior without code changes. The Hermes orchestrator uses static AI_GUIDE.md files (phase 12) that must be manually maintained. This phase adds a dynamic policy engine: a workflow_loader.py module that reads structured YAML/Markdown workflow definitions from each project, extracts agent configuration (system prompts, tool restrictions, quality gates, pipeline selection, environment variables), and applies them at runtime. This means project owners can tune orchestrator behavior by editing a workflow file rather than modifying the orchestrator itself. The loader supports per-label, per-priority, and per-issue-type overrides, enabling fine-grained control over how the orchestrator handles different kinds of work.

### Deliverables

- [ ] **Workflow definition schema** -- Structured YAML schema for defining agent policies per project
  - [ ] `p36.d1.t1` Define workflow policy YAML schema
    > Create a workflow_policy_schema.yaml that defines the structure of workflow policy files. Fields: system_prompt (agent persona override), tools (allowed/restricted tool list), pipeline (which pipeline template to use), quality_gates (minimum test coverage, max lint violations, required checks), env (environment variables for the workspace), limits (max turns, max files, timeout), labels (auto-apply labels based on issue type), hooks (pre/post pipeline shell commands). Support per-label overrides so bug issues get different policies than feature issues. Document the schema with examples.
    _Files: ~/zion/projects/agent-orchestration/workflow_policy_schema.yaml_
  - [ ] Schema supports at least 8 policy fields (system_prompt, tools, pipeline, quality_gates, env, limits, labels, hooks)
    _Validation: read schema documentation_
  _~100 LOC_
- [ ] **Workflow loader module** -- Python module that loads and validates workflow policies from project directories
  - [ ] `p36.d2.t1` Create workflow_loader.py module
    > Create workflow_loader.py: (1) load_policy(project_dir) -- search for .orchestrator/workflow.yaml or .orchestrator/workflow.md in the project, parse it, validate against schema, return a Policy dataclass, (2) merge_policies(base_policy, overrides) -- merge per-label overrides into base policy, with label-specific values taking precedence, (3) apply_policy(policy, workspace) -- write policy settings into workspace config (system prompt to .orchestrator/system-prompt.md, env vars to .orchestrator/env.json, tool restrictions to .orchestrator/tools.yaml), (4) validate_policy(policy) -- check for invalid combinations (e.g., restricted tools that the pipeline requires), (5) --dry-run to preview policy application without modifying workspace. Support fallback: if no workflow file exists, use orchestrator.yaml defaults.
    _Files: ~/zion/projects/agent-orchestration/workflow_loader.py_
  - [ ] Can load a workflow policy file, validate it against schema, and return a policy object
    _Validation: python3 workflow_loader.py load --path /path/to/project_
  _~150 LOC_
- [ ] **Integration with orchestrator and executor** -- Wire the workflow loader into the orchestrator loop so policies are applied per-issue
  - [ ] `p36.d3.t1` Integrate workflow_loader into orchestrator.py
    > Modify orchestrator.py run_loop() to: (1) after spawner creates a workspace, call workflow_loader.load_policy(repo_dir) to get the project policy, (2) pass the policy to the executor so AI nodes use the policy's system prompt, (3) apply tool restrictions from policy to the executor session, (4) use policy's pipeline selection instead of default if specified, (5) set environment variables from policy in the workspace. In executor.py, add policy parameter to DAGExecutor that overrides default settings. Policy is resolved once per workspace creation and cached for the pipeline run.
    _Files: ~/zion/projects/agent-orchestration/orchestrator.py, ~/zion/projects/agent-orchestration/executor.py_
  - [ ] Orchestrator applies workflow policy when spawning a workspace for an issue
    _Validation: create a workflow.yaml, file an issue, run orchestrator, verify policy applied_
  _~80 LOC_
- [ ] **Policy template generator** -- CLI tool that generates a starter workflow policy from an existing project
  - [ ] `p36.d4.t1` Add policy generation to workflow_loader.py
    > Add --generate mode to workflow_loader.py: (1) analyze the project (reuse onboard.py detection from phase 24), (2) generate a workflow.yaml with: appropriate pipeline selection based on project type, sensible quality gates (test command, lint command), tool restrictions for safety (no network access for simple projects), environment variables from detected config files, (3) output the generated policy as YAML. Include comments explaining each field. This makes it trivial for project owners to adopt the workflow policy system.
    _Files: ~/zion/projects/agent-orchestration/workflow_loader.py_
  - [ ] Can generate a workflow.yaml from project analysis with sensible defaults
    _Validation: python3 workflow_loader.py generate --path /path/to/project_
  _~80 LOC_

### Technical Notes

The workflow loader is the key differentiator between static configuration and dynamic policy. The critical insight from Symphony is that behavior should be configurable per-project without code changes. The loader reads YAML (not markdown) for machine-parseable configuration, but supports markdown comments for human readability. Policy resolution order: per-label override > project workflow.yaml > orchestrator.yaml defaults. Keep the schema simple -- YAML with 8-10 fields is enough. Do not try to replicate Symphony's full WORKFLOW.md specification; focus on the most impactful policy fields.

### Risks

- Policy files could conflict with orchestrator.yaml settings -- need clear precedence rules
- Complex policies may be hard to debug -- include --explain mode that shows effective settings
- Malformed policy files could break the orchestrator -- validate strictly and fall back to defaults

## [ ] phase-37: Event-Driven Trigger Mode (PLANNED)

**Goal:** Complement cron-based polling with webhook/event-driven triggers for faster issue response times

Symphony's polling daemon reads work every 30 seconds. Hermes uses cron-based scheduling (typically 5-15 minute intervals). For time-sensitive workflows, this polling delay is suboptimal. This phase adds an event-driven trigger mode: a lightweight HTTP server (using Python's built-in http.server) that receives GitHub webhooks and immediately queues matching issues for processing. The event mode runs alongside the existing cron mode -- cron handles the steady-state polling while events handle immediate triggers. This is not about replacing cron (cron is proven and reliable) but about adding a fast-path for urgent work. The webhook server writes trigger events to a shared queue file that the next cron iteration picks up, or can be configured to spawn an immediate orchestrator run.

### Deliverables

- [ ] **Webhook receiver server** -- Lightweight HTTP server that receives GitHub webhooks and triggers orchestrator runs
  - [ ] `p37.d1.t1` Create webhook_server.py
    > Create webhook_server.py: (1) HTTP server on configurable port (default 8471) using Python's http.server, (2) POST /webhook endpoint that validates GitHub webhook signature (X-Hub-Signature-256), (3) filter events: only process "issues" events with action "opened" or "labeled", (4) check if the issue has the agent-ready label, (5) write trigger event to ~/.orchestrator/triggers/pending.jsonl with: issue_number, repo, timestamp, webhook_id, (6) health endpoint GET /health returning server status, (7) graceful shutdown on SIGTERM. Use threading for concurrent request handling. Log all received webhooks for auditability.
    _Files: ~/zion/projects/agent-orchestration/webhook_server.py_
  - [ ] Server receives issue events via webhook and writes them to the trigger queue
    _Validation: send test webhook, verify trigger event created_
  _~150 LOC_
- [ ] **Trigger queue consumer** -- Module that reads pending trigger events and integrates with the orchestrator poller
  - [ ] `p37.d2.t1` Add trigger queue to orchestrator.py
    > Modify orchestrator.py run_loop() to: (1) before calling the poller, check for pending trigger events in ~/.orchestrator/triggers/pending.jsonl, (2) if triggers exist, prioritize those issues (add them to the front of the work queue), (3) mark processed triggers as done by moving them to ~/.orchestrator/triggers/processed.jsonl, (4) deduplicate triggers (same issue triggered multiple times), (5) expire stale triggers (older than N minutes, since cron will pick them up anyway). This means webhook-triggered issues get processed immediately on the next cron cycle rather than waiting for the poller to discover them.
    _Files: ~/zion/projects/agent-orchestration/orchestrator.py_
  - [ ] Orchestrator checks trigger queue before polling GitHub API
    _Validation: create trigger event, run orchestrator, verify it processes the triggered issue first_
  _~80 LOC_
- [ ] **Webhook setup CLI** -- CLI command to register GitHub webhooks for a repository
  - [ ] `p37.d3.t1` Add webhook setup to webhook_server.py
    > Add --setup mode to webhook_server.py: (1) use gh CLI to create a webhook on the target repo (gh api repos/{owner}/{repo}/hooks --input -), (2) configure events: ["issues"], (3) generate a shared secret and display it for webhook signature validation, (4) test the webhook with a ping event, (5) --teardown mode removes the webhook. Also add --status to list active webhooks and their delivery status.
    _Files: ~/zion/projects/agent-orchestration/webhook_server.py_
  - [ ] Can register and verify a webhook on a GitHub repo using gh CLI
    _Validation: python3 webhook_server.py setup owner/repo --url https://example.com:8471/webhook_
  _~80 LOC_
- [ ] **Event mode integration tests** -- Tests for webhook receiving, trigger queue, and orchestrator integration
  - [ ] `p37.d4.t1` Create test_webhook.py
    > Create test_webhook.py: (1) test webhook signature validation (valid/invalid signatures), (2) test event filtering (only issues events processed), (3) test trigger queue write and read, (4) test trigger deduplication (same issue triggered twice), (5) test trigger expiration (old triggers cleaned up), (6) test orchestrator prioritization of triggered issues, (7) test webhook setup via gh CLI (mocked). Use unittest.mock for HTTP server testing.
    _Files: ~/zion/projects/agent-orchestration/test_webhook.py_
  - [ ] Tests cover webhook validation, trigger processing, and deduplication
    _Validation: python3 -m pytest test_webhook.py -v_
  _~120 LOC_

### Technical Notes

The webhook server is deliberately lightweight -- no Flask/FastAPI dependency, just Python's built-in http.server. This keeps deployment simple and avoids dependency conflicts. The webhook server is optional -- the orchestrator works fine without it using cron-only mode. The trigger queue uses JSONL files (append-only) for reliability -- even if the server crashes mid-write, the file can be recovered. For production use, ngrok or a reverse proxy (nginx) would handle TLS termination and expose the webhook endpoint to GitHub.

### Risks

- Webhook server requires a publicly accessible URL -- may need ngrok or similar for local development
- GitHub webhook delivery can fail and retry -- need idempotent trigger processing
- Webhook secret management requires secure storage -- document how to configure
- HTTP server adds another process to monitor -- integrate with health check from phase 14

## [ ] phase-38: Cross-Project Knowledge Transfer (PLANNED)

**Goal:** Enable agents to share learned patterns, solutions, and conventions across multiple repositories

When the orchestrator works across multiple repos (phase 16), each project is treated independently. But agents often encounter the same patterns across projects: similar error handling approaches, shared architectural patterns, common library usage. Gas Town's Beads system enables shared state between agents. This phase adds a knowledge base that captures patterns learned from successful pipeline runs and makes them available to agents working on other projects. When an agent encounters a similar problem that was solved in another repo, it gets the previous solution as context. This creates a "learning organization" effect where the orchestrator gets more effective over time across all projects, not just within a single repo.

### Deliverables

- [ ] **Pattern extraction module** -- Module that extracts reusable patterns from successful pipeline runs
  - [ ] `p38.d1.t1` Create knowledge.py pattern extraction module
    > Create knowledge.py: (1) extract_patterns(run_id) -- analyze a successful execution log to extract: issue type (from labels/title), solution_approach (from AI node prompts and outputs), files_changed (from git diff in workspace), commands_used (from bash nodes), test_strategy (from test node), (2) classify_pattern(pattern) -- categorize the pattern (error-handling, api-design, refactoring, testing, etc.), (3) store_pattern(pattern) -- save to ~/.orchestrator/knowledge/patterns.jsonl with: hash, category, source_repo, source_issue, created_at, effectiveness (derived from test results). Patterns are deduplicated by content hash to avoid storing identical solutions.
    _Files: ~/zion/projects/agent-orchestration/knowledge.py_
  - [ ] Can analyze a completed run and extract patterns (solution approach, files changed, commands used)
    _Validation: python3 knowledge.py extract --run RUN_ID_
  _~120 LOC_
- [ ] **Knowledge query module** -- Module that retrieves relevant patterns for a given issue from the knowledge base
  - [ ] `p38.d2.t1` Add knowledge query to knowledge.py
    > Add query mode to knowledge.py: (1) query_patterns(issue_description, repo, top_n=3) -- find patterns from other repos that are relevant to the current issue, (2) relevance scoring based on: category match (same issue type), keyword overlap (similar terms in issue vs pattern description), effectiveness (prefer patterns from successful runs), recency (prefer recent patterns), (3) format_pattern(pattern) -- convert a pattern to a concise agent-readable context string suitable for inclusion in the AI node prompt, (4) --similar flag to find patterns from the same repo (intra-project knowledge). Output as structured JSON or formatted text.
    _Files: ~/zion/projects/agent-orchestration/knowledge.py_
  - [ ] Can find similar patterns from other projects for a given issue description
    _Validation: python3 knowledge.py query --issue "add error handling to API endpoints"_
  _~100 LOC_
- [ ] **Knowledge integration with executor** -- Automatically inject relevant knowledge into AI node prompts
  - [ ] `p38.d3.t1` Integrate knowledge into executor AI nodes
    > Modify executor.py AI node execution to: (1) before constructing the AI prompt, call knowledge.query_patterns(issue_description, current_repo), (2) if relevant patterns found, append them to the system prompt as "Relevant patterns from other projects:" section, (3) limit context injection to top 3 patterns to avoid prompt bloat, (4) add config option enable_knowledge (default true) and knowledge_max_patterns (default 3) to orchestrator.yaml. The knowledge injection is transparent to the agent -- it just gets better context.
    _Files: ~/zion/projects/agent-orchestration/executor.py, ~/zion/projects/agent-orchestration/orchestrator.py_
  - [ ] AI nodes receive relevant cross-project patterns in their context
    _Validation: create a pattern, file an issue, run pipeline, check AI prompt includes the pattern_
  _~60 LOC_
- [ ] **Knowledge management CLI** -- CLI to browse, prune, and manage the pattern knowledge base
  - [ ] `p38.d4.t1` Add knowledge management CLI to knowledge.py
    > Add management subcommands to knowledge.py: (1) list (--category, --repo, --since, --top N) -- browse stored patterns, (2) prune (--older-than, --min-effectiveness) -- remove low-quality or stale patterns, (3) export (--format json/markdown, --output file) -- export patterns for sharing between orchestrator instances, (4) import (--input file) -- import patterns from another instance, (5) stats -- show knowledge base statistics (total patterns, per-category counts, coverage by repo). Add --auto-extract flag to run pattern extraction on all recent successful runs.
    _Files: ~/zion/projects/agent-orchestration/knowledge.py_
  - [ ] Can list, search, prune, and export patterns from the knowledge base
    _Validation: python3 knowledge.py list --category error-handling --limit 10_
  _~80 LOC_

### Technical Notes

Knowledge transfer is fundamentally about "learning from experience" across projects. The key challenge is relevance -- agents should only see patterns that are actually useful for their current task. Simple keyword matching is a good starting point; future work could use embeddings for semantic similarity. The knowledge base is stored as flat JSONL files for simplicity -- no database needed for the expected scale (hundreds to low thousands of patterns). Patterns from failed runs are NOT stored (only successful runs contribute to knowledge), which keeps quality high by default.

### Risks

- Pattern injection could confuse agents if patterns are irrelevant -- need good relevance scoring
- Knowledge base could grow unbounded -- need pruning strategy
- Cross-project patterns may use different conventions -- need repo-specific filtering
- Prompt bloat from too many patterns -- strict limit on injected context

## [ ] phase-39: Browser-Based UI Verification (Chrome DevTools Protocol) (PLANNED)

**Goal:** Enable agents to drive a headless browser to visually verify UI changes, reproduce bugs, and validate end-to-end user flows before submitting PRs

The Harness Engineering research explicitly calls out "Direct UI Manipulation: Wiring tools like Chrome DevTools Protocol into the agent's runtime, allowing it to reproduce bugs and verify UI fixes autonomously." Phase 31 (Self-Verifying Agent Toolkit) covers assertion-based verification but not browser/visual verification. This phase adds a headless browser integration layer that agents can call from pipeline nodes to: (1) navigate to pages and check rendering, (2) fill forms and validate submissions, (3) take screenshots for visual regression, (4) reproduce reported bugs by following reproduction steps. This closes the Application Legibility gap for UI-focused projects.

### Deliverables

- [ ] **Browser automation module** -- Python module that wraps Chrome DevTools Protocol for agent-driven browser interactions
  - [ ] `p39.d1.t1` Create browser_verify.py module
    > Python module using playwright or CDP directly: (1) launch_headless(url) -- start Chrome in headless mode, return a BrowserSession, (2) session.navigate(url), session.fill(selector, value), session.click(selector), session.screenshot(path), (3) session.get_page_text() -- extract visible text for assertion, (4) session.wait_for(selector, timeout) -- wait for element to appear, (5) session.close(). Use subprocess to manage Chrome process. Fall back gracefully if Chrome is not installed. Include --mode headed for debugging.
    _Files: ~/zion/projects/agent-orchestration/browser_verify.py_
  - [ ] Module can launch headless Chrome, navigate to a URL, and return page content
    _Validation: python3 browser_verify.py --navigate http://localhost:3000_
  - [ ] Supports form filling, click, scroll, and screenshot capture
    _Validation: run through a form submission test_
  _~150 LOC_
- [ ] **BROWSER node type for DAG executor** -- Add a BROWSER node type that runs browser verification steps from the pipeline
  - [ ] `p39.d2.t1` Add BROWSER node type to DAG (depends: p39.d1.t1)
    > Add NodeType.BROWSER to dag.py. The browser node takes: url (base URL to navigate), steps (list of actions: navigate, fill, click, wait, screenshot, assert_text), assert_text (expected text to verify on page), screenshot_on_failure (bool, capture screenshot when assertion fails). Executor calls browser_verify.py with the steps. If assertion fails, node fails and screenshot is saved to workspace for debugging.
    _Files: ~/zion/projects/agent-orchestration/dag.py, ~/zion/projects/agent-orchestration/executor.py_
  - [ ] Pipeline YAML can include BROWSER nodes for UI verification
    _Validation: create pipeline with browser node, execute it_
  _~100 LOC_
- [ ] **Visual regression detection** -- Screenshot-based comparison to detect unintended visual changes
  - [ ] `p39.d3.t1` Add visual regression to browser_verify.py (depends: p39.d1.t1)
    > Add visual regression to browser_verify.py: (1) capture_baseline(url, selector, path) -- save a reference screenshot, (2) compare_screenshot(baseline_path, current_path, threshold) -- compare pixel difference, return match percentage and diff image, (3) --threshold flag (default 0.01 = 1% pixel difference allowed), (4) store baselines in workspace/.orchestrator/baselines/. Include --update-baseline flag to refresh baselines after intentional visual changes.
    _Files: ~/zion/projects/agent-orchestration/browser_verify.py_
  - [ ] Can compare screenshots and report pixel-level differences
    _Validation: take baseline screenshot, modify UI, take new screenshot, compare_
  _~100 LOC_
- [ ] **Browser verification pipeline template** -- Pipeline YAML that adds browser-based UI verification for frontend projects
  - [ ] `p39.d4.t1` Create browser-pipeline.yaml (depends: p39.d2.t1, p39.d3.t1)
    > Create pipelines/browser-pipeline.yaml: AI(implement) -> Bash(build/start dev server) -> BROWSER(navigate to app, verify rendering) -> Bash(run unit tests) -> BROWSER(fill form, submit, verify result) -> AI(review) -> Bash(commit). Include env vars for dev server URL and startup command. The browser nodes serve as integration tests that verify the UI actually works after code changes.
    _Files: ~/zion/projects/agent-orchestration/pipelines/browser-pipeline.yaml_
  - [ ] Pipeline template includes BROWSER nodes for UI testing before commit
    _Validation: read pipeline YAML, trace through nodes_
  _~60 LOC_

### Technical Notes

Use Playwright (pip install playwright) if available for reliable CDP control, with a subprocess-based Chrome fallback. The BROWSER node is complementary to VERIFY nodes -- VERIFY checks structured assertions, BROWSER checks visual/interaction behavior. Screenshots on failure are critical for debugging -- they give agents and humans a visual record of what went wrong. Keep browser sessions short-lived to avoid resource leaks.

### Risks

- Headless Chrome may not be available in all environments -- need graceful degradation
- Browser tests are inherently slower than unit tests -- keep them focused on critical flows
- Visual regression can be flaky due to rendering differences (fonts, anti-aliasing) -- use per-environment baselines
- Browser automation adds a heavy dependency (Chrome/Chromium) -- make it optional

## [ ] phase-40: Multi-Model Agent Backend Abstraction (PLANNED)

**Goal:** Abstract the AI execution layer so the orchestrator can route work to different models and providers based on task type, cost, and quality requirements

The Harness Engineering research describes the Inner Harness as "infrastructure inside developer tools (Cursor, Claude Code, Codex)" and notes it is "increasingly commoditized as providers converge on similar execution primitives." The current orchestrator is tightly coupled to a single model/provider via delegate_task. This phase adds a backend abstraction layer that: (1) defines a uniform interface for AI execution, (2) supports multiple backends (Claude, GPT, local models, Codex), (3) routes tasks to the optimal backend based on task type and cost, (4) enables fallback when a backend is unavailable. This is the Inner Harness abstraction that Symphony treats as a pluggable component, and it unlocks cost optimization by routing simple tasks to cheaper models while preserving quality for complex ones.

### Deliverables

- [ ] **Backend abstraction interface** -- Python interface defining the uniform contract for all AI execution backends
  - [ ] `p40.d1.t1` Create backend.py abstraction layer
    > Create backend.py with: (1) AIBackend abstract base class with execute(prompt, system_prompt, tools, max_turns, context_window) -> BackendResult, (2) ClaudeBackend -- wraps delegate_task with acp_command=claude, (3) SubprocessBackend -- wraps any CLI tool (Codex, aider, etc.) via subprocess, (4) MockBackend -- returns canned responses for testing, (5) BackendConfig dataclass with model, provider, max_tokens, temperature. Each backend reports: model name, token usage estimate, latency, cost estimate.
    _Files: ~/zion/projects/agent-orchestration/backend.py_
  - [ ] Interface defines execute(prompt, context, tools) -> result with structured output
    _Validation: read backend.py, check interface definition_
  - [ ] At least 2 backend implementations (Claude, subprocess/CLI)
    _Validation: read backend implementations_
  _~180 LOC_
- [ ] **Backend routing engine** -- Module that selects the optimal backend for each AI node based on task characteristics
  - [ ] `p40.d2.t1` Create router.py backend selection module (depends: p40.d1.t1)
    > Create router.py: (1) select_backend(node_config, issue_labels, budget_remaining) -- returns the best backend for a given task, (2) routing rules based on: task complexity (simple edit vs full implementation), role requirements (reviewer needs strong model, tester can use cheaper model), budget constraints, model availability, (3) routing_config.yaml defines: default_backend, per_role_overrides, per_label_overrides, fallback_chain (what to try if primary backend fails), (4) --dry-run to preview routing decisions without executing.
    _Files: ~/zion/projects/agent-orchestration/router.py, ~/zion/projects/agent-orchestration/routing_config.yaml_
  - [ ] Can route simple tasks to cheaper backends and complex tasks to premium ones
    _Validation: test routing with different task types_
  - [ ] Routing rules are configurable via YAML
    _Validation: read routing config_
  _~120 LOC_
- [ ] **Backend integration with executor** -- Wire the backend abstraction into the DAG executor so AI nodes use the routing engine
  - [ ] `p40.d3.t1` Integrate backend router into executor (depends: p40.d1.t1, p40.d2.t1)
    > Modify executor.py AI node execution to: (1) call router.select_backend() with node config and issue context, (2) instantiate the selected backend, (3) execute via the backend interface instead of direct delegate_task call, (4) log which backend was used, estimated cost, and actual latency, (5) on backend failure, try the next backend in the fallback chain before giving up. Backward compatible -- if no routing config, use default ClaudeBackend.
    _Files: ~/zion/projects/agent-orchestration/executor.py_
  - [ ] AI nodes in pipelines use the backend router instead of hardcoded delegate_task
    _Validation: run pipeline, check execution log shows backend selection_
  _~80 LOC_
- [ ] **Backend cost comparison reporting** -- Track and report cost/quality metrics per backend to inform routing decisions
  - [ ] `p40.d4.t1` Add backend reporting to router.py (depends: p40.d2.t1, p8.d1.t1)
    > Add --report mode to router.py: (1) aggregate execution logs by backend, (2) compute per-backend metrics: total_cost, success_rate, avg_latency, avg_tokens, failure_reasons, (3) identify cost savings from routing (compare actual cost vs if everything used the premium backend), (4) suggest routing rule adjustments based on data (e.g., "tester role has 95% success rate with cheap model -- consider always routing there"). Output as table or JSON.
    _Files: ~/zion/projects/agent-orchestration/router.py_
  - [ ] Can report cost per backend, success rate, and average latency
    _Validation: python3 router.py --report --period week_
  _~80 LOC_

### Technical Notes

The backend abstraction is the Inner Harness layer from the research. Keep it simple: a Python ABC with 2-3 implementations. The key insight is that not all AI tasks need the most expensive model -- code review can use a fast model, complex implementation needs a powerful one. The routing engine is the "model router" pattern from production ML systems, applied to agent orchestration. Start with ClaudeBackend (existing delegate_task) and SubprocessBackend (any CLI tool), add more backends as needed.

### Risks

- Different backends produce different quality output -- routing a complex task to a weak model wastes tokens on retries
- Backend availability varies -- fallback chains add latency
- Cost estimation is approximate -- actual costs depend on provider pricing
- Adding more backends increases maintenance burden -- keep the interface minimal

## [ ] phase-41: Intelligent Scheduling and Priority Queuing (GUPP Enforcement) (PLANNED)

**Goal:** Replace simple cron polling with an intelligent scheduler that prioritizes work, enforces urgency, and optimizes throughput

The Gas Town research describes the "Gastown Universal Propulsion Principle" (GUPP): "if an agent has work on its hook, it must run it immediately." The current orchestrator uses simple cron-based polling that processes issues in GitHub API order with no concept of priority, urgency, or strategic scheduling. This phase adds: (1) a priority queue that ranks issues by urgency, complexity, dependencies, and strategic value, (2) urgency scoring based on issue age, labels, and dependencies, (3) GUPP-style enforcement that ensures ready work is processed immediately rather than waiting for the next cron cycle, (4) scheduling policies that balance throughput (many simple issues) with progress (complex issues don't starve). This transforms the orchestrator from a passive poller into an active scheduler that maximizes the value of every agent-hour.

### Deliverables

- [ ] **Priority queue system** -- Ordered work queue with configurable priority scoring for issues
  - [ ] `p41.d1.t1` Create priority_queue.py module
    > Create priority_queue.py: (1) score_issue(issue) -- compute priority score from: urgency (age-based: older issues score higher), labels (bug > feature > chore), complexity (simple issues first for throughput), dependencies (blocked issues deprioritized), strategic_value (from issue metadata or label), (2) enqueue(issue, score) -- add to priority queue backed by ~/.orchestrator/state/priority-queue.jsonl, (3) dequeue() -- return highest-priority issue, (4) reprioritize(issue_number, new_score) -- adjust priority after external events, (5) --dump to inspect queue state, --clear to reset.
    _Files: ~/zion/projects/agent-orchestration/priority_queue.py_
  - [ ] Issues are scored and ranked by configurable priority criteria
    _Validation: queue 5 issues with different labels/ages, verify ordering_
  - [ ] Queue persists across orchestrator restarts
    _Validation: restart orchestrator, check queue is restored_
  _~150 LOC_
- [ ] **Urgency scoring engine** -- Module that calculates urgency scores based on issue age, SLA targets, and dependency chains
  - [ ] `p41.d2.t1` Add urgency scoring to priority_queue.py (depends: p41.d1.t1)
    > Add urgency scoring to priority_queue.py: (1) age_factor -- linear ramp from creation date, configurable half_life (issues double in urgency every N days), (2) dependency_boost -- if an issue has sub-issues waiting on it, boost its priority (detect via gh CLI issue references), (3) SLA_targets (from priority_config.yaml) -- define target resolution times per label (P0: 1 hour, P1: 1 day, P2: 1 week), urgency spikes as SLA approaches, (4) starvation_prevention -- ensure complex issues don't get perpetually skipped by simple ones (aging factor that guarantees eventual processing). Output urgency breakdown per issue for transparency.
    _Files: ~/zion/projects/agent-orchestration/priority_queue.py, ~/zion/projects/agent-orchestration/priority_config.yaml_
  - [ ] Issues that have been open longer get higher urgency scores
    _Validation: create issues of different ages, check scoring_
  - [ ] Issues blocking other issues get boosted priority
    _Validation: create dependency chain, check parent issue priority_
  _~120 LOC_
- [ ] **GUPP enforcement in orchestrator loop** -- Modify the orchestrator to use the priority queue instead of raw poller order, processing high-priority work immediately
  - [ ] `p41.d3.t1` Integrate priority queue into orchestrator loop (depends: p41.d1.t1, p41.d2.t1)
    > Modify orchestrator.py run_loop() to: (1) poll issues as before, but instead of processing in API order, add all to priority queue with scores, (2) dequeue the highest-priority issue, spawn worker for it, (3) re-score remaining issues on each iteration (urgency increases with time), (4) when webhook triggers arrive (from phase 37), add them to queue with elevated priority, (5) log scheduling decisions: "Skipped issue #42 (priority 3.2) in favor of issue #38 (priority 8.7, SLA in 2h)".
    _Files: ~/zion/projects/agent-orchestration/orchestrator.py_
  - [ ] Orchestrator processes issues by priority score rather than API order
    _Validation: file 3 issues, verify highest-priority is processed first_
  - [ ] When webhook triggers arrive (phase 37), they jump the queue
    _Validation: trigger webhook, verify issue is processed before lower-priority queued items_
  _~100 LOC_
- [ ] **Scheduling analytics and SLA tracking** -- Track scheduling performance: time-to-first-response, SLA compliance, queue depth trends
  - [ ] `p41.d4.t1` Add scheduling analytics to priority_queue.py (depends: p41.d1.t1, p8.d1.t1)
    > Add --analytics mode to priority_queue.py: (1) compute avg_time_to_spawn (from issue creation to worker start), (2) SLA compliance rate (% of issues processed within target time), (3) queue_depth trends (average, peak, growth rate), (4) throughput (issues processed per day/week), (5) starvation detection (issues that have been in queue > N times without being selected). Store historical analytics in ~/.orchestrator/logs/scheduling/ for trend analysis.
    _Files: ~/zion/projects/agent-orchestration/priority_queue.py_
  - [ ] Can report average time from issue creation to worker spawn
    _Validation: python3 priority_queue.py --analytics --period week_
  - [ ] SLA breach rate is tracked and reported
    _Validation: check analytics output for SLA metrics_
  _~100 LOC_

### Technical Notes

The priority queue is the scheduling brain of the orchestrator. The key insight from Gas Town's GUPP is that work should flow immediately, not wait for polling cycles. The queue is file-backed (JSONL) for persistence. Urgency scoring uses simple heuristics (age, labels, dependencies) rather than ML -- keep it transparent and debuggable. Starvation prevention is critical: without it, a constant stream of simple issues could permanently block complex ones.

### Risks

- Priority scoring heuristics may not match actual business priorities -- need configurable weights
- Urgency scoring could lead to thrashing if priorities change rapidly between iterations
- Queue persistence adds I/O overhead on every loop iteration -- keep it lightweight
- GUPP enforcement could overwhelm the system if too many high-priority issues arrive at once -- need backpressure

## Global Risks

- Symphony/Gas Town/Archon are all rapidly evolving -- this roadmap may need updates as those projects change
- delegate_task sessions are synchronous and bounded by parent turn -- long-running orchestrator tasks need careful design (background terminals or chained cron)
- GitHub Issues as control plane requires a public or accessible repo -- private repo token management adds complexity
- Token costs for autonomous loops can escalate quickly (Symphony team uses 1B tokens/day) -- need cost awareness in the orchestrator
- Speculative execution (phase 28) can multiply costs if not carefully budgeted
- Inter-agent coordination (phase 30) adds complexity that may not be needed at low concurrency levels
- Dark factory mode (phase 35) should only be enabled for well-tested projects with comprehensive safety gates
- Token budget enforcement (phase 32) relies on estimates -- actual costs may differ significantly
- Webhook server (phase 37) requires network exposure -- needs security review for production use
- Cross-project knowledge (phase 38) could leak proprietary patterns between repos -- need per-repo knowledge isolation controls
- Browser automation (phase 39) requires Chrome/Chromium -- adds a heavy runtime dependency and may not work in all CI environments
- Multi-model routing (phase 40) could route complex tasks to underpowered models if scoring is wrong -- need conservative defaults
- Priority scheduling (phase 41) could starve complex tasks if urgency weights favor simple fast completions -- need starvation prevention

## Conventions

- Python scripts use python3 (no bare python command on this system)
- GitHub API via gh CLI, not raw curl
- All new code goes to ~/zion/projects/agent-orchestration/
- Skills go to ~/.hermes/skills/ following existing category structure
- Wiki pages follow SCHEMA.md conventions (frontmatter, wikilinks, tag taxonomy)

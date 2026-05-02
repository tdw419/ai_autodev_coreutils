# Hermes Agent Orchestration

Apply patterns from OpenAI Symphony, Harness Engineering, Gas Town, and Archon to the Hermes agent ecosystem. Synthesize research into wiki, map concepts to existing infrastructure, and implement concrete improvements.

**Progress:** 17/69 phases complete, 0 in progress

**Deliverables:** 67/275 complete

**Tasks:** 74/275 complete

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
| phase-17 Structural Invariants Engine | COMPLETE | 4/4 | 390 | 10 |
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
| phase-42 External Application Observability Integration | PLANNED | 0/4 | 430 | 10 |
| phase-43 Automated Refactoring Pipeline (Self-Healing Codebase) | PLANNED | 0/4 | 320 | 10 |
| phase-44 System Health Scorecard and Effectiveness Trends | PLANNED | 0/4 | 410 | 8 |
| phase-45 Symphony Spec Compliance and WORKFLOW.md Engine | PLANNED | 0/4 | 340 | 8 |
| phase-46 Golden Principles Registry and Evolution | PLANNED | 0/4 | 410 | 10 |
| phase-47 Cattle vs Pets Worker Model (Session Identity and Disposability) | PLANNED | 0/4 | 430 | 10 |
| phase-48 Cost Optimization and Intelligent Model Routing | PLANNED | 0/4 | 400 | 10 |
| phase-49 Human Feedback Capture and Agent Behavior Tuning | PLANNED | 0/4 | 410 | 8 |
| phase-50 Orchestrator Chaos Engineering and Fault Injection Testing | PLANNED | 0/4 | 460 | 20 |
| phase-51 Orchestrator Federation and Cross-Instance Coordination | PLANNED | 0/4 | 420 | 12 |
| phase-52 Agent Output Provenance Tracking | PLANNED | 0/4 | 390 | 8 |
| phase-53 Dynamic Workforce Autoscaling | PLANNED | 0/4 | 410 | 10 |
| phase-54 Version-Controlled Work Graph (Beads Pattern) | PLANNED | 0/4 | 520 | 12 |
| phase-55 Automated agent.md Project Bootstrap Generator | PLANNED | 0/4 | 560 | 10 |
| phase-56 Symphony Spec Compliance Adapter | PLANNED | 0/4 | 560 | 12 |
| phase-57 Skill Registry and Reusable Role Templates | PLANNED | 0/4 | 490 | 10 |
| phase-58 Agent Session Replay and Forensic Analysis | PLANNED | 0/4 | 560 | 10 |
| phase-59 PR Velocity Metrics and Orchestrator ROI Tracking | PLANNED | 0/4 | 460 | 8 |
| phase-60 Human-Agent Workflow Optimization | PLANNED | 0/4 | 460 | 8 |
| phase-61 Agent Quality Regression Testing | PLANNED | 0/4 | 510 | 10 |
| phase-62 Prompt Engineering as Infrastructure | PLANNED | 0/4 | 460 | 8 |
| phase-63 Orchestrator REST API and Platform Layer | PLANNED | 0/4 | 560 | 10 |
| phase-64 Workspace Sandboxing and OS-Level Isolation | PLANNED | 0/4 | 480 | 12 |
| phase-65 Stop Hooks and Agent Loop Control | PLANNED | 0/4 | 420 | 10 |
| phase-66 Scheduled Periodic Maintenance Automation | PLANNED | 0/4 | 420 | 10 |
| phase-67 Pre-PR Self-Verification Gate | PLANNED | 0/4 | 400 | 10 |
| phase-68 Agent Session Identity and Continuity | PLANNED | 0/4 | 400 | 10 |
| phase-69 Orchestrator Integration Test Suite | PLANNED | 0/4 | 420 | 15 |

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
| phase-5 | phase-42 | soft | OBSERVE node type extends the DAG executor from phase 5 |
| phase-7 | phase-42 | soft | Tests should cover observability integration before production use |
| phase-33 | phase-42 | soft | Application legibility analysis from phase 33 identifies which projects need log integration |
| phase-39 | phase-42 | soft | Browser verification from phase 39 and log observability from phase 42 are complementary UI vs backend observability |
| phase-10 | phase-43 | soft | Refactoring pipeline consumes GC scan results from phase 10 |
| phase-13 | phase-43 | soft | Refactoring PRs use PR creation from phase 13 |
| phase-15 | phase-43 | soft | Refactoring PRs should always require human review per safety policies |
| phase-32 | phase-43 | soft | Refactoring consumes tokens -- respect budget limits from phase 32 |
| phase-42 | phase-43 | soft | OBSERVE nodes from phase 42 provide log context for understanding violations |
| phase-8 | phase-44 | soft | Health scorecard reads execution history logs from phase 8 |
| phase-9 | phase-44 | soft | Review sensor scores from phase 9 feed into the quality signal of the health score |
| phase-14 | phase-44 | soft | Health monitoring data from phase 14 provides system uptime and reliability signals |
| phase-27 | phase-44 | soft | Dashboard from phase 27 provides real-time state that complements historical trends |
| phase-32 | phase-44 | soft | Cost tracking from phase 32 provides the cost efficiency signal for the health score |
| phase-35 | phase-44 | soft | Dark factory confidence scores from phase 35 are a key effectiveness signal |
| phase-4 | phase-45 | soft | WORKFLOW.md integration modifies the spawner from phase 4 |
| phase-36 | phase-45 | soft | Dynamic Policy Engine from phase 36 is the general case; WORKFLOW.md is the specific Symphony format |
| phase-24 | phase-45 | soft | Project onboarding from phase 24 can generate WORKFLOW.md as part of bootstrap |
| phase-10 | phase-46 | soft | GC scanning from phase 10 is extended to include principles compliance checks |
| phase-17 | phase-46 | soft | Structural invariants from phase 17 provide the AST analysis that structural principle checks build on |
| phase-19 | phase-46 | soft | Self-improvement from phase 19 tracks principle compliance trends |
| phase-44 | phase-46 | soft | Health scorecard from phase 44 includes principles compliance as a quality signal |
| phase-4 | phase-47 | soft | Worker identity modifies the spawner from phase 4 |
| phase-8 | phase-47 | soft | Knowledge extraction reads from execution logs created by phase 8 |
| phase-11 | phase-47 | soft | Session disposal integrates with workspace lifecycle from phase 11 |
| phase-20 | phase-47 | soft | Knowledge injection must respect context budget limits from phase 20 |
| phase-38 | phase-47 | soft | Cross-project knowledge transfer from phase 38 benefits from the knowledge store |
| phase-32 | phase-48 | soft | Cost optimization builds on the cost tracking data from phase 32 |
| phase-20 | phase-48 | soft | Context budget data from phase 20 feeds into cost optimization analysis |
| phase-40 | phase-48 | soft | Multi-model backend from phase 40 can execute model tier recommendations |
| phase-13 | phase-49 | soft | Feedback capture reads PRs created by the PR automation from phase 13 |
| phase-15 | phase-49 | soft | Approval policies from phase 15 may need adjustment based on feedback patterns |
| phase-44 | phase-49 | soft | Health scorecard from phase 44 should include rejection rate as a quality signal |
| phase-46 | phase-49 | soft | Human feedback can inform principle evolution from phase 46 |
| phase-14 | phase-50 | soft | Health monitoring from phase 14 provides the baseline that chaos testing verifies |
| phase-25 | phase-50 | soft | Resilience from phase 25 should be validated by chaos testing |
| phase-7 | phase-50 | soft | Chaos tests extend the test suite from phase 7 with fault injection scenarios |
| phase-35 | phase-50 | hard | Dark factory mode from phase 35 requires passing chaos tests as a prerequisite |
| phase-4 | phase-51 | soft | Federation extends the base orchestrator loop from phase 4 with cross-instance coordination |
| phase-16 | phase-51 | soft | Multi-repo orchestration from phase 16 is a prerequisite for effective federation |
| phase-30 | phase-51 | soft | Inter-agent communication from phase 30 provides the notification patterns that federation extends |
| phase-41 | phase-51 | soft | Priority queuing from phase 41 should work across federated instances |
| phase-8 | phase-52 | soft | Provenance data is stored alongside execution logs from phase 8 |
| phase-13 | phase-52 | soft | PR automation from phase 13 is where git commits are created |
| phase-6 | phase-52 | soft | Role specialization from phase 6 provides the agent roles that provenance tracks |
| phase-19 | phase-52 | soft | Self-improvement analysis from phase 19 benefits from provenance data |
| phase-29 | phase-52 | soft | A/B testing analytics from phase 29 can use provenance for attribution |
| phase-4 | phase-53 | soft | Autoscaling modifies the orchestrator loop from phase 4 |
| phase-14 | phase-53 | soft | Health monitoring from phase 14 provides resource metrics that autoscaling uses |
| phase-32 | phase-53 | soft | Token budget tracking from phase 32 provides cost constraint for scaling decisions |
| phase-41 | phase-53 | soft | Priority queuing from phase 41 determines which work is queued (input to scaling decisions) |
| phase-44 | phase-53 | soft | Health scorecard from phase 44 includes resource efficiency metrics from autoscaling |
| phase-4 | phase-54 | soft | Work graph replaces the flat issue queue from phase 4 with dependency-aware scheduling |
| phase-6 | phase-54 | soft | Role specialization from phase 6 is used for role-based work pulling |
| phase-26 | phase-54 | soft | Work decomposition from phase 26 (Mayor pattern) creates the work items that the graph tracks |
| phase-30 | phase-54 | soft | Inter-agent communication from phase 30 provides the notification channel for dependency resolution |
| phase-41 | phase-54 | soft | Priority queuing from phase 41 can prioritize within the set of ready graph items |
| phase-12 | phase-55 | soft | Self-documentation from phase 12 provides the pattern that agent.md generation follows |
| phase-33 | phase-55 | soft | App legibility toolkit from phase 33 benefits from auto-generated agent.md quality scores |
| phase-24 | phase-55 | soft | Project onboarding from phase 24 should include agent.md generation |
| phase-45 | phase-55 | soft | WORKFLOW.md engine from phase 45 complements agent.md as project-level guides |
| phase-4 | phase-56 | soft | Symphony adapter wraps the base orchestrator from phase 4 |
| phase-15 | phase-56 | soft | Safety policies from phase 15 map to Symphony approval policies |
| phase-11 | phase-56 | soft | Workspace management from phase 11 must match Symphony workspace isolation conventions |
| phase-45 | phase-56 | soft | WORKFLOW.md engine from phase 45 is the Symphony workflow loader equivalent |
| phase-6 | phase-57 | soft | Role specialization from phase 6 is enhanced by reusable skill composition |
| phase-34 | phase-57 | soft | Agent-generated tooling from phase 34 can be packaged as shareable skills |
| phase-38 | phase-57 | soft | Cross-project knowledge from phase 38 benefits from skill sharing between projects |
| phase-12 | phase-57 | soft | Self-documentation patterns from phase 12 inform skill metadata and documentation |
| phase-8 | phase-58 | soft | Execution logs from phase 8 provide the base data that session recordings extend |
| phase-18 | phase-58 | soft | Trace tools from phase 18 are enhanced by full session replay |
| phase-19 | phase-58 | soft | Self-improvement loop from phase 19 consumes forensic analysis results |
| phase-20 | phase-58 | soft | Context window optimization from phase 20 benefits from context degradation detection |
| phase-46 | phase-58 | soft | Golden principles from phase 46 can be derived from forensic analysis patterns |
| phase-8 | phase-59 | soft | Execution history from phase 8 provides cost data for ROI computation |
| phase-13 | phase-59 | soft | PR automation from phase 13 is the primary source of agent-created PRs |
| phase-32 | phase-59 | soft | Cost tracking from phase 32 provides token cost data for cost-per-PR computation |
| phase-44 | phase-59 | soft | Health scorecard from phase 44 provides system metrics that complement business metrics |
| phase-9 | phase-59 | soft | Review sensor scores from phase 9 provide quality signals for trend analysis |
| phase-4 | phase-60 | soft | Orchestrator from phase 4 creates the issues and PRs that the human workflow tooling manages |
| phase-9 | phase-60 | soft | Review sensor scores from phase 9 are used in PR review queue prioritization |
| phase-13 | phase-60 | soft | PR automation from phase 13 creates the PRs that appear in the review queue |
| phase-49 | phase-60 | soft | Feedback capture from phase 49 provides the data for tracking human review patterns |
| phase-59 | phase-60 | soft | Velocity metrics from phase 59 include human review time tracking |
| phase-5 | phase-61 | soft | DAG executor from phase 5 is used to run benchmark tasks through the full pipeline |
| phase-7 | phase-61 | soft | Test infrastructure from phase 7 ensures the orchestrator code itself is reliable before benchmarking |
| phase-9 | phase-61 | soft | Review sensor from phase 9 provides quality scores for benchmark results |
| phase-19 | phase-61 | soft | Self-improvement from phase 19 consumes benchmark results to identify improvement opportunities |
| phase-29 | phase-61 | soft | A/B testing from phase 29 generates the comparison data that benchmarks validate |
| phase-32 | phase-61 | soft | Cost tracking from phase 32 provides token efficiency data for benchmark scoring |
| phase-5 | phase-62 | soft | DAG executor from phase 5 uses prompts that the library will manage |
| phase-6 | phase-62 | soft | Role system from phase 6 has embedded prompts that should be extracted to the library |
| phase-36 | phase-62 | soft | Dynamic policy engine from phase 36 and prompt library both manage agent instructions -- they should be coordinated |
| phase-52 | phase-62 | soft | Provenance tracking from phase 52 should log which prompt version was used for each execution |
| phase-4 | phase-63 | soft | REST API wraps the orchestrator core from phase 4 |
| phase-8 | phase-63 | soft | Execution history from phase 8 provides data for API status/metrics endpoints |
| phase-9 | phase-63 | soft | Review sensor scores from phase 9 are exposed via metrics endpoint |
| phase-32 | phase-63 | soft | Cost tracking from phase 32 is exposed via metrics endpoint |
| phase-59 | phase-63 | soft | Velocity metrics from phase 59 are exposed via API metrics endpoint |
| phase-11 | phase-64 | soft | Workspace lifecycle from phase 11 manages the workspaces that sandboxing protects |
| phase-15 | phase-64 | soft | Safety policies from phase 15 define what actions should be blocked -- sandboxing enforces them |
| phase-35 | phase-64 | hard | Dark factory mode from phase 35 requires sandboxing as a prerequisite -- no human review means isolation must be robust |
| phase-5 | phase-64 | soft | DAG executor from phase 5 creates the worker processes that need sandboxing |
| phase-8 | phase-64 | soft | Execution logs from phase 8 should include sandbox audit events |
| phase-20 | phase-65 | soft | Context budgeting from phase 20 ensures iteration summaries fit in smart zone limits |
| phase-8 | phase-65 | soft | Execution logs from phase 8 record each loop iteration for debugging |
| phase-5 | phase-65 | soft | DAG executor loop nodes from phase 5 are extended with stop hook support |
| phase-10 | phase-66 | soft | Garbage collector from phase 10 is the primary maintenance task to schedule |
| phase-14 | phase-66 | soft | Health monitoring from phase 14 provides daily health check data |
| phase-17 | phase-66 | soft | Invariant checker from phase 17 provides weekly architecture scans |
| phase-19 | phase-66 | soft | Self-improvement from phase 19 provides weekly analysis |
| phase-46 | phase-66 | soft | Golden principles from phase 46 provide the "deviations from golden principles" scanning target |
| phase-32 | phase-66 | soft | Cost tracking from phase 32 provides daily cost reports |
| phase-9 | phase-67 | soft | Review sensor from phase 9 provides the inferential verification check |
| phase-17 | phase-67 | soft | Invariant checker from phase 17 provides the architectural verification check |
| phase-13 | phase-67 | soft | PR automation from phase 13 is extended with pre-PR verification |
| phase-65 | phase-67 | soft | Stop hooks from phase 65 can use verification gate as a completion criterion |
| phase-8 | phase-68 | soft | Execution logs from phase 8 provide the historical data for agent profiling |
| phase-11 | phase-68 | soft | Workspace lifecycle from phase 11 provides session state for handoff detection |
| phase-6 | phase-68 | soft | Role profiles from phase 6 define the roles that affinity tracking applies to |
| phase-18 | phase-68 | soft | Trace formatter from phase 18 creates compact summaries for session handoff |
| phase-7 | phase-69 | soft | Unit tests from phase 7 provide the foundation that integration tests build on |
| phase-4 | phase-69 | soft | Orchestrator from phase 4 is the primary system under test |
| phase-5 | phase-69 | soft | DAG executor from phase 5 is a core component tested by integration suite |
| phase-23 | phase-69 | soft | E2E validation from phase 23 provides integration test scenarios |

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

## [x] phase-17: Structural Invariants Engine (COMPLETE)

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
  - [x] `p17.d2.t1` Create invariants.yaml schema and example config (depends: p17.d1.t1)
    > Define invariants.yaml schema with sections: layers (ordered list of module layers), forbidden_imports (regex patterns), dependency_rules (source_layer -> allowed_target_layers), required_annotations (functions/classes that need type hints), circular_limit (max allowed cycle length, 0 = none). Create example-invariants.yaml for a typical layered project (models/repo/service/api).
    _Files: ~/zion/projects/agent-orchestration/invariants.yaml_
  - [x] invariants.yaml schema supports forbidden_imports, layer_order, dependency_direction, required_annotations, circular_dependency_limit
    _Validation: read YAML schema_
  - [x] Example invariants.yaml provided for a typical layered project
    _Validation: read example config_
  _~80 LOC_
- [x] **Integrate invariant checker into pipelines** -- Add invariant checking as a gate in the standard and team pipelines
  - [x] `p17.d3.t1` Add invariant check to pipeline templates (depends: p17.d1.t1, p5.d3.t1)
    > Add a Bash node to standard-pipeline.yaml and team-pipeline.yaml that runs invariant_checker.py with the project's invariants.yaml. Place it after the implement node and before tests, so architectural violations are caught early. Gate the pipeline on failure (stop before tests if invariants fail).
    _Files: ~/zion/projects/agent-orchestration/pipelines/standard-pipeline.yaml, ~/zion/projects/agent-orchestration/pipelines/team-pipeline.yaml_
  - [x] standard-pipeline.yaml and team-pipeline.yaml include an invariant check node after implementation
    _Validation: read pipeline YAML_
  _~40 LOC_
- [x] **Tests for invariant checker** -- Unit tests covering all violation types and edge cases
  - [x] `p17.d4.t1` Create test_invariant_checker.py (depends: p17.d1.t1)
    > Create test fixtures (sample Python files with intentional violations) and test cases: valid project passes all checks, forbidden import detected, layer violation detected, circular dependency detected, missing type annotation detected, empty project returns clean report, invalid config handled gracefully, --fix flag corrects reorderable violations.
    _Files: ~/zion/projects/agent-orchestration/test_invariant_checker.py_
  - [x] Test file with 10+ test cases covering AST parsing, layer enforcement, cycle detection
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
  - [x] `p18.d1.t1` Create trace_formatter.py module (depends: p8.d1.t1)
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
  - [x] `p18.d3.t1` Add failure correlation to trace_formatter (depends: p18.d1.t1)
    > Add --correlate flag to trace_formatter.py that: (1) reads the last N pipeline runs, (2) groups failures by node_id and failure_type, (3) identifies recurring patterns (same node failing in >50% of runs), (4) outputs a summary: "Node 'test' failed in 8/10 recent runs. Common error: ImportError. Suggested fix: check dependencies." This enables the orchestrator or a human to spot systemic issues.
    _Files: ~/zion/projects/agent-orchestration/trace_formatter.py_
  - [ ] Can identify that a specific node type or pipeline step fails repeatedly across runs
    _Validation: python3 trace_formatter.py --correlate --last 20_
  _~80 LOC_
- [ ] **Self-debug pipeline template** -- Pipeline YAML that uses trace tools to enable agents to debug and fix their own failures
  - [x] `p18.d4.t1` Create debug-pipeline.yaml (depends: p18.d2.t1, p5.d3.t1)
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
  - [x] `p19.d1.t1` Create self_improve.py analyzer module (depends: p8.d1.t1)
    > Python module that: (1) reads all pipeline runs from execution_log.py, (2) computes per-node failure rates, (3) identifies failure sequences (which nodes fail after which), (4) detects bottlenecks (slowest nodes, most retried loops), (5) identifies pipeline-level patterns (which pipelines have lowest success rate), (6) outputs structured JSON report with findings and suggested actions. Support --period flag for time-windowed analysis.
    _Files: ~/zion/projects/agent-orchestration/self_improve.py_
  - [ ] Can identify top 5 failing nodes across all runs with failure rates
    _Validation: python3 self_improve.py --analyze --last 50_
  - [ ] Detects patterns like "test node fails 60% of the time after implement node" or "loop node always hits max iterations"
    _Validation: run analysis on synthetic history_
  _~150 LOC_
- [ ] **Parameter auto-tuner** -- Automatically adjust pipeline parameters (loop max, timeout, retry count) based on historical performance
  - [x] `p19.d2.t1` Add parameter tuning to self_improve.py (depends: p19.d1.t1)
    > Add --tune mode to self_improve.py: (1) analyze loop nodes to determine if max_iterations is too low (most loops hit the limit) or too high (loops almost never reach it), (2) analyze timeout values for bash nodes (are tests timing out?), (3) suggest adjusted values with confidence scores, (4) support --apply flag to write suggested values back to pipeline YAML files, (5) keep a tuning history log to track changes over time.
    _Files: ~/zion/projects/agent-orchestration/self_improve.py_
  - [ ] Can suggest parameter adjustments based on failure patterns (e.g., "loop max 3 is insufficient, 80% of loops hit the limit")
    _Validation: python3 self_improve.py --tune_
  _~100 LOC_
- [ ] **Weekly self-review cron** -- Cron job that runs the analyzer weekly and generates an improvement report
  - [x] `p19.d3.t1` Create weekly self-review cron (depends: p19.d1.t1)
    > Create a weekly Hermes cron that runs self_improve.py --analyze --period week and outputs a summary report. The report includes: top failure patterns, pipeline success rates, parameter tuning suggestions, and a "health score" for the orchestrator. Optionally creates GitHub Issues for high-priority findings. Keep the report in ~/.orchestrator/reports/ for historical comparison.
  - [ ] Cron job runs weekly and outputs a structured improvement report
    _Validation: cronjob list_
  _~30 LOC_
- [ ] **Improvement action executor** -- Module that can automatically apply low-risk improvements suggested by the analyzer
  - [x] `p19.d4.t1` Add improvement executor to self_improve.py (depends: p19.d2.t1, p13.d1.t1)
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

## [ ] phase-42: External Application Observability Integration (PLANNED)

**Goal:** Enable agents to access target application logs, metrics, and traces during pipeline execution for effective debugging and verification

The Harness Engineering research explicitly identifies "Integrated Observability: Providing agents with local access to logs, metrics, and traces so they can reason about the behavior of the code they have just written" as a core pillar of Application Legibility. Currently, agents can run tests and lint but cannot inspect the target application's runtime behavior. This creates a significant blind spot: agents can write code that passes unit tests but fails in production due to runtime issues they cannot observe. This phase adds an observability bridge that: (1) discovers and reads application log files from the target project, (2) parses common log formats (structured JSON, unstructured text, common frameworks), (3) surfaces relevant log entries as context in AI node prompts when debugging or verifying changes, (4) supports reading metrics from local metrics endpoints (Prometheus, /health, /metrics), (5) adds an OBSERVE node type to the DAG executor for explicit observability checks. This closes the Application Legibility gap for runtime behavior.

### Deliverables

- [ ] **Log discovery and parsing module** -- Python module that discovers, reads, and parses application log files from target projects
  - [ ] `p42.d1.t1` Create observability.py log discovery module
    > Create observability.py: (1) discover_logs(project_dir) -- scan for log files in common locations: logs/, var/log/, *.log, docker-compose stdout captures, CI artifacts, (2) parse_logs(log_path, format="auto") -- detect format (JSON, key=value, common frameworks like Django/Flask/Express), return structured list of log entries, (3) search_logs(entries, query) -- filter by level (ERROR, WARN), time range, message pattern, (4) tail_logs(log_path, n=50) -- return the last N entries for recent error context, (5) summarize_logs(entries) -- produce a concise summary suitable for agent context (error counts by type, recent errors, warnings). Auto-detect log rotation (compressed files, numbered suffixes).
    _Files: ~/zion/projects/agent-orchestration/observability.py_
  - [ ] Module can discover log files in common locations (logs/, var/log, stdout captures)
    _Validation: python3 observability.py discover --project /path/to/project_
  - [ ] Supports structured JSON logs and common unstructured formats
    _Validation: feed sample log files, verify parsed output_
  _~150 LOC_
- [ ] **Metrics endpoint reader** -- Module that reads metrics from local application endpoints (Prometheus, /health, /metrics)
  - [ ] `p42.d2.t1` Add metrics reader to observability.py (depends: p42.d1.t1)
    > Add metrics reading to observability.py: (1) read_metrics(url, format="auto") -- fetch metrics from a local endpoint, auto-detect format (Prometheus text, JSON, health check), (2) parse_prometheus(text) -- parse Prometheus exposition format into structured metrics, (3) extract_key_metrics(metrics) -- pull out common signals: request_total, error_total, latency_p50/p95/p99, up status, (4) diff_metrics(before, after) -- compare metric snapshots before and after a code change to detect regressions, (5) --wait-for-ready flag to poll until an endpoint responds (useful after starting a dev server). Timeout after 30 seconds.
    _Files: ~/zion/projects/agent-orchestration/observability.py_
  - [ ] Can read metrics from a running local application endpoint
    _Validation: start a test server with /metrics, run reader, verify output_
  - [ ] Extracts key metrics (request counts, error rates, latency percentiles)
    _Validation: check parsed output for expected metric names_
  _~120 LOC_
- [ ] **OBSERVE node type for DAG executor** -- Add an OBSERVE node type that reads logs/metrics during pipeline execution and surfaces findings to subsequent AI nodes
  - [ ] `p42.d3.t1` Add OBSERVE node type to DAG executor (depends: p42.d1.t1, p42.d2.t1)
    > Add NodeType.OBSERVE to dag.py. The observe node takes: logs (list of log file glob patterns or "auto" for discovery), metrics_url (optional endpoint URL), filters (error level, time range, patterns), assert (optional: "no_errors", "error_count < N", "latency_p95 < 500ms"). Executor calls observability.py to read logs/metrics, formats findings as a structured summary, and injects it into the pipeline context for subsequent AI nodes. If assert fails, node fails with details. This lets agents see runtime behavior without manual log diving.
    _Files: ~/zion/projects/agent-orchestration/dag.py, ~/zion/projects/agent-orchestration/executor.py_
  - [ ] Pipeline YAML can include OBSERVE nodes for log and metric checks
    _Validation: create pipeline with OBSERVE node, execute it_
  - [ ] AI nodes after OBSERVE receive log/metric context in their prompts
    _Validation: check AI node prompt includes observability data_
  _~100 LOC_
- [ ] **Debug-aware pipeline template** -- Pipeline YAML that integrates observability checks for debugging and verification
  - [ ] `p42.d4.t1` Create debug-pipeline.yaml (depends: p42.d3.t1)
    > Create pipelines/debug-pipeline.yaml: AI(analyze issue) -> OBSERVE(read logs before change, assert no pre-existing errors) -> AI(implement fix) -> Bash(test) -> OBSERVE(read logs after change, assert no new errors) -> AI(review, with log context) -> Bash(commit). This pipeline gives agents full visibility into runtime behavior. Include env vars for log paths and metrics URL. The before/after OBSERVE comparison catches regressions that unit tests miss.
    _Files: ~/zion/projects/agent-orchestration/pipelines/debug-pipeline.yaml_
  - [ ] Pipeline template includes OBSERVE nodes for log-based debugging
    _Validation: read pipeline YAML, trace through nodes_
  _~60 LOC_

### Technical Notes

Observability integration is the bridge between "agent writes code" and "agent understands the system." The key insight from Harness Engineering is that agents need to be able to verify their own work at the application level, not just the unit test level. Log discovery is heuristic-based -- check common locations, don't require configuration. Metrics reading requires the target app to be running -- the OBSERVE node should gracefully degrade if the app is not running (skip, don't fail). Log injection into AI prompts must be size-limited to avoid context bloat -- summarize, don't dump raw logs.

### Risks

- Log files may be large -- need tailing and summarization, not full reads
- Log formats vary wildly across projects -- auto-detection will have blind spots
- Metrics endpoints may not exist or use non-standard formats -- need graceful degradation
- Reading logs could expose sensitive information -- filter out secrets, PII before injection
- OBSERVE nodes add pipeline latency (waiting for app startup, reading logs) -- keep them focused

## [ ] phase-43: Automated Refactoring Pipeline (Self-Healing Codebase) (PLANNED)

**Goal:** Combine garbage collection scanning with automated fix generation and PR creation into an autonomous self-healing pipeline

The research describes the future outlook: "codebases are inherently self-correcting. Garbage Collection Loops run weekly as background tasks, scanning for deviations from golden principles and opening targeted refactoring pull requests." Phase 10 (GC) scans for convention violations and reports them. Phase 13 (PR automation) creates PRs from workspace branches. But these two capabilities are not connected -- GC findings require manual action to fix. This phase closes the loop by creating an automated refactoring pipeline that: (1) runs GC scanning to detect violations, (2) categorizes findings by severity and effort, (3) delegates each fix to an AI worker with the violation as context, (4) runs tests to verify the fix doesn't break anything, (5) creates a PR for each batch of fixes. This is the "Self-Correcting Codebase" from the research made real: the orchestrator not only detects drift but actively repairs it.

### Deliverables

- [ ] **Refactoring job generator** -- Module that takes GC scan results and generates prioritized refactoring jobs
  - [ ] `p43.d1.t1` Create refactoring.py job generator
    > Create refactoring.py: (1) generate_jobs(gc_findings) -- take output from garbage_collector.py --conventions, categorize by: severity (error > warning > style), fix_effort (simple rename > moderate refactor > complex restructure), file_group (group findings in same file/directory), (2) prioritize_jobs(jobs) -- sort by severity * confidence, then group into PR-sized batches (max 10 files per PR), (3) estimate_tokens(jobs) -- estimate tokens needed for each job (for budget awareness from phase 32), (4) filter_jobs(jobs, scope) -- allow filtering by category, file pattern, or severity threshold, (5) --dry-run to preview what refactoring PRs would be created without actually making changes. Output as structured JSON.
    _Files: ~/zion/projects/agent-orchestration/refactoring.py_
  - [ ] Can take GC findings and produce a prioritized list of fix jobs
    _Validation: run GC scan, feed results to generator, verify job list_
  - [ ] Jobs are grouped by file/area to minimize PR size
    _Validation: check that related findings are grouped_
  _~120 LOC_
- [ ] **Autonomous fix execution pipeline** -- Pipeline YAML that autonomously fixes detected violations and creates PRs
  - [ ] `p43.d2.t1` Create auto-refactor-pipeline.yaml (depends: p43.d1.t1, p42.d3.t1)
    > Create pipelines/auto-refactor-pipeline.yaml: OBSERVE(scan logs for context) -> AI(analyze GC findings, plan fixes) -> Loop(fix violations, max=5 per iteration) -> Bash(run tests) -> Loop(retry on test failure, max=3) -> REVIEW(LLM judge for fix quality) -> Bash(create branch, commit fixes) -> Bash(create PR with detailed description of what was fixed and why). The pipeline is designed to be run by the orchestrator as a cron job, creating refactoring PRs that humans can review and merge.
    _Files: ~/zion/projects/agent-orchestration/pipelines/auto-refactor-pipeline.yaml_
  - [ ] Pipeline takes a GC finding, fixes it, tests the fix, and creates a PR
    _Validation: create a test violation, run pipeline, verify fix and PR_
  - [ ] Multiple violations are batched into a single PR when related
    _Validation: create 3 violations in same file, verify single PR_
  _~80 LOC_
- [ ] **Refactoring cron job integration** -- Weekly cron job that runs the full refactoring cycle: scan, fix, PR
  - [ ] `p43.d3.t1` Create refactoring cron job (depends: p43.d2.t1)
    > Create a weekly Hermes cron job that: (1) runs garbage_collector.py --conventions on target projects, (2) feeds findings to refactoring.py generate_jobs, (3) for each job batch, runs the auto-refactor pipeline, (4) creates PRs for each batch, (5) reports summary (violations found, fixes attempted, fixes succeeded, PRs created). Include budget check: skip refactoring if weekly token budget is nearly exhausted (from phase 32). Respect safety policies from phase 15 (no auto-merge for refactoring PRs -- always human review).
  - [ ] Cron job runs the refactoring pipeline weekly
    _Validation: cronjob list_
  - [ ] Respects token budget limits (from phase 32)
    _Validation: check cron prompt for budget check_
  _~40 LOC_
- [ ] **Refactoring effectiveness tracking** -- Track the long-term impact of automated refactoring on codebase health
  - [ ] `p43.d4.t1` Add effectiveness tracking to refactoring.py (depends: p43.d1.t1)
    > Add --report mode to refactoring.py: (1) track refactoring history in ~/.orchestrator/logs/refactoring/ (jobs generated, fixes attempted, tests passed/failed, PRs created, PRs merged), (2) compute recurrence rate -- do fixed violations come back? (indicates the GC rules or agent fixes need improvement), (3) track violation trend -- is the total violation count decreasing over time? (4) track fix quality -- what percentage of refactoring PRs pass review without changes? (5) output weekly/monthly summary. This closes the feedback loop: measure the impact of self-healing on codebase health.
    _Files: ~/zion/projects/agent-orchestration/refactoring.py_
  - [ ] Can report refactoring trends: violations fixed over time, recurrence rate
    _Validation: python3 refactoring.py --report --period month_
  _~80 LOC_

### Technical Notes

The self-healing pipeline is the realization of the "Self-Correcting Codebase" vision from the research. The key design decision is that refactoring PRs always require human review (never auto-merge) -- this is a safety boundary. The pipeline batches related fixes into single PRs to avoid PR fatigue. Recurrence tracking is critical: if the same violation keeps coming back, either the GC rule is wrong or the agent fix is insufficient. The refactoring cron should run weekly (not daily) to avoid overwhelming reviewers with PRs.

### Risks

- Automated fixes could introduce bugs -- always run tests and require human review
- Refactoring PRs could conflict with active development -- merge queue from phase 21 helps
- GC findings may be noisy (false positives) -- need confidence threshold before auto-fixing
- Weekly refactoring PRs could accumulate if not reviewed -- track stale PRs
- Token costs for refactoring scale with codebase size -- need per-project budget limits

## [ ] phase-44: System Health Scorecard and Effectiveness Trends (PLANNED)

**Goal:** Track and report the orchestrator''s overall effectiveness over time with historical trend analysis and a health scorecard

The research cites specific effectiveness metrics: "500% increase in landed pull requests within the first three weeks" and "10x increase in development velocity." These are system-level metrics that measure the orchestrator's overall impact, not just individual run outcomes. Phase 8 (execution history) logs individual pipeline runs. Phase 27 (live dashboard) shows real-time state. But no phase aggregates historical data into effectiveness trends or produces a health scorecard that answers: "Is the orchestrator getting better or worse over time?" This phase adds: (1) a metrics aggregation engine that computes weekly/monthly KPIs from execution logs, (2) a health scorecard that summarizes system health in a single score (0-100), (3) trend analysis that detects improvements and regressions in orchestrator effectiveness, (4) automated reporting that surfaces actionable insights. This is essential for the Dark Factory model (phase 35) -- you cannot trust an autonomous system without measuring its effectiveness.

### Deliverables

- [ ] **Metrics aggregation engine** -- Module that computes KPIs from execution history logs
  - [ ] `p44.d1.t1` Create health_scorecard.py aggregation engine (depends: p8.d1.t1)
    > Create health_scorecard.py: (1) compute_kpis(period="week"|"month", repo=None) -- aggregate execution logs from phase 8 into KPIs: issues_resolved, prs_landed, prs_created, success_rate (pipeline runs that complete without failure), avg_time_to_resolution (issue open to PR merged), avg_pipeline_duration, test_pass_rate, cost_per_issue, agent_turns_per_issue, (2) compare_periods(current, previous) -- compute week-over-week or month-over-month changes for each KPI, (3) detect_anomalies(kpis) -- flag KPIs that deviate significantly from historical baseline (>2 standard deviations), (4) --format table|json|markdown for different output modes. Store computed KPIs in ~/.orchestrator/metrics/kpis-YYYY-MM-DD.jsonl for historical analysis.
    _Files: ~/zion/projects/agent-orchestration/health_scorecard.py_
  - [ ] Computes weekly KPIs: PRs landed, issues resolved, success rate, avg time-to-resolution
    _Validation: python3 health_scorecard.py --kpi --period week_
  - [ ] Reads from execution history created by phase 8
    _Validation: generate test execution logs, verify KPI computation_
  _~150 LOC_
- [ ] **Health scorecard computation** -- Composite health score (0-100) derived from multiple effectiveness signals
  - [ ] `p44.d2.t1` Add health score computation to health_scorecard.py (depends: p44.d1.t1)
    > Add health score to health_scorecard.py: (1) compute_health_score(kpis) -- weighted composite score from: success_rate (weight 0.30), test_pass_rate (0.20), cost_efficiency (issues per $1 of tokens, 0.15), time_efficiency (avg resolution time vs SLA, 0.15), quality_score (from review sensor phase 9, 0.10), coverage (fraction of repo issues handled, 0.10), (2) health_level(score) -- map to: excellent (85+), good (70-84), fair (55-69), poor (40-54), critical (<40), (3) trend_direction(score_history) -- is the score improving, stable, or declining over the last N periods?, (4) scorecard_config.yaml defines weights, thresholds, and anomaly detection parameters. Output as a visual scorecard with emoji indicators for each signal.
    _Files: ~/zion/projects/agent-orchestration/health_scorecard.py, ~/zion/projects/agent-orchestration/scorecard_config.yaml_
  - [ ] Outputs a single health score with breakdown by signal
    _Validation: python3 health_scorecard.py --score_
  - [ ] Score weights are configurable
    _Validation: read scorecard_config.yaml_
  _~120 LOC_
- [ ] **Trend analysis and regression detection** -- Detect long-term trends in orchestrator effectiveness and flag regressions
  - [ ] `p44.d3.t1` Add trend analysis to health_scorecard.py (depends: p44.d1.t1, p44.d2.t1)
    > Add trend analysis to health_scorecard.py: (1) analyze_trends(kpi_history, periods=8) -- compute linear regression slope for each KPI over the last N weeks, classify as: improving (slope > threshold), stable (near zero), declining (slope < -threshold), (2) correlate_metrics(kpis) -- find correlations between metrics (e.g., does higher agent_turns correlate with higher success rate?), (3) generate_recommendations(trends) -- based on declining metrics, suggest actions: "Success rate declining -- check if recent issues are harder (more complex labels)" or "Cost per issue increasing -- review routing rules from phase 40", (4) --trend-report produces a markdown summary with tables and recommendations. Store trend analysis in ~/.orchestrator/metrics/trends.jsonl.
    _Files: ~/zion/projects/agent-orchestration/health_scorecard.py_
  - [ ] Can identify when success rate or cost efficiency is declining over time
    _Validation: generate test data with declining trend, verify detection_
  - [ ] Produces actionable recommendations for improving declining metrics
    _Validation: check trend report for recommendations_
  _~100 LOC_
- [ ] **Weekly effectiveness report cron job** -- Automated weekly report that surfaces orchestrator health and actionable insights
  - [ ] `p44.d4.t1` Create weekly effectiveness report cron job (depends: p44.d2.t1, p44.d3.t1)
    > Create a weekly Hermes cron job that: (1) runs health_scorecard.py to compute KPIs and health score, (2) runs trend analysis to detect regressions, (3) generates a markdown report with: health scorecard (with breakdown), KPI table (current vs previous period), trend indicators, actionable recommendations, top issues by resolution time, cost summary, (4) saves report to ~/zion/projects/agent-orchestration/reports/weekly-YYYY-MM-DD.md. The report is designed for human consumption -- a weekly "orchestrator health check" that answers "how is the system doing?" in one page.
  - [ ] Cron job generates and delivers a weekly effectiveness report
    _Validation: cronjob list_
  _~40 LOC_

### Technical Notes

The health scorecard is the "instrument panel" for the orchestrator. The key insight from the research is that effective systems are measured systems -- you cannot improve what you cannot measure. The score is a composite of multiple signals, not a single metric, to avoid gaming any one number. Trend analysis uses simple linear regression -- no ML needed. The weekly report is designed for quick human scanning: one page, clear signals, actionable recommendations. Historical KPI data should be retained indefinitely for long-term trend analysis (JSONL files are compact).

### Risks

- KPI definitions may not capture what matters -- need iteration based on real usage
- Health score could mask individual metric regressions if weights are wrong -- show full breakdown
- Trend analysis on small datasets (first few weeks) will be noisy -- require minimum data before flagging
- Weekly reports add noise if the system is stable -- include "no significant changes" summary

## [ ] phase-45: Symphony Spec Compliance and WORKFLOW.md Engine (PLANNED)

**Goal:** Align the Hermes orchestrator with the OpenAI Symphony SPEC.md format, implementing WORKFLOW.md as a per-project policy engine

The research doc details Symphony's SPEC.md with specific config parameters (tracker.kind, polling.interval_ms, agent.max_turns, agent.max_concurrent, codex.approval_policy) and the WORKFLOW.md concept as a per-project policy engine that defines prompt templates and runtime settings. Phase 36 (Dynamic Policy Engine) covers general policy loading, but does not implement the specific WORKFLOW.md format or Symphony spec parameter alignment. This phase makes the orchestrator directly compatible with the Symphony specification format, enabling projects that define WORKFLOW.md files to be picked up automatically -- just like Symphony does. It also maps Symphony's config params to Hermes equivalents so teams migrating from Symphony to Hermes have a clear translation path.

### Deliverables

- [ ] **WORKFLOW.md parser and validator** -- Python module that reads WORKFLOW.md files and extracts pipeline templates, prompt settings, and runtime parameters in Symphony-spec format
  - [ ] `p45.d1.t1` Create workflow_parser.py module
    > Python module that: (1) reads WORKFLOW.md from a project root, (2) extracts structured sections: pipeline (node definitions, edges), prompts (per-role prompt templates), settings (max_turns, approval_policy, timeout), (3) validates against a JSON schema for WORKFLOW.md format, (4) converts Symphony-spec settings to Hermes orchestrator.yaml equivalents, (5) supports fallback: if WORKFLOW.md is missing, use default pipeline and AI_GUIDE.md. Output as a WorkflowConfig dataclass.
    _Files: ~/zion/projects/agent-orchestration/workflow_parser.py_
  - [ ] Module can parse a WORKFLOW.md file and extract pipeline, prompts, and settings
    _Validation: python3 workflow_parser.py --file WORKFLOW.md_
  - [ ] Validates WORKFLOW.md against a schema (required sections, valid parameter names)
    _Validation: create invalid WORKFLOW.md, verify parser reports errors_
  _~120 LOC_
- [ ] **Symphony-to-Hermes config translator** -- Module that maps Symphony SPEC.md parameters to Hermes orchestrator.yaml equivalents
  - [ ] `p45.d2.t1` Add Symphony config translation to workflow_parser.py
    > Add --translate mode to workflow_parser.py: (1) read a Symphony-spec config YAML, (2) map each Symphony parameter to its Hermes equivalent (tracker.kind -> poller backend, polling.interval_ms -> orchestrator polling_interval, agent.max_turns -> role max_turns, agent.max_concurrent -> orchestrator max_concurrent, codex.approval_policy -> safety approval_mode), (3) output a valid orchestrator.yaml with comments showing the original Symphony parameter, (4) flag any Symphony features with no Hermes equivalent. Include a translation reference table in the output.
    _Files: ~/zion/projects/agent-orchestration/workflow_parser.py_
  - [ ] Can translate Symphony config (tracker.kind, polling.interval_ms, agent.max_turns, etc.) to Hermes config format
    _Validation: python3 workflow_parser.py --translate --symphony-config symphony.yaml_
  _~80 LOC_
- [ ] **WORKFLOW.md integration with spawner** -- Auto-detect and use WORKFLOW.md when spawning workers for a project
  - [ ] `p45.d3.t1` Integrate WORKFLOW.md detection into spawner.py
    > Modify spawner.py to: (1) before spawning, check for WORKFLOW.md in the target repo root, (2) if found, parse it with workflow_parser.py, (3) use the WORKFLOW.md pipeline instead of the default pipeline from orchestrator.yaml, (4) apply WORKFLOW.md prompt templates per role, (5) apply WORKFLOW.md runtime settings (max_turns, timeout), (6) log which workflow file was used for each spawn. If WORKFLOW.md is missing, fall back to orchestrator.yaml defaults (existing behavior).
    _Files: ~/zion/projects/agent-orchestration/spawner.py_
  - [ ] Spawner checks for WORKFLOW.md in the target repo and uses its pipeline/prompts if present
    _Validation: create a test WORKFLOW.md, spawn worker, verify it uses the custom pipeline_
  _~60 LOC_
- [ ] **Example WORKFLOW.md template** -- Reference WORKFLOW.md template that projects can copy and customize
  - [ ] `p45.d4.t1` Create WORKFLOW.md.template
    > Create WORKFLOW.md.template with: (1) pipeline section (example DAG with all node types), (2) prompts section (per-role prompt templates with placeholders), (3) settings section (all configurable parameters with comments explaining each), (4) header comments explaining the format and how it maps to Symphony SPEC.md, (5) link to the workflow_parser.py --validate command for checking syntax. Include a minimal version (WORKFLOW.md.minimal) for simple projects.
    _Files: ~/zion/projects/agent-orchestration/WORKFLOW.md.template, ~/zion/projects/agent-orchestration/WORKFLOW.md.minimal_
  - [ ] Template WORKFLOW.md exists with documentation of all supported sections
    _Validation: read template file, verify sections match parser schema_
  _~80 LOC_

### Technical Notes

WORKFLOW.md is Symphony's key innovation for per-project policy. Making Hermes compatible with this format means projects can be shared between Symphony and Hermes orchestrators. The parser should be lenient: unknown sections are ignored, missing sections use defaults. The translation layer is important for teams migrating from Symphony to Hermes.

### Risks

- WORKFLOW.md format may evolve as Symphony matures -- parser needs version tolerance
- Per-project WORKFLOW.md files could conflict with orchestrator.yaml global settings -- need clear precedence rules
- Translation may lose information for Symphony features with no Hermes equivalent

## [ ] phase-46: Golden Principles Registry and Evolution (PLANNED)

**Goal:** Create a formal, evolving registry of "golden principles" and "taste invariants" that GC loops and agents measure against

The research describes "Garbage Collection Loops" scanning for deviations from "golden principles" and the human role as defining "taste invariants" (security, performance, user experience). Phase 10 implements convention scanning against AI_GUIDE.md rules, but there is no formal concept of golden principles as a separate, evolving entity. Golden principles are higher-level than code conventions -- they represent architectural and qualitative goals that persist across refactors and evolve over time. This phase creates a principles.yaml registry where Jericho (or an LLM) defines these principles, the GC scanner measures codebases against them, and the self-improvement loop tracks principle compliance over time. This is the bridge between "human defines taste" and "agents implement taste" from the research.

### Deliverables

- [ ] **Principles registry schema and storage** -- YAML schema for defining golden principles with categories, severity, and evolution metadata
  - [ ] `p46.d1.t1` Create principles.yaml schema and default registry
    > Define principles.yaml schema with: (1) principles list, each with: id, name, category (security/performance/readability/architecture/testability), description, severity (critical/high/medium/low), check_type (structural/convention/semantic), created_at, created_by (human/agent), status (active/deprecated/superseded), superseded_by (if replaced), (2) global settings: scan_frequency, evolution_mode (manual/auto-suggest), compliance_threshold. Create a default principles.yaml with 10-15 common principles: "no circular dependencies", "all public APIs have type annotations", "test coverage above 80%", "no secrets in code", "functions under 50 lines", "no god classes", "error handling at boundaries", etc.
    _Files: ~/zion/projects/agent-orchestration/principles.yaml_
  - [ ] principles.yaml schema supports categories (security, performance, readability, architecture), severity levels, and deprecation metadata
    _Validation: read schema, verify structure_
  _~100 LOC_
- [ ] **Principles compliance checker** -- Module that measures a codebase against the principles registry and produces a compliance score
  - [ ] `p46.d2.t1` Create principles_checker.py module
    > Python module that: (1) loads principles.yaml, (2) for each active principle, runs the appropriate check: structural (AST analysis, import graph, line counting) or semantic (LLM assessment via delegate_task for qualitative principles like "good error messages"), (3) outputs a compliance report with per-principle score (0-100), overall score (weighted average), and violations list, (4) supports --format json|markdown|terminal, (5) supports --baseline to store current scores and --diff to compare against baseline. Structural checks use existing tools from invariant_checker.py and gc_scanner.py. Semantic checks use a focused LLM prompt per principle.
    _Files: ~/zion/projects/agent-orchestration/principles_checker.py_
  - [ ] Can scan a codebase and produce per-principle compliance scores and an overall score
    _Validation: python3 principles_checker.py --scan . --principles principles.yaml_
  - [ ] Supports both structural checks (AST-based) and semantic checks (LLM-based)
    _Validation: run with mixed check types_
  _~150 LOC_
- [ ] **Principles evolution workflow** -- Enable principles to be added, deprecated, and evolved over time with full audit trail
  - [ ] `p46.d3.t1` Add principle lifecycle management to principles_checker.py
    > Add to principles_checker.py: (1) --add-principle mode: interactive prompt to define a new principle (name, category, description, check_type), append to principles.yaml, (2) --deprecate mode: mark a principle as deprecated with reason and replacement, (3) --evolve mode: LLM analyzes compliance history and suggests new principles based on recurring violations that are not covered by existing principles, (4) --history mode: show evolution timeline of all principle changes, (5) store evolution history in ~/.orchestrator/principles/history.jsonl. The evolution mode is the key innovation -- the system learns what principles it needs based on what it keeps finding wrong.
    _Files: ~/zion/projects/agent-orchestration/principles_checker.py_
  - [ ] Can add a new principle, deprecate an old one, and track the evolution history
    _Validation: python3 principles_checker.py --add-principle --evolve_
  _~100 LOC_
- [ ] **Principles integration with GC and self-improvement** -- Wire principles compliance into the garbage collection loop and self-improvement analysis
  - [ ] `p46.d4.t1` Integrate principles into GC and self-improvement
    > Modify garbage_collector.py to include principles_checker as a scan step (after convention scanning), reporting principle violations alongside convention violations. Modify self_improve.py (phase 19) to track principle compliance scores over time and include them in the improvement report. Add a principles compliance section to the health scorecard (phase 44). This creates a closed loop: principles define quality -> GC measures compliance -> self-improvement tracks trends -> evolution suggests new principles.
    _Files: ~/zion/projects/agent-orchestration/garbage_collector.py_
  - [ ] GC loop includes principles compliance in its scan output
    _Validation: run GC scan, check output includes principles scores_
  - [ ] Self-improvement analyzer tracks principle compliance trends over time
    _Validation: run self-improve analysis, check for principles section_
  _~60 LOC_

### Technical Notes

The key distinction from existing phases: conventions (phase 10) are style rules (naming, imports), invariants (phase 17) are architectural rules (layering, dependencies), and principles (this phase) are qualitative goals (readability, testability, security posture). Principles are the "taste invariants" from the research -- they require human judgment to define but can be mechanically measured once defined. The evolution workflow is what makes this phase unique: the system suggests new principles based on what it observes.

### Risks

- Semantic checks (LLM-based) are expensive and inconsistent -- use sparingly, only for high-value principles
- Too many principles creates noise -- start with 10-15 and grow slowly
- Principle evolution could drift from original intent -- human review required for all new principles

## [ ] phase-47: Cattle vs Pets Worker Model (Session Identity and Disposability) (PLANNED)

**Goal:** Implement the Symphony/Gas Town pattern of treating agent sessions as disposable "cattle" while maintaining persistent identity and project knowledge as "pets"

The research describes the orchestrator treating "individual agent sessions as ephemeral cattle, while treating the agent's identity and the project's state as persistent pets." This architectural pattern is fundamental to the Dark Factory model: workers are thrown away after each task, but knowledge accumulates. Currently, the Hermes orchestrator creates workspaces but has no concept of worker identity (each worker is anonymous), no knowledge persistence between sessions (each pipeline run starts fresh), and no explicit disposability model (workspaces persist indefinitely). This phase adds: (1) worker identity cards that track what each worker "learned" during its session, (2) a knowledge carry-forward system that injects relevant past-learnings into new worker sessions, (3) explicit session lifecycle (spawn -> work -> harvest -> dispose) with knowledge extraction at harvest time, (4) a "pet" store for persistent project-level knowledge that survives across all worker sessions.

### Deliverables

- [ ] **Worker identity and session tracking** -- Assign unique identities to worker sessions and track what each worker learns
  - [ ] `p47.d1.t1` Add worker identity system to spawner.py
    > Modify spawner.py to: (1) generate a unique worker_id (UUID) for each session, (2) create a session card at workspace/.orchestrator/session.json with: worker_id, role, spawned_at, issue_number, pipeline, status, (3) during pipeline execution, append "learnings" to the session card: files_created, files_modified, errors_encountered, solutions_applied, (4) on completion, write a session_summary with: total duration, nodes executed, files changed, success/failure, key_insights (extracted from AI node outputs). This makes each worker traceable and its session inspectable after disposal.
    _Files: ~/zion/projects/agent-orchestration/spawner.py_
  - [ ] Each worker session has a unique ID, role, and learns log
    _Validation: spawn a worker, check session metadata_
  _~80 LOC_
- [ ] **Knowledge carry-forward system** -- Extract and persist learnings from completed sessions for injection into future sessions
  - [ ] `p47.d2.t1` Create knowledge_store.py module
    > Python module that: (1) on session completion (harvest), extracts key learnings from session.json: what worked, what failed, what files were involved, (2) stores learnings in a per-repo knowledge base at ~/.orchestrator/knowledge/{repo}/ as JSONL files indexed by topic (file paths, error types, task types), (3) on new session spawn, queries the knowledge base for relevant past learnings based on: files involved in the current issue, labels, similar issue titles, (4) formats relevant learnings as a compact context block (<500 tokens) for injection into the AI node prompt, (5) supports --query to manually search the knowledge base and --prune to remove stale entries. The carry-forward is the "pet" -- knowledge persists even though the "cattle" (worker) is disposed.
    _Files: ~/zion/projects/agent-orchestration/knowledge_store.py_
  - [ ] Learnings from past sessions are available for injection into new worker prompts
    _Validation: complete a session, start a new one on similar task, check prompt includes past learnings_
  _~150 LOC_
- [ ] **Session harvest and disposal pipeline** -- Formalize the worker lifecycle with knowledge extraction at harvest time
  - [ ] `p47.d3.t1` Add harvest step to orchestrator session lifecycle
    > Modify orchestrator.py and workspace_manager.py to: (1) after pipeline completion (success or failure), run a "harvest" step that calls knowledge_store.py extract(), (2) harvest extracts: files changed (from git diff), errors encountered (from execution log), solutions that worked (from AI node outputs), (3) write harvested knowledge to the knowledge base, (4) then proceed to workspace archival (existing cleanup from phase 11), (5) add a HARVEST node type to dag.py that can be included in pipelines to trigger mid-session knowledge extraction (useful for long-running pipelines). The harvest step is what transforms disposable sessions into persistent organizational knowledge.
    _Files: ~/zion/projects/agent-orchestration/orchestrator.py, ~/zion/projects/agent-orchestration/workspace_manager.py, ~/zion/projects/agent-orchestration/dag.py_
  - [ ] Completed sessions are harvested (learnings extracted) before disposal (workspace archived)
    _Validation: complete a pipeline, verify harvest step runs before archival_
  _~100 LOC_
- [ ] **Persistent project knowledge ("pets")** -- Maintain a project-level knowledge store that accumulates across all worker sessions
  - [ ] `p47.d4.t1` Add project knowledge summary and analytics to knowledge_store.py
    > Add to knowledge_store.py: (1) --project-summary mode that outputs: total sessions, total learnings, most-modified files, common error patterns, successful solution patterns, knowledge coverage (which files/areas have accumulated the most knowledge), (2) --knowledge-graph mode that shows relationships between learnings (file A and file B are often modified together, error X is usually caused by pattern Y), (3) integrate with the executor prompt builder so project knowledge is automatically injected into AI node prompts when available, (4) add a knowledge retention policy: learnings older than N days with no re-use are pruned, keeping the knowledge base fresh and relevant. The project knowledge is the ultimate "pet" -- it outlives every individual worker session.
    _Files: ~/zion/projects/agent-orchestration/knowledge_store.py_
  - [ ] Project knowledge grows over time as more sessions complete
    _Validation: run 3 sessions, check knowledge base has entries from all 3_
  - [ ] Knowledge can be queried to understand what the system has learned about a project
    _Validation: python3 knowledge_store.py --project-summary --repo owner/repo_
  _~100 LOC_

### Technical Notes

The "cattle vs pets" metaphor is the core architectural insight. Workers (cattle) are created, do work, and are destroyed. Knowledge (pets) persists and grows. The knowledge store is the "organizational memory" of the orchestrator. Keep learnings compact -- store patterns, not raw outputs. The harvest step is critical: it is the moment where disposable session state becomes persistent organizational knowledge. Without harvest, every session starts from zero.

### Risks

- Knowledge extraction quality depends on the session summary -- poorly summarized sessions add noise
- Knowledge base could grow large -- need retention policies and pruning
- Injecting past knowledge into prompts adds context tokens -- must respect budget limits
- Knowledge relevance scoring may be inaccurate for novel tasks -- don't let stale knowledge mislead

## [ ] phase-48: Cost Optimization and Intelligent Model Routing (PLANNED)

**Goal:** Analyze token spending patterns and automatically suggest or apply cost optimizations across the orchestrator

Phase 32 tracks costs but does not optimize them. The research describes the OpenAI team spending $2-3K/day with 1B+ output tokens, treating code as disposable. At this scale, cost optimization becomes a first-class concern. This phase goes beyond tracking to actively identifying wasteful patterns: retries that consume more tokens than the original attempt, AI nodes using expensive models for trivial tasks, loop nodes hitting max iterations on unsolvable problems, and context budgets that are too large for simple issues. The optimizer suggests cheaper model alternatives, flags wasteful pipelines, and can auto-apply cost-saving parameter changes. This is the "attention is scarce" principle from Harness Engineering applied to token economics.

### Deliverables

- [ ] **Cost pattern analyzer** -- Module that identifies wasteful token spending patterns from execution history
  - [ ] `p48.d1.t1` Create cost_optimizer.py analyzer module (depends: p32.d1.t1)
    > Python module that: (1) reads execution logs and cost_tracker data, (2) computes per-pipeline, per-role, per-node-type average costs, (3) identifies waste patterns: retry cost exceeding original cost (loop amplification), AI nodes using expensive models for tasks that completed in <3 turns, context budgets >50% unused (over-budgeted), (4) estimates savings if cheaper models were used for specific node types, (5) outputs structured report with: current spend, waste percentage, top savings opportunities ranked by impact. Support --period flag and --threshold to filter small savings.
    _Files: ~/zion/projects/agent-orchestration/cost_optimizer.py_
  - [ ] Can identify top 5 most expensive pipeline patterns (by average token cost per run)
    _Validation: python3 cost_optimizer.py --analyze --last 50_
  - [ ] Detects specific waste patterns: excessive retries, oversized context, wrong model tier
    _Validation: run analysis on synthetic history with known waste patterns_
- [ ] **Model tier recommendation engine** -- Suggest cheaper model alternatives for specific task types based on historical success rates
  - [ ] `p48.d2.t1` Add model tier recommendations to cost_optimizer.py (depends: p48.d1.t1)
    > Add --recommend-models mode: (1) group AI node executions by task type (based on node name, role, pipeline context), (2) for each task type, compute success rate per model used, (3) if a cheaper model has >=95% success rate for a task type, recommend downgrading, (4) if an expensive model is needed (success rate <80% on cheaper models), flag as "requires premium model", (5) output a model routing table: task_type -> recommended_model -> confidence -> estimated_savings. Store recommendations in ~/.orchestrator/model-routing.yaml for use by phase 40 (multi-model backend).
    _Files: ~/zion/projects/agent-orchestration/cost_optimizer.py_
  - [ ] Can recommend model tier per node type based on historical success/failure data
    _Validation: python3 cost_optimizer.py --recommend-models_
  - [ ] Recommendations include confidence scores based on historical data volume
    _Validation: check output includes confidence and sample size_
- [ ] **Cost-aware pipeline parameters** -- Auto-adjust pipeline parameters (loop max, context budget, retry count) to minimize cost while maintaining success rate
  - [ ] `p48.d3.t1` Add cost-aware parameter tuning to cost_optimizer.py (depends: p48.d1.t1, p20.d1.t1)
    > Add --tune-params mode: (1) analyze loop nodes: if most loops succeed in 1-2 iterations, recommend reducing max_iterations (saves retry cost), (2) analyze context budgets: if most AI nodes use <40% of budget, recommend reducing budget (saves input tokens), (3) analyze retry patterns: if retry success rate is <30%, recommend reducing retry count (saves wasted tokens), (4) output parameter recommendations with estimated savings and success rate impact. Support --apply flag to write changes to pipeline YAML files. Keep a tuning log with before/after comparisons.
    _Files: ~/zion/projects/agent-orchestration/cost_optimizer.py_
  - [ ] Can suggest parameter adjustments that reduce cost without significantly impacting success rate
    _Validation: python3 cost_optimizer.py --tune-params_
- [ ] **Cost optimization cron integration** -- Weekly cron that runs cost analysis and reports savings opportunities
  - [ ] `p48.d4.t1` Create cost optimization cron job (depends: p48.d1.t1)
    > Create a weekly Hermes cron that runs cost_optimizer.py --analyze --period week --recommend-models --tune-params and outputs a structured report. The report includes: total spend for the period, top waste patterns, model tier recommendations, parameter tuning suggestions, and estimated total savings if all recommendations are applied. Store reports in ~/.orchestrator/reports/cost/ for historical comparison. Optionally create GitHub Issues for high-impact savings opportunities (>$50/week estimated).
  - [ ] Cron job runs weekly and outputs a cost optimization report
    _Validation: cronjob list_

### Technical Notes

Cost optimization is the financial sustainability layer. The research shows that at scale ($2-3K/day), even 10% savings matter. The key insight: most waste comes from retries on unsolvable problems and over-provisioned context budgets, not from the base model cost. Recommendations should always include confidence intervals and sample sizes -- small datasets produce unreliable recommendations.

### Risks

- Aggressive cost optimization could reduce quality -- always measure success rate impact
- Model tier recommendations require sufficient historical data (50+ runs per task type)
- Parameter tuning could make some edge cases worse while improving the average case

## [ ] phase-49: Human Feedback Capture and Agent Behavior Tuning (PLANNED)

**Goal:** Capture human review decisions from PRs and issues, analyze patterns, and feed them back to improve agent behavior

The research describes humans moving "up-stack" from writing code to "designing invariants," "tuning scaffolds," and defining "taste." But there is no mechanism for capturing the human's review decisions and using them to improve agent behavior. When a human rejects a PR, leaves an inline comment, or reopens a closed issue, that feedback is currently lost. This phase creates a feedback loop: (1) capture human review actions (approve, reject, comment) on agent-generated PRs, (2) analyze feedback patterns to identify recurring rejection reasons, (3) feed patterns back into the orchestrator as new rules, prompts, or safety policies, (4) track improvement over time as rejection rate decreases. This is the "outer harness guide" concept made adaptive -- instead of static AI_GUIDE.md rules, the system learns from human corrections.

### Deliverables

- [ ] **Feedback capture module** -- Module that reads GitHub review comments and PR actions on agent-generated PRs and structures them as feedback signals
  - [ ] `p49.d1.t1` Create feedback_capture.py module (depends: p13.d1.t1)
    > Python module that: (1) reads PR review comments via gh CLI (gh pr view --comments, gh api repos/{owner}/{repo}/pulls/{number}/comments), (2) filters for PRs labeled "auto-generated" or created by the orchestrator, (3) categorizes each comment: approval ("looks good", "lgtm"), rejection ("this approach is wrong", "please revert"), suggestion ("use X instead of Y", "consider Z"), question ("why did you..."), (4) extracts the file and line each comment refers to, (5) stores feedback in ~/.orchestrator/feedback/{repo}/YYYY-MM-DD.jsonl with: pr_number, issue_number, comment_text, category, file, line, reviewer. Support --sync flag to fetch recent feedback from GitHub.
    _Files: ~/zion/projects/agent-orchestration/feedback_capture.py_
  - [ ] Can read PR review comments and categorize them (approval, rejection, suggestion, question)
    _Validation: python3 feedback_capture.py --pr 42_
  - [ ] Captures the relationship between feedback and the specific code changes that triggered it
    _Validation: check output links comments to files and lines_
- [ ] **Feedback pattern analyzer** -- Analyze accumulated human feedback to identify recurring rejection reasons and behavior patterns
  - [ ] `p49.d2.t1` Add feedback pattern analysis to feedback_capture.py (depends: p49.d1.t1)
    > Add --analyze mode: (1) read all feedback entries, (2) group by rejection category, (3) identify recurring patterns: same file/line getting rejected repeatedly, same role producing the same type of rejection, same pipeline step consistently triggering corrections, (4) compute rejection rate over time (improving or worsening), (5) output structured report: rejection_categories (sorted by frequency), recurring_issues (specific patterns that appear in >20% of rejections), improvement_suggestions (auto-generated rules or prompt additions that would prevent the rejections), trend (rejection rate trajectory). Store analysis results for trend tracking.
    _Files: ~/zion/projects/agent-orchestration/feedback_capture.py_
  - [ ] Can identify top rejection categories across all agent-generated PRs
    _Validation: python3 feedback_capture.py --analyze --last 30_
  - [ ] Maps rejection patterns to specific orchestrator components (role, pipeline, node type)
    _Validation: check output includes component attribution_
- [ ] **Adaptive prompt tuning from feedback** -- Automatically generate prompt additions and rule suggestions from human feedback patterns
  - [ ] `p49.d3.t1` Add adaptive prompt tuning to feedback_capture.py (depends: p49.d2.t1)
    > Add --suggest-rules mode: (1) take the top rejection patterns from analysis, (2) for each pattern, generate a specific rule or prompt addition that would prevent it, (3) categorize suggestions: ai_guide_rules (additions to AI_GUIDE.md), role_prompt_additions (additions to role system prompts), pipeline_gate_checks (new bash nodes for pipelines), safety_policy_updates (new approval rules), (4) output suggestions as YAML with: pattern, frequency, suggested_rule, target (which component to modify), confidence, (5) support --apply to write suggestions to the appropriate config files (with backup). Support --dry-run to preview. The key: feedback becomes fuel for orchestrator improvement.
    _Files: ~/zion/projects/agent-orchestration/feedback_capture.py_
  - [ ] Can generate suggested AI_GUIDE.md additions based on recurring rejection patterns
    _Validation: python3 feedback_capture.py --suggest-rules_
  - [ ] Suggestions are specific and actionable (not generic advice)
    _Validation: review generated suggestions for specificity_
- [ ] **Feedback-driven improvement dashboard** -- Track human feedback metrics and improvement trends in the status dashboard
  - [ ] `p49.d4.t1` Add feedback metrics to status.sh (depends: p49.d2.t1)
    > Add a "Human Feedback" section to status.sh: overall rejection rate (last 30 days), rejection rate trend (improving/stable/worsening), top 3 rejection categories, number of auto-generated suggestions pending review. Call feedback_capture.py to get the data. Color code: green for improving trends, yellow for stable, red for worsening. Include a count of feedback-driven rules that have been applied.
    _Files: ~/zion/projects/agent-orchestration/status.sh_
  - [ ] status.sh shows rejection rate trend and top feedback categories
    _Validation: run status.sh, check for feedback section_

### Technical Notes

The feedback loop is the bridge between "human defines taste" and "agents learn taste." Key design decisions: (1) only capture feedback on agent-generated PRs to avoid noise, (2) categorize feedback using simple keyword matching first, upgrade to LLM classification if needed, (3) never auto-apply suggestions without human review -- the system suggests, the human decides. The improvement cycle: human rejects PR -> system captures feedback -> pattern identified -> rule suggested -> human approves rule -> agent behavior improves -> fewer rejections.

### Risks

- Feedback categorization may be inaccurate -- need human validation of categories
- Small sample sizes (few agent PRs) make pattern analysis unreliable
- Auto-generated suggestions could conflict with existing rules -- need deduplication
- Reviewer comments may be subjective or wrong -- the system should not blindly follow all feedback

## [ ] phase-50: Orchestrator Chaos Engineering and Fault Injection Testing (PLANNED)

**Goal:** Test the orchestrator''s resilience under failure conditions by injecting faults and verifying recovery behavior

The research emphasizes the Elixir/BEAM runtime's fault tolerance: hot code reloading, supervisor trees, and "let it crash" philosophy. The Hermes orchestrator has been built with various failure handling mechanisms (health checks, auto-recovery, workspace archival, approval timeouts) but none of these have been tested under actual failure conditions. This phase creates a chaos engineering toolkit that deliberately injects faults (worker crash, API timeout, disk full, network failure, config corruption) and verifies that the orchestrator recovers gracefully. This is the "Dark Factory" reliability prerequisite: before running fully autonomous, verify the system handles failures without human intervention. Modeled on chaos engineering practices (Netflix Chaos Monkey, Gremlin) but adapted for agent orchestration.

### Deliverables

- [ ] **Fault injection framework** -- Python module that can inject various fault types into orchestrator components during testing
  - [ ] `p50.d1.t1` Create chaos.py fault injection module
    > Python module that: (1) defines fault types: worker_crash (kill delegate_task process), api_timeout (delay gh CLI responses), disk_full (fill workspace to limit), config_corrupt (inject invalid YAML into config files), network_failure (block GitHub API endpoints), process_kill (kill orchestrator mid-loop), (2) each fault has: inject() and restore() methods, severity level, and expected recovery behavior, (3) support --inject FAULT --target TARGET and --restore for manual use, (4) provide a Python API for programmatic use in tests: with chaos.inject("api_timeout"): ... , (5) log all fault injections and recovery attempts. Include a --safe-mode flag that only injects faults in test workspaces.
    _Files: ~/zion/projects/agent-orchestration/chaos.py_
  - [ ] Can inject at least 5 fault types: worker crash, API timeout, disk full, config corruption, process kill
    _Validation: python3 chaos.py --inject worker_crash --target test_workspace_
  - [ ] Faults can be injected programmatically (for test integration) and via CLI (for manual testing)
    _Validation: run injection from CLI and from test code_
- [ ] **Recovery verification tests** -- Test suite that injects faults and verifies the orchestrator recovers correctly
  - [ ] `p50.d2.t1` Create test_chaos.py with fault injection tests (depends: p50.d1.t1)
    > Create pytest test suite: (1) test_worker_crash_recovery: inject worker crash, verify orchestrator marks workspace as failed and does not spawn replacement without human approval, (2) test_api_timeout_recovery: inject API timeout, verify poller retries and eventually skips the repo, (3) test_disk_full_recovery: fill workspace, verify workspace_manager detects and archives, (4) test_config_corrupt_recovery: corrupt YAML, verify config validation catches it and falls back to defaults, (5) test_process_kill_recovery: kill orchestrator, verify it resumes cleanly on restart (state recovery), (6) test_concurrent_faults: inject multiple faults simultaneously, verify no cascading failures. Use tmp_path fixtures for isolation.
    _Files: ~/zion/projects/agent-orchestration/test_chaos.py_
  - [ ] Test suite covers all major fault types with pass/fail recovery verification
    _Validation: python3 -m pytest test_chaos.py -v_
  - [ ] Each test verifies specific recovery behavior (not just "no crash")
    _Validation: read test assertions_
- [ ] **Resilience scoring** -- Score the orchestrator''s resilience based on chaos test results and track improvements over time
  - [ ] `p50.d3.t1` Add resilience scoring to chaos.py (depends: p50.d2.t1)
    > Add --score mode: (1) run all chaos tests, (2) compute per-fault-type recovery rate, (3) compute overall resilience score as weighted average (critical faults weighted higher), (4) compare against previous scores to show trend, (5) output as table: fault_type | injected | recovered | score | trend. Store scores in ~/.orchestrator/chaos/history.jsonl. Add resilience score to the health scorecard (phase 44). Target: resilience score >=80 before enabling dark factory mode (phase 35).
    _Files: ~/zion/projects/agent-orchestration/chaos.py_
  - [ ] Can compute a resilience score (0-100) based on chaos test pass rates
    _Validation: python3 chaos.py --score_
- [ ] **Chaos testing cron job** -- Scheduled job that runs chaos tests periodically and reports resilience status
  - [ ] `p50.d4.t1` Create chaos testing cron job (depends: p50.d3.t1)
    > Create a weekly Hermes cron that runs chaos.py --score in a test environment. The cron: (1) runs all chaos tests, (2) computes resilience score, (3) if score drops below 80%, create a GitHub Issue warning about resilience regression, (4) store results for trend tracking, (5) output a summary: overall score, per-fault-type scores, regressions detected, recommended actions. Keep the test environment isolated from production workspaces.
  - [ ] Cron job runs chaos tests weekly and reports resilience score
    _Validation: cronjob list_

### Technical Notes

Chaos engineering for orchestrators is different from traditional chaos engineering. The "system under test" is the orchestration logic (poll, spawn, recover), not the application code. Faults should target the orchestration layer: gh CLI failures, delegate_task crashes, filesystem issues. The key insight: an orchestrator that cannot handle its own failures will cascade those failures to all workers. Resilience score is the gate for dark factory mode.

### Risks

- Fault injection could leak into production if safe-mode is disabled -- always use test workspaces
- Some faults (network failure) are hard to inject realistically in a test environment
- Resilience scoring may not capture all failure modes -- supplement with manual testing
- Chaos tests may be flaky if they depend on timing -- use deterministic fault injection where possible

## [ ] phase-51: Orchestrator Federation and Cross-Instance Coordination (PLANNED)

**Goal:** Enable multiple Hermes orchestrator instances to coordinate work across repos, teams, or cloud regions

The research describes Gas Town managing 20-30 Claude Code instances simultaneously. Phase 30 covers inter-agent communication within a single orchestrator, but does not address the scenario where multiple Hermes orchestrator instances need to coordinate: one per organization, one per cloud region, or one per team. Without federation, multiple orchestrators could create conflicting PRs, duplicate work on the same issues, or waste resources on tasks already handled by another instance. This phase adds a federation layer: (1) a distributed lock service for issue assignment (preventing two orchestrators from working on the same issue), (2) a shared work status protocol for cross-instance visibility, (3) work stealing for load balancing between instances, and (4) a federation status view that shows all instances and their current workload. This is the "Kubernetes for Agents" pattern from Gas Town applied at the orchestrator level rather than the agent level.

### Deliverables

- [ ] **Distributed lock service** -- File-based or API-based distributed locking for issue assignment across orchestrator instances
  - [ ] `p51.d1.t1` Create federation_lock.py module
    > Python module implementing distributed locking: (1) uses GitHub issue labels as the lock mechanism (add "orch-working-{instance_id}" label to claim an issue, check for existing labels before claiming), (2) supports optional file-based locking for non-GitHub coordination (lock files in a shared filesystem or S3), (3) lock TTL with automatic expiry (default 4 hours), (4) lock acquisition returns: acquired (bool), lock_holder (instance_id if locked by another), lock_expiry (when current lock expires), (5) heartbeat to extend lock TTL while work is in progress, (6) CLI: python3 federation_lock.py acquire --issue 42 --instance my-instance, release, status. The GitHub-label approach requires no external infrastructure.
    _Files: ~/zion/projects/agent-orchestration/federation_lock.py_
  - [ ] Two orchestrator instances competing for the same issue results in only one acquiring the lock
    _Validation: run two instances simultaneously, verify single assignment_
  - [ ] Lock acquisition and release is atomic and handles stale locks (timeout-based expiry)
    _Validation: simulate stale lock, verify cleanup_
- [ ] **Federation status protocol** -- Shared status protocol that allows orchestrator instances to see each other''s workload
  - [ ] `p51.d2.t1` Create federation_status.py module (depends: p51.d1.t1)
    > Python module for cross-instance status sharing: (1) each instance writes its status to a shared location (GitHub repo issue/label, shared JSON file, or simple HTTP endpoint), (2) status includes: instance_id, active_issues, capacity_remaining, health_score, last_heartbeat, repos_monitored, (3) query_all() returns status of all known instances, (4) query_capacity(repo) returns total capacity across all instances monitoring a repo, (5) detect_stale() identifies instances that have not heartbeated recently (possible crash), (6) CLI: python3 federation_status.py publish, query, detect-stale. Default shared location: a designated GitHub issue with structured comments, or a JSON file in a shared filesystem.
    _Files: ~/zion/projects/agent-orchestration/federation_status.py_
  - [ ] Each orchestrator instance publishes its status (active issues, capacity, health) to a shared location
    _Validation: run two instances, check shared status_
  - [ ] Instances can query other instances'' status to avoid duplicate work
    _Validation: instance A checks instance B''s workload before claiming an issue_
- [ ] **Work stealing for load balancing** -- Enable under-loaded orchestrator instances to pick up work from over-loaded instances
  - [ ] `p51.d3.t1` Add work stealing to federation_status.py (depends: p51.d2.t1)
    > Add --steal-work mode: (1) query all instances for capacity, (2) if this instance has capacity >50% and another instance is at >80% capacity, (3) offer to take queued (not active) issues from the overloaded instance, (4) transfer is coordinated via the lock service: release lock on source instance, acquire on destination, (5) respect priority queue: only steal low-priority work, (6) log all transfers. Also add --rebalance mode for one-time manual rebalancing. Work stealing enables horizontal scaling: add more orchestrator instances and they automatically distribute load.
    _Files: ~/zion/projects/agent-orchestration/federation_status.py_
  - [ ] An idle instance can detect an overloaded instance and offer to take work
    _Validation: simulate load imbalance, verify work redistribution_
  - [ ] Work stealing respects priority and does not preempt in-progress work
    _Validation: check that active issues are not stolen_
- [ ] **Federation integration with orchestrator** -- Integrate federation locks and status into the orchestrator main loop
  - [ ] `p51.d4.t1` Integrate federation into orchestrator.py (depends: p51.d1.t1, p51.d2.t1, p4.d3.t1)
    > Modify orchestrator.py: (1) add federation section to orchestrator.yaml: enabled (bool), instance_id (string), shared_backend (github_labels|file|http), heartbeat_interval, lock_ttl, (2) in run_loop(): before spawning, acquire federation lock on the issue (skip if lock held by another instance), (3) after each loop iteration, publish instance status via federation_status.py, (4) on startup, register instance; on shutdown, deregister, (5) add --no-federation flag to disable for single-instance mode (default behavior unchanged), (6) add federation section to status.sh showing all instances and their workloads.
    _Files: ~/zion/projects/agent-orchestration/orchestrator.py, ~/zion/projects/agent-orchestration/orchestrator.yaml, ~/zion/projects/agent-orchestration/status.sh_
  - [ ] Orchestrator acquires federation lock before spawning workers and publishes status after each loop
    _Validation: run orchestrator with federation enabled, check lock labels and status_
  - [ ] Federation can be enabled/disabled via config without code changes
    _Validation: set federation.enabled: false, verify orchestrator runs without federation_

### Technical Notes

Federation is the scaling architecture. The GitHub-label-based locking approach is deliberately simple: no etcd, no Redis, no external dependencies. Labels on GitHub Issues serve as a natural distributed lock visible to all instances. The trade-off: label-based locking has higher latency (API calls) but zero infrastructure cost. For high-performance federation, the file-based or HTTP backend can be swapped in. Federation should be opt-in: single-instance mode (the default) should not be affected.

### Risks

- Distributed locking adds latency to every issue assignment
- Stale locks could prevent work from being picked up -- TTL expiry handles this but adds delay
- Federation status could become a bottleneck if too many instances publish frequently
- Work stealing could cause thrashing if instances constantly redistribute work
- No consensus protocol -- federation is eventually consistent, not strongly consistent

## [ ] phase-52: Agent Output Provenance Tracking (PLANNED)

**Goal:** Track which agent, role, session, and pipeline produced each line of code for full auditability and attribution

The research describes the Dark Factory experiment where "every line of the million-line codebase was authored by Codex agents." This level of provenance is essential for auditing, debugging, and understanding agent contributions over time. The current orchestrator records pipeline-level results in execution logs (phase 8) but has no code-level provenance. This phase adds git-based provenance: each agent commit is tagged with metadata (agent role, pipeline name, run ID, issue number), a provenance CLI can query which agent modified any given file or line range, and a summary report shows per-agent contribution stats. This enables the "who wrote what" question that is critical for the Dark Factory model and for understanding agent productivity patterns. The research emphasizes that "when agents failed, the team analyzed the environment" -- provenance data makes this analysis possible at the code level.

### Deliverables

- [ ] **Provenance metadata in git commits** -- Tag each agent commit with structured metadata (role, pipeline, run ID, issue)
  - [ ] `p52.d1.t1` Add provenance metadata to spawner.py commits
    > Modify spawner.py (or the PR creator from phase 13) to include a structured provenance footer in every agent commit: "Agent-Role: implementer", "Pipeline: standard-pipeline", "Run-ID: <uuid>", "Issue: #42", "Session: <timestamp>". Use git trailer format (--trailer) for clean separation from commit body. Also store the mapping in a local provenance DB (JSON file at ~/.orchestrator/provenance/) for fast queries.
    _Files: ~/zion/projects/agent-orchestration/spawner.py, ~/zion/projects/agent-orchestration/pr_automation.py_
  - [ ] Agent commits include structured metadata in commit message footer
    _Validation: inspect git log for agent commits, check metadata format_
  - [ ] Metadata is machine-parseable (structured footer format)
    _Validation: python3 provenance.py parse <commit-hash>_
  _~80 LOC_
- [ ] **Provenance query CLI** -- CLI tool to query which agent modified any file or line range
  - [ ] `p52.d2.t1` Create provenance.py CLI (depends: p52.d1.t1)
    > Create provenance.py with subcommands: (1) blame --file <path> [--lines N-M] -- shows which agent commits touched the given file/lines, parsed from git trailers, (2) summary [--role] [--since DATE] -- shows lines added/modified per agent role, (3) history --issue N -- shows all commits made for a specific issue, (4) export --format json -- exports full provenance data. Uses git log --format="" --grep to find agent commits, parses trailers with git interpret-trailers.
    _Files: ~/zion/projects/agent-orchestration/provenance.py_
  - [ ] Can query provenance for a specific file or line range
    _Validation: python3 provenance.py blame --file foo.py --lines 10-20_
  - [ ] Can show contribution summary per agent/role
    _Validation: python3 provenance.py summary --repo owner/repo_
  _~150 LOC_
- [ ] **Provenance in execution history** -- Link execution log entries to git commits for end-to-end traceability
  - [ ] `p52.d3.t1` Link execution logs to git commits (depends: p52.d1.t1)
    > Modify execution_log.py to include a "commits" field in the run record. After a pipeline completes, use git log to find commits in the workspace and record their hashes in the execution log. Update orch_history.py show command to display associated commits.
    _Files: ~/zion/projects/agent-orchestration/execution_log.py, ~/zion/projects/agent-orchestration/orch_history.py_
  - [ ] Execution log entries reference the git commits they produced
    _Validation: check execution log JSON for commit hash field_
  _~60 LOC_
- [ ] **Contribution analytics** -- Generate analytics on agent productivity patterns from provenance data
  - [ ] `p52.d4.t1` Add analytics subcommand to provenance.py (depends: p52.d2.t1)
    > Add analytics subcommand that aggregates provenance data: (1) lines per role (implementer vs reviewer vs tester), (2) avg lines per session, (3) pipeline success rate by role, (4) time-to-merge by role, (5) files most frequently modified by agents. Output as terminal table. This data feeds into the self-improvement loop (phase 19) and A/B testing analytics (phase 29) to identify which roles and pipelines are most productive.
    _Files: ~/zion/projects/agent-orchestration/provenance.py_
  - [ ] Can generate per-role, per-pipeline, and per-issue productivity reports
    _Validation: python3 provenance.py analytics --last 30d_
  _~100 LOC_

### Technical Notes

Git trailers are the cleanest way to embed agent metadata in commits -- they are structured, parseable, and don't interfere with commit body content. The provenance CLI uses git log filtering (not a custom database) for queries, keeping it simple and git-native. For the local provenance index (fast queries), use a simple JSON file updated after each pipeline run.

### Risks

- Provenance metadata could bloat commit messages -- keep it concise (trailer format)
- Git blame with agent metadata may be confusing for human developers -- provide a human-readable summary mode
- Provenance data may be sensitive (agent identity, pipeline performance) -- consider access controls

## [ ] phase-53: Dynamic Workforce Autoscaling (PLANNED)

**Goal:** Automatically scale the worker pool up and down based on queue depth and system resources

The research describes Symphony's max_concurrent config and Gas Town managing 20-30 Claude Code instances. The current orchestrator has a static max_concurrent limit (phase 4) and priority queuing (phase 41), but the pool size never changes based on demand. This is analogous to running Kubernetes with a fixed replica count. This phase adds autoscaling: monitor queue depth and system resources (CPU, memory, token budget), dynamically adjust max_concurrent up/down within configured bounds, and implement cooldown periods to prevent thrashing. The scaling decisions are logged for analysis and feed into the cost optimization (phase 48) and health monitoring (phase 14) systems. This enables the "elastic workforce" pattern where the orchestrator naturally handles burst workloads (many issues filed at once) without manual config changes, and conserves resources during quiet periods.

### Deliverables

- [ ] **Workforce autoscaler module** -- Python module that monitors queue depth and resources, adjusts max_concurrent accordingly
  - [ ] `p53.d1.t1` Create autoscaler.py module
    > Create autoscaler.py that: (1) takes current queue depth (from poller), active worker count, and system metrics (CPU%, memory%, token budget remaining from phase 32), (2) applies scaling rules: scale_up when queue_depth > (active_workers * scale_up_threshold) and resources available, scale_down when queue_depth == 0 and idle_time > cooldown_period, (3) respects bounds: min_workers (default 1), max_workers (default 10), scale_step (default 1), cooldown_seconds (default 300), (4) returns new_target_workers count, (5) logs every scaling decision with reason, (6) supports --dry-run mode for simulation. Scaling formula: target = min(max(queue_depth * aggressiveness, min_workers), max_workers) where aggressiveness is configurable (default 0.5 = conservative).
    _Files: ~/zion/projects/agent-orchestration/autoscaler.py_
  - [ ] Autoscaler increases workers when queue depth exceeds threshold
    _Validation: simulate queue backlog, verify worker count increases_
  - [ ] Autoscaler decreases workers when queue is empty and resources are idle
    _Validation: simulate empty queue, verify worker count decreases_
  - [ ] Scaling respects configured min/max bounds
    _Validation: set min=1 max=5, verify autoscaler stays within bounds_
  _~150 LOC_
- [ ] **Autoscaler integration with orchestrator** -- Hook autoscaler into the orchestrator main loop
  - [ ] `p53.d2.t1` Integrate autoscaler into orchestrator.py (depends: p53.d1.t1)
    > Modify orchestrator.py run_loop(): (1) add autoscaling section to orchestrator.yaml: enabled (bool), min_workers, max_workers, scale_up_threshold, scale_down_cooldown, aggressiveness, resource_checks (cpu, memory, token_budget), (2) at the start of each loop iteration, call autoscaler.calculate_target(queue_depth, active_workers, system_metrics), (3) use the returned target as the effective max_concurrent for this iteration (instead of the static config value), (4) log scaling events, (5) add --no-autoscale flag to disable (default: use static max_concurrent as before).
    _Files: ~/zion/projects/agent-orchestration/orchestrator.py, ~/zion/projects/agent-orchestration/orchestrator.yaml_
  - [ ] Orchestrator calls autoscaler each loop iteration and adjusts spawn behavior
    _Validation: run orchestrator with autoscaling enabled, check logs for scaling events_
  _~80 LOC_
- [ ] **Resource-aware scaling policies** -- Use system resources (CPU, memory, token budget) as additional scaling signals
  - [ ] `p53.d3.t1` Add resource-aware policies to autoscaler (depends: p53.d1.t1, p32.d1.t1)
    > Extend autoscaler.py with resource checks: (1) CPU check: read /proc/loadavg or use psutil, don't scale up if CPU > 80%, (2) Memory check: don't scale up if available memory < 2GB, (3) Token budget check: integrate with cost_tracker.py (phase 32), don't scale up if remaining budget < cost_per_worker_estimate * scale_duration, (4) Disk check: don't scale up if disk < 1GB free (workspace isolation needs disk), (5) Each check is optional and configurable in orchestrator.yaml.
    _Files: ~/zion/projects/agent-orchestration/autoscaler.py_
  - [ ] Scaling is blocked or reversed when system resources are constrained
    _Validation: simulate high CPU, verify no scale-up_
  - [ ] Token budget from phase 32 is used as a scaling constraint
    _Validation: set low token budget, verify scale-down_
  _~100 LOC_
- [ ] **Scaling history and analytics** -- Track scaling events and provide analytics on workforce utilization
  - [ ] `p53.d4.t1` Add scaling history to autoscaler (depends: p53.d2.t1)
    > Append scaling events to ~/.orchestrator/logs/scaling.jsonl (timestamp, action, old_workers, new_workers, queue_depth, reason, resource_snapshot). Add history subcommand that shows: scaling events timeline, avg/max/min workforce size over a period, queue depth vs workforce correlation, resource utilization during peak. Feed this data into the health scorecard (phase 44) for the "resource efficiency" signal.
    _Files: ~/zion/projects/agent-orchestration/autoscaler.py_
  - [ ] Scaling events are logged and queryable
    _Validation: python3 autoscaler.py history --last 7d_
  _~80 LOC_

### Technical Notes

Autoscaling should be conservative by default -- scale up slowly, scale down faster (to save resources). Cooldown periods prevent thrashing. The resource checks are optional guards; the primary signal is queue depth. The scaling formula is deliberately simple: no ML-based prediction, just reactive scaling based on current state. This is the "cattle" pattern applied to worker count.

### Risks

- Aggressive autoscaling could overwhelm the system -- default to conservative settings
- Scaling down too fast could kill workers mid-task -- only scale down by not replacing finished workers
- Token budget estimation is imprecise -- use conservative estimates and hard floor
- Autoscaling adds complexity to the orchestrator loop -- must be easily disableable

## [ ] phase-54: Version-Controlled Work Graph (Beads Pattern) (PLANNED)

**Goal:** Implement a dependency-aware work graph that tracks work items, their relationships, and state transitions with full history, inspired by Gas Town's Beads/Dolt state management

Gas Town's Beads is described as "a version-controlled SQL database built on Dolt" that "replaces messy markdown plans with a dependency-aware graph that tracks every molecule of work." It enables a pull-based execution model where agents pull work from their hooks as soon as it becomes available, rather than relying on a central scheduler. Phase 30 covers inter-agent communication (message passing between agents), but does not address the work graph itself -- the structured representation of work items, their dependencies, and state transitions. This phase implements a lightweight work graph: (1) work items are nodes in a directed graph with dependency edges, (2) state transitions (pending -> ready -> in_progress -> done -> blocked) are tracked with timestamps and provenance, (3) agents pull ready work items (no central push), (4) the graph is persisted as YAML/JSON (version-controllable alongside the codebase), and (5) the graph enables intelligent scheduling -- an item only becomes ready when all its dependencies are satisfied. This transforms the flat issue queue into a dependency-aware work graph that Gas Town calls the "pull-based execution model."

### Deliverables

- [ ] **Work graph data model and persistence** -- Define the work graph schema (nodes, edges, states) and persist it as version-controllable YAML/JSON
  - [ ] `p54.d1.t1` Create work_graph.py module
    > Create work_graph.py with: (1) WorkItem dataclass: id, title, description, state (pending/ready/in_progress/done/blocked/failed), dependencies (list of IDs), assignee, role, created_at, started_at, completed_at, provenance (issue_number, pipeline, run_id), metadata (arbitrary key-value), (2) WorkGraph class: add_item, add_dependency, get_ready_items (items whose deps are all done), transition_state, topological_order, get_critical_path, detect_cycles, (3) Persistence: save/load as YAML to work_graph.yaml (version-controllable), auto-save on every mutation, (4) CLI: add, remove, depends-on, show, ready, transition, graph (ASCII art of dependency graph), critical-path. States follow the Beads model: pending (deps not met), ready (deps met, not started), in_progress (agent working), done (completed), blocked (dep failed).
    _Files: ~/zion/projects/agent-orchestration/work_graph.py_
  - [ ] Work items can be created with dependencies on other items
    _Validation: python3 work_graph.py add --id W1 --depends-on W0_
  - [ ] State transitions are tracked with timestamps
    _Validation: python3 work_graph.py show W1, check state history_
  - [ ] Graph is persisted as YAML (version-controllable)
    _Validation: check work_graph.yaml exists and is valid_
  _~200 LOC_
- [ ] **Pull-based work assignment** -- Agents pull ready work items instead of being pushed by the orchestrator
  - [ ] `p54.d2.t1` Add pull-based assignment to work_graph.py (depends: p54.d1.t1)
    > Add to work_graph.py: (1) pull_ready(role=None) -> WorkItem: atomically claims the next ready item matching the optional role filter, transitions to in_progress, sets started_at and assignee, returns the item, (2) release(item_id, state="pending"): releases a claimed item back to ready or pending, (3) complete(item_id): transitions to done, checks if any blocked items become ready (dependency resolution), (4) fail(item_id, reason): transitions to failed, marks all downstream dependents as blocked, (5) File-based locking for atomic claim (use fcntl or lockfile). The pull model means no central scheduler decides what to work on -- agents ask "what can I do?" and the graph answers based on dependency state. This is the GUPP principle applied to work assignment.
    _Files: ~/zion/projects/agent-orchestration/work_graph.py_
  - [ ] Agent can query for and claim the next ready work item
    _Validation: python3 work_graph.py pull --role implementer_
  - [ ] Claiming an item transitions it to in_progress and blocks re-claim
    _Validation: two agents pulling simultaneously results in one getting the item_
  _~120 LOC_
- [ ] **Issue-to-graph synchronization** -- Sync GitHub Issues into the work graph, maintaining the issue tracker as control plane
  - [ ] `p54.d3.t1` Add issue sync to work_graph.py (depends: p54.d1.t1)
    > Add sync_from_github(repo, labels) to work_graph.py: (1) uses gh CLI to list issues with specified labels, (2) creates/updates WorkItems for each issue, (3) parses dependency references from issue body (e.g. "Depends on #42" or "Blocked by #43"), (4) adds dependency edges for referenced issues, (5) marks issues as done if they are closed on GitHub, (6) handles merge conflicts (local graph changes vs GitHub state -- GitHub wins for issue state, local graph wins for dependency edges). Also add a --watch mode that syncs periodically.
    _Files: ~/zion/projects/agent-orchestration/work_graph.py_
  - [ ] GitHub Issues are automatically imported as work graph items
    _Validation: python3 work_graph.py sync --repo owner/repo_
  - [ ] Issue dependencies (blocked-by) are preserved as graph edges
    _Validation: sync issues with dependencies, check graph edges_
  _~100 LOC_
- [ ] **Graph-aware orchestrator scheduling** -- Replace the flat issue queue with graph-aware scheduling in the orchestrator
  - [ ] `p54.d4.t1` Integrate work graph into orchestrator.py (depends: p54.d2.t1, p54.d3.t1)
    > Modify orchestrator.py: (1) add scheduling section to orchestrator.yaml: mode (flat|graph), graph_file (path to work_graph.yaml), auto_sync (bool), (2) in graph mode: instead of poller -> spawner, do: sync issues to graph -> pull ready items -> spawn workers for pulled items -> on completion, mark graph items done (which may unblock dependents), (3) the graph mode respects dependency ordering -- an issue blocked by an open dependency will not be scheduled even if it has the agent-ready label, (4) add status.sh section showing graph state: ready items, blocked items, critical path, dependency chains. Flat mode remains the default for backward compatibility.
    _Files: ~/zion/projects/agent-orchestration/orchestrator.py, ~/zion/projects/agent-orchestration/orchestrator.yaml, ~/zion/projects/agent-orchestration/status.sh_
  - [ ] Orchestrator uses work graph for scheduling instead of flat issue list
    _Validation: enable graph mode in orchestrator, check that dependency order is respected_
  - [ ] Graph can be enabled/disabled via config (backward compatible)
    _Validation: set scheduling.mode: flat, verify old behavior_
  _~100 LOC_

### Technical Notes

The work graph is deliberately file-based (YAML), not database-backed. This makes it version-controllable alongside the codebase -- a key insight from Beads/Dolt. The pull model is simpler than push: agents don't need to register for notifications, they just ask "what's ready?" The graph handles dependency resolution, blocking, and critical path calculation. For multi-instance coordination (phase 51), the pull model with file locking is naturally compatible with the federation approach.

### Risks

- Circular dependencies could deadlock the graph -- cycle detection is critical
- File-based locking may not work well across NFS/S3 -- document limitations
- Graph sync with GitHub could be slow for repos with many issues -- batch and cache
- The graph adds complexity compared to the flat queue -- must be optional and well-tested
- Dependency parsing from issue body is fragile -- provide structured syntax (e.g. Depends-On #42)

## [ ] phase-55: Automated agent.md Project Bootstrap Generator (PLANNED)

**Goal:** Automatically generate high-quality agent.md files for any project by analyzing codebase structure, conventions, and tooling

The research describes agent.md as "the context file that makes AI coding agents actually useful" and notes that "analysis of over 2,500 repositories indicates that the most successful implementations follow a structured pattern." Phase 12 covers self-documentation for the orchestrator itself, and phase 45 covers WORKFLOW.md parsing, but neither generates agent.md files for external projects. This phase creates an agent.md generator that scans a target project's codebase to produce a comprehensive agent.md: (1) detect tech stack (languages, frameworks, package managers) from config files, (2) extract build/test/lint commands from package.json, Makefile, pyproject.toml, etc., (3) identify code conventions from linting configs (eslint, prettier, ruff), (4) detect project structure patterns (monorepo layout, src/ convention), (5) generate three-tier boundaries (Always/Ask First/Never) based on common dangerous operations, (6) include code examples from the existing codebase. This is the "Guides" layer of the Outer Harness -- automating the creation of the feedforward controls that shape agent behavior. Without a good agent.md, agents make wrong assumptions about tech stack versions, build commands, and coding style.

### Deliverables

- [ ] **Codebase scanner module** -- Python module that scans a project directory to detect tech stack, tooling, and conventions
  - [ ] `p55.d1.t1` Create agentmd_gen.py scanner module
    > Create agentmd_gen.py with scan(project_dir) function: (1) detect languages from file extensions and config files (package.json -> Node.js, pyproject.toml -> Python, Cargo.toml -> Rust, go.mod -> Go, pom.xml -> Java), (2) extract versions from lock files and config, (3) detect package managers (npm/yarn/pnpm/pip/poetry/cargo/go), (4) extract scripts from package.json, Makefile targets, pyproject.toml [tool.xxx], (5) detect linting/formatting configs (.eslintrc, .prettierrc, ruff.toml, rustfmt.toml), (6) detect project structure (src/, lib/, cmd/, pkg/, monorepo packages/), (7) detect CI config (.github/workflows/, .gitlab-ci.yml) for test commands. Return a structured ProjectProfile dict.
    _Files: ~/zion/projects/agent-orchestration/agentmd_gen.py_
  - [ ] Can detect at least 5 tech stacks (Node.js, Python, Rust, Go, Java)
    _Validation: python3 agentmd_gen.py scan ~/some/project_
  - [ ] Extracts build, test, and lint commands from project config files
    _Validation: scan a project with package.json, verify npm commands extracted_
- [ ] **agent.md template renderer** -- Render a complete agent.md from the scanned project profile
  - [ ] `p55.d2.t1` Create agent.md template renderer (depends: p55.d1.t1)
    > Add generate(profile, output_path) to agentmd_gen.py: (1) render agent.md with sections: Tech Stack (languages + versions), Build Commands (exact commands with flags), Test Commands, Lint/Format Commands, Code Style (detected conventions), Project Structure (directory tree), Code Examples (extract 2-3 representative files), Three-Tier Boundaries (Always: lint/test, Ask First: DB/migration/API changes, Never: secrets/production data), Common Gotchas (detected from README or common patterns), (2) use simple f-string templates, (3) output to project root as AGENTS.md (GitHub standard) or agent.md (Symphony standard), (4) CLI: python3 agentmd_gen.py generate --project ~/path --output ./agent.md --format symphony|github
    _Files: ~/zion/projects/agent-orchestration/agentmd_gen.py_
  - [ ] Generated agent.md follows the structured pattern from research (tech stack, commands, examples, boundaries)
    _Validation: python3 agentmd_gen.py generate ~/some/project, read output_
  - [ ] Includes code examples from the actual codebase
    _Validation: check that generated agent.md contains real code snippets_
- [ ] **agent.md quality scoring** -- Score existing agent.md files against the research-backed best practices
  - [ ] `p55.d3.t1` Add scoring to agentmd_gen.py (depends: p55.d2.t1)
    > Add score(agentmd_path) function: (1) check for required sections (tech stack, commands, boundaries), (2) verify commands are accurate (try running dry-run or parsing), (3) check for code examples, (4) validate three-tier boundaries are present and reasonable, (5) score 0-100 with breakdown per section, (6) suggest improvements. This enables the orchestrator to evaluate agent.md quality as part of the application legibility score (phase 33).
    _Files: ~/zion/projects/agent-orchestration/agentmd_gen.py_
  - [ ] Can score an existing agent.md on completeness and quality
    _Validation: python3 agentmd_gen.py score ./agent.md_
- [ ] **Orchestrator integration** -- Auto-generate agent.md for repos managed by the orchestrator
  - [ ] `p55.d4.t1` Integrate agentmd_gen into orchestrator onboarding (depends: p55.d2.t1, p4.d3.t1)
    > Add --bootstrap-agentmd to orchestrator.py: (1) on first encounter with a repo, run agentmd_gen.py scan + generate, (2) save generated agent.md in the workspace, (3) inject it as additional context for agent sessions (like AI_GUIDE.md), (4) add a "refresh" command to re-scan and update agent.md when the project evolves, (5) log agent.md quality scores to execution history. This completes the Outer Harness "Guides" automation loop.
    _Files: ~/zion/projects/agent-orchestration/orchestrator.py, ~/zion/projects/agent-orchestration/spawner.py_
  - [ ] Orchestrator can generate/update agent.md for target repos as part of onboarding
    _Validation: run orchestrator with --bootstrap-agentmd flag_

### Technical Notes

The agent.md generator is the key to making the Outer Harness portable. Instead of manually crafting agent.md for every project (which is the current bottleneck), the generator creates a baseline that humans can refine. The scoring system enables continuous improvement: as the orchestrator runs, it can detect when the agent.md is stale (commands changed, new dependencies added) and flag it for update. This directly implements the research insight that "the most successful implementations follow a structured pattern" by automating that pattern.

### Risks

- Generated agent.md may miss project-specific conventions not detectable from file structure
- Code examples may include sensitive data -- filter before including
- Scoring may not capture qualitative aspects (clarity, usefulness)
- Generated files need human review before use in production

## [ ] phase-56: Symphony Spec Compliance Adapter (PLANNED)

**Goal:** Make Hermes a compatible implementation of the OpenAI Symphony specification, enabling drop-in replacement for teams already using Symphony configs

The research describes Symphony as "an open-source framework designed to solve the critical operational bottlenecks that arise when human engineers attempt to supervise autonomous agents at scale" with a SPEC.md that defines the contract between issue trackers, workspace managers, workflow loaders, and agent runners. Phase 45 covers WORKFLOW.md parsing, but does not aim for full Symphony spec compliance. This phase creates a Symphony compatibility layer: (1) a SPEC.md parser that reads Symphony-formatted configs and translates them to Hermes equivalents, (2) a Linear-to-GitHub Issues adapter (Symphony uses Linear as its reference tracker), (3) Codex App Server JSON-RPC compatibility for agent communication, (4) a compliance test suite that verifies Hermes behaves according to Symphony spec. This positions Hermes as a Symphony-compatible orchestrator, enabling teams to migrate from Symphony's Elixir implementation to Hermes without rewriting their configs. The research emphasizes that Symphony is "the first major step" in orchestration standards -- compatibility with the spec is strategically valuable.

### Deliverables

- [ ] **Symphony SPEC.md parser** -- Parse Symphony-formatted configuration files and translate to Hermes equivalents
  - [ ] `p56.d1.t1` Create symphony_compat.py parser
    > Create symphony_compat.py: (1) parse Symphony SPEC.md format: tracker.kind (linear/github), polling.interval_ms, agent.max_turns, agent.max_concurrent, codex.approval_policy, workspace.base_path, (2) map to Hermes equivalents: tracker.kind -> repo config, polling.interval_ms -> cron schedule, agent.max_turns -> pipeline max_steps, agent.max_concurrent -> max_concurrent, codex.approval_policy -> safety policy, (3) handle Symphony workspace path conventions (issue-ID-based isolation), (4) output a valid orchestrator.yaml, (5) validate that all required Symphony params have Hermes equivalents (report gaps). CLI: python3 symphony_compat.py parse SPEC.md, translate SPEC.md --output orchestrator.yaml, validate SPEC.md.
    _Files: ~/zion/projects/agent-orchestration/symphony_compat.py_
  - [ ] Can parse a Symphony SPEC.md and extract all config parameters
    _Validation: python3 symphony_compat.py parse SPEC.md_
  - [ ] Translates Symphony config to Hermes orchestrator.yaml format
    _Validation: python3 symphony_compat.py translate SPEC.md --output orchestrator.yaml_
- [ ] **Linear-to-GitHub Issues adapter** -- Translate Linear issue states to GitHub Issue states for Symphony compatibility
  - [ ] `p56.d2.t1` Add Linear adapter to symphony_compat.py (depends: p56.d1.t1)
    > Add linear_adapter module: (1) map Linear states: Todo -> agent-ready label, In Progress -> in-progress label, Done -> close issue, (2) use Linear API (via token) to poll issues, (3) create/update corresponding GitHub Issues with state sync, (4) bidirectional sync: changes in GitHub reflect back to Linear, (5) handle Linear-specific fields (cycle, project, priority) by mapping to GitHub labels/milestones. CLI: python3 symphony_compat.py linear-sync --token TOKEN --project PROJ_ID --repo owner/repo. The adapter enables teams using Linear (Symphony default) to use Hermes without switching issue trackers.
    _Files: ~/zion/projects/agent-orchestration/symphony_compat.py_
  - [ ] Can map Linear issue states (Todo, In Progress, Done) to GitHub equivalents
    _Validation: python3 symphony_compat.py linear-sync --project PROJ_ID_
- [ ] **Symphony compliance test suite** -- Test suite verifying Hermes behaves according to Symphony spec requirements
  - [ ] `p56.d3.t1` Create test_symphony_compat.py (depends: p56.d1.t1)
    > Create pytest suite: (1) test_spec_parsing: parse sample SPEC.md, verify all fields extracted, (2) test_config_translation: verify Symphony config translates to valid Hermes config, (3) test_workspace_isolation: verify Hermes workspace paths match Symphony conventions (deterministic issue-ID mapping), (4) test_approval_policies: verify untrusted/on-failure/never map to Hermes safety policies, (5) test_polling_equivalence: verify Hermes cron-based polling is equivalent to Symphony's continuous polling, (6) test_linear_sync: mock Linear API, verify state mapping. Use fixtures with sample SPEC.md files.
    _Files: ~/zion/projects/agent-orchestration/test_symphony_compat.py_
  - [ ] Test suite covers all Symphony spec requirements
    _Validation: python3 -m pytest test_symphony_compat.py -v_
  - [ ] Tests verify workspace isolation, polling, approval policies
    _Validation: read test assertions_
- [ ] **Symphony mode flag** -- Enable Symphony-compatible mode in the orchestrator via a single flag
  - [ ] `p56.d4.t1` Add Symphony mode to orchestrator (depends: p56.d1.t1, p56.d2.t1, p4.d3.t1)
    > Add --symphony flag to orchestrator.py: (1) detect SPEC.md in project root, (2) use symphony_compat.py to parse and translate config, (3) run in Symphony-compatible mode: Linear adapter for issues, Symphony workspace conventions, Symphony approval policies, (4) log Symphony spec compliance status, (5) add symphony section to status.sh showing spec version and compliance status. This makes Hermes a drop-in Symphony implementation.
    _Files: ~/zion/projects/agent-orchestration/orchestrator.py, ~/zion/projects/agent-orchestration/status.sh_
  - [ ] Orchestrator runs in Symphony-compatible mode with --symphony flag
    _Validation: python3 orchestrator.py --symphony --config SPEC.md_

### Technical Notes

Symphony compatibility is a strategic differentiator. As Symphony becomes the de facto standard for agent orchestration, being a compatible implementation means teams can adopt Hermes without rewriting their configs. The Linear adapter is the most complex part -- Linear's API requires a separate token and has different concepts (cycles, projects) than GitHub Issues. The adapter should be optional: teams using GitHub Issues directly don't need it.

### Risks

- Symphony spec may change as it matures -- parser needs version tolerance
- Linear API requires separate authentication and may have rate limits
- Symphony has features with no Hermes equivalent -- document gaps clearly
- Compliance testing may be fragile if Symphony spec is ambiguous

## [ ] phase-57: Skill Registry and Reusable Role Templates (PLANNED)

**Goal:** Create a registry of reusable skills and role templates that can be shared across projects and teams

The Harness Engineering research describes "the skills, documentation, and automated review agents that together defined what 'good' code looked like" as the core value of the outer harness. Phase 6 creates role specialization but roles are project-local (YAML files in roles/ directory). Phase 34 covers agent-generated tooling but doesn't address sharing. This phase creates a skill registry: (1) a standardized format for packaging skills (prompt templates + tools + quality gates), (2) a local registry (directory-based, no server required) for storing and versioning skills, (3) publish/subscribe workflow for sharing skills between projects, (4) skill composition (combining multiple skills into a role), (5) a CLI for managing skills (list, install, create, publish). This enables the "Dark Factory" pattern at scale: instead of each project building its own harness from scratch, teams share proven skills. The research notes that the OpenAI team's harness was their "competitive advantage" -- a skill registry makes that advantage shareable.

### Deliverables

- [ ] **Skill packaging format** -- Define a standardized format for packaging reusable skills
  - [ ] `p57.d1.t1` Define skill package format and create skill_registry.py
    > Create skill_registry.py: (1) skill package format: skill.yaml (name, version, description, author, tags, dependencies, applicable_labels, role_requirements), prompt.md (prompt template with {{variables}}), tools/ (optional tool scripts), gates/ (optional quality gate scripts), examples/ (usage examples), (2) create command: scaffolds a new skill package directory, (3) validate command: checks skill format completeness, (4) each skill is a directory under ~/.orchestrator/skills/ or a project-local skills/ directory. Design inspired by VS Code extensions and npm packages but simpler (no registry server, just git-friendly directories).
    _Files: ~/zion/projects/agent-orchestration/skill_registry.py_
  - [ ] Can create a skill package with prompt template, tools, and quality gates
    _Validation: python3 skill_registry.py create --name my-skill --template ./template.md_
  - [ ] Skill package format is self-describing (metadata, version, dependencies)
    _Validation: read skill.yaml, verify all fields present_
- [ ] **Local skill registry** -- Directory-based registry for storing and managing installed skills
  - [ ] `p57.d2.t1` Add registry management to skill_registry.py (depends: p57.d1.t1)
    > Add registry operations: (1) list [--installed|--available|--tag TAG] -- show skills in registry, (2) install SKILL [--global|--project] -- copy skill to local registry, (3) uninstall SKILL -- remove from local registry, (4) search QUERY -- search by name/description/tags, (5) info SKILL -- show detailed skill metadata, (6) update SKILL -- pull latest version from source. Registry locations: global: ~/.orchestrator/skills/, project: ./skills/. Project-local skills override global ones (same pattern as .gitignore vs global gitignore).
    _Files: ~/zion/projects/agent-orchestration/skill_registry.py_
  - [ ] Can list, search, and install skills from the registry
    _Validation: python3 skill_registry.py list, install, search_
  - [ ] Skills can be installed globally or per-project
    _Validation: install skill globally, verify available in all projects_
- [ ] **Skill composition engine** -- Combine multiple skills into a composite role for complex tasks
  - [ ] `p57.d3.t1` Add skill composition to skill_registry.py (depends: p57.d1.t1)
    > Add compose command: (1) takes a list of skills and merges their prompts (in order, with section headers), (2) combines tool scripts (with conflict detection), (3) merges quality gates (union of all gates), (4) outputs a composite role YAML compatible with roles.py from phase 6, (5) handles variable conflicts (prompt variables with same name must have compatible types), (6) supports skill layers (base skill + overrides). Example: "full-stack" = python-skill + testing-skill + review-skill. This enables building complex roles from simple, reusable components.
    _Files: ~/zion/projects/agent-orchestration/skill_registry.py_
  - [ ] Can compose multiple skills into a single role
    _Validation: python3 skill_registry.py compose --role full-stack --skills python,testing,review_
- [ ] **Skill sharing via git** -- Enable sharing skills between projects and teams via git repositories
  - [ ] `p57.d4.t1` Add git-based sharing to skill_registry.py (depends: p57.d2.t1)
    > Add git operations: (1) publish SKILL --repo GIT_URL -- push skill directory to a remote repo, (2) install SKILL --from GIT_URL -- clone/install skill from a git repo, (3) fork SKILL -- create a project-local copy for customization, (4) diff SKILL -- compare local customization against upstream, (5) update -- pull latest upstream changes. No registry server needed -- git repos are the distribution mechanism. Support GitHub, GitLab, and local file paths as sources.
    _Files: ~/zion/projects/agent-orchestration/skill_registry.py_
  - [ ] Can publish a skill to a git repo and install it in another project
    _Validation: publish skill to git, install from git URL_

### Technical Notes

The skill registry is deliberately simple: no npm-like registry server, no authentication, no dependency resolution beyond a flat list. Git is the distribution mechanism. The composition engine is the key innovation: it allows building complex agent behaviors from simple, tested, reusable components. This is the "Lego bricks" approach to the outer harness. Skills should be versioned (semver in skill.yaml) to handle breaking changes.

### Risks

- Skill composition could create conflicting prompts -- need clear precedence rules
- No centralized registry means discovery is harder -- consider a skills-index repo
- Skill quality varies -- consider a skill review/rating system
- Composed roles may exceed context window limits -- need composition budgeting

## [ ] phase-58: Agent Session Replay and Forensic Analysis (PLANNED)

**Goal:** Enable full replay and forensic analysis of agent sessions for debugging, learning, and quality assurance

The Harness Engineering research emphasizes that "when agents failed, the team analyzed the environment to identify missing capabilities or structures." The current system records execution logs (phase 8) and provides trace formatting (phase 18), but neither supports full session replay. In the Dark Factory model where humans never review code, understanding WHY an agent made specific decisions is critical. This phase creates a session replay system: (1) record every agent action (tool calls, file reads/writes, shell commands) with full context, (2) a replay CLI that steps through a session action-by-action showing the agent's context at each point, (3) forensic analysis that identifies decision points, dead ends, and context degradation, (4) diff-based comparison between successful and failed sessions to identify patterns, (5) automatic generation of "failure reports" that summarize what went wrong and suggest harness improvements. This transforms debugging from "read the log" to "watch the movie" and directly supports the self-improvement loop (phase 19) with richer data.

### Deliverables

- [ ] **Session recording module** -- Record every agent action with full context for later replay
  - [ ] `p58.d1.t1` Create session_recorder.py module
    > Create session_recorder.py: (1) SessionRecorder class that wraps agent execution and records: timestamp, action_type (tool_call, file_read, file_write, shell_cmd, llm_request), action_params, action_result, context_snapshot (files read, tokens remaining, workspace state hash), (2) recordings stored as JSONL in ~/.orchestrator/recordings/{session_id}.jsonl, (3) compact mode: store file diffs instead of full file contents to save space, (4) support for parallel sessions (each worker gets its own recording), (5) max_recording_size config to prevent disk exhaustion, (6) recording metadata: session_id, issue_number, pipeline, role, start_time, end_time, outcome (success/failure).
    _Files: ~/zion/projects/agent-orchestration/session_recorder.py_
  - [ ] Agent sessions are recorded with tool calls, context, and results
    _Validation: run an agent session, check recording file exists_
  - [ ] Recordings include sufficient context to reconstruct the agent''s view at each step
    _Validation: replay recording, verify context matches original session_
- [ ] **Session replay CLI** -- Step through recorded sessions action-by-action with full context
  - [ ] `p58.d2.t1` Create session_replay.py CLI (depends: p58.d1.t1)
    > Create session_replay.py: (1) replay SESSION_ID -- interactive terminal replay showing each action with context, (2) step forward/backward through actions, (3) jump N -- jump to action number N, (4) filter --type TYPE -- show only specific action types, (5) context N -- show the full agent context at action N (files read, prompt state), (6) summary -- show session summary: total actions, action type breakdown, tokens used, files modified, duration, (7) export --format json/markdown -- export session for sharing or analysis. The replay is read-only: it reconstructs the agent's view without executing anything.
    _Files: ~/zion/projects/agent-orchestration/session_replay.py_
  - [ ] Can replay a session showing each action and its context
    _Validation: python3 session_replay.py replay SESSION_ID_
  - [ ] Supports forward/backward stepping, jumping to specific actions, and filtering by type
    _Validation: step through replay, jump to action 42, filter to shell_cmd only_
- [ ] **Forensic analysis engine** -- Analyze recorded sessions to identify failure patterns and decision quality
  - [ ] `p58.d3.t1` Add forensic analysis to session_replay.py (depends: p58.d2.t1)
    > Add analyze command: (1) detect dead ends: actions that produced no useful progress (e.g., test failures followed by identical retry), (2) detect context degradation: increasing context usage without corresponding progress, (3) detect ineffective patterns: repeated failed approaches, excessive file reads without writes, (4) score decision quality: ratio of productive vs unproductive actions, (5) identify "pivot points" where the agent changed strategy, (6) compare SESSION1 SESSION2: diff two sessions highlighting divergent decisions and their outcomes, (7) generate failure report: summary of what went wrong, suggested harness improvements (e.g., "add a linter check after file edits" or "increase max_turns for this task type").
    _Files: ~/zion/projects/agent-orchestration/session_replay.py_
  - [ ] Can identify dead ends, context degradation, and ineffective actions in a session
    _Validation: python3 session_replay.py analyze SESSION_ID_
  - [ ] Can compare successful and failed sessions to identify patterns
    _Validation: python3 session_replay.py compare SESSION1 SESSION2_
- [ ] **Replay-driven self-improvement** -- Feed forensic analysis results into the self-improvement loop
  - [ ] `p58.d4.t1` Integrate forensic analysis with self-improvement loop (depends: p58.d3.t1, p19.d1.t1)
    > Modify self_improve.py to: (1) on session failure, run forensic analysis automatically, (2) aggregate failure patterns across sessions (e.g., "30% of failures involve context overflow"), (3) generate specific improvement suggestions based on failure patterns, (4) feed suggestions into the golden principles registry (phase 46) and skill registry (phase 57), (5) add a "replay" command to orch_history.py that launches session replay for a specific execution. This closes the loop: failures -> recordings -> analysis -> improvements -> fewer failures.
    _Files: ~/zion/projects/agent-orchestration/self_improve.py, ~/zion/projects/agent-orchestration/orch_history.py_
  - [ ] Forensic analysis results are used to generate improvement suggestions
    _Validation: run analyze on failed sessions, check suggestions are generated_

### Technical Notes

Session replay is the "black box flight recorder" for agents. The key design decision: recordings should be compact (JSONL with diffs, not full file copies) to avoid disk issues. The forensic analysis is deliberately heuristic -- it identifies patterns, not root causes. The comparison feature is the most powerful: by diffing a successful session against a failed one, you can see exactly where the agent diverged and what caused the failure. This is the "analyze the environment" capability from the research made systematic.

### Risks

- Recordings could consume significant disk space -- compact mode and size limits are essential
- Session replay may expose sensitive data (secrets, credentials) -- redaction needed
- Forensic analysis heuristics may produce false positives -- treat as suggestions, not facts
- Full context snapshots may be too large for complex sessions -- use diff-based approach

## [ ] phase-59: PR Velocity Metrics and Orchestrator ROI Tracking (PLANNED)

**Goal:** Build a dedicated metrics layer that measures the orchestrator's business impact -- PR throughput, time-to-merge, cost-per-PR, and quality trends over time

The research opens with a striking claim: "teams adopting this scaffolding approach saw a 500% increase in landed pull requests within the first three weeks." Yet no existing phase measures this. Phase 44 (Health Scorecard) covers system health (uptime, resource usage), but not business-value metrics. The economic argument is central to the research: "code is free, but attention is scarce" and "the primary cost center shifts from implementation to verification and infrastructure." This phase builds the measurement infrastructure to validate these claims for the Hermes orchestrator: (1) track PR creation rate, merge rate, time-to-merge, and cycle time, (2) compute cost-per-PR using data from phase 32 (cost tracker), (3) measure quality trends (PR revert rate, post-merge bug rate), (4) generate weekly/monthly ROI reports comparing agent-assisted vs manual development, (5) surface actionable insights (e.g., "role X produces 40% faster merges than role Y"). This transforms the orchestrator from a technical tool into a business dashboard that justifies continued investment in harness engineering.

### Deliverables

- [ ] **PR velocity data collector** -- Collect and aggregate PR lifecycle metrics from GitHub
  - [ ] `p59.d1.t1` Create velocity_metrics.py data collector
    > Create velocity_metrics.py: (1) collect command using gh CLI to fetch PRs with timestamps (created_at, merged_at, closed_at, review_submitted_at), (2) track PR lifecycle stages: created -> first_review -> approved -> merged (or closed without merge), (3) compute per-PR metrics: time_to_first_review, time_to_merge, cycle_time, files_changed, lines_added, lines_removed, (4) detect reverts: PRs whose description or commits reference a previous PR number, (5) store metrics as JSONL in ~/.orchestrator/metrics/velocity/{repo}.jsonl, (6) support incremental collection (only fetch new PRs since last collection), (7) tag PRs with metadata: agent_role (from phase 6), pipeline (from phase 5), issue_labels.
    _Files: ~/zion/projects/agent-orchestration/velocity_metrics.py_
  - [ ] PR creation, review, merge, and revert events are tracked
    _Validation: python3 velocity_metrics.py collect --repo OWNER/REPO --days 30_
  - [ ] Data is stored in a queryable format for trend analysis
    _Validation: query historical data across date ranges_
- [ ] **Cost-per-PR computation** -- Combine PR metrics with cost tracking data to compute economic efficiency
  - [ ] `p59.d2.t1` Add cost-per-PR computation to velocity_metrics.py (depends: p59.d1.t1, p32.d1.t1)
    > Add roi command: (1) correlate PR metrics with execution_log cost data from phase 8/32, (2) compute cost_per_pr = total_tokens_cost / merged_pr_count, (3) compute cost_per_line = total_tokens_cost / lines_merged, (4) compute cost_efficiency_trend: rolling 7-day and 30-day averages, (5) compare agent-assisted PRs vs manually-created PRs (detect via commit messages or labels), (6) estimate human-hours-saved: time_to_merge_agent vs historical manual average, (7) output as table with trend arrows. This is the "token billionaire strategy" made measurable.
    _Files: ~/zion/projects/agent-orchestration/velocity_metrics.py_
  - [ ] Cost-per-PR is computed and tracked over time
    _Validation: python3 velocity_metrics.py roi --repo OWNER/REPO --days 30_
- [ ] **Quality trend analysis** -- Track code quality metrics over time to detect improvements or regressions
  - [ ] `p59.d3.t1` Add quality trend analysis to velocity_metrics.py (depends: p59.d1.t1)
    > Add quality command: (1) compute revert_rate = reverted_prs / total_merged_prs per week, (2) compute post_merge_failure_rate using CI results from PR merge commits, (3) track review_sensor scores from phase 9 as quality proxy, (4) compute test_coverage_delta: change in test coverage per PR batch, (5) detect quality regressions: alert when revert_rate or failure_rate increases by >20% week-over-week, (6) correlate quality with agent role and pipeline to identify which configurations produce the best quality. Store results in ~/.orchestrator/metrics/quality/.
    _Files: ~/zion/projects/agent-orchestration/velocity_metrics.py_
  - [ ] PR revert rate and post-merge failure rate are tracked
    _Validation: python3 velocity_metrics.py quality --repo OWNER/REPO --days 30_
- [ ] **ROI report generator** -- Generate weekly/monthly reports summarizing orchestrator business impact
  - [ ] `p59.d4.t1` Add report generator to velocity_metrics.py (depends: p59.d2.t1, p59.d3.t1)
    > Add report command: (1) aggregate velocity, cost, and quality data for the report period, (2) compute key KPIs: PRs_landed, avg_time_to_merge, cost_per_pr, revert_rate, total_tokens_spent, (3) compute trend comparison: this_period vs previous_period (with % change), (4) identify highlights: "fastest merge", "most expensive PR", "role with highest quality", (5) generate actionable recommendations: "switch role X to role Y for task type Z based on quality data", (6) output as markdown report saved to ~/.orchestrator/metrics/reports/{date}.md, (7) support --format json for programmatic consumption. This is the report that justifies the orchestrator investment.
    _Files: ~/zion/projects/agent-orchestration/velocity_metrics.py_
  - [ ] Can generate a structured report with key metrics and trends
    _Validation: python3 velocity_metrics.py report --period weekly_

### Technical Notes

This is the "prove the ROI" phase. The research claims 500% PR increase -- this phase builds the infrastructure to measure that claim for Hermes. The key design decision: metrics are collected passively (no extra agent calls), only from gh CLI and existing execution logs. The report format should be shareable -- this is what gets shown to stakeholders to justify the orchestrator. Cost-per-PR is the single most important metric: it directly answers "is this worth it?"

### Risks

- gh CLI rate limits on large repos -- use incremental collection and caching
- Cost attribution is imprecise (execution logs may not map 1:1 to PRs) -- use best-effort correlation
- Historical manual-baseline data may not exist -- start measuring from day 1 and compare against itself over time
- Quality metrics (revert rate) are lagging indicators -- complement with leading indicators from review sensor

## [ ] phase-60: Human-Agent Workflow Optimization (PLANNED)

**Goal:** Build tooling that optimizes the human side of the orchestrator workflow -- streamlined ticket filing, PR review queues, triage automation, and the human's "command center" experience

The research describes a fundamental role transformation: "engineers shift their role from supervising execution to filing speculative tickets and reviewing completed work at the end of the pipeline." Phase 49 captures human feedback, but no phase builds the tooling to make this new workflow efficient. The human's experience is the bottleneck the research identifies: "the human-as-a-bottleneck problem, where a developer could only effectively manage a limited number of concurrent AI interactions." This phase builds: (1) smart ticket templates that auto-populate from codebase context (the "speculative ticket" pattern), (2) a PR review queue that prioritizes and summarizes agent-created PRs for efficient human review, (3) triage automation that classifies incoming issues and suggests agent-readiness, (4) a lightweight "command center" CLI that gives humans a single interface for all orchestrator interactions (file tickets, review PRs, check status, adjust config). This is the "from coder to architect" transformation made practical.

### Deliverables

- [ ] **Smart ticket filing with codebase context** -- Auto-populate ticket templates with relevant codebase context for efficient issue creation
  - [ ] `p60.d1.t1` Create human_workflow.py with smart ticket filing
    > Create human_workflow.py: (1) ticket command that creates GitHub Issues via gh CLI, (2) auto-detect relevant files from issue title using grep/search, (3) auto-detect affected tests from file paths, (4) suggest appropriate labels based on issue content (bug, feature, refactor, agent-ready), (5) suggest appropriate agent role based on issue type, (6) include a "complexity estimate" based on affected files and test coverage, (7) output the issue body in markdown for review before creation, (8) support --dry-run to preview without creating. The goal: a human should be able to file a well-structured, agent-ready ticket in under 60 seconds.
    _Files: ~/zion/projects/agent-orchestration/human_workflow.py_
  - [ ] Can create a ticket with auto-detected codebase context
    _Validation: python3 human_workflow.py ticket --title "Add logging" --repo OWNER/REPO_
- [ ] **PR review queue and summarizer** -- Prioritized queue of agent-created PRs with AI-generated summaries for efficient human review
  - [ ] `p60.d2.t1` Add PR review queue to human_workflow.py (depends: p60.d1.t1)
    > Add review-queue command: (1) fetch open PRs via gh CLI, (2) filter to agent-created PRs (by author or label), (3) generate a one-line summary of each PR (title + files changed + test status), (4) sort by priority: blocking PRs first (other PRs depend on them), then by age (oldest first), then by review_score (lowest score = needs most attention), (5) show review sensor scores from phase 9, (6) batch mode: show 5 PRs at a time for review marathon sessions, (7) approve/merge shortcuts via gh CLI, (8) track human review time to feed back into velocity metrics (phase 59).
    _Files: ~/zion/projects/agent-orchestration/human_workflow.py_
  - [ ] Can list pending agent-created PRs sorted by priority
    _Validation: python3 human_workflow.py review-queue --repo OWNER/REPO_
- [ ] **Issue triage automation** -- Classify incoming issues and suggest agent-readiness with confidence scores
  - [ ] `p60.d3.t1` Add issue triage to human_workflow.py (depends: p60.d1.t1)
    > Add triage command: (1) fetch open untriaged issues via gh CLI, (2) classify each issue: bug/feature/refactor/docs/test, using keyword heuristics from title and body, (3) estimate complexity: small (1-2 files), medium (3-5 files, existing tests), large (6+ files or new modules), (4) assess agent-readiness: ready (clear requirements, existing tests), needs-refinement (ambiguous scope), not-suitable (requires human judgment, security implications), (5) auto-label issues: agent-ready, needs-human, blocked, (6) estimate effort in agent turns based on complexity, (7) output as a triage table with recommendations. This automates the "filing speculative tickets" workflow from the research.
    _Files: ~/zion/projects/agent-orchestration/human_workflow.py_
  - [ ] Can classify issues and suggest agent-readiness
    _Validation: python3 human_workflow.py triage --repo OWNER/REPO_
- [ ] **Command center CLI** -- Single unified CLI for all human-orchestrator interactions
  - [ ] `p60.d4.t1` Add unified command center to human_workflow.py (depends: p60.d1.t1, p60.d2.t1, p60.d3.t1)
    > Add status command and unified entry point: (1) status -- show: open issues by status (triage/ready/in-progress/review), PRs in review queue, active workers, recent completions (last 24h), (2) config -- quick access to orchestrator config (max_concurrent, active repos, polling interval), (3) history -- recent human actions (tickets filed, PRs reviewed, config changes), (4) alias support: common workflows as shortcuts (e.g., "morning-review" = triage + review-queue + status), (5) --watch mode for status that auto-refreshes. This is the human's "command center" -- the single interface they need to interact with the orchestrator.
    _Files: ~/zion/projects/agent-orchestration/human_workflow.py_
  - [ ] Can perform all common human workflows from a single CLI
    _Validation: python3 human_workflow.py status && python3 human_workflow.py ticket --help && python3 human_workflow.py review-queue --help_

### Technical Notes

The key insight from the research: the human bottleneck is the real constraint, not the agents. The orchestrator can run 24/7, but humans can only review so many PRs per day. This phase maximizes the human's throughput: better ticket templates reduce filing time, better review queues reduce triage time, better summaries reduce per-PR review time. The triage classifier is deliberately heuristic (keyword-based), not LLM-based, to keep it fast and deterministic.

### Risks

- Auto-classification may mislabel issues -- always require human confirmation before labeling
- Review summaries may miss important context -- show full PR details on demand, don''t rely solely on summaries
- Command center CLI could become bloated -- keep it focused on the top 5 human workflows
- gh CLI rate limits on large repos -- cache results and use conditional requests

## [ ] phase-61: Agent Quality Regression Testing (PLANNED)

**Goal:** Create a benchmarking framework that measures agent output quality on canonical tasks over time, catching regressions as models or configurations change

The research emphasizes that quality comes from the harness: "the team focused on building the harness: the skills, documentation, and automated review agents that together defined what 'good' code looked like." Phase 7 tests the orchestrator's own code, but no phase systematically measures the quality of agent output. This is critical because: (1) model updates can silently degrade agent performance, (2) configuration changes (new roles, pipelines, policies) can have unintended quality impacts, (3) without baseline measurements, you can't prove the orchestrator is improving. This phase creates: (1) a benchmark suite of canonical tasks with known-good outputs, (2) automated benchmark runner that executes tasks through the full pipeline and scores results, (3) quality metrics: correctness (tests pass), style compliance (linters pass), review score (from phase 9 sensor), efficiency (tokens used, turns taken), (4) regression detection: alert when benchmark scores drop below thresholds, (5) trend tracking: visualize quality over time across model versions and config changes. This is the "agent CI" -- continuous integration for agent quality.

### Deliverables

- [ ] **Benchmark task suite** -- Curated set of canonical tasks with known-good reference implementations
  - [ ] `p61.d1.t1` Create benchmark task definitions
    > Create benchmarks/ directory with task definitions in YAML: (1) each task has: id, title, description, difficulty (small/medium/large), category (bug-fix, feature, refactor, test, docs), (2) setup: files to create, code state before task, (3) acceptance: tests that must pass, linters that must pass, files that must exist, (4) reference_solution: a known-good implementation for comparison, (5) scoring_weights: correctness, style, efficiency weights for composite score. Start with 10 tasks across all categories.
    _Files: ~/zion/projects/agent-orchestration/benchmarks/, ~/zion/projects/agent-orchestration/quality_bench.py_
  - [ ] At least 10 benchmark tasks covering different complexity levels
    _Validation: python3 quality_bench.py list -- show task catalog_
  - [ ] Each task has a reference solution and scoring criteria
    _Validation: inspect task definition YAML files_
- [ ] **Benchmark runner** -- Execute benchmark tasks through the full agent pipeline and score results
  - [ ] `p61.d2.t1` Create benchmark runner in quality_bench.py (depends: p61.d1.t1)
    > Create quality_bench.py run command: (1) load task definition from YAML, (2) create isolated workspace with task setup files, (3) execute task through the DAG pipeline from phase 5 (plan -> implement -> test -> review), (4) score results: correctness (all acceptance tests pass = 100%, partial pass = proportional), style (linters pass = bonus points), review_score (from phase 9 sensor if available), efficiency (fewer tokens/turns = bonus), (5) capture full execution for forensic analysis (phase 58), (6) output structured results as JSON, (7) support --save to store results in ~/.orchestrator/benchmarks/results/{task_id}/{timestamp}.json, (8) support --baseline to compare against a previous run.
    _Files: ~/zion/projects/agent-orchestration/quality_bench.py_
  - [ ] Can run a benchmark task end-to-end and produce a score
    _Validation: python3 quality_bench.py run --task bug-fix-001_
- [ ] **Regression detection** -- Detect quality regressions by comparing benchmark results over time
  - [ ] `p61.d3.t1` Add regression detection to quality_bench.py (depends: p61.d2.t1)
    > Add regress command: (1) load historical benchmark results, (2) compare latest run against baseline (previous run or N-run average), (3) regression criteria: score dropped by >10% (configurable per task), new test failures, linter failures, (4) output regression report: which tasks regressed, by how much, possible causes (config changes, model version), (5) support --threshold to set custom regression sensitivity, (6) exit code 1 on regression (CI-friendly), (7) suggest investigation actions: "review phase 58 forensic analysis for regressed task".
    _Files: ~/zion/projects/agent-orchestration/quality_bench.py_
  - [ ] Alerts when benchmark scores drop below configurable thresholds
    _Validation: deliberately degrade a benchmark, run regression check, verify alert_
- [ ] **Quality trend visualization** -- Track and visualize agent quality trends over time across configurations
  - [ ] `p61.d4.t1` Add trend tracking to quality_bench.py (depends: p61.d3.t1)
    > Add trends command: (1) aggregate benchmark results by day/week, (2) compute quality trend: overall score trajectory, per-category scores, per-role scores, (3) detect statistically significant changes (moving average crossover), (4) correlate quality with: model version, config changes (from git log), token budget (from phase 32), (5) output as markdown table with trend arrows, (6) identify "best configuration" per task type based on historical data, (7) feed insights into self-improvement loop (phase 19) and A/B testing (phase 29). This answers: "is our harness getting better or worse over time?"
    _Files: ~/zion/projects/agent-orchestration/quality_bench.py_
  - [ ] Can generate a trend report showing quality over time
    _Validation: python3 quality_bench.py trends --days 30_

### Technical Notes

Benchmarks must be deterministic: same task definition should produce comparable results across runs. The key challenge is task design: tasks must be self-contained (no external dependencies), have clear acceptance criteria, and cover a representative range of real-world work. Start with 10 tasks, grow to 30+. Benchmark results are the "source of truth" for agent quality -- they should be version-controlled alongside the orchestrator config.

### Risks

- Benchmark tasks may not represent real-world complexity -- include diverse task types and定期 update
- Agent performance varies between runs (non-deterministic) -- use median of 3 runs for stability
- Benchmark execution is expensive (uses real tokens) -- run weekly, not on every commit
- Task setup/teardown may leave residual state -- use isolated workspaces with cleanup

## [ ] phase-62: Prompt Engineering as Infrastructure (PLANNED)

**Goal:** Treat agent prompts as version-controlled, testable, and iterable code artifacts -- the "Guides" layer of the outer harness made into infrastructure

The research repeatedly emphasizes that the outer harness -- specifically "guides" like agent.md files and playbooks -- is where enterprise value is created: "the majority of enterprise-specific value is created, as it encodes the specific quality gates and compliance standards of the organization." Phase 3 upgraded AI_GUIDE.md templates and phase 36 adds dynamic policy loading, but prompts themselves are not treated as first-class code artifacts. Currently, prompts are embedded in role YAMLs, pipeline configs, and Python code with no versioning, testing, or iteration infrastructure. This phase builds: (1) a prompt library that stores prompt templates as versioned YAML files, (2) prompt diff and rollback tools, (3) a prompt testing framework (input/output pairs with expected behavior), (4) automated prompt quality scoring (conciseness, clarity, instruction-following), (5) integration with the DAG executor so prompts are loaded from the library rather than embedded in code. This makes the "guides" layer as rigorously maintained as the code itself.

### Deliverables

- [ ] **Prompt template library** -- Version-controlled prompt templates stored as structured YAML files
  - [ ] `p62.d1.t1` Create prompt library in prompts/ directory
    > Create prompts/ directory and prompt_lib.py: (1) each prompt template is a YAML file: id, name, description, version, category (planning, implementation, review, testing, triage), variables (with types and defaults), template (the actual prompt text with {{variable}} placeholders), metadata (created_by, last_modified, usage_count), (2) prompt_lib.py init -- scaffold a new prompt template, (3) prompt_lib.py list -- list all templates with metadata, (4) prompt_lib.py show ID -- display a template with variable descriptions, (5) prompt_lib.py render ID --var=value -- render a template with specific variable values, (6) prompt_lib.py history ID -- show git log of changes to this prompt. Prompts are plain YAML files tracked in git -- no database needed.
    _Files: ~/zion/projects/agent-orchestration/prompts/, ~/zion/projects/agent-orchestration/prompt_lib.py_
  - [ ] Prompt templates can be stored, listed, and loaded
    _Validation: python3 prompt_lib.py list && python3 prompt_lib.py show implement_
- [ ] **Prompt testing framework** -- Test prompt templates against input/output test cases to verify behavior
  - [ ] `p62.d2.t1` Add prompt testing to prompt_lib.py (depends: p62.d1.t1)
    > Add test command: (1) test cases defined alongside prompts in prompts/{id}_tests.yaml: input variables, expected_output_patterns (regex), forbidden_output_patterns (things the prompt should NOT produce), (2) test ID -- render prompt with test inputs, check output against expected/forbidden patterns, (3) test --all -- run all test suites, (4) test --watch -- re-run tests when prompt files change, (5) test --score -- rate prompt quality: instruction clarity (does output follow all instructions), conciseness (is output appropriately concise), consistency (do multiple runs with same input produce similar output), (6) output test results as TAP format for CI integration. This is "unit testing for prompts."
    _Files: ~/zion/projects/agent-orchestration/prompt_lib.py_
  - [ ] Can define test cases and run them against a prompt template
    _Validation: python3 prompt_lib.py test implement_
- [ ] **Prompt diff and rollback** -- Compare prompt versions and rollback to previous versions
  - [ ] `p62.d3.t1` Add diff and rollback to prompt_lib.py (depends: p62.d1.t1)
    > Add diff and rollback commands: (1) diff ID --compare VERSION -- show word-level diff between two versions of a prompt, (2) diff ID --last -- compare against the previous version, (3) diff ID --baseline -- compare against the original version, (4) highlight meaningful changes: added/removed instructions, changed variable defaults, modified constraints, (5) rollback ID --version VERSION -- restore a specific version from git history, (6) rollback ID --last -- undo the most recent change, (7) support --dry-run for rollback (preview without changing). Since prompts are YAML files in git, all versioning uses git under the hood.
    _Files: ~/zion/projects/agent-orchestration/prompt_lib.py_
  - [ ] Can diff two versions of a prompt and rollback
    _Validation: modify a prompt, run diff, run rollback, verify restored_
- [ ] **Prompt executor integration** -- Wire the prompt library into the DAG executor and role system
  - [ ] `p62.d4.t1` Integrate prompt library with executor and roles (depends: p62.d1.t1)
    > Modify executor.py and roles.py: (1) AI nodes in pipeline YAML can reference prompts by ID: prompt_ref: "implement" instead of embedding prompt text, (2) role YAMLs can reference prompt templates for their system prompt, (3) executor resolves prompt_ref by loading from prompt library, substituting variables from pipeline context, (4) fallback: if prompt_ref not found, use inline prompt (backward compatible), (5) log which prompt version was used for each execution (for audit trail in phase 52), (6) support prompt overrides per-repo (repo-local prompts/ directory takes precedence over global). This makes prompts centrally managed and version-controlled.
    _Files: ~/zion/projects/agent-orchestration/executor.py, ~/zion/projects/agent-orchestration/roles.py_
  - [ ] DAG executor loads prompts from the prompt library instead of embedded strings
    _Validation: configure a pipeline to use a prompt from the library, execute it_

### Technical Notes

The research insight: "The outer harness is characterized by guides -- feedforward controls that shape behavior before the agent acts." Currently these guides are scattered across YAML files, Python code, and markdown. Centralizing them in a version-controlled library makes them maintainable, testable, and auditable. The key design decision: prompts are YAML files in git, not a database. This keeps them simple, diffable, and branchable. The testing framework is deliberately lightweight: regex pattern matching, not LLM-based evaluation.

### Risks

- Prompt template abstraction may add complexity without clear benefit for small teams -- keep the CLI simple
- Test cases for prompts are inherently subjective -- use pattern matching, not exact matching
- Prompt versioning depends on git discipline -- enforce commit messages on prompt changes
- Centralized prompt library could conflict with per-repo customization -- support both global and local prompts

## [ ] phase-63: Orchestrator REST API and Platform Layer (PLANNED)

**Goal:** Expose the orchestrator's capabilities as a REST API for integration with external tools, IDEs, and dashboards

The research describes Symphony as "an open specification that allows any organization to transform their project board into a command center for the next generation of autonomous digital labor." Currently the Hermes orchestrator is Hermes-internal: all interaction is through CLI scripts and cron jobs. This limits integration with external tools (IDE plugins, CI/CD systems, team dashboards, other orchestration frameworks). This phase builds: (1) a lightweight REST API server using Python's built-in http.server (no Flask/FastAPI dependency), (2) endpoints for core operations: submit work, check status, list workers, get metrics, manage config, (3) webhook receiver for GitHub events (PR merged, issue labeled) that triggers orchestrator actions, (4) API key authentication and rate limiting, (5) OpenAPI spec for discoverability. This transforms the orchestrator from a Hermes-internal tool into a platform that any tool can integrate with.

### Deliverables

- [ ] **REST API server** -- Lightweight HTTP server exposing orchestrator capabilities
  - [ ] `p63.d1.t1` Create api_server.py REST API server
    > Create api_server.py using Python's http.server: (1) GET /health -- health check, (2) GET /api/v1/status -- orchestrator status (active workers, queue depth, recent completions), (3) GET /api/v1/workers -- list active workers with details, (4) GET /api/v1/workers/{id} -- specific worker status, (5) POST /api/v1/work -- submit work item (title, description, repo, labels), (6) GET /api/v1/work/{id} -- work item status, (7) GET /api/v1/metrics -- recent metrics (PR velocity, costs, quality scores from phases 59/32/9), (8) GET /api/v1/config -- current config (read-only), (9) all responses as JSON, (10) proper HTTP status codes, (11) CORS headers for browser-based dashboards, (12) structured error responses. No external dependencies -- pure Python stdlib.
    _Files: ~/zion/projects/agent-orchestration/api_server.py_
  - [ ] API server starts and responds to health check
    _Validation: python3 api_server.py start && curl localhost:8080/health_
- [ ] **Webhook receiver** -- Receive GitHub webhooks and trigger orchestrator actions
  - [ ] `p63.d2.t1` Add webhook receiver to api_server.py (depends: p63.d1.t1)
    > Add webhook endpoints: (1) POST /api/v1/webhooks/github -- receive GitHub webhook events, (2) validate webhook signature (X-Hub-Signature-256), (3) handle events: issues (labeled, opened, closed), pull_request (opened, closed, merged), (4) on issue labeled "agent-ready": add to orchestrator queue, (5) on PR merged: record completion, update metrics, trigger cleanup, (6) on PR closed without merge: record failure, trigger forensic analysis (phase 58), (7) support configurable event-to-action mapping in orchestrator.yaml, (8) webhook secret stored in config. This is the event-driven complement to polling (phase 4).
    _Files: ~/zion/projects/agent-orchestration/api_server.py_
  - [ ] Can receive a webhook and trigger an orchestrator action
    _Validation: send test webhook payload, verify action triggered_
- [ ] **Authentication and rate limiting** -- API key authentication and request rate limiting
  - [ ] `p63.d3.t1` Add auth and rate limiting to api_server.py (depends: p63.d1.t1)
    > Add security: (1) API key authentication: X-API-Key header, keys stored in ~/.orchestrator/api_keys.yaml, (2) key metadata: name, created, permissions (read/write/admin), rate_limit, (3) rate limiting: per-key requests per minute, configurable per key, (4) admin endpoints (POST/DELETE config, manage keys) require admin permission, (5) audit log: all API requests logged with timestamp, key, endpoint, status, (6) support API key rotation: generate new key, revoke old key with grace period. No OAuth -- API keys are sufficient for internal use.
    _Files: ~/zion/projects/agent-orchestration/api_server.py_
  - [ ] Unauthenticated requests are rejected
    _Validation: curl without API key returns 401_
- [ ] **OpenAPI spec and CLI client** -- Generate OpenAPI specification and a CLI client for the API
  - [ ] `p63.d4.t1` Create OpenAPI spec and api_client.py (depends: p63.d1.t1)
    > Create: (1) openapi.yaml -- OpenAPI 3.0 spec describing all endpoints, request/response schemas, authentication, (2) api_client.py -- CLI client that wraps the REST API: api_client.py status, api_client.py submit --title X --repo Y, api_client.py workers, api_client.py metrics, (3) api_client.py uses urllib (no requests dependency), (4) api_client.py supports --server and --api-key flags, (5) api_client.py --json for machine-readable output, (6) api_client.py watch -- follow status changes in real-time. The API client makes the orchestrator accessible from any environment, not just the Hermes host.
    _Files: ~/zion/projects/agent-orchestration/openapi.yaml, ~/zion/projects/agent-orchestration/api_client.py_
  - [ ] OpenAPI spec is generated and a CLI client can interact with the API
    _Validation: python3 api_client.py status --api-key KEY --server localhost:8080_

### Technical Notes

Deliberately lightweight: Python stdlib http.server, no Flask/FastAPI/requests. The API server is single-threaded (sufficient for internal use) but supports threading via ThreadingHTTPServer. The webhook receiver is the most impactful feature: it eliminates polling latency by reacting to events in real-time. The API client is the "remote control" for the orchestrator -- it enables scriptable access from any machine.

### Risks

- API server exposes internal state -- authentication is critical, never run without API keys
- Webhook receiver requires network exposure -- needs firewall rules and TLS in production
- Single-threaded server may not handle concurrent requests well -- use ThreadingHTTPServer
- No database -- all state is in-memory from existing modules -- restart loses transient state
- API versioning (v1) must be maintained for backward compatibility as the API evolves

## [ ] phase-64: Workspace Sandboxing and OS-Level Isolation (PLANNED)

**Goal:** Add OS-level sandboxing to agent workspaces -- filesystem restrictions, network policies, and resource limits to prevent agents from causing unintended side effects

The research describes Symphony's approach to workspace isolation: "strict safety invariants are enforced to ensure path normalization and sanitization, preventing agents from escaping their assigned boundaries." Phase 11 (Workspace Lifecycle) manages workspace creation/cleanup but provides only directory-level isolation. In the Dark Factory model (phase 35) where agents run fully autonomously with no human review, stronger isolation is essential. This phase builds: (1) filesystem sandboxing using Linux namespaces or chroot to restrict agent file access to their workspace, (2) network policy enforcement (allow/deny specific hosts/ports), (3) resource limits (CPU, memory, disk, wall-clock time) using cgroups or ulimit, (4) capability auditing -- log all system calls that agents attempt, flagging suspicious ones, (5) a "sandbox policy" YAML that defines per-role isolation levels (implementer gets full network, reviewer gets none). This makes the "high-trust environment" from the research actually trustworthy.

### Deliverables

- [ ] **Filesystem sandboxing module** -- Restrict agent file access to their workspace directory
  - [ ] `p64.d1.t1` Create sandbox.py filesystem isolation module
    > Create sandbox.py: (1) SandboxContext class that sets up filesystem isolation for a workspace, (2) support multiple isolation levels: none (current behavior), soft (warning on escape attempts), hard (block escape attempts), (3) soft mode: use a custom file opener that logs but allows access outside workspace, (4) hard mode: use chroot or mount namespace to restrict filesystem access to workspace directory, (5) allowlist for read-only access outside workspace (e.g., /usr/lib for Python packages, system PATH), (6) path sanitization: normalize all paths, reject symlinks that escape workspace, (7) integration with workspace_manager.py from phase 11 -- sandbox setup as part of workspace initialization, (8) detect and log escape attempts even in soft mode. Start with soft mode as default -- hard mode requires root.
    _Files: ~/zion/projects/agent-orchestration/sandbox.py_
  - [ ] Agent cannot access files outside their workspace
    _Validation: run agent in sandbox, attempt to read /etc/passwd, verify blocked_
- [ ] **Network policy enforcement** -- Control which network hosts and ports agents can access
  - [ ] `p64.d2.t1` Add network policy to sandbox.py (depends: p64.d1.t1)
    > Add network policy to SandboxContext: (1) network_policy in sandbox YAML: allowlist (hosts, ports, protocols), denylist, default_deny, (2) preset policies: open (no restrictions -- for implementer role), restricted (allow github.com, pypi.org, npmjs.org -- for dependency installation), locked (deny all -- for reviewer role), (3) enforcement via iptables rules (requires root) or LD_PRELOAD socket interceptor (user-space, no root needed), (4) DNS resolution filtering, (5) log all connection attempts (allowed and denied), (6) per-role default policies in roles/ directory. The LD_PRELOAD approach is preferred for zero-root deployment.
    _Files: ~/zion/projects/agent-orchestration/sandbox.py_
  - [ ] Agent network access is restricted per policy
    _Validation: configure deny-all policy, run agent, verify network calls blocked_
- [ ] **Resource limits and timeouts** -- Enforce CPU, memory, disk, and wall-clock time limits per workspace
  - [ ] `p64.d3.t1` Add resource limits to sandbox.py (depends: p64.d1.t1)
    > Add resource limits to SandboxContext: (1) resource_limits in sandbox YAML: max_cpu_percent, max_memory_mb, max_disk_mb, max_wall_time_seconds, max_processes, (2) enforcement via resource module (Python-level) and ulimit (system-level), (3) graceful shutdown: send SIGTERM, wait grace_period, then SIGKILL, (4) track resource usage during execution: peak memory, CPU time, disk usage, (5) report resource usage in execution logs (phase 8), (6) per-role default limits: implementer gets more resources, reviewer gets less, (7) detect resource exhaustion before it happens: warn at 80% of limit. Start with Python-level enforcement (resource module) which works without root.
    _Files: ~/zion/projects/agent-orchestration/sandbox.py_
  - [ ] Agent processes are killed when exceeding resource limits
    _Validation: set memory limit to 100MB, run agent that allocates 500MB, verify killed_
- [ ] **Capability auditing and policy configuration** -- Log all privileged operations and provide per-role sandbox policies
  - [ ] `p64.d4.t1` Add auditing and policy config to sandbox.py (depends: p64.d2.t1, p64.d3.t1)
    > Add auditing and configuration: (1) audit log: record all sandbox events (file access outside workspace, network connections, resource limit approaches, escape attempts), (2) audit log stored in ~/.orchestrator/audit/{session_id}.jsonl, (3) sandbox_policy.yaml: per-role policies defining isolation_level, network_policy, resource_limits, (4) integrate with executor.py: apply sandbox when creating worker process, (5) integrate with safety.py from phase 15: sandbox violations trigger safety policy actions, (6) report command: summarize sandbox events for a session (operations attempted, blocked, allowed), (7) strict mode: any sandbox violation immediately terminates the agent and flags the execution. This is the "strict safety invariants" from the research made enforceable.
    _Files: ~/zion/projects/agent-orchestration/sandbox.py, ~/zion/projects/agent-orchestration/sandbox_policy.yaml_
  - [ ] All filesystem/network/privilege operations are logged
    _Validation: run agent, check audit log for all system operations_

### Technical Notes

Start with soft-mode filesystem restrictions and Python-level resource limits (no root required). Hard-mode isolation (chroot, namespaces, iptables) is available but optional -- it requires root and may not work in all environments. The LD_PRELOAD network interceptor is the key innovation: it provides network filtering without root, without containers, and without modifying agent code. The sandbox policy is per-role: implementers need network access (pip install), reviewers don't. This is defense-in-depth: even if an agent goes rogue, it can't escape its sandbox.

### Risks

- Hard-mode isolation requires root -- may not work in all deployment environments
- LD_PRELOAD may not work with statically-linked binaries or some Python builds
- Overly restrictive sandboxing could break legitimate agent operations (package installs, git operations)
- Resource limits may kill agents mid-task, losing work -- implement checkpoint before limit
- Chroot escape is possible for root processes -- never run agents as root inside sandbox

## [ ] phase-65: Stop Hooks and Agent Loop Control (PLANNED)

**Goal:** Implement the "stop hooks" mechanism from the Ralph Wiggum pattern to intercept agent termination, check for completion tags, and re-feed prompts when work remains

The research describes stop hooks as the mechanism that makes Ralph Wiggum loops work: "stop hooks that intercept the agent's attempt to exit, check for completion tags, and re-feed the prompt if work remains." This phase implements that mechanism as a reusable module that wraps around delegate_task sessions, enabling autonomous multi-iteration agent loops with fresh context per iteration.
Without stop hooks, the Ralph Wiggum pattern is a concept without an implementation -- agents simply exit when done and there is no mechanism to detect incomplete work and restart with fresh context.

### Deliverables

- [ ] **Stop hook framework module** -- Create stop_hooks.py that intercepts agent session termination and decides whether to re-feed the prompt or allow exit
  - [ ] `p65.d1.t1` Create stop_hooks.py with core framework
    > Create stop_hooks.py with: (1) StopHook class with before_exit(session_state) -> continue|stop decision, (2) CompletionCriteria enum: TAG_FOUND, ALL_TESTS_PASS, EXIT_CODE, FILE_PATTERN, CUSTOM_SCRIPT, (3) SessionState dataclass: workspace_path, iteration_count, last_output, test_results, completion_tags_found, (4) LoopController that wraps a delegate_task session: run loop until hook returns stop or max_iterations reached, (5) each iteration starts fresh context (Ralph Wiggum smart zone), (6) persistent artifacts carry over (git history, workspace files), (7) iteration summary logged to execution_log, (8) CLI: python3 stop_hooks.py --workspace PATH --max-iterations 10 --criteria tag:IMPLEMENTATION_COMPLETE
    _Files: ~/zion/projects/agent-orchestration/stop_hooks.py_
  - [ ] Hook can intercept agent exit and inspect completion state
    _Validation: unit test with mock agent that exits with various states_
  - [ ] Hook supports configurable completion criteria (tags, file patterns, exit codes, test results)
    _Validation: test with each criterion type_
  - [ ] Hook enforces max_iterations to prevent infinite loops
    _Validation: test that agent stops after N iterations_
- [ ] **Completion tag detection** -- Detect completion markers in agent output and workspace files
  - [ ] `p65.d2.t1` Add completion detection to stop_hooks.py (depends: p65.d1.t1)
    > Add completion detection: (1) tag scanning in agent output: look for patterns like [DONE], [COMPLETE], IMPLEMENTATION_COMPLETE, <!-- READY -->, (2) file-based detection: check for completion marker files in workspace (.done, .complete), (3) TODO detection: count TODO/FIXME comments before and after, consider complete if all resolved, (4) test result detection: if tests were run, check if they pass, (5) git diff detection: if agent made no changes since last iteration, consider stuck, (6) configurable tag patterns via YAML config, (7) compound criteria: ALL must be met (AND) or ANY must be met (OR)
    _Files: ~/zion/projects/agent-orchestration/stop_hooks.py_
  - [ ] Detects standard completion tags in agent output text
    _Validation: test with output containing various tag formats_
  - [ ] Detects completion markers in workspace files (e.g., TODO comments resolved)
    _Validation: test with workspace containing marker files_
- [ ] **Loop context management** -- Manage context reset between iterations, carrying over only persistent artifacts
  - [ ] `p65.d3.t1` Add context management to stop_hooks.py (depends: p65.d1.t1)
    > Add context management: (1) iteration summary: extract key facts from previous iteration (what was done, what failed, what remains), (2) summary injected as context for next iteration (not full conversation), (3) workspace snapshot: save workspace state at end of each iteration for rollback, (4) progressive context: iteration N gets summary of iterations 1..N-1 (not full history), (5) smart zone enforcement: use context_budget.py from phase 20 to ensure summaries fit in budget, (6) failure context: if previous iteration failed, include error analysis in next iteration prompt, (7) test results carry over: include test output from previous iteration to help agent fix failures
    _Files: ~/zion/projects/agent-orchestration/stop_hooks.py_
  - [ ] Each iteration starts with fresh prompt context
    _Validation: test that iteration N+1 does not include iteration N conversation_
  - [ ] Persistent artifacts (git, files, test results) carry over
    _Validation: test that workspace state persists across iterations_
- [ ] **Integration with executor and tests** -- Integrate stop hooks with the DAG executor and add comprehensive tests
  - [ ] `p65.d4.t1` Integrate stop_hooks with executor and add tests (depends: p65.d2.t1, p65.d3.t1)
    > Integration and tests: (1) add LOOP_HOOK config option to Loop node in dag.py, (2) executor.py uses stop_hooks when loop node has hook config, (3) test_stop_hooks.py: test tag detection, file detection, test result detection, max_iterations enforcement, context carry-over, stuck detection, compound criteria, (4) test integration with executor: DAG with loop node using stop hooks, (5) test context budget integration: verify summaries fit in smart zone, (6) edge case tests: agent produces no output, agent crashes, workspace deleted mid-loop, completion tag in wrong format
    _Files: ~/zion/projects/agent-orchestration/stop_hooks.py, ~/zion/projects/agent-orchestration/test_stop_hooks.py, ~/zion/projects/agent-orchestration/dag.py, ~/zion/projects/agent-orchestration/executor.py_
  - [ ] Loop node in DAG executor can use stop hooks for termination
    _Validation: test DAG with loop node that uses stop hooks_
  - [ ] Tests cover all completion criteria types and edge cases
    _Validation: pytest coverage_

### Technical Notes

Stop hooks are the missing implementation piece for the Ralph Wiggum pattern. The research describes them as essential but no existing module implements them. The key insight is that stop hooks check for MACHINE-VERIFIABLE completion criteria, not agent self-assessment. This makes them deterministic and reliable. The fresh-context-per-iteration approach keeps agents in the "smart zone" (30-60% of context window) throughout long-running tasks.

### Risks

- Completion tag detection could have false positives (tag in comments, docs) -- use specific tag formats
- Stuck detection (no changes) could trigger too early on legitimate debugging sessions
- Context summaries could lose important details from previous iterations
- Infinite loop prevention relies on max_iterations -- if set too high, wastes tokens
- Stop hooks add complexity to the agent execution path -- must be optional and default-off

## [ ] phase-66: Scheduled Periodic Maintenance Automation (PLANNED)

**Goal:** Implement scheduled background maintenance tasks that run periodically (daily, weekly) to keep the codebase healthy, modeled on the research's "Garbage Collection Loops run weekly as background tasks"

The research describes a future where "Garbage Collection Loops run weekly as background tasks, scanning for deviations from 'golden principles' and opening targeted refactoring pull requests." Phase 10 implements GC scanning but not the scheduling layer. This phase adds a cron-compatible scheduler that automates periodic maintenance: GC scans, invariant checks, health reports, cost summaries, and self-improvement analysis.

### Deliverables

- [ ] **Maintenance scheduler module** -- Create maintenance.py that defines, schedules, and runs periodic maintenance tasks
  - [ ] `p66.d1.t1` Create maintenance.py with scheduler framework
    > Create maintenance.py with: (1) MaintenanceTask dataclass: name, schedule (daily/weekly/custom cron), last_run, last_result, enabled, (2) TaskRegistry: collection of registered maintenance tasks with config, (3) run_due_tasks(): check which tasks are due and run them, (4) run_task(name): run a specific task and record result, (5) state stored in ~/.orchestrator/maintenance/state.json, (6) results stored in ~/.orchestrator/maintenance/results/{task_name}/, (7) CLI: python3 maintenance.py --run-due, --run TASK, --schedule, --status, --history TASK, (8) --dry-run mode to show what would run without executing, (9) integration with orchestrator.py: add --maintenance flag to run due tasks before polling
    _Files: ~/zion/projects/agent-orchestration/maintenance.py_
  - [ ] Scheduler supports daily and weekly intervals
    _Validation: test with various interval configurations_
  - [ ] Each maintenance task has its own config, last-run timestamp, and result history
    _Validation: inspect state files after running_
- [ ] **Built-in maintenance tasks** -- Register the core maintenance tasks: GC scan, invariant check, health report, cost summary, self-improvement analysis
  - [ ] `p66.d2.t1` Register built-in maintenance tasks in maintenance.py (depends: p66.d1.t1)
    > Register these built-in tasks: (1) daily_gc_scan: run garbage_collector.py scan, schedule daily, output stale workspaces and convention violations, (2) daily_health_check: run health_monitor.py check, schedule daily, output stuck workspaces and alerts, (3) daily_cost_report: run cost_tracker.py report, schedule daily, output cost summary per repo, (4) weekly_invariant_scan: run invariant_checker.py on target repos, schedule weekly, output violations and trends, (5) weekly_self_improve: run self_improve.py analyze, schedule weekly, output improvement suggestions, (6) weekly_golden_principles_scan: scan repos for deviations from golden principles (phase 46), open issues for violations, (7) each task has configurable parameters (e.g., gc max_age, health thresholds), (8) task results include: count of findings, severity distribution, trend vs previous run, actionable items
    _Files: ~/zion/projects/agent-orchestration/maintenance.py_
  - [ ] At least 5 maintenance tasks are registered and runnable
    _Validation: python3 maintenance.py --schedule shows all tasks_
  - [ ] Each task produces a structured result with actionable findings
    _Validation: run each task and inspect output_
- [ ] **Maintenance task result tracking and trends** -- Track results over time to identify trends and recurring issues
  - [ ] `p66.d3.t1` Add result tracking and trend analysis to maintenance.py (depends: p66.d2.t1)
    > Add tracking: (1) result history: store each run result as JSON with timestamp, task_name, findings, summary, (2) trend calculation: compare current run to N previous runs (same day last week, same day last month), (3) trend indicators: increasing, stable, decreasing, new (first occurrence), (4) digest command: summarize all recent maintenance results in a single report, (5) alert thresholds: alert if findings increase by >50% week-over-week, (6) retention policy: keep last 90 days of results, archive older, (7) --digest CLI: python3 maintenance.py --digest --period week, output formatted report suitable for human review
    _Files: ~/zion/projects/agent-orchestration/maintenance.py_
  - [ ] Results are stored with timestamps and comparable across runs
    _Validation: run task twice, compare results_
  - [ ] Trend analysis shows whether findings are increasing or decreasing
    _Validation: run task 3+ times with different data, check trend output_
- [ ] **Cron integration and automated PR creation** -- Enable maintenance tasks to automatically file issues or PRs for findings
  - [ ] `p66.d4.t1` Add GitHub issue creation and cron integration to maintenance.py (depends: p66.d3.t1)
    > Add automation: (1) auto-file-issues: for each actionable finding, create a GitHub issue with structured template (task name, finding, severity, suggested fix), (2) dedup: check if issue already exists for same finding before creating, (3) auto-file-prs: for invariant violations with known fixes, create PR with remediation (using garbage_collector.py remediation), (4) approval gate: auto-PRs go through safety.py approval (phase 15), (5) cron integration: maintenance.py --run-due exits 0 on success (suitable for cron), logs to ~/.orchestrator/logs/maintenance/, (6) notification: if findings exceed threshold, print summary to stdout for cron delivery, (7) test_maintenance.py: test scheduler, task registration, result tracking, trend analysis, issue dedup, cron exit codes
    _Files: ~/zion/projects/agent-orchestration/maintenance.py, ~/zion/projects/agent-orchestration/test_maintenance.py_
  - [ ] Maintenance tasks can create GitHub issues for actionable findings
    _Validation: dry-run shows issue that would be created_
  - [ ] Task can be run via Hermes cron scheduler
    _Validation: cron job runs maintenance.py --run-due successfully_

### Technical Notes

The research specifically envisions GC loops as "weekly background tasks." This phase makes that vision operational by adding a scheduling layer on top of existing scanning/analysis modules. The key design decision is that maintenance tasks are composable -- each is a standalone module that the scheduler invokes, rather than a monolithic maintenance script. This allows tasks from different phases to be scheduled independently.

### Risks

- Auto-filing issues could spam the repo if maintenance tasks produce too many findings
- Auto-filing PRs without human review is risky -- require safety.py approval gate
- Scheduled tasks could conflict with active agent work (e.g., GC deleting workspace in use)
- Trend analysis needs enough history to be meaningful -- first few runs will have no trends
- Cron job failures could go unnoticed -- need alerting mechanism

## [ ] phase-67: Pre-PR Self-Verification Gate (PLANNED)

**Goal:** Create a pipeline gate that combines deterministic and inferential checks, requiring agents to verify their own work before PR submission

The research states agents can "drive application-level tools (Chrome DevTools, CLI scripts) to verify their own work before submitting a pull request." This phase creates a pre-PR verification gate that runs a battery of checks (tests, lints, invariant checks, review sensor) and only allows PR creation when all checks pass. This is the "self-verify" step that turns agent output from "probably correct" to "verified correct."

### Deliverables

- [ ] **Pre-PR verification gate module** -- Create verify_gate.py that runs verification checks and produces a pass/fail verdict
  - [ ] `p67.d1.t1` Create verify_gate.py with verification framework
    > Create verify_gate.py with: (1) VerifyCheck dataclass: name, type (deterministic/inferential), command_or_function, timeout, required (fatal if fails), (2) VerifyResult dataclass: check_name, passed, output, duration, severity, (3) VerifyGate class: register checks, run all, produce verdict, (4) built-in check types: BASH_CHECK (run shell command, check exit code), PYTHON_TEST (run pytest, parse results), INFERENTIAL (call review_sensor.py, check threshold), FILE_PATTERN (check for/against file patterns), INTEGRATION_TEST (run integration test command), (5) gate config in YAML: verify_gate.yaml with check definitions, thresholds, required/optional flags, (6) CLI: python3 verify_gate.py --workspace PATH --config verify_gate.yaml, (7) exit code 0 = all required checks pass, exit code 1 = failures, (8) JSON output mode for programmatic consumption
    _Files: ~/zion/projects/agent-orchestration/verify_gate.py, ~/zion/projects/agent-orchestration/verify_gate.yaml_
  - [ ] Gate runs configurable set of verification checks in sequence
    _Validation: test with mock checks that pass and fail_
  - [ ] Gate produces structured report with per-check results
    _Validation: inspect output report_
- [ ] **Integration with existing verification tools** -- Wire up the gate to use existing modules: invariant_checker, review_sensor, executor tests
  - [ ] `p67.d2.t1` Wire verify_gate to existing verification modules (depends: p67.d1.t1)
    > Wire integrations: (1) INFERENTIAL check type calls review_sensor.py evaluate(), (2) INVARIANT check type calls invariant_checker.py check_directory(), (3) add VERIFY_GATE node type to dag.py: runs verify_gate.py as a pipeline stage, (4) executor.py handles VERIFY_GATE node: runs gate, passes result to context, fails pipeline if required checks fail, (5) default gate config: include pytest (deterministic), invariant check (deterministic), review sensor (inferential), file pattern checks for common anti-patterns, (6) workspace-relative paths: all checks run from workspace directory
    _Files: ~/zion/projects/agent-orchestration/verify_gate.py, ~/zion/projects/agent-orchestration/dag.py, ~/zion/projects/agent-orchestration/executor.py_
  - [ ] Gate can invoke invariant_checker.py and review_sensor.py as checks
    _Validation: test gate with these modules_
  - [ ] Gate integrates with executor.py as a pipeline node
    _Validation: test DAG with VERIFY_GATE node_
- [ ] **Self-verification loop with auto-remediation** -- When verification fails, automatically attempt fixes and re-verify
  - [ ] `p67.d3.t1` Add auto-remediation loop to verify_gate.py (depends: p67.d2.t1)
    > Add remediation: (1) per-check fix_command: optional shell command to run when check fails, (2) fix cycle: run check -> if fail, run fix_command -> re-run check -> repeat up to max_fix_attempts (default 3), (3) fix context: include check failure output in the prompt/context for the fix command, (4) fix verification: after fix, run ALL checks again (not just the failed one) to catch regressions, (5) fix history: record each fix attempt (what failed, what fix ran, did it work), (6) fix summary: report which fixes were applied and which failures remain, (7) integrate with stop_hooks from phase 65: verification gate can be a stop hook criterion (loop until gate passes)
    _Files: ~/zion/projects/agent-orchestration/verify_gate.py_
  - [ ] Gate can run a fix cycle when checks fail
    _Validation: test with a check that fails, then passes after fix_
  - [ ] Fix cycle has max attempts to prevent infinite loops
    _Validation: test that fix cycle stops after max attempts_
- [ ] **Tests and PR automation integration** -- Integrate verification gate with PR automation and add tests
  - [ ] `p67.d4.t1` Integrate verify_gate with pr_automation and add tests (depends: p67.d3.t1)
    > Integration and tests: (1) pr_automation.py --create runs verify_gate.py before creating PR, (2) if gate fails, PR creation is aborted and failure report is attached to workspace, (3) --force flag skips gate (for emergency PRs), (4) gate results included in PR description as verification summary, (5) test_verify_gate.py: test pass/fail, fix cycle, timeout, integration with invariant_checker, integration with review_sensor, integration with pr_automation, edge cases (empty workspace, no config, all checks optional and all fail)
    _Files: ~/zion/projects/agent-orchestration/verify_gate.py, ~/zion/projects/agent-orchestration/test_verify_gate.py, ~/zion/projects/agent-orchestration/pr_automation.py_
  - [ ] PR automation runs verification gate before creating PR
    _Validation: test PR creation with gate that passes and fails_
  - [ ] Comprehensive test suite covers all gate behaviors
    _Validation: pytest coverage_

### Technical Notes

The research emphasizes that agents should "verify their own work" -- this is the mechanism. The gate is a pipeline-level construct (not agent-level) which makes it deterministic and reliable. The auto-remediation loop bridges the gap between "check failed" and "PR ready" by attempting fixes automatically, turning the gate from a pass/fail checkpoint into a self-correcting mechanism.

### Risks

- Verification gate could be too strict, blocking legitimate PRs -- make checks configurable
- Auto-remediation could introduce new bugs -- always re-run full check suite after fixes
- Inferential checks (LLM judge) are inconsistent -- don't make them required by default
- Fix commands could be destructive -- require safety.py approval for fix commands
- Gate adds latency to PR creation -- parallelize independent checks

## [ ] phase-68: Agent Session Identity and Continuity (PLANNED)

**Goal:** Implement persistent agent identity across restarts, following the research's "cattle sessions, pet identity" pattern

The research describes treating "individual agent sessions as ephemeral cattle, while treating the agent's identity and the project's state as persistent pets." Currently, each agent session is anonymous -- there is no way to correlate work across sessions, track an agent's history, or resume interrupted work. This phase adds a session identity layer that persists across restarts, enabling work continuity and historical tracking.

### Deliverables

- [ ] **Agent identity module** -- Create agent_identity.py that generates, tracks, and persists agent identities
  - [ ] `p68.d1.t1` Create agent_identity.py with identity framework
    > Create agent_identity.py with: (1) AgentIdentity dataclass: agent_id (UUID), role, created_at, last_seen, total_sessions, total_tasks_completed, total_tokens_used, specialties (learned strengths), (2) AgentRegistry: manages agent identities in ~/.orchestrator/identities/, (3) assign_identity(role): create or reuse identity for a role, (4) update_activity(agent_id): update last_seen and stats, (5) get_history(agent_id): list all tasks completed by this agent, (6) get_stats(agent_id): performance statistics (success rate, avg duration, preferred task types), (7) identity file format: YAML with full identity record, (8) CLI: python3 agent_identity.py --list, --show ID, --stats ID, --history ID, --retire ID
    _Files: ~/zion/projects/agent-orchestration/agent_identity.py_
  - [ ] Each agent session gets a unique but consistent identity
    _Validation: create session, restart, verify same identity_
  - [ ] Identity persists across orchestrator restarts
    _Validation: restart orchestrator, check identity state files_
- [ ] **Session continuity and work resumption** -- Enable agents to resume interrupted work from previous sessions
  - [ ] `p68.d2.t1` Add session continuity to agent_identity.py (depends: p68.d1.t1)
    > Add continuity: (1) SessionHandoff: when a session ends (voluntarily or crash), create a handoff record: what was being worked on, what was completed, what remains, any in-progress state, (2) handoff stored in ~/.orchestrator/handoffs/{agent_id}/{session_id}.yaml, (3) resume_session(agent_id): check for pending handoff, if found, inject handoff context into new session prompt, (4) handoff context includes: task description, work completed so far, files modified, test results, errors encountered, next steps identified by previous session, (5) merge with workspace_manager: when workspace transitions to failed/crashed, create automatic handoff, (6) handoff expiry: if handoff is older than 24 hours, mark as stale and start fresh (configurable), (7) handoff summary: use trace_formatter.py from phase 18 to create compact summary for context injection
    _Files: ~/zion/projects/agent-orchestration/agent_identity.py_
  - [ ] Agent can pick up where a previous session left off
    _Validation: interrupt session, start new one, verify work continues_
  - [ ] Work context from previous session is available to new session
    _Validation: check that new session has access to previous session's state_
- [ ] **Agent profiling and role affinity** -- Track agent performance across tasks to build role affinity profiles
  - [ ] `p68.d3.t1` Add agent profiling to agent_identity.py (depends: p68.d1.t1)
    > Add profiling: (1) TaskProfile: record of task type, outcome, duration, tokens used for each completed task, (2) RoleAffinity: calculated score for how well an agent identity performs in each role, based on historical success rate and efficiency, (3) update_profile(agent_id, task_result): update agent profile with latest task outcome, (4) get_affinity(agent_id, role): return affinity score (0.0-1.0) for agent in given role, (5) best_agent_for_role(role): return agent identity with highest affinity for a role, (6) integrate with spawner.py: when assigning role, prefer agent with highest affinity, (7) affinity decay: older performance data has less weight (exponential decay), (8) cold start: new agents get neutral affinity (0.5) for all roles
    _Files: ~/zion/projects/agent-orchestration/agent_identity.py, ~/zion/projects/agent-orchestration/spawner.py_
  - [ ] System tracks which task types each agent performs best on
    _Validation: run agent on various tasks, check affinity scores_
  - [ ] Role assignment considers agent affinity when available
    _Validation: check that spawner uses affinity data_
- [ ] **Tests and orchestrator integration** -- Integrate agent identity with the orchestrator and add tests
  - [ ] `p68.d4.t1` Integrate agent_identity with orchestrator and add tests (depends: p68.d2.t1, p68.d3.t1)
    > Integration and tests: (1) orchestrator.py: assign identity when spawning worker, update on completion, (2) execution_log.py: include agent_id in pipeline run records, (3) health_monitor.py: track identity activity in health checks (stale identities), (4) test_agent_identity.py: test identity creation, persistence, session handoff, affinity calculation, cold start, decay, integration with spawner, integration with orchestrator, edge cases (identity file corruption, handoff expiry, affinity ties)
    _Files: ~/zion/projects/agent-orchestration/agent_identity.py, ~/zion/projects/agent-orchestration/test_agent_identity.py, ~/zion/projects/agent-orchestration/orchestrator.py_
  - [ ] Orchestrator assigns and tracks agent identities for all workers
    _Validation: run orchestrator, check identity files created_
  - [ ] Comprehensive tests cover identity lifecycle
    _Validation: pytest coverage_

### Technical Notes

The "cattle vs pets" metaphor from the research is key: sessions (processes) are disposable cattle, but agent identity (the accumulated knowledge of what works) is a persistent pet. This phase makes that metaphor concrete by separating session lifecycle from identity lifecycle. Agent identity is NOT about the AI model itself -- it is about the orchestrator's accumulated knowledge about what works for different task types and roles.

### Risks

- Agent profiling could lead to unfair task distribution -- all tasks should be routable to any agent
- Handoff context could leak sensitive information between sessions
- Affinity scores could become stale if task types change -- implement decay
- Identity files add state that must be managed (backup, cleanup, migration)
- {'Cold start problem': 'new agents have no history, could be unfairly deprioritized'}

## [ ] phase-69: Orchestrator Integration Test Suite (PLANNED)

**Goal:** Create a comprehensive end-to-end test harness that validates the full orchestrator stack against mock or real GitHub issues

The research emphasizes that the harness engineering approach requires rigorous testing: "the team focused on building the harness: the skills, documentation, and automated review agents that together defined what 'good' code looked like." While individual modules have tests (phase 7), there is no integration test that exercises the full pipeline from issue polling through PR creation. This phase creates an integration test suite that validates the orchestrator end-to-end with deterministic mock scenarios.

### Deliverables

- [ ] **Integration test harness** -- Create test_integration_full.py that exercises the full orchestrator pipeline
  - [ ] `p69.d1.t1` Create test_integration_full.py with integration test harness
    > Create test_integration_full.py with: (1) MockGitHubAPI: simulates GitHub Issues API for testing without real repo, (2) MockAgent: simulates delegate_task agent behavior, (3) IntegrationTestSuite class: sets up test environment, runs pipeline, tears down, (4) test_full_pipeline_happy_path: create mock issue, poll it, spawn worker, execute DAG, create PR, verify PR, (5) test_pipeline_with_failure: agent fails, verify failure is handled, workspace marked failed, (6) test_pipeline_with_retry: agent fails, retry succeeds, verify recovery, (7) test_multi_repo_pipeline: two repos with issues, verify correct routing, (8) test_concurrent_workers: two issues in parallel, verify no conflicts, (9) test_safety_gate: issue with dangerous operation, verify safety.py blocks it, (10) test_budget_enforcement: issue that would exceed budget, verify blocked
    _Files: ~/zion/projects/agent-orchestration/test_integration_full.py_
  - [ ] Test suite covers the full pipeline: poll -> spawn -> execute -> verify -> PR
    _Validation: run test suite, verify all stages execute_
  - [ ] Tests are deterministic (no external dependencies required)
    _Validation: run tests in isolated environment, verify consistent results_
- [ ] **Scenario-based integration tests** -- Add tests for specific real-world scenarios from the research
  - [ ] `p69.d2.t1` Add scenario-based tests to test_integration_full.py (depends: p69.d1.t1)
    > Add scenario tests: (1) test_speculative_ticket_workflow: file speculative ticket, agent explores approach, creates PR with findings (research: "filing speculative tickets"), (2) test_ralph_wiggum_loop: complex task requiring multiple iterations, verify context resets between iterations, (3) test_garbage_collection_workflow: GC scan finds violations, auto-fix creates PR, verify remediation, (4) test_role_specialization: issues with different labels routed to different roles, verify correct role behavior, (5) test_invariant_violation_detection: agent introduces layer violation, invariant checker catches it, agent fixes it, (6) test_self_verification_gate: agent completes work, verification gate runs, auto-fix cycle if needed, PR created, (7) test_health_monitoring: stuck workspace detected, alert triggered, workspace recovered, (8) test_session_continuity: agent crashes mid-task, new session resumes from handoff
    _Files: ~/zion/projects/agent-orchestration/test_integration_full.py_
  - [ ] Tests cover key research scenarios: speculative ticket, dark factory, multi-agent swarm
    _Validation: review test names and descriptions_
  - [ ] Each scenario test has clear pass/fail criteria based on research outcomes
    _Validation: inspect test assertions_
- [ ] **Performance and load testing** -- Add performance benchmarks to validate orchestrator scales under load
  - [ ] `p69.d3.t1` Add performance benchmarks to test_integration_full.py (depends: p69.d2.t1)
    > Add benchmarks: (1) BenchmarkSuite class: measures time, memory, token usage for pipeline stages, (2) benchmark_single_issue_latency: measure end-to-end time from issue creation to PR, (3) benchmark_throughput: measure issues processed per minute with N concurrent workers (1, 2, 5, 10), (4) benchmark_polling_overhead: measure time for poll cycle with varying numbers of issues, (5) benchmark_verification_gate: measure time for full verification suite, (6) memory_profile: track memory usage during pipeline execution, detect leaks, (7) benchmark_results stored in ~/.orchestrator/benchmarks/ for trend comparison, (8) CI integration: benchmark can be run in CI with --ci flag that sets baseline thresholds and fails if regressions detected
    _Files: ~/zion/projects/agent-orchestration/test_integration_full.py_
  - [ ] Benchmark measures throughput (issues/minute) and latency (time to PR)
    _Validation: run benchmark, inspect results_
  - [ ] Load test validates behavior with 10+ concurrent workers
    _Validation: run load test, verify no deadlocks or resource exhaustion_
- [ ] **Test fixtures and documentation** -- Create reusable test fixtures and document the integration test approach
  - [ ] `p69.d4.t1` Create test fixtures and document integration testing (depends: p69.d3.t1)
    > Create fixtures and docs: (1) conftest.py: shared pytest fixtures (mock workspace, mock issue, mock config, temp project dir), (2) fixtures/mock_project/: minimal Python project for testing (has tests, lintable code, known structure), (3) fixtures/mock_pipelines/: example DAG YAML files for testing various pipeline patterns, (4) fixtures/mock_roles/: example role profiles for testing role routing, (5) README_TESTING.md: how to run unit tests, integration tests, benchmarks; how to add new test scenarios; how to run in CI mode; how to interpret benchmark results, (6) test matrix: document which modules are tested by which test files, identify coverage gaps, (7) add to self_doc.py inventory: integration test suite as a module
    _Files: ~/zion/projects/agent-orchestration/conftest.py, ~/zion/projects/agent-orchestration/README_TESTING.md_
  - [ ] Test fixtures are reusable across integration tests
    _Validation: fixtures imported and used by multiple tests_
  - [ ] Documentation explains how to run and extend integration tests
    _Validation: read docs, follow instructions, run tests_

### Technical Notes

The research emphasizes that the Dark Factory experiment achieved quality through the harness, not through human review. Integration testing is how we validate that the harness actually works end-to-end. Without integration tests, individual modules could all pass their unit tests while the overall system fails in subtle ways (e.g., context not properly passed between stages, state not properly cleaned up between runs). The mock-based approach ensures tests are deterministic and fast, while still exercising the real code paths.

### Risks

- Mock-based tests may not catch real-world issues (GitHub API quirks, file system permissions)
- Integration tests could be slow if they exercise the full pipeline -- keep scenarios focused
- Test fixtures could become outdated as the orchestrator evolves
- Load tests could be flaky in CI environments with limited resources
- Over-investment in testing could slow feature development -- keep test maintenance low

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
- External observability (phase 42) could expose sensitive data from logs -- need PII/secrets filtering before injecting into agent context
- Automated refactoring (phase 43) could make incorrect fixes that pass tests but change semantics -- always require human review for refactoring PRs
- Health scorecard (phase 44) KPIs may not capture what matters initially -- need iteration based on real usage patterns
- WORKFLOW.md format (phase 45) may evolve as Symphony matures -- parser needs version tolerance
- Per-project WORKFLOW.md files (phase 45) could conflict with orchestrator.yaml global settings -- need clear precedence rules
- Symphony-to-Hermes translation (phase 45) may lose information for Symphony features with no Hermes equivalent
- Semantic principle checks (phase 46) are expensive and inconsistent -- use sparingly, only for high-value principles
- Too many principles (phase 46) creates noise -- start with 10-15 and grow slowly
- Principle evolution (phase 46) could drift from original intent -- human review required for all new principles
- Knowledge extraction quality (phase 47) depends on session summary -- poorly summarized sessions add noise
- Knowledge base (phase 47) could grow large -- need retention policies and pruning
- Injecting past knowledge (phase 47) into prompts adds context tokens -- must respect budget limits
- Knowledge relevance scoring (phase 47) may be inaccurate for novel tasks -- don't let stale knowledge mislead
- Aggressive cost optimization (phase 48) could reduce quality -- always measure success rate impact
- Model tier recommendations (phase 48) require sufficient historical data (50+ runs per task type)
- Parameter tuning (phase 48) could make some edge cases worse while improving the average case
- Feedback categorization (phase 49) may be inaccurate -- need human validation of categories
- Auto-generated suggestions (phase 49) could conflict with existing rules -- need deduplication
- Reviewer comments may be subjective or wrong -- the system should not blindly follow all feedback
- Fault injection (phase 50) could leak into production if safe-mode is disabled -- always use test workspaces
- Resilience scoring (phase 50) may not capture all failure modes -- supplement with manual testing
- Chaos tests (phase 50) may be flaky if they depend on timing -- use deterministic fault injection where possible
- Distributed locking (phase 51) adds latency to every issue assignment
- Stale locks (phase 51) could prevent work from being picked up -- TTL expiry handles this but adds delay
- Federation status (phase 51) could become a bottleneck if too many instances publish frequently
- Work stealing (phase 51) could cause thrashing if instances constantly redistribute work
- No consensus protocol (phase 51) -- federation is eventually consistent, not strongly consistent
- agent.md generator (phase 55) may produce inaccurate tech stack detection for unusual project layouts
- Generated agent.md files (phase 55) need human review before production use
- Symphony spec compliance (phase 56) may break if Symphony spec changes -- needs version tolerance
- Linear API adapter (phase 56) requires separate auth token and has rate limits
- Skill composition (phase 57) could create conflicting prompts that confuse agents
- No centralized skill registry (phase 57) means discovery depends on documentation
- Session recordings (phase 58) could expose secrets in agent context -- redaction essential
- Forensic analysis (phase 58) heuristics may produce false positives -- treat as suggestions
- Velocity metrics (phase 59) depend on GitHub API availability and rate limits
- Cost-per-PR attribution (phase 59) is imprecise -- execution logs may not map 1:1 to PRs
- Human workflow auto-classification (phase 60) may mislabel issues -- require human confirmation
- Benchmark tasks (phase 61) may not represent real-world complexity -- include diverse task types
- Benchmark execution (phase 61) uses real tokens -- run weekly not per-commit to control costs
- Prompt library centralization (phase 62) could conflict with per-repo customization -- support overrides
- REST API (phase 63) exposes internal orchestrator state -- authentication is critical
- Webhook receiver (phase 63) requires network exposure -- needs firewall rules and TLS
- LD_PRELOAD sandboxing (phase 64) may not work with statically-linked binaries
- Overly restrictive sandboxing (phase 64) could break legitimate agent operations (pip, git)
- Stop hooks (phase 65) could false-positive on completion tags -- use specific tag formats
- Maintenance automation (phase 66) auto-filing issues could spam repos with findings
- Pre-PR verification gate (phase 67) could block legitimate PRs if checks too strict
- Agent identity (phase 68) profiling could create unfair task distribution over time
- Integration tests (phase 69) mock-based approach may miss real-world GitHub API quirks

## Conventions

- Python scripts use python3 (no bare python command on this system)
- GitHub API via gh CLI, not raw curl
- All new code goes to ~/zion/projects/agent-orchestration/
- Skills go to ~/.hermes/skills/ following existing category structure
- Wiki pages follow SCHEMA.md conventions (frontmatter, wikilinks, tag taxonomy)

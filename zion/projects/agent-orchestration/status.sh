#!/usr/bin/env bash
# Orchestrator status dashboard
# Shows active workers, recent completions, queue depth

set -euo pipefail

ORCH_DIR="${ORCH_PROJECT_DIR:-$HOME/zion/projects/agent-orchestration}"
WORKSPACES="$ORCH_DIR/workspaces"

if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
    echo "Usage: status.sh [--json]"
    echo ""
    echo "Show orchestrator worker status."
    echo "  --json    Output as JSON"
    exit 0
fi

JSON_MODE=false
[ "${1:-}" = "--json" ] && JSON_MODE=true

# Collect workspace states
active=0
completed=0
failed=0
active_list=""
completed_list=""
failed_list=""
total_workspaces=0

if [ -d "$WORKSPACES" ]; then
    for ws in "$WORKSPACES"/*/; do
        [ -d "$ws" ] || continue
        total_workspaces=$((total_workspaces + 1))
        meta="$ws/meta.json"
        [ -f "$meta" ] || continue

        issue_num=$(basename "$ws")
        title=$(python3 -c "import json; print(json.load(open('$meta')).get('title','?'))" 2>/dev/null || echo "?")
        status=$(python3 -c "import json; print(json.load(open('$meta')).get('status','unknown'))" 2>/dev/null || echo "unknown")
        spawned=$(python3 -c "import json; print(json.load(open('$meta')).get('spawned_at',''))" 2>/dev/null || echo "")

        case "$status" in
            in-progress)
                active=$((active + 1))
                active_list="${active_list}  #${issue_num}  ${title}\n        started: ${spawned}\n"
                ;;
            completed)
                completed=$((completed + 1))
                completed_list="${completed_list}  #${issue_num}  ${title}\n"
                ;;
            failed)
                failed=$((failed + 1))
                failed_list="${failed_list}  #${issue_num}  ${title}\n"
                ;;
        esac
    done
fi

if $JSON_MODE; then
    python3 -c "
import json
print(json.dumps({
    'active': $active,
    'completed': $completed,
    'failed': $failed,
    'total_workspaces': $total_workspaces,
}))
"
    exit 0
fi

# Terminal output
echo "╔══════════════════════════════════════════╗"
echo "║     Hermes Agent Orchestrator Status     ║"
echo "╠══════════════════════════════════════════╣"
printf "║  Active Workers:    %-20s║\n" "$active"
printf "║  Completed:         %-20s║\n" "$completed"
printf "║  Failed:            %-20s║\n" "$failed"
printf "║  Total Workspaces:  %-20s║\n" "$total_workspaces"
echo "╚══════════════════════════════════════════╝"

if [ $active -gt 0 ]; then
    echo ""
    echo "Active Workers:"
    echo -e "$active_list"
fi

if [ $completed -gt 0 ]; then
    echo ""
    echo "Completed:"
    echo -e "$completed_list"
fi

if [ $failed -gt 0 ]; then
    echo ""
    echo "Failed:"
    echo -e "$failed_list"
fi

# Recent execution history
echo ""
echo "─── Recent Pipeline Runs ───"
if [ -x "$ORCH_DIR/orch_history.py" ]; then
    python3 "$ORCH_DIR/orch_history.py" list --last 5 2>/dev/null || echo "  (no run history yet)"
else
    echo "  (orch_history.py not found)"
fi

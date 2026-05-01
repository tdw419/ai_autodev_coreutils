#!/usr/bin/env bash
# Orchestrator status dashboard
# Shows active workers, recent completions, queue depth
# Supports both single-repo and multi-repo workspace layouts

set -euo pipefail

ORCH_DIR="${ORCH_PROJECT_DIR:-$HOME/zion/projects/agent-orchestration}"
WORKSPACES="$ORCH_DIR/workspaces"

if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
    echo "Usage: status.sh [--json] [--costs]"
    echo ""
    echo "Show orchestrator worker status."
    echo "  --json    Output as JSON"
    echo "  --costs   Show per-repo cost summary"
    exit 0
fi

JSON_MODE=false
SHOW_COSTS=false
for arg in "${1:-}" "${2:-}"; do
    [ "$arg" = "--json" ] && JSON_MODE=true
    [ "$arg" = "--costs" ] && SHOW_COSTS=true
done

# scan_workspace META_PATH - extract fields from meta.json
scan_workspace() {
    local meta="$1"
    python3 -c "
import json, sys
try:
    d = json.load(open('$meta'))
    print(d.get('title', '?'))
    print(d.get('status', 'unknown'))
    print(d.get('spawned_at', ''))
    print(d.get('repo_name', ''))
    print(d.get('issue_number', '?'))
except: print('?'); print('unknown'); print(''); print(''); print('?')
" 2>/dev/null
}

# Collect workspace states (handles both flat and repo/nested layouts)
active=0
completed=0
failed=0
active_list=""
completed_list=""
failed_list=""
total_workspaces=0

scan_dir() {
    local dir="$1"
    for ws in "$dir"/*/; do
        [ -d "$ws" ] || continue
        meta="$ws/meta.json"
        [ -f "$meta" ] || {
            # Might be a repo subdirectory (multi-repo layout)
            if [ -d "$ws" ]; then
                scan_dir "$ws"
            fi
            continue
        }

        total_workspaces=$((total_workspaces + 1))
        # Read all fields at once
        read -r title status spawned repo_name issue_num <<< "$(scan_workspace "$meta")"

        case "$status" in
            in-progress)
                active=$((active + 1))
                repo_tag=""
                [ -n "$repo_name" ] && repo_tag=" [$repo_name]"
                active_list="${active_list}  #${issue_num}  ${title}${repo_tag}\n        started: ${spawned}\n"
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
}

if [ -d "$WORKSPACES" ]; then
    scan_dir "$WORKSPACES"
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

# Per-repo cost summary
if $SHOW_COSTS && [ -x "$ORCH_DIR/cost_tracker.py" ]; then
    echo ""
    echo "─── Per-Repo Cost Summary ───"
    python3 "$ORCH_DIR/cost_tracker.py" report --period 7 2>/dev/null || echo "  (no cost data yet)"
fi

# Recent execution history
echo ""
echo "─── Recent Pipeline Runs ───"
if [ -x "$ORCH_DIR/orch_history.py" ]; then
    python3 "$ORCH_DIR/orch_history.py" list --last 5 2>/dev/null || echo "  (no run history yet)"
else
    echo "  (orch_history.py not found)"
fi

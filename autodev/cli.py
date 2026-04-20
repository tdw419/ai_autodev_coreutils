"""Creative Daemon CLI -- entry point for cron and manual invocation."""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        prog="creative-daemon",
        description="AI creative daemon -- the AI chooses what to build",
    )
    subparsers = parser.add_subparsers(dest="command")

    # run: one creative cycle
    run_parser = subparsers.add_parser("run", help="Run one creative cycle")
    run_parser.add_argument("--dry-run", action="store_true", help="Generate intent but don't build")
    run_parser.add_argument("--timeout", type=int, default=900, help="Build timeout in seconds")
    run_parser.add_argument("--cycles", type=int, default=1, help="Number of cycles to run")

    # resume: retry a failed intent
    resume_parser = subparsers.add_parser("resume", help="Retry a failed intent")
    resume_parser.add_argument("intent_id", help="Intent ID to retry")
    resume_parser.add_argument("--timeout", type=int, default=900)

    # status: show state
    subparsers.add_parser("status", help="Show creative daemon status")

    # list: show all intents
    list_parser = subparsers.add_parser("list", help="List all intents")
    list_parser.add_argument("--limit", type=int, default=20)

    # show: display a specific intent
    show_parser = subparsers.add_parser("show", help="Show intent details")
    show_parser.add_argument("intent_id", help="Intent ID to show")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    if args.command == "run":
        from .creative_loop import run_once
        for i in range(args.cycles):
            if i > 0:
                print(f"\n[creative-daemon] Cycle {i+1}/{args.cycles}")
            result = run_once(dry_run=args.dry_run, timeout=args.timeout)
            if result is None and not args.dry_run:
                print("[creative-daemon] No intent generated. Stopping.")
                sys.exit(1)

    elif args.command == "resume":
        from .creative_loop import resume
        result = resume(args.intent_id, timeout=args.timeout)
        if result is None:
            sys.exit(1)

    elif args.command == "status":
        from .creative_loop import status
        status()

    elif args.command == "list":
        from .memory import list_intents
        intents = list_intents()
        for i in intents[:args.limit]:
            print(f"  [{i['status']:9s}] {i['id']}: {i['summary'][:60]}")
        if len(intents) > args.limit:
            print(f"  ... and {len(intents) - args.limit} more")

    elif args.command == "show":
        from .memory import load_intent
        intent = load_intent(args.intent_id)
        if intent is None:
            print(f"Intent {args.intent_id} not found.")
            sys.exit(1)
        print(f"ID:       {intent.id}")
        print(f"Status:   {intent.status.value}")
        print(f"Created:  {intent.created_at}")
        print(f"Summary:  {intent.summary}")
        print(f"Reasoning: {intent.reasoning}")
        print(f"Scope:    {intent.scope}")
        print(f"Target:   {intent.target_dir}")
        print(f"Attempts: {intent.attempt_count}")
        if intent.artifacts:
            print(f"Artifacts: {', '.join(intent.artifacts)}")
        if intent.result_summary:
            print(f"Result:   {intent.result_summary}")
        if intent.completed_at:
            print(f"Completed: {intent.completed_at}")


if __name__ == "__main__":
    main()

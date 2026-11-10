"""Readable commands for validation, experiments, and database verification."""
import argparse
import json

from .data import validate_inventory


def main():
    parser = argparse.ArgumentParser(prog="earlybird")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate", help="Verify all 44 statements and clause provenance")
    sub.add_parser("doctor", help="Check the local database and GDS plugin")
    sub.add_parser("verify", help="Check saved memberships against the live database")
    sub.add_parser("report", help="Regenerate reports from genuine saved results and the review")
    run = sub.add_parser("run", help="Execute genuine database clustering experiments")
    run.add_argument("--k-min", type=int, default=2)
    run.add_argument("--k-max", type=int, default=10)
    run.add_argument("--seeds", type=int, default=10)
    run.add_argument("--no-paraphrases", action="store_true")
    args = parser.parse_args()
    if args.command == "validate":
        print(json.dumps(validate_inventory(), indent=2))
    elif args.command == "report":
        from .pipeline import load_bundle, render_report
        bundle = load_bundle()
        if bundle is None:
            raise SystemExit("Run the experiment before generating a report.")
        render_report(bundle)
        print("Regenerated docs/EXPERIMENT_REPORT.md and docs/ARCHITECTURE.md")
    elif args.command == "run":
        from .pipeline import run_experiment
        run_experiment(args.k_min, args.k_max, args.seeds, not args.no_paraphrases)
    else:
        from .database import Database
        db = Database()
        try:
            print(db.status())
            if args.command == "verify":
                from .pipeline import load_bundle
                bundle = load_bundle()
                if bundle is None:
                    raise SystemExit("No experiment results yet; run earlybird run first.")
                runs = [r for data in bundle["datasets"].values() for r in data["runs"]]
                runs += [r for v in bundle["paraphrases"] for r in v["runs"]]
                failed = [r["id"] for r in runs if not db.verify_run(r)]
                print(f"Verified {len(runs)-len(failed)}/{len(runs)} saved memberships against Neo4j")
                if failed:
                    raise SystemExit(f"Missing or different runs: {failed}")
        finally:
            db.close()


if __name__ == "__main__":
    main()

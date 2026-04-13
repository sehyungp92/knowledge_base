"""Heal wiki substrate — orchestrated repair for Phase 1 of wiki integration.

Runs the following healing steps in order:
1. Prune sub-threshold entity pages (source_count < 3)
2. Link source pages to their entities (add Key Concepts sections)
3. Repair broken links (normalize resolvable, strip unresolvable)
4. Apply auto-fixes (missing frontmatter defaults, missing sections, staleness drift)
5. Run lint summary to measure health score delta

Usage:
    python scripts/heal_wiki.py [--dry-run] [--skip-prune] [--skip-links] [--skip-autofix]
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import structlog

# Force UTF-8 for stdout/stderr on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

logger = structlog.get_logger(__name__)


def _progress(msg: str) -> None:
    print(f"  -> {msg}")


def heal_wiki(
    *,
    dry_run: bool = True,
    skip_prune: bool = False,
    skip_links: bool = False,
    skip_autofix: bool = False,
) -> dict:
    """Run wiki healing pipeline.

    Args:
        dry_run: If True, report changes without writing.
        skip_prune: Skip entity pruning step.
        skip_links: Skip broken link repair step.
        skip_autofix: Skip lint auto-fix step.

    Returns:
        Summary dict with results from each step.
    """
    from reading_app.db import ensure_pool
    ensure_pool()

    results = {}
    t0 = time.monotonic()
    mode = "DRY RUN" if dry_run else "LIVE"
    print(f"\n=== Wiki Healing Pipeline ({mode}) ===\n")

    # Step 0: Pre-healing health check
    print("Step 0: Pre-healing health summary...")
    from retrieval.wiki_lint import run_lint
    pre_report = run_lint(mode="summary", on_progress=_progress)
    results["pre_health"] = {
        "pages": pre_report.pages_scanned,
        "issues": len(pre_report.issues),
        "health": _compute_health(pre_report),
    }
    print(f"  Health: {results['pre_health']['health']:.2f}/1.00, "
          f"{results['pre_health']['issues']} issues across "
          f"{results['pre_health']['pages']} pages\n")

    # Step 1: Prune sub-threshold entities
    if not skip_prune:
        print("Step 1: Pruning sub-threshold entities (source_count < 3)...")
        from retrieval.wiki_writer import prune_sub_threshold_entities
        prune_result = prune_sub_threshold_entities(min_source_count=3, dry_run=dry_run)
        results["prune"] = {
            "pruned": len(prune_result["pruned"]),
            "kept": prune_result["kept"],
            "errors": prune_result["errors"],
        }
        print(f"  Pruned: {results['prune']['pruned']}, "
              f"Kept: {results['prune']['kept']}, "
              f"Errors: {len(results['prune']['errors'])}\n")
    else:
        print("Step 1: SKIPPED (--skip-prune)\n")

    # Step 2: Link source pages to their entities
    print("Step 2: Linking source pages to entities...")
    from retrieval.wiki_writer import link_source_entities
    link_result = link_source_entities(dry_run=dry_run)
    results["link_entities"] = {
        "updated": link_result["updated"],
        "skipped": link_result["skipped"],
        "errors": len(link_result["errors"]),
    }
    print(f"  Updated: {results['link_entities']['updated']}, "
          f"Skipped: {results['link_entities']['skipped']}, "
          f"Errors: {results['link_entities']['errors']}\n")

    # Step 3: Repair broken links
    if not skip_links:
        print("Step 3: Repairing broken links...")
        from retrieval.wiki_lint import repair_broken_links
        link_result = repair_broken_links(dry_run=dry_run, on_progress=_progress)
        results["links"] = {
            "pages_scanned": link_result["pages_scanned"],
            "links_checked": link_result["links_checked"],
            "links_fixed": link_result["links_fixed"],
            "links_stripped": link_result["links_stripped"],
        }
        print(f"  Fixed: {results['links']['links_fixed']}, "
              f"Stripped: {results['links']['links_stripped']}, "
              f"Checked: {results['links']['links_checked']}\n")
    else:
        print("Step 3: SKIPPED (--skip-links)\n")

    # Step 4: Apply auto-fixes (frontmatter defaults, missing sections, etc.)
    if not skip_autofix:
        print("Step 4: Applying lint auto-fixes...")
        if dry_run:
            fix_report = run_lint(mode="summary", on_progress=_progress)
            auto_fixable = sum(1 for i in fix_report.issues if getattr(i, "auto_fixable", False))
            results["autofix"] = {"fixed": 0, "auto_fixable": auto_fixable, "dry_run": True}
            print(f"  Auto-fixable issues found: {auto_fixable} (not applied in dry-run)\n")
        else:
            fix_report = run_lint(mode="fix", on_progress=_progress)
            results["autofix"] = {"fixed": fix_report.fixed, "dry_run": False}
            print(f"  Auto-fixes applied: {fix_report.fixed}\n")
    else:
        print("Step 4: SKIPPED (--skip-autofix)\n")

    # Step 5: Post-healing health check
    if not dry_run:
        print("Step 5: Post-healing health summary...")
        post_report = run_lint(mode="summary", on_progress=_progress)
        results["post_health"] = {
            "pages": post_report.pages_scanned,
            "issues": len(post_report.issues),
            "health": _compute_health(post_report),
        }
        print(f"  Health: {results['post_health']['health']:.2f}/1.00, "
              f"{results['post_health']['issues']} issues across "
              f"{results['post_health']['pages']} pages")

        # Delta
        pre = results["pre_health"]
        post = results["post_health"]
        issue_delta = post["issues"] - pre["issues"]
        health_delta = post["health"] - pre["health"]
        print(f"\n  Delta: {issue_delta:+d} issues, {health_delta:+.3f} health score")
    else:
        print("Step 5: SKIPPED (dry-run mode — re-run without --dry-run to see delta)\n")

    elapsed = time.monotonic() - t0
    print(f"\n=== Healing complete in {elapsed:.1f}s ===\n")
    results["elapsed_s"] = round(elapsed, 1)
    return results


def _compute_health(report) -> float:
    """Compute health score from lint report (0.0 = worst, 1.0 = best)."""
    if report.pages_scanned == 0:
        return 0.0
    # Health = 1 - (issues / (pages * max_issues_per_page))
    # Approximate max_issues_per_page as 10
    raw = 1.0 - (len(report.issues) / (report.pages_scanned * 10))
    return max(0.0, min(1.0, raw))


def main():
    parser = argparse.ArgumentParser(description="Heal wiki substrate")
    parser.add_argument("--live", action="store_true", default=False,
                        help="Apply changes (default is dry-run)")
    parser.add_argument("--skip-prune", action="store_true", help="Skip entity pruning")
    parser.add_argument("--skip-links", action="store_true", help="Skip broken link repair")
    parser.add_argument("--skip-autofix", action="store_true", help="Skip lint auto-fixes")
    args = parser.parse_args()

    dry_run = not args.live

    results = heal_wiki(
        dry_run=dry_run,
        skip_prune=args.skip_prune,
        skip_links=args.skip_links,
        skip_autofix=args.skip_autofix,
    )

    if dry_run:
        print("This was a dry run. Re-run with --live to apply changes.")


if __name__ == "__main__":
    main()

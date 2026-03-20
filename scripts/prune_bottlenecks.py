"""Bottleneck quality pass: reclassify null types, prune generic/duplicate entries.

Cross-theme dedup catches bottlenecks that slipped past within-theme pg_trgm dedup
(e.g., same bottleneck described under multiple themes).

Usage:
    python -m scripts.prune_bottlenecks [--dry-run] [--verbose]
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Keyword-based type classification for null bottleneck_type
# ---------------------------------------------------------------------------
TYPE_PATTERNS: list[tuple[str, list[str]]] = [
    ("algorithmic", [
        r"algorithm", r"architecture", r"model design", r"representation",
        r"attention", r"transformer", r"training (method|approach|technique)",
        r"optimization", r"learning (rate|schedule|algorithm)",
        r"objective function", r"loss function", r"convergence",
    ]),
    ("data", [
        r"data", r"dataset", r"training (data|corpus|set)", r"annotation",
        r"label", r"curate", r"distribution", r"out.of.distribution",
        r"data (quality|scarcity|availability|collection)",
    ]),
    ("compute", [
        r"compute", r"gpu", r"memory", r"flop", r"cost",
        r"inference (cost|latency|time)", r"training (cost|time|budget)",
        r"hardware", r"accelerator", r"throughput", r"batch",
    ]),
    ("integration", [
        r"integration", r"infrastructure", r"deployment", r"production",
        r"pipeline", r"tooling", r"engineering", r"api",
        r"interoperab", r"ecosystem", r"standard",
    ]),
    ("theoretical", [
        r"theoretical", r"mathematical", r"formal", r"fundamental",
        r"proof", r"guarantee", r"impossib", r"understanding",
        r"interpretab", r"explain",
    ]),
    ("regulatory", [
        r"regulat", r"policy", r"legal", r"compliance", r"privacy",
        r"safety", r"ethic", r"governance", r"liability",
    ]),
    ("hardware", [
        r"hardware", r"chip", r"sensor", r"actuator", r"robot",
        r"device", r"physical", r"manufacturing",
    ]),
]


def classify_type(description: str) -> str | None:
    """Classify a bottleneck type from its description using keyword matching."""
    desc_lower = description.lower()
    scores: dict[str, int] = {}
    for btype, patterns in TYPE_PATTERNS:
        for p in patterns:
            if re.search(p, desc_lower):
                scores[btype] = scores.get(btype, 0) + 1
    if not scores:
        return None
    return max(scores, key=lambda k: scores[k])


# ---------------------------------------------------------------------------
# Signal strength scoring
# ---------------------------------------------------------------------------
SPECULATIVE_MARKERS = [
    r"may\b", r"might\b", r"could\b", r"potentially",
    r"hypothetical", r"unclear", r"not yet",
    r"remains to be seen", r"speculative", r"unknown whether",
]

GROUNDED_MARKERS = [
    r"demonstrated", r"observed", r"measured", r"reported",
    r"shown", r"evidence", r"benchmark", r"experiment",
    r"paper", r"study", r"currently", r"today",
    r"requires? \d", r"\d+x", r"\$\d",
]


def score_signal_strength(description: str, confidence: float | None) -> str:
    """Score a bottleneck as grounded, moderate, or speculative."""
    desc_lower = description.lower()
    speculative_hits = sum(1 for p in SPECULATIVE_MARKERS if re.search(p, desc_lower))
    grounded_hits = sum(1 for p in GROUNDED_MARKERS if re.search(p, desc_lower))

    if grounded_hits >= 2 and (confidence or 0) >= 0.7:
        return "grounded"
    if speculative_hits >= 2 or (confidence or 0) < 0.4:
        return "speculative"
    if grounded_hits >= 1 and (confidence or 0) >= 0.5:
        return "grounded"
    return "moderate"


# ---------------------------------------------------------------------------
# Generic low-signal detection
# ---------------------------------------------------------------------------
GENERIC_PATTERNS = [
    r"further research is needed",
    r"(scalability|generalization) (is|remains) (unproven|unclear|uncertain)",
    r"may not (scale|generalize)",
    # Note: "no established method for X" is a valid bottleneck — don't flag it.
    # Only flag truly vacuous descriptions:
    r"the (paper|source|article) does not (address|discuss)",
    r"not (addressed|discussed|evaluated|mentioned) in",
    r"whether .{5,60} remains (unclear|unknown|to be seen)",
]


def is_generic(description: str) -> bool:
    """Check if a bottleneck is a generic observation rather than a specific insight."""
    desc_lower = description.lower()
    return any(re.search(p, desc_lower) for p in GENERIC_PATTERNS)


# ---------------------------------------------------------------------------
# Near-duplicate detection
# ---------------------------------------------------------------------------
def find_near_duplicates(rows: list[dict], threshold: float = 0.85) -> set[str]:
    """Find near-duplicate bottlenecks using word-trigram Jaccard similarity.

    Returns IDs of duplicates to remove (keeps the highest-confidence version).
    """
    from collections import defaultdict

    def trigrams(text: str) -> set[str]:
        words = text.lower().split()[:20]
        return {" ".join(words[i:i+3]) for i in range(len(words) - 2)}

    trigram_index: dict[str, list[int]] = defaultdict(list)
    row_trigrams = []
    for i, r in enumerate(rows):
        tg = trigrams(r["description"])
        row_trigrams.append(tg)
        for t in tg:
            trigram_index[t].append(i)

    duplicates: set[str] = set()
    checked: set[tuple[int, int]] = set()

    for i in range(len(rows)):
        if rows[i]["id"] in duplicates:
            continue
        candidates: dict[int, int] = {}
        for t in row_trigrams[i]:
            for j in trigram_index[t]:
                if j > i and (i, j) not in checked:
                    candidates[j] = candidates.get(j, 0) + 1

        for j, shared in candidates.items():
            if rows[j]["id"] in duplicates:
                continue
            checked.add((i, j))
            union = len(row_trigrams[i] | row_trigrams[j])
            if union == 0:
                continue
            sim = shared / union
            if sim >= threshold:
                if (rows[j].get("confidence") or 0) > (rows[i].get("confidence") or 0):
                    duplicates.add(rows[i]["id"])
                    break
                else:
                    duplicates.add(rows[j]["id"])

    return duplicates


# ---------------------------------------------------------------------------
# Resolution horizon normalization
# ---------------------------------------------------------------------------
HORIZON_CANONICAL = {
    "2_3_years": "3-5_years",
    "5+_years": "3-5_years",  # Normalize rare values
}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Bottleneck quality pass")
    parser.add_argument("--dry-run", action="store_true", help="Print changes without applying")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    from reading_app.config import Config
    from reading_app.db import init_pool, get_conn

    config = Config()
    init_pool(config.postgres_dsn)

    with get_conn() as conn:
        total = conn.execute("SELECT COUNT(*) AS c FROM bottlenecks").fetchone()["c"]
        null_types = conn.execute(
            "SELECT COUNT(*) AS c FROM bottlenecks WHERE bottleneck_type IS NULL"
        ).fetchone()["c"]
        logger.info("Before: %d bottlenecks, %d with null type", total, null_types)

        # Step 1: Reclassify null types
        null_rows = conn.execute(
            "SELECT id, description FROM bottlenecks WHERE bottleneck_type IS NULL"
        ).fetchall()

        reclassified = 0
        for row in null_rows:
            new_type = classify_type(row["description"])
            if new_type:
                if not args.dry_run:
                    conn.execute(
                        "UPDATE bottlenecks SET bottleneck_type = %s WHERE id = %s",
                        (new_type, row["id"]),
                    )
                reclassified += 1
                if args.verbose:
                    logger.debug("Reclassify %s -> %s: %s",
                                 row["id"][:8], new_type, row["description"][:80])

        logger.info("Reclassified %d / %d null-type bottlenecks", reclassified, len(null_rows))

        # Step 2: Normalize resolution horizons
        horizon_fixed = 0
        for old_val, new_val in HORIZON_CANONICAL.items():
            if args.dry_run:
                count = conn.execute(
                    "SELECT COUNT(*) AS c FROM bottlenecks WHERE resolution_horizon = %s",
                    (old_val,),
                ).fetchone()["c"]
                horizon_fixed += count
            else:
                result = conn.execute(
                    "UPDATE bottlenecks SET resolution_horizon = %s WHERE resolution_horizon = %s",
                    (new_val, old_val),
                )
                horizon_fixed += result.rowcount

        if horizon_fixed:
            logger.info("Normalized %d resolution_horizon values", horizon_fixed)

        # Step 3: Identify prune candidates
        all_bns = conn.execute(
            "SELECT id, description, confidence FROM bottlenecks ORDER BY confidence ASC"
        ).fetchall()

        tier1_generic = []
        tier2_speculative = []

        for row in all_bns:
            if is_generic(row["description"]):
                tier1_generic.append(row["id"])
            elif score_signal_strength(row["description"], row["confidence"]) == "speculative":
                tier2_speculative.append(row["id"])

        # Step 4: Cross-theme near-duplicate detection
        logger.info("Scanning for near-duplicate bottlenecks...")
        dup_ids = find_near_duplicates(
            [dict(r) for r in all_bns],
            threshold=0.80,
        )
        tier3_duplicates = list(dup_ids - set(tier1_generic) - set(tier2_speculative))

        logger.info("Prune candidates: %d generic, %d speculative, %d cross-theme duplicates",
                     len(tier1_generic), len(tier2_speculative), len(tier3_duplicates))

        # Soft-delete: set bottleneck_type to 'pruned'
        to_remove = list(set(tier1_generic + tier3_duplicates + tier2_speculative))

        if to_remove and not args.dry_run:
            for bid in to_remove:
                conn.execute(
                    "UPDATE bottlenecks SET bottleneck_type = 'pruned', staleness_score = -1 WHERE id = %s",
                    (bid,),
                )

        if not args.dry_run:
            conn.commit()

        remaining = conn.execute(
            "SELECT COUNT(*) AS c FROM bottlenecks WHERE bottleneck_type != 'pruned' OR bottleneck_type IS NULL"
        ).fetchone()["c"]
        logger.info("After: %d active bottlenecks (pruned %d)", remaining, len(to_remove))

    print("\n=== Bottleneck Quality Pass Complete ===")
    print(f"  Reclassified: {reclassified} null -> typed")
    print(f"  Horizons normalized: {horizon_fixed}")
    print(f"  Pruned: {len(to_remove)} low-signal bottlenecks")
    print(f"    Generic: {len(tier1_generic)}, Speculative: {len(tier2_speculative)}, Duplicates: {len(tier3_duplicates)}")
    print(f"  Active: {remaining} / {total}")
    if args.dry_run:
        print("  [DRY RUN - no changes applied]")


if __name__ == "__main__":
    main()

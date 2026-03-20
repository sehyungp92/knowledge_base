"""Capability quality pass: reclassify maturity, score signal strength, prune low-signal.

Cross-theme dedup catches capabilities that slipped past within-theme pg_trgm dedup
(e.g., same capability described under multiple themes).

Usage:
    python -m scripts.prune_capabilities [--dry-run] [--verbose]
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
# Maturity keyword classification (for unset/null maturity)
# ---------------------------------------------------------------------------
MATURITY_PATTERNS: list[tuple[str, list[str]]] = [
    ("commoditized", [
        r"widely (deployed|adopted|available)", r"commodity", r"standard practice",
        r"off.the.shelf", r"production.grade", r"mainstream",
    ]),
    ("broad_production", [
        r"multiple (companies|organizations|teams) deploy",
        r"commercial (product|service|deployment)s",
        r"widely used in production", r"industry.wide",
    ]),
    ("narrow_production", [
        r"deployed (at|by|in)", r"production (system|use|deployment)",
        r"commercially available", r"shipping", r"in production",
    ]),
    ("demo", [
        r"demonstrat", r"prototype", r"proof.of.concept", r"achieves? \d",
        r"outperforms?", r"state.of.the.art", r"sota", r"benchmark",
        r"zero.shot", r"few.shot", r"success rate",
    ]),
    ("research_only", [
        r"proposed", r"preliminary", r"initial results", r"early",
        r"theoretical", r"conceptual", r"not yet (tested|validated|deployed)",
    ]),
]


def classify_maturity(description: str) -> str | None:
    """Classify a capability maturity from its description using keyword matching."""
    desc_lower = description.lower()
    for maturity, patterns in MATURITY_PATTERNS:
        hits = sum(1 for p in patterns if re.search(p, desc_lower))
        if hits >= 2:
            return maturity
    return None


# ---------------------------------------------------------------------------
# Signal strength scoring
# ---------------------------------------------------------------------------
SPECULATIVE_MARKERS = [
    r"may\b", r"might\b", r"could\b", r"potentially",
    r"hypothetical", r"expected to", r"in theory",
    r"should\b", r"anticipated", r"promising",
]

GROUNDED_MARKERS = [
    r"demonstrated", r"achieves?", r"measured", r"reported",
    r"shown", r"found that", r"benchmark", r"outperforms?",
    r"deployed", r"production", r"\d+%", r"\d+x",
    r"evaluated", r"tested on", r"validated",
]


def score_signal_strength(description: str, confidence: float | None) -> str:
    """Score a capability as grounded, moderate, or speculative."""
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
    r"can (handle|process|generate|perform) .{0,30}tasks?$",
    r"is able to",
    r"supports? .{0,20}(various|different|multiple) .{0,20}(tasks|modalities|domains)",
    r"improves? (upon|over|on) (prior|previous|existing|baseline)",
    r"achieves? (good|better|improved|competitive|comparable) (results|performance)",
    r"the (model|system|approach) can",
    r"(enables?|allows?|facilitates?) .{0,40}$",
]


def is_generic(description: str) -> bool:
    """Check if a capability is a generic observation rather than a specific insight."""
    desc_lower = description.lower()
    return any(re.search(p, desc_lower) for p in GENERIC_PATTERNS)


# ---------------------------------------------------------------------------
# Near-duplicate detection (reuses prune_limitations pattern)
# ---------------------------------------------------------------------------
def find_near_duplicates(rows: list[dict], threshold: float = 0.85) -> set[str]:
    """Find near-duplicate capabilities using word-trigram Jaccard similarity.

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
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Capability quality pass")
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
        caps = conn.execute("SELECT COUNT(*) AS c FROM capabilities").fetchone()["c"]
        null_maturity = conn.execute(
            "SELECT COUNT(*) AS c FROM capabilities WHERE maturity IS NULL"
        ).fetchone()["c"]
        logger.info("Before: %d capabilities, %d with null maturity", caps, null_maturity)

        # Step 1: Reclassify null maturity
        null_rows = conn.execute(
            "SELECT id, description FROM capabilities WHERE maturity IS NULL"
        ).fetchall()

        reclassified = 0
        for row in null_rows:
            new_mat = classify_maturity(row["description"])
            if new_mat:
                if not args.dry_run:
                    conn.execute(
                        "UPDATE capabilities SET maturity = %s WHERE id = %s",
                        (new_mat, row["id"]),
                    )
                reclassified += 1
                if args.verbose:
                    logger.debug("Reclassify %s -> %s: %s",
                                 row["id"][:8], new_mat, row["description"][:80])

        logger.info("Reclassified %d / %d null-maturity capabilities", reclassified, len(null_rows))

        # Step 2: Identify candidates for removal
        all_caps = conn.execute(
            "SELECT id, description, confidence, maturity FROM capabilities ORDER BY confidence ASC"
        ).fetchall()

        tier1_generic = []
        tier2_speculative = []

        for row in all_caps:
            if is_generic(row["description"]):
                tier1_generic.append(row["id"])
            elif score_signal_strength(row["description"], row["confidence"]) == "speculative":
                tier2_speculative.append(row["id"])

        # Step 3: Cross-theme near-duplicate detection
        logger.info("Scanning for near-duplicate capabilities...")
        dup_ids = find_near_duplicates(
            [dict(r) for r in all_caps],
            threshold=0.80,
        )
        tier3_duplicates = list(dup_ids - set(tier1_generic) - set(tier2_speculative))

        logger.info("Prune candidates: %d generic, %d speculative, %d cross-theme duplicates",
                     len(tier1_generic), len(tier2_speculative), len(tier3_duplicates))

        # Soft-delete: set maturity to 'pruned'
        to_remove = list(set(tier1_generic + tier3_duplicates + tier2_speculative))

        if to_remove and not args.dry_run:
            for cid in to_remove:
                conn.execute(
                    "UPDATE capabilities SET maturity = 'pruned', staleness_score = -1 WHERE id = %s",
                    (cid,),
                )

        if not args.dry_run:
            conn.commit()

        remaining = conn.execute(
            "SELECT COUNT(*) AS c FROM capabilities WHERE maturity != 'pruned' OR maturity IS NULL"
        ).fetchone()["c"]
        logger.info("After: %d active capabilities (pruned %d)", remaining, len(to_remove))

    print("\n=== Capability Quality Pass Complete ===")
    print(f"  Reclassified: {reclassified} null -> typed maturity")
    print(f"  Pruned: {len(to_remove)} low-signal capabilities")
    print(f"    Generic: {len(tier1_generic)}, Speculative: {len(tier2_speculative)}, Duplicates: {len(tier3_duplicates)}")
    print(f"  Active: {remaining} / {caps}")
    if args.dry_run:
        print("  [DRY RUN - no changes applied]")


if __name__ == "__main__":
    main()

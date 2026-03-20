"""Limitation quality pass: reclassify unknown types, add signal_strength, prune low-signal.

Targets ~1.3:1 limitation:capability ratio by:
1. Adding a signal_strength column (grounded, moderate, speculative)
2. Reclassifying 'unknown' limitation types using description keywords
3. Scoring signal strength based on evidence quality markers
4. Soft-deleting speculative limitations with low confidence

Usage:
    python -m scripts.prune_limitations [--dry-run] [--verbose]
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
# Keyword-based type classification for 'unknown' limitations
# ---------------------------------------------------------------------------
TYPE_PATTERNS: list[tuple[str, list[str]]] = [
    ("architectural", [
        r"architecture", r"transformer", r"attention", r"model design",
        r"representation", r"embedding", r"token", r"context window",
        r"autoregressive", r"decoder", r"encoder", r"inductive bias",
    ]),
    ("engineering", [
        r"implementation", r"infrastructure", r"latency", r"throughput",
        r"deployment", r"production", r"system", r"pipeline", r"integration",
        r"tooling", r"engineering", r"framework", r"api", r"interface",
    ]),
    ("data", [
        r"data", r"dataset", r"training data", r"annotation", r"label",
        r"corpus", r"sample", r"example", r"curate", r"quality of data",
        r"distribution", r"domain", r"out.of.distribution",
    ]),
    ("compute", [
        r"compute", r"gpu", r"memory", r"flop", r"cost", r"inference cost",
        r"training cost", r"scale", r"parameter", r"billion",
        r"hardware", r"accelerator",
    ]),
    ("theoretical", [
        r"theoretical", r"mathematical", r"proof", r"convergence",
        r"guarantee", r"formal", r"fundamental", r"impossib",
        r"understanding", r"interpretab", r"explain",
    ]),
    ("behavioral", [
        r"reward hacking", r"mode collapse", r"training (instability|instabilities)",
        r"reward (gaming|exploiting)", r"degenerate", r"exploration",
        r"exploitation", r"entropy collapse", r"catastrophic forgetting",
        r"reward model", r"reward signal", r"rl (training|fine-tuning|optimization)",
        r"reinforcement learning", r"policy", r"on-policy", r"off-policy",
        r"training (dynamics|stability|divergence|collapse)",
        r"rlhf", r"rlvr", r"ppo", r"grpo", r"dpo",
        r"overfit", r"underfitting", r"generalization gap",
        r"curriculum", r"credit assignment", r"sparse reward",
    ]),
    ("evaluation", [
        r"benchmark", r"evaluation", r"metric", r"reproducib",
        r"leaderboard", r"contamination", r"saturat", r"ceiling",
        r"measurement", r"ground truth", r"annotation",
        r"inter.rater", r"human eval", r"test set",
        r"pass@", r"accuracy", r"f1", r"bleu", r"rouge",
        r"held.out", r"validation", r"ablation",
    ]),
]


def classify_type(description: str) -> str | None:
    """Classify a limitation type from its description using keyword matching."""
    desc_lower = description.lower()
    scores: dict[str, int] = {}
    for ltype, patterns in TYPE_PATTERNS:
        for p in patterns:
            if re.search(p, desc_lower):
                scores[ltype] = scores.get(ltype, 0) + 1
    if not scores:
        return None
    return max(scores, key=lambda k: scores[k])


# ---------------------------------------------------------------------------
# Signal strength scoring
# ---------------------------------------------------------------------------
SPECULATIVE_MARKERS = [
    r"may\b", r"might\b", r"could\b", r"potentially",
    r"hypothetical", r"unclear", r"not yet tested",
    r"remains to be seen", r"speculative", r"unknown whether",
    r"has not been", r"hasn't been", r"unvalidated",
]

GROUNDED_MARKERS = [
    r"demonstrated", r"observed", r"measured", r"reported",
    r"shown", r"found that", r"evidence", r"experiment",
    r"benchmark", r"evaluation", r"tested", r"validated",
    r"published", r"paper", r"study",
]


def score_signal_strength(description: str, confidence: float | None) -> str:
    """Score a limitation as grounded, moderate, or speculative."""
    desc_lower = description.lower()

    speculative_hits = sum(1 for p in SPECULATIVE_MARKERS if re.search(p, desc_lower))
    grounded_hits = sum(1 for p in GROUNDED_MARKERS if re.search(p, desc_lower))

    # High confidence + grounded language = grounded
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
    r"has not been tested at larger scale",
    r"model hasn.t been (tested|evaluated|deployed)",
    r"further research is needed",
    r"long.term (effects|implications|impact) are unclear",
    r"(scalability|generalization) (is|remains) (unproven|unclear|uncertain)",
    r"may not generalize",
    r"limited to .{0,30} (setting|domain|task)s?$",
    r"no (discussion|mention|analysis|evaluation) of",
    r"the (paper|source|article|author) does not (address|discuss|evaluate|mention)",
    r"not (addressed|discussed|evaluated|mentioned|explored) in",
    r"remains (an open|an unsolved|a significant|a major) (question|problem|challenge)",
    r"whether .{5,60} remains (unclear|unknown|to be seen)",
    r"no (empirical|quantitative|rigorous) (evidence|data|evaluation|validation)",
    r"the source does not",
    r"conspicuously absent",
    r"not publicly (disclosed|available|released)",
    r"no .{0,20}(metric|benchmark|evaluation|comparison)s? (are |is |were )?(provided|given|reported|disclosed)",
]


def is_generic(description: str) -> bool:
    """Check if a limitation is a generic observation rather than a specific insight."""
    desc_lower = description.lower()
    return any(re.search(p, desc_lower) for p in GENERIC_PATTERNS)


def find_near_duplicates(rows: list[dict], threshold: float = 0.85) -> set[str]:
    """Find near-duplicate limitations using trigram similarity.

    Returns IDs of duplicates to remove (keeps the highest-confidence version).
    """
    from collections import defaultdict

    # Group by source to find cross-source duplicates
    # Use word-level trigrams for fast comparison
    def trigrams(text: str) -> set[str]:
        words = text.lower().split()[:20]  # First 20 words
        return {" ".join(words[i:i+3]) for i in range(len(words) - 2)}

    # Build trigram index
    trigram_index: dict[str, list[int]] = defaultdict(list)
    row_trigrams = []
    for i, r in enumerate(rows):
        tg = trigrams(r["description"])
        row_trigrams.append(tg)
        for t in tg:
            trigram_index[t].append(i)

    # Find candidate pairs via shared trigrams
    duplicates: set[str] = set()
    checked: set[tuple[int, int]] = set()

    for i in range(len(rows)):
        if rows[i]["id"] in duplicates:
            continue
        # Get candidates that share trigrams
        candidates: dict[int, int] = {}
        for t in row_trigrams[i]:
            for j in trigram_index[t]:
                if j > i and (i, j) not in checked:
                    candidates[j] = candidates.get(j, 0) + 1

        for j, shared in candidates.items():
            if rows[j]["id"] in duplicates:
                continue
            checked.add((i, j))
            # Jaccard similarity
            union = len(row_trigrams[i] | row_trigrams[j])
            if union == 0:
                continue
            sim = shared / union
            if sim >= threshold:
                # Keep higher confidence, remove the other
                if (rows[j].get("confidence") or 0) > (rows[i].get("confidence") or 0):
                    duplicates.add(rows[i]["id"])
                    break  # i is removed, stop checking
                else:
                    duplicates.add(rows[j]["id"])

    return duplicates


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Limitation quality pass")
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
        # Step 0: Add signal_strength column if missing
        try:
            conn.execute(
                """ALTER TABLE limitations
                   ADD COLUMN IF NOT EXISTS signal_strength TEXT
                   DEFAULT 'moderate'"""
            )
            conn.commit()
            logger.info("Added signal_strength column")
        except Exception:
            conn.rollback()
            logger.info("signal_strength column already exists")

        # Get current counts
        caps = conn.execute("SELECT COUNT(*) AS c FROM capabilities").fetchone()["c"]
        lims = conn.execute("SELECT COUNT(*) AS c FROM limitations").fetchone()["c"]
        unknowns = conn.execute(
            "SELECT COUNT(*) AS c FROM limitations WHERE limitation_type = 'unknown'"
        ).fetchone()["c"]
        logger.info("Before: %d capabilities, %d limitations (ratio %.2f:1), %d unknown type",
                     caps, lims, lims / caps if caps else 0, unknowns)

        # Step 1: Reclassify unknown types
        unknown_rows = conn.execute(
            "SELECT id, description FROM limitations WHERE limitation_type = 'unknown'"
        ).fetchall()

        reclassified = 0
        for row in unknown_rows:
            new_type = classify_type(row["description"])
            if new_type:
                if not args.dry_run:
                    conn.execute(
                        "UPDATE limitations SET limitation_type = %s WHERE id = %s",
                        (new_type, row["id"]),
                    )
                reclassified += 1
                if args.verbose:
                    logger.debug("Reclassify %s -> %s: %s",
                                 row["id"][:8], new_type, row["description"][:80])

        logger.info("Reclassified %d / %d unknown limitations", reclassified, len(unknown_rows))

        # Step 2: Score signal strength for all limitations
        all_lims = conn.execute(
            "SELECT id, description, confidence FROM limitations"
        ).fetchall()

        strength_counts = {"grounded": 0, "moderate": 0, "speculative": 0}
        for row in all_lims:
            strength = score_signal_strength(row["description"], row["confidence"])
            strength_counts[strength] += 1
            if not args.dry_run:
                conn.execute(
                    "UPDATE limitations SET signal_strength = %s WHERE id = %s",
                    (strength, row["id"]),
                )

        logger.info("Signal strength distribution: %s", strength_counts)

        # Step 3: Identify candidates for removal using tiered approach
        # Tier 1: Generic observations (any confidence)
        all_for_pruning = conn.execute(
            """SELECT id, description, confidence, severity
               FROM limitations
               ORDER BY confidence ASC"""
        ).fetchall()

        tier1_generic = []  # Generic patterns regardless of confidence
        tier2_minor_moderate = []  # Minor severity + not grounded
        tier3_duplicates = []  # Near-duplicate limitations

        for row in all_for_pruning:
            if is_generic(row["description"]):
                tier1_generic.append(row["id"])
            elif row["severity"] == "minor" and \
                 score_signal_strength(row["description"], row["confidence"]) != "grounded":
                tier2_minor_moderate.append(row["id"])

        # Tier 3: Find near-duplicates across entire set
        logger.info("Scanning for near-duplicate limitations...")
        dup_ids = find_near_duplicates(
            [dict(r) for r in all_for_pruning],
            threshold=0.80,
        )
        tier3_duplicates = list(dup_ids - set(tier1_generic) - set(tier2_minor_moderate))

        logger.info("Prune candidates: %d generic, %d minor+moderate, %d duplicates",
                     len(tier1_generic), len(tier2_minor_moderate), len(tier3_duplicates))

        # Calculate target: reach ~1.3:1 ratio
        target_lims = int(caps * 1.35)
        excess = lims - target_lims
        if excess <= 0:
            logger.info("Already at or below 1.35:1 ratio, no pruning needed")
            to_remove = []
        else:
            # Apply tiers in order until we hit target
            to_remove = []
            for tier in [tier1_generic, tier3_duplicates, tier2_minor_moderate]:
                for lid in tier:
                    if len(to_remove) >= excess:
                        break
                    if lid not in to_remove:
                        to_remove.append(lid)
                if len(to_remove) >= excess:
                    break

        logger.info("Pruning %d limitations (speculative+generic+low-confidence)", len(to_remove))

        if to_remove and not args.dry_run:
            # Soft delete: set severity to 'pruned' rather than hard delete
            for lid in to_remove:
                conn.execute(
                    "UPDATE limitations SET severity = 'pruned', signal_strength = 'speculative' WHERE id = %s",
                    (lid,),
                )

        if not args.dry_run:
            conn.commit()

        # Final counts
        remaining = conn.execute(
            "SELECT COUNT(*) AS c FROM limitations WHERE severity != 'pruned'"
        ).fetchone()["c"]
        logger.info("After: %d capabilities, %d active limitations (ratio %.2f:1)",
                     caps, remaining, remaining / caps if caps else 0)
        logger.info("Pruned limitations are soft-deleted (severity='pruned'), can be recovered")

    print("\n=== Limitation Quality Pass Complete ===")
    print(f"  Reclassified: {reclassified} unknown -> typed")
    print(f"  Signal strength: {strength_counts}")
    print(f"  Pruned: {len(to_remove)} low-signal limitations")
    print(f"  Final ratio: {remaining}/{caps} = {remaining/caps:.2f}:1" if caps else "  No capabilities")
    if args.dry_run:
        print("  [DRY RUN - no changes applied]")


if __name__ == "__main__":
    main()

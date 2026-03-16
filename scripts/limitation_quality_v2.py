"""Limitation quality v2: comprehensive recalibration and enrichment.

Implements all 7 fixes from docs/limitation-quality-evaluation.md:
  1. Add behavioral + evaluation type patterns (reclassify ~300 unknowns)
  2. Severity recalibration (upgrade/downgrade based on content)
  3. Structural signal_strength scoring (replace keyword-based scoring)
  4. Theme-aware ratio pruning (reduce noise in skewed themes)
  5. Speculative-in-significant downgrade (23 hedging entries)
  6. Embedding-based semantic deduplication (requires Ollama)
  7. Claim-linking pass (grounding_claim_ids)
  + Restore over-pruned quantitative limitations

Usage:
    python -m scripts.limitation_quality_v2 [--dry-run] [--verbose]
    python -m scripts.limitation_quality_v2 --skip-embeddings   # skip fix 6
    python -m scripts.limitation_quality_v2 --only <step>        # run single step
"""

from __future__ import annotations

import argparse
import json
import logging
import re
from collections import defaultdict

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Fix 1: Extended type patterns (adds behavioral + evaluation)
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
    # NEW: behavioral / training dynamics
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
    # NEW: evaluation methodology
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
# Fix 2: Severity recalibration patterns
# ---------------------------------------------------------------------------
UPGRADE_TO_BLOCKING = [
    r"\b(?:5[0-9]|[6-9]\d|100)(?:\.\d+)?%\s*(?:failure|error|degradation|drop|decrease|loss|gap)",
    r"(?:failure|error)\s*rate\s*(?:of\s*)?\b(?:5[0-9]|[6-9]\d|100)(?:\.\d+)?%",
    r"fundamentally cannot",
    r"impossible to",
    r"cannot be (?:solved|achieved|addressed)",
    r"completely fail",
    r"total(?:ly)? (?:fail|break|collapse)",
    r"zero (?:accuracy|performance|success)",
    r"unusable",
    r"no (?:correct|valid|usable) (?:output|result|answer)",
]

DOWNGRADE_TO_MINOR = [
    r"remains to be seen",
    r"further research (?:is )?needed",
    r"it is unclear whether",
    r"has not been tested",
    r"hasn't been tested",
    r"not yet been (?:achieved|tested|demonstrated|validated)",
    r"unknown whether",
    r"remains unclear",
    r"future work",
    r"(?:long|longer).term (?:effects|implications|impact) (?:are |remain )?unclear",
    r"not yet (?:been )?(?:explored|investigated|studied)",
    r"whether .{5,60} remains (?:unclear|unknown|to be seen|an open question)",
    r"preliminary",
    r"early (?:stage|days|results)",
    r"only (?:tested|evaluated|validated) (?:on|with|in) (?:a single|one)",
]


def recalibrate_severity(description: str, current_severity: str) -> str | None:
    """Return new severity if recalibration applies, else None."""
    desc_lower = description.lower()

    # Upgrade: significant -> blocking for quantified severe failures
    if current_severity == "significant":
        for p in UPGRADE_TO_BLOCKING:
            if re.search(p, desc_lower):
                return "blocking"

    # Downgrade: significant -> minor for hedging language
    if current_severity == "significant":
        for p in DOWNGRADE_TO_MINOR:
            if re.search(p, desc_lower):
                return "minor"

    return None


# ---------------------------------------------------------------------------
# Fix 3: Structural signal strength scoring
# ---------------------------------------------------------------------------
NAMED_BENCHMARKS = re.compile(
    r"\b(?:MMLU|GSM|HumanEval|MBPP|MATH|ARC|HellaSwag|WinoGrande|TruthfulQA|"
    r"GPQA|BigBench|SuperGLUE|GLUE|ImageNet|COCO|VQA|SQuAD|NaturalQuestions|"
    r"MT-?Bench|AlpacaEval|Chatbot Arena|LMSYS|LiveBench|IFEval|"
    r"CodeContests|SWE-?bench|WebArena|OSWorld|GAIA|"
    r"rFVD|FID|BLEU|ROUGE|CIDEr|METEOR|BERTScore|"
    r"pass@\d+|top-?\d+|F1|accuracy|precision|recall)\b",
    re.IGNORECASE,
)

PERCENTAGE_RE = re.compile(r"\d+\.?\d*%")
MULTI_DIGIT_RE = re.compile(r"\b\d{2,}\b")
COMPARISON_RE = re.compile(r"\b(?:vs\.?|versus|compared to|outperform|underperform|worse than|better than)\b", re.IGNORECASE)

SPECULATIVE_MARKERS = [
    r"may\b", r"might\b", r"could\b", r"potentially",
    r"hypothetical", r"unclear", r"not yet tested",
    r"remains to be seen", r"speculative", r"unknown whether",
    r"has not been", r"hasn't been", r"unvalidated",
]


def score_signal_strength_v2(description: str, evidence_snippet: str | None) -> str:
    """Structural signal strength scoring based on evidence quality, not writing style."""
    desc_lower = description.lower()
    snippet = (evidence_snippet or "").lower()
    combined = desc_lower + " " + snippet

    has_percentage = bool(PERCENTAGE_RE.search(combined))
    has_benchmark = bool(NAMED_BENCHMARKS.search(combined))
    has_numbers = bool(MULTI_DIGIT_RE.search(combined))
    has_comparison = bool(COMPARISON_RE.search(combined))
    snippet_length = len(evidence_snippet or "")

    speculative_hits = sum(1 for p in SPECULATIVE_MARKERS if re.search(p, desc_lower))

    # Grounded: has percentage OR named benchmark, AND evidence snippet > 100 chars
    if (has_percentage or has_benchmark) and snippet_length > 100:
        return "grounded"

    # Also grounded: has percentage + comparison (strong quantitative evidence)
    if has_percentage and has_comparison:
        return "grounded"

    # Also grounded: has benchmark reference + numbers
    if has_benchmark and has_numbers:
        return "grounded"

    # Speculative: no numbers, no benchmark, AND matches speculative markers
    if not has_numbers and not has_benchmark and not has_percentage and speculative_hits >= 1:
        return "speculative"

    # Speculative: 2+ speculative markers even with some numbers
    if speculative_hits >= 2 and not has_benchmark and not has_percentage:
        return "speculative"

    return "moderate"


# ---------------------------------------------------------------------------
# Fix 5: Speculative-in-significant hedging patterns
# (subset of DOWNGRADE_TO_MINOR, but applied as direct SQL-equivalent)
# ---------------------------------------------------------------------------
HEDGING_PATTERNS = [
    r"remains to be seen",
    r"further research (?:is )?needed",
    r"it is unclear whether",
    r"has not been tested",
    r"not yet been",
    r"hasn't been tested",
]


# ---------------------------------------------------------------------------
# Restore: Quantitative markers for rescuing over-pruned limitations
# ---------------------------------------------------------------------------
def has_quantitative_evidence(description: str) -> bool:
    """Check if a pruned limitation contains quantitative evidence worth keeping."""
    return bool(
        PERCENTAGE_RE.search(description)
        or NAMED_BENCHMARKS.search(description)
        or re.search(r"\b\d+\.?\d*x\b", description)  # multipliers like "10x"
        or re.search(r"\b\d+\s*(?:emails?|hours?|days?|GB|MB|TB|ms|seconds?)/", description)
    )


# ---------------------------------------------------------------------------
# Main execution
# ---------------------------------------------------------------------------
def run_fix1_reclassify_types(conn, dry_run: bool) -> dict:
    """Fix 1: Reclassify unknown types with expanded patterns."""
    rows = conn.execute(
        "SELECT id, description FROM limitations WHERE limitation_type = 'unknown'"
    ).fetchall()

    reclassified = 0
    type_counts: dict[str, int] = defaultdict(int)

    for row in rows:
        new_type = classify_type(row["description"])
        if new_type:
            type_counts[new_type] += 1
            if not dry_run:
                conn.execute(
                    "UPDATE limitations SET limitation_type = %s WHERE id = %s",
                    (new_type, row["id"]),
                )
            reclassified += 1

    remaining = len(rows) - reclassified
    logger.info("Fix 1: Reclassified %d/%d unknowns -> %s (%d still unknown)",
                reclassified, len(rows), dict(type_counts), remaining)
    return {"reclassified": reclassified, "remaining_unknown": remaining, "by_type": dict(type_counts)}


def run_fix2_severity_recalibration(conn, dry_run: bool) -> dict:
    """Fix 2: Recalibrate severity based on content analysis."""
    rows = conn.execute(
        """SELECT id, description, severity FROM limitations
           WHERE severity NOT IN ('pruned') AND severity IS NOT NULL"""
    ).fetchall()

    upgraded = 0
    downgraded = 0

    for row in rows:
        new_severity = recalibrate_severity(row["description"], row["severity"])
        if new_severity:
            if new_severity == "blocking":
                upgraded += 1
            else:
                downgraded += 1
            if not dry_run:
                conn.execute(
                    "UPDATE limitations SET severity = %s WHERE id = %s",
                    (new_severity, row["id"]),
                )

    logger.info("Fix 2: Severity recalibration: %d upgraded to blocking, %d downgraded to minor",
                upgraded, downgraded)
    return {"upgraded_to_blocking": upgraded, "downgraded_to_minor": downgraded}


def run_fix3_signal_strength(conn, dry_run: bool) -> dict:
    """Fix 3: Structural signal strength scoring."""
    rows = conn.execute(
        """SELECT id, description, evidence_sources, signal_strength
           FROM limitations WHERE severity != 'pruned'"""
    ).fetchall()

    counts = {"grounded": 0, "moderate": 0, "speculative": 0}
    changed = 0

    for row in rows:
        # Extract evidence snippet from evidence_sources jsonb
        evidence_snippet = ""
        ev = row.get("evidence_sources")
        if ev:
            if isinstance(ev, str):
                try:
                    ev = json.loads(ev)
                except (json.JSONDecodeError, TypeError):
                    ev = []
            if isinstance(ev, list):
                for src in ev:
                    if isinstance(src, dict):
                        evidence_snippet += " " + src.get("snippet", "")

        new_strength = score_signal_strength_v2(row["description"], evidence_snippet.strip())
        counts[new_strength] += 1

        if new_strength != row.get("signal_strength"):
            changed += 1
            if not dry_run:
                conn.execute(
                    "UPDATE limitations SET signal_strength = %s WHERE id = %s",
                    (new_strength, row["id"]),
                )

    logger.info("Fix 3: Signal strength rescored: %s (%d changed)", counts, changed)
    return {"distribution": counts, "changed": changed}


def run_fix4_theme_ratio_pruning(conn, dry_run: bool) -> dict:
    """Fix 4: Theme-aware ratio pruning for skewed themes."""
    # Calculate per-theme ratios
    theme_stats = conn.execute("""
        SELECT
            t.id AS theme_id,
            t.name AS theme_name,
            COALESCE(cap.cnt, 0) AS cap_count,
            COALESCE(lim.cnt, 0) AS lim_count
        FROM themes t
        LEFT JOIN (
            SELECT theme_id, COUNT(*) AS cnt FROM capabilities GROUP BY theme_id
        ) cap ON cap.theme_id = t.id
        LEFT JOIN (
            SELECT theme_id, COUNT(*) AS cnt FROM limitations
            WHERE severity != 'pruned' GROUP BY theme_id
        ) lim ON lim.theme_id = t.id
        WHERE COALESCE(lim.cnt, 0) > 0
    """).fetchall()

    pruned = 0
    theme_pruned: dict[str, int] = {}

    for ts in theme_stats:
        cap_count = ts["cap_count"]
        lim_count = ts["lim_count"]
        if cap_count == 0:
            continue  # can't compute ratio

        ratio = lim_count / cap_count

        if ratio <= 2.0:
            continue  # preserve all

        if ratio > 8.0:
            # Only keep grounded limitations
            to_prune = conn.execute("""
                SELECT id FROM limitations
                WHERE theme_id = %s AND severity != 'pruned'
                  AND signal_strength != 'grounded'
            """, (ts["theme_id"],)).fetchall()
        elif ratio > 5.0:
            # Only keep grounded + blocking
            to_prune = conn.execute("""
                SELECT id FROM limitations
                WHERE theme_id = %s AND severity != 'pruned'
                  AND signal_strength != 'grounded'
                  AND severity != 'blocking'
            """, (ts["theme_id"],)).fetchall()
        else:
            continue

        if to_prune:
            theme_pruned[ts["theme_name"]] = len(to_prune)
            pruned += len(to_prune)
            if not dry_run:
                for row in to_prune:
                    conn.execute(
                        "UPDATE limitations SET severity = 'pruned' WHERE id = %s",
                        (row["id"],),
                    )

    logger.info("Fix 4: Theme-aware pruning: %d limitations across %d themes",
                pruned, len(theme_pruned))
    if theme_pruned:
        for name, cnt in sorted(theme_pruned.items(), key=lambda x: -x[1])[:10]:
            logger.info("  %s: %d pruned", name, cnt)
    return {"pruned": pruned, "themes_affected": len(theme_pruned), "by_theme": theme_pruned}


def run_fix5_hedging_downgrade(conn, dry_run: bool) -> dict:
    """Fix 5: Downgrade significant-severity limitations with hedging language."""
    # Build ILIKE conditions
    conditions = " OR ".join(f"description ILIKE '%{p}%'" for p in [
        "remains to be seen",
        "further research needed",
        "further research is needed",
        "it is unclear whether",
        "has not been tested",
        "not yet been achieved",
        "not yet been tested",
        "not yet been demonstrated",
        "not yet been validated",
    ])

    result = conn.execute(f"""
        SELECT COUNT(*) AS cnt FROM limitations
        WHERE severity = 'significant' AND ({conditions})
    """).fetchone()

    count = result["cnt"]

    if not dry_run and count > 0:
        conn.execute(f"""
            UPDATE limitations SET severity = 'minor'
            WHERE severity = 'significant' AND ({conditions})
        """)

    logger.info("Fix 5: Downgraded %d hedging limitations from significant -> minor", count)
    return {"downgraded": count}


def run_fix6_embedding_dedup(conn, dry_run: bool, batch_size: int = 50) -> dict:
    """Fix 6: Embedding-based semantic deduplication."""
    from reading_app.embeddings import embed_batch

    # Add embedding column if missing
    try:
        conn.execute(
            "ALTER TABLE limitations ADD COLUMN IF NOT EXISTS embedding VECTOR(768)"
        )
        conn.commit()
        logger.info("Fix 6: Added embedding column to limitations")
    except Exception:
        conn.rollback()

    # Get limitations that need embeddings
    rows = conn.execute("""
        SELECT id, description FROM limitations
        WHERE severity != 'pruned' AND embedding IS NULL
        ORDER BY id
    """).fetchall()

    logger.info("Fix 6: Computing embeddings for %d limitations", len(rows))

    embedded = 0
    for i in range(0, len(rows), batch_size):
        batch = rows[i:i + batch_size]
        texts = [r["description"] for r in batch]
        embeddings = embed_batch(texts)

        for row, emb in zip(batch, embeddings):
            if emb is not None:
                if not dry_run:
                    conn.execute(
                        "UPDATE limitations SET embedding = %s WHERE id = %s",
                        (str(emb), row["id"]),
                    )
                embedded += 1

        if not dry_run:
            conn.commit()

        if (i + batch_size) % 500 == 0 or i + batch_size >= len(rows):
            logger.info("  Embedded %d/%d", min(i + batch_size, len(rows)), len(rows))

    logger.info("Fix 6: Computed %d embeddings", embedded)

    # Now find semantic duplicates via cosine similarity
    # Create index if enough data
    try:
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_limitations_embedding
            ON limitations USING ivfflat (embedding vector_cosine_ops) WITH (lists = 50)
        """)
        conn.commit()
    except Exception:
        conn.rollback()
        logger.warning("Could not create ivfflat index (may need more data)")

    # Find duplicates: for each limitation, find nearest neighbor from different source
    dupes_found = 0
    dupes_pruned = 0

    # Get all active limitations with embeddings
    active = conn.execute("""
        SELECT id, description, confidence, evidence_sources, embedding IS NOT NULL AS has_emb
        FROM limitations
        WHERE severity != 'pruned' AND embedding IS NOT NULL
    """).fetchall()

    logger.info("Fix 6: Scanning %d embedded limitations for duplicates", len(active))

    # Process in chunks to avoid memory issues
    pruned_ids: set[str] = set()
    for row in active:
        if row["id"] in pruned_ids:
            continue

        # Get source IDs for this limitation
        ev = row.get("evidence_sources")
        if isinstance(ev, str):
            try:
                ev = json.loads(ev)
            except (json.JSONDecodeError, TypeError):
                ev = []
        source_ids = set()
        if isinstance(ev, list):
            for src in ev:
                if isinstance(src, dict) and "source_id" in src:
                    source_ids.add(src["source_id"])

        # Find nearest neighbors
        neighbors = conn.execute("""
            SELECT id, description, confidence, evidence_sources,
                   1 - (embedding <=> (SELECT embedding FROM limitations WHERE id = %s)) AS similarity
            FROM limitations
            WHERE id != %s AND severity != 'pruned' AND embedding IS NOT NULL
            ORDER BY embedding <=> (SELECT embedding FROM limitations WHERE id = %s)
            LIMIT 5
        """, (row["id"], row["id"], row["id"])).fetchall()

        for nb in neighbors:
            if nb["similarity"] < 0.90:
                break
            if nb["id"] in pruned_ids:
                continue

            # Check different source
            nb_ev = nb.get("evidence_sources")
            if isinstance(nb_ev, str):
                try:
                    nb_ev = json.loads(nb_ev)
                except (json.JSONDecodeError, TypeError):
                    nb_ev = []
            nb_sources = set()
            if isinstance(nb_ev, list):
                for src in nb_ev:
                    if isinstance(src, dict) and "source_id" in src:
                        nb_sources.add(src["source_id"])

            if source_ids & nb_sources:
                continue  # Same source, not cross-source duplicate

            dupes_found += 1

            # Keep higher confidence version
            row_conf = row.get("confidence") or 0
            nb_conf = nb.get("confidence") or 0
            loser_id = nb["id"] if row_conf >= nb_conf else row["id"]

            pruned_ids.add(loser_id)
            dupes_pruned += 1

            if not dry_run:
                conn.execute(
                    "UPDATE limitations SET severity = 'pruned' WHERE id = %s",
                    (loser_id,),
                )

            if loser_id == row["id"]:
                break  # Current row was the loser, stop checking its neighbors

    if not dry_run:
        conn.commit()

    logger.info("Fix 6: Found %d duplicate pairs, pruned %d", dupes_found, dupes_pruned)
    return {"embedded": embedded, "duplicate_pairs": dupes_found, "pruned": dupes_pruned}


def run_fix7_claim_linking(conn, dry_run: bool) -> dict:
    """Fix 7: Link limitations to their grounding claims via word overlap."""
    # Add column if missing
    try:
        conn.execute(
            "ALTER TABLE limitations ADD COLUMN IF NOT EXISTS grounding_claim_ids JSONB"
        )
        conn.commit()
        logger.info("Fix 7: Added grounding_claim_ids column")
    except Exception:
        conn.rollback()

    # Get limitations with their source IDs
    rows = conn.execute("""
        SELECT id, description, evidence_sources
        FROM limitations
        WHERE severity != 'pruned' AND grounding_claim_ids IS NULL
    """).fetchall()

    linked = 0
    total_links = 0

    for row in rows:
        ev = row.get("evidence_sources")
        if isinstance(ev, str):
            try:
                ev = json.loads(ev)
            except (json.JSONDecodeError, TypeError):
                ev = []

        source_ids = []
        snippets = []
        if isinstance(ev, list):
            for src in ev:
                if isinstance(src, dict):
                    if "source_id" in src:
                        source_ids.append(src["source_id"])
                    if "snippet" in src:
                        snippets.append(src["snippet"])

        if not source_ids:
            continue

        # Get claims from the same sources
        placeholders = ",".join(["%s"] * len(source_ids))
        claims = conn.execute(f"""
            SELECT id, claim_text, evidence_snippet
            FROM claims
            WHERE source_id IN ({placeholders})
        """, source_ids).fetchall()

        if not claims:
            continue

        # Score each claim by word overlap with limitation description + snippets
        lim_text = (row["description"] + " " + " ".join(snippets)).lower()
        lim_words = set(re.findall(r"\b\w{4,}\b", lim_text))  # words >= 4 chars

        if not lim_words:
            continue

        scored = []
        for c in claims:
            claim_text = ((c["claim_text"] or "") + " " + (c["evidence_snippet"] or "")).lower()
            claim_words = set(re.findall(r"\b\w{4,}\b", claim_text))
            if not claim_words:
                continue
            overlap = len(lim_words & claim_words) / len(lim_words | claim_words)
            if overlap > 0.15:  # minimum overlap threshold
                scored.append((c["id"], overlap))

        if not scored:
            continue

        # Keep top 3 claims
        scored.sort(key=lambda x: -x[1])
        claim_ids = [s[0] for s in scored[:3]]

        if not dry_run:
            conn.execute(
                "UPDATE limitations SET grounding_claim_ids = %s WHERE id = %s",
                (json.dumps(claim_ids), row["id"]),
            )

        linked += 1
        total_links += len(claim_ids)

    if not dry_run:
        conn.commit()

    logger.info("Fix 7: Linked %d limitations to %d grounding claims", linked, total_links)
    return {"limitations_linked": linked, "total_claim_links": total_links}


def run_restore_overpruned(conn, dry_run: bool) -> dict:
    """Restore over-pruned limitations that contain quantitative evidence."""
    rows = conn.execute("""
        SELECT id, description FROM limitations WHERE severity = 'pruned'
    """).fetchall()

    restored = 0
    for row in rows:
        if has_quantitative_evidence(row["description"]):
            restored += 1
            if not dry_run:
                conn.execute(
                    "UPDATE limitations SET severity = 'minor', signal_strength = 'moderate' WHERE id = %s",
                    (row["id"],),
                )

    if not dry_run:
        conn.commit()

    logger.info("Restore: Recovered %d over-pruned quantitative limitations", restored)
    return {"restored": restored}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Limitation quality v2 pass")
    parser.add_argument("--dry-run", action="store_true", help="Print changes without applying")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--skip-embeddings", action="store_true",
                        help="Skip fix 6 (embedding-based dedup)")
    parser.add_argument("--only", type=int, choices=range(0, 8),
                        help="Run only a specific step (0=restore, 1-7=fixes)")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    from reading_app.config import Config
    from reading_app.db import init_pool, get_conn

    config = Config()
    init_pool(config.postgres_dsn)

    results = {}

    with get_conn() as conn:
        # Pre-state
        caps = conn.execute("SELECT COUNT(*) AS c FROM capabilities").fetchone()["c"]
        active_lims = conn.execute(
            "SELECT COUNT(*) AS c FROM limitations WHERE severity != 'pruned'"
        ).fetchone()["c"]
        unknowns = conn.execute(
            "SELECT COUNT(*) AS c FROM limitations WHERE limitation_type = 'unknown'"
        ).fetchone()["c"]
        logger.info("Before: %d caps, %d active lims (%.2f:1), %d unknown type",
                     caps, active_lims, active_lims / caps if caps else 0, unknowns)

        steps = {
            0: ("Restore over-pruned", run_restore_overpruned),
            1: ("Reclassify types", run_fix1_reclassify_types),
            2: ("Severity recalibration", run_fix2_severity_recalibration),
            3: ("Signal strength scoring", run_fix3_signal_strength),
            4: ("Theme-aware ratio pruning", run_fix4_theme_ratio_pruning),
            5: ("Hedging downgrade", run_fix5_hedging_downgrade),
            6: ("Embedding dedup", run_fix6_embedding_dedup),
            7: ("Claim linking", run_fix7_claim_linking),
        }

        for step_num, (name, func) in steps.items():
            if args.only is not None and args.only != step_num:
                continue
            if step_num == 6 and args.skip_embeddings:
                logger.info("Skipping fix 6 (embedding dedup) -- use --only 6 to run separately")
                continue

            logger.info("=" * 60)
            logger.info("Step %d: %s", step_num, name)
            logger.info("=" * 60)

            try:
                results[name] = func(conn, args.dry_run)
            except Exception:
                logger.exception("Step %d failed", step_num)
                conn.rollback()
                results[name] = {"error": True}

        if not args.dry_run:
            conn.commit()

        # Post-state
        active_after = conn.execute(
            "SELECT COUNT(*) AS c FROM limitations WHERE severity != 'pruned'"
        ).fetchone()["c"]
        unknowns_after = conn.execute(
            "SELECT COUNT(*) AS c FROM limitations WHERE limitation_type = 'unknown'"
        ).fetchone()["c"]

    print("\n" + "=" * 60)
    print("LIMITATION QUALITY V2 COMPLETE")
    print("=" * 60)
    print(f"  Before: {active_lims} active lims ({active_lims/caps:.2f}:1), {unknowns} unknown type")
    print(f"  After:  {active_after} active lims ({active_after/caps:.2f}:1), {unknowns_after} unknown type")
    print()

    for name, res in results.items():
        print(f"  [{name}]")
        for k, v in res.items():
            if isinstance(v, dict) and len(v) > 5:
                print(f"    {k}: ({len(v)} entries)")
            else:
                print(f"    {k}: {v}")

    if args.dry_run:
        print("\n  [DRY RUN - no changes applied]")


if __name__ == "__main__":
    main()

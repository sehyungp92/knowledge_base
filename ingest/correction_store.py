"""Correction examples store for extraction learning loop.

Persists user corrections from /enrich and /challenge, and retrieves
them as few-shot examples for injection into extraction prompts.
"""

from __future__ import annotations

import json
import logging

from reading_app.db import get_conn

logger = logging.getLogger(__name__)


def store_correction(
    extraction_type: str,
    correction_type: str,
    original_value: dict | None,
    corrected_value: dict | None,
    source_context: str = "",
    source_id: str | None = None,
    theme_id: str | None = None,
    skill_origin: str = "enrich",
) -> None:
    """Persist a correction example."""
    try:
        with get_conn() as conn:
            conn.execute(
                """INSERT INTO correction_examples
                   (extraction_type, correction_type, original_value, corrected_value,
                    source_context, source_id, theme_id, skill_origin)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    extraction_type,
                    correction_type,
                    json.dumps(original_value) if original_value else None,
                    json.dumps(corrected_value) if corrected_value else None,
                    source_context[:500] if source_context else "",
                    source_id,
                    theme_id,
                    skill_origin,
                ),
            )
            conn.commit()
    except Exception:
        logger.debug("Failed to store correction example", exc_info=True)


def get_few_shot_examples(
    extraction_type: str,
    limit: int = 3,
    theme_id: str | None = None,
) -> list[dict]:
    """Get recent corrections for few-shot injection.

    Prioritizes same-theme corrections, then falls back to recent global ones.
    """
    try:
        with get_conn() as conn:
            if theme_id:
                # Try same-theme first
                rows = conn.execute(
                    """SELECT extraction_type, correction_type, original_value, corrected_value
                       FROM correction_examples
                       WHERE extraction_type = %s AND theme_id = %s
                       ORDER BY created_at DESC LIMIT %s""",
                    (extraction_type, theme_id, limit),
                ).fetchall()
                if rows:
                    return [dict(r) for r in rows]

            # Fall back to most recent global
            rows = conn.execute(
                """SELECT extraction_type, correction_type, original_value, corrected_value
                   FROM correction_examples
                   WHERE extraction_type = %s
                   ORDER BY created_at DESC LIMIT %s""",
                (extraction_type, limit),
            ).fetchall()
            return [dict(r) for r in rows]
    except Exception:
        logger.debug("Failed to get few-shot examples", exc_info=True)
        return []


def format_few_shot_block(examples: list[dict]) -> str:
    """Format corrections as a prompt block for injection into extraction prompts.

    Returns empty string if no examples.
    """
    if not examples:
        return ""

    lines = [
        "\n## Calibration from past corrections",
        "These are examples of corrections users made to previous extractions. Use them to calibrate:",
    ]

    for ex in examples:
        ctype = ex.get("correction_type", "?")
        etype = ex.get("extraction_type", "?")
        corrected = ex.get("corrected_value")
        original = ex.get("original_value")

        if ctype == "missed" and corrected:
            desc = corrected.get("description", "?") if isinstance(corrected, dict) else str(corrected)
            extra = ""
            if isinstance(corrected, dict):
                if corrected.get("limitation_type"):
                    extra = f" (type: {corrected['limitation_type']}"
                    if corrected.get("severity"):
                        extra += f", severity: {corrected['severity']}"
                    extra += ")"
                elif corrected.get("maturity"):
                    extra = f" (maturity: {corrected['maturity']})"
            lines.append(f"- MISSED {etype}: \"{desc[:150]}\"{extra}")

        elif ctype == "spurious" and original:
            desc = original.get("description", "?") if isinstance(original, dict) else str(original)
            lines.append(f"- SPURIOUS {etype} rejected: \"{desc[:150]}\" — be more specific")

        elif ctype == "reclassified" and original and corrected:
            field = original.get("field", "?") if isinstance(original, dict) else "?"
            old_val = original.get("value", "?") if isinstance(original, dict) else str(original)
            new_val = corrected.get("value", "?") if isinstance(corrected, dict) else str(corrected)
            lines.append(f"- RECLASSIFIED {etype} {field}: was \"{old_val[:60]}\" → should be \"{new_val[:60]}\"")

    if len(lines) <= 2:
        return ""

    lines.append("")
    return "\n".join(lines)

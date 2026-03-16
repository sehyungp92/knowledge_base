"""Shared theme_id validation utilities.

Three modules independently validate theme_ids against the DB.
This centralizes the logic: load valid IDs, resolve with parent
fallback, and filter entity lists.
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def load_valid_theme_ids(get_conn_fn) -> set[str] | None:
    """Load all theme IDs from DB. Returns None if DB unavailable.

    Robust to mocked DB connections — returns None if the data doesn't
    look like real theme rows (prevents MagicMock objects in the set).
    """
    if get_conn_fn is None:
        return None
    try:
        with get_conn_fn() as conn:
            rows = conn.execute("SELECT id FROM themes").fetchall()
            if rows and isinstance(rows, list):
                ids = set()
                for r in rows:
                    tid = r["id"] if isinstance(r, dict) else r[0]
                    if isinstance(tid, str):
                        ids.add(tid)
                    else:
                        # Non-string IDs mean mocked/invalid data — skip validation
                        return None
                return ids if ids else None
    except Exception:
        logger.debug("Failed to load theme IDs from DB", exc_info=True)
    return None


def resolve_theme_id(theme_id: str, valid_themes: set[str] | None) -> str | None:
    """Resolve a theme_id to a valid one. Tries exact match, then parent path.

    Returns None if unresolvable (caller should skip the entity).
    """
    if valid_themes is None:
        return theme_id  # can't validate, pass through
    if theme_id in valid_themes:
        return theme_id
    # Try parent: "autonomous_agents/computer_use_agents" -> "autonomous_agents"
    parent = theme_id.rsplit("/", 1)[0] if "/" in theme_id else None
    if parent and parent in valid_themes:
        logger.debug("Remapped theme_id %s -> %s (parent fallback)", theme_id, parent)
        return parent
    logger.warning("Dropping entity with unknown theme_id: %s", theme_id)
    return None


def validate_theme_ids_in_entities(
    entities: list[dict], valid_themes: set[str] | None
) -> list[dict]:
    """Filter entities to only those with valid theme_ids.

    Remaps to parent when possible. Mutates theme_id in-place for
    remapped entities. Returns filtered list.
    """
    if valid_themes is None:
        return entities

    result = []
    for entity in entities:
        tid = entity.get("theme_id", "")
        resolved = resolve_theme_id(tid, valid_themes)
        if resolved is not None:
            entity["theme_id"] = resolved
            result.append(entity)
    return result

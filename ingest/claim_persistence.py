"""Persist extracted claims and concepts to the PostgreSQL database.

Moved from scripts.bulk_ingest to avoid cross-layer imports in the
save pipeline (ingest/ importing from scripts/).
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def persist_extractions_to_db(
    source_id: str,
    extractions: dict,
) -> int:
    """Persist extracted claims and concepts to the database.

    Returns number of claims persisted.
    """
    from ulid import ULID
    from reading_app.db import insert_claim, get_or_create_concept, insert_source_concept
    from reading_app.embeddings import embed_batch

    claims = extractions.get("claims", [])
    if not claims:
        logger.debug("No claims to persist for %s", source_id)
        return 0

    # Batch-embed all claim texts in a single API call
    claim_texts = [c.get("claim_text", "") for c in claims]
    embeddings = embed_batch(claim_texts) if claim_texts else []
    if len(embeddings) != len(claims):
        logger.error(
            "Embedding count mismatch for %s: %d claims but %d embeddings",
            source_id, len(claims), len(embeddings),
        )
        return 0

    claims_count = 0
    for claim, embedding in zip(claims, embeddings):
        try:
            claim_id = f"claim_{ULID()}"
            insert_claim(
                id=claim_id,
                source_id=source_id,
                claim_text=claim.get("claim_text", ""),
                claim_type=claim.get("claim_type"),
                section=claim.get("section"),
                confidence=claim.get("confidence"),
                evidence_snippet=claim.get("evidence_snippet"),
                evidence_location=claim.get("evidence_location"),
                evidence_type=claim.get("evidence_type"),
                embedding=embedding,
                temporal_scope=claim.get("temporal_scope"),
            )
            claims_count += 1
        except Exception:
            logger.warning(
                "Failed to persist claim for %s: %s",
                source_id, claim.get("claim_text", "")[:50],
            )

    logger.info("Claims persisted for %s: %d/%d", source_id, claims_count, len(claims))

    for concept in extractions.get("concepts", []):
        try:
            concept_id = get_or_create_concept(
                canonical_name=concept.get("canonical_name", ""),
                concept_type=concept.get("concept_type"),
                description=concept.get("description"),
                aliases=concept.get("aliases"),
            )
            insert_source_concept(source_id, concept_id, relationship="discusses")
        except Exception:
            logger.debug("Failed to persist concept: %s", concept.get("canonical_name", "")[:50], exc_info=True)

    return claims_count

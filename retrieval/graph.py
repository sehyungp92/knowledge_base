"""Graph-Lite retrieval: 1-hop, 2-hop, path explanation, contradictions."""

from __future__ import annotations

import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class GraphRetriever:
    """Postgres-based graph queries for the knowledge graph."""

    def __init__(self, get_conn_fn):
        """Args: get_conn_fn — callable returning a context manager yielding a DB connection."""
        self._get_conn = get_conn_fn

    def one_hop(self, source_id: str) -> list[dict]:
        """Find sources directly connected to a source (bidirectional)."""
        with self._get_conn() as conn:
            rows = conn.execute("""
                SELECT se.source_b AS connected_id, s.title, se.edge_type,
                       se.explanation, se.confidence
                FROM source_edges se
                JOIN sources s ON se.source_b = s.id
                WHERE se.source_a = %s
                UNION
                SELECT se.source_a AS connected_id, s.title, se.edge_type,
                       se.explanation, se.confidence
                FROM source_edges se
                JOIN sources s ON se.source_a = s.id
                WHERE se.source_b = %s
            """, (source_id, source_id)).fetchall()
        return rows

    def two_hop_via_concepts(self, source_id: str, min_overlap: int = 2) -> list[dict]:
        """Find sources connected via shared concepts."""
        with self._get_conn() as conn:
            rows = conn.execute("""
                SELECT DISTINCT s2.id, s2.title,
                       array_agg(DISTINCT c.canonical_name) AS shared_concepts,
                       COUNT(DISTINCT c.id) AS overlap_count
                FROM source_concepts sc1
                JOIN source_concepts sc2 ON sc1.concept_id = sc2.concept_id
                JOIN concepts c ON sc1.concept_id = c.id
                JOIN sources s2 ON sc2.source_id = s2.id
                WHERE sc1.source_id = %s
                  AND sc2.source_id != %s
                GROUP BY s2.id, s2.title
                HAVING COUNT(DISTINCT c.id) >= %s
                ORDER BY overlap_count DESC
            """, (source_id, source_id, min_overlap)).fetchall()
        return rows

    def explain_path(self, source_a: str, source_b: str, max_hops: int = 3) -> list[dict]:
        """Find and explain paths between two sources using recursive CTE."""
        with self._get_conn() as conn:
            rows = conn.execute("""
                WITH RECURSIVE paths AS (
                    -- Base: direct edges from source_a
                    SELECT source_a AS start_node, source_b AS end_node,
                           edge_type, explanation, confidence,
                           ARRAY[source_a, source_b] AS path,
                           1 AS depth
                    FROM source_edges
                    WHERE source_a = %s
                    UNION ALL
                    SELECT source_a AS start_node, source_b AS end_node,
                           edge_type, explanation, confidence,
                           ARRAY[source_b, source_a] AS path,
                           1 AS depth
                    FROM source_edges
                    WHERE source_b = %s

                    UNION ALL

                    -- Recursive: extend paths
                    SELECT p.start_node, se.source_b AS end_node,
                           se.edge_type, se.explanation, se.confidence,
                           p.path || se.source_b,
                           p.depth + 1
                    FROM paths p
                    JOIN source_edges se ON p.end_node = se.source_a
                    WHERE p.depth < %s
                      AND NOT se.source_b = ANY(p.path)
                )
                SELECT path, depth
                FROM paths
                WHERE end_node = %s
                ORDER BY depth ASC
                LIMIT 5
            """, (source_a, source_a, max_hops, source_b)).fetchall()
        return rows

    def find_contradictions(self, topic: str | None = None, threshold: float = 0.85) -> list[dict]:
        """Find potentially contradicting claims via high embedding similarity across sources.

        Returns temporal metadata (source dates) so callers can assess whether
        a disagreement is narrowing or widening over time.
        """
        if not topic:
            return []

        with self._get_conn() as conn:
            try:
                rows = conn.execute("""
                    SELECT c1.id AS claim_a_id, c1.claim_text AS claim_a_text,
                           c1.source_id AS source_a_id,
                           s1.published_at AS source_a_date,
                           s1.title AS source_a_title,
                           c2.id AS claim_b_id, c2.claim_text AS claim_b_text,
                           c2.source_id AS source_b_id,
                           s2.published_at AS source_b_date,
                           s2.title AS source_b_title,
                           1 - (c1.embedding <=> c2.embedding) AS similarity
                    FROM claims c1
                    JOIN claims c2 ON c1.id < c2.id
                    JOIN sources s1 ON c1.source_id = s1.id
                    JOIN sources s2 ON c2.source_id = s2.id
                    WHERE c1.embedding IS NOT NULL AND c2.embedding IS NOT NULL
                      AND c1.source_id != c2.source_id
                      AND (c1.claim_text ILIKE %s OR c2.claim_text ILIKE %s)
                      AND 1 - (c1.embedding <=> c2.embedding) > %s
                    ORDER BY similarity DESC
                    LIMIT 20
                """, (f"%{topic}%", f"%{topic}%", threshold)).fetchall()
                return rows
            except Exception:
                logger.debug("Embedding-based contradiction search failed", exc_info=True)
                return []

    def get_source_implications(self, source_id: str) -> list[dict]:
        """Get cross-theme implications related to a source's themes."""
        with self._get_conn() as conn:
            rows = conn.execute("""
                SELECT cti.*, t1.name AS source_theme_name, t2.name AS target_theme_name
                FROM cross_theme_implications cti
                JOIN themes t1 ON cti.source_theme_id = t1.id
                JOIN themes t2 ON cti.target_theme_id = t2.id
                JOIN source_themes st ON st.theme_id = cti.source_theme_id
                WHERE st.source_id = %s
                ORDER BY cti.confidence DESC
            """, (source_id,)).fetchall()
        return rows

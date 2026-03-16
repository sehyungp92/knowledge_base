"""Graph algorithms module: runs NetworkX algorithms on Postgres edge tables
and materializes results to a graph_metrics table."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

try:
    import networkx as nx
except ImportError:
    nx = None
    logger.warning("networkx not installed — graph algorithm methods will return empty results")

try:
    import community.community_louvain as community_louvain
except ImportError:
    community_louvain = None
    logger.warning("python-louvain not installed — community detection will return empty results")


class KnowledgeGraphAnalyzer:
    """Runs graph algorithms on the knowledge graph and materializes metrics."""

    def __init__(self, get_conn_fn):
        """Args: get_conn_fn — callable returning a context manager yielding a DB connection."""
        self._get_conn = get_conn_fn

    # ------------------------------------------------------------------
    # Graph builders
    # ------------------------------------------------------------------

    def _build_source_graph(self) -> "nx.Graph | None":
        """Build an undirected graph from source_edges."""
        if nx is None:
            return None
        with self._get_conn() as conn:
            rows = conn.execute(
                "SELECT source_a, source_b, edge_type, confidence FROM source_edges"
            ).fetchall()
        G = nx.Graph()
        for r in rows:
            G.add_edge(
                r["source_a"],
                r["source_b"],
                edge_type=r["edge_type"],
                confidence=r["confidence"],
            )
        return G

    def _build_directed_source_graph(self) -> "nx.DiGraph | None":
        """Build a directed graph from source_edges."""
        if nx is None:
            return None
        with self._get_conn() as conn:
            rows = conn.execute(
                "SELECT source_a, source_b, edge_type, confidence FROM source_edges"
            ).fetchall()
        G = nx.DiGraph()
        for r in rows:
            G.add_edge(
                r["source_a"],
                r["source_b"],
                edge_type=r["edge_type"],
                confidence=r["confidence"],
            )
        return G

    def _build_concept_cooccurrence_graph(self) -> "nx.Graph | None":
        """Build an undirected graph where concepts are connected if they
        co-occur in the same source."""
        if nx is None:
            return None
        with self._get_conn() as conn:
            rows = conn.execute(
                "SELECT source_id, concept_id FROM source_concepts"
            ).fetchall()

        # Group concepts by source
        source_concepts: dict[str, list[str]] = {}
        for r in rows:
            source_concepts.setdefault(r["source_id"], []).append(r["concept_id"])

        G = nx.Graph()
        for concepts in source_concepts.values():
            for i in range(len(concepts)):
                for j in range(i + 1, len(concepts)):
                    if G.has_edge(concepts[i], concepts[j]):
                        G[concepts[i]][concepts[j]]["weight"] += 1
                    else:
                        G.add_edge(concepts[i], concepts[j], weight=1)
        return G

    # ------------------------------------------------------------------
    # Compute methods
    # ------------------------------------------------------------------

    def compute_pagerank(self, alpha: float = 0.85) -> list[dict]:
        """PageRank on directed source graph."""
        if nx is None:
            return []
        G = self._build_directed_source_graph()
        if G is None or G.number_of_nodes() == 0:
            return []

        scores = nx.pagerank(G, alpha=alpha)
        results = []
        for node, score in scores.items():
            results.append(
                {
                    "metric_type": "pagerank",
                    "entity_type": "source",
                    "entity_id": str(node),
                    "score": score,
                    "metadata": {"alpha": alpha},
                }
            )
        return results

    def compute_communities(self) -> list[dict]:
        """Louvain community detection on undirected source graph."""
        if nx is None or community_louvain is None:
            return []
        G = self._build_source_graph()
        if G is None or G.number_of_nodes() == 0:
            return []

        partition = community_louvain.best_partition(G)
        results = []
        for node, comm_id in partition.items():
            results.append(
                {
                    "metric_type": "community",
                    "entity_type": "source",
                    "entity_id": str(node),
                    "score": float(comm_id),
                    "metadata": {"community_id": comm_id},
                }
            )
        return results

    def compute_betweenness(self) -> list[dict]:
        """Betweenness centrality on concept co-occurrence graph.
        Only returns nodes with score > 0."""
        if nx is None:
            return []
        G = self._build_concept_cooccurrence_graph()
        if G is None or G.number_of_nodes() == 0:
            return []

        # Use approximate betweenness for large graphs (exact is O(V*E))
        if G.number_of_nodes() > 1000:
            logger.info("Using approximate betweenness (k=200) for %d-node graph", G.number_of_nodes())
            scores = nx.betweenness_centrality(G, k=min(200, G.number_of_nodes()))
        else:
            scores = nx.betweenness_centrality(G)
        results = []
        for node, score in scores.items():
            if score > 0:
                results.append(
                    {
                        "metric_type": "betweenness",
                        "entity_type": "concept",
                        "entity_id": str(node),
                        "score": score,
                        "metadata": {},
                    }
                )
        return results

    def compute_theme_influence(self) -> list[dict]:
        """PageRank on theme DAG (theme_edges + cross_theme_implications)."""
        if nx is None:
            return []

        with self._get_conn() as conn:
            theme_rows = conn.execute(
                "SELECT parent_id, child_id, strength FROM theme_edges"
            ).fetchall()
            impl_rows = conn.execute(
                """SELECT source_theme_id, target_theme_id, MAX(confidence) AS confidence
                   FROM cross_theme_implications
                   GROUP BY source_theme_id, target_theme_id"""
            ).fetchall()

        G = nx.DiGraph()
        for r in theme_rows:
            G.add_edge(r["parent_id"], r["child_id"], weight=r["strength"])
        for r in impl_rows:
            G.add_edge(
                r["source_theme_id"],
                r["target_theme_id"],
                weight=r["confidence"],
            )

        if G.number_of_nodes() == 0:
            return []

        scores = nx.pagerank(G, max_iter=200, tol=1e-3)
        results = []
        for node, score in scores.items():
            results.append(
                {
                    "metric_type": "theme_influence",
                    "entity_type": "theme",
                    "entity_id": str(node),
                    "score": score,
                    "metadata": {},
                }
            )
        return results

    # ------------------------------------------------------------------
    # Materialization
    # ------------------------------------------------------------------

    def materialize(self) -> dict:
        """Run all compute methods and upsert results into graph_metrics.

        Returns a summary dict with counts per metric type and any errors.
        """
        all_results: list[dict] = []
        errors: list[str] = []

        for method_name in (
            "compute_pagerank",
            "compute_communities",
            "compute_betweenness",
            "compute_theme_influence",
        ):
            try:
                results = getattr(self, method_name)()
                all_results.extend(results)
            except Exception:
                logger.exception("Failed to run %s", method_name)
                errors.append(method_name)

        if all_results:
            now = datetime.now(timezone.utc)
            with self._get_conn() as conn:
                for r in all_results:
                    conn.execute(
                        """
                        INSERT INTO graph_metrics
                            (metric_type, entity_type, entity_id, score, metadata, computed_at)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (metric_type, entity_type, entity_id)
                        DO UPDATE SET score = EXCLUDED.score,
                                      metadata = EXCLUDED.metadata,
                                      computed_at = EXCLUDED.computed_at
                        """,
                        (
                            r["metric_type"],
                            r["entity_type"],
                            r["entity_id"],
                            r["score"],
                            json.dumps(r["metadata"]),
                            now,
                        ),
                    )

        summary: dict[str, int] = {}
        for r in all_results:
            summary[r["metric_type"]] = summary.get(r["metric_type"], 0) + 1

        return {"counts": summary, "errors": errors}

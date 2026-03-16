"""Compute and materialize graph metrics (PageRank, communities, betweenness, theme influence).

Must run AFTER compute_edges.py so edges exist for the algorithms.

Usage:
    python -m scripts.compute_graph_metrics
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    from reading_app.config import Config
    from reading_app.db import init_pool, get_conn

    config = Config()
    init_pool(config.postgres_dsn)

    from retrieval.graph_algorithms import KnowledgeGraphAnalyzer

    logger.info("Materializing graph metrics...")
    analyzer = KnowledgeGraphAnalyzer(get_conn)
    result = analyzer.materialize()

    logger.info("Graph metrics complete: %s", result)
    if result.get("errors"):
        logger.warning("Errors during computation: %s", result["errors"])

    # Print summary
    counts = result.get("counts", {})
    print("\n=== Graph Metrics Summary ===")
    for metric_type, count in sorted(counts.items()):
        print(f"  {metric_type}: {count} entries")
    print()


if __name__ == "__main__":
    main()

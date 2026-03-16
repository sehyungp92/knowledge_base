"""Delete a source and all its dependent data from the knowledge base.

Usage:
    python -m scripts.delete_source <source_id>
    python -m scripts.delete_source <url>
    python -m scripts.delete_source <source_id> --yes

Resolves the target by source ID first, then by URL lookup.
Shows source details and prompts for confirmation before deleting.
Use --yes / -y to skip the confirmation prompt.
"""

from __future__ import annotations

import argparse
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def resolve_source(identifier: str) -> dict | None:
    """Look up a source by ID or URL."""
    from reading_app.db import get_conn

    with get_conn() as conn:
        # Try by ID first
        row = conn.execute(
            "SELECT * FROM sources WHERE id = %s", (identifier,)
        ).fetchone()
        if row:
            return row

        # Try by exact URL
        row = conn.execute(
            "SELECT * FROM sources WHERE url = %s", (identifier,)
        ).fetchone()
        if row:
            return row

        # Try URL substring match (for partial URLs)
        row = conn.execute(
            "SELECT * FROM sources WHERE url LIKE %s LIMIT 1",
            (f"%{identifier}%",),
        ).fetchone()
        return row


def main():
    parser = argparse.ArgumentParser(description="Delete a source from the knowledge base")
    parser.add_argument("identifier", help="Source ID (ULID) or URL to delete")
    parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation prompt")
    args = parser.parse_args()

    # Init DB
    from reading_app.db import ensure_pool
    ensure_pool()

    # Resolve source
    source = resolve_source(args.identifier)
    if not source:
        print(f"No source found matching: {args.identifier}")
        sys.exit(1)

    source_id = source["id"]
    title = source.get("title", "(untitled)")
    url = source.get("url", "(no url)")
    status = source.get("processing_status", "unknown")

    print(f"\nSource to delete:")
    print(f"  ID:     {source_id}")
    print(f"  Title:  {title}")
    print(f"  URL:    {url}")
    print(f"  Status: {status}")
    print()

    if not args.yes:
        confirm = input("Delete this source and ALL dependent data? [y/N] ").strip().lower()
        if confirm not in ("y", "yes"):
            print("Aborted.")
            sys.exit(0)

    # Perform deletion
    from reading_app.db import delete_source
    summary = delete_source(source_id)

    # Print results
    print(f"\nDeleted: {title}")
    print(f"{'='*50}")
    for table, count in sorted(summary.items()):
        if count > 0:
            print(f"  {table:.<35} {count}")
    total = sum(summary.values())
    print(f"  {'total':.<35} {total}")
    print()


if __name__ == "__main__":
    main()

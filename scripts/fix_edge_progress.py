"""
Separate edge_progress.json completed_pairs into confirmed (in DB) vs unconfirmed.

- Loads edge_progress.json
- Queries source_edges table for all distinct (source_a, source_b) pairs
- Splits completed_pairs into:
    completed_pairs = only pairs confirmed in DB
    failed_pairs = all unconfirmed pairs (no-relationship + actual failures)
- Resets failed=0, skipped=0 counters
- Backs up original file first

Usage:
    python -m scripts.fix_edge_progress
"""

import json
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROGRESS_FILE = PROJECT_ROOT / "scripts" / "edge_progress.json"
BACKUP_FILE = PROJECT_ROOT / "scripts" / "edge_progress.json.bak"


def main():
    from reading_app.config import Config
    from reading_app.db import init_pool, get_conn

    # 1. Backup
    print(f"Backing up {PROGRESS_FILE} -> {BACKUP_FILE}")
    shutil.copy2(PROGRESS_FILE, BACKUP_FILE)

    # 2. Load progress file
    with open(PROGRESS_FILE, "r") as f:
        data = json.load(f)

    completed_pairs = data["completed_pairs"]
    print(f"Total completed_pairs in file: {len(completed_pairs)}")

    # 3. Connect to DB and get all edge pairs
    cfg = Config()
    init_pool(cfg.postgres_dsn)

    with get_conn() as conn:
        rows = conn.execute(
            "SELECT DISTINCT source_a, source_b FROM source_edges"
        ).fetchall()

    db_pairs = set()
    for row in rows:
        # Normalize: always store as sorted tuple so order doesn't matter
        a, b = row["source_a"], row["source_b"]
        pair = tuple(sorted([a, b]))
        db_pairs.add(pair)

    print(f"Distinct source pairs with edges in DB: {len(db_pairs)}")

    # 4. Split completed_pairs
    confirmed = []
    unconfirmed = []

    for pair in completed_pairs:
        normalized = tuple(sorted(pair))
        if normalized in db_pairs:
            confirmed.append(pair)
        else:
            unconfirmed.append(pair)

    print(f"Confirmed (have edges in DB): {len(confirmed)}")
    print(f"Unconfirmed (no edges / failed): {len(unconfirmed)}")

    # Check: are there DB pairs NOT in completed_pairs?
    completed_set = set(tuple(sorted(p)) for p in completed_pairs)
    db_not_in_completed = db_pairs - completed_set
    if db_not_in_completed:
        print(f"WARNING: {len(db_not_in_completed)} DB pairs not in completed_pairs!")
    else:
        print("All DB pairs are accounted for in completed_pairs.")

    # 5. Update the progress data
    data["completed_pairs"] = confirmed
    data["failed_pairs"] = unconfirmed
    data["edges_created"] = len(confirmed)
    data["failed"] = 0
    data["skipped"] = 0

    # 6. Write updated file
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"\nUpdated {PROGRESS_FILE}:")
    print(f"  completed_pairs: {len(data['completed_pairs'])}")
    print(f"  failed_pairs: {len(data['failed_pairs'])}")
    print(f"  edges_created: {data['edges_created']}")
    print(f"  failed: {data['failed']}")
    print(f"  skipped: {data['skipped']}")


if __name__ == "__main__":
    main()

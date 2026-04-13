#!/bin/bash
# bootstrap_scheduler.sh
# Waits until 05:00 GMT, then resumes source bootstrap.
# Safe due to idempotent skip logic — already-created pages are skipped.

set -e

PROJECT_DIR="/c/Users/sehyu/Documents/Other/Projects/knowledge_base"
PYTHON="$PROJECT_DIR/venv/Scripts/python"
LOG_FILE="$PROJECT_DIR/scripts/bootstrap_scheduler.log"

cd "$PROJECT_DIR"
export PYTHONUTF8=1

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "Scheduler started. Sources so far: $(ls wiki/sources/*.md 2>/dev/null | wc -l)"

# ── Wait until 05:00 GMT ────────────────────────────────────────────
log "Waiting until 05:00 GMT to start bootstrap..."
while true; do
    current_hhmm=$(date -u +%H%M)
    if [ "$current_hhmm" -ge "0500" ]; then
        break
    fi
    sleep 30
done

log "05:00 reached. Starting bootstrap sources..."
log "Sources before start: $(ls wiki/sources/*.md 2>/dev/null | wc -l)"

"$PYTHON" scripts/bootstrap_wiki.py --sources-only >> "$LOG_FILE" 2>&1
FINAL_COUNT=$(ls wiki/sources/*.md 2>/dev/null | wc -l)
log "Bootstrap complete. Total source pages: $FINAL_COUNT"

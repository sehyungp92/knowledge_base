#!/bin/bash
set -e
PROJECT_DIR="/c/Users/sehyu/Documents/Other/Projects/knowledge_base"
PYTHON="$PROJECT_DIR/venv/Scripts/python"
LOG_FILE="$PROJECT_DIR/scripts/bootstrap_entities.log"
cd "$PROJECT_DIR"
export PYTHONUTF8=1

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"; }

log "Scheduler started. Waiting until 07:00 local time..."
log "Entities so far: $(ls wiki/entities/*.md 2>/dev/null | wc -l)"

while true; do
    current_hhmm=$(date +%H%M)
    if [ "$current_hhmm" -ge "0700" ]; then
        break
    fi
    sleep 30
done

log "07:00 reached. Resuming entity bootstrap..."
log "Entities before start: $(ls wiki/entities/*.md 2>/dev/null | wc -l)"

"$PYTHON" scripts/bootstrap_wiki.py --entities-only >> "$LOG_FILE" 2>&1
FINAL_COUNT=$(ls wiki/entities/*.md 2>/dev/null | wc -l)
log "Bootstrap complete. Total entity pages: $FINAL_COUNT"

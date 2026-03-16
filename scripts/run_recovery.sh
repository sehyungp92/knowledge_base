#!/usr/bin/env bash
# Full recovery pipeline — runs all reprocessing steps in order.
# Logs everything to scripts/run_recovery.log
# Run: bash scripts/run_recovery.sh

set -euo pipefail
LOG="scripts/run_recovery.log"
echo "=== Recovery pipeline started at $(date) ===" | tee -a "$LOG"

run_step() {
    local step="$1"
    shift
    echo "" | tee -a "$LOG"
    echo "=== Step: $step — $(date) ===" | tee -a "$LOG"
    python -m "$@" 2>&1 | tee -a "$LOG"
    echo "=== Step done: $step — $(date) ===" | tee -a "$LOG"
}

# Step 1: Themes first (provides context for everything else)
run_step "Themes" scripts.reprocess_failed --themes --delay 3

# Step 2: Claims and Summaries in parallel
echo "" | tee -a "$LOG"
echo "=== Step: Claims + Summaries (parallel) — $(date) ===" | tee -a "$LOG"
python -m scripts.reprocess_failed --claims --delay 3 2>&1 | tee -a "${LOG}.claims" &
PID_CLAIMS=$!
python -m scripts.reprocess_failed --summaries --delay 3 2>&1 | tee -a "${LOG}.summaries" &
PID_SUMMARIES=$!
CLAIMS_OK=0; wait $PID_CLAIMS || CLAIMS_OK=$?
SUMMARIES_OK=0; wait $PID_SUMMARIES || SUMMARIES_OK=$?
cat "${LOG}.claims" >> "$LOG"
cat "${LOG}.summaries" >> "$LOG"
if [ "$CLAIMS_OK" -ne 0 ]; then
    echo "WARNING: Claims reprocessing exited with code $CLAIMS_OK" | tee -a "$LOG"
fi
if [ "$SUMMARIES_OK" -ne 0 ]; then
    echo "WARNING: Summaries reprocessing exited with code $SUMMARIES_OK" | tee -a "$LOG"
fi
echo "Claims done (exit=$CLAIMS_OK), Summaries done (exit=$SUMMARIES_OK)" | tee -a "$LOG"

# Step 3: Landscape signals
run_step "Landscape" scripts.reprocess_failed --landscape --delay 3

# Step 4: Edge computation
run_step "Edges" scripts.compute_edges --limit 1000 --delay 1

# Step 5: Graph metrics
run_step "GraphMetrics" scripts.compute_graph_metrics

# Step 6: State summaries
# run_step "StateSummaries" scripts.generate_state_summaries --delay 5

# Step 7: Anticipations
run_step "Anticipations" scripts.generate_anticipations --delay 5

# Final scan
echo "" | tee -a "$LOG"
echo "=== Final data quality scan — $(date) ===" | tee -a "$LOG"
python -m scripts.reprocess_failed --scan 2>&1 | tee -a "$LOG"

echo "" | tee -a "$LOG"
echo "=== Recovery pipeline complete at $(date) ===" | tee -a "$LOG"

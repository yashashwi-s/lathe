#!/bin/bash
# Phase B batch: v0.1-feedback (arm A) vs v2-feedback (arm B), run IN PARALLEL.
# Each arm: opus, medium effort, visual, $2 budget cap.
cd ~/Downloads/learn/latex_typst
PY=~/mamba/envs/lathe/bin/python
LABEL=ab2
BUD=2
LOG=metric_research/batch_logs
mkdir -p "$LOG"

# "sample_id|target" (target = lathe id or dsx corpus path); bash 3.2 compatible
PAIRS=(
  "06_tables_moderate_010|06_tables_moderate_010"
  "05_tables_simple_023|05_tables_simple_023"
  "09_algorithms_003|09_algorithms_003"
  "pubmed_table_004|dataset_expansion/corpus/pubmed_table/pubmed_table_004"
  "arxiv5t_paper_019|dataset_expansion/corpus/arxiv5t_paper/arxiv5t_paper_019"
  "i2s_equation_001|dataset_expansion/corpus/i2s_equation/i2s_equation_001"
)

pids=()
for pair in "${PAIRS[@]}"; do
  sid="${pair%%|*}"
  tgt="${pair##*|}"
  # arm A: v0.1 scalar feedback (harness v3)
  $PY harness_baseline/run_task.py "$tgt" --visual --harness v3 --model opus \
      --effort medium --max-budget-usd $BUD --label $LABEL \
      > "$LOG/${sid}__armA.log" 2>&1 &
  pids+=($!)
  # arm B: v2 evidence-vector feedback
  $PY metric_research/run_phaseb.py "$tgt" --visual --model opus \
      --effort medium --max-budget-usd $BUD --label $LABEL \
      > "$LOG/${sid}__armB.log" 2>&1 &
  pids+=($!)
done

echo "launched ${#pids[@]} runs in parallel: ${pids[*]}"
wait
echo "=== BATCH DONE $(date) ==="
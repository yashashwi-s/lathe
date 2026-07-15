#!/bin/bash
# Sequentially run a queue of harness invocations. Usage: run_queue.sh <queue-file>
# Queue file: one run_task.py / run_oneturn.py arg-line per row.
cd "$(dirname "$0")"
total=$(grep -c . "$1")
i=0
while IFS= read -r line; do
  [ -z "$line" ] && continue
  i=$((i+1))
  echo "### [$i/$total] $line  ($(date +%H:%M:%S))"
  python3 $line || echo "### RUN FAILED: $line"
done < "$1"
echo "### QUEUE_DONE $1"

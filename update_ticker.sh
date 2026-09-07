#!/bin/bash
# usage: update_ticker.sh TICKER LOW AVG HIGH
TICKER="$1"
LOW="$2"
AVG="$3"
HIGH="$4"
FOUND=""
for f in analyst_targets_*.txt; do
  case "$f" in *_OLD*) continue;; esac
  if grep -qP "^${TICKER}\t" "$f" 2>/dev/null; then
    FOUND="$f"
    break
  fi
done
if [ -z "$FOUND" ]; then
  echo "NOTFOUND"
  exit 1
fi
awk -F'\t' -v OFS='\t' -v t="$TICKER" -v low="$LOW" -v avg="$AVG" -v high="$HIGH" '
BEGIN{done=0}
$1==t && done==0 {$4=low; $5=avg; $6=high; done=1}
{print}
' "$FOUND" > "${FOUND}.tmp" && mv "${FOUND}.tmp" "$FOUND"
echo "UPDATED:$FOUND"

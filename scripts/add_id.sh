#!/usr/bin/env bash

awk 'NF && $0 !~ /^#/ {c++; print c ", " $0; next} {print}'

# i=1
# while IFS= read -r line; do
#   echo "$i, $line"
#   ((i++))
# done

# awk '{print NR ", " $0}'
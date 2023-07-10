#!/usr/bin/bash
set -euo

python update.py

# Check if there was new data
new_data=$(git status --porcelain -- raw_data.json | grep ' M')

if [ -n "$new_data" ]; then
  python process.py
  git add raw_data.json processed_data.json
  git commit -m "update"
  # git push
else
  echo "No new data. Exiting."
  exit 0
fi


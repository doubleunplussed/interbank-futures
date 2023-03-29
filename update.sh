#!/usr/bin/bash
set -euo

./download.sh

# Check if there are any untracked files in the "pdfs" directory
untracked_files=$(git status --porcelain --untracked-files -- pdfs | grep '??')

if [ -n "$untracked_files" ]; then
  python extract.py
  python process.py
  git add pdfs pdfdata.json processed_data.json
  git commit -m "update"
  git push
else
  echo "No new file downloaded. Exiting."
  exit 0
fi


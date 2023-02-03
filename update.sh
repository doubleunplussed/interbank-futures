#!/usr/bin/bash
set -euxo
./download.sh
python extract.py
python process.py
git add pdfs pdfdata.json processed_data.json
git commit -m update
git push

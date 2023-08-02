from pathlib import Path
from datetime import datetime
import json
import requests

# Script to download the latest interbank futures settlement prices from the ASX page,
# and update raw_data.json with the results.

URL = (
    "https://asx.api.markitdigital.com/asx-research/1.0/derivatives/interest-rate/"
    + "IB/futures?days=1&height=179&width=179"
)

DATAFILE = Path('raw_data.json')
try:
    alldata = json.loads(DATAFILE.read_text())
except FileNotFoundError:
    alldata = {}

todaydata = json.loads(requests.get(URL).content)['data']

items = todaydata['items']
items.sort(key=lambda item: item['dateExpiry'])

for item in todaydata['items']:
    month = datetime.fromisoformat(item['dateExpiry']).strftime('%b-%y')
    settlement_date = item['datePreviousSettlement']
    if settlement_date not in alldata:
        alldata[settlement_date] = {}
    rate = float(f"{100 - item['pricePreviousSettlement']:.3f}")
    alldata[settlement_date][month] = rate


DATAFILE.write_text(json.dumps(alldata, indent=4))

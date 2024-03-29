import json
from pathlib import Path
from datetime import datetime

import requests
import numpy as np
import pandas as pd

import matplotlib.units as munits
import matplotlib.dates as mdates
import matplotlib.pyplot as plt




def get_forward_rate_data():
    
    FILE = Path('f17-forward-rates.csv')
    try:
        url = "https://www.rba.gov.au/statistics/tables/csv/f17-forward-rates.csv"
        data = requests.get(url).content
        FILE.write_bytes(data)
    except requests.exceptions.ConnectionError:
        print("Silly RBA with their 30 second DNS TTL...")

    df = (
        pd.read_csv(
            FILE,
            encoding='WINDOWS-1252',
            skiprows=[0, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        )
        .dropna(axis=0, how='all')
        .dropna(axis=1, how='all')
    )
    curves = {}
    dates = []
    maxrates = []
    for _, row in df.iterrows():
        date = np.datetime64(datetime.strptime(row[0], '%d-%b-%Y'), 'D')
        dates.append(date)
        maxrate = row[1]
        for rate in row[2:6]:
            if rate > maxrate:
                maxrate = rate
            else:
                break
        maxrates.append(maxrate)
    return np.array(dates), np.array(maxrates)


def get_bond_yields():

    FILE = Path('f2-data.csv')
    try:
        url = "https://www.rba.gov.au/statistics/tables/csv/f2-data.csv"
        data = requests.get(url).content
        FILE.write_bytes(data)
    except requests.exceptions.ConnectionError:
        print("Silly RBA with their 30 second DNS TTL...")
    

    df = (
        pd.read_csv(
            FILE,
            encoding='WINDOWS-1252',
            skiprows=[0, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        )
        .dropna(axis=0, how='all')
        .dropna(axis=1, how='all')
    )

    dates = []
    for _, row in df.iterrows():
        date = np.datetime64(datetime.strptime(row[0], '%d-%b-%Y'), 'D')
        dates.append(date)

    rates = df['Australian Government 2 year bond']
    return np.array(dates), np.array(rates)



munits.registry[np.datetime64] = mdates.ConciseDateConverter()

data = json.loads(Path('processed_data.json').read_text('utf8'))

dates = [np.datetime64(d, 'D') for d in data]
terminal_rates = [max(v.values()) for v in data.values()]
final_rates = [list(v.values())[-1] for v in data.values()]

dates = np.append(dates, [dates[-1] + 1])
terminal_rates = np.append(terminal_rates, [terminal_rates[-1]])
# final_rates = np.append(final_rates, [final_rates[-1]])

ois_dates, ois_terminal_rates = get_forward_rate_data()
ois_dates = np.append(ois_dates, [ois_dates[-1] + 1])
ois_terminal_rates = np.append(ois_terminal_rates, [ois_terminal_rates[-1]])

bond_dates, bond_yields = get_bond_yields()
bond_dates = np.append(bond_dates, [bond_dates[-1] + 1])
bond_yields = np.append(bond_yields, [bond_yields[-1]])


plt.step(
    dates,
    terminal_rates,
    where='post',
    label=f"Interbank futures ({terminal_rates[-1]:.2f}%)",
)
plt.step(
    ois_dates,
    ois_terminal_rates,
    where='post',
    label=f"Overnight-indexed swaps ({ois_terminal_rates[-1]:.2f}%)",
)
plt.step(
    bond_dates,
    bond_yields,
    where='post',
    label=f"2Y bond yield ({bond_yields[-1]:.2f}%)",
)

plt.grid(True, color='k', linestyle=':', alpha=0.5)
plt.title("Market-implied terminal rate")
plt.ylabel("Rate (%)")
plt.legend()
plt.axis(xmin=np.datetime64('2022-05-15'), xmax=dates[-1] + 180, ymin=2.0, ymax=5.0)
plt.show()

import json
from pathlib import Path
from datetime import datetime

import numpy as np

import matplotlib.units as munits
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

munits.registry[np.datetime64] = mdates.ConciseDateConverter()

data = json.loads(Path('processed_data.json').read_text('utf8'))

all_dates = np.array([np.datetime64(d, 'D') for d in data])

def get_decision_day(month):
    """Return a np.datetime64 for the first Tuesday of the month"""
    d = datetime.strptime(month, '%b-%y')
    return np.datetime64(d.replace(day=(2 - d.weekday()) % 7 or 6), 'D')

month_keys = [
    # 'Jun-22',
    'Jul-22',
    'Aug-22',
    'Sep-22',
    'Oct-22',
    'Nov-22',
    'Dec-22',
    # 'Jan-23',
    'Feb-23',
    'Mar-23',
    'Apr-23',
    'May-23',
    'Jun-23',
    'Jul-23',
    'Aug-23',
    'Sep-23',
    'Oct-23',
    'Nov-23',
    'Dec-23',
    'Feb-24',
    'Mar-24',
    'Apr-24',
    # 'May-24',
]

actual_cash_rate = {
    'Mar-22': 0.1,
    'Apr-22': 0.1,
    'May-22': 0.35,
    'Jun-22': 0.85,
    'Jul-22': 1.35,
    'Aug-22': 1.85,
    'Sep-22': 2.35,
    'Oct-22': 2.60,
    'Nov-22': 2.85,
    'Dec-22': 3.10,
    'Feb-23': 3.35,
}

MONTHS = ['Nov-22', 'Dec-22', 'Feb-23', 'Mar-23']
MONTHS = month_keys[:20]

plt.figure(figsize=(12, 8))
for i, month in enumerate(MONTHS):
    rates = np.array(
        [
            v.get(month, actual_cash_rate.get(month, np.nan))
            for v in data.values()
        ]
    )

    start = np.datetime64('2022-06-08')

    rates = rates[all_dates >= start]
    dates = all_dates[all_dates >= start]

    alldates = np.arange(dates[0], dates[-1] + 2)
    allrates = np.full(len(alldates), np.nan)
    for d, r in zip(dates, rates):
        allrates[alldates>=d] = r

    ax = plt.subplot(4, 5, i + 1)
    decision_day = get_decision_day(month)
    plt.step(
        alldates[alldates < decision_day],
        allrates[alldates < decision_day],
        where='post',
        label=f"{month}",
        color=f"C{i}",
    )
    if alldates[-1] >= decision_day:
        plt.plot([decision_day], [actual_cash_rate[month]], 'ro', markersize=2)
    plt.grid(True, color='k', linestyle=':', alpha=0.5)
    # plt.title(f'Market expectation of {month} rate hike')
    plt.axis(
        xmin=start,
        xmax=alldates[-1] + 7,
        ymin=1,
        ymax=4.8,
    )

    ax.yaxis.set_major_locator(plt.MultipleLocator(1))

    locator = mdates.DayLocator([1])
    ax.xaxis.set_major_locator(locator)
    formatter = mdates.ConciseDateFormatter(locator, show_offset=False)
    ax.xaxis.set_major_formatter(formatter)

    plt.legend()

    xlabels_visible = i in (15, 16, 17, 18, 19) 
    ylabels_visible = i in (0, 5, 10, 15)

    if ylabels_visible:
        plt.ylabel('implied rate (%)')
    plt.tick_params(
        axis='x',
        bottom=xlabels_visible,
        labelbottom=xlabels_visible,
    )
    plt.tick_params(
        axis='y',
        left=ylabels_visible,
        labelleft=ylabels_visible,
    )

plt.subplots_adjust(
    left=0.05,
    bottom=0.05,
    right=0.975,
    top=0.975,
    wspace=0,
    hspace=0,
)


plt.show()

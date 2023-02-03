import json
from pathlib import Path
from subprocess import check_call

import numpy as np

import matplotlib.units as munits
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

munits.registry[np.datetime64] = mdates.ConciseDateConverter()

data = json.loads(Path('processed_data.json').read_text('utf8'))

outdir = Path('plots')
outdir.mkdir(exist_ok=True)

months = [
    'Apr-22',
    'May-22',
    'Jun-22',
    'Jul-22',
    'Aug-22',
    'Sep-22',
    'Oct-22',
    'Nov-22',
    'Dec-22',
    'Jan-23',
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
    'Jan-24',
    'Feb-24',
    'Mar-24',
    'Apr-24',
    'May-24',
    'Jun-24',
    'Jul-24',
]


actual_cash_rate = {
    'Apr-22': 0.1,
    'May-22': 0.35,
    'Jun-22': 0.85,
    'Jul-22': 1.35,
    'Aug-22': 1.85,
    'Sep-22': 2.35,
    'Oct-22': 2.60,
    'Nov-22': 2.85,
    'Dec-22': 3.10,
    'Jan-23': 3.10,
}


# Pad data with NaNs:
padded_data = data.copy()
for k, v in data.items():
    padded_data[k] = {month: v.get(month, np.NaN) for month in months}

data = padded_data

plt.figure(figsize=(8,6))
for i, date in enumerate(data):
    
    for d in list(data)[:i]:
        labels = [a.replace('-', '\n') for a in data[d].keys()]
        y = list(data[d].values())
        plt.plot(labels, y, 'ko-', alpha=0.025)

    labels = [a.replace('-', '\n') for a in data[date].keys()]
    y = list(data[date].values())

    plt.plot(
        [a.replace('-', '\n') for a in actual_cash_rate.keys()],
        list(actual_cash_rate.values()),
        'o-',
        label='Actual cash rate target',
        color='C1',
    )
    plt.plot(labels, y, 'ko-', label=f"Interbank futures as of {date}")

    plt.gca().yaxis.set_major_locator(plt.MultipleLocator(0.2))
    plt.axis(ymin=0, ymax=4.5, xmin=labels[0], xmax=labels[-1])
    plt.grid(True, color='k', alpha=0.5, linestyle=":")
    plt.ylabel("cash rate (%)")
    plt.tight_layout()
    plt.legend(loc='lower right')
    # plt.show()
    plt.savefig(outdir / f'{i:04d}.png')
    plt.clf()
    print(i)

# convert to gif
check_call(
    ['convert']
    + [outdir / f'{j:04d}.png' for j in range(len(data))]
    + [
        '-delay',
        '500',
        outdir / f'{len(data) - 1:04d}.png',
        'animated.gif',
    ]
)

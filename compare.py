import json
from pathlib import Path

import numpy as np

import matplotlib.units as munits
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

munits.registry[np.datetime64] = mdates.ConciseDateConverter()

data = json.loads(Path('processed_data.json').read_text('utf8'))

dates = list(data.keys())

dates = [dates[-30], dates[-7], dates[-2], dates[-1]]


# dates = [
    # '2022-11-02',
    # '2022-11-21',
    # '2022-11-22',
    # '2022-11-23',
    # '2022-11-24',
    # '2022-11-25',
    # '2022-11-28',
    # '2022-11-29',
    # '2022-11-30',
    # '2022-12-01',
    # '2022-12-02',
    # '2022-12-05',
    # '2022-12-06',


keys = [
    # 'Jun-22',
    # 'Jul-22',
    # 'Aug-22',
    # 'Sep-22',
    # 'Oct-22',
    # 'Nov-22',
    # 'Dec-22',
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
]

months = [m.split('-')[0] for m in keys]

x = np.arange(len(months))  # the label locations

width = 0.8 / len(dates)

ALL = False

for i, date in enumerate(dates):
    y = list(data[date][k] for k in keys)
    if not ALL:
        label = f"Market forecast as of {date}"
        color = None
    elif date == dates[0]:
        label = 'Previous market forecasts'
        color = 'C0'
    elif date == dates[-1]:
        label = "Current market forecast"
        color = 'C1'
    else:
        label = None
        color = 'C0'
    plt.bar(
        x - 0.4 + i * width,
        y,
        width,
        label=label,
        color=color,
    )
# plt.bar(x - width, rates1, width, label=date1)
# plt.bar(x, rates2, width, label=date2)
# plt.bar(x + width, rates3, width, label=date3)
plt.gca().set_xticks(x, months)

plt.gca().yaxis.set_major_locator(plt.MultipleLocator(0.1))
plt.axis(ymin=2.5, xmin=-0.8, xmax=len(months) - 0.5)
plt.grid(True, axis='y', color='k', alpha=0.25)
plt.ylabel("Market-implied rate (%)")
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()

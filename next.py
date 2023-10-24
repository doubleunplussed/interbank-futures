import json
from pathlib import Path

import numpy as np

import matplotlib.units as munits
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

munits.registry[np.datetime64] = mdates.ConciseDateConverter()

data = json.loads(Path('processed_data.json').read_text('utf8'))

all_dates = np.array([np.datetime64(d, 'D') for d in data])

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
    'Mar-23': 3.60,
    'Apr-23': 3.60,
    'May-23': 3.85,
    'Jun-23': 4.10,
    'Jul-23': 4.10,
    'Aug-23': 4.10,
    'Sep-23': 4.10,
    'Oct-23': 4.10,
}

MONTHS = ['Nov-23', 'Dec-23', 'Feb-24']
# MONTHS = month_keys[1:10]

for i, month in enumerate(MONTHS):
    #this_month = month_keys[month_keys.index(month) - 1]
    #this_month_rate = np.array(
    #    [
    #        v.get(this_month, actual_cash_rate.get(this_month, np.nan))
    #        for v in data.values()
    #    ]
    #)
    this_month_rate = list(actual_cash_rate.values())[-1]
    next_month_rate = np.array(
        [
            v.get(month, actual_cash_rate.get(month, np.nan))
            for v in data.values()
        ]
    )

    start = np.datetime64('2022-06-08')
    #this_month_rate = this_month_rate[all_dates >= start]
    next_month_rate = next_month_rate[all_dates >= start]
    dates = all_dates[all_dates >= start]

    hike = next_month_rate - this_month_rate

    print(month)
    print(f'E(hike) = {100*hike[-1]:.1f} bps')

    P25 = 100 * (hike[-1]) / 0.25
    print(f"P25: {P25:.2f}%")

    P50 = 100 * (hike[-1] - 0.25) / 0.25
    print(f"P50: {P50:.2f}%")

    P75 = 100 * (hike[-1] - 0.50) / 0.25
    print(f"P75: {P75:.2f}%")
    print()

    alldates = np.arange(dates[0], dates[-1] + 2)
    allhikes = np.full(len(alldates), np.nan)
    for d, r in zip(dates, hike):
        allhikes[alldates>=d] = r

    plt.figure()
    # plt.subplot(3, 3, i + 1)
    plt.step(
        alldates,
        100 * allhikes / 0.25,
        where='post',
        label=f"{month}",
        color=f"C{i}",
    )
    plt.grid(True, color='k', linestyle=':', alpha=0.5)
    plt.title(f'Market expectation of {month} rate hike')
    plt.axis(ymin=-10, ymax=20)
    plt.gca().yaxis.set_major_locator(plt.MultipleLocator(10))
    plt.legend()

    # xlabels_visible = i in (6, 7, 8) 
    # ylabels_visible = i in (0, 3, 6)

    # if ylabels_visible:
    #     plt.ylabel('E(hike) (bps)')
    # plt.tick_params(
    #     axis='x',
    #     bottom=xlabels_visible,
    #     labelbottom=xlabels_visible,
    # )
    # plt.tick_params(
    #     axis='y',
    #     left=ylabels_visible,
    #     labelleft=ylabels_visible,
    # )

    plt.ylabel('fraciton of 25bps priced (%)')

# plt.subplots_adjust(
#     left=0.1,
#     bottom=0.1,
#     right=0.9,
#     top=0.9,
#     wspace=0,
#     hspace=0,
# )


# plt.figure()
# hike_lower = (hike[-1] // .25) * 0.25
# hike_upper = hike_lower + 0.25
# plt.step(alldates, 100 * (allhikes - hike_lower) / 0.25, where='post')
# plt.grid(True, color='k', linestyle=':', alpha=0.5)
# plt.title(f"Market-implied probability of {int(100*hike_upper)}bps {month} hike")
# plt.ylabel(f"P{int(100*hike_upper)} (%)")
# plt.axis(ymin=0, ymax=100)
# plt.gca().yaxis.set_major_locator(plt.MultipleLocator(10))

plt.show()

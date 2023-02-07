from datetime import datetime
import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt





def get_decision_day(month):
    """Return the day of the first Tuesday of the month"""
    d = datetime.strptime(month, '%b-%y')
    return d.replace(day=(1 - d.weekday()) % 7 + 1)


def before_decision_day(date, month):
    """Return whether a date is before interest rate decision day in the given month"""
    d = datetime.strptime(date, '%Y-%m-%d')
    return d < get_decision_day(month)




data = json.loads(Path('processed_data.json').read_text('utf8'))

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
    # 'Jan-23': 3.10,
    'Feb-23': 3.35,
}

forecast_cash_rate = {}
for month in list(actual_cash_rate)[1:]:
    prior = [d for d in data if before_decision_day(d, month)]
    if not prior:
        continue
    forecast_cash_rate[month] = data[max(prior)][month]

hikes = {
    m: h
    for m, h in zip(
        list(actual_cash_rate)[1:], np.diff(list(actual_cash_rate.values()))
    )
}

forecast_hikes = {
    m: forecast - previous
    for m, forecast, previous in zip(
        list(forecast_cash_rate), forecast_cash_rate.values(), actual_cash_rate.values()
    )
}

prob_of_outcome = {
    m: 1 - abs(forecast_hikes[m] - hikes[m]) / 0.25 for m in forecast_hikes
}


bins = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
bins = np.array([0.0, 0.25, 0.5, 0.75, 1.0])

binlabels = ['0–25%', '25–50%', '50–75%', '75–100%']
binlabels = [f"{100 * a:.0f}–{100 * b:.0f}%" for a, b in zip(bins[:-1], bins[1:])]

yes = np.zeros(len(bins) - 1, dtype=int)
no = np.zeros(len(bins) - 1, dtype=int)
variances = np.zeros(len(bins) - 1)
EV = np.zeros(len(bins) - 1)
for p in prob_of_outcome.values():
    for i, (binmin, binmax) in enumerate(zip(bins[:-1], bins[1:])):
        if binmin <= p < binmax:
            yes[i] += 1
            variances[i] += p * (1 - p)
            EV[i] += p
        if binmin <= 1 - p < binmax:
            no[i] += 1
            variances[i] += p * (1 - p)
            EV[i] += 1 - p



plt.errorbar(
    binlabels,
    100 * EV / (yes + no),
    100 * np.sqrt(variances) / (yes + no),
    fmt='ko',
    capsize=2,
    label="expected proportion of outcomes assuming perfect calibration"
)

plt.plot(
    binlabels,
    100 * yes / (yes + no),
    'ro',
    zorder=10,
    label="actual proportion of true outcomes",
)

# x = np.linspace(0, 1, 100)
# plt.plot(x, x)
plt.title("interbank futures calibration curve")
plt.axis(ymin=0, ymax=100, xmin=-0.5, xmax=len(binlabels) - 0.5)
plt.grid(True, color='k', linestyle=":", alpha=0.5)
plt.xlabel("Probability bin")
plt.ylabel("Proportion of true outcomes (%)")
plt.legend()


for k, v in forecast_hikes.items():
    print(
        f"{k}: forecast {100 * v:.2f} bps, "
        + f"actual {100 * hikes[k]:.0f}, "
        + f"predicted with P={100 * prob_of_outcome[k]:.1f}%"
    )
print()
print("Of outcomes priced with probability")
for label, y, n, ev, var in zip(binlabels, yes, no, EV, variances):
    print(f"{label}: {y}/{y+n} occurred (expected: {ev:.1f} ± {var:.1f})")



plt.show()

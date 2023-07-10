interbank-futures
-----------------

This is some code I use to extract probabilities of cash rate target hikes/cuts from
interbank futures


This used to do optical character recognition to extract numbers from the [asx
pdf](https://www.asx.com.au/data/trt/ib_expectation_curve_graph.pdf) of rates at which
interbank futures settled each day, but now justs gets data from [This API
endpoint](https://asx.api.markitdigital.com/asx-research/1.0/derivatives/interest-rate/IB/futures?days=1&height=179&width=179)

The main problem with looking at the rates implied by each contract directly is that the
interbank futures contracts refer to the average cash rate over each calendar month,
whereas rate changes are made on the first Tuesday of the month. In addition, the actual
cash rate may not be equal to the cash rate target at any given time - at the moment the
actual cash rate banks lend to each other at is about four basis points below the RBA's
target. Both these must be taken into account.

I have some data going back to April, and consistent data from May when I started
automating data scraping.

What these scripts do:

* `update.py` downloads the latest settlement prices from the ASX API and saves them to
  `raw_data.json`

* `process_data.py` does some calendar-based maths to convert the market-implied average
  cash rate over each calendar month to a market-implied cash rate target after the RBA
  meeting on the first Tuesday of each month, and saves the result to
  `processed_data.json`. Although there is no meeting in Jan, the code treats Jan no
  differently and computes a cash rate as if there was still a meeting - one can just
  ignore the result for January.

* `terminal.py` plots the market-implied terminal cash rate over time from both
  interbank futures, as well as the overnight-indexed swaps market using data published
  monthly from the RBA.

* `compare.py` makes bar charts comparing the cash rate forecasts for different dates -
  which dates can be set in-code.

* `gridcompare.py` makes plots of all cash rate forecasts (past and present) over time
  for some set of months, and marks the actual cash rate

* `next.py` makes charts of the expected cash rate for the next few meetings. It also
  prints the implied probabilities of certain hikes, assuming that the real hike must be
  one of two possible hikes separated by 25bps.

I'm publishing this code as-is for those who are curious, but it was written without the
intention of being easy to use for others, hence why many settings are just made by
editing the code directly.

The python scripts can be run with any recent version of Python as `python
<scriptname>.py`. They require the `numpy`, `matplotlib`, `pandas`, and `requests`
packages.

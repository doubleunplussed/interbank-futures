interbank-futures
-----------------

This is some code I use to extract probabilities of cash rate target hikes/cuts from
interbank futures, based on the [asx
pdf](https://www.asx.com.au/data/trt/ib_expectation_curve_graph.pdf) of rates at which
interbank futures settled each day. This PDF is usually published each evening.

The main problem with looking at the asx pdf directly is that the interbank futures
contracts refer to the average cash rate over each calendar month, whereas rate changes
are made on the first Tuesday of the month. In addition, the actual cash rate may not be
equal to the cash rate target at any given time - at the moment the actual cash rate
banks lend to each other at is about four basis points below the RBA's target. Both
these must be taken into account.

I have some data going back to April, and consistent data from May when I started
automating downloading the PDF each evening.

What these scripts do:

* `download.sh` downloads the current ASX pdf and saves it, using a hash of its contents
  as the filename. This way it can be run frequently and will save unique PDFs with
  unique filenames without overwriting older ones.

* `extract.py` extracts the numbers from each PDF and saves them to `pdfdata.json`

* `process_data.py` does some calendar-based maths to convert the market-implied average
  cash rate over each calendar month to a market-implied cash rate target after the RBA
  meeting on the first Tuesday of each month, and saves the result to
  processed_data.json. Although there is no meeting in Jan, the code treats Jan no
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
<scriptname>.py`. Most require only the `numpy`, `matplotlib`, and `pandas` packages.

`extract.py` also requires the `PyPDF3` Python package, and calls several linux tools on
the command line, including `tesseract`, `imagemagick`. You can install these on Linux
with `sudo apt install imagemagick tesseract-ocr`. If you're not on Linux, you're on
your own.

from pathlib import Path
import json
from datetime import datetime
import calendar

# This script converts the calendar month market expectations of the overnight cash rate
# contained in raw_data.json into expectations of the cash rate *target* after each
# month's RBA interest rate decision, and saves the results to processed_data.json. This
# corrects both for the fact that inter-meeting periods do not align with calendar
# months, and that the overnight cash rate differs from the target by some amount - the
# current difference is assumed to persist for all future months.
 
def get_n_days(month):
    """Return number of days in the month"""
    d = datetime.strptime(month, '%b-%y')
    return calendar.monthrange(d.year, d.month)[1]


def get_decision_day(month):
    """Return the day of the first Tuesday of the month"""
    d = datetime.strptime(month, '%b-%y')
    return (1 - d.weekday()) % 7 + 1


def get_prev_month(month):
    """Return the month preceding the given month"""
    d = datetime.strptime(month, '%b-%y')
    d = d.replace(
        year=(d.year - 1) if d.month == 1 else d.year,
        month=(d.month - 2) % 12 + 1,
    )
    return d.strftime('%b-%y')


def before_decision_day(date):
    """Return whether a date is before interest rate decision day in that
    month"""
    d = datetime.strptime(date, '%Y-%m-%d')
    return d.day < get_decision_day(d.strftime('%b-%y'))


def prepend_prev_month(rates):
    """Prepend to the rates dict the most recent rate we have for the month prior to the
    first month in the dict"""
    month = list(rates.keys())[0]
    prev_month = get_prev_month(month)
    prev_month_avrate = [d for d in data.values() if prev_month in d][-1][prev_month]
    return {prev_month: prev_month_avrate, **rates}


def get_month(date):
    """Return the month string (e.g. Feb-22) corresponding to a date string"""
    return datetime.strptime(date, '%Y-%m-%d').strftime('%b-%y')

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
    'Jan-23': 3.10,
    'Feb-23': 3.35,
    'Mar-23': 3.60,
    'Apr-23': 3.60,
    'May-23': 3.85,
    'Jun-23': 4.10,
    'Jul-23': 4.10,
    'Aug-23': 4.10,
}

data = json.loads(Path('raw_data.json').read_text('utf8'))
processed_data = {}
for date, rates in data.items():
    if before_decision_day(date) or get_month(date) not in rates:
        rates = prepend_prev_month(rates)
    processed_rates = {}

    # Compute delta from the first month's data
    month, avrate = list(rates.items())[0]
    prev_month = get_prev_month(month)
    prev_target = actual_cash_rate[prev_month]
    current_target = actual_cash_rate[month]

    f_this_month = get_decision_day(month) / get_n_days(month)

    delta = avrate - f_this_month * prev_target - (1 - f_this_month) * current_target

    print(delta)
    
    processed_rates[month] = current_target

    for month, avrate in list(rates.items())[1:]:
        prev_month = get_prev_month(month)
        prev_avrate = processed_rates[prev_month] + delta
        f_this_month = get_decision_day(month) / get_n_days(month)
        rate = (avrate - f_this_month * prev_avrate) / (1 - f_this_month)
        processed_rates[month] = round(rate - delta, 3)

    processed_data[date] = processed_rates



Path('processed_data.json').write_text(json.dumps(processed_data, indent=4), 'utf8')

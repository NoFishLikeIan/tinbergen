import calendar

months = [abbr for abbr in calendar.month_abbr if len(abbr) > 0]


def get_month_index(abbr):
    return months.index(abbr) + 1

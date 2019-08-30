import os
import calendar

environment = os.environ

data_path = environment['DATA_PATH'] if 'DATA_PATH' in environment else './data'
out_path = environment['OUT_PATH'] if 'OUT_PATH' in environment else './out'
plot_path = environment['PLOT_PATH'] if 'PLOT_PATH' in environment else './plot'
plot_path = environment['TIME_COL'] if 'TIME_COL' in environment else 'Period'

inflation_series_path = os.path.join(data_path, 'inflation_series.csv')

start_year = 1958
events_dummies = [(7, 1973), (7, 1976), (1, 1979), (7, 1982), (1, 1990)]

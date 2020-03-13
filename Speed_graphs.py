import datetime
import pandas as pd
import matplotlib.pyplot as plt

def _get_datetime(timestamp):
    _date, _time = timestamp.split(' ')
    _year, _month, _day = map(int, _date.split('-'))
    _hours, _mins, _seconds = map(int, (_time[:-8], _time[-7:-5], _time[-4:-2]))

    if int(_hours) == 12 and timestamp.endswith('am'):
        _hours = 0
    if int(_hours) == 12 and timestamp.endswith('pm'):
        _hours = 12
    else:
        _hours = _hours + (12 if timestamp.endswith('pm') else 0)

    _mins = int(_mins)
    _seconds = int(_seconds)
    return datetime.datetime(_year, _month, _day, _hours, _mins, _seconds)


def _get_speed():
    table = pd.read_csv("Untitled 1.csv", usecols=[3, 4])

    DateTime = []
    Speed = []
    for row, column in table.iterrows():
        datetime = _get_datetime(column['Time Captured'])
        speed = column['MPH']

        DateTime.append(datetime)
        Speed.append(speed)

    plt.figure(num=None, figsize=(30, 5), dpi=750, facecolor='w', edgecolor='w')
    plt.grid(axis='both')
    plt.plot(DateTime, Speed, '-')
    plt.savefig('Speed_graph.svg')
    # plt.show()

_get_speed()
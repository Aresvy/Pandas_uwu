#! /usr/bin/python3.7
"""
The porpuse of this program is to see any abnormalities such as GPS Stucks (When the unit appears to be in the same Latitude and Longitude for every GPS point),
GhostTrips (When the time between DateTimes are long) and also can count the number of Trips that made the unit (Long trips > 30 min, Short Trips < 30 min).

There's a little inconvience, in the .CSV archive you need to separate the Latitude and Longitude to a separate columns, to do this (in Libre office) select the column 'Lat, Lon'
then go to Data --> Text to Column --> click OK. This will separate the 'Lat, Lon' column.
"""

import datetime
import pandas as pd
table = pd.read_csv("Unit_10:010030012088286_LAS.csv", usecols=[3,14,22,23,24])


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


def _number_of_trips():
    global table
    deltas = []
    ShortTrip = 0
    LongTrip = 0
    Timestamp_1 = None
    Timestamp_2 = None
    for row, DT in table.iterrows():
        Datetimes = _get_datetime(DT['Time Captured'])
        EventCode = DT['Event Code']
        if EventCode == 2:
            Timestamp_1 = Datetimes
        if EventCode == 5 and Timestamp_1:
            Timestamp_2 = Datetimes

        if Timestamp_1 and Timestamp_2:
            delta = Timestamp_1 - Timestamp_2

            deltas.append(delta.seconds)
            Timestamp_1 = None
            Timestamp_2 = None

    for i in deltas:
        try:
            if deltas[i] > 1800: #The value of 1800 is in seconds witch is 30 min#
                LongTrip = LongTrip + 1
            else:
                ShortTrip = ShortTrip + 1
        except:
            pass
    print(f"The number of short trips are {str(ShortTrip)}")
    print(f"The number of long trips are {str(LongTrip)}")

def _number_of_trips_2():
    global table
    deltas = []
    ShortTrip = 0
    LongTrip = 0
    Timestamp_1 = None
    Timestamp_2 = None
    for row, DT in table.iterrows():
        Datetimes = _get_datetime(DT['Time Captured'])
        EventCode = DT['Event Code']
        if EventCode == 5:
            Timestamp_1 = Datetimes
        if EventCode == 2 and Timestamp_1:
            Timestamp_2 = Datetimes

        if Timestamp_1 and Timestamp_2:
            delta = Timestamp_1 - Timestamp_2

            deltas.append(delta.seconds)
            Timestamp_1 = None
            Timestamp_2 = None

    for i in deltas:
        try:
            if deltas[i] > 1800: #The value of 1800 is in seconds witch is 30 min#
                LongTrip = LongTrip + 1
            else:
                ShortTrip = ShortTrip + 1
        except:
            pass
    print(f"The number of short trips_2 are {str(ShortTrip)}")
    print(f"The number of long trips_2 are {str(LongTrip)}")



def _ghost_trips():
    deltas = []
    EventCode = []
    TimeStamps = []

    TS1 = None
    TS2 = None
    for row, DT in table.iterrows():
        DateTime = _get_datetime(DT['Time Captured'])
        Timestamp = DT['Time Captured']
        TimeStamps.append(Timestamp)

        TriggerBy = DT['Triggered By']
        EventCode.append(TriggerBy)

        if TS1 is None and TS2 is None:
            TS1 = DateTime
        elif TS1 != None and TS2 is None :
            TS2 = DateTime

        if TS1 and TS2:
            delta = TS1 - TS2
            deltas.append(delta.seconds)

            TS1 = None
            TS2 = None


    TimeS = TimeStamps[0::2]
    EC = EventCode[0::2]

    for i,ec,ts in zip(deltas,EC,TimeS):
        if i > 180:
            minutes = i / 60
            print(f"Probale GhostTrip was found at {ts}, while the EventCode was '{ec}'. Time elapsed {minutes} min ")


def _gps_stuck():
    DateTime = []
    Lat_deltas = []
    Lon_deltas = []

    LatD_1 = None
    LatD_2 = None
    LonD_1 = None
    LonD_2 = None

    for rows, columns in table.iterrows():
        Date = columns["Time Captured"]
        DateTime.append(Date)
        Lat = columns["Lat"]
        Lon = columns[" Lon"]

        if LatD_1 is None and LatD_2 is None:
            LatD_1 = Lat
        elif LatD_1 != None and LatD_2 is None:
            LatD_2 = Lat

        if LatD_1 and LatD_2:
            Latitude_delta = LatD_1 - LatD_2
            Lat_deltas.append(Latitude_delta)

            LatD_1 = None
            LatD_2 = None

        if LonD_1 is None and LonD_2 is None:
            LonD_1 = Lon
        elif LonD_1 != None and LonD_2 is None:
            LonD_2 = Lon

        if LonD_1 and LonD_2:
            Longitude_Delta = LonD_1 - LonD_2
            Lon_deltas.append(Longitude_Delta)

            LonD_1 = None
            LonD_2 = None

    DT = DateTime[0::2]

    for i, z, d in zip(Lat_deltas, Lon_deltas, DT):
        if i == 0 and z == 0:
            print(f"GPS Stuck {i, z} Go and check the time captured at {d}")


_number_of_trips()
_number_of_trips_2()
_gps_stuck()
_ghost_trips()

import datetime
import pandas as pd

table = pd.read_csv("Untitled 1.csv", usecols=[3,14,22,23])

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

def get_num_trips():
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
            if i > 1800: #The value of 1800 is in seconds witch is 30 min#
                LongTrip = LongTrip + 1
            else:
                ShortTrip = ShortTrip + 1
        except:
            pass

    print(f"The number of short trips are {str(ShortTrip)}")
    print(f"The number of long trips are {str(LongTrip)}")

def lost_gps_points():
    global table
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
            print(f"An abnormality was found at {ts}, while the EventCode was '{ec}'. Time elapsed {minutes} min ")

def gps_stuck():
    deltas = []
    EventCode = []
    TimeStamps = []

    TS1 = None
    TS2 = None

    table = pd.read_csv("Untitled 1.csv",
                        usecols=[3, 23])

    for row, DT in table.iterrows():
        DateTime = _get_datetime(DT['Time Captured'])
        Timestamp = DT['Time Captured']
        TimeStamps.append(Timestamp)

        TriggerBy = DT['Triggered By']
        EventCode.append(TriggerBy)

        if TS1 is None and TS2 is None:
            TS1 = DateTime
        elif TS1 != None and TS2 is None:
            TS2 = DateTime

        if TS1 and TS2:
            delta = TS1 - TS2
            deltas.append(delta.seconds)

            TS1 = None
            TS2 = None

    TimeS = TimeStamps[0::2]
    EC = EventCode[0::2]

    for i, ec, ts in zip(deltas, EC, TimeS):
        if i > 180:
            minutes = i / 60
            print(f"An abnormality was found at {ts}, while the EventCode was '{ec}'. Time elapsed {minutes} min ")


# get_num_trips()
# gps_stuck()
lost_gps_points()
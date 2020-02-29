#! /usr/bin/python3.7
import datetime
import pandas as pd
import zipp

from loguru import logger

def _getme_GPS():
    GPS = []

    table = pd.read_csv("Untitled 1.csv", usecols=[22])

    for row, Lat_Lon in table.iterrows():
        LL = Lat_Lon["Lat, Lon"]
        GPS.append(LL)

    coordinates = []
    deltas = []
    coord_1 = None
    coord_2 = None

    for cord in GPS:
        pair = [float(s) for s in cord.strip().split(",")]
        coordinates.append(pair)

    if coord_1 is None and coord_2 is None:
        coord_1 = coordinates
    else:
        pass
    if coord_1 != None and coord_2 is None:
        coord_2 = coordinates
    else:
        pass

    print(coord_1)






    # if coord_1 and coord_2:
    #     delta = coord_1 - coord_2
    #     deltas.append(delta)
    #
    #     coord_1 = None
    #     coord_2 = None



    # Lat = [i.split(',')[0] for i in GPS]
    # Lon = [i.split(',')[1] for i in GPS]
    # Latitude = [float(i) for i in Lat]
    # Longitude = [float(i) for i in Lon]
    # print(Latitude)


_getme_GPS()
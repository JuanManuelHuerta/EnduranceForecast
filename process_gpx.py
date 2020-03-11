#!/usr/bin/env python3

__author__      = "Juan M. Huerta"
__copyright__   = "Copyright 2020, Juan M. Huerta"

import sys
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
from json import dumps
from datetime import datetime
import operator
from math import radians, cos, sin, asin, sqrt
import numpy as np
import math
from collections import namedtuple


import csv

try:
    from itertools import imap
except:
    imap = map

#from scipy import signal

class multi_sensor_point:

    def __init__(self,dt,lat,ele,lon,heartRate,speed):
        self.latitude=lat
        self.longitude=lon
        self.datetime=dt
        self.speed = speed
        self.elevation=ele
        self.heart_rate=heartRate
        self.time_offset=dt


def load_gpx(file_location):
    my_data = eval(dumps(bf.data(fromstring(open(file_location,'rt').read()))))
    a='{http://www.topografix.com/GPX/1/1}'
    X=[]
    S=[]
    md=None
    origin=None
    for p in my_data[a+"gpx"][a+"trk"][a+"trkseg"][a+"trkpt"]:
        datetime_object = datetime.strptime(p[a+"time"]['$'], '%Y-%m-%dT%H:%M:%SZ')
        if md is None or datetime_object < md:
            md = datetime_object
            origin =(float(p['@lat']),  float(p['@lon']))
            #X.append( [datetime_object,  float(p['@lat']), float(p[a+"ele"]['$']),  float(p['@lon'])])
        S.append( multi_sensor_point(datetime_object,  float(p['@lat']), float(p[a+"ele"]['$']),  float(p['@lon']),None,None))
            
       ##  Duplet of (time, coordinates) :  (time, lat, lon)                                                                                                                                        
       # X=[[(x[0]-md).total_seconds(),(x[1],x[3])] for x in X]
    X=[[(x.datetime-md).total_seconds(),(x.latitude,x.longitude,x.elevation)] for x in S]
    return sorted(X,key=operator.itemgetter(0))


X=load_gpx("sample.gpx")

for x in X:
    print(x)



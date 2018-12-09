#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 13:28:16 2018

@author: HannaTuomi
"""

#Dot map for MA Zipcodes showing % making green change

"""
Example of dot density map
"""
import geoplotlib
from geoplotlib.utils import read_csv
from geoplotlib.layers import DotDensityLayer as dd

import numpy as np


zipcodes = open('/Users/HannaTuomi/Desktop/CFG Green Streets/ziplatlon.csv')
greenness = open('/Users/HannaTuomi/Desktop/CFG Green Streets/Greenness_by_Zip.csv')



green_data = {}
for line in greenness:
    newline = line.strip().split(',')
    ZIP = newline[0] 
    while len(ZIP) != 5:
        ZIP = str('0' + str(ZIP))
    newline[0] = ZIP
    green_data[newline[0]] = (newline[1], newline[2])
    
print(green_data)
    
zips = {}
for line in zipcodes:
    newline = line.strip().split(',')
    try:
        int(newline[0])
    except:
        continue
    ZIP = newline[0] 
    while len(ZIP) != 5:
        ZIP = str('0' + str(ZIP))
    newline[0] = ZIP
    zips[newline[0]] = [newline[0], float(newline[1]), float(newline[2])]

for element in green_data.keys():
    if element in zips.keys():
        size = (int(round((int(green_data[element][0]))/10)))
        color = np.array([94, 214,79])*float(green_data[element][1])
        geoplotlib.dot(['zip','lat','lon'].append(zips[element]), color, size, f_tooltip=None)
#        geoplotlib.add_layer(dd(zips[element], [94, 214,79], None, None))
        
geoplotlib.show()

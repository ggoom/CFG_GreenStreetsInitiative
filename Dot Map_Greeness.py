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


zipcodes = open('ziplatlon.csv')
greenness = open('Greenness_by_Zip.csv')

zipcode = read_csv('ziplatlon.csv')

green_data = {}
for line in greenness:
    newline = line.strip().split(',')
    ZIP = newline[0] 
    while len(ZIP) != 5:
        ZIP = str('0' + str(ZIP))
    newline[0] = ZIP
    green_data[newline[0]] = (newline[1], newline[2])

    
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
    zips[newline[0]] = [newline[0], float((newline[1])), float((newline[2]))]

for element in green_data.keys():
    if element in zips.keys():
        
        size = int(green_data[element][0])//10
       
        color = int(255*(1-(2*float(green_data[element][1]))))
        print(element, size, color)


#        geoplotlib.add_layer(dd({'zip':zips[element][0], 'lat': [(zips[element][1])], 'lon': [(zips[element][2])]}, [color,255,color],size, None))
#        

        
#geoplotlib.hist(zipcode, cmap='hot', alpha=94, colorscale='lin', binsize=10, show_tooltip=False,
#         scalemin=0, scalemax=None, f_group=None, show_colorbar=True)


#geoplotlib.show()

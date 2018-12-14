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
    #insert the correct csv with format (zip, #people, %green change)

#read the csv for green data to make it usable in geoplotlib
green_data = {}
for line in greenness:
    newline = line.strip().split(',')
    ZIP = newline[0] 
    while len(ZIP) != 5:
        ZIP = str('0' + str(ZIP))
    newline[0] = ZIP
    green_data[newline[0]] = (newline[1], newline[2])

green_data_for_tooltip = {'percent': {}}
for element in green_data.keys():
    green_data_for_tooltip['percent'][element] = green_data[element][1]
    
    
#read the csv for zipcodes to make it usable in geoplotlib
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

##create the pop-up box with green change %s
#manager = HotspotManager()
#for element in zips.keys():
#    manager.add_poly(zipselement[1], element[2], )
#manager.pick()
#        

#create a new dot for each zipcode
for element in green_data.keys():
    if element in zips.keys():
        #scale dot size by number of people
        size = int(green_data[element][0])//10
       
        #scale color by percentage of people who make a green change
        color = int(255*(1-(2*float(green_data[element][1]))))
        
        #create the data to make a dot for
        data = {'zip':zips[element][0], 'lat': [(zips[element][1])], 'lon': [(zips[element][2])]}
        
        #add the dot for the zipcode
        geoplotlib.add_layer(dd(data, [color,255,color],size, \
            f_tooltip=None))
#        dd.draw(proj, mouse_x, mouse_y, ui_manager)
        
        #add labels for zipcode
        geoplotlib.labels(data, 'zip' , color='k', font_name= 'helvetica', \
           font_size=8, anchor_x='left', anchor_y='top')

        

geoplotlib.show()

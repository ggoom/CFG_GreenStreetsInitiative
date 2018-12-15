#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 16:14:29 2018

@author: HannaTuomi
"""
import plotly.plotly as py
import pandas as pd
from  plotly.offline import plot

def Read_CSV_Organize_Data(filename):
    green_data = {}
    persons ={}
    emissions = {}
    for line in open(filename):
        newline = line.strip().split(',')
        ZIP = newline[1] 
        if ZIP == ' Home ZipCode':
            continue
        while len(ZIP) != 5:
            ZIP = str('0' + str(ZIP))
        newline[0] = ZIP
        
        if newline[4] == '':
            continue
    
        if ZIP in persons.keys():
            persons[ZIP] += 1
            emissions[ZIP] += int(newline[4])
        else:
            persons[ZIP] = 1
            emissions[ZIP] = int(newline[4])
                
        
    for ZIP in persons.keys():
        green_data[ZIP] = (persons[ZIP], (float(emissions[ZIP])/int(persons[ZIP])))
        
    return green_data

#read the csv for zipcodes to make it usable in geoplotlib
def ZipCodes_for_map (filename):
    zips = {}
    zipcodes = open(filename)
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
        
    return zips

#produces (#people, emissions/person)
green_data = Read_CSV_Organize_Data('map_testing_data.csv')
zip_data =ZipCodes_for_map('ziplatlon.csv')


people = []
emissions = []

for zipcode in green_data.keys():
    people.append(green_data[zipcode][0])
    emissions.append(green_data[zipcode][1])
    
max_people = max(people)
max_emissions = max(emissions)

zips_for_map = []
lat_for_map = []
lon_for_map = []
size_for_map = []
color_for_map= []
for zipcode in green_data.keys():
    if zipcode in zip_data.keys():
        zips_for_map.append(zipcode)
        lat_for_map.append(zip_data[zipcode][1])
        lon_for_map.append(zip_data[zipcode][2])
        size_for_map.append(20*(green_data[zipcode][0]/max_people))
        color_for_map.append(str('rgb(' +str(int(255*(green_data[zipcode][1]/max_emissions))) + ', 255, ' + \
                    str(int(255*(green_data[zipcode][1]/max_emissions))) + ')' ))

    
zips = []
scale = 5000
n = 0
for i in range(0, len(zips_for_map)):
    ZIP= dict(
        type = 'scattergeo',
        locationmode = 'USA-states',
        lon = lon_for_map[i],
        lat = lat_for_map[i],
        text = zips_for_map[i],
        marker = dict(
            size = size_for_map[i],
            color = color_for_map[i],
            line = dict(width=0.5, color='rgb(40,40,40)'),
            sizemode = 'area'),
        name= str(n))
    n += 1
    zips.append(ZIP)

layout = dict(
        title = 'Participants and Reduction in Carbon Emissions/Person per Zipcode<br>(Click legend to toggle traces)',
        showlegend = True,
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showland = True,
            landcolor = 'rgb(217, 217, 217)',
            subunitwidth=1,
            countrywidth=1,
            subunitcolor="rgb(255, 255, 255)",
            countrycolor="rgb(255, 255, 255)"
        ),
    )

print(zips)
fig = dict(data = zips, layout=layout)
py.iplot(fig, validate=False, filename='test2')









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
from geoplotlib.layers import DotDensityLayer as dd

#########CODE FOR DUMMY DATA - PROOF OF CONCEPT - % GREEN CHANGES
#greenness = open('Greenness_by_Zip.csv')  
    #insert the correct csv with format (zip, #people, %green change)

##read the csv for green data to make it usable in geoplotlib
#green_data = {}
#for line in greenness:
#    newline = line.strip().split(',')
#    ZIP = newline[0] 
#    while len(ZIP) != 5:
#        ZIP = str('0' + str(ZIP))
#    newline[0] = ZIP
#    green_data[newline[0]] = (newline[1], newline[2])
#
#green_data_for_tooltip = {'percent': {}}
#for element in green_data.keys():
#    green_data_for_tooltip['percent'][element] = green_data[element][1]
    
##create a new dot for each zipcode
#for element in green_data.keys():
#    if element in zips.keys():
#        #scale dot size by number of people
#        size = int(green_data[element][0])//10
#       
#        #scale color by percentage of people who make a green change
#        color = int(255*(1-(2*float(green_data[element][1]))))
#        
#        #create the data to make a dot for
#        data = {'zip':zips[element][0], 'lat': [(zips[element][1])], 'lon': [(zips[element][2])]}
#        
#        #add the dot for the zipcode
#        geoplotlib.add_layer(dd(data, [color,255,color],size, \
#            f_tooltip=None))
#
#        
#        #add labels for zipcode
#        geoplotlib.labels(data, 'zip' , color='k', font_name= 'helvetica', \
#           font_size=8, anchor_x='left', anchor_y='top')
#
#        
#
#geoplotlib.show()
    
    
####USE WITH CSV CREATEd BY CFG_SQL.sql from REAL DATA
    
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
        
#create a new dot for each zipcode
def Make_Map(green_data, zips):
    sizes = []
    for tup in green_data.values():
        sizes.append(tup[0])
    max_size = max(sizes)
    
    colors = []
    for tup in green_data.values():
        colors.append(tup[1])
    max_color = max(colors)
    
    for element in green_data.keys():
        if element in zips.keys():
        
            #create the data to make a dot for
            data = {'zip':zips[element][0], 'lat': [(zips[element][1])], 'lon': [(zips[element][2])], \
                    'color': [int(255*(green_data[element][1]/max_color)), 255, int(255*(green_data[element][1]/max_color))], \
                    'size':50*(int(green_data[element][0])/max_size)}
        
            #add the dot for the zipcode
            geoplotlib.add_layer(dd(data, data['color'], data['size'], f_tooltip=None))
        
            #add labels for zipcode
            geoplotlib.labels(data, 'zip' , color='k', font_name= 'helvetica', \
                              font_size=8, anchor_x='left', anchor_y='top')
    geoplotlib.show()


###Testing###
    
green_data = Read_CSV_Organize_Data('map_testing_data.csv')
zipcodes = ZipCodes_for_map('ziplatlon.csv')
Make_Map(green_data, zipcodes)



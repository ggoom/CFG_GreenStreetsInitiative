#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 21:59:39 2018

@author: HannaTuomi
"""

#make a person class where instances each have their home, work, total distance, and modes of transport
class Person(object):
    """ Create a person with all their information: home, work zip, total distance
    primary, secondary, and tertiary transportation methods
    """
    def __init__(self, home, work, total_distance, primary, secondary, tertiary):
        self.home = home
        self.work = work
        self.total_distance = total_distance
        self.primary = primary
        self.secondary = secondary
        self.tertiary = tertiary
    def get_home(self):
        return self.home
    def get_work(self):
        return self.work
    def get_total_distance(self):
        return self.total_distance
    def get_primary(self):
        return self.primary
    def get_secondary(self):
        return self.secondary
    def get_tertiary(self):
        return self.tertiary
    def __str__(self):
        return "Home: " + str(self.get_home()) + ' ' +  "Work: " + str(self.get_work())  + ' ' + 'Distance: '  + str(self.get_total_distance()) + \
                ' ' + "Primary: " + str(self.get_primary()) +' ' + "Secondary: " + str(self.get_secondary()) + ' ' + "Tertiary: "  + str(self.get_tertiary())
    def __repr__(self):
        return self.__str__()
    def modes(self):   
        """get a tuple of the (primary, secondary, tertiary) modes of transport"""
        return (self.get_primary(), self.get_secondary(), self.get_tertiary())


#sort the people into categories - person and related data go in for their home and work zips


#creates a list of the data for each person

def People(filename):
    data =open(filename).read().split('\n')

    people = []
    for line in data:
        info = line.split(',')
        line.rstrip('\n') 
        if info[0] == "Home Zip":
            continue
        people.append(Person(info[0], info[1], info[19], info[20], info[21], info[22]))
    
    return people

#create a dict for each zipcode to organize the data - returns all the modes people from there are taking to work
def Home_ZipCode (people):
    """people -  list of person instances with all relevant data
       returns - a dictionary 
           key(all home zipcodes) 
           values(modes of transport that people from there take to work)
    """
    
    home_zip = {}   #keys are zipcodes, values are lists of the people modes
    for person in people:
        if person.get_home() in home_zip.keys():
            home_zip[person.get_home()] +=  [person.modes()]
        else:
            home_zip[person.get_home()] =  [person.modes()]
    return home_zip
        
def Work_ZipCode(people):
    """people -  list of person instances with all relevant data
       returns - a dictionary 
           key(all work zipcodes) 
           values(modes of transport that people take to get there)
    """
    work_zip = {}   #keys are zipcodes, values are lists of the people modes
    for person in people:
        if person.get_work() in work_zip.keys():
            work_zip[person.get_work()] +=  [person.modes()]
        else:
            work_zip[person.get_work()] = [person.modes()]
        
    return work_zip
        


def Primary_Dict(data):
    """Takes in the data for a specific zipcde and returns a dictionary with:
        keys = mode of primary transportation
        values = number of people who take that mode"""
        
    primary_mode_dict = {}
    for person in data:
        if person[0] not in primary_mode_dict.keys():
            primary_mode_dict[person[0]] = 1
        else:
            primary_mode_dict[person[0]] += 1
            
    return primary_mode_dict




############ Actual Production/Testing ####################

#Generate/upload data from the correct file
data = People("Final_Dummy Data.csv")


###for testing purposes get a list of possible home, work zipcodes
Avail_Home_zip = []
Avail_Work_zip = []
for element in data:
    if element.get_home() not in Avail_Home_zip:
        Avail_Home_zip.append(element.get_home())
    if element.get_work() not in Avail_Work_zip:
        Avail_Work_zip.append(element.get_home())

print("Available Home Zips: " , Avail_Home_zip)
print("Available Work Zips: " , Avail_Work_zip)

### end of test purposes section

#Input box: Give Zipcode of your home or work
which_dict = input("Home or work? (Type 'home' or 'work') ")
chart_zip_code = str(input("What Zip-Code? "))
go = False

try:
    if which_dict == "home":
        data_for_zip = Home_ZipCode(data)[chart_zip_code]
    elif which_dict == "work":
        data_for_zip = Work_ZipCode(data)[chart_zip_code]
    else:
        raise Exception
    
    primary_mode_dict = Primary_Dict(data_for_zip)  
    total = len(data_for_zip)
    
    go = True

except: #check that there is data/ correct type data exists and can be used
    if which_dict != "home" and which_dict != "work":
        print("Not a valid location identifier, try again!")
    else:
        print( "Error, no data for this zip code, try again! ")
    
#plot the data
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

#if we can get the data (inputs are valid and as expected)
if go:    
    
##########Pie chart for percentage of people by primary transportation

    labels = [element for element in primary_mode_dict.keys()]
    sizes = [int(primary_mode_dict[element])/total for element in primary_mode_dict.keys()  ]
    colors = ['gray', 'silver', 'firebrick', 'darksalmon', 'sandybrown', 'gold', 'olivedrab', 'darkgreen', 'lightseagreen', 'skyblue', 'dodgerblue', 'royalblue', 'navy', 'slateblue', 'darkorchid', 'palevioletred', 'lightgreen', 'white']

    plt.pie(sizes, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=False, startangle=10)
 
    plt.axis('equal')
    plt.show()

##########bar graph

    objects = [element for element in primary_mode_dict.keys()]
    y_pos = np.arange(len(objects))
    performance = [int(primary_mode_dict[element])/total for element in primary_mode_dict.keys()  ]
 
    plt.barh(y_pos, performance, align='center', alpha=0.5)
    plt.yticks(y_pos, objects)
    plt.xlabel('')
    plt.title('Percentage of People Per Primary Transportation from' + ' ' + str(chart_zip_code))
 
    plt.show()


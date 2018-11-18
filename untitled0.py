#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 21:59:39 2018

@author: 
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

def Home_ZipCode(data,home): 
    '''
    data is a list of People
    home is a str of a Zipcode
    
    returns a condensed list of of all people objects from data with same home zipcodes
    '''
    same_home=[]
    for person in data:
        if person.get_home()==home:
            same_home.append(person)
    return same_home

def Primary_List(data):
    """Takes in the data for a specific zipcode and returns a dictionary with:
        
        data is a list of People
        
        keys = mode of primary transportation
        values = number of people who take that mode"""
        
    primary_mode_dict = {}
    for person in data:
        if person.get_primary() not in primary_mode_dict.keys():
            primary_mode_dict[person.get_primary()] = 1
        else:
            primary_mode_dict[person.get_primary()] += 1
    
    return sorted(primary_mode_dict, key=primary_mode_dict.get, reverse=True)

def Primary_Paths(): 
    

#TESTING THE FUNCTIONS

peopleList = People("Final_Dummy Data.csv")
specificList = Home_ZipCode(peopleList,"02110")
sortedPrimary = Primary_List(specificList)
print(sortedPrimary)


#TEST

import plotly.plotly as py

data = dict(
    type='sankey',
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(
        color = "black",
        width = 0.5
      ),
      label = sortedPrimary,
      color = ["blue", "red", "blue", "blue", "blue", "blue"]
    ),
    link = dict(
      source = [0,1,0,2,3,3],
      target = [2,3,3,4,4,5],
      value = [8,4,2,8,4,2]
  ))

layout =  dict(
    title = "Basic Sankey Diagram",
    font = dict(
      size = 10
    )
)

fig = dict(data=[data], layout=layout)
py.plot(fig, validate=False)
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

def Primary_Dict(data_for_zip):
    """Takes in the data for a specific zipcode and returns a dictionary with:
        keys = mode of primary transportation
        values = number of people who take that mode"""
        
    primary_mode_dict = {}
    for person in data_for_zip:
        if person.get_primary() not in primary_mode_dict.keys():
            primary_mode_dict[person.get_primary()] = 1
        else:
            primary_mode_dict[person.get_primary()] += 1
    return primary_mode_dict

def Primary_List(data):
    """Takes in the data for a specific zipcode and list of modes of transport from most to least frequent:
        
        data is a list of People
        """
        
    primary_mode_dict = Primary_Dict(data)
#    print(sorted(primary_mode_dict, key=primary_mode_dict.get, reverse=True))
    return sorted(primary_mode_dict, key=primary_mode_dict.get, reverse=True)



def has_secondary(data):    #condenses data_for_zip to new list of Persons who all have secondary modes of transport
    has_secondary_list=[]
    for i in data:
        if i.get_secondary()!="":
            has_secondary_list.append(i)
    return has_secondary_list

def Secondary_Dict(data):
    """Takes in the data for a specific zipcode and returns a dictionary with:
        keys = commutes from primary to secondary transportation
        values = list with number of people who take that commute"""
    secondary_mode_dict = {}
    for person in data:
#        print(person.get_secondary())
        if type(person.get_secondary()) == str:
            commute = person.get_primary() + " and " + person.get_secondary() #creates str that represents unique commute
#            print(commute)
            if commute not in secondary_mode_dict.keys():
                secondary_mode_dict[commute] = 1
            else:
                secondary_mode_dict[commute] += 1
        else:
            if person.get_secondary() not in secondary_mode_dict.keys():
                secondary_mode_dict[person.get_secondary()] = 1
            else:
                secondary_mode_dict[person.get_secondary()] += 1
#    print(secondary_mode_dict)
    return secondary_mode_dict  

def Secondary_List(data):
    """Takes in the data for a specific zipcode and returns a list.
        
        data is a list of People
        
        keys = mode of primary transportation
        values = number of people who take that mode"""
        
    secondary_mode_dict = Secondary_Dict(data)
#    print(sorted(secondary_mode_dict, key=secondary_mode_dict.get, reverse=True))
    return sorted(secondary_mode_dict, key=secondary_mode_dict.get, reverse=True)

def secondary_paths(data_for_zip2, target1): #makes list of dictionaries where index in list is primary, key is secondary, value is #
    matrix=['dummy space']  #clunky solution...not sure if even need it.
    for source in target1:  #for every primary mode
        for person in data_for_zip2:
            if person.get_primary()==label1[source]:
                target = person.get_primary() + " and " + person.get_secondary() #same format as "commute" above
                if source==len(matrix):     #if primary is new
                    matrix.append({target:1})
                elif target not in matrix[source]: #if secondary is new
                    matrix[source][target]=1
                else:                               #add person with same primary-secondary path
                    matrix[source][target]+=1
    return matrix


#TESTING THE FUNCTIONS

peopleList = People("Final_Dummy Data.csv")
data_for_zip = Home_ZipCode(peopleList,"02110")

#1st layer of sankey, home -> primaries
sortedPrimary = Primary_List(data_for_zip)
primary_modes_dict=Primary_Dict(data_for_zip)


label1=["02110"]    
#print(sortedPrimary)
label1.extend(sortedPrimary) #why doesnt this work????????//
color1=["blue"] #makes blue label for home
color1+= ["red"]*len(sortedPrimary) #adds red labels for primaries
source1=[0]*len(sortedPrimary) #the [0] thing makes as many source 0's as primaries for home->primary
target1=[]
for i in range(1,len(sortedPrimary)+1): #adds # of targets as there are primary modes
    target1.append(i)
value1= []
for mode in sortedPrimary: #uses the primary dict to say how many use each mode as primary
    value1.append(primary_modes_dict[mode])


#makes 2nd layer of sankey, primaries -> secondaries
data_for_zip2=has_secondary(data_for_zip)
sortedSecondary=Secondary_List(data_for_zip2)    
path_matrix = secondary_paths(data_for_zip2, target1) #!!!this is the key to the second layer!!!
#print(path_matrix)

label2 = sortedSecondary
color2 = ["orange"]*len(sortedSecondary)
source2=[]
for i in range(1,len(path_matrix)):
    if i=="dummy space":
        continue
    source2.extend([i]*len(path_matrix[i]))
target2=[]
for i in path_matrix:
    if i=="dummy space":
        continue
    for mode in list(i.keys()): #!!!
        target2.append(label2.index(mode)+len(label1))
value2=[]
for i in path_matrix:
    if i=="dummy space":
        continue
    value2.extend(list(i.values()))

#extend labels from 1st layer to add labels for 2nd layer
label1.extend(label2)
color1.extend(color2)
source1.extend(source2)
target1.extend(target2)
value1.extend(value2)

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
      label = label1,
      color = color1
    ),
    link = dict(
      source=source1,
      target =target1,
      value = value1
  ))

layout =  dict(
    title = "Commutes for this Zip Code",
    font = dict(
      size = 10
    )
)

fig = dict(data=[data], layout=layout)
#py.plot(fig, validate=False)
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 16:03:24 2018

@author: Jocelyn Ting
"""

# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api

import plotly.plotly as py
from plotly.graph_objs import *

array1=[2,5]
array2=[3,3]

new_data = Scatter(x=array1, y=array2 )

data = Data( [ new_data ] )

plot_url = py.plot(data, filename='myplot')

print(plot_url)
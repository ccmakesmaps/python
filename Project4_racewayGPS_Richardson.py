# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 15:03:19 2020

@author: Chelsea Richardson

Takes a csv file of race car GPS readings and generates a polyline shapefile of the car's GPS tracks.
"""

import csvtoshp

# Set input variables
spreadsheet = r"C:\PSU\02_GEOG485\Lesson4\WakefieldParkRaceway_20160421.csv"
output = r"C:\PSU\02_GEOG485\Lesson4\WakefieldParkRaceway_20160421.shp"

try:
    # Process the input CSV file and return a dictionary containing coordinate sets of each lap
    lapDictionary, timeDictionary = csvtoshp.getCoords(spreadsheet)
    
    # Create new polyline feature class in WGS84
    csvtoshp.gpsTracks(output, lapDictionary, timeDictionary)
    
    print(str(output),"created.")
    
except:
    print("Oh no, something went wrong.")

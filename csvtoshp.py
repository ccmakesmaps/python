# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 15:03:19 2020

@author: Chelsea Richardson

Functions for taking a csv file of race car GPS readings and
generating a polyline shapefile of the car's tracks.
"""

def getCoords(spreadsheet):
    import csv
    # Open the input CSV file
    with open(spreadsheet, "r") as carGPS:
        #Set up CSV reader and get lap, lat, and lon field indices from the header
        csvReader = csv.reader(carGPS)
        header = next(csvReader)
        lapIndex = header.index("Lap")
        latIndex = header.index("Latitude")
        lonIndex = header.index("Longitude")
        
        # Create a dictionary to store coordinate pairs of each lap
        lapDictionary = {}
        
        # Loop through the lines in the file to get lat and lon coordinates and lap number
            # Produce output: Lap: 0 Lon: 1.23 Lat: 2.34
        for row in csvReader:
            # use if to skip row if number of fields does not match header row or starts with '#'
            if row[0].startswith('#'):
                pass
            else:
                # use else to proceed with row otherwise
                lap = int(row[lapIndex])
                lat = float(row[latIndex])
                lon = float(row[lonIndex])
            
            # Create x,y coordinate pair for the current row
            point = (lon,lat)
            
            # Check if current lap number exists in lapDictionary
            if not lap in lapDictionary:
            # If not:
                # Create a new list with only one point
                points = [point]
                
                # Create new entry for lap in lapDictionary
                lapDictionary[lap] = points
                
            else:
                # Update the information for current lap in lapDictionary
                points = lapDictionary[lap]
                points.append(point)
            
    return lapDictionary

def gpsTracks(output, lapDictionary):
    import arcpy, os
    arcpy.env.overwriteOutput = True
    
    # Create new polyline feature class using WGS84
    sr = arcpy.SpatialReference(4326)
    outputFolder = os.path.dirname(output)
    outputFile = os.path.basename(output)
    arcpy.CreateFeatureclass_management(outputFolder, outputFile, "POLYLINE", "", "", "", sr)
    arcpy.AddField_management(output, "lapNo", "SHORT")
    
    # Add polyline features created from coordinates in lapDictionary
    with arcpy.da.InsertCursor(output, ("SHAPE@", "lapNo")) as cursor:
        for lap in lapDictionary:
            points = lapDictionary[lap]
            cursor.insertRow((points, lap))
    del cursor

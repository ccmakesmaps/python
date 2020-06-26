# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 15:45:50 2020
@author: Chelsea Richardson

Takes NHL player point data and generates separate shapefiles containing
the records for players of specified positions who come from a given nation.
Then adds and calculates fields containing player height and weight in metric units.
"""

import arcpy
arcpy.env.overwriteOutput = True

# Tool parameters - edit these to change the positions or nation of interest
# Position Codes: RW = Right Wing, LW = Left Wing, C = Center, D = Defenseman, G = Goaltender
nationOfOrigin = "Sweden"
positionCodes = ["LW", "RW", "C"]

# Workspace path, input shapefiles, and their relevant field names
arcpy.env.workspace = "C:\\PSU\\02_GEOG485\\Lesson3\\Data"
countries = "Countries_WGS84.shp"
players = "nhlrosters.shp"
countryName = "CNTRY_NAME"
playerPosition = "position"

try:
    for positionCode in positionCodes:
        whereCountry = countryName + " =  '" + nationOfOrigin + "'"
        selectionCountryLayer = arcpy.SelectLayerByAttribute_management(countries, 'NEW_SELECTION', whereCountry)
        playersLayer = arcpy.SelectLayerByLocation_management(players, 'WITHIN', selectionCountryLayer)
        wherePosition = playerPosition + " =  '" + positionCode + "'"
        playersSubLayer = arcpy.SelectLayerByAttribute_management(playersLayer, 'SUBSET_SELECTION', wherePosition)
        
        # Execute Copy Features and Add Fields
        outputFC = "nhlRoster_" + nationOfOrigin + "_" + positionCode + ".shp"
        arcpy.CopyFeatures_management(playersSubLayer, outputFC)
        fields = ["weight", "weight_kg", "height", "height_cm"]
        arcpy.AddFields_management(outputFC, [["weight_kg", "FLOAT"], ["height_cm", "FLOAT"]])

        # Use update cursor to populate metric height and weight fields
        with arcpy.da.UpdateCursor(outputFC, fields) as cursor:
            for row in cursor:
                # Convert weight to kg and height to cm
                row[1] = row[0] * 0.453592
                feet, inches = row[2].rsplit("' ", 1)
                inches = inches[:-1]
                row[3] = ((int(feet) * 12) + int(inches)) * 2.54
                cursor.updateRow(row)        
        del row, cursor
        
except:
    print (arcpy.GetMessages())
 
finally:
    arcpy.Delete_management(playersLayer)
    arcpy.Delete_management(selectionCountryLayer)
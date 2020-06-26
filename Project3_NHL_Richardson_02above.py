# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 15:45:50 2020
@author: Chelsea Richardson

Takes NHL player point data and generates separate shapefiles containing
the records for players of specified positions who come from a given nation.
Then adds and calculates fields containing player height and weight in metric units.
Then adds and populates a field containing each player's zodiac sign based on their birthdate.
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
        fields = ["weight", "weight_kg", "height", "height_cm", "birthDate", "zodiac"]
        arcpy.AddFields_management(outputFC, [["weight_kg", "FLOAT", 6], ["height_cm", "FLOAT", 6], ["zodiac", "TEXT", 12]])

        # Use update cursor to populate metric height and weight fields and the zodiac sign field
        with arcpy.da.UpdateCursor(outputFC, fields) as cursor:
            for row in cursor:
                # Convert weight to kg and height to cm
                row[1] = row[0] * 0.453592
                feet, inches = row[2].rsplit("' ", 1)
                inches = inches[:-1]
                row[3] = ((int(feet) * 12) + int(inches)) * 2.54
                cursor.updateRow(row)
                # Convert birthDate to string and populate the zodiac sign field
                bdaystr = str(row[4])
                year, strmonth, rest = bdaystr.rsplit("-", 2)
                month = int(strmonth)
                strday = rest[:-9]
                day = int(strday)
                if month == 1: 
                    row[5] = 'Capricorn' if (day < 20) else 'Aquarius'
                    cursor.updateRow(row)
                elif month == 2: 
                    row[5] = 'Aquarius' if (day < 19) else 'Pisces'
                    cursor.updateRow(row)
                elif month == 3: 
                    row[5] = 'Pisces' if (day < 21) else 'Aries'
                    cursor.updateRow(row)
                elif month == 4: 
                    row[5] = 'Aries' if (day < 20) else 'Taurus'
                    cursor.updateRow(row)
                elif month == 5: 
                    row[5] = 'Taurus' if (day < 21) else 'Gemini'
                    cursor.updateRow(row)
                elif month == 6: 
                    row[5] = 'Gemini' if (day < 21) else 'Cancer'
                    cursor.updateRow(row)
                elif month == 7: 
                    row[5] = 'Cancer' if (day < 23) else 'Leo'
                    cursor.updateRow(row)
                elif month == 8: 
                    row[5] = 'Leo' if (day < 23) else 'Virgo'
                    cursor.updateRow(row)
                elif month == 9: 
                    row[5] = 'Virgo' if (day < 23) else 'Libra'
                    cursor.updateRow(row)
                elif month == 10: 
                    row[5] = 'Libra' if (day < 23) else 'Scorpio'
                    cursor.updateRow(row)
                elif month == 11: 
                    row[5] = 'Scorpio' if (day < 22) else 'Sagittarius'
                    cursor.updateRow(row)
                elif month == 12: 
                    row[5] = 'Sagittarius' if (day < 22) else 'Capricorn'
                    cursor.updateRow(row)
        del row, cursor
        
except:
    print (arcpy.GetMessages())
 
finally:
    arcpy.Delete_management(playersLayer)
    arcpy.Delete_management(selectionCountryLayer)
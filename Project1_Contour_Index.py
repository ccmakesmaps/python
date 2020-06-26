# -*- coding: utf-8 -*-
"""
Created on Mon May 25 20:43:50 2020

@author: Chelsea Richardson

Creates contour shapefile from DEM input.
Contour interval units will match those of the DEM input.

Requires Spatial Analyst.
"""

import arcpy
from arcpy.sa import Contour
arcpy.env.overwriteOutput = True

try:
    # Set variables for Contour tool and index contour field
    inputRaster = "C:/PSU/02_GEOG485/Lesson1/Data/foxlake"
    outputShapefile = "C:/PSU/02_GEOG485/Lesson1/Data/foxlake_contour.shp"
    contourInterval = 25
    baseContour = 0
    fieldName = "Index100m"
    expression = "getClass(int(!Contour!))"
    
    codeblock = """
def getClass(Contour):
    if Contour % 100 == 0:
        return 1
    else:
        return 0"""

    # Execute Contour (Spatial Analyst)
    Contour(inputRaster, outputShapefile, contourInterval, baseContour)

    # Execute Add Field (Data Management)
    arcpy.AddField_management(outputShapefile, fieldName, "SHORT", 2)
    
    # Execute Calculate Field (Data Management)
    arcpy.CalculateField_management(outputShapefile, fieldName, expression, "PYTHON3", codeblock)

    # Report successful completion
    arcpy.AddMessage("Huzzah!")
    
    # Print details to IPython console
    print (arcpy.GetMessages())

except:
    # Report an error message
    arcpy.AddError("Could not complete contour generation")
    
    # Report any error messages that the Contour tool generated
    arcpy.AddMessage(arcpy.GetMessages())
    
    # Print details to IPython console
    print (arcpy.GetMessages())
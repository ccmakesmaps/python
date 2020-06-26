# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 16:08:48 2020

@author: Chelsea Richardson

Script iterates through all vector datasets in input container, reprojecting
them to match the coordinate system of a specified input vector dataset.
"""

import arcpy
import os
arcpy.env.overwriteOutput = True

# Tool parameters - target folder and feature class with target coordinate system
targetFolder = arcpy.GetParameterAsText(0)
inputFC = arcpy.GetParameterAsText(1)

# Get the target coordinate system from the user-provided feature class
outSpatialRef = arcpy.Describe(inputFC).spatialReference

# Set the workspace from the user-provided folder or gdb path
arcpy.env.workspace = targetFolder

# List all feature classes within the workspace
featureClassList = arcpy.ListFeatureClasses()

# Define a list for feature classes that get reprojected
outFeatureClasses = []

try:
    # Loop through each feature class in the list
    for featureClass in featureClassList:
    
        # First check to make sure fc has a defined coordinate system
        # Then check that it is different from the target coordinate system
        # Else, run the Project tool
        inSpatialRef = arcpy.Describe(featureClass).spatialReference
            
        if inSpatialRef.Name == "Unknown":
            print (featureClass + " is missing coordinate system information and cannot be projected.")
        
        elif inSpatialRef.Name == outSpatialRef.Name:
            print (featureClass + " is already in the target projection. Hooray!")
        
        else:
            # Use if-else to account for shapefile extension
            rootName = featureClass

            if rootName.endswith(".shp"):
                rootName = rootName.replace(".shp","")
                
                outFC = os.path.join(targetFolder, rootName + "_project.shp")
                
            else:
                outFC = os.path.join(targetFolder, featureClass + "_project")
            
            # Run Project tool
            arcpy.Project_management(featureClass, outFC, outSpatialRef)
            outFeatureClasses.append(featureClass)
            print("Project Run #" + str(len(outFeatureClasses)) + "... " + arcpy.GetMessages())
            
           
    # Print messages
    print("Script successful. Huzzah!")
    
    if len(outFeatureClasses) > 1:
        outFCList = ", ".join(outFeatureClasses)
        others, last = outFCList.rsplit(',', 1)
        print(str(len(outFeatureClasses)) + " output feature classes were created.")
        print(others + " and" + last + " were reprojected to the target coordinate system, which is " + outSpatialRef.Name + ".")

    elif len(outFeatureClasses) == 0:
        print("No feature classes were reprojected. Everything within the specified container is already in " + outSpatialRef.Name + ".")
     
    else:
        outFCList = "".join(outFeatureClasses)
        print(str(len(outFeatureClasses)) + " output feature class was created.")
        print(outFCList + " was reprojected to the target coordinate system, which is " + outSpatialRef.Name + ".")

except:
    # Print error messages
    print("Something is rotten in the state of Denmark. Please see error message(s).")
    print(arcpy.GetMessages(2))

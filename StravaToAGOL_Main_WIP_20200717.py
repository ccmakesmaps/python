# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 11:13:25 2020

@author: Chelsea Richardson

PSU GEOG485 Final
Script takes a Strava export zip archive, gets new activities since its last run,
and processes them to be appended to existing ArcGIS Online hosted feature layer.
"""

import datetime, StravaToAGOL

workspace = r"C:\PSU\02_GEOG485\Final\data"

# Specify the zip file downloaded from Strava
stravazip = r"C:\PSU\02_GEOG485\Final\data\_archive\export_1267461_200224.zip" # Make this an input parameter for script tool when finished

# CSV tables
exportCSV = "activities.csv" # This is always the file name in the Strava export archive
historyCSV = "StravaUpdateHistory.csv" # Read at start, write at end
#oldCSV = "activities_20200224.csv" # Get this string from historyCSV in 1st function
updateCSV = "activities_" + datetime.today().strftime('%Y%m%d') + ".csv" # This is the table of Strava activities to be pushed to AGOL

# Geoprocessing variables
targetGDB = r"C:\PSU\02_GEOG485\Final\GEOG485Final\GEOG485Final.gdb"
gpsFolder = r"C:\PSU\02_GEOG485\Final\data\activities" # Make sure this folder is empty before running

# Get a list of Activity IDs previously added to AGOL
existActIDs, oldCSV = StravaToAGOL.listOldActivities(historyCSV)
    
# Extract the activities table from the Strava zip archive
# and write CSV table of all current activities omitting unwanted fields and rows
StravaToAGOL.writeUpdateCSV(stravazip, exportCSV, updateCSV)
    
# Extract just new activities from GPS files in the Strava archive
StravaToAGOL.extractGPSfiles(stravazip, oldCSV, updateCSV)
    
# Convert the extracted GPS files to CSV files containing coordinates
runInfo = StravaToAGOL.GPStoCSV(gpsFolder)
    
# Convert the CSV files to polyline features and write them to a FC
# then join attribute table, then add fields used in OpsDash
appendFC = StravaToAGOL.CSVtoFC(gpsFolder, targetGDB)
    
# Update the StravaHistory log CSV (WIP - not tested yet)
StravaToAGOL.updateHistory(historyCSV, updateCSV, appendFC)
    
print("Script successful. See details in " + historyCSV)

# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 11:13:25 2020

@author: Chelsea Richardson
"""
# Functions for Strava dashboard update script

# Function: get list of old activities
#   open history log CSV and read last row to get old activities CSV
#   open old activities csv
#   put ActivityID values into a list
#   return list existActIDs
def listOldActivities(historyCSV):
    import csv
    # Create a list to store Activity IDs of features already on AGOL
    existActIDs = []
    with open(oldCSV, "r") as oldActivities:
        # Set up CSV reader and get Activity ID field index from the header
        csvReader = csv.reader(oldActivities)
        header = next(csvReader)
        actidIndex = header.index("Activity ID")
    # Use For loop to get Activity IDs and add them to list of existing Activity IDs
    for row in csvReader:
        existActIDs.append(str(row[actidIndex]))
    return [existActIDs, oldCSV]

# Function: write csv of new activities
#   extract activities.csv from zip file
#   put activity IDs and attributes into a dictionary
#   use dictionary to write run/ride rows that have Filename to updateCSV
def writeUpdateCSV(stravazip, exportCSV, updateCSV):
    import csv, zipfile
    # Create a dictionary to store attributes of each activity
    actDictionary = {}
    # unzip just activities.csv from the zip file
    with zipfile.ZipFile(stravazip, "r") as datazip:
        datazip.extract(exportCSV)
        
    with open(exportCSV, "r") as exportActivities:
        # Set up CSV reader and get field indices from the header
        csvReader = csv.reader(exportActivities)
        header = next(csvReader)
        actidIndex = header.index("Activity ID")
        dateIndex = header.index("Activity Date")
        nameIndex = header.index("Activity Name")
        typeIndex = header.index("Activity Type")
        timeIndex = header.index("Elapsed Time")
        distIndex = header.index("Distance")
        fileIndex = header.index("Filename")
    
        # Use For loop to populate actDictionary with attributes
        for row in csvReader:
            # Create list to contain attributes
            attributes = [row[dateIndex], row[nameIndex], row[typeIndex], row[timeIndex], row[distIndex], row[fileIndex]]
            actID = row[actidIndex]
            actDictionary[actID] = attributes
        
    headerCleanup = ["Activity Description", "Relative Effort", "Commute", "Activity Gear"]
    for fieldName in headerCleanup:
        header.remove(fieldName)

    with open(updateCSV, "w", newline='') as outTable:
        fieldnames = ",".join(header)
        csvWriter = csv.writer(outTable)
        csvWriter.writerow(header)

        for key, value in actDictionary.items():
#WIP        #if value[2] == "run","ride" and value[5] is not null:
            # create a list with the key and values together
            value.insert(0, key)
            # write the row with this list
            csvWriter.writerow(value)
#WIP        #else: pass

# Function: extract just the new activities from the zipped gps files
#   use "update csv" to make a list from the Filename field
#   use "old csv" to remove from that list the files that have already been processed
#   use list to extract just the new files in "update csv" from the zip archive
def extractGPSfiles(stravazip, oldCSV, updateCSV):
    import csv, zipfile
    # Create a list for the Filename field, compare updateCSV to oldCSV, then extract just the new files
    gpsFiles = []
    with open(updateCSV, "r") as updateTable:
        csvReader = csv.reader(updateTable)
        header = next(csvReader)
        fileIndex = header.index("Filename")
        # Use For loop to get filenames and add them to list of gpsFiles to be extracted
        for row in csvReader:
            gpsFiles.append(str(row[fileIndex]))

    with open(oldCSV, "r") as existTable:
        csvReader = csv.reader(existTable)
        header = next(csvReader)
        fileIndex = header.index("Filename")
        # Use For loop to get old filenames and remove them from list of gpsFiles to be extracted
        for row in csvReader:
            gpsFiles.remove(str(row[fileIndex]))

    # Unzip each item still in list gpsFiles from the zip archive
    with zipfile.ZipFile(stravazip, 'r') as datazip:
        for Filename in gpsFiles:
            datazip.extract(Filename)

# Function: convert the extracted gps files to csv
#   run through activities folder of unzipped gps files;
#   use gzip to decompress any .gz files; convert .fit to .gpx; then convert all to .csv
def GPStoCSV(gpsFolder):
    import csv, os, gzip, shutil #, fitparse, pytz
    from gpx_csv_converter import Converter
    # Get a list of files in gpsFolder
    gpsFiles = os.listdir(gpsFolder)

    # First handle the .gz files
    for gpsFile in gpsFiles:
        if gpsFile.endswith(".gz"):
            outfile = gpsFile.replace(".gz","")
            #call on gzip function to decompress the file in same folder
            with gzip.open(gpsFile, "rb") as f_in:
                with open(outfile, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
            # Delete the .gz version of the file
            os.remove(gpsFile)
        else:
            pass

    # Refresh the file list
    gpsFiles = os.listdir(gpsFolder)
    # Next, repeat the For loop to ensure all gps files are in .gpx format
    for gpsFile in gpsFolder:
        if gpsFile.endswith(".fit"):
            # convert fit to gpx
            ## WIP - need to figure out how to parse FIT files
        else:
            pass

    # Refresh the file list
    gpsFiles = os.listdir(gpsFolder)
    # Then repeat the For loop a final time to convert all gpx files to csv
    for gpsFile in gpsFolder:
        if gpsFile.endswith(".gpx"):
            csvFile = gpsFile.replace(".gpx",".csv")
            # Convert gpx to csv
            Converter(gpsFile,csvFile)
            # Delete the gpx file
            os.remove(gpsFile)            
        else:
            print("Check it: " + gpsFile + " not converted.")

## WIP - this function is not yet finished
# Function: convert the csv files to features in a polyline FC, then join the table and add fields for AGOL display
#   run through .csv files, store ID and coords as key and values in a dictionary
#   write each line of the dictionary to a polyline feature in appendFC
#   join the "update csv" table to appendFC
#   add fields for AGOL, then use update cursor to populate the new fields
def CSVtoFC(gpsFolder, targetGDB):
    import arcpy, csv, os
    arcpy.env.overwriteOutput = True
    
    # Make a list of gpsFiles in gpsFolder
    gpsFiles = os.listdir(gpsFolder)
    
    # Create a dictionary to store coordinate pairs of each activity
    actDictionary = {}
    
    for gpsFile in gpsFiles:
        # Open the CSV file
        with open(csvFile, "r") as actGPS:
            actID = csvFile.replace(".csv","")
            # Set up CSV reader and get lat and lon field indices from the header
            csvReader = csv.reader(actGPS)
            header = next(csvReader)
            latIndex = header.index("latitude")
            lonIndex = header.index("longitude")
            
            # Loop through the lines in the file to get lat and lon coordinates
            for row in csvReader:
                lat = float(row[latIndex])
                lon = float(row[lonIndex])
                
                # Create x,y coordinate pair for the current row
                point = (lon,lat)
                
                # Check if current actID exists in lapDictionary
                if not actID in actDictionary:
                    # If not:
                    # Create a new list with only one point
                    points = [point]
                    
                    # Create new entry for lap in actDictionary
                    actDictionary[actID] = points
                    
                else:
                    # Update the information for current actID in actDictionary
                    points = actDictionary[actID]
                    points.append(point)
    
    # Create new polyline feature class using WGS84
    sr = arcpy.SpatialReference(4326)
    appendFC = "append_" + datetime.today().strftime('%Y%m%d')
    arcpy.CreateFeatureclass_management(targetGDB, appendFC, "POLYLINE", "", "", "", sr)
    ## WIP arcpy.AddFields_management(appendFC, [["fieldname0", "SHORT"], ["fieldname1", "TEXT", 20]])
    
    # Add polyline features created from coordinates in actDictionary
    with arcpy.da.InsertCursor(output, ("SHAPE@", "actID")) as cursor:
        for actID in actDictionary:
            points = actDictionary[actID]
            cursor.insertRow((points, actID))
    del cursor
    return appendFC

## WIP - this entire function is not tested yet, just pieced together
# Function: update the history log csv
#   open StravaHistory.csv and write one new row
#   date, # of features added (run, ride), total # of features after append, csv Filename
def updateHistory(historyCSV, updateCSV, appendFC):
    import csv, arcpy
    
    # Get the number of new run activities
    in_rows = arcpy.SelectLayerByAttribute_management(appendFC, "NEW_SELECTION", "[ActivityType] = 'Run'")
    newRuns = arcpy.GetCount_management(in_rows)
    
    # Get the number of new ride activities
    in_rows = arcpy.SelectLayerByAttribute_management(appendFC, "NEW_SELECTION", "[ActivityType] = 'Ride'")
    newRides = arcpy.GetCount_management(in_rows)
    
    # Get a list of all activities that have been processed
    ActivityIDs = []
    with open(updateCSV, "r") as Activities:
        # Set up CSV reader and get Activity ID field index from the header
        csvReader = csv.reader(Activities)
        header = next(csvReader)
        actidIndex = header.index("Activity ID")
    # Use For loop to get Activity IDs and add them to list of existing Activity IDs
    for row in csvReader:
        ActivityIDs.append(str(row[actidIndex]))
    
    # Create list containing info to write to the history log csv
    runInfo = [str(datetime.today().strftime('%Y%m%d')), str(newRuns), str(newRides), str(len(ActivityIDs)), updateCSV]
    runInfo = ",".join(runInfo)
    with open(updateCSV, "w", newline='') as outTable:
        csvWriter = csv.writer(outTable)
        # write the row
        csvWriter.writerow("date, # of features added (run, ride), total # of features after append, csv Filename")
  
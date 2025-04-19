# This script takes the geometries from the City of Chicago's bike lane datasets from the current year and an older year.
# Any bike lanes still existing in the current dataset are removed from the older dataset. Polylines are created from the geometries
# and the separate polyline features are dissolved into a single polyline per bike lane. Current bike lanes are labeled current and
# and older bike lanes are not longer in the current dataset are labeled as archived in the status field.
def removeKey(key, dictionary):
    if key in dictionary:
       del dictionary[key]

# Importing arcpy, allowing overwriting and setting my workspace
import arcpy
arcpy.env.overwriteOutput = True
arcpy.env.workspace = r"C:\PSU\Geog485\FinalLesson"

# Setting my variables
# Setting the file paths for the bike lane datasets
newBL = r"C:\PSU\Geog485\FinalLesson\Bike_Routes_New.shp"
oldBL = r"C:\PSU\Geog485\FinalLesson\CDOT_Bikeways_2016_0311_20241017.csv"
currentBL = r"C:\PSU\Geog485\FinalLesson\Bike_Routes_20241015.csv"

# Creating empty dictionaries to hold geometry data
dicCBL = {}
dicOBL = {}

# Getting the spatial reference from the current bike lane dataset
sr = arcpy.SpatialReference(4326)
spatial_reference = sr

# Creating a new bike lane dataset
bikeLaneFC = arcpy.management.CreateFeatureclass(arcpy.env.workspace, "BikeLane.shp", "POLYLINE", "", "", "", spatial_reference)

# Adding the STATUS field to the new bike lane dataset
arcpy.management.AddField(bikeLaneFC, "HISTORICAL", "TEXT")
statusField = "HISTORICAL"
# Adding the Bike_Lane field to hold the bike lane name
arcpy.management.AddField(bikeLaneFC, "Bike_Lane", "TEXT")
bikeLaneNameField = "Bike_Lane"

# Creating a variable to hold the fields the dissolve will be set on
dissolveFields = [bikeLaneNameField, statusField]

import csv

# Opening the current bike lane dataset and extracting coordinates
with open(currentBL, "r") as bikeLaneFile:
    csvReader = csv.reader(bikeLaneFile)
    header = next(csvReader)
    print(header)
    bikeLaneNameIndex = header.index("STREET")
    print(bikeLaneNameIndex)
    bikeLaneGeoIndex = header.index("the_geom")
    print(bikeLaneGeoIndex)
    for row in csvReader:
        bikeLaneStreet = row[bikeLaneNameIndex]
        bikeLaneGeo = row[bikeLaneGeoIndex]
        if row[bikeLaneNameIndex] in dicCBL:
           blGeometries = dicCBL[bikeLaneStreet]
           blGeometries.append([bikeLaneGeo])
        else:
           dicCBL[bikeLaneStreet] = [[bikeLaneGeo]]
           blGeometries = dicCBL[bikeLaneStreet]
           blGeometries.append([bikeLaneGeo])

# Opening the Old Bike Lane Data and extracting coordinates
with open(oldBL, "r") as oldBikeLaneFile:
     csvReader = csv.reader(oldBikeLaneFile)
     header = next(csvReader)
     print(header)
     bikeLaneNameIndex = header.index("STREET")
     print(bikeLaneNameIndex)
     bikeLaneGeoIndex = header.index("the_geom")
     print(bikeLaneGeoIndex)
     for row in csvReader:
         bikeLaneStreet = row[bikeLaneNameIndex]
         bikeLaneGeo = row[bikeLaneGeoIndex]
         if row[bikeLaneNameIndex] in dicOBL:
              blGeometries = dicOBL[bikeLaneStreet]
              blGeometries.append([bikeLaneGeo])
         else:
              dicOBL[bikeLaneStreet] = [[bikeLaneGeo]]
              blGeometries = dicOBL[bikeLaneStreet]
              blGeometries.append([bikeLaneGeo])

# Deleting the empty keys from the dictionaries
key_to_delete = ""
removeKey(key_to_delete, dicCBL)
removeKey(key_to_delete, dicOBL)


# Deleting the keys for bike lanes in the older dataset that still exist in the current dataset
for key in list(dicCBL):
    if key in dicOBL:
       del dicOBL[key]

# Gathering the geometry data and creating array coordinate points from the current bike lane dataset
for bikeLane in dicCBL:
        with arcpy.da.InsertCursor(bikeLaneFC, ["SHAPE@", statusField, bikeLaneNameField]) as cursor:
            polylineArray = arcpy.Array()
            print("I am working on " + bikeLane)
            # Looping through the dictionary
            bikeLaneCoords = dicCBL[bikeLane]
            for item in bikeLaneCoords:
                # Looping through each string in the key values
                for string in item:
                    # Replacing 'MULTILINESTRING' and the outer ()
                    coords_str = string.replace('MULTILINESTRING ((', '').replace('))', '').replace(')', '').replace('(', '').replace('MULTILINESTRING', '')
                    print(coords_str)
                    # Splitting the string into coordinate pairs on the ','
                    coords_points = coords_str.split(",")
                    # Looping through the coordinate pairs
                    for coord_pair in coords_points:
                    # Splitting the coordinate pairs on the ''
                        coord_point = coord_pair.split()
                        lat = coord_point[0]
                        long = coord_point[1]
                        currentPoint = arcpy.Point(float(lat),float(long))
                        polylineArray.add(currentPoint)
                polyline = arcpy.Polyline(polylineArray, sr)
                cursor.insertRow((polyline,"No", bikeLane))
                polylineArray.removeAll()

# Gathering the geometry data and creating array coordinate points from the old bike lane dataset
for bikeLane in dicOBL:
        with arcpy.da.InsertCursor(bikeLaneFC, ["SHAPE@", statusField, bikeLaneNameField]) as cursor:
            polylineArray = arcpy.Array()
            print("I am working on " + bikeLane)
            # Looping through the dictionary
            bikeLaneCoords = dicOBL[bikeLane]
            for item in bikeLaneCoords:
                # Looping through each string in the key values
                for string in item:
                    # Replacing 'MULTILINESTRING' and the outer ()
                    coords_str = string.replace('MULTILINESTRING ((', '').replace('))', '').replace(')', '').replace('(', '').replace('MULTILINESTRING', '')
                    print(coords_str)
                    # Splitting the string into coordinate pairs on the ','
                    coords_points = coords_str.split(",")
                    # Looping through the coordinate pairs
                    for coord_pair in coords_points:
                    # Splitting the coordinate pairs on the ','
                        coord_point = coord_pair.split()
                        lat = coord_point[0]
                        long = coord_point[1]
                        currentPoint = arcpy.Point(float(lat),float(long))
                        polylineArray.add(currentPoint)
                # Creating the polyline from the array points
                polyline = arcpy.Polyline(polylineArray, sr)
                cursor.insertRow((polyline,"Yes", bikeLane))
                polylineArray.removeAll()

# Dissolving the bike lane segments into single polylines based on bike lane name
arcpy.management.Dissolve(bikeLaneFC, newBL, dissolveFields)








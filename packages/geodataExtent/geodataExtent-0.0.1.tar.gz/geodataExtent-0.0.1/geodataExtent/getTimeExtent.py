import csv
import os
import sys
import json
import functools
import math
import sqlite3
import time as timeMod

# add local modules folder
file_path = '../Python_Modules'
sys.path.append(file_path)

from osgeo import gdal, ogr, osr
import click
import netCDF4 as nc
import pandas as pd
import pygeoj
import shapefile
import xarray as xr
import ogr2ogr
from DateTime import DateTime
from datetime import date


# asking for parameters in command line
@click.command()
@click.option('--path', prompt="File path", help='Path to file')
@click.option('--name', prompt="File name", help="File name with extension")
@click.option('--clear', default=False, help='Argument wether you want to display only the Output \nOptions: 1, yes, y and true')
def main(path, name, clear):
    res = getTimeExtent(name, path)
    if clear:
        click.clear()
    if res[0] != None:
        click.echo(res[0])
    else:
        click.echo(res[1])

def getTimeExtent(name, path):
    """
    returns the bounding Box of supported Datatypes and standards in WGS84.
    
    supported data: Shapefile (.shp), GeoJson (.json/.geojson), GeoTIFF (.tif), netCDF (.nc),
                    GeoPackage (.gpkg), alle ISO19xxx standardisiete Formate, CSV on the web
    
    @param path Path to the file
    @param name name of the file with extension
    @returns a boundingbox as an array in WGS84, formated like [minLong, minLat, maxLong, maxLat]
    """
    # connect name and path to file
    filepath = "%s\%s" % (path, name)
    # get file extension
    filename, file_extension = os.path.splitext(filepath)
    # print(file_extension)
    # netCDF handeling
    if file_extension == ".nc":
        try:
            # https://gis.stackexchange.com/questions/270165/gdal-to-acquire-netcdf-like-metadata-structure-in-python
            ds = xr.open_dataset(filepath)
            # transform coordinates section in a dictionary
            time = ds.to_dict()['coords']['time']['data']
            isoTimeSeq = list(map(DateTime,(list(map(str, time)))))
            isoTimeSeq.sort()
            avgInt = 0
            if len(isoTimeSeq) > 1:
                interval = []

                for i in range(len(isoTimeSeq)-1):
                    interval.append(isoTimeSeq[i+1] - isoTimeSeq[i])
                
                avgInt = functools.reduce(lambda x, y: x + y, interval) / float(len(interval))
                # avgInt = math.floor(avgInt*1000)/1000
                # print(avgInt)
            
            return ([str(isoTimeSeq[0]), str(isoTimeSeq[-1]), avgInt],None)

            
        # errors
        except KeyError:
            return (None, "'time' may be spelled wrong: should be 'time")
        except:
            return (None, "File Error!")

    elif file_extension == ".csv" or file_extension == ".txt":
        # column name should be either date, time or timestamp

         # @see https://stackoverflow.com/questions/16503560/read-specific-columns-from-a-csv-file-with-csv-module
        try: # finding the correct collums for latitude and longitude
            csvfile = open(filepath)
            head = csv.reader(csvfile, delimiter=' ', quotechar='|')
            # get the headline and convert, if possible, ';' to ',' 
            # and seperate each word devided by a ',' into an array 
            header = next(head)[0].replace(";", ",").split(",")
            time = None
            # searching for valid names for latitude and longitude
            for t in header:
                if t == "date":
                   time = "date"
                if t == "time":
                    time = "time"
                if t == "timestamp":
                    time = "timestamp"

            # if there is no valid name or coordinates, an exception is thrown an cought with an errormassage
            if(time == None):
                raise ValueError("pleas rename timestamp to: date/time/timestamp")
        # errors
        except ValueError as e:
            return (None, e)
        except:
            return (None, "File Error!")
        
        # if no error accured
        else:
            try:
                df = pd.read_csv(filepath, header=0)
                # get time from found columns
                timestamp = df[time].tolist()

                isoTimeSeq = list(map(DateTime,(list(map(str, timestamp)))))
                isoTimeSeq.sort()
                avgInt = 0
                if len(isoTimeSeq) > 1:
                    interval = []

                for i in range(len(isoTimeSeq)-1):
                    interval.append(isoTimeSeq[i+1] - isoTimeSeq[i])
                
                avgInt = functools.reduce(lambda x, y: x + y, interval) / float(len(interval))
                # avgInt = math.floor(avgInt*1000)/1000
                # print(avgInt)
            
                return ([str(isoTimeSeq[0]), str(isoTimeSeq[-1]), avgInt], None)

            # in case the words are separated by a ';' insted of a comma
            except KeyError:
                try:
                    # tell the reader that the seperator is a ';'
                    df = pd.read_csv(filepath, header=0, sep=';')
                    # get all coordinates from found collums
                    timestamp = df[time].tolist()
                    
                    isoTimeSeq = list(map(DateTime,(list(map(str, timestamp)))))
                    isoTimeSeq.sort()
                    avgInt = 0
                    if len(isoTimeSeq) > 1:
                        interval = []

                    for i in range(len(isoTimeSeq)-1):
                        interval.append(isoTimeSeq[i+1] - isoTimeSeq[i])
                    
                    avgInt = functools.reduce(lambda x, y: x + y, interval) / float(len(interval))
                    # avgInt = math.floor(avgInt*1000)/1000
                    # print(avgInt)
                
                    return ([str(isoTimeSeq[0]), str(isoTimeSeq[-1]), avgInt], None)
                # the csv is not valid
                except KeyError:
                    return (None, "Pleas seperate your data with either ',' or ';'!" )
            # errors
            except:
                return (None, "File Error: File not found or check if your csv file is valid to 'csv on the web'")

    elif file_extension == ".json" or file_extension == ".geojson":
        ds = open(filepath)
        jsonDict = json.load(ds)
        isoTimeSeq = []
        if jsonDict["type"] == "FeatureCollection":
            prop = ""
            if "time" in jsonDict["features"][0]:
                prop = "time"
            elif "date" in jsonDict["features"][0]:
                prop = "date"
            else:
                return (None, "no time data available")

            timeext = []
            for feature in jsonDict["features"]:
                timeext.append(feature["properties"][prop])
            isoTimeSeq = list(map(DateTime, timeext))

            isoTimeSeq.sort()
            avgInt = 0
            if len(isoTimeSeq) > 1:
                interval = []

            for i in range(len(isoTimeSeq)-1):
                interval.append(isoTimeSeq[i+1] - isoTimeSeq[i])
            
            avgInt = functools.reduce(lambda x, y: x + y, interval) / float(len(interval))
            # print(avgInt)
        
            return ([str(isoTimeSeq[0]), str(isoTimeSeq[-1]), avgInt], None)
        else:
            prop = ""
            if "time" in jsonDict:
                prop = "time"
            elif "date" in jsonDict:
                prop = "date"
            else:
                return (None, "no time data available")

            timeext = jsonDict["properties"]["time"]
            timeext = DateTime(timeext)
            return ([timeext, timeext, 0], None)


    elif file_extension == ".gpkg":
        try:
            conn = sqlite3.connect(filepath)
            c = conn.cursor()
            c.execute("""   SELECT last_change 
                            FROM gpkg_contents 
                    """)
            row = c.fetchone()
            row = list(map(DateTime, row))
            # print(row)
            return ([str(row[0]), str(row[0]), 0], None)
        except:
            return (None, "File Error!")
        finally:
            try:
                conn.close()
            except:
                pass

    elif file_extension == ".tif" or file_extension == ".tiff":
        # ds =  gdal.Open(filepath)
        # print(gdal.Info(ds))
        return (None, "Filetype %s not yet supported" % file_extension)
    
    else:
        return (None, "Filetype %s not yet supported" % file_extension)

# Main method
if __name__ == '__main__':
    main()

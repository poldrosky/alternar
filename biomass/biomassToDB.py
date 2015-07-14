#!/usr/bin/env python3

'This script process biomass map of Narino'

import os, sys, math, time, csv, io
import gdal
import numpy
import Pdbc

dataset = gdal.Open('biomass/biomass_narino.TIF')
geoTransform = dataset.GetGeoTransform()

cols = dataset.RasterXSize
rows = dataset.RasterYSize
pixelWidth = geoTransform[1]
pixelHeight = geoTransform[5]
originX = geoTransform[0]
originY = geoTransform[3]
array = dataset.ReadAsArray()

biomass = []
for x in range(rows):
    for y in range(cols):
        value = array[x][y]
        if (value!=0):
            latitude = originX + (y * pixelWidth)
            longitude = originY + (x * pixelHeight)
            biomass.append('{0}\t{1}\t{2}'.format(latitude, longitude, value)) 

biomass = '\n'.join(biomass)                
db = Pdbc.DBConnector('landsat', 'omar', '1234', 'localhost', '5432')
db.copyToTable('biomass',io.StringIO(biomass))

print('Done')



                        

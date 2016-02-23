#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  DNtoToAReflectanceL8.py
#  
#  Copyright 2016 Omar Ernesto Cabrera Rosero <omarcabrera@udenar.edu.co>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#


'This script process bands landsat 8, calculate radiance and reflectance and copy values of reflectace in db'

import os, sys, math, time, csv, io
import gdal
import numpy
import Pdbc

bandList = ['1','2','3','4','5','6','7','8','9','10']

class Landsat(object):
    def __init__(self, nameFolder):
        self.idLandsat = nameFolder
        self.metadata = self.readMetadata(self.idLandsat)
        self.getMetadata()

    def readMetadata(self, idLandsat):
        fileMTL = os.popen('ls '+idLandsat+'/*_MTL.txt').read().split('\n')[0]
        metadataFile = open(fileMTL,'r')
        metadata = {}
        for line in metadataFile:
            if not line.strip() == "END":
                val = line.strip().split('=')
                metadata [val[0].strip()] = val[1].strip().strip('"')
            else:
                break
        metadataFile.close()
        return metadata

    def acquireMetadata(self, band):

        metadatalist = []
    
        BANDFILE = "FILE_NAME_BAND_" + band
        ML = "RADIANCE_MULT_BAND_" + band
        AL  = "RADIANCE_ADD_BAND_" + band
        Mp = "REFLECTANCE_MULT_BAND_" + band
        Ap = "REFLECTANCE_ADD_BAND_" + band
        metadatalist = [BANDFILE, ML, AL, Mp, Ap]
        return metadatalist        

    def getMetadata(self):
        self.band = {}

        self.SE = self.metadata['SUN_ELEVATION']
        self.K1 = self.metadata['K1_CONSTANT_BAND_10']
        self.K2 = self.metadata['K2_CONSTANT_BAND_10']
        self.DATE = self.metadata['DATE_ACQUIRED']
        
        for b in bandList:
            metlist = self.acquireMetadata(b)
            BANDFILE = self.metadata[metlist[0]]
            ML = self.metadata[metlist[1]]
            AL = self.metadata[metlist[2]]            
            if (b!='10'):
                Mp = self.metadata[metlist[3]]
                Ap = self.metadata[metlist[4]]
            
            self.band[b] = Band(self.idLandsat, BANDFILE, ML, AL, Mp, Ap, b)
                                    
class Band(object):
    def __init__(self, idLandsat, BANDFILE, ML, AL, Mp, Ap, band):
        self.BANDFILE = BANDFILE
        self.ML = ML
        self.AL = AL
        self.Mp = Mp
        self.Ap = Ap
        self.band = band
        self.dataset = gdal.Open(idLandsat+'/'+BANDFILE, gdal.GA_ReadOnly)
        self.geoTransform = self.dataset.GetGeoTransform()
        self.cols = self.dataset.RasterXSize
        self.rows = self.dataset.RasterYSize
        self.pixelWidth = self.geoTransform[1]
        self.pixelHeight = self.geoTransform[5]
        self.originX = self.geoTransform[0]
        self.originY = self.geoTransform[3]
        self.array = self.dataset.ReadAsArray()
        
class Point(object):
    def __init__(self, landsat, x , y):
        self.landsat = landsat
        self.x = x
        self.y = y
        self.radiance = {}
        self.reflectance = {}
        self.DN = {}
        cols = landsat.band['1'].cols
        
        for b in bandList:
            if(b!='10'):
                if(landsat.band[b].cols == cols):
                    self.DN[b] = landsat.band[b].array[x][y]
                    self.reflectance[b] = self.calcReflectance(landsat.band[b].Mp, landsat.band[b].Ap, self.DN[b], landsat.SE)

                elif(landsat.band[b].cols > cols):
                    self.DN[b] = landsat.band[b].array[int(x/2)][int(y/2)]
                    self.reflectance[b] = self.calcReflectance(landsat.band[b].Mp, landsat.band[b].Ap, self.DN[b], landsat.SE)

            elif(b=='10'):
                self.DN[b] = landsat.band[b].array[x][y]
                self.radiance[b] = self.calcRadiance(landsat.band[b].ML, landsat.band[b].AL, self.DN[b])
                self.temp = self.calcTemp(landsat.K1, landsat.K2, self.radiance['10'])
                    
        self.idLandsat = landsat.idLandsat        
        self.pixelWidth = landsat.band[str(1)].pixelWidth
        self.pixelHeight = landsat.band[str(1)].pixelHeight
        self.originX = landsat.band[str(1)].originX
        self.originY = landsat.band[str(1)].originY
        self.latitude = self.originX + (y * self.pixelWidth)
        self.longitude = self.originY + (x * self.pixelHeight)
        
    def calcRadiance (self, ML,AL, DN):
        'This function calculate Conversion to TOA Radiance'    
        ML = float(ML)
        AL = float(AL)
        
        radiance = (ML * DN) + AL

        return radiance

    def calcReflectance (self, Mp, Ap, DN, SE):
        'This function calculate Conversion to TOA Reflectance'
        Mp = float(Mp)
        Ap = float(Ap)
        SE = float(SE)
        
        reflectanceWithoutCorrection = (Mp * DN) + Ap
        reflectance = reflectanceWithoutCorrection / (math.sin(math.radians(SE)))

        return reflectance

    def calcTemp (self, K1, K2, radiance):
        'This function calculate Temp'
        K1 = float(K1)
        K2 = float(K2)
        radiance = float(radiance)            

        temp = K2 / (math.log((K1/radiance)+1))

        return temp

def rasterToDB(nameFolders):
    for i in range(len(nameFolders)-1):
        #if os.path.isfile(nameFolders[i]):
        #    os.system('rm -R '+nameFolders[i].split('.')[0])
        #os.system('mkdir '+nameFolders[i].split('.')[0])
        #os.system('tar -xvf '+nameFolders[i]+' -C '+nameFolders[i].split('.')[0])              
        landsat = Landsat(nameFolders[i].split('.')[0])
        #date_landsat = '{0}\t{1}'.format(landsat.idLandsat, landsat.DATE)
        #db.copyToTable('date_landsat',io.StringIO(date_landsat))
        data = []
        discarded = []
        for x in range(0,landsat.band['1'].rows,30):
            for y in range(0,landsat.band['1'].cols,30):
                if(landsat.band['1'].array[x][y]==0 or landsat.band['2'].array[x][y]==0 or
                   landsat.band['3'].array[x][y]==0 or landsat.band['4'].array[x][y]==0 or
                   landsat.band['5'].array[x][y]==0 or landsat.band['6'].array[x][y]==0 or
                   landsat.band['7'].array[x][y]==0 or landsat.band['8'].array[x/2][y/2]==0 or
                   landsat.band['9'].array[x][y]==0 or landsat.band['10'].array[x][y]==0):
                     continue
                point = Point(landsat, x, y)
                data.append('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}\t{11}'.format(point.idLandsat,
                                                                                                  point.latitude,
                                                                                                  point.longitude,
                                                                                                  point.reflectance['1'],
                                                                                                  point.reflectance['2'],
                                                                                                  point.reflectance['3'],
                                                                                                  point.reflectance['4'],
                                                                                                  point.reflectance['5'],
                                                                                                  point.reflectance['6'],
                                                                                                  point.reflectance['7'],
                                                                                                  point.reflectance['8'],
                                                                                                  point.reflectance['9'],
                                                                                                  point.temp))
                print(point.latitude, point.longitude, point.DN['1'], point.DN['8'], point.reflectance['1'], point.reflectance['8'], point.temp)
                #input("prueba")

                                                      
        data = '\n'.join(data)
        discarded = '\n'.join(discarded)                
        #db.copyToTable('reflectance',io.StringIO(reflectance))
        #db.copyToTable('discarded',io.StringIO(discarded))
        #os.system('rm -R '+nameFolders[i].split('.')[0])	
                                  
path = os.getcwd()
path += '/L8'
os.chdir(path)

tiempo1 = time.time()

db = Pdbc.DBConnector('db', 'user', 'pass', 'ip', 'port')
                        
filterImg = 'LC8*'
nameFolders = os.popen('ls '+filterImg+'bz').read().split("\n")

rasterToDB(nameFolders)

tiempo2 = time.time()

print(tiempo2-tiempo1)

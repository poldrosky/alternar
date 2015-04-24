#!/usr/bin/env python3

'This script process bands landsat, calculate radiance and reflectance and copy values of reflectace in db'

import os, sys, math, time, csv, io
import gdal
import numpy
import Pdbc

bandList = ['1','2','3','4','5','61','7']

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
    
        if ("RADIANCE_MAXIMUM_BAND_" + band) in self.metadata.keys(): 
            BANDFILE = "FILE_NAME_BAND_" + band
            LMAX = "RADIANCE_MAXIMUM_BAND_" + band
            LMIN = "RADIANCE_MINIMUM_BAND_" + band
            QCALMAX = "QUANTIZE_CAL_MAX_BAND_" + band
            QCALMIN = "QUANTIZE_CAL_MIN_BAND_" + band
            DATE = "DATE_ACQUIRED"
            metadatalist = [BANDFILE, LMAX, LMIN, QCALMAX, QCALMIN, DATE]
            return metadatalist        

        elif ("LMAX_BAND" + band) in self.metadata.keys():
            BANDFILE = "BAND" + band + "_FILE_NAME"
            LMAX = "LMAX_BAND" + band
            LMIN = "LMIN_BAND" + band
            QCALMAX = "QCALMAX_BAND" + band
            QCALMIN = "QCALMIN_BAND" + band
            DATE ="ACQUISITION_DATE"
            metadatalist = [BANDFILE, LMAX, LMIN, QCALMAX, QCALMIN, DATE]
            return metadatalist
            
        elif(band == '61'):
            if ("RADIANCE_MAXIMUM_BAND_6_VCID_1") in self.metadata.keys():
                BANDFILE = "FILE_NAME_BAND_6_VCID_1"
                LMAX = "RADIANCE_MAXIMUM_BAND_6_VCID_1"
                LMIN = "RADIANCE_MINIMUM_BAND_6_VCID_1"
                QCALMAX = "QUANTIZE_CAL_MAX_BAND_6_VCID_1"
                QCALMIN = "QUANTIZE_CAL_MIN_BAND_6_VCID_1"
                DATE = "DATE_ACQUIRED"
                metadatalist = [BANDFILE, LMAX, LMIN, QCALMAX, QCALMIN, DATE] 
                return metadatalist

        else:
            print('There was a problem reading the metadata for this file.')

        return metadatalist
        
    def getMetadata(self):
        self.band = {}
        for b in bandList:
            metlist = self.acquireMetadata(b)
            BANDFILE = self.metadata[metlist[0]]
            LMAX = self.metadata[metlist[1]]
            LMIN = self.metadata[metlist[2]]
            QCALMAX = self.metadata[metlist[3]]
            QCALMIN = self.metadata[metlist[4]]
            self.DATE = self.metadata[metlist[5]]
            self.band[b] = Band(self.idLandsat, BANDFILE, LMAX, LMIN, QCALMAX, QCALMIN, self.DATE, b)
                                    
class Band(object):
    def __init__(self, idLandsat, BANDFILE, LMAX, LMIN, QCALMAX, QCALMIN, DATE, band):
        self.BANDFILE = BANDFILE
        self.LMAX = LMAX
        self.LMIN = LMIN
        self.QCALMAX = QCALMAX
        self.QCALMIN = QCALMIN
        self.DATE = DATE
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
    def __init__(self, landsat, x , y, SIType):
        self.landsat = landsat
        self.x = x
        self.y = y
        self.SIType = SIType
        self.radiance = {}
        self.reflectance = {}
        self.QCAL = {}
        cols = landsat.band['1'].cols
        
        for b in bandList:
            if(landsat.band[b].cols == cols):
                self.QCAL[b] = landsat.band[b].array[x][y]
                self.radiance[b] = self.calcRadiance(landsat.band[b].LMAX, 
                                                         landsat.band[b].LMIN,
                                                         landsat.band[b].QCALMAX,
                                                         landsat.band[b].QCALMIN, self.QCAL[b])
            
            elif((landsat.band[b].cols - cols/2) <=1):
                self.QCAL[b] = landsat.band[b].array[int(x/2)][int(y/2)]
                self.radiance[b] = self.calcRadiance(landsat.band[b].LMAX, 
                                                         landsat.band[b].LMIN,
                                                         landsat.band[b].QCALMAX,
                                                         landsat.band[b].QCALMIN, self.QCAL[b])
            
            if(b!='61'):
                self.reflectance[b] = self.calcReflectance(calcSolarDist(calcJDay(landsat.band[b].DATE)),
                                                                                getESUN(landsat.band[b].band, SIType),
                                                                                landsat.metadata['SUN_ELEVATION'],
                                                                                self.radiance[b])
                                                                                
            elif(self.radiance['61']>=0):
                self.band6 = 1282.71 / numpy.log(((666.09 * 0.95) / self.radiance['61'] ) +1 )

        self.NDVI =  (self.reflectance['4'] - self.reflectance['3']) / (self.reflectance['4'] + self.reflectance['3'])
                                                                                
        self.idLandsat = landsat.idLandsat        
        self.pixelWidth = landsat.band[str(1)].pixelWidth
        self.pixelHeight = landsat.band[str(1)].pixelHeight
        self.originX = landsat.band[str(1)].originX
        self.originY = landsat.band[str(1)].originY
        self.latitude = self.originX + (y * self.pixelWidth)
        self.longitude = self.originY + (x * self.pixelHeight)
        
        #self.latitude = latitude - (latitude%450)
        #self.longitude = longitude - (longitude%450)
                
    def cloud(self):
        if(self.reflectance['3']<0.08):
            return 'non-cloud' # filter one less 0.08 is not cloud
        elif((self.reflectance['2'] - self.reflectance['5']) / (self.reflectance['2'] + self.reflectance['5'])) > 0.7:
            return 'non-cloud' # filter two NDSI less 0.7 is not cloud
        elif(self.band6 > 300):
            return 'non-cloud' # filter three temp more 300 is not cloud
        elif(((1 - self.reflectance['5']) * self.band6) > 225):
            return 'ambiguous' # filter four 
        elif((self.reflectance['4']/self.reflectance['3']) > 2):
            return 'ambiguous' # filter five
        elif((self.reflectance['4']/self.reflectance['2']) > 2):
            return 'ambiguous' # filter six
        elif((self.reflectance['4']/self.reflectance['5']) < 1):
            return 'ambiguous' # filter seven
        elif((self.reflectance['5']/self.band6) > 210):
            return 'warn-cloud' # filter eight
        else:
            return 'cold-cloud' #filter eight
        
        
    def calcRadiance (self, LMAX, LMIN, QCALMAX, QCALMIN, QCAL):
        'This function calculate Spectral Radiance Scaling Method'    
        LMAX = float(LMAX)
        LMIN = float(LMIN)
        QCALMAX = float(QCALMAX)
        QCALMIN = float(QCALMIN)
        offset = (LMAX - LMIN)/(QCALMAX-QCALMIN)
        radiance = offset * (QCAL - QCALMIN) + LMIN
            
        return radiance

    def calcReflectance(self, solarDist, ESUN, solarElevation, radianceRaster):
    
        #Value for solar zenith is 90 degrees minus solar elevation (angle from horizon to the center of the sun)
        #http://landsathandbook.gsfc.nasa.gov/data_properties/prog_sect6_3.html

        solarZenith = ((90.0 - (float(solarElevation)))*math.pi)/180 #Converted from degrees to radians
        solarDist = float(solarDist)
        ESUN = float(ESUN)
        radiance = radianceRaster            
        
        reflectance = (math.pi * radiance * math.pow(solarDist, 2)) / (ESUN * math.cos(solarZenith))

        return reflectance
       
    def __str__(self):
        return "%s %s" % (self.x, self.y)

def calcSolarDist (jday):

    #Values taken from d.csv file which is a formatted version of the d.xls file
    #associated with the Landsat7 handbook, representing the distance of the sun
    #for each julian day (1-366).
    #landsathandbook.gsfc.nasa.gov/excel_docs/d.xls (included in the parent folder)
    #this line keeps the relative path were this script is executing
        
    jday = int(jday)
    dist = distances[jday - 1]

    return dist 

def calcJDay (date):
    
    #Seperate date aspects into list (check for consistnecy in formatting of all
    #Landsat7 metatdata) YYYY-MM-DD
    dt = date.rsplit("-")

    #Cast each part of the date as a in integer in the 9 int tuple mktime
    t = time.mktime((int(dt[0]), int(dt[1]), int(dt[2]), 0, 0, 0, 0, 0, 0))

    #As part of the time package the 7th int in mktime is calulated as Julian Day
    #from the completion of other essential parts of the tuple
    jday = time.gmtime(t)[7]

    return jday

def getESUN(bandNum, SIType):
    SIType = SIType
    ESUN = {}
    #from NASA's Landsat7 User Handbook Table 11.3 http://landsathandbook.gsfc.nasa.gov/pdfs/Landsat7_Handbook.pdf
    #ETM+ Solar Spectral Irradiances(generated using the Thuillier solar spectrum)
    if SIType == 'ETM+ Thuillier':
        ESUN = {'b1':1997,'b2':1812,'b3':1533,'b4':1039,'b5':230.8,'b7':84.90,'b8':1362}

    #from NASA's Landsat7 User Handbook Table 11.3 http://landsathandbook.gsfc.nasa.gov/data_prod/prog_sect11_3.html
    #ETM+ Solar Spectral Irradiances (generated using the combined Chance-Kurucz Solar Spectrum within MODTRAN 5)
    if SIType == 'ETM+ ChKur':
        ESUN = {'b1':1970,'b2':1842,'b3':1547,'b4':1044,'b5':225.7,'b7':82.06,'b8':1369}

    #from NASA's Landsat7 User Handbook Table 9.1 http://landsathandbook.gsfc.nasa.gov/pdfs/Landsat7_Handbook.pdf
    #from the LPS ACCA algorith to correct for cloud cover
    if SIType == 'LPS ACAA Algorithm':
        ESUN = {'b1':1969,'b2':1840,'b3':1551,'b4':1044,'b5':225.7,'b7':82.06,'b8':1368}

    #from Revised Landsat-5 TM Radiometric Calibration Procedures and Postcalibration
    #Dynamic Ranges Gyanesh Chander and Brian Markham. Nov 2003. Table II. http://landsathandbook.gsfc.nasa.gov/pdfs/L5TMLUTIEEE2003.pdf
    #Landsat 4 ChKur
    if SIType == 'Landsat 5 ChKur':
        ESUN = {'b1':1957,'b2':1825,'b3':1557,'b4':1033,'b5':214.9,'b7':80.72}
    
    #from Revised Landsat-5 TM Radiometric Calibration Procedures and Postcalibration
    #Dynamic Ranges Gyanesh Chander and Brian Markham. Nov 2003. Table II. http://landsathandbook.gsfc.nasa.gov/pdfs/L5TMLUTIEEE2003.pdf
    #Landsat 4 ChKur
    if SIType == 'Landsat 4 ChKur':
        ESUN = {'b1':1957,'b2':1826,'b3':1554,'b4':1036,'b5':215,'b7':80.67} 

    bandNum = 'b'+str(bandNum)
    
    return ESUN[bandNum]    

def rasterToDB(nameFolders):
    for i in range(len(nameFolders)-1):
        if os.path.isfile(nameFolders[i]):
            os.system('rm -R '+nameFolders[i].split('.')[0])
        os.system('mkdir '+nameFolders[i].split('.')[0])
        os.system('tar -xvf '+nameFolders[i]+' -C '+nameFolders[i].split('.')[0])              
        landsat = Landsat(nameFolders[i].split('.')[0])
        #date_landsat = '{0}\t{1}'.format(landsat.idLandsat, landsat.DATE)
        #db.copyToTable('date_landsat',io.StringIO(date_landsat))
        reflectance = []
        discarded = []
        for x in range(0,landsat.band['1'].rows,15):
            for y in range(0,landsat.band['1'].cols,15):
                if(landsat.band['1'].array[x][y]==0 or landsat.band['2'].array[x][y]==0 or
                 landsat.band['3'].array[x][y]==0 or landsat.band['4'].array[x][y]==0 or
                 landsat.band['5'].array[x][y]==0):
                     continue
                SIType = 'ETM+ Thuillier'
                point = Point(landsat, x, y, SIType)
                if (point.QCAL['61']==0):
                    continue
                cloud = point.cloud()
                if(cloud == 'non-cloud'):
                    reflectance.append('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}'.format(point.idLandsat,
                                                                                                       point.latitude,
                                                                                                       point.longitude,
                                                                                                       point.reflectance['1'],
                                                                                                       point.reflectance['2'],
                                                                                                       point.reflectance['3'],
                                                                                                       point.reflectance['4'],
                                                                                                       point.reflectance['5'],
                                                                                                       point.band6,
                                                                                                       point.reflectance['7']))                                                                                                           
                else:
                    discarded.append('{0}\t{1}\t{2}\t{3}'.format(point.idLandsat, point.latitude, point.longitude, cloud))
                                    
        reflectance = '\n'.join(reflectance)
        discarded = '\n'.join(discarded)                
        db.copyToTable('reflectance',io.StringIO(reflectance))
        db.copyToTable('discarded',io.StringIO(discarded))
        os.system('rm -R '+nameFolders[i].split('.')[0])	
                                  
path = os.getcwd()
path += '/L7Clipper'
os.chdir(path)

f = open('../d.csv', "r")
lines = f.readlines()[2:]

distances = []
for x in range(len(lines)):
    distances.append(float(lines[x].strip().split(',')[1]))
f.close()

tiempo1 = time.time()

db = Pdbc.DBConnector('landsat', 'omar', '1234', 'localhost', '5432')
                        
filterImg = 'LE7*'
nameFolders = os.popen('ls '+filterImg+'bz').read().split("\n")	    

rasterToDB(nameFolders)

tiempo2 = time.time()

print(tiempo2-tiempo1)

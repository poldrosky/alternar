#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  windRoseKML.py
#  
#  Copyright 2015 Omar Ernesto Cabrera Rosero <omarcabrera@udenar.edu.co>
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

import Pdbc
import math
from pyproj import Proj, transform
from pykml.factory import KML_ElementMaker as KML
from lxml import etree

db = Pdbc.DBConnector('wind', 'omar', '123', '190.254.4.128', '5432')

inf = float("inf")

dictDirection = {'1':(337.5,360+22.5), '2':(22.5, 67.5), '3':(67.5,112.5), '4':(112.5,157.5),
             '5':(157.5,202.5), '6':(202.5, 247.5), '7':(247.5, 292.5), '8':(292.5, 337.5)}

colors = {'1':'ff0000ff', '2':'ffff00ff', '3':'ffff0000', '4':'ffffff00', 
          '5':'ff00ff00', '6':'ff00ffff', '7':'ff00007f', '8':'ff7f007f',
          '9':'ff7f0000', '10':'ff7f7f00', '11':'ff007f00', '12':'ff007f82', '13':'ff4c4c4c'}
          
dictSpeed = {'1':(0,0.3), '2':(0.3,1.6), '3':(1.6,3.4), '4':(3.4,5.5),
         '5':(5.5,8.0), '6':(8,10.8), '7':(10.8,13.9), '8':(13.9,17.2),
         '9':(17.2,20.8), '10':(20.8,24.4), '11':(24.4,28.5), '12': (28.5,32.7), '13':(32.7,inf)}
         
dictDirection1 = {'1':'N', '2':'NE', '3':'E', '4':'SE',
              '5':'S', '6':'SW', '7':'W', '8':'NW'}

def reproject3857to4326(point,h):
    inProj = Proj(init='epsg:3857')
    outProj = Proj(init='epsg:4326')
    x,y = transform(inProj,outProj,point[0],point[1])
    pointstr = str(x)+','+str(y)+','+str(h) 
    return pointstr

def buildKML(patterns, latitude, longitude):
    patterns = [(i.replace("\'",'').replace('\"','')) for i in patterns]
    
    count = 100
    for pattern in patterns:
        direction = pattern[:1]
        speed = int(pattern[1:])
        #print(dictDirection[str(direction)],speed)
        origin = (latitude, longitude)
        points = []
        for a in range(int(dictDirection[str(direction)][0]*10)+100,int(dictDirection[str(direction)][1]*10)-99):
            angle = a/10
            X = (speed * 200) * math.sin(math.radians(angle))
            Y = (speed * 200) * math.cos(math.radians(angle))
            point = (latitude+X, longitude+Y)
            points.append(point)
            
        pointsReproject = ''
        pointsReproject1 = ''
        for point in points:
            pointsReproject += (reproject3857to4326(point, count)+'\n')
            
        for point in reversed(points):
            pointsReproject1 += (reproject3857to4326(point, count-70)+'\n')
        
        coordinates = reproject3857to4326(origin, count)+'\n'+pointsReproject+reproject3857to4326(origin,count)
        coordinates1 = reproject3857to4326(origin, count-70)+'\n'+pointsReproject1+reproject3857to4326(origin,count-70)
        coordinates2 = reproject3857to4326(origin, count)+'\n'+reproject3857to4326(points[0], count)+'\n'+reproject3857to4326(points[0], count-70)+'\n'+reproject3857to4326(origin, count-70)
        coordinates3 = reproject3857to4326(origin, count)+'\n'+reproject3857to4326(points[-1], count)+'\n'+reproject3857to4326(points[-1], count-70)+'\n'+reproject3857to4326(origin, count-70) 
        coordinates4 = pointsReproject+pointsReproject1
        
        poly = KML.Placemark(
                KML.description('Speed: '+str(dictSpeed[str(speed)])),
                KML.TimeStamp(KML.when(count)),
                KML.name('Localization: '+str(latitude)+','+str(longitude)),
                KML.styleUrl('#color'+str(speed)),
                KML.Polygon(
                    KML.extrude('0'),
                    KML.altitudeMode('relativeToGround'),
                    KML.outerBoundaryIs(
                       KML.LinearRing(
                           KML.coordinates(
                            coordinates
                            ),
                          ),
                        ),
                      ),
                    )
                    
        poly1 = KML.Placemark(
                KML.TimeStamp(KML.when(count)),
                KML.styleUrl('#color'+str(speed)),
                KML.Polygon(
                    KML.extrude('0'),
                    KML.altitudeMode('relativeToGround'),
                    KML.outerBoundaryIs(
                       KML.LinearRing(
                           KML.coordinates(
                            coordinates1
                            ),
                          ),
                        ),
                      ),
                    )
                    
        poly2 = KML.Placemark(
                KML.TimeStamp(KML.when(count)),
                KML.styleUrl('#color'+str(speed)),
                KML.Polygon(
                    KML.extrude('0'),
                    KML.altitudeMode('relativeToGround'),
                    KML.outerBoundaryIs(
                       KML.LinearRing(
                           KML.coordinates(
                            coordinates2
                            ),
                          ),
                        ),
                      ),
                    )
                    
        poly3 = KML.Placemark(
                KML.TimeStamp(KML.when(count)),
                KML.styleUrl('#color'+str(speed)),
                KML.Polygon(
                    KML.extrude('0'),
                    KML.altitudeMode('relativeToGround'),
                    KML.outerBoundaryIs(
                       KML.LinearRing(
                           KML.coordinates(
                            coordinates3
                            ),
                          ),
                        ),
                      ),
                    )
                    
        poly4 = KML.Placemark(
                KML.TimeStamp(KML.when(count)),
                KML.styleUrl('#color'+str(speed)),
                KML.Polygon(
                    KML.extrude('0'),
                    KML.altitudeMode('relativeToGround'),
                    KML.outerBoundaryIs(
                       KML.LinearRing(
                           KML.coordinates(
                            coordinates4
                            ),
                          ),
                        ),
                      ),
                    )
                    
        folder.append(poly)
        folder.append(poly1)
        folder.append(poly2)
        folder.append(poly3)
        folder.append(poly4)
        count+=100

def drawPatterns(table, param):
    query = 'SELECT * FROM stations ORDER BY latitude, longitude limit 2'
    stations = db.resultQuery(query)
    for station in stations:
        query = 'SELECT max({0}) FROM {1} WHERE latitude={2} and longitude={3}'.format(param, table, station[1], station[2])
        maxParam = db.resultQuery(query)
        if(param == 'len_pattern'):
            query = '''SELECT 
                            *
                       FROM 
                            {0} 
                       WHERE 
                            latitude={1} and longitude={2} and {3}={4}
                       ORDER BY 
                            len_pattern, diff_speed, frequency'''.format(table, station[1], station[2], param, maxParam[0][0])
        elif(param == 'frequency'):
            query = '''SELECT 
                            *
                       FROM 
                            {0} 
                       WHERE 
                            latitude={1} and longitude={2} and {3}={4}
                       ORDER BY 
                            frequency, len_pattern, diff_speed'''.format(table, station[1], station[2], param, maxParam[0][0])
        elif(param == 'diff_speed'):
            query = '''SELECT 
                            *
                       FROM 
                            {0} 
                       WHERE 
                            latitude={1} and longitude={2} and {3}={4}
                       ORDER BY 
                            diff_speed, diff_direction, len_pattern, frequency'''.format(table, station[1], station[2], param, maxParam[0][0])
        elif(param == 'diff_direction'):
            query = '''SELECT 
                            *
                       FROM 
                            {0} 
                       WHERE 
                            latitude={1} and longitude={2} and {3}={4}
                       ORDER BY 
                            diff_direction, diff_speed, len_pattern, frequency'''.format(table, station[1], station[2], param, maxParam[0][0]) 
        
        result = db.resultQuery(query)
        latitude = result[0][1]
        longitude = result[0][2]
        patterns = result[0][3]        
        buildKML(patterns, latitude, longitude)
    
def main():
    global folder
    folder = KML.Folder()    
    for i in range(1,14):
        style = KML.Style(
                    KML.PolyStyle(
                        KML.color(colors[str(i)]),
                        KML.colorMode('normal')
                        ),
                    id="color"+str(i)
                )    
        folder.append(style)
    
    #nameKML = 'len_pattern'
    #nameKML = 'frequency'
    #nameKML = 'diff_speed'
    nameKML = 'diff_direction'
        
    drawPatterns('patternsbyhourclosed50', nameKML)       
    outfile = open(nameKML+'.kml','wb')
    outfile.write(etree.tostring(folder, pretty_print=True))
    
if __name__ == '__main__':
    main()
    

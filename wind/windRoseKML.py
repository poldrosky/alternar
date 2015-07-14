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

db = Pdbc.DBConnector('db', 'user', 'pass', 'localhost', 'port')

dictDirection = {'1':(337.5,360+22.5), '2':(22.5, 67.5), '3':(67.5,112.5), '4':(112.5,157.5),
             '5':(157.5,202.5), '6':(202.5, 247.5), '7':(247.5, 292.5), '8':(292.5, 337.5)}

def getPatterns(table, id):
    query = 'SELECT * FROM {0} where id={1}'.format(table,id)
    result = db.resultQuery(query)
    patterns = result[0][3]
    latitude = result[0][1]
    longitude = result[0][2]
    return patterns, latitude, longitude
    
def reproject3857to4326(point,h):
    inProj = Proj(init='epsg:3857')
    outProj = Proj(init='epsg:4326')
    x,y = transform(inProj,outProj,point[0],point[1])
    pointstr = str(x)+','+str(y)+','+str(h) 
    return pointstr


# Here write table and pattern id
patterns, latitude, longitude = getPatterns('patternsmax50',666)

patterns = [(i.replace("\'",'').replace('\"','')) for i in patterns]

colors = {'1':'ffd35602', '2':'ffc15716', '3':'ffaf592b', '4':'ff9e5b40', 
          '5':'ff8c5d55', '6':'ff7b5e6a', '7':'ff69607f', '8':'ff576294',
          '9':'ff4664a9', '10':'ff3465be', '11':'ff6723ff', '12':'ff1169e8', '13':'ff006bfd'}


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
            KML.TimeStamp(KML.when(count)),
            KML.name(pattern),
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
            KML.name(pattern),
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
            KML.name(pattern),
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
            KML.name(pattern),
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
            KML.name(pattern),
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
    
outfile = open('prueba.kml','wb')
outfile.write(etree.tostring(folder, pretty_print=True))

    

           
    

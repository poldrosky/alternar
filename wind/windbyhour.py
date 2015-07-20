#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  windbyhour.py
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

import os
import Pdbc
import time
import csv
import io

t1 = time.time()

inf = float("inf")
global id
id =0

db = Pdbc.DBConnector('db', 'user', 'pass', 'localhost', 'port')

dictDirection = {'1':(337.5,22.5), '2':(22.5, 67.5), '3':(67.5,112.5), '4':(112.5,157.5),
             '5':(157.5,202.5), '6':(202.5, 247.5), '7':(247.5, 292.5), '8':(292.5, 337.5)}

dictSpeed = {'01':(0,0.3), '02':(0.3,1.6), '03':(1.6,3.4), '04':(3.4,5.5),
         '05':(5.5,8.0), '06':(8,10.8), '07':(10.8,13.9), '08':(13.9,17.2),
         '09':(17.2,20.8), '10':(20.8,24.4), '11':(24.4,28.5), '12': (28.5,32.7), '13':(32.7,inf)}
         
dictDirection1 = {'1':'N', '2':'NE', '3':'E', '4':'SE',
              '5':'S', '6':'SW', '7':'W', '8':'NW'}
              

def conversion(s):
    result = []
    for i in s:
        directionWind = i[:1]
        speedWind = i[1:]
        result.append(str(dictDirection1[directionWind])+str(dictSpeed[speedWind]))
    return result
    
def getSpeed(s):
    result = []
    for i in s:
        result.append(dictSpeed[i[1:]])
    return result
    
def getDirection(s):
    result = []
    for i in s:
        result.append(dictDirection1[i[:1]])
    return result

def classifySpeed(value, dictClass):
    """Ingresa un valor y una dicionario y retorna el numero del grupo"""
    for i in dictClass:
        if value > dictClass[i][0] and value <= dictClass[i][1]:
            return i

def classifyDirection(value, dictClass):
    """Ingresa un valor y una dicionario y retorna el numero del grupo"""
    for i in dictClass:
        if value > dictClass[i][0] and value <= dictClass[i][1]:
            return i
    return '01'


query = 'SELECT latitude, longitude FROM stations ORDER BY latitude, longitude'
stations = db.resultQuery(query)

for station in stations:
    os.system('rm output.dat output.mfi')
    query1 = 'SELECT * FROM timeseries50 WHERE latitude='+str(station[0])+' AND longitude='+str(station[1])+' ORDER BY timewind'
    rows = db.resultQuery(query1)
    dataList = []
    count = 0
    
    print(len(rows))
    
    for i in range(0, 24):
        directionWind = classifyDirection(rows[i][6],dictDirection)
        speedWind = classifySpeed(rows[i][7],dictSpeed)
        value = directionWind+speedWind
        dataList.append([])
        dataList[count].append(value)
    dataList[count].append('\n')
    count += 1
    
    for i in range(25, len(rows)):        
        dataList.append([])
        directionWind = classifyDirection(rows[i][6],dictDirection)
        speedWind = classifySpeed(rows[i][7],dictSpeed)
        value = directionWind+speedWind
        dataList[count] = dataList[count-1][1:-1]
        dataList[count].append(value)
        dataList[count].append('\n')
        count +=1
    
    output = open('output.dat','w')
    st = ''
    for i in dataList:
        st += ' '.join(i)
    
    output.write(st)
    output.close()
    
    if os.path.getsize('output.dat') == 0:
        continue
    
    support = int(count * 0.2)
            
    os.system('./lcm_seq Ffm -l '+str(4)+ ' output.dat ' + str(support) + ' output.mfi > /dev/null') #maximal
    #os.system('./lcm_seq Ffc -l '+str(4)+ ' output.dat ' + str(support) + ' output.mfi > /dev/null') #close
    
    os.system('wc -l output.mfi')
        
    output1 = csv.reader(open('output.mfi', 'r'),delimiter=' ')
    
    stdin = ''
    for line in output1:
        pattern = line[0:-2]
        frequency = line[-1].replace('(','').replace(')','')
        diffPattern = set(pattern)
        translatePattern = conversion(pattern)
        lenPattern = len(pattern)
        speed = getSpeed(pattern)
        direction = getDirection(pattern)
        diffSpeed = len(set(speed))
        diffDirection = len(set(direction))
        stdin+= (str(id) +'\t'+
                str(station[0]) +'\t'+
                str(station[1]) +'\t'+
                str(pattern).replace('[','{').replace(']','}') +'\t'+
                str(lenPattern) +'\t'+
                str(frequency) +'\t'+
                str(translatePattern).replace('[','{').replace(']','}') +'\t'+
                str(direction).replace('[','{').replace(']','}') +'\t'+
                str(speed).replace('[','{').replace(']','}') +'\t'+
                str(diffDirection) +'\t'+
                str(diffSpeed) +'\n')
                
        id +=1
    
    db.copyToTable('patternsbyhour', io.StringIO(stdin))

t2 = time.time()

print(t2-t1)
                
print('done')

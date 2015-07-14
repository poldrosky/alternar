#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  windRoseGeneral.py
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


# Use library windrose 1.5, https://github.com/scls19fr/windrose

import Pdbc
import time
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np
from math import pi

from windrose import WindroseAxes

t1 = time.time()

db = Pdbc.DBConnector('db', 'user', 'pass', 'localhost', 'port')

query = 'SELECT DISTINCT latitude, longitude FROM timeseries50 ORDER BY latitude, longitude LIMIT 1'
stations = db.resultQuery(query)

for station in stations:
    ws = []
    wd = []
    query1 = 'SELECT * FROM timeseries50 WHERE latitude='+str(station[0])+' AND longitude='+str(station[1])+' ORDER BY timewind'
    rows = db.resultQuery(query1)
    for row in rows:
        wd.append(row[6])
        ws.append(row[7])
    ws = np.array(ws)
    wd = np.array(wd)    
    df = pd.DataFrame({"speed": ws, "direction": wd})
    
    #windrose like a stacked histogram with normed (displayed in percent) results
    ax = WindroseAxes.from_ax()
    ax.bar(df.direction, df.speed, normed=True, opening=0.8, edgecolor='white')
    ax.set_legend()
    ax.set_title('Estación: '+str(station[0])+' , '+str(station[1]))
    plt.show()
    
t2 = time.time()

print(t2-t1)
                
print('done')

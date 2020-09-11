# !/usr/bin/python
# -*- coding: utf-8 -*-
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time
import serial
import time
from datetime import datetime

# start by initializing Qt
app = QtGui.QApplication([])

view = pg.GraphicsWindow()
view.resize(800,500)
view.setWindowTitle('ECG Monitoring')

p1 = view.addPlot(0,1,title="Raw ECG")
p2 = view.addPlot(1,1,title="Low-Pass Filtered ECG")

curve1 = p1.plot(pen='b')
curve2 = p2.plot(pen='r')

p1.setYRange(0,1500, padding=0)
p2.setYRange(0,1500, padding=0)

datax = [0] * 19
datay = [0] * 19
data_filter = [0] * 19
filter_coef = [0.000454665481664494, 0.00355945381522087, 0.00635871854161046, -0.00422929091333384, -0.0317513205905760, -0.0380851026729248, 0.0374608537584544, 0.194837858068540, 0.331466126840366, 0.331466126840366, 0.194837858068540, 0.0374608537584544, -0.0380851026729248, -0.0317513205905760, -0.00422929091333384, 0.00635871854161046, 0.00355945381522087, 0.000454665481664494]
raw = serial.Serial("COM11", 250000)

start_time = time.time()

i = 0        #incremental for array index

now = datetime.now()
current_time = now.strftime("%y%m%d_%H%M%S")
print("Current Time =", current_time)
record = open('%s.txt' % current_time, 'a')

@profile
def update():
   global curve, data

   bytesR_H = raw.read()
   bytesR_L = raw.read()
   valueR = (ord(bytesR_H) << 5) + ord(bytesR_L)
   # raw.flushInput()
   # raw.flushOutput()

   global i

   elapsedtime = time.time() - start_time

   datax.append(elapsedtime)
   datay.append(valueR)
   xdata = datax
   ydata = datay

   # filtering
   i += 1
   data_filter.append(sum([x*y for x,y in zip(filter_coef,ydata[i:i+18])]))

   # print(data_filter[i])

   # display filtered data
   if (i % 2) == 0:
      curve1.setData(xdata, ydata)
      # app.processEvents()
      p1.setXRange(elapsedtime - 3, elapsedtime)

      curve2.setData(xdata, data_filter)
      # app.processEvents()
      p2.setXRange(elapsedtime - 3, elapsedtime)

   #record data
   now = datetime.now()
   current_time = now.strftime("%y%m%d_%H%M%S")
   print(current_time,',',valueR, file=record)


timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)

if __name__ == '__main__':
   import sys

   if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
       QtGui.QApplication.instance().exec_() # execute until exit or the above conditions are not met



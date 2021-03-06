
import serial
from matplotlib import pyplot as plt
from matplotlib import animation as animation
from matplotlib import style
import io
import argparse
import numpy as np
import PyQt5
from tools import WriteData, PlotData
from tools import WriteData


def init():
    device = serial.Serial()
    device.baudrate = 9600
    device.port = "/dev/ttyUSB0"
    device.timeout = 10
  #  device.nonblocking()
    return device

def collectData(fileName, datas):
    file = open(fileName, "w")
    for data in datas:
        file.write(data)
    file.close()


def plotData(data):
    pass


#fig = plt.figure()
#ax1 = fig.add_subplot(1,1,1)

#def animate(i):
  #  graph_data = open("data/data1.dat", "r")
  #  lines = graph_data.split('\n')
  #  xs = []
  #  ys = []
  #  for line in lines:
  #      if len(line) > 1:
  #          t, x, y, z = line.split(',')
  #          xs.append(t)
  #          ys.append(z)
  #      ax1.clear()
  #      ax1.plot()

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate( i):
        graph_data = open("data/data1.dat", "r")
        lines = graph_data.split('\n')
        xs = []
        ys = []
        for line in lines:
            if len(line) > 1:
                t, x, y, z = line.split(',')
                xs.append(t)
                ys.append(z)
            ax1.clear()
            ax1.plot()

def main():
    style.use("fivethirtyeight")

    print("Starting SerialPlotter")
    
    #initialize device
    device = init()
    file = open("data/data1.dat", "w")
    collectData = WriteData(device, file)
    
    ani = PlotData()
    collectData.start() # start thread
    ani.start()

    collectData.join()
    ani.join()
    print("join")
    device.close()    
    
    
if __name__ == '__main__':
    main()


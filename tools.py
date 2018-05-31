import serial
import multiprocessing
import io
from matplotlib import pyplot as plt
from matplotlib import animation as animation
from matplotlib import style
import serialPlotter

class WriteData(multiprocessing.Process):
    def __init__(self, uartdevice, file):
        self.file = file
        self.device = uartdevice
        multiprocessing.Process.__init__(self)

    def run(self):
        print("[Writing to file " + str(self.pid) + " started]")
        self.device.open() # open uart device
        if not self.device.is_open:
            print("Device coludn't open")
            exit(-1)
        else:
            G = 9.8081
            datas = []
            datax = []
            dataz = []
            datay = []
            linecntr = 0
            sio = io.TextIOWrapper(io.BufferedRWPair(self.device,self.device)) 
            
            self.device.read(2)
            #line = sio.readline()
            while True:
                line = sio.readline()
                line.encode('utf-8').strip()
                if len(line) < 2:
                    print("END communication")
                    break
                linecntr = linecntr + 1    
                line = str(linecntr) + "," + line
                self.file.write(line)           
                datas.append(line)
                line = line.split(",")
            #  print(line)
                tempz = float(line[3])
                datax.append(float(line[1]))
                datay.append(float(line[2]))
                dataz.append(tempz)
                




class PlotData(multiprocessing.Process):
    def __init__(self):
        multiprocessing.Process.__init__(self)

    

    def run(self):
        ani = animation.FuncAnimation(serialPlotter.fig, serialPlotter.animate, interval=1000)
        plt.show()
import serial
from matplotlib import pyplot as plt
import io
import argparse

def init():
    device = serial.Serial()
    device.baudrate = 9600
    device.port = "/dev/ttyUSB0"

    return device

def main():

  #  parser = argparse.ArgumentParser(description='Simple serial plotter')
   # parser.add_argument("-b", "--baud", help="Setup baudrate",type=int)
    #parser.add_argument("-p", "--port", help="Serial port")
    #parser.add_argument("-t", "--parity", help="Parity bit set up")
    #parser.add_argument("-d", "--datasofplot", help="How many datas to plot")

    print("Starting SerialPlotter")
    
    #initialize device
    device = init()

    device.open()   

    if not device.is_open:
        print("Device coludn't open")
        exit(-1)
    else:
        datas = []
        datax = []
        dataz = []
        datay = []
        linecntr = 0
        sio = io.TextIOWrapper(io.BufferedRWPair(device,device)) 

        while linecntr < 2:
            line = sio.readline()
            if line[0] is "-":
                datas.append(line)
                datax.append(float(line[0:9]))
                datay.append(float(line[11:20]))
                dataz.append(float(line[22:31]))
                print(line)
                linecntr += 1
            else:
                pass

        device.close()    
        for data in datas:
            print(data)
        print("dataz")
        for x in datax:
            print(x)
        print("datay")
        for y in datay:
            print(y)
        print("datax: ")
        for z in dataz:
            print(z)

if __name__ == '__main__':
    main()
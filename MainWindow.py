from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtSerialPort
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import sys
import random
import sys


import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

import random


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("SerialPlotter")

        # create variables
        self.x = []
        self.y = []
        self.z = []

        # create figure for plot
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolBar = NavigationToolbar(self.canvas, self)

        # create menus
        self.mainMenu = self.menuBar()
        # self.createToolBar()
        self.createFileMenu(self.mainMenu)
        self.createEditMenu(self.mainMenu)
        self.createDeviceMenu(self.mainMenu)
        self.createFiltersMenu(self.mainMenu)
        self.createAboutMenu(self.mainMenu)

        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        wid = QtWidgets.QWidget(self)
        self.setCentralWidget(wid)
        verticalLayout = QVBoxLayout(self)

        # setup the layout for the window
        wid.setLayout(verticalLayout)
        verticalLayout.addWidget(self.mainMenu)
        verticalLayout.addWidget(self.toolBar)
        verticalLayout.addWidget(self.canvas)
        verticalLayout.addWidget(self.button)

        self.setLayout(verticalLayout)

        self.devicePort = None

        # self.createButton()
        self.show()

    def createButton(self):
        button = QtWidgets.QPushButton('Quit', self)
        button.clicked.connect(QtCore.QCoreApplication.instance().quit)

    def createFileMenu(self, mainMenu):
        """
        """
        fileMenu = mainMenu.addMenu('&File')

        newAct = QtWidgets.QAction("&New", self)
        newAct.setShortcut("Ctrl+N")
        newAct.setToolTip("Create new Window")
        newAct.triggered.connect(self.newWindow)

        openAct = QtWidgets.QAction("&Load", self)
        openAct.setShortcut("Ctrl+O")
        openAct.setToolTip("Load saved data")
        openAct.triggered.connect(self.loadData)

        saveAct = QtWidgets.QAction("&Save", self)
        saveAct.setShortcut("Ctrl+S")
        saveAct.setToolTip("Save data")

        exitAct = QtWidgets.QAction("&Quit", self)
        exitAct.setShortcut("Ctrl+Q")
        exitAct.setStatusTip('Leave The App')
        exitAct.triggered.connect(self.exitApp)

        fileMenu.addAction(newAct)
        fileMenu.addAction(openAct)
        fileMenu.addAction(saveAct)
        fileMenu.addAction(exitAct)

    def createEditMenu(self, mainMenu):
        """
        """
        editMenu = mainMenu.addMenu('&Edit')

    def createDeviceMenu(self, mainMenu):
        """
        Create device menu, list all avaliable devices
        """
        deviceMenu = mainMenu.addMenu('&Device')
        availablePorts = QtSerialPort.QSerialPortInfo.availablePorts()
        if len(availablePorts) is 0:
            emptymsg = QtWidgets.QAction("No device found", self)
            deviceMenu.addAction(emptymsg)
        else:
            # create signalmapper to find out wich button is presed
            self.signalMapper = QtCore.QSignalMapper(self)

            actionGroup = QtWidgets.QActionGroup(self, exclusive=True)
            i = 0
            self.deviceMap = {}
            for port in availablePorts:
                action = actionGroup.addAction(QtWidgets.QAction(
                    port.portName(), self,  checkable=True))  # make checkable the ports
                deviceMenu.addAction(action)
                action.triggered.connect(
                    self.signalMapper.map)  # connect signal
                portname = port.portName()
                self.signalMapper.setMapping(action, i)
                # add portname and idnex to a map
                self.deviceMap.__setitem__(i, portname)
                i = i + 1

            self.signalMapper.mapped.connect(self.setDevice)
            print(str(self.deviceMap))
            sys.stdout.flush()

        ''' actionGroup = QtWidgets.QActionGroup(self, exclusive=True)
        for i in range(3):
            action = actionGroup.addAction(QtWidgets.QAction(str(i),self,  checkable=True)) #make checkable the ports
            deviceMenu.addAction(action)
            action.triggered.connect(self.setDevice) '''

    # TODO: megcsinálni hogy lehessen tudni melyik ezsköz van kiválasztva
    def setDevice(self, deviceName):
        print("buli van")
        print(deviceName)

    # TODO: csatlakozzon az eszközhöz
    def connectToDevice(self):
        #self.device = QtSerialPort.QSerialPortInfo.availablePorts()
        pass

    def createFiltersMenu(self, mainMenu):
        filtersMenu = mainMenu.addMenu("Fi&lters")

    def createAboutMenu(self, mainMenu):
        """
        """
        aboutMenu = mainMenu.addMenu('&About')

    def createToolBar(self):
        """
        Creates Toolbar
        """
        newAction = QtWidgets.QAction(
            QtGui.QIcon("./resources/new.png"), "New", self)
        self.toolBar = self.addToolBar("MainToolBar")
        self.toolBar.addAction(newAction)
        newAction.triggered.connect(self.newWindow)

        quitAction = QtWidgets.QAction(
            QtGui.QIcon("resources/quit.png"), "Quit", self)
        self.toolBar = self.addToolBar("MainToolBar")
        self.toolBar.addAction(quitAction)
        quitAction.triggered.connect(self.exitApp)

    def newWindow(self):
        """
        Create new window
        """
        self.__init__()

    def exitApp(self):
        # FIXME: close nem mukodik
        print("Closing...", end="")
        self.close()
        print("OK")
        # sys.exit()

    def saveData(self, fileName, datas):
        """
        :param filename: the location and a filename whre to save the file
        :param datas: the datas to save
        :return: returns nothing
        """
        file = open(fileName, "w")
        for data in datas:
            file.write(data)
        file.close()

    def loadData(self):

        fileChooser = QtWidgets.QFileDialog()
        fileChooser.setViewMode(QtWidgets.QFileDialog.Detail)
        fileChooser.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        fileName = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open Saved Data", "/home/mate", "Image Files (*.data *.dat *.txt)")
        print(fileName[0])
        sys.stdout.flush()


        try:
            self.dataFile = open(fileName[0], "r")

            for line in self.dataFile:
             #   print(line, end="")
             #   sys.stdout.flush()

                data = line.split(",")
                self.x.append(data[0])
                self.y.append(data[1])
                self.z.append(data[2])

            self.dataFile.close()
        except:
            print("Something went wrong by file opening")
            sys.stdout.flush()

    def plot(self):
        ''' plot some random stuff '''
        # random data
       # data = [random.random() for i in range(10)]
        if len(self.z) is 0:
            print("No file loaded")
            sys.stdout.flush()

        else:
            dataz = self.z
            datax = self.x
            datay = self.y
            data = []
            # TODO : ezt befejezni
            for i in range(len(dataz)-5):
                tmp = ( float(dataz[i]) + float(dataz[i+1]) + float(dataz[i+2]) + float(dataz[i+3]) ) / 4
                data.append(tmp)

            # create an axis
            fig = self.figure.add_subplot(111)
            #fig = self.figure
            # discards the old graph
            fig.clear()

            # plot data
            #fig.plot(datax, "r", label="X")
            #fig.plot(datay, "g", label="Y")
            fig.plot(data, "b", label="Z")
            fig.legend()
            # grid on
            fig.grid()
            fig.set_ylim((9, 11))
            fig.set_xlabel("time[s]")
            fig.set_ylabel("velocity[m/s^2]")
           
            

            # debug
            # file = open("/home/mate/random.data", "w+")
            # i = 0
            # for d in data:
            #     file.write(str(i) + " "+str(d)+"\n")
            #     i = i + 1
            # file.close()

            # refresh canvas
            self.canvas.draw()


"""

"""


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())


if __name__ == '__main__':
   # window()
    main()

import sys
import os
import random
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np

class MainWindow(QMainWindow):
    
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.create_chart()
        
        
    def create_chart(self):
        self.frame = QWidget()
        
        self.dpi = 100
        self.fig = Figure((6.0,5.0), dpi = self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.frame)
        
        self.axes = self.fig.add_subplot(111)
        self.axes.set_axis_bgcolor('black')
        self.axes.grid(True, color='gray')
        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        self.pause = QPushButton('Pausa')
        self.connect(self.pause, SIGNAL('clicked()'), self.doPause)
        vbox.addWidget(self.pause)
        self.frame.setLayout(vbox)
        self.setCentralWidget(self.frame)
        self.data = []
        
        for x in range(10):
            self.data.append(generaData())
            
        self.line = self.axes.plot(
            self.data,
            linewidth = 1,
            color = (1, 1, 0),
            )[0]
           
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)
        self.timer.start(100)
        
    def doPause(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start()
        
    def refresh(self):
        self.data.append(generaData())
        self.draw_chart()
        
        
    def draw_chart(self):
        count = len(self.data)
        xmax = count if count > 50 else 50
        xmin = xmax - 50
        
        self.axes.set_xbound(lower = xmin, upper = xmax)
        self.axes.set_ybound(lower = 0, upper = 1023)
        
        self.line.set_xdata(np.arange(len(self.data)))
        self.line.set_ydata(np.array(self.data))
        
        self.canvas.draw()
        
        
def generaData():
    return random.randint(0,1023)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

# vim: ts=4 et sw=4 st=4 
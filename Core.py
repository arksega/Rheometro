# -*- coding: utf-8 -*-
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
        
        #Generacion de elementos principales de la grafica
        self.frame = QWidget()
        self.dpi = 100
        self.fig = Figure((6.0,5.0), dpi = self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.frame)
        
        #Configuracion de la grafica
        self.axes = self.fig.add_subplot(111)
        self.axes.set_axis_bgcolor('black')
        self.axes.grid(True, color='gray')
        
        #Declaracion de interfaz grafica
        self.pause = QPushButton('Pausar')
        self.pause.setDisabled(True)
        self.comenzar = QPushButton('Comenzar')
        self.comenzar.setCheckable(True)
        self.guardar = QPushButton('Guardar')
        self.pause.clicked.connect(self.doPause)
        self.nombreL = QLabel('Nombre de la prueba')
        self.nombre = QLineEdit()
        self.tiempoPrueba = QSpinBox()
        self.tiempoPrueba.setMinimum(1)
        self.tiempoPrueba.setDisabled(True)
        self.politicaTiempo = QButtonGroup()
        self.tiempoFijo = QRadioButton('Tiempo fijo')
        self.tiempoIlimitado = QRadioButton('Tiempo ilimitado')
        self.tiempoIlimitado.setChecked(True)
        self.grupoTiempo = QGroupBox('Manejo de tiempo')
        self.tiempoIlimitado.toggled.connect(self.cambiaPolitica)
        
        
        hbox = QGridLayout()
        
        hbox.addWidget(self.tiempoIlimitado,0,0)
        hbox.addWidget(self.tiempoFijo,1,0)
        hbox.addWidget(self.tiempoPrueba,1,1)
        hbox.addWidget(self.pause,0,2,2,1)
        self.grupoTiempo.setLayout(hbox)
        
        vbox = QGridLayout()
        vbox.addWidget(self.nombreL,1,0)
        vbox.addWidget(self.nombre,1,1,)
        vbox.addWidget(self.comenzar,1,2)
        vbox.addWidget(self.guardar,1,3)
        vbox.addWidget(self.grupoTiempo,2,0,1,2)
        vbox.addWidget(self.canvas,0,0,1,4)
        
        self.frame.setLayout(vbox)
        self.setCentralWidget(self.frame)
        self.data = []
        
            
        self.line = self.axes.plot(
            self.data,
            linewidth = 1,
            color = (1, 1, 0),
            )[0]
           
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)
        self.timer.setInterval(50)
        
        self.contadorPrincipal = QTimer()
        self.contadorPrincipal.timeout.connect(self.detenerPrueba)
        self.contadorPrincipal.setInterval(525600000) #Un año
        
        self.comenzar.toggled.connect(self.togglePrueba)
        
        self.draw_chart()
        
    def detenerPrueba(self):
        self.timer.stop()
        self.contadorPrincipal.stop()
        self.comenzar.setText('Comenzar')
        self.pause.setText('Pausar')
        self.pause.setDisabled(True)
        
    def comenzarPrueba(self):
        self.data = []
        self.draw_chart()
        self.timer.start()
        self.contadorPrincipal.start()
        self.comenzar.setText('Detener')
        self.pause.setDisabled(False)
    
    def togglePrueba(self):
        if self.comenzar.isChecked():
            self.comenzarPrueba()
        else:
            self.detenerPrueba()
        
    def cambiaPolitica(self):
        if self.tiempoIlimitado.isChecked():
            self.tiempoPrueba.setDisabled(True)
        else:
            self.tiempoPrueba.setEnabled(True)
        
    def doPause(self):
        if self.timer.isActive():
            self.timer.stop()
            self.pause.setText('Reanudar')
        else:
            self.timer.start()
            self.pause.setText('Pausar')
        
    def refresh(self):
        self.data.append(generaData())
        self.draw_chart()
        
        
    def draw_chart(self):
        count = (len(self.data) * 50) / 1000.0
        xmax = count if count > 3 else 3
        xmin = xmax - 3
        
        self.axes.set_xbound(lower = xmin, upper = xmax)
        self.axes.set_ybound(lower = 0, upper = 1023)
        
        self.line.set_xdata(np.arange(0,count, .050))
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
# -*- coding: utf-8 -*-
import sys
import serial
import os
import random
import threading
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.figure import Figure
import numpy as np

class ReadArduino(threading.Thread):
    def __init__(self):
        self.active = True
        #Inicializa serial
        self.ser = serial.Serial('/dev/ttyACM2', 9600)
        threading.Thread.__init__(self)
        
    def run(self):
        while self.active:
            self.data = self.ser.readline()
    
    def led0(self, estado):
        comando = 'A' if estado else 'B'
        self.ser.write(comando)

    def led1(self, estado):
        comando = 'C' if estado else 'D'
        self.ser.write(comando)

    def led2(self, estado):
        comando = 'E' if estado else 'F'
        self.ser.write(comando)

    def led3(self, estado):
        comando = 'G' if estado else 'H'
        self.ser.write(comando)

    def stop(self):
        self.active = False
            
class MainWindow(QMainWindow):
    
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.create_chart()
        
    def create_chart(self):
        self.arduino = ReadArduino()
        self.arduino.start()

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
        self.pause.clicked.connect(self.doPause)
        
        self.comenzar = QPushButton('Comenzar')
        self.comenzar.setCheckable(True)
        
        self.guardar = QPushButton('Guardar')
        self.guardar.clicked.connect(self.doGuardar)
        
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
        self.grupoSignal = QGroupBox(u'Señales')
        self.tiempoIlimitado.toggled.connect(self.cambiaPolitica)
        
        self.led0 = QPushButton('0')
        self.led1 = QPushButton('1')
        self.led2 = QPushButton('2')
        self.led3 = QPushButton('3')
        self.led0.setCheckable(True)
        self.led1.setCheckable(True)
        self.led2.setCheckable(True)
        self.led3.setCheckable(True)
        self.led0.toggled.connect(self.arduino.led0)
        self.led1.toggled.connect(self.arduino.led1)
        self.led2.toggled.connect(self.arduino.led2)
        self.led3.toggled.connect(self.arduino.led3)

        gt = QGridLayout()
        gt.addWidget(self.tiempoIlimitado,0,0)
        gt.addWidget(self.tiempoFijo,1,0)
        gt.addWidget(self.tiempoPrueba,1,1)
        gt.addWidget(self.pause,0,2,2,1)
        self.grupoTiempo.setLayout(gt)
        
        gs = QGridLayout()
        gs.addWidget(self.led0,2,2)
        gs.addWidget(self.led1,2,3)
        gs.addWidget(self.led2,3,2)
        gs.addWidget(self.led3,3,3)
        self.grupoSignal.setLayout(gs)
        
        gp = QGridLayout()
        gp.addWidget(self.nombreL,1,0)
        gp.addWidget(self.nombre,1,1,)
        gp.addWidget(self.comenzar,1,2)
        gp.addWidget(self.guardar,1,3)
        gp.addWidget(self.grupoTiempo,2,0,1,2)
        gp.addWidget(self.grupoSignal,2,2,1,2)
        gp.addWidget(self.canvas,0,0,1,4)
        

        
        self.frame.setLayout(gp)
        self.setCentralWidget(self.frame)
        self.data = []
        
            
        self.line = self.axes.plot(
            self.data,
            linewidth = 1,
            color = (1, 1, 0),
            )[0]

        self.tiempoTrancurrido = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)
        self.lecturasXSegundo = 20
        self.timer.setInterval(1000 / self.lecturasXSegundo)
        
        self.contadorPrincipal = QTimer()
        self.contadorPrincipal.timeout.connect(self.comenzar.toggle)
        
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
        self.tiempoTrancurrido = 0
        self.draw_chart()
        if self.tiempoFijo.isChecked():
            self.contadorPrincipal.setInterval(self.tiempoPrueba.value() * 1000)
        else:
            self.contadorPrincipal.setInterval(525600000) #Un año
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
            
    def doGuardar(self):
        if self.nombre.text() == '':
            mensaje = QMessageBox(self)
            mensaje.setText('Ingrese un nombre para la prueba')
            mensaje.setWindowTitle('Error al guardar')
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.exec_()
        elif len(self.data) == 0:
            mensaje = QMessageBox(self)
            mensaje.setText('No hay datos para guardar')
            mensaje.setWindowTitle('Error al guardar')
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.exec_()
        else:
            nombre = str(self.nombre.text().toUtf8())
            archivo = open(nombre + '.csv', 'w')
            archivo.write(str(self.data)[1:-1] + '\n')
            archivo.close()

            pdf = PdfPages(nombre + '.pdf')
            self.fig.savefig(pdf, format='pdf')
            pdf.close()

            self.canvas.print_figure(nombre + '.png', dpi=self.dpi)

            mensaje = QMessageBox(self)
            mensaje.setText('La prueba a sido guardada correctamente')
            mensaje.setWindowTitle('Guardado con exito')
            mensaje.setIcon(QMessageBox.Information)
            mensaje.exec_()
        
    def doPause(self):
        if self.timer.isActive():
            self.timer.stop()
            self.contadorPrincipal.stop()
            self.pause.setText('Reanudar')
        else:
            self.timer.start()
            self.contadorPrincipal.setInterval(self.tiempoPrueba.value() * 1000 - self.tiempoTrancurrido)
            self.contadorPrincipal.start()
            self.pause.setText('Pausar')
        
    def refresh(self):
        self.tiempoTrancurrido += 1000 / self.lecturasXSegundo
        #self.data.append(generaData())
        self.data.append(int(self.arduino.data))
        self.draw_chart()
        
        
    def draw_chart(self):
        count = round(len(self.data) * 1.0 / self.lecturasXSegundo, 3)
        xmax = count if count > 3 else 3
        xmin = xmax - 3
        
        self.axes.set_xbound(lower = xmin, upper = xmax)
        self.axes.set_ybound(lower = 0, upper = 1023)
        
        self.line.set_xdata(np.arange(0,count, 1.0 / self.lecturasXSegundo))
        self.line.set_ydata(np.array(self.data))
        
        self.canvas.draw()
        
    def closeEvent(self,event):
        self.arduino.stop()
        
def generaData():
    return random.randint(0,1023)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

# vim: ts=4 et sw=4 st=4 
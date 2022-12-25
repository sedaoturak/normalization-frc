# -------- Desktop Application for Normalization  -------- #
# Date: 25th December, 2021
# Author: Seda Oturak

import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QWidget, QMessageBox, QLineEdit
from PyQt5 import uic
from PyQt5.QtGui import QDoubleValidator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from db import Database
import cv2
import numpy as np

class PlotWindow(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(PlotWindow, self).__init__(fig)

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        # load gui file
        self.win = uic.loadUi(r"GUI.ui",self)

        self.csvPath = None
        self.imgPath = None
        self.db = None
        self.FVF = None
        self.cho_FVF = None
        self.nor_TS = None
        self.EM = None
        
        self.initUI()
        self.win.show()

    def initUI(self):
        """Activate buttons and other widgets"""

        self.win.btTest.clicked.connect(self.openFile)
        self.win.btImage.clicked.connect(self.fiber_volume_fraction)
        self.win.btOK.clicked.connect(self.chosen_FVF)
        self.win.btNorm.clicked.connect(self.normalize)

    def openFile(self):
        """Take test data from user and add it to database"""

        self.csvPath, _ = QFileDialog.getOpenFileName(self,"Open File",r"C:","csv File (*.csv)")
        
        # Send csv file to database
        self.db = Database(self.csvPath)

    def fiber_volume_fraction(self):
        """Take image from user and calculate fiber volume fraction from image"""
        
        self.imgPath, _ = QFileDialog.getOpenFileName(self,"Download Image",r"C:",)
        
        # read image
        img = cv2.imread(self.imgPath)

        # convert image color to gray
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # identify threshold to separate resin and fiber
        ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_TRIANGLE)

        # find number of black (resin) pixels
        black_pix = np.sum(thresh>ret)

        # find total number of pixels
        tot_pix = img.size

        # find number of white (fiber) pixels
        white_pix = tot_pix-black_pix

        # calculate fiber volume fraction        
        self.FVF = white_pix/tot_pix


    def chosen_FVF(self, line_edit):
        """Take normalizing fiber volume fraction from user"""

        # Take normalizing FVF as float format by line edit 
        self.line_edit = self.win.QLineEdit
        self.line_edit.setValidator(QDoubleValidator(0.00, 0.99, 2))
        # Convert text input to float
        self.cho_FVF = self.line_edit.text()
        self.cho_FVF = float(self.cho_FVF) if self.cho_FVF else 0

    def normalize(self):
        """Find normalized values of tensile strength and elastic modulus"""
        
        self.nor_TS = round(self.db.int_TS * self.cho_FVF/self.FVF)
        self.nor_EM = round(self.db.EM * self.cho_FVF/self.FVF)

        self.view_results()

    def view_results(self):
        """View stress vs. strain curve, normalized values and fiber volume fraction of the sample"""
        
        # plot stress & strain curve on a window
        self.db.plot()

        # # show normalized and FVF values on a window
        msg = QMessageBox()
        msg.setInformativeText("Normalized Tensile Strength: {} MPa \nNormalized Elastic Modulus: {} GPa \nFiber Volume Fraction: {:.2f}".format(self.nor_TS, self.nor_EM, self.FVF))
        msg.setWindowTitle("Results")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Analyzer(object):
    def setupUi(self, Analyzer):
        Analyzer.setObjectName("Analyzer")
        Analyzer.resize(712, 613)
        self.centralwidget = QtWidgets.QWidget(Analyzer)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.filterBox = QtWidgets.QComboBox(self.centralwidget)
        self.filterBox.setObjectName("filterBox")
        self.verticalLayout.addWidget(self.filterBox)
        self.analyze = QtWidgets.QPushButton(self.centralwidget)
        self.analyze.setObjectName("analyze")
        self.verticalLayout.addWidget(self.analyze)
        Analyzer.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Analyzer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 712, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        Analyzer.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Analyzer)
        self.statusbar.setObjectName("statusbar")
        Analyzer.setStatusBar(self.statusbar)
        self.actionLinear_Files = QtWidgets.QAction(Analyzer)
        self.actionLinear_Files.setObjectName("actionLinear_Files")
        self.actionPressure_Files = QtWidgets.QAction(Analyzer)
        self.actionPressure_Files.setObjectName("actionPressure_Files")
        self.actionInflator_Files = QtWidgets.QAction(Analyzer)
        self.actionInflator_Files.setObjectName("actionInflator_Files")
        self.actionExit = QtWidgets.QAction(Analyzer)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionLinear_Files)
        self.menuFile.addAction(self.actionPressure_Files)
        self.menuFile.addAction(self.actionInflator_Files)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(Analyzer)
        QtCore.QMetaObject.connectSlotsByName(Analyzer)

    def retranslateUi(self, Analyzer):
        _translate = QtCore.QCoreApplication.translate
        Analyzer.setWindowTitle(_translate("Analyzer", "Analyzer"))
        self.analyze.setText(_translate("Analyzer", "Read Data"))
        self.menuFile.setTitle(_translate("Analyzer", "File"))
        self.actionLinear_Files.setText(_translate("Analyzer", "Linear Files"))
        self.actionPressure_Files.setText(_translate("Analyzer", "Pressure Files"))
        self.actionInflator_Files.setText(_translate("Analyzer", "Inflator Files"))
        self.actionExit.setText(_translate("Analyzer", "Exit"))


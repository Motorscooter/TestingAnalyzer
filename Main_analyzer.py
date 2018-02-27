# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 13:58:10 2018

@author: scott.downard
"""
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import Mainwindow
from LinearReader import *
from exporttoexcel import *
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column, row, gridplot, widgetbox, layout
from bokeh.models import Legend, ColumnDataSource, HoverTool
from bokeh.models.widgets import Panel, Tabs, DataTable, TableColumn
import bokeh.io as bk
import bokeh.plotting
import numpy as np
import pandas as pd


class LinearApp(QtWidgets.QMainWindow, Mainwindow.Ui_Analyzer):

    
    def __init__(self,parent=None):
        filterlist = ['Raw','60','180']
        super(LinearApp, self).__init__(parent)
        self.setupUi(self)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['Test Name','Line Color'])
        self.filterBox.addItems(filterlist)

        self.actionLinear_Files.triggered.connect(self.browse_folder_linear)
        self.actionPressure_Files.triggered.connect(self.browse_folder_pressure)
        self.actionInflator_Files.triggered.connect(self.browse_folder_inflator)
#        self.openFile.clicked.connect(self.browse_folder)
#        self.graphbtn.clicked.connect(self.graph)
#        self.export_2.clicked.connect(self.exportexcel)
    def browse_folder_linear(self):
#        self.listWidget.clear()
        
        self.directory = QtWidgets.QFileDialog.getExistingDirectory(self,"Pick a Folder")
        if self.directory:
            self.tableWidget.clear()
            self.test_list = []
            group_list = []
            self.data_dict = fileReadlin(self.directory)            
            for keys in self.data_dict:
                self.test_list.append(keys)
             
            for i in range(len(self.test_list)):
                group_list.append(str(i+1))
            self.tableWidget.setRowCount(len(self.test_list))
            i = 0
            for k in self.test_list:
                self.tableWidget.setItem(i,0,QtWidgets.QTableWidgetItem("Test_"+str(k))) 
                comboBox = QtWidgets.QComboBox()
                comboBox.addItems(group_list)
                comboBox.setCurrentIndex(i)
                self.tableWidget.setCellWidget(i,1,comboBox)               
                i +=1
                
    def browse_folder_pressure(self):
#        self.listWidget.clear()
        
        self.directory = QtWidgets.QFileDialog.getExistingDirectory(self,"Pick a Folder")
        if self.directory:
            self.tableWidget.clear()
            self.test_list = []
            group_list = []
            self.data_dict = fileReadpres(self.directory)            
            for keys in self.data_dict:
                self.test_list.append(keys)
             
            for i in range(len(self.test_list)):
                group_list.append(str(i+1))
            self.tableWidget.setRowCount(len(self.test_list))
            i = 0
            for k in self.test_list:
                self.tableWidget.setItem(i,0,QtWidgets.QTableWidgetItem("Test_"+str(k))) 
                comboBox = QtWidgets.QComboBox()
                comboBox.addItems(group_list)
                comboBox.setCurrentIndex(i)
                self.tableWidget.setCellWidget(i,1,comboBox)               
                i +=1 
                
    def browse_folder_inflator(self):
#        self.listWidget.clear()
        
        self.directory = QtWidgets.QFileDialog.getExistingDirectory(self,"Pick a Folder")
        if self.directory:
            self.tableWidget.clear()
            self.test_list = []
            group_list = []
            self.data_dict = fileReadinfl(self.directory)            
            for keys in self.data_dict:
                self.test_list.append(keys)
             
            for i in range(len(self.test_list)):
                group_list.append(str(i+1))
            self.tableWidget.setRowCount(len(self.test_list))
            i = 0
            for k in self.test_list:
                self.tableWidget.setItem(i,0,QtWidgets.QTableWidgetItem("Test_"+str(k))) 
                comboBox = QtWidgets.QComboBox()
                comboBox.addItems(group_list)
                comboBox.setCurrentIndex(i)
                self.tableWidget.setCellWidget(i,1,comboBox)               
                i +=1    
    def exportexcel(self):
        i = 0
        savedirectory = QtWidgets.QFileDialog.getExistingDirectory(self,"Save File")
        for keys in self.data_dict:
            self.data_dict[keys]['Acceleration']['Title'] = self.test_name[i]
            i += 1
        exportToexcel(self.data_dict,self.data,savedirectory,self.titlebox.text())
        
        
    def graph(self):
        if self.directory:
            
            group_list = []
            self.test_name = []
            color_list = ['black','red','blue','green','purple','grey','orange',
              'yellow','darkgreen','magenta','gold','aquamarine']
            group_color = []
            filtersize = self.filterBox.currentText()
            plotTitle = self.titlebox.text()
            for i in range(len(self.test_list)):
                self.test_name.append(self.tableWidget.item(i,0).text())
                group_list.append(self.tableWidget.cellWidget(i,1).currentText())
            self.final_data = {i:group_list.count(i) for i in group_list}
            for key in self.final_data:
                self.final_data[key] = {}
            for i in group_list:
                group_color.append(color_list[int(i)])
            for i in range(len(self.test_list)):
                if filtersize == 'Raw':
                    continue
                else:
                    self.data_dict[self.test_list[i]]['Acceleration']['Data'] = filterProcessing(self.data_dict[self.test_list[i]]['Acceleration']
                    ['Data'],int(filtersize),self.data_dict[self.test_list[i]]
                    ['Acceleration']['Sample Rate'])
                
          
            test_list = []
            accel_list = []
            disp_list = []
            time_list = []

            #Check to make sure sample rate are the same between all tests, 
            #if they are
            #Create a variable for the sample rate of the build sheet.
            for key in self.data_dict:
                test_list.append(key)
                accel_list.append((self.data_dict[key]['Acceleration']['Data']))
                disp_list.append((self.data_dict[key]['Displacement']['Data']))
                time_list.append((self.data_dict[key]['Acceleration']['Time']))

            
            maxAccel, maxDisp, contTime = tableCalc(accel_list,disp_list,time_list)
#            output_file(plotTitle + '.html')
            p1 = figure(width = 1200, height = 450, title = plotTitle)
            p2 = figure(width = 1200, height = 450, title = plotTitle)
            legend_set1 = []
            legend_set2 = []
            for i in range(len(accel_list)):
                a = p1.line(disp_list[i],accel_list[i],line_color = group_color[i], alpha = 1, muted_color = group_color[i],muted_alpha=0)
                b = p2.line(time_list[i],accel_list[i],line_color = group_color[i], alpha = 1, muted_color = group_color[i],muted_alpha=0)
                legend_set1.append((self.test_name[i],[a]))
                legend_set2.append((self.test_name[i],[b]))
                
              
            
            

            
            legend1 = Legend(items = legend_set1, location=(0,0))
            legend1.click_policy = "mute"
            p1.add_layout(legend1,'right')   
            p1.legend.orientation = "vertical"
            p1.legend.padding = 1
            p1.xaxis.axis_label = "Displacement (mm)"
            p1.yaxis.axis_label = "Acceleration (g)"
            p1.xaxis.axis_label = "Displacement (mm)"
            p1.yaxis.axis_label = "Acceleration (g)"

            tab1 = Panel(child=p1, title='Accel vs Disp')            
            
            legend2 = Legend(items = legend_set2, location=(0,0))
            legend2.click_policy = "mute"            
            p2.legend.orientation = "vertical"
            p2.add_layout(legend2,'right')
            p2.legend.padding = 1
            p2.xaxis.axis_label = "Time (msec)"
            p2.yaxis.axis_label = "Acceleration (g)"    
            tab2 = Panel(child=p2, title='Accel vs Time')  


            self.data = dict(testnum = self.test_name,
                        max_accel = maxAccel,
                        max_displacment = maxDisp,
                        contact_time = contTime)
            source = ColumnDataSource(self.data)
            
            columns = [TableColumn(field= "testnum", title="Test Name"),
                       TableColumn(field= "max_accel" ,title="Maximum Acceleration"),
                       TableColumn(field= "max_displacment",title = "Maximum Dipslacement"),
                       TableColumn(field = "contact_time" ,title = "Contact Time @ 2g's")]
            data_table = DataTable(source = source, columns = columns, width = 700, height = 300) 
            tab3 = Panel(child=data_table, title= plotTitle + ' Data Table')                   
            tabs = Tabs(tabs=[tab1,tab2,tab3])
            show(tabs)
            
        
                
             

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = LinearApp()
    form.show()
    app.exec_()
if __name__ == '__main__':
    main()

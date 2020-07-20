# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'project.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from PyQt5 import  QtCore, QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import pymongo
from database_query import *


def parse_to_frame(cur,headers):
    new_dict = {}
    for header in headers:
        new_dict[header] = []
    for row in cur:
        for header in headers:
            new_dict[header].append(row[header])
    return new_dict
        
def limit(old_dict, num):
        new_dict = dict(old_dict)
        for key in old_dict.keys():
            n = len(old_dict[key])
            if n <= num: 
                return new_dict
            for i in range(num,n,1):
                new_dict[key].pop(num)
        return new_dict


secret = open('confidentials.txt')
info = []
for line in secret:
    info.append(line.strip())
myclient = pymongo.MongoClient("mongodb+srv://"+info[1]+":"+info[0]+"@cluster0.oyu7v.mongodb.net/"+info[2]+"?retryWrites=true&w=majority")
mydb = myclient["calgary_traffic"]
col_v_16 = mydb["traffic_volume_2016"]
col_v_17 = mydb["traffic_volume_2017"]
col_v_18 = mydb["traffic_volume_2018"]
h_v_16 = []
h_v_17 = []
h_v_18 = []
for key in col_v_16.find_one():
    if key == '_id': continue
    h_v_16.append(key)
for key in col_v_17.find_one():
    if key == '_id': continue
    h_v_17.append(key)
for key in col_v_18.find_one():
    if key == '_id': continue
    h_v_18.append(key)
    
d_v_16 = parse_to_frame(col_v_16.find().limit(100),h_v_16)
d_v_17 = parse_to_frame(col_v_17.find().limit(100),h_v_17)
d_v_18 = parse_to_frame(col_v_18.find().limit(100),h_v_18)
d_v_16_s = parse_to_frame(col_v_16.find().sort('volume',-1).limit(100),h_v_16)
d_v_17_s = parse_to_frame(col_v_17.find().sort('volume',-1).limit(100),h_v_17)
d_v_18_s = parse_to_frame(col_v_18.find().sort('VOLUME',-1).limit(100),h_v_18)

volume_2016 = DBQuery(mydb,year='2016')
volume_2017 = DBQuery(mydb,year='2017')
volume_2018 = DBQuery(mydb,year='2018')
m_v_16 = volume_2016.total_max()
m_v_17 = volume_2017.total_max()
m_v_18 = volume_2018.total_max()

col_a = mydb["traffic_incidents"]
h_a = []
for key in col_a.find_one():
    if key == '_id': continue
    h_a.append(key)

d_a_16 = parse_to_frame(col_a.find({'START_DT':{'$regex':'2016'}}).limit(100),h_a)
d_a_17 = parse_to_frame(col_a.find({'START_DT':{'$regex':'2017'}}).limit(100),h_a)
d_a_18 = parse_to_frame(col_a.find({'START_DT':{'$regex':'2018'}}).limit(100),h_a)

traffic_accidents = DBQuery(mydb,type='accident')
d_a_16_s = limit(traffic_accidents.get_sorted_incident(year='2016'),20)
d_a_17_s = limit(traffic_accidents.get_sorted_incident(year='2017'),20)
d_a_18_s = limit(traffic_accidents.get_sorted_incident(year='2018'),20)
m_a_16 = traffic_accidents.max_accident(year='2016')[1]
m_a_17 = traffic_accidents.max_accident(year='2017')[1]
m_a_18 = traffic_accidents.max_accident(year='2018')[1]

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalFrame = QtWidgets.QFrame(self.centralwidget)
        self.verticalFrame.setGeometry(QtCore.QRect(30, 30, 211, 501))
        self.verticalFrame.setAutoFillBackground(True)
        self.verticalFrame.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.verticalFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.verticalFrame.setObjectName("verticalFrame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalFrame)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.comboBox = QtWidgets.QComboBox(self.verticalFrame)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(["Traffic Volume","Traffic Incidents"])
        self.verticalLayout.addWidget(self.comboBox)
        self.comboBox_2 = QtWidgets.QComboBox(self.verticalFrame)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItems(["2016","2017","2018"])
        self.verticalLayout.addWidget(self.comboBox_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.pushButton_1 = QtWidgets.QPushButton(self.verticalFrame)
        self.pushButton_1.setObjectName("pushButton_1")
        self.pushButton_1.clicked.connect(lambda:self.b1Callback())
        self.verticalLayout.addWidget(self.pushButton_1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalFrame)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(lambda :self.b2Callback())
        self.verticalLayout.addWidget(self.pushButton_2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem3)
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalFrame)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(lambda :self.b3Callback())
        self.verticalLayout.addWidget(self.pushButton_3)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem4)
        self.pushButton_4 = QtWidgets.QPushButton(self.verticalFrame)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(lambda :self.b4Callback())
        self.verticalLayout.addWidget(self.pushButton_4)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem5)
        self.label = QtWidgets.QLabel(self.verticalFrame)
        self.label.setStyleSheet("QLabel {background-color:rgb(255, 0, 0)}")
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(270, 30, 491, 521))
        self.stackedWidget.setFrameShape(QtWidgets.QFrame.Panel)
        self.stackedWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.widget = QtWidgets.QWidget(self.page)
        self.widget.setGeometry(QtCore.QRect(0, 0, 490, 520))
        self.widget.setObjectName("widget")
        self.stackedWidget.addWidget(self.page)
        #pg.setConfigOptions(foreground='d',background='k')
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.tableWidget = QtWidgets.QTableWidget(self.page_2)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 490, 520))
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(4)
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.webView = QWebEngineView(self.page_3)
        
        self.webView.setGeometry(QtCore.QRect(0, 0, 490, 520))
        self.webView.load(QUrl("file:///C:/traffic_2016.html"))
        self.webView.show()
        self.webView.setObjectName("webView")
        self.stackedWidget.addWidget(self.page_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.gw = pg.GraphicsLayoutWidget(parent=self.page)
        self.gw.resize(490,520)
        self.plot = self.gw.addPlot(title='Dummy',labels={'left':'Y','bottom':'X'})
        self.retranslateUi(MainWindow)
        self.comboBox.setCurrentIndex(0)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_1.setText(_translate("MainWindow", "Read"))
        self.pushButton_2.setText(_translate("MainWindow", "Sort"))
        self.pushButton_3.setText(_translate("MainWindow", "Analyze"))
        self.pushButton_4.setText(_translate("MainWindow", "Map"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        
    def b1Callback(self):
        try:
            self.pending()
            self.stackedWidget.setCurrentIndex(1)
            self.tableWidget.clear()
            choice1 = self.comboBox.currentText()
            choice2 = self.comboBox_2.currentText()
            data = {}
            if 'olum' in choice1:
                if '16' in choice2:
                    data = d_v_16
                elif '17' in choice2:
                    data = d_v_17
                else:
                    data = d_v_18
            else:
                if '16' in choice2:
                    data = d_a_16
                elif '17' in choice2:
                    data = d_a_17
                else:
                    data = d_a_18
            self.populate_table(data)
            self.success('Collection read')
        except:
            self.failure('Collection not read')
        
        
        
    def b2Callback(self):
        try:
            self.pending()
            self.stackedWidget.setCurrentIndex(1)
            self.tableWidget.clear()
            choice1 = self.comboBox.currentText()
            choice2 = self.comboBox_2.currentText()
            data = {}
            if 'olum' in choice1:
                if '16' in choice2:
                    data = d_v_16_s
                elif '17' in choice2:
                    data = d_v_17_s
                else:
                    data = d_v_18_s
            else:
                if '16' in choice2:
                    data = d_a_16_s
                elif '17' in choice2:
                    data = d_a_17_s
                else:
                    data = d_a_18_s
            self.populate_table(data)
            self.success('Data sorted')
        except:
            self.failure('Data not sorted')
        
    def b3Callback(self):
        try:
            self.pending()
            self.stackedWidget.setCurrentIndex(0)
            self.plot.clear()
            year = [2016, 2017, 2018]
            title = ''
            typ = ''
            data = [0, 0, 0]
            choice1 = self.comboBox.currentText()
            if 'olum' in choice1:
                title = 'Traffic Flow plot'
                data = [m_v_16,m_v_17,m_v_18]
                typ = 'Highest traffic volume'
            else:
                title = 'Traffic Incident plot'
                data = [m_a_16,m_a_17,m_a_18]
                typ = 'Highest incident concentration'
            self.plot.setLabels(title=title,left=typ,bottom='Year')
            self.curve = self.plot.plot(year,data)
            self.success('Data plotted')
        except:
            self.failure('Data not plotted')
        
    def b4Callback(self):
        try:
            self.pending()
            self.stackedWidget.setCurrentIndex(2)
            self.tableWidget.clear()
            choice1 = self.comboBox.currentText()
            choice2 = self.comboBox_2.currentText()
            link_name = ''
            if 'olum' in choice1:
                if '16' in choice2:
                    link_name = "file:///C:/traffic_2016.html"
                elif '17' in choice2:
                    link_name = "file:///C:/traffic_2017.html"
                else:
                    link_name = "file:///C:/traffic_2018.html"
            else:
                if '16' in choice2:
                    link_name = "file:///C:/incidents_2016.html"
                elif '17' in choice2:
                    link_name = "file:///C:/incidents_2017.html"
                else:
                    link_name = "file:///C:/incidents_2018.html"
            self.webView.load(QUrl(link_name))
            self.success('Map displayed')
        except:
            self.failure('Map not displayed')
        
    def populate_table(self, struct):
        self.tableWidget.clear()
        col = row = 0
        headers = []
        for key in struct.keys():
            headers.append(key)
            row = len(struct[key])
            col += 1
        self.tableWidget.setHorizontalHeaderLabels(headers)
        self.tableWidget.setColumnCount(col)
        self.tableWidget.setRowCount(row)
        for n, key in enumerate(struct):
            for m, item in enumerate(struct[key]):
                newitem=QtWidgets.QTableWidgetItem(str(item))
                self.tableWidget.setItem(m,n,newitem)
        
            
        
        
    def pending(self):
        self.label.setText('Executing...')
        self.label.setStyleSheet("QLabel {background-color:yellow}")
        
    def success(self,text):
        self.label.setText(text)
        self.label.setStyleSheet("QLabel {background-color:green}")
        
    def failure(self,text):
        self.label.setText(text)
        self.label.setStyleSheet("QLabel {background-color:red}")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

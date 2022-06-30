# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'results.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(800, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(10, 50, 781, 501))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 779, 499))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.tableWidget = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.tableWidget.setGeometry(QtCore.QRect(5, 1, 771, 491))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.scrollArea.setWidget(self.tableWidget)
        self.vb=QtWidgets.QVBoxLayout()
        self.vb.addWidget(self.scrollArea)
        MainWindow.setLayout(self.vb)


        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 10, 75, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(110, 10, 81, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.res=[]
        self.m=MainWindow
        #self.pushButton.clicked.connect(self.export)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Results"))
        self.pushButton.setText(_translate("MainWindow", "Export"))
        self.pushButton_2.setText(_translate("MainWindow", "Save As HTML"))
    def table(self,res):

        self.tableWidget.setRowCount(len(res.items())*11)
        self.tableWidget.setColumnCount(9)
        header=['Video','Time','Class','DIVIDER1','DIVIDER2','DIVIDER3','DIVIDER6','DIVIDER5','DIVIDER6']
        self.tableWidget.setHorizontalHeaderLabels(header)
        self.res.append(header)
        classes = ["car","bicycle","motorcycle","bus","background","non-motorized_vehicle","single_unit_truck","pedestrian","work_van","articulated_truck","pickup_truck"]

        for i in range(len(res)):
            self.res.append(res[i+1])
            for ic in range(len(classes)):


                self.tableWidget.setItem(i*11+ic, 0, QTableWidgetItem(str(res[i+1][0])))
                self.tableWidget.setItem(i*11+ic, 1, QTableWidgetItem(str(res[i+1][1])))
                self.tableWidget.setItem(i*11+ic, 2, QTableWidgetItem(str(classes[ic])))
                self.tableWidget.setItem(i*11+ic, 3, QTableWidgetItem(str(res[i+1][2][ic])))
                self.tableWidget.setItem(i*11+ic, 4, QTableWidgetItem(str(res[i+1][3][ic])))
                self.tableWidget.setItem(i*11+ic, 5, QTableWidgetItem(str(res[i+1][4][ic])))
                self.tableWidget.setItem(i*11+ic, 6, QTableWidgetItem(str(res[i+1][5][ic])))
                self.tableWidget.setItem(i*11+ic, 7, QTableWidgetItem(str(res[i+1][6][ic])))
                self.tableWidget.setItem(i*11+ic, 8, QTableWidgetItem(str(res[i+1][7][ic])))
            #self.tableWidget.setItem(i, 8, QTableWidgetItem(str(classes[ic])))
        self.tableWidget.move(0, 0)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        newres = []
        head = self.res[0]
        newres.append(head)
        for i in self.res[1:]:
            for ic in range(len(classes)):
                r = [i[0], i[1], classes[ic], i[2][ic], i[3][ic], i[4][ic], i[5][ic], i[6][ic], i[7][ic]]
                newres.append(r)
        self.res=newres







if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    #res={1:['vid','121',1,2,3,4,5,6],4:['vid','121',1,2,3,4,5,6],5:['vid','121',1,2,3,4,5,6],6:['vid','121',1,2,3,4,5,6],7:['vid','121',1,2,3,4,5,6],8:['vid','121',1,2,3,4,5,6],9:['vid','121',1,2,3,4,5,6],2:['vid','121',1,2,3,4,5,6],3:['vid','121',1,2,3,4,5,6]}

    #ui.table(res)

    MainWindow.show()
    sys.exit(app.exec_())


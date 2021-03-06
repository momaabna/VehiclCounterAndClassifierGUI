# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'v1.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 633)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        #self.centralwidget.setGeometry(QtCore.QRect(293, 2, 891, 511))
        #self.centralwidget.autoFillBackground()
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(2, 2, 256, 192))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(290, 0, 891, 511))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")


        self.label = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)#QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(290, 0, 891, 511))

        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setGeometry(QtCore.QRect(293, 2, 891, 511))
        self.scroll.setFrameRect(QtCore.QRect(293, 2, 891, 511))
        self.scroll.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.formLayout = QtWidgets.QGridLayout()

        self.label.addWidget(self.scroll)

        #self.label.setAutoFillBackground(True)
        #self.label.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        #self.label.setObjectName("label")
        self.listWidget_2 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_2.setGeometry(QtCore.QRect(0, 220, 256, 281))
        self.listWidget_2.setObjectName("listWidget_2")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(400, 520, 781, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(300, 520, 91, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSetting = QtWidgets.QMenu(self.menubar)
        self.menuSetting.setObjectName("menuSetting")
        self.menuSetting_2 = QtWidgets.QMenu(self.menubar)
        self.menuSetting_2.setObjectName("menuSetting_2")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        self.menuAbout_2 = QtWidgets.QMenu(self.menubar)
        self.menuAbout_2.setObjectName("menuAbout_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setIconSize(QtCore.QSize(32, 32))
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionOpen_Project = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/png/favorites.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen_Project.setIcon(icon1)
        self.actionOpen_Project.setObjectName("actionOpen_Project")
        self.actionSave = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/images/png/tif file.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon2)
        self.actionSave.setObjectName("actionSave")
        self.actionClip_From_Video = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/images/png/movie folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionClip_From_Video.setIcon(icon3)
        self.actionClip_From_Video.setObjectName("actionClip_From_Video")
        self.actionClip_From_Online_Source = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/images/png/url history.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionClip_From_Online_Source.setIcon(icon4)
        self.actionClip_From_Online_Source.setObjectName("actionClip_From_Online_Source")
        self.actionClip_Time = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/images/png/volume.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionClip_Time.setIcon(icon5)
        self.actionClip_Time.setObjectName("actionClip_Time")
        self.actionView = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/images/png/computer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionView.setIcon(icon6)
        self.actionView.setObjectName("actionView")
        self.actionWorkSpace = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/images/png/network drive connected.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionWorkSpace.setIcon(icon7)
        self.actionWorkSpace.setObjectName("actionWorkSpace")
        self.actionNew_Project = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/images/png/folder close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew_Project.setIcon(icon8)
        self.actionNew_Project.setObjectName("actionNew_Project")
        self.actionClassification_Setting = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/images/png/help and suport.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionClassification_Setting.setIcon(icon9)
        self.actionClassification_Setting.setObjectName("actionClassification_Setting")
        self.actionCounter_Setting = QtWidgets.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/images/png/counter.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCounter_Setting.setIcon(icon10)
        self.actionCounter_Setting.setObjectName("actionCounter_Setting")
        self.actionStart = QtWidgets.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/images/png/Play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionStart.setIcon(icon11)
        self.actionStart.setObjectName("actionStart")
        self.actionPause = QtWidgets.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/images/png/Pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPause.setIcon(icon12)
        self.actionPause.setObjectName("actionPause")
        self.actionClip_From_USB_Camera = QtWidgets.QAction(MainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/images/png/webcam-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionClip_From_USB_Camera.setIcon(icon13)
        self.actionClip_From_USB_Camera.setObjectName("actionClip_From_USB_Camera")
        self.actionNumber_Of_Threads = QtWidgets.QAction(MainWindow)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/images/png/processor.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNumber_Of_Threads.setIcon(icon14)
        self.actionNumber_Of_Threads.setObjectName("actionNumber_Of_Threads")
        self.menuFile.addAction(self.actionNew_Project)
        self.menuFile.addAction(self.actionOpen_Project)
        self.menuFile.addAction(self.actionSave)
        self.menuSetting.addAction(self.actionClip_From_Video)
        self.menuSetting.addAction(self.actionClip_From_Online_Source)
        self.menuSetting.addAction(self.actionClip_From_USB_Camera)
        self.menuSetting.addAction(self.actionStart)
        self.menuSetting.addAction(self.actionPause)
        self.menuSetting_2.addAction(self.actionClip_Time)
        self.menuSetting_2.addAction(self.actionWorkSpace)
        self.menuSetting_2.addAction(self.actionClassification_Setting)
        self.menuSetting_2.addAction(self.actionCounter_Setting)
        self.menuSetting_2.addAction(self.actionNumber_Of_Threads)
        self.menuAbout.addAction(self.actionView)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSetting.menuAction())
        self.menubar.addAction(self.menuSetting_2.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.menubar.addAction(self.menuAbout_2.menuAction())
        self.toolBar.addAction(self.actionNew_Project)
        self.toolBar.addAction(self.actionOpen_Project)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionClip_From_Video)
        self.toolBar.addAction(self.actionClip_From_Online_Source)
        self.toolBar.addAction(self.actionClip_From_USB_Camera)
        self.toolBar.addAction(self.actionStart)
        self.toolBar.addAction(self.actionPause)
        self.toolBar.addAction(self.actionClip_Time)
        self.toolBar.addAction(self.actionNumber_Of_Threads)
        self.toolBar.addAction(self.actionClassification_Setting)
        self.toolBar.addAction(self.actionWorkSpace)
        self.toolBar.addAction(self.actionCounter_Setting)
        self.toolBar.addAction(self.actionView)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Vehicle Counter and Classifier"))
        #self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><img src=\":/images/icon.png\"/></p></body></html>"))
        self.progressBar.setFormat(_translate("MainWindow", "%p%"))
        self.label_2.setText(_translate("MainWindow", "Idle"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSetting.setTitle(_translate("MainWindow", "Video"))
        self.menuSetting_2.setTitle(_translate("MainWindow", "Setting"))
        self.menuAbout.setTitle(_translate("MainWindow", "View"))
        self.menuAbout_2.setTitle(_translate("MainWindow", "About"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionOpen_Project.setText(_translate("MainWindow", "Open Project"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionClip_From_Video.setText(_translate("MainWindow", "Clip From Video"))
        self.actionClip_From_Online_Source.setText(_translate("MainWindow", "Clip From Online Source"))
        self.actionClip_Time.setText(_translate("MainWindow", "Clip Time"))
        self.actionView.setText(_translate("MainWindow", "View"))
        self.actionWorkSpace.setText(_translate("MainWindow", "WorkSpace"))
        self.actionNew_Project.setText(_translate("MainWindow", "New Project"))
        self.actionClassification_Setting.setText(_translate("MainWindow", "Classification Setting"))
        self.actionCounter_Setting.setText(_translate("MainWindow", "Counter Setting"))
        self.actionStart.setText(_translate("MainWindow", "Start"))
        self.actionPause.setText(_translate("MainWindow", "Pause"))
        self.actionClip_From_USB_Camera.setText(_translate("MainWindow", "Clip From USB Camera"))
        self.actionNumber_Of_Threads.setText(_translate("MainWindow", "Number Of Threads"))

import resource

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


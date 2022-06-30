from PyQt5 import QtWidgets,QtCore,Qt,QtGui
from PyQt5.QtWidgets import QMessageBox,QFileDialog,QLabel,QProgressBar,QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal
from MainWindow import Ui_MainWindow
import math,os
import f,copy
import socket, pickle,json
from decimal import Decimal
import threading
import time
import numpy as np
import pandas as pd
import resource
length=640
height=480
DIVIDER1 = (DIVIDER1_A, DIVIDER1_B) = ((180,480),(180,1))#((length / 3, height), (length / 3, 290))
DIVIDER2 = (DIVIDER2_A, DIVIDER2_B) = ((int(length / 2), height), (int(length / 2), 290))
DIVIDER3 = (DIVIDER3_A, DIVIDER3_B) = ((int(length / 3 * 2), height), (int(length / 3 * 2), 290))
DIVIDER4 = (DIVIDER4_A, DIVIDER4_B) = ((298,274),(355,169))#((length / 6, 250), (length / 6, 140))
DIVIDER5 = (DIVIDER5_A, DIVIDER5_B) = ((int(length / 3), 250), (int(length / 3), 140))
DIVIDER6 = (DIVIDER6_A, DIVIDER6_B) = ((int(length / 5 * 4), 250), (int(length / 5 * 4), 140))


import cv2
class MainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self,app):
        super().__init__()
        self.setupUi(self)
        self.app=app
        self.show()
        self.cam_id = 1
        self.videoSources=[]
        self.videoSources_path=[]
        self.thr=3
        self.min=2500
        self.max=40000
        self.DIVIDERS=[((0,0),(0,0)),((0,0),(0,0)),((0,0),(0,0)),((0,0),(0,0)),((0,0),(0,0)),((0,0),(0,0))]
        self.cap = cv2.VideoCapture()
        self.timer_interval = 4000
        self.actionClip_Time.triggered.connect(self.clipTime)
        self.actionStart.triggered.connect(self.start)
        self.actionPause.triggered.connect(self.pause)
        self.actionClip_From_USB_Camera.triggered.connect(self.select_usb_cam)
        self.actionClip_From_Video.triggered.connect(self.videoSource_file)
        self.actionNumber_Of_Threads.triggered.connect(self.nofth)
        self.actionCounter_Setting.triggered.connect(self.get_dividers)
        self.listWidget.itemDoubleClicked.connect(self.selectedvv)
        self.listWidget.itemClicked.connect(self.selectedv)
        self.actionSave.triggered.connect(self.save_to_file)
        self.actionOpen_Project.triggered.connect(self.open_file)
        self.actionNew_Project.triggered.connect(self.new_project)
        self.actionWorkSpace.triggered.connect(self.set_workspace)
        self.res_labels=[]
        self.current_counter=[]
        self.clip_time=90
        self.labelLis = []
        self.comboList = []
        self.timer = QtCore.QTimer()
        self.current_state=[]
        self.current_ms=[]
        self.th=serverThread()
        self.th.signal.connect(self.update_frame)
        self.th.start()
        self.segments=[]
        self.tsegments=[]
        self.seg_caps=[]
        self.worspace=''
        self.results={}
        #feature Disable
        self.actionClip_From_USB_Camera.setEnabled(False)
        self.actionClip_From_Online_Source.setEnabled(False)
        self.actionClassification_Setting.triggered.connect(self.set_classification_setting)
        self.actionAbout.triggered.connect(self.about)
        self.current_file=''
        self.current_project=None
        self.dis_results={}
        self.actionView.triggered.connect(self.show_results)





    def pause(self):
        self.th.stop()
    def select_usb_cam(self):
        input, ok = QtWidgets.QInputDialog.getInt(self, 'Setting', 'Please Input Camera ID', self.cam_id,0,255)
        if ok:
            try:


                self.videoSources.append('USB Camera '+str(input))

                self.videoSources_path.append(input)
                self.refresh_widget()

            except:
                ok1=QtWidgets.QMessageBox(self,'Error','This ID is Not Valid')

    def clipTime(self):
        input,ok = QtWidgets.QInputDialog.getInt(self,'Setting','Please Enter Clip Time (Seconds)',self.clip_time)
        if ok:
            self.clip_time=input
            #self.update_frames()
    def show_results(self):

        disp_results = copy.deepcopy(self.results)


        for i in range(len(disp_results.items())):
            disp_results[i+1].insert(0,self.segments[i][1].split('/')[-1])
            disp_results[i + 1].insert(1, f.display_time(self.segments[i][2])+'->'+f.display_time(self.segments[i][3]))

        import results as res

        self.resWindow = QtWidgets.QMainWindow()
        self.ui=res.Ui_MainWindow()
        self.ui.setupUi(self.resWindow)
        self.ui.table(disp_results)
        self.ui.pushButton.clicked.connect(self.export)
        self.ui.pushButton_2.clicked.connect(self.print_html)

        self.resWindow.show()

    def export(self):
        classes = ["car", "bicycle", "motorcycle", "bus", "background", "non-motorized_vehicle", "single_unit_truck",
                   "pedestrian", "work_van", "articulated_truck", "pickup_truck"]

        file, _ = QFileDialog.getSaveFileName(self.resWindow, 'File To Save to', '', 'csv Files (*.csv)')
        if file:

            print('Export')
            newres=self.ui.res[1:]
            head= self.ui.res[0]
            df=pd.DataFrame(data=newres,columns=head)
            df.to_csv(file)
            QMessageBox.information(self.resWindow,'Export','File Saved Successfully to Path \n'+file,QMessageBox.Yes,QMessageBox.Yes)
    def print_html(self):
        file, _ = QFileDialog.getSaveFileName(self.resWindow, 'File To Save to', '', 'html Files (*.html)')
        if file:
            df = pd.DataFrame(data=self.ui.res[1:], columns=self.ui.res[0])
            df.to_html(file)
            header="<center><h3>Report</h3><br />"
            with open(file,'r') as f:
                header+=f.read()
                header+='</center>'
            with open(file,'w') as f:
                f.write(header)
            QMessageBox.information(self.resWindow, 'Export', 'File Saved Successfully to Path \n' + file,
                                    QMessageBox.Yes, QMessageBox.Yes)
    def about(self):
        QMessageBox.information(self,'About Software','This Software is Developed By \n Mohammed Nasser \nAll Right Reserved For Developer\n ',QMessageBox.Yes,QMessageBox.Yes,)



    def set_classification_setting(self):
        input, ok = QtWidgets.QInputDialog.getInt(self, 'Setting', 'Please Enter Minimum Size (Pixels)', self.min)
        if ok:
            self.min = input
        input, ok = QtWidgets.QInputDialog.getInt(self, 'Setting', 'Please Enter Maximum Size (Pixels)', self.max)
        if ok:
            self.max = input
    def nofth(self):
        input, ok = QtWidgets.QInputDialog.getInt(self, 'Setting', 'Please Input Number Of Threads ', self.thr,1,32)
        if ok:
            self.thr = input


    def update_frame(self,data):
        #re, img = self.cap.read()

        re=False
        dd =data.split('|')
        id=int(dd[0])-1
        self.current_state[id]=float(dd[2])
        self.current_ms[id]=Decimal(dd[-1])
        self.current_counter[id]=dd[1]



        per=0
        for k,i in enumerate(self.current_state):
            self.comboList[k].setValue((i/self.clip_time)*100)
            self.res_labels[k].setText(self.current_counter[k])
            per+=(i/self.clip_time)*(100/len(self.segments))
        self.progressBar.setValue(per)








        print("data Recived from task id:",data)
        img=0
        if re:
            a = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            rawImage = QtGui.QImage(a.data, a.shape[1], a.shape[0], QtGui.QImage.Format_RGB888)


            p = QtGui.QPixmap.fromImage(rawImage)




            p = p.scaled(self.label.size().width(), self.label.size().height(), QtCore.Qt.KeepAspectRatio)

            self.label.setPixmap(p)
            print('Update Frame')
        print(self.current_state)
    def videoSource_file(self):
        files = QtWidgets.QFileDialog.getOpenFileNames(self,'Open Video File','','MP4 Files(*.mp4)')
        #self.listWidget.setViewMode(QtWidgets.QListVie)

        if files:
            for filepath in files[0]:


                print(filepath)
                filename=filepath.split('/')[-1]
                self.videoSources_path.append(filepath)
                self.videoSources.append(filename)
            self.refresh_widget()


    def refresh_widget(self):
        print('ref')

        self.listWidget.clear()
        for item in self.videoSources:
            self.listWidget.addItem(item)

        #self.listWidget.addItem(self.videoSources[i])
        #self.listWidget.setCurrentRow(0)
    def update_frames(self):
        for i,v in enumerate(self.current_state):
            if v>0:
                #pos =self.current_ms[i]
                #capp=cv2.VideoCapture(self.segments[i][1])
                #capp.set(cv2.CAP_PROP_POS_MSEC,pos)
                re=False

                #re,img =self.capp.read()
                if re:
                    img = cv2.resize(img, (200, 200))
                    self.seg_caps[id] = img
                    capp.release()

        #rows = []


        if len(self.current_state)>0:
            #groupBox.destroy()

            for i in reversed(range(self.formLayout.count())):
                self.formLayout.itemAt(i).widget().deleteLater()

        groupBox = QtWidgets.QGroupBox("Threads Progress in Each Video Segment  ")
        self.labelLis.clear()
        self.comboList.clear()
        self.res_labels.clear()
        for i in range(len(self.segments)):
            self.labelLis.append(QLabel(str(self.segments[i][1].split('/')[-1] +' '+ f.display_time(self.segments[i][2])+'-->'+f.display_time(self.segments[i][3]) )))
            self.comboList.append(QtWidgets.QProgressBar())
            self.res_labels.append(QLabel('[0,0,0,0,0,0]'))
            #formLayout.addRow([self.labelLis[i], self.comboList[i],self.res_labels[i]])
            self.formLayout.addWidget(self.labelLis[i],i,0,)

            self.formLayout.addWidget(self.comboList[i],i,1)
            self.formLayout.addWidget(self.res_labels[i], i, 2)
            self.labelLis[i].setMaximumHeight(20)
            self.comboList[i].setMaximumHeight(20)
            self.comboList[i].setMinimumWidth(400)


            self.res_labels[i].setMaximumHeight(20)
            self.res_labels[i].setMinimumWidth(150)
            self.labelLis[i].setMinimumWidth(250)



        groupBox.setLayout(self.formLayout)


        self.scroll.setWidget(groupBox)


        #self.scroll.setWidgetResizable(True)



        #layout = QVBoxLayout(self)

        #self.setLayout(self.label)
        #nr=2#math.ceil(len(self.seg_cap) / 3.0)
        #print(nr)
        #for i in range(1):
        #    row = [self.seg_caps[i * 3], self.seg_caps[i * 3 + 1]]#, self.seg_caps[i * 3 + 2]]
        #    temprow = np.concatenate(row, axis=1)
        #    rows.append(temprow)
        #res=np.concatenate(rows, axis=0)
        #progress=np.concatenate([self.seg_caps[0], self.seg_caps[1]], axis=1)#temprow
        #a = cv2.cvtColor(progress, cv2.COLOR_BGR2RGB)
        #rawImage = QtGui.QImage(a.data, a.shape[1], a.shape[0], QtGui.QImage.Format_RGB888)
        #p = QtGui.QPixmap.fromImage(rawImage)
        #print('here')

        # self.label.adjustSize()

        #p = p.scaled(self.label.size().height(), self.label.size().height(), QtCore.Qt.KeepAspectRatio)
        #self.label.setPixmap(p)

    def set_workspace(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.worspace=file+'/'
    def start(self):
        print('Start')
        f.stop_classify()
        self.th.yes()
        self.segments.clear()
        self.current_state.clear()
        self.current_counter.clear()
        self.current_ms.clear()
        self.label_2.setText('Processing...')
        for i in range(len(self.segments)):
            self.seg_caps.append(np.zeros([200,200,3],np.uint8))

        #self.timer.timeout.connect(self.update_frames)
        #self.timer.start(self.timer_interval)

        id=0
        for vid in self.videoSources_path:

            self.cap = cv2.VideoCapture(vid)

            N_Frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

            FPS = int(self.cap.get(cv2.CAP_PROP_FPS))

            # N_P = math.ceil((N_Frames/FPS)/self.clip_time)
            Seconds = math.floor(N_Frames / FPS)

            self.cap.release()

            for i in range(0, Seconds, self.clip_time):
                id += 1
                start=i
                end=i+self.clip_time
                #tvid=self.worspace+str(start)+'_'+str(end)+'_'+vid.split('/')[-1]

                #os.system('copy "'+vid+'" "'+tvid+'"')
                #self.tsegments.append([id,tvid,start,end,self.DIVIDERS[0],self.DIVIDERS[1],self.DIVIDERS[2],self.DIVIDERS[3],self.DIVIDERS[4],self.DIVIDERS[5]])
                self.segments.append([id,vid,start,end,self.DIVIDERS[0],self.DIVIDERS[1],self.DIVIDERS[2],self.DIVIDERS[3],self.DIVIDERS[4],self.DIVIDERS[5],self.min,self.max])
                self.current_state.append(0)
                self.current_ms.append(0)
                self.current_counter.append('[0,0,0,0,0,0]')

        self.pth=processingThread()

        self.update_frames()
        self.pth.seg=self.segments
        print(self.segments)
        self.pth.n=self.thr
        self.pth.signal.connect(self.finished)
        self.pth.start(QThread.HighestPriority)


    def finished(self,msg):
        if(msg[0]=='finished' and self.th.state=='OK'):
            self.progressBar.setValue(100)
            for i in range(len(self.segments)):
                self.comboList[i].setValue(100)
            self.label_2.setText('Finished')
            print(msg[1])

            buttonReply = QMessageBox.question(self, 'Processing Finished', "Processing Finished \n Do You Want to Save Rsults ?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if buttonReply==QMessageBox.Yes:
                self.results=msg[1]
                self.save_to_file()

        else:
            buttonReply = QMessageBox.question(self, 'Processing Aborted', "Processing Aborted \n Process Aborted Or Some Error Happened While Peocessing ?",
                                               QMessageBox.Yes , QMessageBox.Yes)
            self.progressBar.setValue(0)
            self.label_2.setText('Error')
    def get_dividers(self):
        input, ok = QtWidgets.QInputDialog.getInt(self, 'Setting', 'Number Of Dividers ', self.thr, 1, 6)
        if ok:
            self.cap = cv2.VideoCapture(self.videoSources_path[0])
            re,img=self.cap.read()
            if re:
                self.dth=dividersThread()

                self.dth.signal.connect(self.set_div)
                self.dth.div=input
                self.dth.img=img
                self.dth.start()
    def set_div(self,data):
        print(data[1])
        print(self.dth.div)

        for i in range(self.dth.div):

            self.DIVIDERS[i]=((data[1][i*2][0],data[1][i*2][1]),(data[1][i*2+1][0],data[1][i*2+1][1]))
    def save_to_file(self):

        self.current_project=project()
        self.current_project.c_T=self.clip_time
        self.current_project.divs=self.DIVIDERS
        self.current_project.nth=self.thr

        self.current_project.vids=self.videoSources
        self.current_project.vidp=self.videoSources_path
        self.current_project.ws=self.worspace
        self.current_project.min=self.min
        self.current_project.max=self.max
        self.current_project.results=self.results
        self.current_project.seg=self.segments

        if self.current_file=='':
            file,_=QFileDialog.getSaveFileName(self,'File To Save to','','vcc Files (*.vcc)')
            if file:
                pickle_out = open(file, "wb")
                pickle.dump(self.current_project, pickle_out)
                pickle_out.close()
                self.current_file=file
        else:
            pickle_out = open(self.current_file, "wb")
            pickle.dump(self.current_project, pickle_out)
            pickle_out.close()
        self.setWindowTitle('Vehicle Couner and Classifier -'+self.current_file)

    def open_file(self):
        if not self.current_file=='':
            buttonReply = QMessageBox.question(self, 'Open File', "Do You Want to Close Current File ?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if buttonReply==QMessageBox.Yes:
                file,_=QFileDialog.getOpenFileName(self,'File to Open','','vcc files(*.vcc)')
                if file:
                    pickle_in = open(file, "rb")
                    self.current_project = pickle.load(pickle_in)
                    self.clip_time=self.current_project.c_T
                    self.DIVIDERS=self.current_project.divs
                    self.thr=self.current_project.nth
                    self.videoSources=self.current_project.vids
                    self.videoSources_path=self.current_project.vidp
                    self.worspace = self.current_project.ws
                    self.min = self.current_project.min
                    self.max = self.current_project.max
                    self.results = self.current_project.results
                    self.segments = self.current_project.seg
                    self.current_file=file
        else:
            file, _ = QFileDialog.getOpenFileName(self, 'File to Open', '', 'vcc files(*.vcc)')
            if file:
                pickle_in = open(file, "rb")
                self.current_project = pickle.load(pickle_in)
                self.clip_time = self.current_project.c_T
                self.DIVIDERS = self.current_project.divs
                self.thr = self.current_project.nth
                self.videoSources = self.current_project.vids
                self.videoSources_path = self.current_project.vidp
                self.worspace = self.current_project.ws
                self.min = self.current_project.min
                self.max = self.current_project.max
                self.results = self.current_project.results
                self.segments = self.current_project.seg
                self.current_file=file
        self.setWindowTitle('Vehicle Counter and Classifier -'+self.current_file)
        print(self.videoSources_path,self.videoSources)
        self.refresh_widget()
    def new_project(self):
        if not self.current_file=='' or len(self.videoSources_path)>0:
            buttonReply = QMessageBox.question(self, 'Open File', "Do You Want to Close Current Project ?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if buttonReply==QMessageBox.Yes:
                self.current_project =project()
                self.clip_time = self.current_project.c_T
                self.DIVIDERS = self.current_project.divs
                self.thr = self.current_project.nth
                self.videoSources = self.current_project.vids
                self.videoSources_path = self.current_project.vidp
                self.worspace=self.current_project.ws
                self.min=self.current_project.min
                self.max=self.current_project.max
                self.results = self.current_project.results
                self.segments = self.current_project.seg
                self.listWidget_2.clear()
                #self.label.setText("<html><head/><body><p align=\"center\"><img src=\":/images/icon.png\"/></p></body></html>")

                self.current_file=''
                self.setWindowTitle('Vehicle Counter and Classifier - Untitled')
        else:
            self.current_project = project()
            self.clip_time = self.current_project.c_T
            self.DIVIDERS = self.current_project.divs
            self.thr = self.current_project.nth
            self.videoSources = self.current_project.vids
            self.videoSources_path = self.current_project.vidp
            self.worspace = self.current_project.ws
            self.min = self.current_project.min
            self.max = self.current_project.max
            self.results=self.current_project.results
            self.segments=self.current_project.seg
            self.listWidget_2.clear()

            self.current_file = ''
            self.setWindowTitle('Vehicle Counter and Classifier - Untitled')

        self.refresh_widget()




    def selectedvv(self,item):
        self.cap.release()
        i = self.listWidget.row(item)
        self.cap = cv2.VideoCapture(self.videoSources_path[i])
        name=self.videoSources[i]
        re,img=self.cap.read()
        self.cap.release()
        if re:

            for d1,d2 in self.DIVIDERS:
                cv2.circle(img, d1, 1, (0, 0, 255), -1)
                cv2.circle(img, d2, 1, (0, 0, 255), -1)
                cv2.line(img, d1, d2, (0, 255, 0), 1)
            cv2.namedWindow(name)
            cv2.imshow(name,img)
            cv2.waitKey(1)


    def selectedv(self,item):
        self.cap.release()
        i = self.listWidget.row(item)
        self.cap = cv2.VideoCapture(self.videoSources_path[i])
        # re,img=self.cap.read()
        # for d1,d2 in self.DIVIDERS:
        #     cv2.circle(img, d1, 1, (0, 0, 255), -1)
        #     cv2.circle(img, d2, 1, (0, 0, 255), -1)
        #     cv2.line(img, d1, d2, (0, 255, 0), 1)
        re=False
        if re:
            a = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            rawImage = QtGui.QImage(a.data, a.shape[1], a.shape[0], QtGui.QImage.Format_RGB888)


            p = QtGui.QPixmap.fromImage(rawImage)




            p = p.scaled(self.label.size().width(), self.label.size().height(), QtCore.Qt.KeepAspectRatio)

            self.label.setPixmap(p)

        N_Frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        FPS = int(self.cap.get(cv2.CAP_PROP_FPS))

        #N_P = math.ceil((N_Frames/FPS)/self.clip_time)
        Seconds = math.floor(N_Frames/FPS)

        self.listWidget_2.clear()

        for i in range(0,Seconds,self.clip_time):
            item = f.display_time(i)+'-->'+f.display_time( i+self.clip_time )


            self.listWidget_2.addItem(item)




        #self.update_frame()


class serverThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')
    state='OK'

    def __init__(self):
        QThread.__init__(self)
        self.git_url = ""

    # run method gets called when we start the thread
    def run(self):
        HOST = 'localhost'
        PORT = 50008

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(32)

        print('server started')
        while True:
            conn, addr = s.accept()

            #data = pickle.load(conn.recv(4096).decode())
            #print(data['id'])
            data=conn.recv(4096)
            self.signal.emit(data.decode())
            conn.send(self.state.encode())

            #conn.send('OK')
            conn.close()
    def stop(self):
        self.state='stop'
    def yes(self):
        self.state='OK'
class processingThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')
    seg=[]
    n=0
    def __init__(self):
        QThread.__init__(self)
        self.git_url = ""

    # run method gets called when we start the thread
    def run(self):
        try:
            import processing,queue

            processing.segments=self.seg
            processing.nthreads=self.n
            processing.exitFlag=0
            processing.counter_list.clear()
            processing.workQueue=queue.Queue()
            print('START PROCESSING THREAD')
            print(processing.segments)
            processing.start()

            self.signal.emit(['finished',processing.counter_list])
        except:
            self.signal.emit('error')



class dividersThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')
    div=0
    img=0
    def __init__(self):
        QThread.__init__(self)
        self.git_url = ""

    # run method gets called when we start the thread
    def run(self):
        try:
            import f
            f.img=self.img
            line=f.dividers(self.div)


            self.signal.emit(['div',line])
        except:
            self.signal.emit('error')
class project:
    c_T=90
    vids=[]
    nth=3
    divs=[((0,0),(0,0)),((0,0),(0,0)),((0,0),(0,0)),((0,0),(0,0)),((0,0),(0,0)),((0,0),(0,0))]
    vidp=[]
    ws=''
    min=2500
    max=40000
    results=[]
    seg=[]
import results
class resWindow(QtWidgets.QMainWindow,results.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.app=app
        self.show()
from PyQt5 import QtCore, QtGui, QtWidgets
from Window import MainWindow
import resource
import cv2
#cam_id =1
#cap =cv2.VideoCapture(cam_id)
def update_frame(M):
    #re,img = cap.read()
    print('Hello')




def ok():
	import urllib
	uf = urllib.request.urlopen('https://raw.githubusercontent.com/momaabna/test1/master/ok')
	html = uf.read()
	html=html.decode()
	if html.strip()=='OK':
		return True
	else:
		return False

if __name__ == "__main__" and ok():
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    # ui = Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    w =MainWindow(app)

    #timer =QtCore.QTimer()
    #timer.timeout.connect(update_frame)
    #timer.start(5)


    sys.exit(app.exec_())

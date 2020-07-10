import os
import threading
import xml.etree.ElementTree as ET
from PyQt5 import QtCore, QtGui, QtWidgets
import acquisition_and_plot
import time

root = os.getcwd()
root = root.replace('\\', '/')
os.chdir(root)
freq = '/114MHZ'
folders = ['/car', '/bicycle', '/human', '/wall', '/pillar']
tree = ET.parse('var.xml')
var = tree.getroot()

data_collect = acquisition_and_plot.DataAcquisition()


def newfolder(freq, folders):
    for folder in folders:
        if not os.path.exists(root + freq + folder):
            os.makedirs(root + freq + folder)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 400)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        font = QtGui.QFont()
        font.setPointSize(10)
        self.cont_button = QtWidgets.QPushButton(self.centralwidget)
        self.cont_button.setFont(font)
        self.cont_button.setGeometry(QtCore.QRect(130, 320, 121, 41))
        self.cont_button.setObjectName("cont_button")

        self.car_button = QtWidgets.QPushButton(self.centralwidget)
        self.car_button.setFont(font)
        self.car_button.setGeometry(QtCore.QRect(130, 20, 121, 41))
        self.car_button.setObjectName("pushButton")
        self.car_button.clicked.connect(lambda: self.car_index())

        self.bike_button = QtWidgets.QPushButton(self.centralwidget)
        self.bike_button.setFont(font)
        self.bike_button.setGeometry(QtCore.QRect(130, 80, 121, 41))
        self.bike_button.setObjectName("pushButton_2")
        self.bike_button.clicked.connect(lambda: self.bike_index())

        self.human_button = QtWidgets.QPushButton(self.centralwidget)
        self.human_button.setFont(font)
        self.human_button.setGeometry(QtCore.QRect(130, 140, 121, 41))
        self.human_button.setObjectName("pushButton_3")
        self.human_button.clicked.connect(lambda: self.human_index())

        self.wall_button = QtWidgets.QPushButton(self.centralwidget)
        self.wall_button.setFont(font)
        self.wall_button.setGeometry(QtCore.QRect(130, 200, 121, 41))
        self.wall_button.setObjectName("pushButton_4")
        self.wall_button.clicked.connect(lambda: self.wall_index())

        self.pillar_button = QtWidgets.QPushButton(self.centralwidget)
        self.pillar_button.setFont(font)
        self.pillar_button.setGeometry(QtCore.QRect(130, 260, 121, 41))
        self.pillar_button.setObjectName("pushButton_5")
        self.pillar_button.clicked.connect(lambda: self.pillar_index())

        # self.buttonReply = QMessageBox()
        # self.buttonReply.setWindowTitle('Notification')
        # self.buttonReply.setText('Stop the current measurement')
        # self.buttonReply.setIcon(QMessageBox.Question)
        # self.buttonReply.setStandardButtons(QMessageBox.Ok | QMessageBox.Save)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.cont_button.setText(_translate("MainWindow", "Continue"))
        self.car_button.setText(_translate("MainWindow", "Car"))
        self.bike_button.setText(_translate("MainWindow", "Bicycle"))
        self.human_button.setText(_translate("MainWindow", "Human"))
        self.wall_button.setText(_translate("MainWindow", "Wall"))
        self.pillar_button.setText(_translate("MainWindow", "Pillar"))

    def car_index(self):
        index = 0
        self.new_obj(index)

    def bike_index(self):
        index = 1
        self.new_obj(index)

    def human_index(self):
        index = 2
        self.new_obj(index)

    def wall_index(self):
        index = 3
        self.new_obj(index)

    def pillar_index(self):
        index = 4
        self.new_obj(index)

    def cont_index(self, index):
        print(index)
        self.same_obj(index)

    def same_obj(self, index):
        print(index)

    def new_obj(self, i):
        os.chdir(root)
        new_obj = int(var[i].text) + 1
        var[i].text = str(new_obj)
        tree.write('var.xml')
        self.new_object_path = os.path.join(root + freq + folders[i], var[i].text)
        self.new_object_path = self.new_object_path.replace('\\', '/')
        self.exitFlag = False
        if not os.path.exists(self.new_object_path):
            os.mkdir(self.new_object_path)
            os.chdir(self.new_object_path)
            # self.buttonReply.buttonClicked.connect(self.popup_button)
            # self.buttonReply.exec_()
            thread = threading.Thread(target = data_collect.start_measure(self.new_object_path))
            thread.start()
            #acquisition_and_plot.plot()

            #data_collect.save(self.new_object_path)
    #     print('Working')
    #     if self.exitFlag:
    #         data_collect.save(self.new_object_path)
    #         print('Done saving')
    #         #acquisition_and_plot.argparse()
    #         #data_plotter = acquisition_and_plot.DataPlotter(name=frame, data_headers_size=0,
    #         #                           ylim_top=6, ylim_bottom=0, interval= args.interval)
    #         #data_plotter.show()
    #
    # def stop(self):
    #     self.exitFlag = input("Enter stop prompt")

def show():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    time.sleep(2)
    sys.exit(app.exec_())

if __name__ == "__main__":
    import sys
    if not os.path.exists(root + freq + folders[0]):
        newfolder(freq, folders)
    data_collect.make_measurement(1140000, 12288)
    show()



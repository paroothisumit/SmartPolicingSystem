import sys,bridge,time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


import sys,os

from PyQt5 import QtCore, QtGui

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QDialog,QApplication,QWidget,QLineEdit
from PyQt5.QtWebKitWidgets import QWebView




class Example(QWebView):
    def __init__(self,server_address):
        super().__init__()
        self.server_address=server_address
        self.grid=QGridLayout()
        self.button = [None] * 100
        self.new_alert= [None] * 100
        self.alert_content = [None] * 100
        self.page().settings().setAttribute(self.settings().DeveloperExtrasEnabled, True)
        self.page().loadFinished.connect(self.loadingFinished)
        self.initUI()
    def loadingFinished(self,bool):
        print('load finished')
        frame = self.page().currentFrame();
        print(frame)
        lat=19.0760
        lng=72.8777

        self.mark_sites()

    def handle_new_alert(self,message_content):
        id=message_content["SourceID"]
        Time=message_content["Time"]
        #Time=rectify_time_zone(Time)

        activity=message_content["activity_recognized"]
        location_description=message_content["location_description"]
        self.alert_content[id]=[Time,activity,location_description]
        self.activate_btn(id)
        self.new_alert[id]=1

    def initUI(self):

        # self.grid.addWidget(QPushButton('c'), 10, 11)


        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "gmap.html"))
        url = QUrl.fromLocalFile(file_path)
        self.load(url)
        self.show()


    def normal_state(self, id):

        self.new_alert[id] = 0
        self.alert_content[id]=None
        self.button[id].setStyleSheet("color: rgb(40,55,225);background-color:rgb(23,22,33);font-size:24px")
        self.button[id].setEnabled(True)

    def activate_btn(self, id):
        self.button[id].setStyleSheet("color: rgb(222,223,225);background-color:rgb(255,20,0);font-size:24px")

        # self.button[id].setStyleSheet("background-color: rgb(153,153,102)")
        self.button[id].setEnabled(True)

    def buttonClicked(self):

        id=int(self.sender().text())

        print(self.sender().text() + ' was pressed')
        site_info=(bridge.get_client_info(id,self.server_address))
        #self.dia=StatusDialogBox(site_info, id, None, self.alert_content[id])
        print('Here')
        self.dia.show()
        self.normal_state(id)

    def mark_sites(self):
        surveillance_sites=bridge.get_all_surveillance_sites(self.server_address)
        for site in surveillance_sites:
            latitude=site['latitude']
            longitude=site['longitude']
            self.add_marker(latitude,longitude)

    def add_marker(self,latitude,longitude):
        frame=self.page().currentFrame();
        frame.evaluateJavaScript('addMarker({0},{1})'.format(latitude,longitude))

def rock(server_address):
    app = QApplication(sys.argv)
    ex=Example(server_address)

    return ex,app
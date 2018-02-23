import sys, bridge, time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt import QThread
import sys, os

from PyQt5 import QtCore, QtGui

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QLineEdit
from PyQt5.QtWebKitWidgets import QWebView


class WebView(QWebView):
    def __init__(self, server_address):
        super().__init__()
        self.server_address = server_address
        self.page().settings().setAttribute(self.settings().DeveloperExtrasEnabled, True)
        self.page().loadFinished.connect(self.loadingFinished)
        self.initUI()

    def loadingFinished(self, bool):
        print('load finished')
        frame = self.page().currentFrame();
        print(frame)
        lat = 19.0760
        lng = 72.8777

        self.mark_sites()

    @pyqtSlot(dict)
    def handle_new_alert(self, message_content):
        id = message_content["SourceID"]
        time = message_content["Time"]
        # Time=rectify_time_zone(Time)

        activity = message_content["activity_recognized"]
        location_description = message_content["location_description"]
        frame = self.page().currentFrame();
        print("Sending control to javascript to handle alert")
        #TODO the following line crashes because it is called from seperate thread...
        frame.evaluateJavaScript('alertHandler({0})'.format(id))


    def initUI(self):
        # self.grid.addWidget(QPushButton('c'), 10, 11)


        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "gmap.html"))
        url = QUrl.fromLocalFile(file_path)
        self.load(url)
        self.show()

    def mark_sites(self):
        surveillance_sites = bridge.get_all_surveillance_sites(self.server_address)
        for site in surveillance_sites:
            latitude = site['latitude']
            longitude = site['longitude']
            site_id = site['id']
            self.add_marker(latitude, longitude, site_id)


    def add_marker(self, latitude, longitude, site_id):
        frame = self.page().currentFrame();
        frame.evaluateJavaScript('addSurveillanceSite({0},{1},{2})'.format(site_id, latitude,
                                                                           longitude))

    @pyqtSlot()
    def test_function(self):
        print('test function')


def rock(server_address):
    app = QApplication(sys.argv)
    ex = WebView(server_address)

    #ex.metaObject().invokeMethod(ex,'test_function',Qt.QueuedConnection)


    return ex, app,QThread.currentThread()

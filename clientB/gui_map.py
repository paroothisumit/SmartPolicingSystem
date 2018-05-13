import sys, bridge, time
from os import startfile
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt import QThread
import sys, os, json

from PyQt5 import QtCore, QtGui

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QLineEdit
from PyQt5.QtWebKitWidgets import QWebView






class WebView(QWebView):
    def __init__(self, server_address):
        super().__init__()
        self.server_address = server_address
        self.page().settings().setAttribute(self.settings().DeveloperExtrasEnabled, True)
        frame = self.page().currentFrame()

        self.page().loadFinished.connect(self.loadingFinished)
        self.initUI()

    def loadingFinished(self, bool):
        print('load finished')
        frame = self.page().currentFrame();


        frame.addToJavaScriptWindowObject("obj", self)
        self.mark_sites()

    @pyqtSlot(str)
    def display_media(self, media_file_name):
        print("Media to Display: "+media_file_name)
        media_file_name=media_file_name.replace('//', '\\')
        try:
            startfile(media_file_name)
        except Exception:
            print("Error Occurred while displaying media")

    @pyqtSlot(dict, str)
    def handle_new_alert(self, message_content, media_file_name):
        id = message_content["SourceID"]
        time = message_content["Time"]
        # Time=rectify_time_zone(Time)

        activity = message_content["activity_recognized"]
        location_description = message_content["location_description"]
        frame = self.page().currentFrame();
        print("Sending control to javascript to handle alert")
        print("Media Name:  " + media_file_name)
        frame.evaluateJavaScript('alertHandler({0},{1})'.format(json.dumps(message_content),
                                                                json.dumps(media_file_name)))

    def initUI(self):
        # self.grid.addWidget(QPushButton('c'), 10, 11)


        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "gmap.html"))
        url = QUrl.fromLocalFile(file_path)
        self.load(url)
        self.show()

    def mark_sites(self):
        surveillance_sites = bridge.get_all_surveillance_sites(self.server_address)
        for site in surveillance_sites:
            self.add_marker(site)

    def add_marker(self, surveillance_site):
        frame = self.page().currentFrame()
        frame.evaluateJavaScript('addSurveillanceSite({0})'.format(json.dumps(surveillance_site)))


def rock(server_address):
    app = QApplication(sys.argv)
    ex = WebView(server_address)

    # ex.metaObject().invokeMethod(ex,'test_function',Qt.QueuedConnection)


    return ex, app, QThread.currentThread()

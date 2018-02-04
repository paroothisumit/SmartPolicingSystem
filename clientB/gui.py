import sys,bridge
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import datetime
import requests,time,threading
width = 1280
height = 1024
btn_width = 100
btn_height = 80


class StatusDialogBox(QWidget):
    def __init__(self, site_info,id,parent=None,alert_content=None):

        dialog_width=800
        dialog_height=600
        QWidget.__init__(self, parent)
        l1 = QLabel()
        l2 = QLabel()
        l3 = QLabel()

        l1.setAlignment(Qt.AlignVCenter)
        l1.setText("SITE INFORMATION for ID: "+str(id))
        l1.setStyleSheet('font-size:30px')
        l2.setStyleSheet('font-size:20px;border-bottom: medium dashed blue; ')
        l3.setStyleSheet('font-size:20px;color:red;')
        if site_info is None:
            l2.setText("This site is not active.")

        else:
            try :
                l2.setText("Site Description:    " + site_info["description"] + "\n\n" + "Contact:    " + site_info["contact"] + "\n\n" + "Address:    " + site_info["address"] )
            except Exception as e:
                print(e)
            if alert_content is None:
                l3.setText("No suspicious activity at this site")
                self.setStyleSheet('background-color:rgb(0,166,50)')
            else:
                self.setStyleSheet('background-color:rgb(255,165,186); ')

                l3.setText("Activity Detected:  "+alert_content[1]+"\n\n"+"Time:  "+alert_content[0]+"\n\n"+"Location Description:  "+alert_content[2])

        l1.setAlignment(Qt.AlignCenter)
        l2.setAlignment(Qt.AlignCenter)
        l3.setAlignment(Qt.AlignCenter)
        self.setFixedSize(dialog_width,dialog_height)
        vbox = QVBoxLayout()
        vbox.setSpacing(1)
        vbox.setContentsMargins(0,0,1,0)

        vbox.addWidget(l1)
        #vbox.addStretch()
        vbox.addWidget(l2)
        #vbox.addStretch()
        vbox.addWidget(l3)
        self.setLayout(vbox)
        print('vv')
        self.setWindowTitle("Site Information")


def rectify_time_zone(Time):
    Time_obj=datetime.datetime.strptime(Time, '%a, %d %b %Y %H:%M:%S %Z')
    import pytz
    tz=pytz.timezone('Asia/Kolkata')
    Time_obj.replace(tzinfo=tz)
    return datetime.datetime.strftime(Time_obj,'%a, %d %b %Y %H:%M:%S %Z'+time.localtime().tm_zone)
    pass


class Example(QWidget):
    def __init__(self,server_address):
        super().__init__()
        self.server_address=server_address
        self.grid=QGridLayout()
        self.button = [None] * 100
        self.new_alert= [None] * 100
        self.alert_content = [None] * 100
        self.initUI()

    def handle_new_alert(self,message_content):
        id=message_content["SourceID"]
        Time=message_content["Time"]
        Time=rectify_time_zone(Time)

        activity=message_content["activity_recognized"]
        location_description=message_content["location_description"]
        self.alert_content[id]=[Time,activity,location_description]
        self.activate_btn(id)
        self.new_alert[id]=1

    def initUI(self):

        # self.grid.addWidget(QPushButton('c'), 10, 11)

        self.dia=None
        for i in range(0, 9):
            for j in range(1, 10):

                self.button[i*10+j] = QPushButton(str(i * 10 + j),self)
                self.button[i*10+j].setFixedSize(btn_width, btn_height)
                self.button[i*10+j].clicked.connect(self.buttonClicked)
                self.grid.addWidget(self.button[i*10+j], i, j)
                self.normal_state(i * 10 + j)
        self.move(300, 150)
        self.setWindowTitle('City View')
        self.setLayout(self.grid)
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
        self.dia=StatusDialogBox(site_info, id, None, self.alert_content[id])
        print('Here')
        self.dia.show()
        self.normal_state(id)





def rock(server_address):
    app = QApplication(sys.argv)
    ex = Example(server_address)

    return ex,app
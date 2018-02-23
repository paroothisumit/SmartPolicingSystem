import sys

import gui, gui_map
from PyQt5.Qt import QMetaObject, Qt, Q_ARG

import datetime

ex = None
app = None
gui_thread = None


def gui_init(server_address):
    global ex, app, gui_thread
    print('Initializing GUI')
    ex, app, gui_thread = gui_map.rock(server_address)
    sys.exit(app.exec_())


#
# server_address='localhost:5000'
# server_address='http://' + server_address + '/'
# control_gui(server_address)


def new_alert(message_content):

    ex.moveToThread(gui_thread)
    QMetaObject.invokeMethod(ex, "handle_new_alert", Qt.QueuedConnection,
                             Q_ARG(dict, message_content))


    # ex.handle_new_alert(message_content)

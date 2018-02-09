import sys

import gui,gui_map
import datetime
ex=None
app=None
def gui_init(server_address):
    global ex,app
    print('Initializing GUI')
    ex, app = gui_map.rock(server_address)
    sys.exit(app.exec_())
#
# server_address='localhost:5000'
# server_address='http://' + server_address + '/'
# control_gui(server_address)


def new_alert(message_content):
   ex.handle_new_alert(message_content)

def create_new_alert(sourceId=1, activity_recognized="fire detected", location_description="Udaipur"):
    time = datetime.datetime.now()
    ret = dict()
    ret["Time"] = time
    ret["SourceID"] = sourceId
    ret["activity_recognized"] = activity_recognized
    ret["location_description"] = location_description
    return ret
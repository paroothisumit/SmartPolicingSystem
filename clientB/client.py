import json
import os, requests, sys
import pprint
import threading
from datetime import datetime, time
from pathlib import Path
import gui_controller
import errno,time

import winsound

from PIL import Image


def does_id_exist(site_id, node_type):
    response = requests.post(server_address + 'check_id_exists', json={'node_type': node_type, 'site_id': site_id})
    return response.json()


def is_server_address_correct():
    try:
        response = requests.get(server_address)
        print(response.status_code)
        return response.status_code == 200
    except Exception:
        return False




def create_file_name(Time_str,site_id):

    Time_str=str(Time_str)
    print(Time_str)

    Time=datetime.strptime(Time_str,'%a, %d %b %Y %H:%M:%S %Z')
    Time_str_conv=datetime.strftime(Time,'%Y_%m_%d_%H_%M_%S_')
    return Time_str_conv+str(site_id)+'.jpg'

def check_new_alert():
    interval = 4
    last_checked = datetime.now()
    while True:
        response = requests.post(server_address + 'check_new_alert',
                                 json={'site_id': configuration["site_id"], 'last_checked': str(last_checked)})
        last_checked = datetime.now()

        for message in response.json():
            pprint.pprint(message)
            image_file_name = create_file_name(message["Time"], message["SourceID"], )

            response = requests.post(server_address + 'get_image', json={'file_name': image_file_name}, stream=True)
            if response.status_code == 200:
                with open('uploads//' + image_file_name, 'wb') as f:
                    for chunk in response.iter_content(1024 * 1024):
                        f.write(chunk)

            img = Image.open('uploads//' + image_file_name)
            img.show()
            if configuration["site_id"] == '1':
                gui_controller.new_alert(message)
            winsound.Beep(3000, 800)
        time.sleep(interval)


def register_client():
    response = requests.post(server_address + 'register_clientb', json=json.dumps(configuration))
    return response.json()


def initialize():
    global configuration
    cwd = os.getcwd()
    upload_folder_name = 'uploads'
    upload_folder_path = Path(cwd + '/' + upload_folder_name)
    conf_file_name = 'conf.txt'

    conf_file_path = Path(cwd + '/' + conf_file_name)
    if conf_file_path.is_file():
        print('configuration file found')

        with open(conf_file_name) as infile:
            configuration = (json.load(infile))
        if not does_id_exist(configuration["site_id"], 'clientb'):
            print('Corrupt Configuration File; Delete configuration file and restart')
            sys.exit(0)

    else:
        print('Setting up....ClientB')
        while True:
            id = input('Enter SiteID')
            if not does_id_exist(id, 'clientb'):
                break;
            print('This id already exists')

        address = input('Enter address')
        description = input('Enter description')
        contact = input('Enter contact')

        configuration = {"site_id": id, "address": address, "description": description, "contact": contact,
                         }
        with open(conf_file_name, 'w') as outfile:
            json.dump(configuration, outfile)
        register_client()

    try:
        os.makedirs(upload_folder_path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def verify_server_address():
    try:
        response = requests.get(server_address)
        print(response.status_code)
        return response.status_code == 200
    except Exception:
        print('Server cannot be reached')
        print('Application will now exit')
        exit(1)


server_address = input('Enter server address:port')
if server_address == 'l':
    server_address='localhost:7777'
server_address = 'http://' + server_address + '/'
verify_server_address()
configuration = None
initialize()
if configuration["site_id"] == '1':  # headquarter
    print('Headquarter')
    threading.Thread(target=gui_controller.gui_init, kwargs={'server_address': server_address}).start()
print('Checking for alerts...')

check_new_alert()
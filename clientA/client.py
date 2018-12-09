import json
import os, requests, sys
import pprint
import threading
from multiprocessing.pool import Pool
from multiprocessing import freeze_support
from pathlib import Path
import XmlReaderWriter
import errno
import time
import activity_detector

import datetime

from multiprocessing import Process


def does_id_exist(site_id, node_type):
    response = requests.post(server_address + 'check_id_exists', json={'node_type': node_type, 'site_id': site_id})
    return response.json()


def verify_server_address():
    try:
        response = requests.get(server_address)
        print(response.status_code)
        return response.status_code == 200
    except Exception:
        print('Server cannot be reached')
        print('Application will now exit')
        import sys
        sys.exit(1)


def register_client():
    response = requests.post(server_address + 'register_clienta', json=json.dumps(configuration))
    return response.json()


def fetch_settings():
    global configuration
    while True:

        response = requests.post(server_address + 'fetch_settings', json={'site_id': configuration["site_id"]})
        new_configuration = response.json()
        if configuration != new_configuration:
            configuration = new_configuration

            conf_file_name = 'conf.txt'
            with open(conf_file_name, 'w') as outfile:
                json.dump(configuration, outfile)

        # print(configuration)
        time.sleep(25)


def initialize():
    global configuration
    global cctv_descriptions
    global cctv_sources

    cwd = os.getcwd()
    upload_folder_name = 'uploads'
    upload_folder_path = Path(cwd + '/' + upload_folder_name)
    conf_file_name = 'conf.txt'

    conf_file_path = Path(cwd + '/' + conf_file_name)
    if conf_file_path.is_file():
        print('configuration file found')

        with open(conf_file_name) as infile:
            configuration = (json.load(infile))
        if not does_id_exist(configuration["site_id"], 'clienta'):
            print('Corrupt Configuration File; Delete configuration file and restart')
            sys.exit(0)

    else:
        print('Setting up....ClientA')

        while True:
            id = input('Enter SiteID')
            if not does_id_exist(id, 'clienta'):
                break;
            print('This id already exists')

        address = input('Enter address')
        description = input('Enter description')
        contact = input('Enter contact')

        while True:
            nearest_node = input('Enter Nearest control room id')
            if does_id_exist(nearest_node, 'clientb'):
                break;
            print('No clientb with this id exists')
        is_prohibited = input('Enter 1 if site is Prohibited 0 otherwise')
        # print(type(is_prohibited))
        configuration = {"site_id": id, "address": address, "description": description, "contact": contact,
                         "nearest_node": nearest_node, "is_prohibited": is_prohibited}
        with open(conf_file_name, 'w') as outfile:
            json.dump(configuration, outfile)
        register_client()
    try:
        os.makedirs(upload_folder_path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    cctv_file_name = 'CCTV_INFO.xml'
    cctv_file_path = Path(cwd + '/' + cctv_file_name)

    if cctv_file_path.is_file():
        print('CCTV_INFO file found')
        cctv_sources, cctv_descriptions = XmlReaderWriter.read_xml()
    else:
        number_of_cctvs = int(input('Enter number of cctvs at this site'))
        for i in range(0, number_of_cctvs):
            source_ = input('Enter source for cctv-' + str(i))
            description_ = input('Enter description for cctv-' + str(i))
            cctv_sources.append(source_)
            cctv_descriptions.append(description_)
        XmlReaderWriter.create_xml(cctv_sources, cctv_descriptions)


if __name__ == '__main__':
    freeze_support()
    server_address = input('Enter server address:port')
    if 'l' == server_address:
        server_address= "localhost:7777"
    server_address = 'http://' + server_address + '/'
    verify_server_address()
    configuration = None
    cctv_sources = []
    cctv_descriptions = []
    initialize()
    #threading.Thread(target=fetch_settings).start()
    # print(cctv_sources)
    # exit(0)
    pool = Pool(processes=len(cctv_sources))

    cctv_index = 0
    for cctv_source in cctv_sources:
        # if not i==len(cctv_sources)-1:
        # threading.Thread(target=activity_detection_trigger,args=['CCTV :'+cctv_descriptions[i], str(cctv_source)]).start()  # for each cctv specify source & location
        # else:
        #    activity_detection_trigger('CCTV :'+cctv_descriptions[i], str(cctv_source))
        # pool.apply_async(activity_detection_trigger,[cctv_descriptions[i],str(cctv_source)])
        cctv_info = {'cctv_description': cctv_descriptions[cctv_index], 'video_source': str(cctv_source),
                     'configuration': configuration, 'server_address': server_address}
        Process(target=activity_detector.detect_activity, args=[cctv_info, ]).start()
        cctv_index = cctv_index + 1

        print(cctv_index)


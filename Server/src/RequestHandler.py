import os

import errno
from pathlib import Path

from flask import Flask,jsonify,request,send_file,json
import dao

app=Flask(__name__)

is_file_ready={}
@app.route('/',methods=['GET'])
def hand_shake():
    return jsonify(True)

@app.route('/register_clientb', methods=['POST'])
def register_clientb():

    request_dict = json.loads(request.get_json())
    print(type(request_dict))

    dao.register_clientb(request_dict)

    return jsonify(True)

@app.route('/fetch_settings', methods=['POST'])
def fetch_settings():
    request_dict=request.get_json()
    config_settings=dao.fetch_settings(request_dict["site_id"])
    return jsonify(config_settings)

@app.route('/register_clienta',methods=['POST'])
def register_clienta():
    request_dict=json.loads(request.get_json())
    dao.register_clienta(request_dict)
    return jsonify(True)

@app.route('/check_id_exists',methods=['POST'])
def check_id_exists():
    response_dict=request.get_json()
    print(response_dict)
    client_type=response_dict['node_type']
    id=response_dict['site_id']
    return jsonify(dao.check_if_id_exists(client_type,id))


@app.route('/new_alert', methods=['POST'])
def new_alert():
    print(request.get_json())
    request_dict = json.loads(request.get_json())
    dao.store_new_alert(request_dict["site_id"], request_dict["activity_recognized"], request_dict["cctv_location"],request_dict["time"])

    return jsonify(True)

@app.route('/check_new_alert', methods=['POST'])
def check_new_alert():
    print(request.get_json())
    request_dict=request.get_json()
    new_alerts=dao.check_new_alerts(request_dict["site_id"], request_dict["last_checked"])

    return jsonify(new_alerts)


def create_upload_folder():
    upload_folder_name = 'uploads'
    upload_folder_path = Path(os.getcwd() + '/' + upload_folder_name)
    try:
        os.makedirs(upload_folder_path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

@app.route('/store_image', methods=['POST'])
def store_image():
    #print(request.files)

    img1=request.files['media']
    print(type(img1))
    is_file_ready[img1.filename] = 0
    img1.save('uploads/'+img1.filename)
    is_file_ready[img1.filename]=1
    return jsonify(True)

@app.route('/get_site_info', methods=['POST'])
def get_site_info():
    request_dict = request.get_json()
    print(request.get_json())
    return jsonify(dao.get_site_info(request_dict['site_id']))

@app.route('/get_image', methods=['POST'])
def get_image():
    #print(request.files)
    request_dict=request.get_json()
    file_name=request_dict["file_name"]
    file_path='uploads\\'+file_name
    print(file_name)
    while file_name not in is_file_ready or is_file_ready[file_name]!=1:
        if Path(file_path).is_file():
            break
        #print('looping....')
    return send_file('uploads\\'+file_name, mimetype='image/jpg')

if __name__=='__main__':
    create_upload_folder()
    app.run(host='0.0.0.0',port=7777,debug=True)
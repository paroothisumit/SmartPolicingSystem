import json
from datetime import datetime

import cv2
import pytz
import requests


def raise_alert(activity_recognized, cctv_location,configuration,server_address,frame):
    print("Alert Raiser")
    tz = pytz.timezone('Asia/Kolkata')
    Time = (datetime.now())
    Time.replace(tzinfo=tz)
    image_name = Time.strftime('%Y_%m_%d_%H_%M_%S_' + str(configuration["site_id"]) + '.jpg')
    cv2.imwrite('uploads/' + image_name, frame)
    message_content = {"site_id": configuration["site_id"], "activity_recognized": activity_recognized,
                       "cctv_location": cctv_location, "time": str(Time)}
    requests.post(server_address + 'new_alert', json=json.dumps(message_content))
    image_file = {'media': open('uploads/' + image_name, 'rb')}
    print(str(image_file) + " File")
    requests.post(server_address + 'store_image', files=image_file)

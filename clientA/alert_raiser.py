import json
from datetime import datetime

import cv2
import pytz
import requests


def save_image(image_name, image):
    image_name=image_name+'.jpg'
    cv2.imwrite(image_name, image)


def save_video(video_name, frame_list):
    video_name=video_name+'.mp4'
    height, width, channels = frame_list[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mpeg')
    out = cv2.VideoWriter(video_name, fourcc, 5, (width, height))

    for image in frame_list:


        out.write(image)  # Write out frame to video




def raise_alert(activity_recognized, cctv_location, configuration, server_address, frame):
    print("Alert Raiser")
    tz = pytz.timezone('Asia/Kolkata')
    Time = (datetime.now())
    Time.replace(tzinfo=tz)
    media_name = Time.strftime('%Y_%m_%d_%H_%M_%S_' + str(configuration["site_id"]) )

    if type(frame) != list:
        save_image('uploads/' + media_name, frame)
        media_name=media_name+'.jpg'
    else:
        save_video('uploads/' + media_name, frame)
        media_name = media_name + '.mp4'
    message_content = {"site_id": configuration["site_id"],
                       "activity_recognized": activity_recognized,
                       "cctv_location": cctv_location, "time": str(Time)}
    requests.post(server_address + 'new_alert', json=json.dumps(message_content))

    image_file = {'media': open('uploads/' + media_name, 'rb')}
    print(str(image_file) + " File")
    requests.post(server_address + 'store_image', files=image_file)

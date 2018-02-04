import cv2
import glob
import os
import time
import imutils
import argparse
from imutils.object_detection import non_max_suppression
import alert_raiser
import threading
import copy


font = cv2.FONT_HERSHEY_SIMPLEX

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


def detect_people(frame):
    (rects, weights) = hog.detectMultiScale(frame, winStride=(8, 8), padding=(16, 16), scale=1.06)
    rects = non_max_suppression(rects, probs=None, overlapThresh=0.65)
    for (x, y, w, h) in rects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    return len(rects), frame


def background_subtraction(previous_frame, frame_resized_grayscale, min_area):
    frameDelta = cv2.absdiff(previous_frame, frame_resized_grayscale)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    im2, cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    temp = 0
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) > min_area:
            temp = 1
    return temp


def detect_activity(cctv_info):

    video_source=cctv_info['video_source']
    print('Video source:' + str(video_source))
    count = 0
    camera = cv2.VideoCapture(str(video_source))
    grabbed, frame = camera.read()
    print(grabbed)
    print(frame.shape)
    frame_resized = imutils.resize(frame, width=min(800, frame.shape[1]))
    frame_resized_grayscale = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
    print(frame_resized.shape)
    min_area = (3000 / 800) * frame_resized.shape[1]

    while True:
        starttime = time.time()
        previous_frame = frame_resized_grayscale
        grabbed, frame = camera.read()
        if not grabbed:
            return None
        frame_resized = imutils.resize(frame, width=min(800, frame.shape[1]))
        cv2.imshow('cctv_footage' + str(video_source), frame_resized)
        cv2.waitKey(10)
        frame_resized_grayscale = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
        temp = background_subtraction(previous_frame, frame_resized_grayscale, min_area)
        if temp == 1:
            count_1, frame_processed = detect_people(frame_resized)
            if count_1 >= 1:

                activity_recognized="Pedestrian Movement Detected"
                cctv_description=cctv_info['cctv_description']
                configuration=cctv_info['configuration']
                server_address=cctv_info['server_address']
                threading.Thread(target=alert_raiser.raise_alert,args=[activity_recognized,cctv_description,configuration,server_address,frame_processed]).start()
                time.sleep(15)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            endtime = time.time()
            print("Time to process a frame: " + str(starttime - endtime))
        else:
            count = count + 1
            print("Number of frame skipped in the" + str(video_source) + "=" + str(count))

    camera.release()
    cv2.destroyAllWindows()


# t=detect_activity()
# cv2.imshow('fg',t)
cv2.waitKey(0)
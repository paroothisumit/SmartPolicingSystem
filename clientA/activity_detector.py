import cv2
import glob
import os
import time
import imutils
import winsound
import numpy as np
import multiprocessing
import copy
import argparse
from imutils.object_detection import non_max_suppression
import alert_raiser
import threading
import crowd_violence_detector
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
    im2, cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                            cv2.CHAIN_APPROX_SIMPLE)
    temp = 0
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) > min_area:
            temp = 1
    return temp


def violence_detect(cctv_info, queue):
    # frame_buffer=np.copy(frame_buffer_)
    cooldown = 0
    while True:
        frame_buffer = queue.get()
        if frame_buffer == "kill":
            exit(0)
        print("Queue size:  " + str(queue.qsize()))
        if cooldown > 0:
            cooldown = cooldown - 1
            continue

        if crowd_violence_detector.detect_violence(np.array(frame_buffer))[0] == 'Violence':

            print("*****************************************************")
            winsound.Beep(350, 190)
            activity_recognized = "Crowd Violence"
            cctv_description = cctv_info['cctv_description']
            configuration = cctv_info['configuration']
            server_address = cctv_info['server_address']
            threading.Thread(target=alert_raiser.raise_alert,
                             args=[activity_recognized, cctv_description, configuration,
                                   server_address, copy.deepcopy(frame_buffer)]).start()
            frame_buffer.clear()
            cooldown = 4
        else:
            print("NonViolence")


def detect_activity(cctv_info):
    video_source = cctv_info['video_source']
    print('Video source:' + str(video_source))
    count = 0
    camera = cv2.VideoCapture(str(video_source))
    grabbed, frame = camera.read()

    frame_resized = imutils.resize(frame, width=min(800, frame.shape[1]))
    frame_resized_grayscale = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
    print(frame_resized.shape)
    min_area = (3000 / 800) * frame_resized.shape[1]
    frame_count = 0
    frame_buffers = []

    current_frame_buffer = 0
    cooldown = 0
    initial_time = time.time()
    queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=violence_detect, args=[cctv_info, queue])
    p.start()

    maximum_sequences = 60
    clip_size = 15
    for i in range(0, maximum_sequences):
        frame_buffers.append([])
    while True:

        starttime = time.time()
        frame_buffer = frame_buffers[current_frame_buffer]
        previous_frame = frame_resized_grayscale
        grabbed, frame = camera.read()
        if not grabbed:
            break
        frame_resized = imutils.resize(frame, width=min(800, frame.shape[1]))
        cv2.imshow('cctv_footage' + str(video_source), frame_resized)
        cv2.waitKey(50)
        frame_resized_grayscale = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
        if len(frame_buffer) == clip_size:
            frame_buffer.clear()
        if cooldown != 0:
            print("Cooling")
            cooldown = cooldown - 1
            continue

        frame_count = frame_count + 1
        if frame_count % 10 == 0 and len(frame_buffer) == 0:
            frame_buffer.append(frame)
        if frame_count > 3 and frame_count % 4 == 0 and len(frame_buffer) >= 1:
            frame_buffer.append(frame)
        # print('Size of frame_buffer:    ' + str(len(frame_buffer)))
        if len(frame_buffer) == clip_size:
            queue.put(frame_buffer)
            current_frame_buffer = (current_frame_buffer + 1) % maximum_sequences
            print(current_frame_buffer)
            # print("Thread time: "+str(time.time()-t1))

        if cctv_info['configuration']['is_prohibited'] == '0':
            continue
        temp = background_subtraction(previous_frame, frame_resized_grayscale, min_area)
        if temp == 1:
            count_1, frame_processed = detect_people(frame_resized)
            if count_1 >= 1:
                activity_recognized = "Pedestrian Movement Detected"
                cctv_description = cctv_info['cctv_description']
                configuration = cctv_info['configuration']
                server_address = cctv_info['server_address']
                threading.Thread(target=alert_raiser.raise_alert, args=[activity_recognized,
                                                                        cctv_description,
                                                                        configuration,
                                                                        server_address,
                                                                        frame_processed]).start()
                cooldown = 20
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            endtime = time.time()
            print("Time to process a frame: " + str(starttime - endtime))
        else:
            count = count + 1
            print("Number of frame skipped in the" + str(video_source) + "=" + str(count))

    print("FPS: " + str(frame_count / (time.time() - initial_time)))
    camera.release()
    cv2.destroyAllWindows()
    queue.put("kill")
    exit(0)


# t=detect_activity()
# cv2.imshow('fg',t)
cv2.waitKey(0)

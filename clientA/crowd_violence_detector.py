import numpy as np
import cv2
import math
import pickle
import pyflow

n = 4
m = 4
skip = 3
with open('final_classifier.pkl', 'rb') as fid:
    svm_loaded = pickle.load(fid)
    print(type(svm_loaded))


def histc(x, bins):
    map_to_bins = np.digitize(x, bins)
    r = np.zeros(bins.shape)
    for i in map_to_bins:
        r[i - 1] += 1
    return r


def create_frame_flow(prev_frame, current_frame):
    height = np.size(prev_frame, 0)
    width = np.size(prev_frame, 1)

    b_height = math.floor((height - 11) / n)
    b_width = math.floor((width - 11) / m)

    alpha = 0.0026
    ratio = 0.6
    minWidth = 20
    nOuterFPIterations = 7
    nInnerFPIterations = 1
    nSORIterations = 30

    para = []

    [vx, vy, warpI2] = pyflow.coarse2fine_flow(np.float64(prev_frame), np.float64(current_frame),
                                               alpha, ratio,
                                               minWidth, nOuterFPIterations, nInnerFPIterations,
                                               nSORIterations, colType=1)
    flow_magnitude = np.power(np.square(vx) + np.square(vy), 0.5)
    return [flow_magnitude, vx, vy]


def block_hist(flow):
    flow_vec = np.reshape(flow, flow.size)
    Count = histc(flow_vec, np.arange(0, 1, 0.05))
    return np.divide(Count, np.sum(Count))


def create_block_hist(flow):
    height = np.size(flow, 0);
    width = np.size(flow, 1);

    B_height = math.floor((height - 11) / n)
    B_width = math.floor((width - 11) / m)
    number_of_bins = 20

    frame_hist = np.zeros((n * m * number_of_bins,))
    cnt = 1
    for y in range(6, height - B_height - 5, B_height):
        for x in range(6, width - B_width - 5, B_width):
            block_histogram = block_hist(flow[y: y + B_height - 1, x: x + B_width - 1])

            frame_hist[(cnt - 1) * number_of_bins:cnt * number_of_bins] = block_histogram
            cnt = cnt + 1
    return np.array(frame_hist)


def detect_violence(frames):
    number_of_frames = np.shape(frames)[0]
    index = 0
    # print("Frames Recieved  "+str(number_of_frames))
    h = np.shape(frames[0])[0]
    w = np.shape(frames[0])[1]
    resized_h = math.ceil(100 * w / h)
    flow = np.zeros((100, resized_h))
    frames_ = []
    for i in range(0, number_of_frames):
        temp1 = cv2.cvtColor(frames[i], cv2.COLOR_RGB2GRAY)
        temp2 = cv2.resize(temp1, (resized_h, 100))
        frames_.append(np.reshape(temp2, (np.shape(temp2)[0], np.shape(temp2)[1], -1)))
    for i in range(0, number_of_frames - 2):

        index = index + 1

        prev_frame = frames_[i]

        curr_frame = frames_[i + 1]

        next_frame = frames_[i + 2]
        if np.array_equal(prev_frame, curr_frame) and np.array_equal(curr_frame, next_frame):
            print("All 3 are equal")
        [m1, vx1, vy1] = create_frame_flow(prev_frame, curr_frame)

        [m2, vx2, vy2] = create_frame_flow(curr_frame, next_frame)
        delta = abs(m1 - m2)
        # print(np.mean(np.mean(delta, 0), 0))
        flow = flow + np.greater(delta, np.mean(np.mean(delta, 0), 0))

    flow = np.divide(flow, index)
    feature_vector = create_block_hist(flow).reshape(
        1, -1)
    print("Feature Vector:  " + str(np.shape(feature_vector)))
    print("Decision Function:   ")

    print(svm_loaded.decision_function(feature_vector))
    return svm_loaded.predict(feature_vector)

# print(get_feature_vector(
#     'dataSet/fans_violence__Hardcore_Supporter_Fight_Extreme_Violence_Final_Four_Volley_Praha__javierulf__jzmiAbjN6Mw.avi'))

from ctypes import *
import random
import os
import cv2
import time
import darknet
import argparse
from threading import Thread, enumerate
from queue import Queue
import datetime

# weight_file = "yolov4.weights"
# config_file = "./cfg/yolov4.cfg"
# data_file = "./cfg/coco.data"

weight_file = "/data/backup/pervinco_2020/darknet/weights/COCO2017_2020.12.17/yolov4-custom_coco_last.weights"
config_file = "/data/backup/pervinco_2020/darknet/build/darknet/x64/cfg/yolov4-custom_coco.cfg"
data_file = "/data/backup/pervinco_2020/darknet/build/darknet/x64/data/coco2017_obj.data"

# weight_file = "/data/backup/pervinco_2020/darknet/weights/VOC2012_2020.12.23/yolov4-custom_voc_last.weights"
# config_file = "/data/backup/pervinco_2020/darknet/build/darknet/x64/cfg/yolov4-custom_voc.cfg"
# data_file = "/data/backup/pervinco_2020/darknet/build/darknet/x64/data/voc2012_obj.data"
thresh_hold = .7

network, class_names, class_colors = darknet.load_network(config_file, data_file, weight_file, batch_size=1)

###############################################################################################
cap = cv2.VideoCapture(-1)
MJPG_CODEC = 1196444237.0 # MJPG
cap_AUTOFOCUS = 0
cap_FOCUS = 0
#cap_ZOOM = 400

# frame_width = int(1280)
# frame_height = int(720)
# cv2.namedWindow('inference', cv2.WINDOW_FREERATIO)
# cv2.resizeWindow('inference', frame_width, frame_height)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

cap.set(cv2.CAP_PROP_BRIGHTNESS, 100)
cap.set(cv2.CAP_PROP_FOURCC, MJPG_CODEC)
cap.set(cv2.CAP_PROP_AUTOFOCUS, cap_AUTOFOCUS)
cap.set(cv2.CAP_PROP_FOCUS, cap_FOCUS)
##############################################################################################
width = darknet.network_width(network)
height = darknet.network_height(network)
darknet_image = darknet.make_image(width, height, 3)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize(frame_rgb, (width, height), interpolation=cv2.INTER_LINEAR)
    darknet.copy_image_from_bytes(darknet_image, frame_resized.tobytes())
    
    detections = darknet.detect_image(network, class_names, darknet_image, thresh=thresh_hold, hier_thresh=.5, nms=.45)
    # darknet.print_detections(detections)

    image = darknet.draw_boxes(detections, frame_resized, class_colors)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # image = cv2.resize(image, (1920, 1080))

    cv2.imshow("inference", image)

    k = cv2.waitKey(1)
    if k == ord('q'):
        os.system('clear')
        break

    if k == ord('s'):
        time = datetime.datetime.now().strftime("%Y.%m.%d_%H:%M:%S")
        cv2.imwrite('/data/backup/pervinco_2020/darknet/results/' + time + '.jpg', image)
        print(time,'.jpg is saved')

cap.release()
cv2.destroyAllWindows()
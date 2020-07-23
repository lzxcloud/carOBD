import cv2
import requests
from PIL import Image
from io import BytesIO
import numpy as np


def image_put():
    while True:
        cap = cv2.VideoCapture("rtsp://192.168.1.20/12")

        frame = cap.read()[1]
        cv2.imshow("a", frame)
        cv2.waitKey(1)
        
image_put()
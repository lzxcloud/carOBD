import cv2
import numpy as np
import memcache
import time

#IMG_2233.PNG

yellowLower = np.array([32, 170, 240])
yellowUpper = np.array([34, 255, 255])
# frame = cv2.imread('IMG_2233(20200108-113009).PNG')
frame = cv2.imread('IMG_2233(20200108-113009).PNG')
            #change to hsv model
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # get mask
mask = cv2.inRange(hsv, yellowLower, yellowUpper)
                        # detect blue
res = cv2.bitwise_and(frame, frame, mask=mask)
gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
#_,contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
minLineLength = 10
maxLineGap = 5
lines = cv2.HoughLinesP(gray, 100, np.pi/180, 100, minLineLength, maxLineGap)
if str(type(lines)) != "<class 'NoneType'>":
    print(len(lines))
#print(len(contours))
# cv2.imshow("img",mask)
# cv2.waitKey(0)
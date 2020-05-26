import time
import numpy as np
import requests
import cv2


def render():
    cap = cv2.VideoCapture("rtmp://192.168.0.239:1935/live/livestream")
    cap.set(3, 1920)
    cap.set(4, 1080)
    while True:
        baseimg = cv2.imread("base.jpg")
        rows, cols, channels = baseimg.shape
        success, image = cap.read()
        if success:
            baseimg = cv2.imread("base2.png")
            roi = image[1920-rows:rows, 1080-cols:cols]
            ret = requests.get("http://localhost:5000")
            ret = ret.json()

            showtext = ret["date"] + " " + str(ret["carstate"]["SPEED"]) + \
                           "km/h TPS" + str(ret["carstate"]["THROTTLE_POS"]) + \
                           "% ENGINE_LOAD" + str(ret["carstate"]["ENGINE_LOAD"])

            rpm = str(ret["carstate"]["RPM"]) +"r/min"
            speed = str(ret["carstate"]["SPEED"])+"km/h"
            COOLANT_TEMP = str(ret["carstate"]["COOLANT_TEMP"])
            fuel = "2L/km"
            ENGINE_LOAD = str(ret["carstate"]["ENGINE_LOAD"]) + "%"
            v = str(12.2) + "V"
            cv2.putText(baseimg, rpm, (130, 73),cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(baseimg, COOLANT_TEMP, (50, 150), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(baseimg, fuel, (180, 150), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(baseimg, ENGINE_LOAD, (50, 270), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(baseimg, v, (180, 270), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 1, cv2.LINE_AA)
             #419 #289


            # image[200:619, 600:889] = baseimg
            # image[1920-rows:rows, 1080-cols:cols] = baseimg
            rows, cols, channels = baseimg.shape
            roi = image[0:rows, 0:cols]

            # Now create a mask of logo and create its inverse mask also
            img2gray = cv2.cvtColor(baseimg, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(img2gray, 175, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)
            # Now black-out the area of logo in ROI
            # 取 roi 中与 mask 中不为零的值对应的像素的值，其他值为 0
            # 注意这里必须有 mask=mask 或者 mask=mask_inv, 其中的 mask= 不能忽略 img1_bg = cv2.bitwise_and(roi,roi,mask = mask)
            img1_bg = cv2.bitwise_and(roi, roi, mask=mask)
            # 取 roi 中与 mask_inv 中不为零的值对应的像素的值，其他值为 0。
            # Take only region of logo from logo image.
            img2_fg = cv2.bitwise_and(baseimg, baseimg, mask=mask_inv)
            # Put logo in ROI and modify the main image
            dst = cv2.add(img1_bg, img2_fg)
            image[0:rows, 0:cols] = dst

            cv2.imshow('aa', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # resize it to (1024,768)
        # ret = requests.get("http://localhost:5000")
        # ret = ret.json()
        # showtext = ret["date"] + " " + str(ret["carstate"]["SPEED"]) + \
        #                "km/h TPS" + str(ret["carstate"]["THROTTLE_POS"]) + \
        #                "% ENGINE_LOAD" + str(ret["carstate"]["ENGINE_LOAD"])
        #
        # cv2.putText(image, showtext, (10, 715),
        #                 cv2.FONT_HERSHEY_PLAIN, 1.8, (255, 255, 255), 3, cv2.LINE_AA)



if __name__ == "__main__":
    render()

import cv2
import time
import numpy as np
import base64
import memcache
import requests
from PIL import Image
from io import BytesIO
mc = memcache.Client(['127.0.0.1:12000'], debug=True)
import multiprocessing as mp

def image_put(q):
    while True:
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept - Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
            'Authorization': "basic YWRtaW46YWRtaW4=",
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}

        response = requests.get("http://192.168.1.20/tmpfs/auto.jpg", headers=headers)
        image = Image.open(BytesIO(response.content))
        q.put(image)


def image_get(q, window_name):
    #cv2.namedWindow(window_name, flags=cv2.WINDOW_FREERATIO)
    yellowLower = np.array([32, 170, 240])
    yellowUpper = np.array([34, 255, 255])
    while True:
        try:
            image = q.get()
            frame = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
            # change to hsv model
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # get mask
            mask = cv2.inRange(hsv, yellowLower, yellowUpper)
            # detect blue
            res = cv2.bitwise_and(frame, frame, mask=mask)
            gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
            minLineLength = 10
            maxLineGap = 5
            lines = cv2.HoughLinesP(gray, 100, np.pi / 180, 100, minLineLength, maxLineGap)
            _, contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) > 0:
                if str(type(lines)) != "<class 'NoneType'>":
                    mc.set("ishuman", True)
                else:
                    mc.set("ishuman", False)
            else:
                mc.set("ishuman", False)
        except Exception as e:
            #print(e)
            mc.set("ishuman", False)
            continue
        #cv2.imshow(window_name, frame)
        time.sleep(0.1)
        #cv2.waitKey()


# def people():
#     yellowLower = np.array([32, 170, 240])
#     yellowUpper = np.array([34, 255, 255])
#     while True:
#         try:
#             # headers = {
#             #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#             #     'Accept - Encoding': 'gzip, deflate',
#             #     'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
#             #     'Authorization': "basic YWRtaW46YWRtaW4=",
#             #     'Connection': 'Keep-Alive',
#             #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
#             #
#             # response = requests.get("http://192.168.1.20/tmpfs/auto.jpg", headers=headers)
#             # image = Image.open(BytesIO(response.content))
#             frame = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
#             #change to hsv model
#             hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#             # get mask
#             mask = cv2.inRange(hsv, yellowLower, yellowUpper)
#                         # detect blue
#             res = cv2.bitwise_and(frame, frame, mask=mask)
#             gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
#             minLineLength = 10
#             maxLineGap = 5
#             lines = cv2.HoughLinesP(gray, 100, np.pi/180, 100, minLineLength, maxLineGap)
#             _, contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#             if len(contours) > 0:
#                 if str(type(lines)) != "<class 'NoneType'>":
#                     mc.set("ishuman", True)
#                 else:
#                     mc.set("ishuman", False)
#             else:
#                 mc.set("ishuman", False)
#         except Exception as e:
#             print(e)
#             mc.set("ishuman", False)
#             continue


def run_multi_camera():
    camera_ip_l = [
        "172.20.114.26",  # ipv4
        # 把你的摄像头的地址放到这里，如果是ipv6，那么需要加一个中括号。
    ]

    mp.set_start_method(method='spawn')  # init
    queue = mp.Queue(maxsize=2)

    # processes = [mp.Process(target=image_put, args=(queue)),
    #              mp.Process(target=image_get, args=(queue, "s"))]
    #
    # [process.start() for process in processes]
    # [process.join() for process in processes]
    processes = []
    processes.append(mp.Process(target=image_put, args=(queue, )))
    processes.append(mp.Process(target=image_get, args=(queue, "b")))
    #
    # # for queue, camera_ip in zip(queues, camera_ip_l):
    # #     print(queue, camera_ip)
    # #     # processes.append(mp.Process(target=image_put, args=(queue,)))
    # #     # processes.append(mp.Process(target=image_get, args=(queue, camera_ip)))
    for process in processes:
        process.daemon = True
        process.start()
    for process in processes:
        process.join()


if __name__ == '__main__':
    time.sleep(10)
    run_multi_camera()





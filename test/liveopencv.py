import subprocess
import datetime
import memcache
import cv2
import time
import multiprocessing as mp


mc = memcache.Client(['192.168.1.10:12000'], debug=True)
fps = 25


def image_put(q):
    while True:
        now = time.time()
        baseimg = cv2.imread("../sourcefile/live.png")
        ret = mc.get('info')
        rpm = str(ret["carstate"]["RPM"]) + "r/min"
        speed = str(ret["carstate"]["SPEED"]) + "km/h"
        COOLANT_TEMP = str(ret["carstate"]["COOLANT_TEMP"])
        fuel = str(ret["carstate"]["FUEL"])
        ENGINE_LOAD = str(round(ret["carstate"]["ENGINE_LOAD"], 1)) + "%"
        v = str(12.2) + "V"
        nowtime = datetime.datetime.now().strftime('%H-%M-%S')
        cv2.putText(baseimg, nowtime, (10, 340), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 1, cv2.LINE_AA)
        # cv2.putText(baseimg, rpm, (130, 73), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(baseimg, rpm, (130, 73), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(baseimg, COOLANT_TEMP, (50, 150), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(baseimg, fuel, (180, 150), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(baseimg, ENGINE_LOAD, (50, 270), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(baseimg, v, (180, 270), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 1, cv2.LINE_AA)
        q.put(baseimg)
        sleeptime = time.time() - now
        sleeptime = 1 / fps - sleeptime
        if sleeptime > 0:
            time.sleep(sleeptime)
        #q.get() if q.qsize() > 1 else time.sleep(0.2)


def image_get(q, window_name):
    #cv2.namedWindow(window_name, flags=cv2.WINDOW_FREERATIO)
    size = [280, 400]
    rtmp = 'rtmp://localhost/live/test'
    sizeStr = str(size[0]) + 'x' + str(size[1])
    command = ['ffmpeg',
                    '-y',
                    '-f', 'rawvideo',
                    '-vcodec', 'rawvideo',
                    '-pix_fmt', 'bgr24',
                    '-s', sizeStr,
                    '-r', "25",
                    '-i', '-',
                    '-c:v', 'libx264',
                    '-pix_fmt', 'yuv420p',
                    '-preset', 'ultrafast',
                    '-f', 'flv',
                    rtmp]
    pipe = subprocess.Popen(command
                            , shell=False
                            , stdin=subprocess.PIPE
                            )
    while True:
        frame = q.get()
        pipe.stdin.write(frame.tostring())
        #cv2.imshow(window_name, frame)
        # time.sleep(0.2)
        #cv2.waitKey()

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
    run_multi_camera()
    #test()


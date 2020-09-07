from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
import memcache
import time
import cv2
import numpy as np
import datetime
from multiprocessing import Process
import os
import json
from webutils.formhelper import SettingForm
import subprocess
import datetime
import memcache
import multiprocessing as mp

mc = memcache.Client(['127.0.0.1:12000'], debug=True)
fps = 25

class flag():
    def __init__(self):
        self.flag = False

flagstop = flag()
flaglivestop = flag()
processes = []

d = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parent_path = os.path.dirname(d)

class VideoRender(object):
    def __init__(self, baseimgpath, save_path):
        self.baseimgpath = baseimgpath
        self.fps = 30
        self.save_path = save_path

    def render_video(self):
        try:
            fps = 30.0  # 视频帧率
            size = (289, 419)
            fourcc = cv2.VideoWriter_fourcc(*'X264')
            file = self.save_path + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".mp4"
            videoWriter = cv2.VideoWriter(file, fourcc, fps, size)
            while not flagstop.flag:
                now = time.time()
                baseimg = cv2.imread(self.baseimgpath)
                ret = mc.get('info')
                rpm = str(ret["carstate"]["RPM"]) + "r/min"
                speed = str(ret["carstate"]["SPEED"]) + "km/h"
                COOLANT_TEMP = str(ret["carstate"]["COOLANT_TEMP"])
                fuel = str(ret["carstate"]["FUEL"])
                ENGINE_LOAD = str(round(ret["carstate"]["ENGINE_LOAD"],1)) + "%"
                v = str(12.2) + "V"
                cv2.putText(baseimg, rpm, (130, 73), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 2, cv2.LINE_AA)
                cv2.putText(baseimg, COOLANT_TEMP, (50, 150), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(baseimg, fuel, (180, 150), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(baseimg, ENGINE_LOAD, (50, 270), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(baseimg, v, (180, 270), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 1, cv2.LINE_AA)
                videoWriter.write(baseimg)
                sleeptime = time.time() - now
                sleeptime = 1 / fps - sleeptime
                if sleeptime > 0:
                    time.sleep(sleeptime)
                #time.sleep(1 / fps)
            videoWriter.release()
            cv2.destroyAllWindows()
        except Exception as e:
            print(str(e))
            mc.set('error', str(e))


def image_put(q):
    while not flagstop.flag:
        try:
            now = time.time()
            baseimg = cv2.imread(parent_path + "/sourcefile/live.png")
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
        except Exception as e:
            mc.set("liverror", str(e))
        #q.get() if q.qsize() > 1 else time.sleep(0.2)


def image_get(q, rtmpaddress):
    try:
        #cv2.namedWindow(window_name, flags=cv2.WINDOW_FREERATIO)
        size = [280, 400]
        rtmp = rtmpaddress
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
        while not flagstop.flag:
            frame = q.get()
            pipe.stdin.write(frame.tostring())
    except Exception as e:
        mc.set("liverror", str(e))


def run_multi_camera(rtmpaddress):
    mp.set_start_method(method='spawn')  # init
    queue = mp.Queue(maxsize=2)

    processes.append(mp.Process(target=image_put, args=(queue, )))
    processes.append(mp.Process(target=image_get, args=(queue, rtmpaddress)))
    for process in processes:
        process.daemon = True
        process.start()
    for process in processes:
        process.join()


def home_page(request):
    return render(request, 'dashboard.html', {"action": "home"})


def video(request):
    state = mc.get("videostate")
    error = mc.get('error')
    return render(request, 'videos.html', {"action": "video", "videostate": state})


def settings(request):
    d = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    parent_path = os.path.dirname(d)
    with open(parent_path + "/settings.json", "r") as f:
        settings = json.load(f)
    if request.method == "GET":
            return render(request, 'settings.html', {"action": "video", "displacemen": settings["displacemen"],
                                                     "obdmode": settings["obd"]["mode"], "address": settings["obd"]["address"]})

    if request.method == "POST":
        form = SettingForm(request.POST)
        if form.is_valid():
            displacemen = request.POST["displacemen"]
            address = request.POST["address"]
            settings["displacemen"] = displacemen
            settings["obd"]["address"] = address
            settings = json.dumps(settings)
            with open(parent_path + "/settings.json", "w") as f:
                f.write(settings)
            os.system("sudo reboot")
        else:
            print(form.cleaned_data)  #
            print(form.errors)  # ErrorDict : {"校验错误的字段":["错误信息",]}
            print(form.errors.get("name"))  # ErrorList ["错误信息",]


def record(request):
    state = mc.get("videostate")
    error = mc.get('error')
    return render(request, 'record.html', {"action": "video", "videostate": state})

def start_record(request):
    if request.method =="POST":
        savepath =request.POST["savepath"]
        flagstop.flag = False
        mc.set('videostate', True)
        video = VideoRender("/home/pi/Documents/carOBD/dashboard/web/utils/base.jpg", savepath)
        videoprocess = Process(target=video.render_video())
        videoprocess.start()
        # return redirect(reverse("video"))
        # video = VideoRender('/Users/aizawanozomi/mycodes/carOBDPI/carOBD/dashboard/web/utils/baseimg.jpg', savepath)
        #
        # # videoprocess = Process(target=video.render_video())
        return redirect(reverse("video"))

    # if request.method == "GET":GET
    #     #
    #     # elif request.method == "POST":
    #     #
    #     #     return HttpResponse("start")


def stop_record(request):
    flagstop.flag = True
    mc.set('videostate', False)
    return redirect(reverse("video"))


def get_info(request):
    ret = mc.get("info")
    return JsonResponse(ret)


def live(request):
    state = mc.get("livestate")
    print(mc.get("liverror"))
    return render(request, 'live.html', {"action": "video", "livestate": state})


def startLive(request):
    if request.method =="POST":
        rtmpaddress =request.POST["live"]

        flaglivestop.flag = False
        mc.set('livestate', True)
        run_multi_camera(rtmpaddress)
        return redirect(reverse("video"))


def stopLive(request):
    flaglivestop.flag = True
    print(processes)
    for p in processes:
        p.terminate()
        p.join()
    mc.set('livestate', False)
    return redirect(reverse("video"))

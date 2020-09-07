import cv2
from flask import Flask, render_template, Response
import time
import requests


class VideoCamera(object):
    def __init__(self, filename):
        # 通过opencv获取实时视频流
        self.cap = cv2.VideoCapture(0)
        print("Camera warming up ...")
        time.sleep(1)
        # Prepare Capture
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.cap.set(3, 1280)
        self.cap.set(4, 720)
        w = int(self.cap.get(3))
        h = int(self.cap.get(4))
        print(fps)
        print(w, h)
        # Define the codec and create VideoWriter object
        # self.fourcc =  cv2.VideoWriter_fourcc(*'XVID')  # You also can use (*'XVID')
        self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.out = cv2.VideoWriter(
            filename + '.avi', self.fourcc, fps, (w, h), True)

    def __del__(self):
        self.cap.release()

    def saveVideo(self):
        # Write the frame...

        self.out.write(self.frame)

    def delall(self):
        self.cap.release()
        self.out.release()

    def get_frame(self):
        success, image = self.cap.read()
        # 因为opencv读取的图片并非jpeg格式，因此要用motion JPEG模式需要先将图片转码成jpg格式图片
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes(), image


class flag():
    def __init__(self):
        self.flag = True


app = Flask(__name__)
flagstop = flag()


@app.route('/')  # 主页
def index():
    # jinja2模板，具体格式保存在index.html文件中
    return render_template('cameraViewr.html')


@app.route('/start')  # 主页
def start():
    # jinja2模板，具体格式保存在index.html文件中
    pass


@app.route('/stop')  # 结束录制
def stop():
    # jinja2模板，具体格式保存在index.html文件中
    print("stop")
    flagstop.flag = False
    return "stoped"


def gen():
    while True:
        start_time = time.time()
        capture_duration = 300
        camera = VideoCamera(str(start_time))
        is5min = int(time.time() - start_time) < capture_duration
        while is5min & flagstop.flag:
            success, image = camera.cap.read()
            # resize it to (1024,768)
            displayImg = cv2.resize(image, (1024, 768))
            ret = requests.get("http://localhost:5000")
            ret = ret.json()
            showtext = ret["date"] + " " + str(ret["carstate"]["SPEED"]) + \
                "km/h TPS" + str(ret["carstate"]["THROTTLE_POS"]) + \
                "% ENGINE_LOAD" + str(ret["carstate"]["ENGINE_LOAD"])
            cv2.putText(image, showtext, (10, 715),
                        cv2.FONT_HERSHEY_PLAIN, 1.8, (255, 255, 255), 3, cv2.LINE_AA)
            camera.out.write(image)
            # 因为opencv读取的图片并非jpeg格式，因此要用motion JPEG模式需要先将图片转码成jpg格式图片
            ret, jpeg = cv2.imencode('.jpg', image)
            frame = jpeg.tobytes()
            # frame = camera.get_frame()[0]

        # 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        camera.delall()
        flagstop.flag = True
        time.sleep(1)


@app.route('/video_feed')  # 这个地址返回视频流响应
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)

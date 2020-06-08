import time
import datetime
import numpy as np
import cv2
import memcache

mc = memcache.Client(['127.0.0.1:12000'], debug=True)


class VideoRender(object):
    def __init__(self, baseimgpath):
        self.baseimgpath = baseimgpath

    def render_video(self):
        try:
            fps = 30  # 视频帧率
            # print(self.baseimgpath)
            # baseimg = cv2.imread(self.baseimgpath)
            # print(type(baseimg))
            size = (289, 419)
            fourcc = cv2.VideoWriter_fourcc(*'X264')
            # videowriter = cv2.VideoWriter(
            #         'output.avi',fourcc, fps,size, True)
            filename = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".mp4"
            videoWriter = cv2.VideoWriter(filename, fourcc, 30.0, size)
            mc.set('videostate', True)
            while True:
                now = time.time()
                # ret, frame = cap.read()
                baseimg = cv2.imread("/home/pi/Documents/carOBD/dashboard/web/utils/base.jpg")
                ret = mc.get('info')
                rpm = str(ret["carstate"]["RPM"]) + "r/min"
                speed = str(ret["carstate"]["SPEED"]) + "km/h"
                COOLANT_TEMP = str(ret["carstate"]["COOLANT_TEMP"])
                fuel = "2L/km"
                ENGINE_LOAD = str(ret["carstate"]["ENGINE_LOAD"]) + "%"
                v = str(12.2) + "V"
                cv2.putText(baseimg, rpm, (130, 73), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 2, cv2.LINE_AA)
                cv2.putText(baseimg, COOLANT_TEMP, (50, 150), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(baseimg, fuel, (180, 150), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(baseimg, ENGINE_LOAD, (50, 270), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(baseimg, v, (180, 270), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 1, cv2.LINE_AA)
                endtime = time.time()
                sleeptime = endtime - now
                cv2.imshow("1", baseimg)
                videoWriter.write(baseimg)
                time.sleep(1 / fps - sleeptime)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            videoWriter.release()
            cv2.destroyAllWindows()
        except Exception as e:
            print(e)
            mc.set('error', str(e))


# def render_video(baseimgpath):
#     fps = 30  # 视频帧率
#     baseimg = cv2.imread(baseimgpath)
#     print(type(baseimg))
#     cap = cv2.VideoCapture(0)
#     size = (289, 419)
#
#     fourcc = cv2.VideoWriter_fourcc(*'XVID')
#     # videowriter = cv2.VideoWriter(
#     #         'output.avi',fourcc, fps,size, True)
#     filename = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".mp4"
#     videoWriter = cv2.VideoWriter(filename, fourcc, 5.0, size)
#
#     while True:
#         # ret, frame = cap.read()
#         baseimg = cv2.imread(baseimgpath)
#         rows,cols,a = baseimg.shape
#         print(rows, cols)
#         ret = mc.get('info')
#         rpm = str(ret["carstate"]["RPM"]) + "r/min"
#         speed = str(ret["carstate"]["SPEED"]) + "km/h"
#         COOLANT_TEMP = str(ret["carstate"]["COOLANT_TEMP"])
#         fuel = "2L/km"
#         ENGINE_LOAD = str(ret["carstate"]["ENGINE_LOAD"]) + "%"
#         v = str(12.2) + "V"
#         cv2.putText(baseimg, rpm, (130, 73), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 2, cv2.LINE_AA)
#         cv2.putText(baseimg, COOLANT_TEMP, (50, 150), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 1, cv2.LINE_AA)
#         cv2.putText(baseimg, fuel, (180, 150), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 1, cv2.LINE_AA)
#         cv2.putText(baseimg, ENGINE_LOAD, (50, 270), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 1, cv2.LINE_AA)
#         cv2.putText(baseimg, v, (180, 270), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 1, cv2.LINE_AA)
#         videoWriter.write(baseimg)
#         cv2.imshow('aa', baseimg)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     cap.release()
#     videoWriter.release()
#     cv2.destroyAllWindows()


if __name__ == "__main__":
    video = VideoRender('/Users/aizawanozomi/mycodes/carOBDPI/carOBD/dashboard/web/utils/baseimg.jpg')
    video.render_video()
    #render_video("/Users/aizawanozomi/mycodes/carOBDPI/carOBD/sourcefile/base.jpg")
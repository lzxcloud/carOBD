from multiprocessing import Process
import cv2
import datetime

class VideoRender(object):
    def __init__(self, baseimgpath):
        self.baseimgpath = baseimgpath

    def render_video(self):
        try:

            fps = 30  # 视频帧率
            # print(self.baseimgpath)
            # baseimg = cv2.imread(self.baseimgpath)
            # print(type(baseimg))
            cap = cv2.VideoCapture(0)
            size = (289, 419)

            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            # videowriter = cv2.VideoWriter(
            #         'output.avi',fourcc, fps,size, True)
            filename = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".mp4"
            videoWriter = cv2.VideoWriter(filename, fourcc, 5.0, size)
            while True:
                # ret, frame = cap.read()
                baseimg = cv2.imread("/Users/aizawanozomi/mycodes/carOBDPI/carOBD/sourcefile/base.jpg")
                # ret = mc.get('info')
                # rpm = str(ret["carstate"]["RPM"]) + "r/min"
                # speed = str(ret["carstate"]["SPEED"]) + "km/h"
                # COOLANT_TEMP = str(ret["carstate"]["COOLANT_TEMP"])
                # fuel = "2L/km"
                # ENGINE_LOAD = str(ret["carstate"]["ENGINE_LOAD"]) + "%"
                # v = str(12.2) + "V"
                # cv2.putText(baseimg, rpm, (130, 73), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 2, cv2.LINE_AA)
                # cv2.putText(baseimg, COOLANT_TEMP, (50, 150), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 1, cv2.LINE_AA)
                # cv2.putText(baseimg, fuel, (180, 150), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 1, cv2.LINE_AA)
                # cv2.putText(baseimg, ENGINE_LOAD, (50, 270), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 1, cv2.LINE_AA)
                # cv2.putText(baseimg, v, (180, 270), cv2.FONT_HERSHEY_PLAIN, 1.8, (0, 0, 0), 1, cv2.LINE_AA)
                videoWriter.write(baseimg)
            cap.release()
            videoWriter.release()
            cv2.destroyAllWindows()
        except Exception as e:
            mc.set('error', str(e))



def run():
    video = VideoRender("/Users/aizawanozomi/mycodes/carOBDPI/carOBD/sourcefile/base.jpg")
    videoprocess = Process(target=video.render_video())
    #obdprocess = Process(target=testobdserver.odbinfo())
    videoprocess.start()




if __name__ == "__main__":
    run()
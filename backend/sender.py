#!/usr/bin/python3
import memcache
import time
import  requests
import json
#发送信息到远端服务器


def savedata():
    time.sleep(1)
    step = 0
    sendlist = []
    while True:
        ret = requests.get("http://localhost:5000/")
        step +=1
        try:
            ret = ret.json()
            carstate = ret["carstate"]
            kPa = carstate["INTAKE_PRESSURE"] - carstate["BAROMETRIC_PRESSURE"]
            bar = kPa / 100
            carstate["BAR"] = bar
            sendlist.append(carstate)
            time.sleep(1)
            if step == 60:
                try:
                    ret = requests.post("http://demo:10800/save", data={"data": json.dumps(sendlist)})
                except Exception as e:
                    pass
                step = 0
                sendlist = []
        except:
            time.sleep(30)
            savedata()
time.sleep(10)
savedata()
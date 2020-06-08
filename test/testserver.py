#!/usr/bin/python3
from flask import Flask
from flask_restful import Api, Resource
from flask_cors import *
import time
import datetime
import random
import  requests
import threading
import json
# import redis
# # 这里替换为连接的实例host和port
# host = '192.168.0.50'
# port = 6379
#
# pwd = 'pm12@gdmm'
# r = redis.StrictRedis(host=host, port=6379, password=pwd)
# r.set('foo', 'bar')
# print(r.get('foo'))

app = Flask(__name__)
api = Api(app)
CORS(app, supports_credentials=True)


class carinfo(Resource):
    def get(self):
        pack = {
            "date": datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
            "carstate": {

                "date": datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
                "RPM": random.randint(800, 7000),
                "SPEED": random.randint(0, 180),
                "COOLANT_TEMP": random.randint(20, 120),
                "INTAKE_TEMP": random.randint(20, 120),
                "INTAKE_PRESSURE": random.randint(0, 255),
                "ENGINE_LOAD": random.randint(0, 100),
                "THROTTLE_POS": random.randint(0, 100),
                "RUN_TIME": 2700,
                "CONTROL_MODULE_VOLTAGE": 14.3,
                "BAROMETRIC_PRESSURE": 89,

            }
        }
        return pack


api.add_resource(carinfo, '/')

if __name__ == '__main__':
    #result = bluetooth.lookup_name('DC:0D:30:47:76:43', timeout=3)
    # if (result != None):
    # time.sleep(5)
    # t1 = threading.Thread(target=savedata)
    # t1.start()
    app.run(host='0.0.0.0')
    
    # else:
    # print("Disconnected")
    #call(["sudo", "rfcomm", "release", "0"])
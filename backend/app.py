#!/usr/bin/python3
from flask import Flask
from flask_restful import Api, Resource
from flask_cors import *
import memcache
import time

app = Flask(__name__)
api = Api(app)
CORS(app, supports_credentials=True)
mc = memcache.Client(['127.0.0.1:12000'], debug=False)
mc.set("ishuman", False)
class carinfoapi(Resource):
    def get(self):
        return mc.get("info")
#用于识别行人 可选
class ishuman(Resource):
    def get(self):
        return mc.get("ishuman")

api.add_resource(carinfoapi, '/')
api.add_resource(ishuman, '/ishuman')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
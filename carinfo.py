import obd
import time
import datetime
import random
import memcache
import multiprocessing
import os

allcommands = [
    obd.commands.RPM,
    obd.commands.SPEED,
    obd.commands.COOLANT_TEMP,
    obd.commands.INTAKE_TEMP,
    obd.commands.INTAKE_PRESSURE,
    obd.commands.ENGINE_LOAD,
    obd.commands.THROTTLE_POS,
    obd.commands.RUN_TIME,
    obd.commands.CONTROL_MODULE_VOLTAGE,
    obd.commands.BAROMETRIC_PRESSURE,
    obd.commands.FUEL_RAIL_PRESSURE_DIRECT,
    obd.commands.TIMING_ADVANCE
]

mc = memcache.Client(['127.0.0.1:12000'], debug=True)
mc.set("ishuman", False)
def run():
    connection = obd.OBD(fast=True,timeout=0.1)
    while True:
        pack = {
            "date": datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
            "carstate": {
            "date": datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
            "RPM": None,
            "SPEED": None,
            "COOLANT_TEMP": None,
            "INTAKE_TEMP": None,
            "INTAKE_PRESSURE": None,
            "ENGINE_LOAD": None,
            "THROTTLE_POS": None,
            "RUN_TIME": None,
            "CONTROL_MODULE_VOLTAGE": None,
            "BAROMETRIC_PRESSURE": None,
            "FUEL_RAIL_PRESSURE":None,
            "TIMING_ADVANCE":None,
            "ISHUMAN":mc.get("ishuman")
            }
        }
        retlist = []
        for cmd in allcommands:
            retlist.append(connection.query(cmd).value.magnitude)



        pack["carstate"]["RPM"] = retlist[0]
        pack["carstate"]["SPEED"] = retlist[1]
        pack["carstate"]["COOLANT_TEMP"] = retlist[2]
        pack["carstate"]["INTAKE_TEMP"] = retlist[3]
        pack["carstate"]["INTAKE_PRESSURE"] = retlist[4]
        pack["carstate"]["ENGINE_LOAD"] = retlist[5]
        pack["carstate"]["THROTTLE_POS"] = retlist[6]
        pack["carstate"]["RUN_TIME"] = retlist[7]
        pack["carstate"]["CONTROL_MODULE_VOLTAGE"] = retlist[8]
        pack["carstate"]["BAROMETRIC_PRESSURE"] = retlist[9]
        pack["carstate"]["FUEL_RAIL_PRESSURE"] = retlist[10]
        pack["carstate"]["TIMING_ADVANCE"] = retlist[11]
        mc.set("info", pack)
        time.sleep(0.2)
        
time.sleep(5) 
run()

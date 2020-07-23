import obd
import json
import memcache
import datetime
import time
import os

def run():
    mc = memcache.Client(['127.0.0.1:12000'], debug=True)
    mc.set("ishuman", False)
    allcommands = {}
    with open('/home/pi/Documents/carOBD/settings.json', 'r') as f:
        settings = json.load(f)

        displacemen = float(settings["displacemen"]) /1000

        for i in settings["obdallcommand"]:
            command = getattr(obd.commands, i)
            allcommands[i] = command
        # 用于识别行人 可选
    pack = {}
    connection = obd.OBD(fast=True, timeout=0.1)
    # try:

    while True:
        pack = {
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
                "FUEL_RAIL_PRESSURE": None,
                "TIMING_ADVANCE": None,
                "MAF": None,
                "FUEL": None,
                "ISHUMAN": mc.get("ishuman")
            }
        }
        # retlist = []
        for cmd in allcommands.keys():
            r = connection.query(allcommands[cmd])
            if not r.is_null():
                pack["carstate"][cmd] = r.value.magnitude

            else:
                pack["carstate"][cmd] = None

        if pack["carstate"]["MAF"] == None:
            # L = 1.59617602 * int(retlist[0]) * int(retlist[4]) / (int(retlist[3]) + 233) / 5 / 0.002 * 0.0018
            # L = 1.59617602 *int(pack["carstate"]["RPM"]) * int(["carstate"]["INTAKE_PRESSURE"]) / (
            #             int(["carstate"]["INTAKE_TEMP"]) + 233) / int(["carstate"]["SPEED"]) / 0.002 * 0.0018
            # L = 7.9808801 * 0.0018 * float(retlist[0]) * int(retlist[4]) / (int(retlist[3]) + 233) / retlist[
            #     1] * 100
            if pack["carstate"]["SPEED"] > 0:
                pack['carstate']['FUEL'] = 7.9808801 * displacemen * float(pack["carstate"]["RPM"]) * int(
                    pack["carstate"]["INTAKE_PRESSURE"]) / (int(pack["carstate"]["INTAKE_TEMP"])+273 + 233) / \
                                           pack["carstate"]["SPEED"] * 100
                if pack['carstate']['FUEL'] > 19.9:
                    pack['carstate']['FUEL'] = 19.9
                pack['carstate']['FUEL'] = str(round(pack['carstate']['FUEL'], 1)) + "L/100km"
            else:
                pack['carstate']['FUEL'] =  7.9808801 * displacemen * float(pack["carstate"]["RPM"]) * int(
                    pack["carstate"]["INTAKE_PRESSURE"]) / (int(pack["carstate"]["INTAKE_TEMP"]) + 273 + 233)
                pack['carstate']['FUEL'] = str(round(pack['carstate']['FUEL'], 1)) + "L/h"
        else:
            if pack["carstate"]["SPEED"] > 0:
                pack['carstate']['FUEL'] = 489.79591836 * pack['carstate']['MAF'] / (pack["carstate"]["SPEED"] * 14.7)
                if pack['carstate']['FUEL'] > 19.9:
                    pack['carstate']['FUEL'] = 19.9
                pack['carstate']['FUEL'] =str(round(pack['carstate']['FUEL'], 1)) + "L/100km"
            else:
                pack['carstate']['FUEL'] = str(round(3600 * pack['carstate']['MAF'] / 735 / 14.7, 1)) + "L/h"
        mc.set("info", pack)
        time.sleep(0.2)
    # except Exception as e:


#     print(str(e))
if __name__ == "__main__":
    d = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    time.sleep(5)
    with open(d + "/settings.json", 'r') as f:
        settings = json.load(f)["obd"]
        if settings["mode"] == "Bluetooth":
            cmd = "sudo rfcomm bind 0 {0} 1 ".format(settings["address"])
            os.system(cmd)
    time.sleep(3)
    run()

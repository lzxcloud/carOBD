import obd
import json
import memcache
import datetime
import time


# allcommands = [
#     obd.commands.RPM,
#     obd.commands.SPEED,
#     obd.commands.COOLANT_TEMP,
#     obd.commands.INTAKE_TEMP,
#     obd.commands.INTAKE_PRESSURE,
#     obd.commands.ENGINE_LOAD,
#     obd.commands.THROTTLE_POS,
#     obd.commands.RUN_TIME,
#     obd.commands.CONTROL_MODULE_VOLTAGE,
#     obd.commands.BAROMETRIC_PRESSURE,
#     obd.commands.FUEL_RAIL_PRESSURE_DIRECT,
#     obd.commands.TIMING_ADVANCE,
# ]


def run():
    mc = memcache.Client(['127.0.0.1:12000'], debug=True)
    mc.set("ishuman", False)
    allcommands = {}
    with open('../settings.json', 'r') as f:
        settings = json.load(f)["obdallcommand"]
        for i in settings:
            command = getattr(obd.commands, i)
            allcommands[i]=command
        # 用于识别行人 可选
    print(allcommands)
    pack = {}
    try:
        connection = obd.OBD(fast=True, timeout=0.1)
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
            #retlist = []
            for cmd in allcommands:
                r = connection.query(cmd)
                if not r.is_null():
                    pack[cmd] = r.value.magnitude
                else:
                    pack[cmd] = None
            # pack["carstate"]["RPM"] = int(retlist[0])
            # pack["carstate"]["SPEED"] = retlist[1]
            # pack["carstate"]["COOLANT_TEMP"] = round(retlist[2], 1)
            # pack["carstate"]["INTAKE_TEMP"] = retlist[3]
            # pack["carstate"]["INTAKE_PRESSURE"] = retlist[4]
            # pack["carstate"]["ENGINE_LOAD"] = round(retlist[5], 1)
            # pack["carstate"]["THROTTLE_POS"] = retlist[6]
            # pack["carstate"]["RUN_TIME"] = retlist[7]
            # pack["carstate"]["CONTROL_MODULE_VOLTAGE"] = round(retlist[8], 1)
            # pack["carstate"]["BAROMETRIC_PRESSURE"] = round(retlist[9], 1)
            # pack["carstate"]["FUEL_RAIL_PRESSURE"] = round(retlist[10], 1)
            # pack["carstate"]["TIMING_ADVANCE"] = round(retlist[11], 1)
            # pack["carstate"]["MAF"] = retlist[12]

            if pack["MAF"] == None:
                #L = 1.59617602 * int(retlist[0]) * int(retlist[4]) / (int(retlist[3]) + 233) / 5 / 0.002 * 0.0018
                # L = 1.59617602 *int(pack["carstate"]["RPM"]) * int(["carstate"]["INTAKE_PRESSURE"]) / (
                #             int(["carstate"]["INTAKE_TEMP"]) + 233) / int(["carstate"]["SPEED"]) / 0.002 * 0.0018
                # L = 7.9808801 * 0.0018 * float(retlist[0]) * int(retlist[4]) / (int(retlist[3]) + 233) / retlist[
                #     1] * 100
                if pack["carstate"]["SPEED"] > 0:
                    pack['carstate']['FUEL'] = 7.9808801 * 0.0018 * float(pack["carstate"]["RPM"]) * int(
                        pack["carstate"]["INTAKE_PRESSURE"]) / (int(pack["carstate"]["INTAKE_TEMP"]) + 233) / \
                                               pack["carstate"]["SPEED"] * 100
                    if pack['carstate']['FUEL'] > 19.9:
                        pack['carstate']['FUEL'] = 19.9
                    pack['carstate']['FUEL'] = round(pack['carstate']['FUEL'], 1)
                else:
                    pack['carstate']['FUEL'] = 7.9808801 * 0.0018 * float(pack["carstate"]["RPM"]) * int(
                        pack["carstate"]["INTAKE_PRESSURE"]) / (int(pack["carstate"]["INTAKE_TEMP"]) + 233)
            else:
                if pack["carstate"]["SPEED"] > 0:
                    pack['carstate']['FUEL'] = 489.79591836 * pack['carstate']['MAF']/(pack["carstate"]["SPEED"] * 14.7)
                    if pack['carstate']['FUEL'] > 19.9:
                        pack['carstate']['FUEL'] = 19.9
                    pack['carstate']['FUEL'] = round(pack['carstate']['FUEL'], 1)
                else:
                    pack['carstate']['FUEL'] = round(3600 * pack['carstate']['MAF']/735/14.7, 1)

            mc.set("info", pack)
            time.sleep(0.2)
            print(pack)
    except Exception as e:
        print(str(e))
time.sleep(5)
run()

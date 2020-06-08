import memcache
import time
import random

mc = memcache.Client(['127.0.0.1:12000'], debug=True)
def odbinfo():
    while True:
        pack = {"carstate":{}}
        pack["carstate"]["RPM"] = random.randint(500, 800)
        pack["carstate"]["SPEED"] = random.randint(0, 120)
        pack["carstate"]["COOLANT_TEMP"] = random.randint(20, 80)
        pack["carstate"]["INTAKE_TEMP"] = random.randint(0, 20)
        pack["carstate"]["INTAKE_PRESSURE"] = random.randint(55,100)
        pack["carstate"]["ENGINE_LOAD"] = random.randint(0, 100)
        pack["carstate"]["THROTTLE_POS"] = random.randint(0, 100)
        pack["carstate"]["RUN_TIME"] = 1100
        pack["carstate"]["CONTROL_MODULE_VOLTAGE"] = "14.4"
        pack["carstate"]["BAROMETRIC_PRESSURE"] = random.randint(0, 100)
        pack["carstate"]["FUEL_RAIL_PRESSURE"] = random.randint(0, 100)
        pack["carstate"]["TIMING_ADVANCE"] = random.randint(0, 100)
        pack["carstate"]["MAF"] = random.randint(0, 100)
        pack["carstate"]["FUEL"] = random.randint(0, 100)

        # L = 1.59617602 * pack["carstate"]["RPM"] * ["carstate"]["INTAKE_PRESSURE"] / (["carstate"]["INTAKE_TEMP"] + 233) / \
        #     ["carstate"]["SPEED"] / 0.002 * 0.0018
        # if ["carstate"]["SPEED"] == 0:
        #     fuel = "暂无"
        # else:
        #     fuel = str(L) + "/100Km"
        # pack['carstate']['fuel'] = L
        mc.set("info", pack)
        time.sleep(1)

odbinfo()
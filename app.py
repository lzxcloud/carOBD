from multiprocessing import Process
import os
import obd
#from test import testobdserver
#from backend import carinfo
import json

# allcommands = ["RPM",
#                "SPEED",
#                "COOLANT_TEMP",
#                "INTAKE_TEMP",
#                "INTAKE_PRESSURE",
#                "ENGINE_LOAD",
#                "THROTTLE_POS",
#                "RUN_TIME",
#                "CONTROL_MODULE_VOLTAGE",
#                "BAROMETRIC_PRESSURE",
#                "FUEL_RAIL_PRESSURE_DIRECT",
#                "TIMING_ADVANCE",
# ]
# commands = []
# for i in allcommands:
#     command = getattr(obd.commands, i)
#     commands.append(command)
# print(commands)
if __name__ == "__main__":
    #读取配置文件


    # obdprocess = Process(target=testobdserver.odbinfo())
    # obdprocess.start()
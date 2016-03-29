#!/usr/bin/env python

from datetime import timedelta, datetime;
import os
import time
from influxdb import InfluxDBClient
import smbus
from LiPoPSU import bq27510
from RPi import GPIO
from docopt import docopt

def battery_data(battery):
    tte = battery.TimeToEmpty
    ttf = battery.TimeToFull

    soc = battery.StateOfCharge
    v   = battery.Voltage
    ac  = battery.AverageCurrent
    nac = battery.NominalAvailableCapacity
    fac = battery.FullAvailableCapacity
    fcc = battery.FullChargeCapacity
    rc  = battery.RemainingCapacity

    print("SOC: %3.2d%%\tV: %4.3fV\tI: %4.3fA\tTTE: %s\tTTF: %s\tNAC: %4.3fAh\tFAC: %4.3fAh\tFCC: %4.3fAh\tRC: %4.3fAh" % (soc, v, ac, tte, ttf, nac, fac, fcc, rc))
    return [
        {
            "measurement": "battery_status",
            "fields": {
                "StateOfCharge": soc,
                "Voltage": v,
                "AverageCurrent": ac,
                "TimeToEmpty": tte,
                "TimeToFull": ttf,
                "NominalAvailableCapacity": nac,
                "FullAvailableCapacity": fac,
                "FullChargeCapacity": fcc,
                "RemaningCapacity": rc
            },
            'points': [battery.StateOfCharge, battery.Voltage, battery.AverageCurrent, str(tte), str(ttf), battery.NominalAvailableCapacity, battery.FullAvailableCapacity, battery.FullChargeCapacity, battery.RemainingCapacity],
            'name': 'Battery Status',
            'columns': ['StateOfCharge', 'Volts', 'Amps', 'TimeToEmpty', 'TimeToFull', 'NominalAvailableCapacity', 'FullAvalableCapacity', 'FullChargeCapacity', 'RemainingCapacity'],
        }
    ]

def run():
    influx = InfluxDBClient(server, port, database, password, user)

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)

    GPIO.output(18, 1)

    address   = 0x55
    pmaddress = 0x09

    bus  = smbus.SMBus(1)

    battery = bq27510.bq27510(bus)

    while True:
        influx.write_points(battery_data(battery))
        time.sleep(5)


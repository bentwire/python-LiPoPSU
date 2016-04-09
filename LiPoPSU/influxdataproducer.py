#!/usr/bin/env python

"""Generate time series data for influxdb.

Usage:
    influx-data-producer [--host=<dbhost>] [--port=<dbport>] [--dbname=<name>] [--dbpass=<passwd>] [--dbuser=<user>] [--ssl]

Options:
    -h, --help  Show this screen.
    --host=<dbhost>  The influxdb host [default: localhost]
    --port=<dbport>  The influxdb port [default: 8086]
"""

# from datetime import timedelta, datetime;
# import os
import time
from influxdb import InfluxDBClient
from LiPoPSU import bq27510
from docopt import docopt

try:
    from RPi import GPIO
except Exception as e:
    print("Demo mode activated.")

try:
    import smbus
except:
    print("Demo mode activated")


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

    sc      = battery.StandbyCurrent
    stte    = battery.StandbyTimeToEmpty
    mlc     = battery.MaxLoadCurrent
    mltte   = battery.MaxLoadTimeToEmpty

    ae      = battery.AvailableEnergy
    ap      = battery.AveragePower
    ttecp   = battery.TTEatConstantPower

    cc      = battery.CycleCount

    temp    = battery.Temperature

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
                "RemaningCapacity": rc,
                "StandbyCurrent": sc,
                "StandbyTimeToEmpty": stte,
                "MaxLoadCurrent": mlc,
                "MaxLoadTimeToEmpty": mltte,
                "AvailableEnergy": ae,
                "AveragePower": ap,
                "TTEatConstantPower": ttecp,
                "CycleCount": cc,
                "Temperature": temp
            },
            'name': 'Battery Status',
        }
    ]


def run():
    arguments = docopt(__doc__, version='0.1.0')

    host     = arguments['--host']
    port     = arguments['--port']
    database = arguments['--dbname']
    password = arguments['--dbpass']
    user     = arguments['--dbuser']
	
    ssl      = arguments['--ssl']

    influx = InfluxDBClient(host, port, database, password, user, ssl=ssl, verify_ssl=ssl)

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)

    GPIO.output(18, 1)

    bus  = smbus.SMBus(1)

    battery = bq27510.bq27510(bus)

    while True:
        try:
            influx.write_points(battery_data(battery))
        except Exception as e:
            print("Exception: '%s'" % (e))
            continue
        time.sleep(5)

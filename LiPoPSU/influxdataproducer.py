#!/usr/bin/env python

"""Generate time series data for influxdb.

Usage:
    influx-data-producer [--host=<dbhost>] [--port=<dbport>] [--ssl] [--dbname=<name>] [--dbpass=<passwd>] [--dbuser=<user>] [--loglevel=<LEVEL>]

Options:
    -h, --help  Show this screen.
    --host=<dbhost>  The influxdb host [default: localhost]
    --port=<dbport>  The influxdb port [default: 8086]
    --ssl            Enable TLS support
    --loglevel=<LEVEL>  The log level to report at. [default: INFO]
"""

# from datetime import timedelta, datetime;
# import os
import time
from influxdb import InfluxDBClient
from LiPoPSU import bq27510
from docopt import docopt

import logging

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

#    print("SOC: %3.2d%%\tV: %4.3fV\tI: %4.3fA\tTTE: %s\tTTF: %s\tNAC: %4.3fAh\tFAC: %4.3fAh\tFCC: %4.3fAh\tRC: %4.3fAh" % (soc, v, ac, tte, ttf, nac, fac, fcc, rc))
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
    arguments = docopt(__doc__, version='0.1.1')

    host     = arguments['--host']
    port     = arguments['--port']
    ssl      = arguments['--ssl']
    database = arguments['--dbname']
    password = arguments['--dbpass']
    user     = arguments['--dbuser']
    loglevel = arguments['--loglevel']
    log      = logging.getLogger('influx-data-producer')

    log.setLevel(getattr(logging, loglevel.upper()))
    logging.basicConfig(level=getattr(logging, loglevel.upper()))

    log.debug("Initializing influxDB connection")
    influx = InfluxDBClient(host, port, database, password, user, ssl=ssl, verify_ssl=ssl)

    log.debug("Initializing SMBus connection")
    try:
        bus = smbus.SMBus(1)
    except Exception as e:
        bus = None

    log.debug("Initializing battery object")
    battery = bq27510.bq27510(bus)

    while True:
        try:
            data = battery_data(battery)
            log.debug("Gathered data points.")
            log.debug(data)
            influx.write_points(data)
        except Exception as e:
            log.warning("Caught exception while uploading data point: '%s'" % (e))
            continue
        time.sleep(5)

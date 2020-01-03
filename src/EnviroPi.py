#!/usr/bin/env python3
#
# Since: December, 2019
# Author: gvenzl
# Name: EnviroPi.py
# Description: EnviroPi program
#
# Copyright 2019 Gerald Venzl
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import argparse
import datetime
import time
import json
import requests

from grove.grove_air_quality_sensor_v1_3 import GroveAirQualitySensor
import seeed_dht

AIR_QUALITY_SENSOR_PIN = 0  # Pin A0
TEMPERATURE_SENSOR_MODEL = seeed_dht.DHT.DHT_TYPE["DHT22"]  # DHT 22 model
TEMPERATURE_SENSOR_PIN = 18  # Pin 12 for PWM

_debug = False


def debug(output):
    if _debug:
        print("{0} - DEBUG: {1}".format(datetime.datetime.utcnow().isoformat() + "Z", output))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--id", required=True, help="The id of the sensor (can be any meaningful string")
    parser.add_argument("-e", "--endpoint", help="The entire REST endpoint (including http/https)")
    parser.add_argument("-p", "--poll", type=int, help="Poll interval in seconds")
    parser.add_argument("-d", "--debug", action='store_true', default=False, help="Produce debug output")
    args = parser.parse_args()

    global _debug
    _debug = args.debug

    debug("Opening Air Quality sensor")
    air_quality_sensor = GroveAirQualitySensor(AIR_QUALITY_SENSOR_PIN)
    debug("Opening Temperature and Humidity sensor")
    temperature_and_humidity_senor = seeed_dht.DHT(TEMPERATURE_SENSOR_MODEL, TEMPERATURE_SENSOR_PIN)

    try:
        while True:
            debug("Reading Air Quality sensor")
            # Divide result by 10 to get to percentage of pollution
            # (int): pollution ratio, 0(0.0%) - 1000(100.0%), 0 is best air quality, 1000 worst air quality
            air_pollution = air_quality_sensor.value / 10.0
            debug("Value air quality sensor: {0}".format(air_pollution))

            debug("Reading Temperature and Humidity sensor")
            # Humidity in percent, temperature in Celsius
            humidity, temperature = temperature_and_humidity_senor.read()
            debug("Values Temperature and Humidity sensor: humidity: {0}, temperature: {1}"
                  .format(humidity, temperature)
                  )

            # Current timestamp in UTC
            tms = datetime.datetime.utcnow()

            # Send data
            if args.endpoint is None:
                debug("Sending data to stdout")
                debug("Raw data: {0}, {1}, {2}, {3}, {4}".format(args.id, tms, air_pollution, humidity, temperature))
                print('Id: "{0}", Timestamp (UTC): "{1}", Air pollution: {2:.1f}%, '
                      'Humidity: {3:.1f}%, Temperature: {4:.1f}c'
                      .format(args.id, tms, air_pollution, humidity, temperature)
                      )
            else:
                debug("Sending data to REST endpoint")
                data = {
                    "id": args.id,
                    "tms_utc": tms.isoformat() + 'Z',
                    "air_poll_pct": round(air_pollution, 1),
                    "humi_pct": round(humidity, 1),
                    "temp_celsius": round(temperature, 1)
                }
                debug("Raw data:\n{0}".format(json.dumps(data, indent=4)))

                headers = {'Content-type': 'application/json'}
                http_response = requests.post(args.endpoint, data=json.dumps(data), headers=headers)

                debug("HTTP response status code: {0}".format(http_response.status_code))
                if http_response.status_code != 200:
                    print("Error sending REST call: " + http_response.reason)
                    debug(http_response.text)

            if args.poll is not None:
                time.sleep(args.poll)
    except KeyboardInterrupt:
        print("Exiting program.")


if __name__ == '__main__':
    main()

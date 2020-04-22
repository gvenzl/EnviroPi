#!/usr/bin/env python3
#
# Since: March, 2020
# Author: gvenzl
# Name: SenseHat.py
# Description: The Sense Hat program
#
# Copyright 2020 Gerald Venzl
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

from sense_emu import SenseHat, ACTION_HELD, ACTION_PRESSED
from time import sleep
import subprocess
import sys

hat = None

# Readings
temp = 0.0    # Temperature in Celsius
humi = 0.0    # Humidity in percentage of relative humidity
pres = 0.0    # Pressure in Millibars
acce = None   # Accelerometer dictionary
comp = 0.0    # Compass direction of North from the magnetometer in degrees
gyro = None   # Gyroscope orientation in degrees from the gyroscope only
orde = None   # current orientation in degrees, 0 to 360, using the aircraft principal axes of pitch, roll and yaw


def println(message):
    """Prints a line on the LED.

    Parameters
    ----------
    message : str
    """
    hat.show_message(message, scroll_speed=0.05)


def shutdown(event):
    """Shuts down the Raspberry Pi.

    Parameters
    ----------
    event : sense_emu.InputEvent
        The input event
    """
    if event.action == ACTION_HELD:
        println("Shutting down.")
        # Shutdown Pi
        subprocess.run("sudo shutdown -h now", shell=True)
        # Exit program
        sys.exit()


def restart(event):
    """Restarts the Raspberry Pi.

    Parameters
    ----------
    event : sense_emu.InputEvent
        The input event
    """
    if event.action == ACTION_HELD:
        println("Restarting...")
        # Restart Pi
        subprocess.run("sudo reboot", shell=True)
        # Exit program
        sys.exit()


def check_connection(event):
    if event.action == ACTION_PRESSED:
        print_connection_status()
    elif event.action == ACTION_HELD:
        reconnect()


def print_connection_status():
    """Prints mobile connection status.
    """
    println("Conn status: ")


def reconnect():
    """Reconnect the mobile connection.
    """


def print_temperature(event):
    """Prints last temperature reading.

    Parameters
    ----------
    event : sense_emu.InputEvent
        The input event
    """
    if event.action == ACTION_PRESSED:
        println("Temp: {0}".format(temp))


def setup():
    """Setup the sense hat.
    """
    global hat
    hat = SenseHat()
    hat.stick.direction_up = restart
    hat.stick.direction_right = check_connection
    hat.stick.direction_down = shutdown
    hat.stick.direction_left = print_temperature


def get_readings():
    """Get current readings.
    """
    global temp, humi, pres, acce, comp, gyro, orde
    temp = round(hat.get_temperature(), 1)
    humi = round(hat.get_humidity(), 1)
    pres = round(hat.get_pressure(), 1)

    acce = hat.get_accelerometer()
    comp = hat.get_compass()
    gyro = hat.get_gyroscope()
    orde = hat.get_orientation_degrees()


def print_readings():
    """Print the readings.
    """
    print("Temperature: {0}".format(temp))
    print("Humidity: {0}".format(humi))
    print("Pressure: {0}".format(pres))
    print("Accelerometer: {0}".format(acce))
    print("Compass: {0}".format(comp))
    print("Gyroscope: {0}".format(gyro))
    print("Orientation (degrees): {0}".format(orde))


if __name__ == '__main__':
    setup()
    try:
        while True:
            get_readings()
            print_readings()
            sleep(1)
    except KeyboardInterrupt:
        hat.clear()
        print("Good Bye!")

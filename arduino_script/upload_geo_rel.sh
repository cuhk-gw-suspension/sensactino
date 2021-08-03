#!/usr/bin/env bash

arduino --upload geophone/geophone.ino --port /dev/ttyUSB1
arduino --upload relative_sensor/relative_sensor.ino --port /dev/ttyUSB2

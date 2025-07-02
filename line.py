#!/usr/bin/env pybricks-micropython

from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

line_sensor = ColorSensor(Port.S3)

robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

BLACK = 5
WHITE = 45
threshold = (BLACK + WHITE) / 2

DRIVE_SPEED = 100
TURN_RATE = 60

PROPORTIONAL_GAIN = 1.2

while True:
    deviation = line_sensor.reflection() - threshold

    turn_rate = PROPORTIONAL_GAIN * deviation

    robot.drive(DRIVE_SPEED, turn_rate)
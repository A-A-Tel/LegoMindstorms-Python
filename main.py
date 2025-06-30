#!/usr/bin/python3
from ev3dev2.sound import Sound
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D

s = Sound()
s.speak('Hello people, python sucks fucking ass')

tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)
tank_drive.on_for_rotations(SpeedPercent(100), SpeedPercent(100), 5)
#!/usr/bin/env pybricks-micropython
import random

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import UltrasonicSensor, TouchSensor, Motor, GyroSensor, ColorSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase

hub = EV3Brick()

touch = TouchSensor(Port.S1)
color = ColorSensor(Port.S3)
gyro = GyroSensor(Port.S2)
ultra = UltrasonicSensor(Port.S4)

arm = Motor(Port.A)
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
drive = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

DISTANCE_THRESHOLD = 500  # mm

gyro.reset_angle(0)
arm.run_until_stalled(100)

class Obstacle:
    angle = 0
    distance = 0

    def __init__(self, angle, distance):
        self.angle = angle
        self.distance = distance

def calculate_turn_amount(current_angle, target_angle):
    """Compute the shortest rotation to the target angle"""
    turn_amount = (target_angle - current_angle + 540) % 360 - 180
    return turn_amount

def turn_to_angle(target_angle):
    current_angle = gyro.angle() % 360
    turn_amount = calculate_turn_amount(current_angle, target_angle)
    drive.turn(turn_amount)

def mid_angle(a1, a2):
    """Calculate center of angular sector"""
    diff = (a2 - a1 + 360) % 360
    return (a1 + diff / 2) % 360

def get_obstacles():
    obstacles = []
    gyro.reset_angle(0)
    start_scan_angle = gyro.angle()

    drive.drive(0, 60)
    detecting = False
    sector_start = 0.0

    dist = 0
    while (gyro.angle() - start_scan_angle) < 360:
        angle = gyro.angle() % 360

        if ultra.distance() < DISTANCE_THRESHOLD:
            if not detecting:
                hub.speaker.beep()
                detecting = True
                sector_start = angle
                dist = ultra.distance()
        else:
            if detecting:
                hub.speaker.beep()
                detecting = False
                sector_end = angle
                center = mid_angle(sector_start, sector_end)
                obstacles.append(Obstacle(center, dist))
                hub.screen.print("Angle: " + str(center) + ", Dist: " + str(dist))

    drive.stop()
    drive.turn(5)
    return obstacles

def terminate_object(obstacle):
    turn_to_angle(obstacle.angle)
    arm.run_until_stalled(-1000)
    drive.straight(DISTANCE_THRESHOLD)
    arm.run_until_stalled(1000)
    drive.straight(-DISTANCE_THRESHOLD)

def shuffle(lst):
    for i in range(len(lst) - 1, 0, -1):
        j = random.randint(0, i)
        lst[i], lst[j] = lst[j], lst[i]

def main():
    obstacles = get_obstacles()
    shuffle(obstacles)

    for obstacle in obstacles:
        terminate_object(obstacle)

main()

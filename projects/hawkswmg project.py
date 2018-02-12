"""Final Ev3 Project
by Megan Hawksworth"""

import robot_controller as robo
import ev3dev.ev3 as ev3
import time


def main():
    robot = robo.Snatch3r()
    robot.climb_building()
    robot.shutdown()

    ev3.Sound.play("/home/robot/csse120/assets/sounds/beauty (1).wav")






main()

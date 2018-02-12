"""Final Ev3 Project
by Megan Hawksworth"""

import robot_controller as robo
import ev3dev.ev3 as ev3
import time


def main():
    ev3.Sound.speak('argh')
    time.sleep(0.1)
    robot = robo.Snatch3r()
    robot.left_motor.run_forever(speed_sp=300)
    robot.shutdown()

    ev3.Sound.play("/home/robot/csse120/assets/sounds/beauty (1).wav")


def climb(robot):
    while True:
        robot.go_forward()


main()
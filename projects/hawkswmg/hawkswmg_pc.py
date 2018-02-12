"""Final Ev3 Project
by Megan Hawksworth"""

import robot_controller as robo
import ev3dev.ev3 as ev3
import time


class DelegateEv3(object):
    def __init__(self):
        self.robot = robo.Snatch3r()
        self.mqtt_client = None


def main():
    my_delegate = DelegateEv3()
    mqtt_client =
    time.sleep(0.3)
    ev3.Sound.play("/home/robot/csse120/assets/sounds/beauty (1).wav")


main()

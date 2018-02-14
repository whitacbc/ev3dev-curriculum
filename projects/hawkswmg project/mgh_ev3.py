"""Final Ev3 project for csse120 by Megan Hawksworth. This project is King
Kong themed. This file is the code that will run on the Ev3"""

import robot_controller as robo
import ev3dev.ev3 as ev3
import time
import mqtt_remote_method_calls as com


class DelegateEv3(object):
    """This delegate helps recieve messages from the ev3"""
    def __init__(self):
        self.mqtt = com.MqttClient()
        self.mqtt.connect_to_pc()


def main():
    robot = robo.Snatch3r()
    mydelegate = DelegateEv3


main()

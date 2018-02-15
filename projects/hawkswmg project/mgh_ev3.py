"""Final Ev3 project for csse120 by Megan Hawksworth. This project is King
Kong themed. This file is the code that will run on the Ev3"""

import robot_controller as robo
import ev3dev.ev3 as ev3
import time
import mqtt_remote_method_calls as com


class DelegateEv3(object):
    """This delegate helps recieve messages from the ev3"""
    def __init__(self, robot):
        self.mqtt = com.MqttClient()
        self.mqtt.connect_to_pc()
        self.robot = robot

    def gorilla_noises(self):
        ev3.Sound.speak("insert noises here")

    def quote_king_kong(self):
        ev3.Sound.play("/home/robot/csse120/assets/sounds/beauty (1).wav")

    def climb_building(self):
        """Moves forward If close to an object, stops the robot and backs
        away. Gorilla noise? hawkswmg"""
        while True:
            self.robot.go_forward(400, 400)
            if self.robot.ir_sensor.proximity == 1:
                self.robot.not_go()
                self.robot.drive_inches(2, -200)
                self.mqtt.send_message("hit_object")
                break
            if self.robot.color_sensor.color == ev3.ColorSensor.COLOR_BLACK:
                self.robot.not_go()
                self.robot.drive_inches(2, -200)
                self.mqtt.send_message("fall_off_building")
                break
            if self.robot.color_sensor.color == ev3.ColorSensor.COLOR_RED:
                while True:
                    if self.robot.color_sensor.color == ev3.ColorSensor.COLOR_RED:
                        self.robot.go_forward(200, 200)
                    if self.robot.color_sensor.color == ev3.ColorSensor.COLOR_WHITE:
                        self.robot.go_right(200)
                    if self.robot.color_sensor.color == ev3.ColorSensor.COLOR_BLUE:
                        break
                self.robot.not_go()
                self.mqtt.send_message("at_the_top")
                self.robot.arm_up()
            time.sleep(0.1)


def main():
    robot = robo.Snatch3r()
    robot.loop_forever()

main()

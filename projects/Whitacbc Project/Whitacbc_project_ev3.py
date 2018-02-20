'''
red is right blue is left

'''

import ev3dev.ev3 as ev3
import mqtt_remote_method_calls as com
import robot_controller as robo
import time

class Messages_from_pc(object):
    MAX_SPEED = 900

    def __init__ (self,rob):
        self.robot = rob
        self.running = True
        self.mqtt_client = None


    def start_manual(self):
        ev3.Sound.speak('Manual Mode is on')

    def go_forward(self, left_speed, right_speed):
        self.robot.go_forward(left_speed,right_speed)

    def go_left(self, left_speed):
        self.robot.go_left(left_speed)

    def go_right(self, right_speed):
        self.robot.go_right(right_speed)

    def go_backwards(self, left_speed, right_speed):
        self.robot.go_backwards(left_speed,right_speed)

    def not_go(self):
        self.robot.not_go()

    def arm_up(self):
        self.robot.arm_up()

    def arm_down(self):
        self.robot.arm_down()


    def arm_calibration(self):
        self.robot.arm_calibration()

    def seek_beacon(self):
       self.robot.seek_beacon()

    def speak_message(self,message):
        ev3.Sound.speak(message[0])



    def Searching(self):
        found = True
        Run_away = True
        turned_left = 0
        turned_right = 0
        gone_forward = [0]
        while found:
            if self.robot.color_sensor.color == ev3.ColorSensor.COLOR_WHITE:
                print('i see white')
                self.robot.not_go()
                gone_forward[len(gone_forward)] += 1
                self.robot.go_forward(300, 300)
                time.sleep(.5)

            if self.robot.color_sensor.color == ev3.ColorSensor.COLOR_BLACK:
                print('i see Black')
                self.robot.not_go()
                turned_left = 1
                turned_right = 0
                self.robot.turn_degrees(-90, 300)
                self.robot.go_forward(300,300)
                time.sleep(1)

            if self.robot.color_sensor.color == ev3.ColorSensor.COLOR_BLUE:
                print('i see Blue')
                self.robot.not_go()
                turned_right = 1
                turned_left = 0
                self.robot.turn_degrees(90, 300)
                self.robot.go_forward(300,300)
                time.sleep(1)

            if self.robot.color_sensor.color == ev3.ColorSensor.COLOR_RED:
                print('i see Red')
                self.robot.not_go()
                self.robot.seek_beacon()
                self.robot.arm_up()
                found = False

        while Run_away:
            for i in gone_forward:
                for k in range(i):
                    self.not_go()
                    self.robot.go_backwards(300,300)
                    time.sleep(.5)

                if turned_left == 1:
                    self.robot.turn_degrees(90,300)
                    turned_left=0
                    turned_right=1

                if turned_right == 1:
                    self.robot.turn_degrees(-90,300)
                    turned_left = 1
                    turned_right = 0

            self.robot.arm_down()



def main():
    print('maze solving program')
    ev3.Sound.speak('Maze Solver')

    robot = robo.Snatch3r()
    messages_from_pc = Messages_from_pc(robot)
    mqtt_client = com.MqttClient(messages_from_pc)
    mqtt_client.connect_to_pc()
    robot.loop_forever()




main()
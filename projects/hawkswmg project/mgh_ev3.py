"""Final Ev3 project for csse120 by Megan Hawksworth. This project is King
Kong themed. This file is the code that will run on the Ev3"""

import robot_controller as robo
import ev3dev.ev3 as ev3
import time
import mqtt_remote_method_calls as com


class DelegateEv3(object):
    """This delegate helps recieve messages from the ev3"""
    def __init__(self, robot):
        self.mqtt = com.MqttClient(self)
        self.robot = robot
        self.running = True

    def gorilla_noises(self):
        ev3.Sound.play("monkeys1.wav")

    def joke_king_kong(self):
        ev3.Sound.speak("What’s big and hairy and climbs up the Empire "
                        "State Building in a dress?").wait()
        time.sleep(2)
        ev3.Sound.speak("Queen Kong").wait()

    def climb_building(self):
        """Moves forward If close to an object, stops the robot and backs
        away. Gorilla noise? hawkswmg"""
        while True:
            self.robot.go_forward(200, 200)
            if self.robot.ir_sensor.proximity < 9:
                print("ev3 file. Too close")
                ev3.Sound.beep()
                self.robot.not_go()
                self.gorilla_noises()
                self.drive_inches(-2, 200)
                time.sleep(0.2)
                self.mqtt.send_message("hit_object")
                break
            if self.robot.color_sensor.color == ev3.ColorSensor.COLOR_BLACK:
                print("ev3 file. Sees black")
                ev3.Sound.beep()
                self.robot.not_go()
                self.gorilla_noises()
                self.drive_inches(-2, 200)
                time.sleep(0.2)
                self.mqtt.send_message("fall_off_building")
                break
            if self.robot.color_sensor.color == ev3.ColorSensor.COLOR_RED:
                print("ev3 file. Sees red")
                ev3.Sound.beep()
                while True:
                    if self.robot.color_sensor.color == ev3.ColorSensor.COLOR_RED:
                        self.robot.go_forward(200, 200)
                    if self.robot.color_sensor.color == ev3.ColorSensor.COLOR_WHITE:
                        print("see white")
                        self.robot.go_right(200)
                    if self.robot.color_sensor.color == ev3.ColorSensor.COLOR_BLUE:
                        print("see blue")
                        break
                self.robot.not_go()
                self.gorilla_noises()
                self.robot.arm_up()
                self.mqtt.send_message("at_the_top")
                break
            time.sleep(0.09)

    def end_the_rampage(self):
        self.mqtt.client.disconnect()
        ev3.Sound.speak("You will never stop me!")
        game_over(self.robot)

    # The files below are from the snatch3r file

    def go_forward(self, left_speed, right_speed):
        """Moves the robot forward given a positive speed for both the left
        and right motors. If the speeds are not the same, makes the robot
        arc."""
        self.robot.left_motor.run_forever(speed_sp=left_speed)
        self.robot.right_motor.run_forever(speed_sp=right_speed)

    def go_left(self, left_speed):
        """Makes the robot turn left with a given speed"""
        self.robot.left_motor.run_forever(speed_sp=-left_speed)
        self.robot.right_motor.run_forever(speed_sp=left_speed)

    def go_right(self, right_speed):
        """Makes the robot turn right with a given speed"""
        self.robot.left_motor.run_forever(speed_sp=right_speed)
        self.robot.right_motor.run_forever(speed_sp=-right_speed)

    def go_backwards(self, left_speed, right_speed):
        """Moves the robot backwards given a negative speed for both the left
                and right motors. If the speeds are not the same, makes the robot
                arc."""
        self.robot.left_motor.run_forever(speed_sp=-left_speed)
        self.robot.right_motor.run_forever(speed_sp=-right_speed)

    def not_go(self):
        """Stops the left and right motors bringing the robot to a stop"""
        self.robot.left_motor.stop(stop_action='brake')
        self.robot.right_motor.stop(stop_action='brake')

    def shutdown(self):
        """Stops all motors and turns off LEDs"""
        self.robot.arm_motor.stop(stop_action='brake')
        self.robot.left_motor.stop(stop_action='brake')
        self.robot.right_motor.stop(stop_action='brake')
        ev3.Leds.all_off()

    def drive_inches(self, inches_target, speed_deg_per_second):
        """ moves the robot by given speed for a given distance. Input
        positive speed to go forward and a negative speed to go backwards."""
        self.robot.left_motor.run_to_rel_pos(position_sp=inches_target * 90,
                                       speed_sp=speed_deg_per_second,
                                       stop_action='brake')
        self.robot.right_motor.run_to_rel_pos(position_sp=inches_target * 90,
                                        speed_sp=speed_deg_per_second,
                                        stop_action='brake')
        self.robot.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.robot.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def arm_up(self):
        """Moves arm up until touch sensor is pressed, then beeps"""
        self.robot.arm_motor.run_forever(speed_sp=900)
        while not self.robot.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.robot.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep()

    def arm_down(self):
        """Moves arm down to previously calibrated position"""
        self.robot.arm_motor.run_to_abs_pos(speed_sp=900)
        self.robot.arm_motor.wait_while(ev3.Motor.STATE_HOLDING)
        ev3.Sound.beep()


def main():
    ev3.Sound.speak("Welcome to King Kong's Adventure").wait()
    robot = robo.Snatch3r()
    mydelegate = DelegateEv3(robot)
    mydelegate.mqtt.connect_to_pc()
    robot.loop_forever()


def game_over(robot):
    dele = DelegateEv3(robot)
    dele.mqtt.connect_to_pc()
    end_btn = ev3.Button()
    end_btn.on_up = lambda state: btn_pressed(dele)
    end_btn.on_down = lambda state: btn_pressed(dele)
    end_btn.on_left = lambda state: btn_pressed(dele)
    end_btn.on_right = lambda state: btn_pressed(dele)
    while dele.running:
        end_btn.process()


def btn_pressed(dele):
    dele.robot.arm_down()
    ev3.Sound.speak("Godzilla was a better movie anyway").wait()
    dele.mqtt.send_message("the_end")
    dele.running = False


main()

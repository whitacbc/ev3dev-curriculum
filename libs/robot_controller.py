"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import time
import math
MAX_SPEED = 900


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many
    different programs."""

    def __init__(self):
        """ construct and store a left motor and a right motor."""
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        assert self.arm_motor.connected
        assert self.touch_sensor.connected
        assert self.left_motor.connected
        assert self.right_motor.connected
        self.color_sensor = ev3.ColorSensor()
        assert self.color_sensor
        self.ir_sensor = ev3.InfraredSensor()
        assert self.ir_sensor
        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        assert self.pixy
        self.running = True
        self.times_climbed = 0

    def drive_inches(self, inches_target, speed_deg_per_second):
        """ moves the robot by given speed for a given distance"""
        self.left_motor.run_to_rel_pos(position_sp=inches_target * 90,
                                       speed_sp=speed_deg_per_second,
                                       stop_action='brake')
        self.right_motor.run_to_rel_pos(position_sp=inches_target * 90,
                                        speed_sp=speed_deg_per_second,
                                        stop_action='brake')
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        """ turns the robot"""
        self.left_motor.run_to_rel_pos(position_sp=-degrees_to_turn * 4.45,
                                       speed_sp=turn_speed_sp,
                                       stop_action='brake')
        self.right_motor.run_to_rel_pos(position_sp=degrees_to_turn * 4.45,
                                        speed_sp=turn_speed_sp,
                                        stop_action='brake')
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def arm_calibration(self):
        self.arm_motor.run_forever(speed_sp=MAX_SPEED)
        while not self.touch_sensor:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep()

        arm_revolutions_for_full_range = 14.2
        self.arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep()
        self.arm_motor.position = 0  # Calibrate the down position as 0 (this line is correct as is).

    def arm_up(self):
        self.arm_motor.run_forever(speed_sp=MAX_SPEED)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep()

    def arm_down(self):
        self.arm_motor.run_to_abs_pos(speed_sp=MAX_SPEED)
        self.arm_motor.wait_while(ev3.Motor.STATE_HOLDING)
        ev3.Sound.beep()

    def shutdown(self):
        self.arm_motor.stop(stop_action='brake')
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')
        ev3.Leds.all_off()
        self.running = False

    def loop_forever(self):
        while self.running:
            time.sleep(0.1)

    def go_forward(self, left_speed, right_speed):
        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)

    def go_left(self, left_speed):
        self.left_motor.run_forever(speed_sp=-left_speed)
        self.right_motor.run_forever(speed_sp=left_speed)

    def go_right(self, right_speed):
        self.left_motor.run_forever(speed_sp=right_speed)
        self.right_motor.run_forever(speed_sp=-right_speed)

    def go_backwards(self, left_speed, right_speed):
        self.left_motor.run_forever(speed_sp=-left_speed)
        self.right_motor.run_forever(speed_sp=-right_speed)

    def not_go(self):
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')

    def seek_beacon(self):
        beacon_seeker = ev3.BeaconSeeker(channel=1)
        forward_speed = 300
        turn_speed = 100
        while True:
            current_heading = beacon_seeker.heading
            current_distance = beacon_seeker.distance
            if current_distance == -128:
                self.go_right(100)
            else:
                if math.fabs(current_heading) < 2:
                    print("On the right heading. Distance: ", current_distance)
                    self.go_forward(forward_speed, forward_speed)
                if math.fabs(current_heading) < 10 and math.fabs(
                        current_heading) > 2:
                    print("Adjusting heading: ", current_heading)
                    if current_heading < 0:
                        self.go_left(turn_speed)
                        time.sleep(0.5)
                    if current_heading > 0:
                        self.go_right(turn_speed)
                        time.sleep(0.5)

                if math.fabs(current_heading) > 10:
                    self.go_right(100)

                if current_distance == 1:
                    self.go_forward(300, 300)
                    time.sleep(1.5)
                    print('you have found the beacon!')
                    self.not_go()
                    what = True
                    break

            print(beacon_seeker.distance, beacon_seeker.heading)
            time.sleep(0.1)
        return what

    def climb_building(self):
        """Moves forward If close to an object, stops the robot and backs
        away. Gorilla noise? hawkswmg"""
        self.times_climbed += 1
        while True:
            self.go_forward(400, 400)
            if self.ir_sensor.proximity == 1:
                self.not_go()
                self.drive_inches(2, -200)
                break
            time.sleep(0.1)
        return self.times_climbed

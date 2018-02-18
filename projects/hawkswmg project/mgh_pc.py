"""Final Ev3 project for csse120 by Megan Hawksworth. This project is King
Kong themed. This file is the code that will run on the PC"""

import tkinter
from tkinter import ttk
from PIL import ImageTk, Image
import mqtt_remote_method_calls as com


class DelegatePC(object):
    """This delegate helps recieve messages from the ev3"""
    def __init__(self):
        self.mqtt = com.MqttClient(self)
        self.mqtt.connect_to_ev3()

    def hit_object(self):
        """Creates a new tkinter window that allows you to turn the robot
        adn continue forward after hitting an object"""
        self.mqtt.client.disconnect()
        print("hit_object")
        wall_crash()

    def fall_off_building(self):
        """Creates a new tkinter window that allows you to turn the robot
                and continue forward after reaching the edge of the given
                map (outlined in black)"""
        self.mqtt.client.disconnect()
        print("fall off")
        see_black()

    def at_the_top(self):
        """prints message and calls function game_over"""
        self.mqtt.client.disconnect()
        print("reached the top")
        game_over()

    def the_end(self):
        """Opens a window with an image and a quit button. Pressing the
        quit button brings you back the choice mode"""
        end_root = tkinter.Toplevel()
        end_root.title("Thanks for Playing")
        end_frame = ttk.Frame(end_root, padding=30)
        end_frame.pack()

        pic = "smile_kiko.jpg"
        img = ImageTk.PhotoImage(Image.open(pic))
        end_pic_label = tkinter.Label(end_frame, image=img)
        end_pic_label.pack()

        end_text = tkinter.Label(end_frame, text="Thanks for playing!",
                                                 font="Calibri")
        end_text.pack()
        end_btn = ttk.Button(end_frame, text="Quit")
        end_btn.pack(side="bottom")
        end_btn['command'] = lambda: quit_mode(self.mqtt, end_root)
        self.mqtt.connect_to_ev3()
        self.mqtt.send_message("shutdown")

        end_root.mainloop()


def main():
    """Gives introduction and the choice of story mode or sandbox mode"""
    root1 = tkinter.Tk()
    root1.title("Welcome to King Kong's Adventure")
    canvas1 = tkinter.Canvas(root1, height=20, relief='raised')
    canvas1.pack()
    intro = ttk.Label(root1, text="King Kong's Adventure!", font="Calibri")
    intro.pack()
    pic = r"C:\Users\hawkswmg.ROSE-HULMAN\Documents\CSSE120\ev3dev" \
          r"-curriculum\projects\hawkswmg project\king-kong 1.jpg"
    img = ImageTk.PhotoImage(Image.open(pic))
    panel = ttk.Label(root1, image=img, padding=20)
    panel.pack()
    start_canvas = tkinter.Canvas(root1, height=100, relief='raised')
    start_canvas.pack()
    intro_text = ttk.Label(start_canvas, text="Join the journey as the story "
                                             "of "
                                        "King Kong unfolds. ")
    intro_text.pack()
    start_btn = ttk.Button(start_canvas, text="Ready to begin?")
    start_btn.pack()
    start_btn['command'] = lambda: mode_choice_tab(root1)

    root1.mainloop()


def mode_choice_tab(root1):
    """Brings up the window to choose a mode"""
    dele = DelegatePC()

    root1.destroy()
    root2 = tkinter.Tk()
    root2.title("Make a choice")
    choice_frame = ttk.Frame(root2, padding=50, relief='raised')
    choice_frame.grid()
    choice_label = ttk.Label(choice_frame, text="How would you like to "
                                                "play?", font="Calibri",
                             padding=20)
    choice_label.grid()
    story_btn = ttk.Button(choice_frame, text="Story Mode", width=20,
                           padding=20)
    story_btn.grid(row=1)
    story_btn['command'] = lambda: story_mode(root2, dele.mqtt)
    sandbox_btn = ttk.Button(choice_frame, text="Sandbox Mode", padding=20,
                             width=20)
    sandbox_btn.grid(row=2)
    sandbox_btn['command'] = lambda: sandbox_mode(root2, dele.mqtt)

    root2.mainloop()


def story_mode(root, mqtt):
    """Sends the user into a stroy mode where the events are
 predetermined based on snippets of the movie"""
    root.withdraw()
    st_root = tkinter.Tk()
    st_root.title("King-Kong: Story mode")
    st_frame = ttk.Frame(st_root, padding=30)
    st_frame.grid()

    return_button = ttk.Button(st_frame, text="Quit")
    return_button.grid(row=0, column=2)
    return_button['command'] = lambda: quit_mode(mqtt, st_root)

    left_blank_space = ttk.Label(st_frame, text="           ", padding=20)
    left_blank_space.grid(row=0, column=0)

    sb_intro = ttk.Label(st_frame, text="Welcome to story mode!",
                         font="Calibri")
    sb_intro.grid(row=1, column=1)
    sb_option1 = ttk.Label(st_frame, text="In this mode you have one goal, "
                                         "to get to the top of the building "
                                         "where the maiden is.\nBut the "
                                         "poilce are trying to stop "
                                         "you! (Probably because you tried "
                                         "to demolish the city.)\nYou will "
                                         "start at the bottom of "
                                         "the building and have to options "
                                         "for scaling the building.",
                          padding=5)
    sb_option1.grid(row=2, column=1)
    sb_option2 = ttk.Label(st_frame, text="Option 1: Move forward")
    sb_option2.grid(row=3, column=1)
    climb_button = ttk.Button(st_frame, text="Climb the building!")
    climb_button.grid(row=4, column=1)
    climb_button['command'] = lambda: climb(mqtt, st_root)

    sb_intro3 = ttk.Label(st_frame, text="Option 2: Turn using the arrow "
                                         "keys (stop between commands using "
                                         "the space bar)", padding=5)
    sb_intro3.grid(row=5, column=1)

    st_root.bind('<Left>', lambda event: move_left(mqtt))
    st_root.bind('<Right>', lambda event: move_right(mqtt))
    st_root.bind('<space>', lambda event: stop(mqtt))

    st_root.mainloop()


def sandbox_mode(root, mqtt):
    """A free-for-all mode where the user is completely free to control the
    robot"""
    root.destroy()
    sb_root = tkinter.Tk()
    sb_root.title("King-Kong: Sandbox mode")
    sb_frame = ttk.Frame(sb_root, padding=30)
    sb_frame.grid()

    return_button = ttk.Button(sb_frame, text="Return")
    return_button.grid(row=0, column=2)
    return_button['command'] = lambda: quit_mode(mqtt, sb_root)
    left_blank_space = ttk.Label(sb_frame, text="           ", padding=20)
    left_blank_space.grid(row=0, column=0)

    sb_intro = ttk.Label(sb_frame, text="Welcome to sandbox mode!",
                         font="Calibri")
    sb_intro.grid(row=1, column=1)
    sb_intro1 = ttk.Label(sb_frame, text="In this mode, you can control the "
                                        "robot in any way you want!")
    sb_intro1.grid(row=2, column=1)
    sb_intro2 = ttk.Label(sb_frame, text="Nothing's stopping you from going "
                                        "on a rampage with robo King-Kong.")
    sb_intro2.grid(row=3, column=1)
    sb_intro3 = ttk.Label(sb_frame, text="First you might need a few "
                                        "directions for how to use robo "
                                         "King-Kong...")
    sb_intro3.grid(row=4, column=1)

    sb_direc = ttk.Label(sb_frame, text="How to use the robot:")
    sb_direc.grid(row=5, column=1)
    sb_movedirec = ttk.Label(sb_frame, text="Use the arrow keys to move the "
                                           "robot around", padding=5)
    sb_movedirec.grid(row=6, column=1)
    sb_armdirec = ttk.Label(sb_frame, text="Press the 'u' and 'd' buttons "
                                           "the move the robots arm")
    sb_armdirec.grid(row=7, column=1)
    sb_stopdirec = ttk.Label(sb_frame, text="Press the space bar between "
                                           "actions to stop the robot",
                             padding=5)
    sb_stopdirec.grid(row=8, column=1)

    sb_root.bind('<Up>', lambda event: move_forward(mqtt))
    sb_root.bind('<Down>', lambda event: move_backward(mqtt))
    sb_root.bind('<Left>', lambda event: move_left(mqtt))
    sb_root.bind('<Right>', lambda event: move_right(mqtt))
    sb_root.bind('<space>', lambda event: stop(mqtt))
    sb_root.bind('<u>', lambda event: arm_up(mqtt))
    sb_root.bind('<d>', lambda event: arm_down(mqtt))

    sb_noisedirec = ttk.Label(sb_frame, text="Use the buttons below to make "
                                             "robo King-Kong speak!")
    sb_panel = tkinter.Canvas(sb_root)
    sb_panel.grid()
    sb_noisedirec.grid(row=9, column=1)
    noise_button = ttk.Button(sb_panel, text="Noises")
    noise_button.grid(row=10, column=0)
    noise_button['command'] = lambda: make_noise(mqtt)
    quote_button = ttk.Button(sb_panel, text="King-Kong Joke")
    quote_button.grid(row=10, column=2)
    quote_button['command'] = lambda: joke(mqtt)

    btm_blank_space = ttk.Label(sb_panel, text="           ", padding=20)
    btm_blank_space.grid(row=11, column=0)

    sb_root.mainloop()


"""Below are the functions used in DelegatePC"""


def wall_crash():
    """When the robot sends signal, opens a window saying that there is a
    helicopter in the way. Gives options of turning (using arrow keys) or
    calling the climb_the_building function"""
    dele = DelegatePC()
    dele.mqtt.connect_to_ev3()
    hit_root = tkinter.Tk()
    hit_root.title("Watch where you are going!")
    hit_frame = ttk.Frame(hit_root, padding=30)
    hit_frame.grid()

    hit_text = tkinter.Label(hit_frame, text="There is a helicopter in the "
                                             "way!",
                             font="Calibri")
    hit_text.grid(row=1, column=1)
    return_button = ttk.Button(hit_frame, text="Quit")
    return_button.grid(row=0, column=2)
    return_button['command'] = lambda: quit_mode(dele.mqtt, hit_root)
    left_blank_space = ttk.Label(hit_frame, text="           ", padding=20)
    left_blank_space.grid(row=0, column=0)

    hit_direc1 = ttk.Label(hit_frame, text="Use the arrow keys to turn "
                                           "away from the object in front of"
                                           "you.")
    hit_direc1.grid(row=2, column=1)
    hit_direc2 = ttk.Label(hit_frame, text="Use the space bar to "
                                           "stop between actions.")
    hit_direc2.grid(row=3, column=1)
    hit_direc3 = ttk.Label(hit_frame, text="When you think you will head "
                                           "in a "
                                           "good direction, press the "
                                           "button below ")
    hit_direc3.grid(row=4, column=1)

    climb_btn = ttk.Button(hit_frame, text="Climb the building!")
    climb_btn.grid(row=5, column=1)
    climb_btn['command'] = lambda: climb(dele.mqtt, hit_root)

    hit_root.bind('<Left>', lambda event: move_left(dele.mqtt))
    hit_root.bind('<Right>', lambda event: move_right(dele.mqtt))
    hit_root.bind('<space>', lambda event: stop(dele.mqtt))

    hit_root.mainloop()


def see_black():
    """When the robot sends signal, opens a window saying that you are
    about to fall off the building. Gives options of turning (using arrow
    keys) or calling the climb_the_building function"""
    dele = DelegatePC()
    dele.mqtt.connect_to_ev3()

    fall_root = tkinter.Tk()
    fall_root.title("Watch where you are going!")
    fall_frame = ttk.Frame(fall_root, padding=30)
    fall_frame.grid()

    fall_text = tkinter.Label(fall_frame, text="You are about to fall "
                                               "off the building!",
                              font="Calibri")
    fall_text.grid(row=1, column=1)
    return_button = ttk.Button(fall_frame, text="Quit")
    return_button.grid(row=0, column=2)
    return_button['command'] = lambda: quit_mode(dele.mqtt, fall_root)
    left_blank_space = ttk.Label(fall_frame, text="           ",
                                 padding=20)
    left_blank_space.grid(row=0, column=0)

    fall_direc1 = ttk.Label(fall_frame, text="Use the arrow keys to turn "
                                             "away from the object in front of"
                                             "you.")
    fall_direc1.grid(row=2, column=1)
    fall_direc2 = ttk.Label(fall_frame, text="Use the space bar to "
                                             "stop between actions.")
    fall_direc2.grid(row=3, column=1)
    fall_direc3 = ttk.Label(fall_frame, text="When you think you will "
                                             "head in a "
                                             "good direction, press the "
                                             "button below ")
    fall_direc3.grid(row=4, column=1)

    climb_btn = ttk.Button(fall_frame, text="Climb the building!")
    climb_btn.grid(row=5, column=1)
    climb_btn['command'] = lambda: climb(dele.mqtt, fall_root)

    fall_root.bind('<Left>', lambda event: move_left(dele.mqtt))
    fall_root.bind('<Right>', lambda event: move_right(dele.mqtt))
    fall_root.bind('<space>', lambda event: stop(dele.mqtt))

    fall_root.mainloop()


def game_over():
    """When the robot sends signal, opens a window that tells you that you
    have found the maiden and reached the top of the building. When OK is
    clicked sends message "end the rampage" to the robot"""
    dele = DelegatePC()
    dele.mqtt.connect_to_ev3()

    top_root = tkinter.Tk()
    top_root.title("You Made it!")
    top_frame = ttk.Frame(top_root, padding=30)
    top_frame.grid()

    top_text = tkinter.Label(top_frame, text="Congratulations! You made "
                                             "it!!",
                             font="Calibri")
    top_text.grid(row=1, column=1)
    top_button = ttk.Button(top_frame, text="Quit")
    top_button.grid(row=0, column=2)
    top_button['command'] = lambda: quit_mode(dele.mqtt, top_root)
    left_blank_space = ttk.Label(top_frame, text="           ",
                                 padding=20)
    left_blank_space.grid(row=0, column=0)

    top_direc1 = ttk.Label(top_frame, text="You found the maiden "
                                           "at the top of "
                                           "the building!")
    top_direc1.grid(row=2, column=1)
    top_direc2 = ttk.Label(top_frame, text="But, like all stories this "
                                           "one must reach it's end.")
    top_direc2.grid(row=3, column=1)
    top_direc3 = ttk.Label(top_frame, text="In  order to stop King "
                                           "Kong's rampage, hit one of "
                                           "the buttons on the robot ")
    top_direc3.grid(row=4, column=1)
    ok_btn = ttk.Button(top_frame, text="OK")
    ok_btn.grid(row=5, column=1)
    ok_btn['command'] = lambda: dele.mqtt.send_message("end_the_rampage")

    top_root.mainloop()


"""The functions below are the handles on the buttons used in both modes"""


def move_forward(mqttclient):
    """Sends a message for the robot to go forward"""
    print("forward")
    mqttclient.send_message("go_forward", (300, 300))


def move_backward(mqttclient):
    """Sends a message for the robot to go backward"""
    print("backward")
    mqttclient.send_message("go_backwards", (300, 300))


def move_left(mqttclient):
    """Sends a message for the robot to turn left"""
    print("left")
    mqttclient.send_message("go_left", [300])


def move_right(mqttclient):
    """Sends a message for the robot to turn right"""
    print("right")
    mqttclient.send_message("go_right", [300])


def stop(mqttclient):
    """Sends a message for the robot to stop"""
    print("stop")
    mqttclient.send_message("not_go")


def make_noise(mqttclient):
    """Sends a message for the robot to make gorilla noises"""
    print("noise")
    mqttclient.send_message("gorilla_noises")


def joke(mqttclient):
    """Sends a message for the robot to say a king kong quote"""
    print("joke")
    mqttclient.send_message("joke_king_kong")


def arm_up(mqttclient):
    """Sends a message for the robot to lift its arm"""
    print("arm_up")
    mqttclient.send_message("arm_calibration")
    mqttclient.send_message("arm_up")


def arm_down(mqttclient):
    """Sends a message for the robot to lower its arm"""
    print("arm_down")
    mqttclient.send_message("arm_down")


def quit_mode(mqttclient, root):
    """Sends a message for the robot to stop all motors and noises. It also
    opens the choice window"""
    mqttclient.send_message("shutdown")
    mode_choice_tab(root)


def climb(mqttclient, root):
    """Sends a message for the robot to use the command climb_building from
    robot controller. It also removes the current tkinter window"""
    mqttclient.send_message("climb_building")
    root.destroy()


main()

"""Final Ev3 project for csse120 by Megan Hawksworth. This project is King
Kong themed. This file is the code that will run on the PC"""

import tkinter
from tkinter import ttk
from PIL import ImageTk, Image
import mqtt_remote_method_calls as com


class DelegatePC(object):
    """This delegate helps recieve messages from the ev3"""
    def __init__(self):
        self.mqtt = com.MqttClient()
        self.mqtt.connect_to_ev3()


def main():
    """Gives introduction and the choice of story mode or sandbox mode"""
    root1 = tkinter.Tk()
    root1.title("Welcome to King Kong's Adventure")
    canvas1 = tkinter.Canvas(root1, height=20, relief='raised')
    canvas1.pack()
    intro = ttk.Label(root1, text="King Kong's Adventure!", font="Calibri")
    intro.pack()
    pic = r"C:\Users\hawkswmg.ROSE-HULMAN\Documents\CSSE120\ev3dev" \
          r"-curriculum" \
          "\libs\king-kong 1.jpg"
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
    story_btn['command'] = lambda: story_mode(root2)
    sandbox_btn = ttk.Button(choice_frame, text="Sandbox Mode", padding=20,
                             width=20)
    sandbox_btn.grid(row=2)
    sandbox_btn['command'] = lambda: sandbox_mode(root2)

    root2.mainloop()


def story_mode(root):
    """Sends the user into a stroy mode where the events are
 prede termined based on snippets of the movie"""
    root.destroy()


def sandbox_mode(root):
    """A free-for-all mode where the user is completely free to control the
    robot"""
    root.destroy()
    mydelegate = DelegatePC()
    sb_root = tkinter.Tk()
    sb_root.title("King-Kong: Sandbox mode")
    sb_frame = ttk.Frame(sb_root, padding=30)
    sb_frame.grid()

    return_button = ttk.Button(sb_frame, text="Return")
    return_button.grid(row=0, column=2)
    return_button['command'] = lambda: mode_choice_tab(sb_root)
    left_blank_space = ttk.Label(sb_frame, text="           ", padding=20)
    left_blank_space.grid(row=0, column=0)

    sb_intro = ttk.Label(sb_frame, text="Welcome to sandbox mode!")
    sb_intro.grid(row=1, column=1)
    sb_intro1 = ttk.Label(sb_frame, text="In this mode, you can control the "
                                        "robot in any way you want! ")
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
    sb_stopdirec = ttk.Label(sb_frame, text="Press the space bar between "
                                           "actions to stop the robot",
                             padding=10)
    sb_stopdirec.grid(row=7, column=1)

    sb_root.bind('<Up>', lambda event: move_forward(mydelegate.mqtt))
    sb_root.bind('<Down>', lambda event: move_backward(mydelegate.mqtt))
    sb_root.bind('<Left>', lambda event: move_left(mydelegate.mqtt))
    sb_root.bind('<Right>', lambda event: move_right(mydelegate.mqtt))
    sb_root.bind('<space>', lambda event: stop(mydelegate.mqtt))

    sb_noisedirec = ttk.Label(sb_frame, text="Use the buttons below to make "
                                             "robo King-Kong speak!")
    sb_panel = tkinter.Canvas(sb_root)
    sb_panel.grid()
    sb_noisedirec.grid(row=7, column=1)
    noise_button = ttk.Button(sb_panel, text="Noises")
    noise_button.grid(row=8, column=0)
    noise_button['command'] = lambda: make_noise(mydelegate.mqtt)
    quote_button = ttk.Button(sb_panel, text="Quote King-Kong")
    quote_button.grid(row=8, column=2)
    quote_button['command'] = lambda: quote(mydelegate.mqtt)

    btm_blank_space = ttk.Label(sb_panel, text="           ", padding=20)
    btm_blank_space.grid(row=9, column=0)


# The functions below are the handles on the buttons from sandbox_mode


def move_forward(mqttclient):
    print("forward")
    mqttclient.send_message("go_forward", (300, 300))


def move_backward(mqttclient):
    print("backward")
    mqttclient.send_message("go_backwards", (300, 300))


def move_left(mqttclient):
    print("left")
    mqttclient.send_message("go_left", [300])


def move_right(mqttclient):
    print("right")
    mqttclient.send_message("go_right", [300])


def stop(mqttclient):
    print("stop")
    mqttclient.send_message("not_go")


def make_noise(mqttclient):
    print("noise")
    mqttclient.send_message("gorilla_noises")


def quote(mqttclient):
    print("quote")
    mqttclient.send_message("quote_King-Kong")


main()

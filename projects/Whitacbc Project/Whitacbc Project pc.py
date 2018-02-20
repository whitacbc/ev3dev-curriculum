'''
Temple Run v0.9
'''

import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


class PC_deligate(object):
    def __init__(self, Message_Label):
        self.display_label = Message_Label


def Main_Menu(mqtt_client):
    root = tkinter.Tk()
    root.title('MAIN MENU')

    main_frame = ttk.Frame(root,padding=10, relief='raised')
    main_frame.grid()

    simpletxt = ttk.Label(main_frame, text="Temple Run")
    simpletxt.grid(row=0)

    quit_button = ttk.Button(main_frame, text='Quit')
    quit_button.grid(row=2, column=1)
    quit_button['command'] = lambda: root.destroy()


    enter_button = ttk.Button(main_frame, text="Enter the Temple")
    enter_button.grid(row=2, column=0)
    enter_button['command'] = lambda: change_to_story(mqtt_client,root)

    root.mainloop()
def change_to_story(mqtt_client,root):

    root.destroy()
    story(mqtt_client)



def story(mqtt_client):
    root = tkinter.Tk()
    root.title('Story Time')

    main_frame = ttk.Frame(root, padding=50, relief='raised')
    main_frame.grid()

    story_text = ttk.Label(root,text= 'The date is 20**, Bitcoin crashed from $22,000 to $15 in two hours and the world'
                                  ' fell apart into a hell like\n landscape. Your name is Guy Dangerous and you have'
                                  ' searched your whole life for an ancient artifact\nso that he would have enough'
                                  ' money to pay off the loan he took out to pay for one bitcoin.\nToday is your lucky'
                                  'day you have finaly found a rare artifact that will make you richer than your '
                                  'wildest dreams.\nBut between you and your dreams lies a dangours maze that only a '
                                  'robot can get through')

    story_text.grid(row=0, column=1)

    next_butten = ttk.Button(root, text= 'Next')
    next_butten.grid(row=1, column= 2)
    next_butten['command'] = lambda: to_choose_setting_screen(mqtt_client,root)

    Go_back = ttk.Button( root, text = 'Go Back')
    Go_back.grid(row=1,column=0)
    Go_back['command'] = lambda: go_back_to_main(mqtt_client,root)

    root.mainloop()

def go_back_to_main(mqtt_client,root):
    root.destroy()
    Main_Menu(mqtt_client)

def to_choose_setting_screen(mqtt_client,root):
    root.destroy()
    choose_setting(mqtt_client)

def choose_setting(mqtt_client):
    root = tkinter.Tk()
    root.title('Instructions')

    main_frame = ttk.Frame(root, padding=15, relief='raised')
    main_frame.grid()

    more_text = ttk.Label(main_frame, text='Please choose a game mode')
    more_text.grid(row=0)

    autonomous_mode = ttk.Button(main_frame, text='Autonomous Mode',padding=20)
    autonomous_mode['command'] = lambda: change_to_autonomous(mqtt_client,root)
    autonomous_mode.grid(row=1)

    Manual_drive = ttk.Button(main_frame, text='Manual Challenge',padding=20)
    Manual_drive['command'] = lambda: change_to_manual(mqtt_client,root)
    Manual_drive.grid(row=2)

def change_to_autonomous(mqtt_client,root):
    root.destroy()
    Autonomous(mqtt_client)

def change_to_manual(mqtt_client,root):
    root.destroy()
    Manual(mqtt_client)

def Autonomous(mqtt_client):
    root = tkinter.Tk()
    root.title('Autonomous mode')

    main_frame = ttk.Frame(root , padding=50, relief='raised')
    main_frame.grid()

    top_text = ttk.Label(main_frame, text='autonomous mode is now enabled\nplease watch the robot')
    top_text.grid()

    mqtt_client.send_message('speak_message',['Looking for clues'])
    mqtt_client.send_message('go_forward', [300, 300])
    mqtt_client.send_message('Searching')


def Manual(mqtt_client):
    root = tkinter.Tk()
    root.title('Manual Robot Control')
    mqtt_client.send_message('start_manual')

    main_frame = ttk.Frame(root, padding=50, relief='raised')
    main_frame.grid()

    label = ttk.Label(main_frame,text='Manual driving mode')
    label.grid(column=1,row=0)

    up_button = ttk.Button(main_frame,text='UP',padding=20)
    up_button['command'] = lambda: mqtt_client.send_message("go_forward",[600,600])
    root.bind('<w>', lambda event: mqtt_client.send_message("go_forward",[600,600]))
    up_button.grid(column=1,row=1)

    down_button = ttk.Button(main_frame,text='Down',padding=20)
    down_button['command'] = lambda: mqtt_client.send_message('go_backwards',[600,600])
    root.bind('<s>', lambda event: mqtt_client.send_message("go_backwards", [600,600]))
    down_button.grid(row=3,column=1)

    right_button = ttk.Button(main_frame,text='Right',padding=20)
    right_button['command']= lambda: mqtt_client.send_message('go_right', [600])
    root.bind('<d>', lambda event: mqtt_client.send_message("go_right", [600]))
    right_button.grid(column=3,row=2)

    left_button = ttk.Button(main_frame,text='Left',padding=20)
    left_button['command'] = lambda: mqtt_client.send_message('go_left', [600])
    root.bind('<a>', lambda event: mqtt_client.send_message("go_left", [600]))
    left_button.grid(column=0,row=2)

    stop_button = ttk.Button(main_frame,text='STOP', padding=20)
    stop_button['command']= lambda: mqtt_client.send_message('not_go')
    root.bind('<space>', lambda event: mqtt_client.send_message("not_go"))
    stop_button.grid(column=1,row=2)

    Arm_Up_button = ttk.Button(main_frame,text='Arm Up',padding=20)
    Arm_Up_button['command']=lambda: mqtt_client.send_message('arm_up')
    root.bind('<r>', lambda event: mqtt_client.send_message("arm_up"))
    Arm_Up_button.grid(column=5,row=1)

    Arm_down_button = ttk.Button(main_frame,text='Arm Down',padding=20)
    Arm_down_button['command']=lambda: mqtt_client.send_message('arm_down')
    root.bind('<f>', lambda event: mqtt_client.send_message('arm_down'))
    Arm_down_button.grid(column=5,row=3)

    Arm_calabrate_button = ttk.Button(main_frame,text='Arm Calibration',padding=20)
    Arm_calabrate_button['command']=lambda: mqtt_client.send_message('arm_calibration')
    Arm_calabrate_button.grid(column=5,row=2)

def main():

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    Main_Menu(mqtt_client)


main()
import random
from PIL import Image
import pyautogui as pya
import cv2
import pytesseract
import re
import keyboard
import time
from datetime import datetime, timedelta
import threading
import multiprocessing
import numpy as np
import tkinter as tk
import sys
from tkinter import scrolledtext
import os
from PIL import Image, ImageTk, ImageOps
import telegram
import asyncio
## Currently not developed
card_type = "Normal"
## END DEV


long_session= "long_session"  # anti bot detection for long sessions but runs slower
## MODES
# set ONLY ONE of these to true at a time
only_sell = "only_sell" # always sells the players
only_buy = "only_buy" # stores all in the club
KRSU = "KRSU" # keep rares sell uncommons
## END MODES


account_id = 'account_id'
bot_id = 'bot_id'
text_noti = 'text_noti'

#pytesseract exe location
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#initialize global variables and counters
general_time_mult = 'general_time_mult'
time_to_load_search = "time_to_load_search"
max_loops = 'max_loops'  # max amount of searches the code will do
resolution_1440 = 'resolution_1440'  # resolution of main monitor with web app
resolution_1080 = 'resolution_1080'
buy_limit = 'buy_limit'  # set max amount of cards to snipe
current_price = 'current_price'  # the price you want to sell at
total_spent = 0
total_earned = 0
searches = 0
bought = 0
transfer_list = 0
missed = 0
total_loops = 0
modes = 0
long_session_count = 0
start_time = time.time()
buy_time = None
TL_clears = 0
purchases = []
script_running = False
paused = False
loop_count = 0
random_int = 0.5
script_running_lock = threading.Lock()
krsu_keeps = 0
krsu_max_keeps = "krsu_max_keeps"
unchecked_image = Image.open('check.png')
checked_image = Image.open('unchecked.png')
checked_image = checked_image.resize((16, 16))
unchecked_image = unchecked_image.resize((15, 15))
random_rest = 0
random_rest_time = 0

def past_input_reader(variables):
    for variable in variables:
        try:
            with open(f'{variable}.txt') as file:
                value = file.read()
                if value.lower() == "true" or value.lower() == "false":
                    value = True if value.lower() == "true" else False
                elif value.isnumeric():
                    value = int(value)
                else:
                    value = str(value)
                globals()[variable] = value
                print(f"{variable} updated to {value}")
        except FileNotFoundError:
            print(f"File not found for variable: {variable}")
        except ValueError:
            print(f"Invalid value in file for variable: {variable}")




def update_current_price():
    global current_price, current_price_real_str, current_price_str
    current_price_real_str = str(current_price)
    if int(current_price) < 1000:
        current_price_str = int(current_price) - 50
    else:
        current_price_str = int(current_price) - 100
    current_price_str = str(current_price_str)


class OutputRedirector:
    def __init__(self, output_area):
        self.output_area = output_area

    def write(self, text):
        self.output_area.insert(tk.END, text)
        self.output_area.see(tk.END)
        self.output_area.update_idletasks()

    def flush(self):
        pass

def run_script(output_area, general_time_mult, time_to_load_search):
    # Redirect standard output to the OutputRedirector object
    print("running script")
    # Call your main function here (replace 'your_main_function' with the actual function name)
    runner(general_time_mult, time_to_load_search)


def run_script_in_thread(output_area, general_time_mult, time_to_load_search):
    try:
        # Acquire the lock to ensure that only one thread is started at a time
        script_running_lock.acquire()
        # Set the global variable to indicate that the script is running
        script_running = True

        print("Starting new thread")
        threading.Thread(target=run_script, args=(output_area, general_time_mult, time_to_load_search)).start()
    except Exception as e:
        print(f"Exception in run_script_in_thread: {e}")
        # Release the lock in case an exception occurs
        script_running_lock.release()
        script_running = False
    else:
        # Release the lock if the thread starts successfully
        script_running_lock.release()


def add_option(frame, label_text, button_text, update_function, initial_value=None):
    option_label = tk.Label(frame, text=label_text, font=("Arial Black", 21), fg="#F8EEC9", bg='#302B27')
    option_label.pack(side=tk.LEFT, padx=0, pady=0)

    option_entry = tk.Entry(frame, bg='#211D1A', fg='#F8EEC9', font=("Arial", 26, "bold"), width=16)
    if initial_value is not None:
        option_entry.insert(0, initial_value)
    option_entry.pack(side=tk.LEFT, padx=0, pady=0)

    option_button = tk.Button(frame, text=button_text, font=("Arial Black", 14), bg='#E9DFCD', fg="#F65624", command=lambda: update_function(option_entry.get()))
    option_button.pack(side=tk.LEFT, padx=0, pady=0)

    return option_label, option_entry


def update_int(value, variable):
    globals()[variable]
    try:
        value = int(value)
        print(f"{variable} updated to {value}")
        with open(f"{variable}.txt", "w") as file:
            file.write(str(value))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
    variable = value


def update_float(value, variable):
    try:
        value = float(value)
        print(f"{variable} updated to {value}")
        with open(f"{variable}.txt", "w") as file:
            file.write(str(value))
        globals()[variable] = value  # assign the updated value to the global variable
    except ValueError:
        print("Invalid input. Please enter a valid number.")


def update_bool(value, variable):
    globals()[variable]
    print(f"{variable} updated to {value}")

    # Save the value to a text file
    with open(f"{variable}.txt", "w") as file:
        file.write(str(value))
    variable = value

def add_boolean_option(parent, variable_name, text, update_function):

    var = tk.BooleanVar()
    var.set(globals()[variable_name])
    var.trace("w", lambda *args: update_function(var.get(), variable_name))

    # Create custom checkbox icons with green check mark and gray X mark
    checked_icon = ImageTk.PhotoImage(checked_image)
    unchecked_icon = ImageTk.PhotoImage(unchecked_image)

    check_button = tk.Checkbutton(parent, text=text, bg='#302B27', fg='#A09787', font=("Arial Black", 13), variable=var,
                                  onvalue=True, offvalue=False, selectcolor="#302B27", activebackground="#302B27",
                                  highlightthickness=0, borderwidth=0, indicatoron=False, image=checked_icon,
                                  compound="left", selectimage=unchecked_icon)
    check_button.checked_icon = checked_icon
    check_button.unchecked_icon = unchecked_icon
    check_button.pack(padx=0, pady=0)
    return check_button

def read_saved_values(variables):
    for variable_name in variables:
        try:
            with open(f"{variable_name}.txt", "r") as file:
                value = file.read().strip().lower()
                if value == "true":
                    value = True
                elif value == "false":
                    value = False
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        value = float(value)
                globals()[variable_name] = value
        except FileNotFoundError:
            globals()[variable_name] = "Please enter value"


def create_gui():
    print("Creating GUI window...")
    option_frames = {}

    def add_option_int(variable_name, label_text, button_text, update_function):
        frame = tk.Frame(root, bg='#1E242A')
        frame.pack(padx=0, pady=0)
        initial_value = globals()[variable_name]
        option_label, option_entry = add_option(frame, label_text, button_text, update_function,
                                                initial_value=initial_value)
        option_label.config(width=20, anchor="w", padx=10)

    def add_option_float(variable_name, label_text, button_text, update_function):
        frame = tk.Frame(root, bg='#1E242A')
        frame.pack(padx=0, pady=0)
        initial_value = globals()[variable_name]
        option_label, option_entry = add_option(frame, label_text, button_text, update_function,
                                                initial_value=initial_value)
        option_label.config(width=20, anchor="w", padx=10)

    def update_bool(value, variable):
        print(f"{variable} updated to {value}")
        with open(f"{variable}.txt", "w") as file:
            file.write(str(value))


    root = tk.Tk()
    root.configure(background='#302B27')
    root.title("Sniper No Sniping!!!")


    frame = tk.Frame(root, bg='#1E242A')
    frame.pack(padx=0, pady=0)

    mode_label = tk.Label(frame, text="SNIPER NO SNIPING", font=("Arial Black", 30, "bold"), bg='#302B27', fg="#F8EEC9")
    mode_label.pack(side="top")

    instructions = ["1} \nTo run the sniper, click on the scope at the bottom of the application\n\n"
                    "2} \nShortly hold the 'pause' button on the keyboard (to the right of the F keys) to immediately halt the program\n\n",
                    "3} \nTo pause the program for 20 seconds after the current search is concluded, hold '-' until the search is done\n\n",
                    "4} \nTo halt the program after the current search is done, hold '=' until the search is finished\n\n",
                    "5} \nThe 'Max Keeps' option is only important if you are running in 'Keep Rares Sell Uncommons' mode\n\n",
                    "6} \nThe 'Long Session' option adds more puases to prevent soft bans from too many searches or too many purchases (useful for overnight sessions!)\n\n",
                    "7} \nThe 'General Time Multiplier' adds a bit of delay to every click in case you find it clicking too slow (1 is default, can go less than 1)\n\n",
                    "8} \nThe 'Time To Load Search' button only changes the time that the program waits after it clicks the search button"]

    # Concatenate the instructions with newlines to create the text to display
    instructions_text = "\n".join(instructions)

    # Create a Text widget to display the instructions
    # Create a frame to hold the label and the text widget
    frame = tk.Frame(root, bg='#302B27')
    frame.pack(side=tk.LEFT, padx=0, pady=0)

    # Add the label to the frame
    mode_label = tk.Label(frame, text="INSTRUCTIONS:", bg='#302B27', fg="#F8EEC9",width=17, font=("Arial Black", 21, "bold"))
    mode_label.pack(side='top', anchor=tk.W)

    # Add the text widget to the frame
    instructions_display = tk.Text(frame, bg='#1E242A', fg="#F8EEC9", height=40, width=60, wrap=tk.WORD)
    instructions_display.insert(tk.END, instructions_text)
    instructions_display.pack(side=tk.TOP, padx=0, pady=0)

    spacer = tk.Frame(frame, height=80, bg='#302B27')
    spacer.pack()

    mode_label = tk.Label(frame, text="OUTPUT:", font=("Arial Black", 21, "bold"), bg='#302B27', fg="#F8EEC9")
    mode_label.pack(side="top", anchor=tk.W)

    output_area = scrolledtext.ScrolledText(frame, bg='#1E242A',fg='#F8EEC9', wrap=tk.WORD, width=50, height=10)
    output_area.pack(side=tk.LEFT, padx=0, pady=0, fill=tk.BOTH, expand=True)
    sys.stdout = OutputRedirector(output_area)

    variables_to_load = ["only_sell", "only_buy", "KRSU", "buy_limit", "max_loops", "current_price", "resolution_1080", "text_noti", "resolution_1440", "krsu_max_keeps", "long_session", "general_time_mult", "time_to_load_search"]

    read_saved_values(variables_to_load)

    spacer = tk.Frame(root, height=30, bg='#302B27')
    spacer.pack()

    add_option_int("buy_limit", "Buy Limit:", "Update", lambda value: update_int(value, "buy_limit"))

    spacer = tk.Frame(root, height=30, bg='#302B27')
    spacer.pack()

    add_option_int("max_loops", "Search Limit:", "Update", lambda value: update_int(value, "max_loops"))

    spacer = tk.Frame(root, height=30, bg='#302B27')
    spacer.pack()

    add_option_int("current_price", "Sell Price:", "Update", lambda value: update_int(value, "current_price"))

    spacer = tk.Frame(root, height=30, bg='#302B27')
    spacer.pack()

    add_option_int("krsu_max_keeps", "Max Keeps:", "Update", lambda value: update_int(value, "krsu_max_keeps"))

    spacer = tk.Frame(root, height=30, bg='#302B27')
    spacer.pack()

    add_option_float("general_time_mult", "General Time Multiplier:", "Update", lambda value: update_float(value, "general_time_mult"))

    spacer = tk.Frame(root, height=30, bg='#302B27')
    spacer.pack()

    add_option_float("time_to_load_search", "Time To Load Search:", "Update", lambda value: update_float(value, "time_to_load_search"))

    spacer = tk.Frame(root, height=30, bg='#302B27')
    spacer.pack()

    left_frame = tk.Frame(root, bg="#302B27")
    left_frame.pack(side="left", padx=70)

    mode_label = tk.Label(left_frame, text="MODES:", font=("Arial Black", 21, "bold"), bg='#302B27', fg="#F8EEC9")
    mode_label.pack(side="top")

    info_label = tk.Label(left_frame, text="(only one may be selected)", font=("Arial Black", 10), bg='#302B27', fg="#AC0D53")
    info_label.pack(side="top")

    only_sell_button = add_boolean_option(left_frame, "only_sell", "Only Sell", update_bool)

    only_buy_button = add_boolean_option(left_frame, "only_buy", "Only Buy", update_bool)

    KRSU_button = add_boolean_option(left_frame, "KRSU", "Keep Rares Sell Uncommons", update_bool)

    spacer = tk.Frame(root, height=30, bg='#302B27')
    spacer.pack()

    right_frame = tk.Frame(root, bg="#302B27")
    right_frame.pack(side="right", padx=70, pady=10)

    mode_label = tk.Label(right_frame, text="RESOLUTION:", bg='#302B27', font=("Arial Black", 21, "bold"), fg="#F8EEC9")
    mode_label.pack(side="top")

    # create the second label with bold black text
    info_label = tk.Label(right_frame, text=" (only one may be selected)", bg='#302B27', font=("Arial Black", 10), fg="#AC0D53")
    info_label.pack(side="top")

    button_1080 = add_boolean_option(right_frame, "resolution_1080", "1080P", update_bool)

    button_1440 = add_boolean_option(right_frame, "resolution_1440", "1440P", update_bool)

    spacer = tk.Frame(right_frame, height=30, bg='#302B27')
    spacer.pack()

    spacer = tk.Frame(right_frame, height=30, bg='#302B27')
    spacer.pack()

    spacer = tk.Frame(root, height=10, bg='#302B27')
    spacer.pack()

    mode_label = tk.Label(root, text="OTHER:", bg='#302B27', font=("Arial Black", 21, "bold"), fg="#F8EEC9")
    mode_label.pack()

    button_long_session = add_boolean_option(root, "long_session", "Long Session", update_bool)

    button_text_notis = add_boolean_option(root, "text_noti", "Text Notifications", update_bool)

    # frame = tk.Frame(root, bg='#302B27')
    # frame.pack(padx=0, pady=0, side='bottom')
    #
    # spacer = tk.Frame(frame, height=20, bg='#302B27')
    # spacer.pack()

    spacer = tk.Frame(right_frame, height=100, bg='#302B27')
    spacer.pack()

    spacer = tk.Frame(right_frame, height=75, bg='#302B27')
    spacer.pack(side='bottom')

    spacer = tk.Frame(left_frame, height=130, bg='#302B27')
    spacer.pack()

    spacer = tk.Frame(left_frame, height=40, bg='#302B27')
    spacer.pack(side='bottom')

    spacer = tk.Frame(root, height=100, bg='#302B27')
    spacer.pack()

    sniping_pic = Image.open('snipe_coins.png')
    sniping_pic_tk = ImageTk.PhotoImage(sniping_pic)

    run_button = tk.Button(root, image=sniping_pic_tk, bg="#33353C", command=lambda: run_script_in_thread(output_area, general_time_mult, time_to_load_search), width=200, height=200)
    run_button.pack(padx=0, pady=0)

    arrow = Image.open('arrow_point.png')
    arrow = arrow.resize((100, 60))
    arrow_left = ImageOps.mirror((arrow))
    arrow_tk = ImageTk.PhotoImage(arrow)
    arrow_left_tk = ImageTk.PhotoImage(arrow_left)

    info_label = tk.Label(left_frame,image=arrow_tk, text="START SNIPIN' ", compound=tk.RIGHT, font=("Arial Black", 30), bg='#302B27', fg="#5fa4ab")
    info_label.pack(side="bottom")

    info_label = tk.Label(right_frame,image=arrow_left_tk, text="START SNIPIN'", compound=tk.LEFT, font=("Arial Black", 30), bg='#302B27', fg="#5fa4ab")
    info_label.pack(side="bottom")

    root.mainloop()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def image_loader():
    rare_png = Image.open(resource_path('rare.png'))
    dupe_png = Image.open(resource_path('dupe.png'))
    failed_img = Image.open(resource_path('fail.png'))
    no_res_img = Image.open(resource_path('no_res.png'))
    won_bid_img = Image.open(resource_path('won_bid.png'))
    soft_png = Image.open(resource_path('soft_banned.png'))
    team_png = Image.open(resource_path('team.png'))
    open_fifa_png = Image.open(resource_path('open_fifa.png'))
    launch_fifa_png = Image.open(resource_path('launch_fifa.png'))
    in_fifa_png = Image.open(resource_path('in_fifa.png'))
    cont_local_png = Image.open(resource_path('cont_local.png'))
    no_res_img_1080 = Image.open(('no_res_1080.png'))
    failed_img_1080 = Image.open(('fail_1080.png'))
    won_bid_img_1080 = Image.open(('won_bid_1080.png'))
    dupe_png_1080 = Image.open(('dupe_1080.png'))

    return rare_png,dupe_png,failed_img,no_res_img,won_bid_img,soft_png,team_png,open_fifa_png,launch_fifa_png,in_fifa_png,cont_local_png, no_res_img_1080, failed_img_1080, won_bid_img_1080, dupe_png_1080

def max_search_check():
    global max_loops, total_loops
    if total_loops >= max_loops + 1:
        print('reached max iterations')
        sys.exit(1)

def ensure_mode_selection():
    global only_buy, only_sell, KRSU
    modes = sum(int(val) for val in [only_buy, only_sell, KRSU])
    if modes != 1:
        print(f'must turn on exactly one mode at a time! Currently {modes} modes are turned on')
        sys.exit(1)

def ensure_resolution():
    global resolution_1080, resolution_1440
    resolution = sum(int(val) for val in [resolution_1440, resolution_1080])
    if resolution != 1:
        print(f'must turn on exactly one resolution at a time! Currently {resolution} resolutions are turned on')
        sys.exit(1)

def clear_transfer_list(clears, transfer, general_time_mult):
    if transfer >=20:
        global transfer_list, TL_clears, resolution
        if resolution_1440:
            print("clearing transfer list")
            time.sleep(general_time_mult * 2)
            pya.click(50, 440)  # transfer list left
            time.sleep(general_time_mult * 2)
            pya.click(1100, 740)  # transfer list mid
            time.sleep(general_time_mult * 2)
            pya.click(1500, 330)  # clear sold
            time.sleep(general_time_mult * 2)
            pya.click(125, 190)  # go back
            time.sleep(general_time_mult * 2)
            pya.click(1500, 450)  # back to buying
            time.sleep(general_time_mult * 2)
            transfer_list = 0
            clears += 1
            TL_clears = clears

        if resolution_1080:
            print("clearing transfer list")
            time.sleep(general_time_mult * 2)
            pya.click(50, 440)  # transfer list left
            time.sleep(general_time_mult * 2)
            pya.click(750, 740)  # transfer list mid
            time.sleep(general_time_mult * 2)
            pya.click(1200, 300)  # clear sold
            time.sleep(general_time_mult * 2)
            pya.click(125, 190)  # go back
            time.sleep(general_time_mult * 2)
            pya.click(1000, 450)  # back to buying
            time.sleep(general_time_mult * 2)
            transfer_list = 0
            clears += 1
            TL_clears = clears


class TelegramStream:
    def __init__(self, bot, chat_id):
        self.bot = bot
        self.chat_id = chat_id

    async def write(self, message):
        await self.bot.send_message(chat_id=self.chat_id, text=message)

    def flush(self):
        pass

def text_notifications(text_noti, bot_token, chat):
    if text_noti:
        bot = telegram.Bot(token=bot_token)
        chat_id = chat
        telegram_stream = TelegramStream(bot, chat_id)
        print(f"TelegramStream bot: {telegram_stream.bot}")
        print(f"TelegramStream chat_id: {telegram_stream.chat_id}")
        return telegram_stream


def long_session_rest(session, long, general_time_mult):
    if session:
        count_res = 0
        global long_session_count, random_rest, random_rest_time
        if long >= random_rest:
            print("\n\nresting")
            time.sleep(general_time_mult * random_rest_time)
            long_session_count = 0
            set_random_rest()
            count_res = 1
    return count_res

def check_for_cancel():
    if keyboard.is_pressed("="):
        print("keyboard interrupt")
        sys.exit(1)

def check_for_20_sec_pause():
    if keyboard.is_pressed("-"):
        print("keyboard interrupt - pause")
        time.sleep(20)

def set_random_rest():
    global random_rest, random_rest_time
    random_rest = random.randrange(200, 400, 1)
    random_rest_time = random.randrange(600, 1200, 1)
    count_res = 0
    return count_res
def set_random_int():
    global random_int, random_rest
    random_int = random.randrange(3, 9, 1)


def teamviewer_closer(general_time_mult):
    team = pya.locateCenterOnScreen(team_png, grayscale=True, region=(800, 500, 700, 400), confidence=0.8)

    if team != None:
        pya.click(1500, 630)  # close teamviewer popup
        time.sleep(general_time_mult * 1)

def krsu_keeps_checker():
    global krsu_keeps, krsu_max_keeps
    if krsu_keeps >= krsu_max_keeps:
        print("reached KRSU max!")
        return True
    else:
        return False

def sell(general_time_mult):
    global current_price_real_str, current_price_str, resolution_1080, resolution_1440


    if resolution_1440:
        pya.click(1750, 700)
        time.sleep(general_time_mult * 0.5)
        pya.click(1750, 880)
        time.sleep(general_time_mult * 0.5)
        pya.typewrite(current_price_real_str)
        time.sleep(general_time_mult * 0.5)
        pya.press('enter')
        time.sleep(general_time_mult * 0.5)
        pya.click(1750, 800)
        time.sleep(general_time_mult * 0.5)
        pya.typewrite(current_price_str)
        time.sleep(general_time_mult * 0.5)
        pya.press('enter')
        time.sleep(general_time_mult * 0.5)
        pya.click(1750, 880)
        time.sleep(general_time_mult * 0.5)
        pya.typewrite(current_price_real_str)
        time.sleep(general_time_mult * 0.5)
        pya.press('enter')
        time.sleep(general_time_mult * 0.5)
        pya.click(1750, 1000)
        time.sleep(general_time_mult * 1)
        pya.click(125, 190)  # go back
        time.sleep(general_time_mult * 0.5)

    if resolution_1080:
        pya.click(1420, 600)
        time.sleep(general_time_mult * 1)
        pya.click(1420, 800)
        time.sleep(general_time_mult * 0.5)
        pya.typewrite(current_price_real_str)
        time.sleep(general_time_mult * 0.5)
        pya.press('enter')
        time.sleep(general_time_mult * 0.5)
        pya.click(1420, 720)
        time.sleep(general_time_mult * 0.5)
        pya.typewrite(current_price_str)
        time.sleep(general_time_mult * 0.5)
        pya.press('enter')
        time.sleep(general_time_mult * 0.5)
        pya.click(1420, 800)
        time.sleep(general_time_mult * 0.5)
        pya.typewrite(current_price_real_str)
        time.sleep(general_time_mult * 0.5)
        pya.press('enter')
        time.sleep(general_time_mult * 0.5)
        pya.click(1420, 920)
        time.sleep(general_time_mult * 1.5)
        pya.click(125, 190)  # go back
        time.sleep(general_time_mult * 0.5)



async def buy_stuff(button_location, general_time_mult, time_to_load_search, text, bot, acc, text_noti):

    global loop_count, searches, long_session_count, total_earned, missed, bought, transfer_list, total_spent, buy_time, resolution_1440, resolution_1080, krsu_keeps


    searches += 1  # increase searches_count

    max_search_check()  # see if max search has been hit

    time.sleep(general_time_mult * random_int / 2)  # sleep a random amount of time



    long_session_count += 1  # increase long_session_count

    if resolution_1080:
        pya.click(button_location)  # move to + or - button
        time.sleep(general_time_mult * 0.5)
        pya.click(1300, 950)  # search for player
        time.sleep(time_to_load_search)
        # perform the act of buying the player
        pya.doubleClick(1420, 740)  # click buy player
        pya.doubleClick(1420, 740)  # click buy player
        pya.doubleClick(1420, 740)  # click buy player
        pya.doubleClick(1420, 740)  # click buy player
        time.sleep(general_time_mult * 0.11)
        pya.click(1000, 620)  # confirm buy
        time.sleep(general_time_mult * 0.5)

        no_res = pya.locateCenterOnScreen(no_res_img_1080, grayscale=True, region=(900, 640, 250, 100), confidence=0.8)
        time.sleep(general_time_mult * 0.1)

        if no_res != None:
            pya.click(125, 190)  # go back
            time.sleep(general_time_mult * 0.5)
        else:

            ######still need 1080 versions!!######
            soft = pya.locateCenterOnScreen(soft_png, grayscale=True, confidence=0.7)  # check if soft banned
            open_fifa = pya.locateCenterOnScreen(open_fifa_png, grayscale=True, confidence=0.7)  # check for other version of soft ban

            if open_fifa != None:
                print("got soft banned (open fifa or wait)")
                sys.exit(1)

            if soft != None:
                print("got soft banned (open fifa or wait)")
                sys.exit(1)
            ################

            failed = pya.locateCenterOnScreen(failed_img_1080, grayscale=True, confidence=0.7)  # check if bid raised any other error message

            time.sleep(general_time_mult * 0.4)

            if failed != None:
                missed += 1
                pya.click(125, 190)  # go back
                time.sleep(general_time_mult * 0.5)

            else:
                won_bid = pya.locateCenterOnScreen(won_bid_img_1080, grayscale=True, confidence=0.7)  # check if bid went through

                time.sleep(general_time_mult * 0.2)

                if won_bid != None:
                    bought += 1
                    transfer_list += 1

                    buy_time = time.time()

                    price = pya.screenshot(region=(1380, 540, 60, 25))
                    # resize the image
                    price = cv2.cvtColor(np.array(price), cv2.COLOR_RGB2BGR)
                    price = cv2.resize(price, (600, 250), interpolation=cv2.INTER_LINEAR)
                    # save the resized image
                    cv2.imwrite("price.png", price)
                    price_cv = cv2.imread('price.png', 0)
                    thresh = cv2.threshold(price_cv, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                    data_price = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')
                    data_price = re.sub("[^0-9]", "", data_price)
                    if data_price.isnumeric():
                        if text_noti:
                            telegrams = text_notifications(text, bot, acc)
                            purchases.append(int(data_price))
                            total_earned = total_earned + 0.95 * current_price - int(data_price)
                            total_spent += int(data_price)
                            await telegrams.write(f"\nBought for: {data_price} \nTotal possibly earned: {total_earned} \nTotal spent: {total_spent}")
                        else:
                            purchases.append(int(data_price))
                            total_earned = total_earned + 0.95 * current_price - int(data_price)
                            total_spent += int(data_price)
                            print("\nBought for:", data_price, "\nTotal possibly earned:", total_earned, "\nTotal spent:", total_spent)


                dupe = pya.locateCenterOnScreen(dupe_png_1080, grayscale=True, region=(1550, 750, 500, 100), confidence=0.8)
                # print(dupe)
                if KRSU:
                    time.sleep(general_time_mult * 0.5)
                    pya.click(1420, 650)  # open bio
                    time.sleep(general_time_mult * 0.5)
                    rarity = pya.screenshot(region=(1266, 590, 200, 30))  # screenshot the card's rarity
                    rarity.save("rarity.png")

                    # read the rarity from the image
                    rarity_cv = cv2.imread('rarity.png', 0)
                    thresh_r = cv2.threshold(rarity_cv, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                    data_rarity = pytesseract.image_to_string(thresh_r, lang='eng', config='--psm 6')



                    time.sleep(general_time_mult * 0.5)

                    if dupe == None:
                        check = krsu_keeps_checker()
                        rare_str = 'Rare'
                        if check:
                            time.sleep(general_time_mult * 0.1)
                            pya.click(1287, 300)  # exit bio
                            time.sleep(general_time_mult * 1)
                            # preform act of selling the player
                            sell(general_time_mult)
                        else:

                            if rare_str in data_rarity:
                                time.sleep(general_time_mult * 0.1)
                                pya.click(1287, 300)  # exit bio
                                time.sleep(general_time_mult * 1)
                                pya.click(1420, 700)  # add to club
                                time.sleep(general_time_mult * 0.5)
                                pya.click(125, 190)  # go back
                                time.sleep(general_time_mult * 0.5)
                                krsu_keeps += 1
                            else:
                                time.sleep(general_time_mult * 0.1)
                                pya.click(1287, 300)  # exit bio
                                time.sleep(general_time_mult * 1)
                                # preform act of selling the player
                                sell(general_time_mult)
                    else:
                        time.sleep(general_time_mult * 0.1)
                        pya.click(1287, 300)  # exit bio
                        time.sleep(general_time_mult * 1)
                        # preform act of selling the player
                        sell(general_time_mult)

                if only_buy:
                    if dupe == None:
                        time.sleep(general_time_mult * 0.5)
                        time.sleep(general_time_mult * 0.5)

                        pya.click(1420, 700)  # add to club
                        time.sleep(general_time_mult * 0.5)
                        pya.click(125, 190)  # go back
                        time.sleep(general_time_mult * 0.5)
                    else:
                        time.sleep(general_time_mult * 0.1)
                        pya.click(1287, 300)  # exit bio
                        time.sleep(general_time_mult * 1)
                        # preform act of selling the player
                        sell(general_time_mult)

                if only_sell:
                    # preform act of selling the player
                    sell(general_time_mult)



    # if bid_price != None:
    if resolution_1440:
        # if bid_price != None:
        pya.click(button_location)  # move to + or - button
        time.sleep(general_time_mult * 0.5)
        pya.click(1600, 1300)  # search for player
        time.sleep(time_to_load_search)
        # perform the act of buying the player
        pya.doubleClick(1750, 830)  # click buy player
        pya.doubleClick(1750, 830)  # click buy player
        pya.doubleClick(1750, 830)  # click buy player
        pya.doubleClick(1750, 830)  # click buy player
        time.sleep(general_time_mult * 0.11)
        pya.click(1260, 800)  # confirm buy
        time.sleep(general_time_mult * 0.5)

        no_res = pya.locateCenterOnScreen(no_res_img, grayscale=True, region=(1200, 800, 300, 100), confidence=0.8)  # check if anyone was even found
        time.sleep(general_time_mult * 0.1)

        if no_res != None:
            pya.click(125, 190)  # go back
            time.sleep(general_time_mult * 0.5)
        else:

            soft = pya.locateCenterOnScreen(soft_png, grayscale=True, confidence=0.7)  # check if soft banned
            open_fifa = pya.locateCenterOnScreen(open_fifa_png, grayscale=True, confidence=0.7)  # check for other version of soft ban

            if open_fifa != None:
                print("got soft banned (open fifa or wait)")
                sys.exit(1)

            if soft != None:
                print("got soft banned (open fifa or wait)")
                sys.exit(1)

            failed = pya.locateCenterOnScreen(failed_img, grayscale=True, confidence=0.7)  # check if bid raised any other error message

            time.sleep(general_time_mult * 0.1)

            if failed != None:
                missed += 1
                pya.click(125, 190)  # go back
                time.sleep(general_time_mult * 0.5)

            else:
                won_bid = pya.locateCenterOnScreen(won_bid_img, grayscale=True, confidence=0.7)  # check if bid went through

                time.sleep(general_time_mult * 0.2)

                if won_bid != None:
                    bought += 1
                    transfer_list += 1

                    buy_time = time.time()

                    price = pya.screenshot(region=(1720, 625, 43, 20))
                    # resize the image
                    price = cv2.cvtColor(np.array(price), cv2.COLOR_RGB2BGR)
                    price = cv2.resize(price, (430, 200), interpolation=cv2.INTER_LINEAR)
                    # save the resized image
                    cv2.imwrite("price.png", price)
                    price_cv = cv2.imread('price.png', 0)
                    thresh = cv2.threshold(price_cv, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                    data_price = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')
                    data_price = re.sub("[^0-9]", "", data_price)
                    if data_price.isnumeric():
                        if text_noti:
                            telegrams = text_notifications(text, bot, acc)
                            purchases.append(int(data_price))
                            total_earned = total_earned + 0.95 * current_price - int(data_price)
                            total_spent += int(data_price)
                            await telegrams.write(
                                f"\nBought for: {data_price} \nTotal possibly earned: {total_earned} \nTotal spent: {total_spent}")
                        else:
                            purchases.append(int(data_price))
                            total_earned = total_earned + 0.95 * current_price - int(data_price)
                            total_spent += int(data_price)
                            print("\nBought for:", data_price, "\nTotal possibly earned:", total_earned,
                                  "\nTotal spent:", total_spent)

                dupe = pya.locateCenterOnScreen(dupe_png, grayscale=True, region=(1550, 750, 500, 100), confidence=0.8)

                if KRSU:
                    time.sleep(general_time_mult * 0.5)
                    pya.click(1750, 750)  # open bio
                    time.sleep(general_time_mult * 0.5)
                    rarity = pya.screenshot(region=(1585, 618, 200, 25))  # screenshot the card's rarity
                    rarity.save("rarity.png")

                    # read the rarity from the image
                    rarity_cv = cv2.imread('rarity.png', 0)
                    thresh_r = cv2.threshold(rarity_cv, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                    data_rarity = pytesseract.image_to_string(thresh_r, lang='eng', config='--psm 6')

                    time.sleep(general_time_mult * 0.5)

                    if dupe == None:
                        rare_str = 'Rare'
                        check = krsu_keeps_checker()
                        if check:
                            time.sleep(general_time_mult * 0.1)
                            pya.click(1600, 325)  # exit bio
                            time.sleep(general_time_mult * 1)
                            # preform act of selling the player
                            sell(general_time_mult)
                        else:
                            if rare_str in data_rarity:
                                time.sleep(general_time_mult * 0.1)
                                pya.click(1600, 325)  # exit bio
                                time.sleep(general_time_mult * 1)
                                pya.click(1750, 800)  # add to club
                                time.sleep(general_time_mult * 0.5)
                                pya.click(125, 190)  # go back
                                time.sleep(general_time_mult * 0.5)
                                krsu_keeps += 1
                            else:
                                time.sleep(general_time_mult * 0.1)
                                pya.click(1600, 325)  # exit bio
                                time.sleep(general_time_mult * 1)
                                # preform act of selling the player
                                sell(general_time_mult)
                    else:
                        time.sleep(general_time_mult * 0.1)
                        pya.click(1600, 325)  # exit bio
                        time.sleep(general_time_mult * 1)
                        # preform act of selling the player
                        sell(general_time_mult)

                if only_buy:
                    if dupe == None:
                        time.sleep(general_time_mult * 0.5)
                        time.sleep(general_time_mult * 0.5)

                        pya.click(1750, 800)  # add to club
                        time.sleep(general_time_mult * 0.5)
                        pya.click(125, 190)  # go back
                        time.sleep(general_time_mult * 0.5)
                    else:
                        time.sleep(general_time_mult * 0.1)
                        pya.click(1600, 325)  # exit bio
                        time.sleep(general_time_mult * 1)
                        # preform act of selling the player
                        sell(general_time_mult)

                if only_sell:
                    # preform act of selling the player
                    sell(general_time_mult)




async def recurring_prints(bot, text, acc, text_noti ):
    global buy_time, TL_clears
    if text_noti:
        if searches % 2 == 0:
            telegrams = text_notifications(text, bot, acc)
            message = f'''total searches: {searches}\ntotal sniped: {bought}\nTotal possibly earned: {total_earned}\nTotal spent: {total_spent}\nTotal missed: {missed}
            '''
            current_time = time.time()
            total_time = current_time - start_time
            delta = timedelta(seconds=total_time)
            # Extract the hours, minutes, and seconds from the timedelta object
            hours, remainder = divmod(delta.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            if bought >= 1:
                time_per_bought = total_time / bought
                time_per_bought_delta = timedelta(seconds=time_per_bought)
                bought_hours, bought_remainder = divmod(time_per_bought_delta.seconds, 3600)
                bought_minutes, bought_seconds = divmod(bought_remainder, 60)
                message += f"average time between purchases: {bought_hours:02d}:{bought_minutes:02d}:{bought_seconds:02d}\n"
                money_per_hour = total_earned / (total_time / 3600)
                message += f"CPH: {money_per_hour}\n"
                if len(purchases) >= 1:
                    avg_price = sum(purchases) / len(purchases)
                    message += f"average price per purchase: {avg_price}\n"

            if buy_time is not None:
                since_last = current_time - buy_time
                delta = timedelta(seconds=since_last - 8)
                hours, remainder = divmod(delta.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                message += f"total time taken: {hours:02d}:{minutes:02d}:{seconds:02d}\ntime since last purchase: {hours:02d}:{minutes:02d}:{seconds:02d}\n"

            message += f"Transfer list has been cleared {TL_clears} times"

            await telegrams.write(message)
    else:
        print(f'\n\n\ntotal searches: {searches}')
        print(f'total sniped: {bought}')
        print(f'Total possibly earned: {total_earned}\nTotal spent: {total_spent}\nTotal missed: {missed}')
        current_time = time.time()
        total_time = current_time - start_time
        delta = timedelta(seconds=total_time)
        # Extract the hours, minutes, and seconds from the timedelta object
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"total time taken: {hours:02d}:{minutes:02d}:{seconds:02d}")
        # Calculate the average time between purchases
        if bought >= 1:
            time_per_bought = total_time / bought
            time_per_bought_delta = timedelta(seconds=time_per_bought)
            bought_hours, bought_remainder = divmod(time_per_bought_delta.seconds, 3600)
            bought_minutes, bought_seconds = divmod(bought_remainder, 60)
            print(f"average time between purchases: {bought_hours:02d}:{bought_minutes:02d}:{bought_seconds:02d}")
            money_per_hour = total_earned / (total_time / 3600)
            print(f"CPH: {money_per_hour}")
            if len(purchases) >= 1:
                avg_price = sum(purchases) / len(purchases)
                print(f"average price per purchase: {avg_price}")

        if buy_time != None:
            since_last = current_time - buy_time
            delta = timedelta(seconds=since_last - 8)
            # Extract the hours, minutes, and seconds from the timedelta object
            hours, remainder = divmod(delta.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            print(f"time since last purchase: {hours:02d}:{minutes:02d}:{seconds:02d}")

        print(f"transfer list has been cleared {TL_clears} times")

def reset_loop_count():
    global loop_count
    loop_count = 0

def increment_loop_count():
    global loop_count
    loop_count += 1  # increase loop_count

rare_png,dupe_png,failed_img,no_res_img,won_bid_img,soft_png,team_png,open_fifa_png,launch_fifa_png,in_fifa_png,cont_local_png, no_res_img_1080, failed_img_1080, won_bid_img_1080, dupe_png_1080 = image_loader()



async def main(general_time_mult, time_to_load_search):



    print("in main")
    # all global vairables needed
    global total_spent, resolution_1440, resolution_1080, total_earned, searches, bought, transfer_list, missed, total_loops, modes, long_session_count, start_time, buy_time, TL_clears, purchases, current_price_real_str, paused, loop_count, current_price, current_price_str, random_int, minus_buy, minus_bid, plus_buy, plus_bid, buy_limit, bot_id, account_id

    ##test

    ## end test



    past_input_reader([max_loops, buy_limit, current_price, KRSU, only_buy, only_sell, resolution_1080, resolution_1440, bot_id, account_id, text_noti])

    if text_noti:
        out = text_notifications(text_noti, bot_id, account_id)
    else:
        file = open("outputs.txt", "w")
        sys.stdout = file


    # sys.stdout = out

    ensure_mode_selection()

    ensure_resolution()

    update_current_price()

    count_res = set_random_rest()


    if resolution_1080:
        minus_bid = 500, 770  # coords of minus bid button
        plus_bid = 970, 770  # coords of plus bid button
        minus_buy = 500, 880  # coords of minus buy button
        plus_buy = 970, 880  # coords of plus buy button


    if resolution_1440:
        minus_bid = 830, 800  # coords of minus bid button
        plus_bid = 1300, 800  # coords of plus bid button
        minus_buy = 830, 915  # coords of minus buy button
        plus_buy = 1300, 915  # coords of plus buy button

    while True:
        if bought >= buy_limit:
            print("reached max purchases")
            sys.exit(1)

        if count_res == 1:
            count_res =  set_random_rest()

        teamviewer_closer(general_time_mult)  # check for teamviewer popup and close it

        total_loops +=1  # increase loops counter
        clear_transfer_list(TL_clears, transfer_list, general_time_mult)  # check if transfer list needs clearing then clear if it does
        count_res = long_session_rest(long_session, long_session_count, general_time_mult)  # check if it's a long session and then rest as needed
        set_random_int()  # set the random value that will be used to sleep


        check_for_cancel()  # check if user wants to cancel script
        check_for_20_sec_pause()  # check if user wants to pause for 20 sec
        if loop_count == 3:
            reset_loop_count() # reset to start over
            await buy_stuff(plus_buy, general_time_mult, time_to_load_search, text_noti, bot_id, account_id, text_noti)
            await recurring_prints(bot_id, text_noti, account_id, text_noti)


        check_for_cancel()  # check if user wants to cancel script
        check_for_20_sec_pause()  # check if user wants to pause for 20 sec
        if loop_count == 2:
            await buy_stuff(plus_bid, general_time_mult, time_to_load_search, text_noti, bot_id, account_id, text_noti)
            increment_loop_count()
            await recurring_prints(bot_id, text_noti, account_id, text_noti)


        check_for_cancel()  # check if user wants to cancel script
        check_for_20_sec_pause()  # check if user wants to pause for 20 sec
        if loop_count == 1:
            await buy_stuff(minus_buy, general_time_mult, time_to_load_search, text_noti, bot_id, account_id, text_noti)
            increment_loop_count()
            await recurring_prints(bot_id, text_noti, account_id, text_noti)

        check_for_cancel()  # check if user wants to cancel script
        check_for_20_sec_pause()  # check if user wants to pause for 20 sec
        if loop_count == 0:
            await buy_stuff(minus_bid, general_time_mult, time_to_load_search, text_noti, bot_id, account_id, text_noti)
            increment_loop_count()
            await recurring_prints(bot_id, text_noti, account_id, text_noti)
        if not text_noti:
            file.flush()

# function that can stop process at the press of '=' button at any time
def listen_for_interrupt():
    while True:
        if keyboard.is_pressed('pause'):
            print("Interrupt received (pressed 'pause' key)")
            if not text_noti:
                os.startfile("outputs.txt")
            sys.exit(1)
        time.sleep(0.1)

def my_process(gen, times):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(gen, times))
def runner(general_time_mult, time_to_load_search):
    print("in run")


    # run both loops at the same time so that a key press can stop the other loop instantly
    loop_process = multiprocessing.Process(target=my_process, args=(general_time_mult, time_to_load_search))
    interrupt_process = multiprocessing.Process(target=listen_for_interrupt)

    loop_process.start()
    interrupt_process.start()

    interrupt_process.join()
    loop_process.terminate()

if __name__ == "__main__":
    multiprocessing.freeze_support()
    create_gui()


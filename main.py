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

## Currently not developed
card_type = "Normal"
## END DEV


current_price = 700  # the price you want to sell at
max_loops = 4000 # max amount of searches the code will do
long_session=True # anti bot detection for long sessions but runs slower
## MODES
# set ONLY ONE of these to true at a time
only_sell = True # always sells the players
only_buy = False # stores all in the club
KRSU = False # keep rares sell uncommons
## END MODES




#pytesseract exe location
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#initialize global variables and counters
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
current_price_real_str = str(current_price)
if current_price < 1000:
    current_price_str = current_price - 50
else:
    current_price_str = current_price - 100
current_price_str = str(current_price_str)
paused = False
loop_count = 0
random_int = 0.5
minus_bid = 830, 800  # coords of minus bid button
plus_bid = 1300, 800  # coords of plus bid button
minus_buy = 830, 915  # coords of minus buy button
plus_buy = 1300, 915  # coords of plus buy button






def image_loader():
    rare_png = Image.open('images/rare.png')
    dupe_png = Image.open('images/dupe.png')
    failed_img = Image.open('images/fail.png')
    no_res_img = Image.open('images/no_res.png')
    won_bid_img = Image.open('images/won_bid.png')
    soft_png = Image.open('images/soft_banned.png')
    team_png = Image.open('images/team.png')
    open_fifa_png = Image.open('images/open_fifa.png')
    launch_fifa_png = Image.open('images/launch_fifa.png')
    in_fifa_png = Image.open('images/in_fifa.png')
    cont_local_png = Image.open('images/cont_local.png')

    return rare_png,dupe_png,failed_img,no_res_img,won_bid_img,soft_png,team_png,open_fifa_png,launch_fifa_png,in_fifa_png,cont_local_png

def max_search_check():
    if total_loops >= max_loops:
        print('reached max iterations')
        exit(1)

def ensure_mode_selection():
    if sum([only_buy, only_sell, KRSU]) != 1:
        modes = sum([only_buy, only_sell, KRSU])
        print(f'must turn on exactly one mode at a time! Currently {modes} modes are turned on')
        exit(1)

def clear_transfer_list(clears, transfer):
    if transfer >=20:
        global transfer_list, TL_clears
        print("clearing transfer list")
        time.sleep(2)
        pya.click(50, 440)  # transfer list left
        time.sleep(2)
        pya.click(1100, 740)  # transfer list mid
        time.sleep(2)
        pya.click(1500, 330)  # clear sold
        time.sleep(2)
        pya.click(125, 190)  # go back
        time.sleep(2)
        pya.click(1500, 450)  # back to buying
        time.sleep(2)
        transfer_list = 0
        clears += 1
        TL_clears = clears

def long_session_rest(session, long):
    if session:
        global long_session_count
        if long >= 200:
            print("\n\nresting")
            time.sleep(300)
            long_session_count = 0

def check_for_cancel():
    if keyboard.is_pressed("="):
        print("keyboard interrupt")
        exit(1)

def check_for_20_sec_pause():
    if keyboard.is_pressed("-"):
        print("keyboard interrupt - pause")
        time.sleep(20)

def set_random_int():
    global random_int
    random_int = random.randrange(1, 4, 1)

def teamviewer_closer():
    team = pya.locateCenterOnScreen(team_png, grayscale=True, region=(800, 500, 700, 400), confidence=0.8)

    if team != None:
        pya.click(1500, 630)  # close teamviewer popup
        time.sleep(1)

def sell():
    global current_price_real_str, current_price_str

    pya.click(1750, 700)
    time.sleep(0.5)
    pya.click(1750, 880)
    time.sleep(0.5)
    pya.typewrite(current_price_real_str)
    time.sleep(0.5)
    pya.press('enter')
    time.sleep(0.5)
    pya.click(1750, 800)
    time.sleep(0.5)
    pya.typewrite(current_price_str)
    time.sleep(0.5)
    pya.press('enter')
    time.sleep(0.5)
    pya.click(1750, 880)
    time.sleep(0.5)
    pya.typewrite(current_price_real_str)
    time.sleep(0.5)
    pya.press('enter')
    time.sleep(0.5)
    pya.click(1750, 1000)
    time.sleep(1)
    pya.click(125, 190)  # go back
    time.sleep(0.5)


def buy_stuff(button_location):

    global loop_count, searches, long_session_count, total_earned, missed, bought, transfer_list, total_spent, buy_time

    searches += 1  # increase searches_count

    time.sleep(random_int / 2)  # sleep a random amount of time

    max_search_check()  # see if max search has been hit

    long_session_count += 1  # increase long_session_count

    # if bid_price != None:
    pya.click(button_location)  # move to + or - button
    time.sleep(0.5)
    pya.click(1600, 1300)  # search for player
    time.sleep(0.5)
    # perform the act of buying the player
    pya.doubleClick(1750, 830)  # click buy player
    pya.doubleClick(1750, 830)  # click buy player
    pya.doubleClick(1750, 830)  # click buy player
    pya.doubleClick(1750, 830)  # click buy player
    time.sleep(0.11)
    pya.click(1260, 800)  # confirm buy
    time.sleep(0.5)

    no_res = pya.locateCenterOnScreen(no_res_img, grayscale=True, region=(1200, 800, 300, 100), confidence=0.8)  # check if anyone was even found
    time.sleep(0.1)

    if no_res != None:
        pya.click(125, 190)  # go back
        time.sleep(0.5)
    else:

        soft = pya.locateCenterOnScreen(soft_png, grayscale=True, confidence=0.7)  # check if soft banned
        open_fifa = pya.locateCenterOnScreen(open_fifa_png, grayscale=True, confidence=0.7)  # check for other version of soft ban

        if open_fifa != None:
            print("got soft banned (open fifa or wait)")
            exit(1)

        if soft != None:
            print("got soft banned")
            exit(1)

        failed = pya.locateCenterOnScreen(failed_img, grayscale=True, confidence=0.7)  # check if bid raised any other error message

        time.sleep(0.1)

        if failed != None:
            missed += 1
            pya.click(125, 190)  # go back
            time.sleep(0.5)

        else:
            won_bid = pya.locateCenterOnScreen(won_bid_img, grayscale=True, confidence=0.7)  # check if bid went through

            time.sleep(0.2)

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
                    purchases.append(int(data_price))
                    total_earned = total_earned + 0.95 * current_price - int(data_price)
                    total_spent += int(data_price)
                    print("\nBought for:", data_price, "\nTotal possibly earned:", total_earned, "\nTotal spent:",
                          total_spent)

            dupe = pya.locateCenterOnScreen(dupe_png, grayscale=True, region=(1550, 750, 500, 100), confidence=0.8)

            if KRSU:
                time.sleep(0.5)
                pya.click(1750, 750)  # open bio
                time.sleep(0.5)
                rarity = pya.screenshot(region=(1585, 618, 200, 25))  # screenshot the card's rarity
                rarity.save("rarity.png")

                # read the rarity from the image
                rarity_cv = cv2.imread('rarity.png', 0)
                thresh_r = cv2.threshold(rarity_cv, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                data_rarity = pytesseract.image_to_string(thresh_r, lang='eng', config='--psm 6')



                time.sleep(0.5)

                if dupe == None:
                    rare_str = 'Rare'
                    if rare_str in data_rarity:
                        time.sleep(0.1)
                        pya.click(1600, 325)  # exit bio
                        time.sleep(1)
                        pya.click(1750, 800)  # add to club
                        time.sleep(0.5)
                        pya.click(125, 190)  # go back
                        time.sleep(0.5)
                    else:
                        time.sleep(0.1)
                        pya.click(1600, 325)  # exit bio
                        time.sleep(1)
                        # preform act of selling the player
                        sell()
                else:
                    time.sleep(0.1)
                    pya.click(1600, 325)  # exit bio
                    time.sleep(1)
                    # preform act of selling the player
                    sell()

            if only_buy:
                if dupe == None:
                    time.sleep(0.5)
                    time.sleep(0.5)
                    pya.click(1750, 800)  # add to club
                    time.sleep(0.5)
                    pya.click(125, 190)  # go back
                    time.sleep(0.5)
                else:
                    time.sleep(0.1)
                    pya.click(1600, 325)  # exit bio
                    time.sleep(1)
                    # preform act of selling the player
                    sell()

            if only_sell:
                # preform act of selling the player
                sell()


def recurring_prints():
    global buy_time, TL_clears

    print('\ntotal searches: ', searches)
    print('total sniped: ', bought)
    print("Total possibly earned:", total_earned, "\nTotal spent:", total_spent, "\nTotal missed:", missed)
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

rare_png,dupe_png,failed_img,no_res_img,won_bid_img,soft_png,team_png,open_fifa_png,launch_fifa_png,in_fifa_png,cont_local_png = image_loader()

ensure_mode_selection()

def main():
    while True:
        #all global vairables needed
        global total_spent, total_earned, searches, bought, transfer_list, missed, total_loops, modes, long_session_count, start_time, buy_time, TL_clears, purchases, current_price_real_str, paused, loop_count, current_price, current_price_str, random_int

        teamviewer_closer()  # check for teamviewer popup and close it

        total_loops +=1  # increase loops counter
        clear_transfer_list(TL_clears, transfer_list)  # check if transfer list needs clearing then clear if it does
        long_session_rest(long_session, long_session_count)  # check if it's a long session and then rest as needed
        set_random_int()  # set the random value that will be used to sleep


        check_for_cancel()  # check if user wants to cancel script
        check_for_20_sec_pause()  # check if user wants to pause for 20 sec
        if loop_count == 3:
            reset_loop_count() # reset to start over
            buy_stuff(plus_buy)
            recurring_prints()


        check_for_cancel()  # check if user wants to cancel script
        check_for_20_sec_pause()  # check if user wants to pause for 20 sec
        if loop_count == 2:
            buy_stuff(plus_bid)
            increment_loop_count()
            recurring_prints()


        check_for_cancel()  # check if user wants to cancel script
        check_for_20_sec_pause()  # check if user wants to pause for 20 sec
        if loop_count == 1:
            buy_stuff(minus_buy)
            increment_loop_count()
            recurring_prints()

        print('hello')
        check_for_cancel()  # check if user wants to cancel script
        check_for_20_sec_pause()  # check if user wants to pause for 20 sec
        if loop_count == 0:
            buy_stuff(minus_bid)
            increment_loop_count()
            recurring_prints()


# function that can stop process at the press of '=' button at any time
def listen_for_interrupt():
    while True:
        if keyboard.is_pressed('pause'):
            print("Interrupt received (pressed 'pause' key)")
            exit(1)


if __name__ == "__main__":

    # run both loops at the same time so that a key press can stop the other loop instantly
    loop_process = multiprocessing.Process(target=main)
    interrupt_process = multiprocessing.Process(target=listen_for_interrupt)

    loop_process.start()
    interrupt_process.start()

    interrupt_process.join()
    loop_process.terminate()

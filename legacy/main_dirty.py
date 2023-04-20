import random
from PIL import Image
import pyautogui as pya
# import pydirectinput as pyd
import cv2
import pytesseract
import re
import keyboard
# import pandas as pd
import time
# import subprocess
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support import expected_conditions as EC
# import bs4
# import requests
from datetime import datetime, timedelta

## Currently not developed
card_type = "Normal"
## END DEV


max_loops = 4000 # max amount of searches the code will do
current_price = 650 # the price you want to sell at
long_session=True # anti bot detection for long sessions but runs slower
## MODES
# set ONLY ONE of these to true at a time
only_sell = True # always sells the players
only_buy = False # stores all in the club
KRSU = False # keep rares sell uncommons
## END MODES





## NO NEED TO LOOK FURTHER FOR GENERAL USE





# names = pd.read_excel('player_futbin_data.xlsx')
# options = Options()
# options.page_load_strategy = 'eager'
# options.add_argument('--enable-extensions')
# options.add_argument("--disable-notifications")
# options.add_argument("--disable-popup-blocking")
# options.add_extension(r'C:\Users\Jagge_vbl7d7m\PycharmProjects\pythonProject\extension_5_4_1_0.crx')
# options.add_argument("disable-infobars")
#
# driver_path = r'C:\cmder\bin\chromedriver.exe'
# service = Service(executable_path=driver_path)

# matches = names.loc[names['Player Name'] == 'dereck-kutesa']
# print(f'Matches {matches}')

# matches = names.loc[names['Player Name'] == 'catalin-cabuz']
# print(matches)
# type_matches = matches.loc[matches['Card Type'] == "Normal"]
# print(type_matches)
# ID = type_matches.iloc[0]['ID']
# print(f'ID :{ID}')
#
# matches = names.loc[names['Player Name'] == 'catalin-cabuz']
# if not matches.empty:
#     print("315")
#     # Check if corresponding row has "Normal" in "Card Type" column
#     type_matches = matches.loc[matches['Card Type'] == "Normal"]
#     if not type_matches.empty:
#         # Get value from "ID" column
#         ID = type_matches.iloc[0]['ID']
#         print(f'ID :{ID}')
#
# exit(1)




# # initialize webdriver
# driver_path = r'C:\cmder\bin\chromedriver.exe'
# driver = webdriver.Chrome(executable_path=driver_path)
#
# # navigate to Futbin homepage
# driver.get('https://www.futbin.com/')
#
# # search for the player
# search_box = WebDriverWait(driver, 3).until(
#     EC.presence_of_element_located((By.NAME, "search_term"))
# )
# search_box.send_keys("saka")
# search_box.submit()
#
# # click the search button
# search_button = driver.find_element_by_xpath('//button[@type="submit"]')
# search_button.click()
#
# # wait for the search results page to load
# driver.implicitly_wait(10)
#
# # locate the first player in the search results list
# player_link = driver.find_element_by_css_selector('.player_full_name > a')
#
# # extract the player ID from the URL
# player_url = player_link.get_attribute('href')
# player_id = player_url.split('/')[-2]
#
# print(player_id)



# player_url = 'https://www.futbin.com/23/player/50661/bukayo-saka'
#
# driver_path = r'C:\cmder\bin\chromedriver.exe' # Replace this with the actual file path where your chromedriver executable is located
# service = Service(executable_path=driver_path)
# driver = webdriver.Chrome(service=service) # Initialize a Chrome webdriver instance
# driver.get(player_url) # Load the player page
#
# time.sleep(5) # Wait for the page to load
#
# # Find the price element using its ID
# price_element = driver.find_element(By.CSS_SELECTOR, '#pc-lowest-1')
#
# # Get the price value from the "data-price" attribute of the element
# price = price_element.get_attribute('data-price')
#
# # Print the price
# print(f"The price of Bukap Saka is {price} coins on PC")
#
# driver.quit() # Close the webdriver instance
#
#
#
#
#
# exit(1)







pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

total_spent = 0
total_earned = 0

current_price_real_str = str(current_price)
if current_price < 1000:
    current_price_str = current_price - 50
else:
    current_price_str = current_price - 100
current_price_str = str(current_price_str)
paused = False
loop_count = 0
# bid_price_img = Image.open('bid_price.png')
# none_found_img = Image.open('none_found.png')
rare_png = Image.open('../images/rare.png')
dupe_png = Image.open('../images/dupe.png')
failed_img = Image.open('../images/fail.png')
no_res_img = Image.open('../images/no_res.png')
won_bid_img = Image.open('../images/won_bid.png')
soft_png = Image.open('../images/soft_banned.png')
team_png = Image.open('../images/team.png')
open_fifa_png = Image.open('../images/open_fifa.png')
launch_fifa_png = Image.open('../images/launch_fifa.png')
in_fifa_png = Image.open('../images/in_fifa.png')
cont_local_png = Image.open('../images/cont_local.png')
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

## BEGIN TESTING CENTER


#
# fifa_path = r'Z:\steam\steamapps\common\FIFA 23\FIFA23.exe'  # Replace this with the path to your fifa.exe
#
# subprocess.call(fifa_path)
#
# time.sleep(30)
#
# launch_button = pya.locateCenterOnScreen(launch_fifa_png, grayscale = True, confidence = 0.7)
# cont_local = pya.locateCenterOnScreen(cont_local_png, grayscale = True, confidence = 0.7)
#
# print(cont_local)
# print(launch_button)
#
# if launch_button != None:
#     pya.click(launch_button)
#
# if cont_local != None:
#     pya.click(cont_local)
#
# time.sleep(30)
#
# in_fifa = pya.locateCenterOnScreen(in_fifa_png, grayscale = True, confidence = 0.7)
#
# while in_fifa == None:
#     in_fifa = pya.locateCenterOnScreen(in_fifa_png, grayscale=True, confidence=0.7)
#     time.sleep(5)
#
# time.sleep(10)
# pyd.press('enter')
# time.sleep(4)
# pyd.press('enter')
# time.sleep(5)
# pyd.press('enter')
# time.sleep(30)
# pyd.press('right')
# time.sleep(1)
# pyd.press('enter')
# time.sleep(20)
# pyd.press('right')
# pyd.press('right')
# pyd.press('enter')
# time.sleep(2)
# pyd.press('right')
# pyd.press('enter')
# pyd.press('w')
# time.sleep(1)
# pyd.press('escape')
# time.sleep(2)
# pyd.press('escape')
# time.sleep(2)
# pyd.press('escape')
# time.sleep(1)
# pyd.press('up')
# time.sleep(1)
# pyd.press('enter')
# time.sleep(10)
# pyd.keyDown('alt')
# pyd.keyDown('f4')
# pyd.keyUp('f4')
# pyd.keyUp('alt')
# time.sleep(5)
# exit(1)

## END TESTING CENTER



if only_sell:
    modes += 1
if only_buy:
    modes += 1
if KRSU:
    modes += 1

if modes >= 2:
    print('only turn on one mode at a time!')
    exit(1)

while 0 < 1:

    total_loops +=1

    if total_loops >= max_loops:
        print('reached max iterations')
        exit(1)
    if long_session:
        if long_session_count >= 200:
            print("\n\nresting")
            time.sleep(300)
            long_session_count = 0

    if transfer_list >=20:
        print("clearing transfer list")
        time.sleep(2)
        pya.click(50,440)
        time.sleep(2)
        pya.click(1100,740)
        time.sleep(2)
        pya.click(1500,330)
        time.sleep(2)
        pya.click(125, 190)
        time.sleep(2)
        pya.click(1500,450)
        time.sleep(2)
        transfer_list = 0
        TL_clears+=1


    if not paused:

        if keyboard.is_pressed("="):
            print("keyboard interrupt")
            break

        if keyboard.is_pressed("-"):
            print("keyboard interrupt - pause")
            time.sleep(20)

        # random_int = random.randrange(2, 4, 1)

        random_int = 1

        # time.sleep(0.2)
        time.sleep(random_int/2)

        # bid_price = pya.locateOnScreen(bid_price_img, grayscale=True, region = (1,1,1,1))

        if loop_count == 2:

            team = pya.locateCenterOnScreen(team_png, grayscale = True, region = (800, 500, 700, 400), confidence = 0.8)


            if team != None:
                pya.click(1500, 630)
                time.sleep(1)

            long_session_count += 1
            searches += 1

            # if random_int == 5:
            #     if loop_count < 3:
            #         loop_count +=1
            # else:
            loop_count +=1
            # if bid_price != None:
            pya.click(1300, 800) # move to + button
            time.sleep(0.5)
            pya.click(1600, 1300)
            time.sleep(0.5)
            #     # perform the act of buying the player
            pya.doubleClick(1750, 830)
            pya.doubleClick(1750, 830)
            pya.doubleClick(1750, 830)
            pya.doubleClick(1750, 830)
            time.sleep(0.11)
            pya.click(1260, 800)
            time.sleep(0.5)

            no_res = pya.locateCenterOnScreen(no_res_img, grayscale = True, region = (1200, 800, 300, 100), confidence = 0.8)
            time.sleep(0.1)

            if no_res != None:
                pya.click(125, 190)
                time.sleep(0.5)
            else:
                soft = pya.locateCenterOnScreen(soft_png, grayscale = True, confidence = 0.7)
                open_fifa = pya.locateCenterOnScreen(open_fifa_png, grayscale=True, confidence=0.7)

                if open_fifa != None:
                    print("got soft banned (open fifa or wait)")
                    exit(1)


                if soft != None:
                    print("got soft banned")
                    exit(1)

                failed = pya.locateCenterOnScreen(failed_img, grayscale = True, confidence = 0.7)
                time.sleep(0.1)

                if failed != None:
                    missed += 1
                    pya.click(125, 190)
                    time.sleep(0.5)
                else:
                    won_bid = pya.locateCenterOnScreen(won_bid_img, grayscale=True, confidence=0.7)
                    time.sleep(0.2)

                    if won_bid != None:

                        buy_time = time.time()

                        bought += 1
                        transfer_list +=1

                        price = pya.screenshot(region=(1720, 625, 43, 20))
                        # name = pya.screenshot(region=(1590, 672, 28, 310))

                        # name.save("name.png")
                        price.save("price.png")

                        # time.sleep(0.2)

                        # name_cv = cv2.imread('price.png', 0)
                        # thresh = cv2.threshold(name_cv, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                        # data_name = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')
                        # # data_name = re.sub("[^0-9]", "", data_name)
                        # if not data_price.isnumeric():
                        #     names = pd.read_excel('player_futbin_data.xlsx')
                        #     # Check if data_name matches any value in "Player Name" column
                        #     matches = names.loc[names['Player Name'] == data_name]
                        #     if not matches.empty:
                        #         # Check if corresponding row has "Normal" in "Card Type" column
                        #         type_matches = matches.loc[matches['Card Type'] == card_type]
                        #         if not type_matches.empty:
                        #             # Get value from "ID" column
                        #             ID = type_matches.iloc[0]['ID']
                        #             print(ID)

                        price_cv = cv2.imread('price.png', 0)
                        thresh = cv2.threshold(price_cv, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                        data_price = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')
                        data_price = re.sub("[^0-9]", "", data_price)
                        if data_price.isnumeric():
                            purchases.append(int(data_price))
                            total_earned = total_earned + 0.95 * current_price - int(data_price)
                            total_spent += int(data_price)
                            print("\nBought for:", data_price, "\nTotal possibly earned:", total_earned, "\nTotal spent:", total_spent)

                    if KRSU:
                        time.sleep(0.5)
                        pya.click(1750,750) # open bio
                        time.sleep(0.5)
                        rarity = pya.screenshot(region=(1585, 618, 200, 25))

                        rarity.save("rarity.png")

                        rarity_cv = cv2.imread('rarity.png', 0)
                        thresh_r = cv2.threshold(rarity_cv, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                        data_rarity = pytesseract.image_to_string(thresh_r, lang='eng', config='--psm 6')

                        rare_str = 'Rare'

                        dupe = pya.locateCenterOnScreen(dupe_png, grayscale=True, region=(1550, 750, 500, 100),confidence=0.8)

                        time.sleep(0.5)

                        if dupe == None:
                            if rare_str in data_rarity:
                                time.sleep(0.1)
                                pya.click(1600,325) #exit bio
                                time.sleep(1)
                                pya.click(1750, 800) #add to club
                                time.sleep(0.5)
                                pya.click(125, 190) #back to search
                                time.sleep(0.5)
                            else:
                                time.sleep(0.1)
                                pya.click(1600, 325) #exit bio
                                time.sleep(1)
                                #     # preform act of selling the player
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
                                pya.click(125, 190)
                                time.sleep(0.5)
                        else:
                            time.sleep(0.1)
                            pya.click(1600, 325)  # exit bio
                            time.sleep(1)
                            #     # preform act of selling the player
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
                            pya.click(125, 190)
                            time.sleep(0.5)



                    if only_buy:
                        if dupe == None:
                            dupe = pya.locateCenterOnScreen(dupe_png, grayscale=True, region=(1550, 750, 500, 100), confidence=0.8)

                            time.sleep(0.5)
                            time.sleep(0.5)
                            pya.click(1750, 800)
                            time.sleep(0.5)
                            pya.click(125, 190)
                            time.sleep(0.5)
                        else:
                            time.sleep(0.1)
                            pya.click(1600, 325)  # exit bio
                            time.sleep(1)
                            #     # preform act of selling the player
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
                            pya.click(125, 190)
                            time.sleep(0.5)


                    if only_sell:
                        #     # preform act of selling the player
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
                        pya.click(125, 190)
                        time.sleep(0.5)

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


        if keyboard.is_pressed("="):
            print("keyboard interrupt")
            break
        if keyboard.is_pressed("-"):
            print("keyboard interrupt - pause")
            time.sleep(20)

        if keyboard.is_pressed('p'):
            paused = not paused
            print("Paused" if paused else "Resumed")
            time.sleep(3)  # delay to avoid rapid toggling of pause state

        if loop_count == 1:

            team = pya.locateCenterOnScreen(team_png, grayscale=True, region=(800, 500, 700, 400), confidence=0.8)

            if team != None:
                pya.click(1500, 630)
                time.sleep(1)

            time.sleep(random_int / 2)
            long_session_count += 1
            searches += 1

            # if random_int == 5:
            #     if loop_count < 3:
            #         loop_count +=1
            # else:
            loop_count +=1
            # if bid_price != None:
            pya.click(830, 915) # move to + button
            time.sleep(0.5)
            pya.click(1600, 1300)
            time.sleep(0.5)
            #     # perform the act of buying the player
            pya.doubleClick(1750, 830)
            pya.doubleClick(1750, 830)
            pya.doubleClick(1750, 830)
            pya.doubleClick(1750, 830)
            time.sleep(0.11)
            pya.click(1260, 800)
            time.sleep(0.5)

            no_res = pya.locateCenterOnScreen(no_res_img, grayscale = True, region = (1200, 800, 300, 100), confidence = 0.8)
            time.sleep(0.1)

            if no_res != None:
                pya.click(125, 190)
                time.sleep(0.5)
            else:

                soft = pya.locateCenterOnScreen(soft_png, grayscale=True, confidence=0.7)

                open_fifa = pya.locateCenterOnScreen(open_fifa_png, grayscale=True, confidence=0.7)

                if open_fifa != None:
                    print("got soft banned (open fifa or wait)")
                    exit(1)

                if soft != None:
                    print("got soft banned")
                    exit(1)

                failed = pya.locateCenterOnScreen(failed_img, grayscale = True, confidence = 0.7)
                time.sleep(0.1)

                if failed != None:
                    missed += 1
                    pya.click(125, 190)
                    time.sleep(0.5)
                else:
                    won_bid = pya.locateCenterOnScreen(won_bid_img, grayscale=True, confidence=0.7)
                    time.sleep(0.2)

                    if won_bid != None:

                        buy_time = time.time()

                        bought += 1
                        transfer_list += 1

                        price = pya.screenshot(region=(1720, 625, 43, 20))
                        # name = pya.screenshot(region=(1590, 672, 28, 310))

                        # name.save("name.png")
                        price.save("price.png")

                        # time.sleep(0.2)

                        # name_cv = cv2.imread('price.png', 0)
                        # thresh = cv2.threshold(name_cv, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                        # data_name = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')
                        # # data_name = re.sub("[^0-9]", "", data_name)
                        # if not data_price.isnumeric():
                        #     names = pd.read_excel('player_futbin_data.xlsx')
                        #     # Check if data_name matches any value in "Player Name" column
                        #     matches = names.loc[names['Player Name'] == data_name]
                        #     if not matches.empty:
                        #         # Check if corresponding row has "Normal" in "Card Type" column
                        #         type_matches = matches.loc[matches['Card Type'] == card_type]
                        #         if not type_matches.empty:
                        #             # Get value from "ID" column
                        #             ID = type_matches.iloc[0]['ID']
                        #             print(ID)

                        price_cv = cv2.imread('price.png', 0)
                        thresh = cv2.threshold(price_cv, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                        data_price = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')
                        data_price = re.sub("[^0-9]", "", data_price)
                        if data_price.isnumeric():
                            purchases.append(int(data_price))
                            total_earned = total_earned + 0.95 * current_price - int(data_price)
                            total_spent += int(data_price)
                            print("\nBought for:", data_price, "\nTotal possibly earned:", total_earned, "\nTotal spent:", total_spent)

                    if KRSU:
                        time.sleep(0.5)
                        pya.click(1750,750)
                        time.sleep(0.5)
                        rarity = pya.screenshot(region=(1585, 618, 200, 25))

                        rarity.save("rarity.png")

                        rarity_cv = cv2.imread('rarity.png', 0)
                        thresh_r = cv2.threshold(rarity_cv, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                        data_rarity = pytesseract.image_to_string(thresh_r, lang='eng', config='--psm 6')

                        rare_str = 'Rare'
                        dupe = pya.locateCenterOnScreen(dupe_png, grayscale=True, region=(1550, 750, 500, 100), confidence=0.8)

                        time.sleep(0.5)

                        if dupe == None:
                            if rare_str in data_rarity:
                                time.sleep(0.1)
                                pya.click(1600, 325)  # exit bio
                                time.sleep(1)
                                pya.click(1750, 800)  # add to club
                                time.sleep(0.5)
                                pya.click(125, 190)  # back to search
                                time.sleep(0.5)
                            else:
                                time.sleep(0.1)
                                pya.click(1600, 325)  # exit bio
                                time.sleep(1)
                                #     # preform act of selling the player
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
                                pya.click(125, 190)
                                time.sleep(0.5)
                        else:
                            time.sleep(0.1)
                            pya.click(1600, 325)  # exit bio
                            time.sleep(1)
                            #     # preform act of selling the player
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
                            pya.click(125, 190)
                            time.sleep(0.5)


                    if only_buy:
                        if dupe == None:
                            dupe = pya.locateCenterOnScreen(dupe_png, grayscale=True, region=(1550, 750, 500, 100), confidence=0.8)

                            time.sleep(0.5)
                            time.sleep(0.5)
                            pya.click(1750, 800)
                            time.sleep(0.5)
                            pya.click(125, 190)
                            time.sleep(0.5)
                        else:
                            time.sleep(0.1)
                            pya.click(1600, 325)  # exit bio
                            time.sleep(1)
                            #     # preform act of selling the player
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
                            pya.click(125, 190)
                            time.sleep(0.5)


                    if only_sell:
                        #     # preform act of selling the player
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
                        pya.click(125, 190)
                        time.sleep(0.5)

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


        if keyboard.is_pressed("="):
            print("keyboard interrupt")
            break
        if keyboard.is_pressed("-"):
            print("keyboard interrupt - pause")
            time.sleep(20)

        if keyboard.is_pressed('p'):
            paused = not paused
            print("Paused" if paused else "Resumed")
            time.sleep(3)  # delay to avoid rapid toggling of pause state

        if loop_count == 3:

            team = pya.locateCenterOnScreen(team_png, grayscale=True, region=(800, 500, 700, 400), confidence=0.8)

            if team != None:
                pya.click(1500, 630)
                time.sleep(1)

            time.sleep(random_int / 2)
            long_session_count += 1
            searches += 1

            # if random_int == 5:
            #     if loop_count < 3:
            #         loop_count +=1
            # else:
            loop_count = 0
            # if bid_price != None:
            pya.click(1300, 915) # move to + button
            time.sleep(0.5)
            pya.click(1600, 1300)
            time.sleep(0.5)
            #     # perform the act of buying the player
            pya.doubleClick(1750, 830)
            pya.doubleClick(1750, 830)
            pya.doubleClick(1750, 830)
            pya.doubleClick(1750, 830)
            time.sleep(0.11)
            pya.click(1260, 800)
            time.sleep(0.5)

            no_res = pya.locateCenterOnScreen(no_res_img, grayscale = True, region = (1200, 800, 300, 100), confidence = 0.8)
            time.sleep(0.1)

            if no_res != None:
                pya.click(125, 190)
                time.sleep(0.5)
            else:

                soft = pya.locateCenterOnScreen(soft_png, grayscale=True, confidence=0.7)

                open_fifa = pya.locateCenterOnScreen(open_fifa_png, grayscale=True, confidence=0.7)

                if open_fifa != None:
                    print("got soft banned (open fifa or wait)")
                    exit(1)

                if soft != None:
                    print("got soft banned")
                    exit(1)

                failed = pya.locateCenterOnScreen(failed_img, grayscale = True, confidence = 0.7)
                time.sleep(0.1)

                if failed != None:
                    missed += 1
                    pya.click(125, 190)
                    time.sleep(0.5)
                else:
                    won_bid = pya.locateCenterOnScreen(won_bid_img, grayscale=True, confidence=0.7)
                    time.sleep(0.2)

                    if won_bid != None:

                        buy_time = time.time()

                        bought += 1
                        transfer_list += 1

                        price = pya.screenshot(region=(1720, 625, 43, 20))
                        # name = pya.screenshot(region=(1590, 672, 28, 310))

                        # name.save("name.png")
                        price.save("price.png")

                        # time.sleep(0.2)

                        # name_cv = cv2.imread('price.png', 0)
                        # thresh = cv2.threshold(name_cv, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                        # data_name = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')
                        # # data_name = re.sub("[^0-9]", "", data_name)
                        # if not data_price.isnumeric():
                        #     names = pd.read_excel('player_futbin_data.xlsx')
                        #     # Check if data_name matches any value in "Player Name" column
                        #     matches = names.loc[names['Player Name'] == data_name]
                        #     if not matches.empty:
                        #         # Check if corresponding row has "Normal" in "Card Type" column
                        #         type_matches = matches.loc[matches['Card Type'] == card_type]
                        #         if not type_matches.empty:
                        #             # Get value from "ID" column
                        #             ID = type_matches.iloc[0]['ID']
                        #             print(ID)

                        price_cv = cv2.imread('price.png', 0)
                        thresh = cv2.threshold(price_cv, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                        data_price = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')
                        data_price = re.sub("[^0-9]", "", data_price)
                        if data_price.isnumeric():
                            purchases.append(int(data_price))
                            total_earned = total_earned + 0.95 * current_price - int(data_price)
                            total_spent += int(data_price)
                            print("\nBought for:", data_price, "\nTotal possibly earned:", total_earned, "\nTotal spent:", total_spent)

                    if KRSU:
                        time.sleep(0.5)
                        pya.click(1750,750)
                        time.sleep(0.5)
                        rarity = pya.screenshot(region=(1585, 618, 200, 25))

                        rarity.save("rarity.png")

                        rarity_cv = cv2.imread('rarity.png', 0)
                        thresh_r = cv2.threshold(rarity_cv, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                        data_rarity = pytesseract.image_to_string(thresh_r, lang='eng', config='--psm 6')

                        rare_str = 'Rare'
                        dupe = pya.locateCenterOnScreen(dupe_png, grayscale=True, region=(1550, 750, 500, 100), confidence=0.8)

                        time.sleep(0.5)

                        if dupe == None:
                            if rare_str in data_rarity:
                                time.sleep(0.1)
                                pya.click(1600, 325)  # exit bio
                                time.sleep(1)
                                pya.click(1750, 800)  # add to club
                                time.sleep(0.5)
                                pya.click(125, 190)  # back to search
                                time.sleep(0.5)
                            else:
                                time.sleep(0.1)
                                pya.click(1600, 325)  # exit bio
                                time.sleep(1)
                                #     # preform act of selling the player
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
                                pya.click(125, 190)
                                time.sleep(0.5)
                        else:
                            time.sleep(0.1)
                            pya.click(1600, 325)  # exit bio
                            time.sleep(1)
                            #     # preform act of selling the player
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
                            pya.click(125, 190)
                            time.sleep(0.5)


                    if only_buy:
                        if dupe == None:
                            dupe = pya.locateCenterOnScreen(dupe_png, grayscale=True, region=(1550, 750, 500, 100), confidence=0.8)

                            time.sleep(0.5)
                            time.sleep(0.5)
                            pya.click(1750, 800)
                            time.sleep(0.5)
                            pya.click(125, 190)
                            time.sleep(0.5)
                        else:
                            time.sleep(0.1)
                            pya.click(1600, 325)  # exit bio
                            time.sleep(1)
                            #     # preform act of selling the player
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
                            pya.click(125, 190)
                            time.sleep(0.5)

                    if only_sell:
                        #     # preform act of selling the player
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
                        pya.click(125, 190)
                        time.sleep(0.5)

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


        if keyboard.is_pressed("="):
            print("keyboard interrupt")
            break
        if keyboard.is_pressed("-"):
            print("keyboard interrupt - pause")
            time.sleep(20)
        if keyboard.is_pressed('p'):
            paused = not paused
            print("Paused" if paused else "Resumed")
            time.sleep(3)  # delay to avoid rapid toggling of pause state

        if loop_count == 0:

            team = pya.locateCenterOnScreen(team_png, grayscale=True, region=(800, 500, 700, 400), confidence=0.8)

            if team != None:
                pya.click(1500, 630)
                time.sleep(1)

            time.sleep(random_int / 2)
            long_session_count += 1
            searches += 1

            loop_count +=1
            #     # if bid_price != None:
            pya.click(830, 800)  # move to - button
            time.sleep(0.5)
            pya.click(1600, 1300)
            time.sleep(0.5)

            #     # perform the act of buying the player
            pya.doubleClick(1750, 830)
            pya.doubleClick(1750, 830)
            pya.doubleClick(1750, 830)
            pya.doubleClick(1750, 830)
            time.sleep(0.11)
            pya.click(1260, 800)
            time.sleep(0.5)

            no_res = pya.locateCenterOnScreen(no_res_img, grayscale=True, region=(1200, 800, 300, 100), confidence = 0.8)
            time.sleep(0.1)

            if no_res != None:
                pya.click(125, 190)
                time.sleep(0.5)
            else:

                soft = pya.locateCenterOnScreen(soft_png, grayscale=True, confidence=0.7)

                open_fifa = pya.locateCenterOnScreen(open_fifa_png, grayscale=True, confidence=0.7)

                if open_fifa != None:
                    print("got soft banned (open fifa or wait)")
                    exit(1)

                if soft != None:
                    print("got soft banned")
                    exit(1)

                failed = pya.locateCenterOnScreen(failed_img, grayscale=True, region=(2000, 150, 400, 200), confidence = 0.7)

                time.sleep(0.5)

                if failed != None:
                    missed += 1
                    pya.click(125, 190)
                    time.sleep(0.5)
                else:

                    won_bid = pya.locateCenterOnScreen(won_bid_img, grayscale=True, confidence=0.7)


                    time.sleep(0.2)

                    if won_bid != None:

                        buy_time = time.time()

                        bought += 1
                        transfer_list += 1
                        price = pya.screenshot(region=(1720, 625, 43, 20))
                        price.save("price.png")

                        # time.sleep(0.75)
                        # pya.click(1750, 750) # click on bio
                        # time.sleep(0.75)
                        # name = pya.screenshot(region=(1590, 672, 310, 28)) #screenshot name in bio

                        # name.save("name.png")

                        # time.sleep(0.5)
                        #
                        # pya.click(1612, 325) #click back to main player page
                        #
                        # time.sleep(0.2)

                        # name_cv = cv2.imread('name.png', 0)
                        # thresh = cv2.threshold(name_cv, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                        # data_name = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')
                        # data_name = data_name.replace(" ", "-")
                        # data_name = data_name.lower()
                        # print(f'Name: {data_name}')
                        # # data_name = re.sub("[^0-9]", "", data_name)
                        # if not data_name.isnumeric():
                        #     print("310")
                        #
                        #     # Check if data_name matches any value in "Player Name" column
                        #     matches = names.loc[names['Player Name'] == data_name]
                        #     print(f'Matches {matches}')
                        #     if not matches.empty:
                        #         print("315")
                        #         # Check if corresponding row has "Normal" in "Card Type" column
                        #         type_matches = matches.loc[matches['Card Type'] == card_type]
                        #         print(f'Type Matches {type_matches}')
                        #         if not type_matches.empty:
                        #             # Get value from "ID" column
                        #             ID = type_matches.iloc[0]['ID']
                        #             print(f'ID :{ID}')

                        price_cv = cv2.imread('price.png', 0)
                        thresh = cv2.threshold(price_cv, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                        data_price = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')
                        data_price = re.sub("[^0-9]", "", data_price)
                        if data_price.isnumeric():
                            purchases.append(int(data_price))
                            total_earned = total_earned + 0.95 * current_price - int(data_price)
                            total_spent += int(data_price)
                            print("\nBought for:", data_price, "\nTotal possibly earned:", total_earned,
                                  "\nTotal spent:", total_spent)

                    if KRSU:
                        time.sleep(0.5)
                        pya.click(1750,750)
                        time.sleep(0.5)
                        rarity = pya.screenshot(region=(1585, 618, 200, 25))

                        rarity.save("rarity.png")

                        rarity_cv = cv2.imread('rarity.png', 0)
                        thresh_r = cv2.threshold(rarity_cv, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                        data_rarity = pytesseract.image_to_string(thresh_r, lang='eng', config='--psm 6')

                        rare_str = 'Rare'
                        dupe = pya.locateCenterOnScreen(dupe_png, grayscale=True, region=(1550, 750, 500, 100), confidence=0.7)

                        time.sleep(0.5)

                        if dupe == None:
                            if rare_str in data_rarity:
                                time.sleep(0.1)
                                pya.click(1600, 325)  # exit bio
                                time.sleep(1)
                                pya.click(1750, 800)  # add to club
                                time.sleep(0.5)
                                pya.click(125, 190)  # back to search
                                time.sleep(0.5)
                            else:
                                time.sleep(0.1)
                                pya.click(1600, 325)  # exit bio
                                time.sleep(1)
                                #     # preform act of selling the player
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
                                pya.click(125, 190)
                                time.sleep(0.5)
                        else:
                            time.sleep(0.1)
                            pya.click(1600, 325)  # exit bio
                            time.sleep(1)
                            #     # preform act of selling the player
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
                            pya.click(125, 190)
                            time.sleep(0.5)



                    if only_buy:
                        dupe = pya.locateCenterOnScreen(dupe_png, grayscale=True, region=(1550, 750, 500, 100), confidence=0.8)

                        time.sleep(0.5)
                        if dupe == None:
                            time.sleep(0.5)
                            pya.click(1750, 800)
                            time.sleep(0.5)
                            pya.click(125, 190)
                            time.sleep(0.5)
                        else:
                            time.sleep(0.1)
                            pya.click(1600, 325)  # exit bio
                            time.sleep(1)
                            #     # preform act of selling the player
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
                            pya.click(125, 190)
                            time.sleep(0.5)

                    if only_sell:
                        #     # preform act of selling the player
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
                        pya.click(125, 190)
                        time.sleep(0.5)
        print('\ntotal searches: ', searches)
        print('total sniped: ', bought)
        print("Total possibly earned:", total_earned, "\nTotal spent:", total_spent, "\nTotal missed:", missed)
        current_time = time.time()
        total_time = current_time-start_time
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
            delta = timedelta(seconds=since_last-8)
            # Extract the hours, minutes, and seconds from the timedelta object
            hours, remainder = divmod(delta.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            print(f"time since last purchase: {hours:02d}:{minutes:02d}:{seconds:02d}")
        print(f"transfer list has been cleared {TL_clears} times")



    if keyboard.is_pressed('p'):
        paused = not paused
        print("Paused" if paused else "Resumed")
        time.sleep(3)  # delay to avoid rapid toggling of pause state

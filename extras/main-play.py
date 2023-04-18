import time
import re
import pyautogui as pyd
from PIL import Image
import pydirectinput as pya
logo = None

radar_image = Image.open('../images/radar.png')
logo_left_img = Image.open("../images/logoleft.png")
logo_img = Image.open("../images/logo.png")
diff_img = Image.open("../images/Difficulty.png")
s_img = Image.open("../images/squad_battle.png")
npc_img = Image.open('../images/npc.png')
y = [2]
u = [2, 12, 25]
Diff_location = None
squad_battle = 20
battlecount = 0
diffcount = 0
radar_old = 99999
time.sleep(3)
while 0 < 1:
    # print(battlecount)


    if diffcount == 25:
        diffcount = 0



    if battlecount == 3:
        battlecount = 0

    if diffcount in u:
        squad_battle = pyd.locateCenterOnScreen(s_img, region=(250, 0, 500, 200), confidence=0.7)

    count = 0
    if squad_battle == None:
        if diffcount == 0:
            Diff_location = pyd.locateCenterOnScreen(diff_img, confidence=0.7)
    while Diff_location != None:
        print(count)
        time.sleep(.25)
        if count == 0:
            pya.click(358, 834)
            pya.click(358, 834)
            time.sleep(0.25)
            Diff_location = pyd.locateCenterOnScreen(diff_img, confidence=0.7)
            if Diff_location == None:
                pya.press('enter')
                time.sleep(0.25)
                pya.click(300, 733)
                pya.click(300, 733)
                time.sleep(0.25)
                pya.press('enter')
                time.sleep(4)
                pya.press('enter')
                time.sleep(2)
                pya.press('enter')
                time.sleep(2)
                pya.press('enter')
                time.sleep(2)
                pya.press('enter')
                time.sleep(2)
                pya.press('enter')
                time.sleep(2)
                pya.press('enter')
        if count == 1:
            pya.click(255, 834)
            pya.click(255, 834)
            time.sleep(0.25)
            Diff_location = pyd.locateCenterOnScreen(diff_img, confidence=0.7)
            if Diff_location == None:
                pya.press('enter')
                pya.click(300, 733)
                pya.click(300, 733)
                time.sleep(0.25)
                pya.press('enter')
                time.sleep(4)
                pya.press('enter')
                time.sleep(2)
                pya.press('enter')
                time.sleep(2)
                pya.press('enter')
                time.sleep(2)
                pya.press('enter')
                time.sleep(2)
                pya.press('enter')
                time.sleep(2)
                pya.press('enter')
        if count == 2:
            pya.click(261, 685)
            pya.click(261, 685)
            time.sleep(0.25)
            Diff_location = pyd.locateCenterOnScreen(diff_img, confidence=0.7)
            if Diff_location == None:
                pya.press('enter')
                pya.click(300, 733)
                pya.click(300, 733)
                time.sleep(0.25)
                pya.press('enter')
                time.sleep(4)
                pya.press('enter')
                time.sleep(2)
                pya.press('enter')
                time.sleep(2)
                pya.press('enter')
                time.sleep(2)
                pya.press('enter')
                time.sleep(2)
                pya.press('enter')
                time.sleep(2)
                pya.press('enter')
        if count == 3:
            pya.click(398, 685)
            pya.click(398, 685)
            time.sleep(0.25)
            Diff_location = pyd.locateCenterOnScreen(diff_img, confidence=0.7)
            if Diff_location == None:
                pya.press('enter')
                pya.click(300, 733)
                pya.click(300, 733)
                time.sleep(0.25)
                pya.press('enter')
                time.sleep(4)
                pya.press('enter')
                time.sleep(2)
                pya.press('enter')
                time.sleep(2)
                pya.press('enter')
                time.sleep(2)
                pya.press('enter')
                time.sleep(2)
                pya.press('enter')
                time.sleep(2)
                pya.press('enter')
        count = count + 1

        if count == 4:
            pya.press('s')
            count = 0
            time.sleep(2)




    if squad_battle != None:
        if battlecount == 0:
            logo = pyd.locateCenterOnScreen(logo_img, confidence=0.9, grayscale=True, region=(2150,1100,300,300))
            logo_left = pyd.locateCenterOnScreen(logo_img, confidence=0.9, grayscale=True, region=(0, 1100, 400, 300))
            print(logo_left)

        # time.sleep(0.05)
        # sanchez = pyd.locateCenterOnScreen("sanchez.png", confidence=0.7)
        # print(sanchez)

        radar = pyd.locateCenterOnScreen(radar_image, grayscale=True, confidence=0.72, region = (1000, 1100, 500, 400))
        radar = str(radar)
        if radar == "None":
            print("no radar")
            pya.press('l')


        if radar != "None":
            radar_coords = re.match("Point\(x=(?P<x>\d+), y=(?P<y>\d+)\)",radar).groupdict()
            radar_new = int(radar_coords['x'])
            radar_dist = radar_new - radar_old
            print(radar_dist)
            if logo != None:
                if radar_new >= 1175:
                    x_dist_1 = radar_new - 1000


                    if radar_dist >= 10:
                        pya.keyDown('a')
                        time.sleep(0.1)
                        pya.keyDown('l')
                        time.sleep(0.4)
                        pya.keyUp('l')
                        pya.keyUp('a')
                        print('right side defend')

                    if radar_dist < 10:
                        npc = pyd.locateCenterOnScreen(npc_img, grayscale=True, confidence=0.75, region=(1000, 1100, x_dist_1, 400))
                        if npc != None:
                            if int(radar_coords['y']) <= 1200:
                                pya.keyDown('a')
                                pya.keyDown('s')
                                time.sleep(0.35)
                                pya.press('l')
                                time.sleep(0.05)
                                pya.keyUp('a')
                                pya.keyUp('s')
                                print('right side pass top')

                            elif int(radar_coords['y']) >= 1300:
                                pya.keyDown('a')
                                pya.keyDown('w')
                                time.sleep(0.35)
                                pya.press('l')
                                time.sleep(0.05)
                                pya.keyUp('a')
                                pya.keyUp('w')
                                print('right side pass bottom')
                            else:
                                pya.keyDown('a')
                                time.sleep(0.35)
                                pya.press('l')
                                time.sleep(0.05)
                                pya.keyUp('a')
                                print('right side pass mid')
                        else:
                            if int(radar_coords['y']) <= 1200:
                                pya.keyDown('a')
                                pya.keyDown('s')
                                time.sleep(0.40)
                                pya.keyUp('a')
                                pya.keyUp('s')
                                print('right side move top')

                            elif int(radar_coords['y']) >= 1300:
                                pya.keyDown('a')
                                pya.keyDown('w')
                                time.sleep(0.40)
                                pya.keyUp('a')
                                pya.keyUp('w')
                                print('right side move bottom')
                            else:
                                pya.keyDown('a')
                                time.sleep(0.40)
                                pya.keyUp('a')
                                print('right side move mid')
                if radar_new < 1200:
                    if int(radar_coords['y']) >= 1250:
                        pya.keyDown('a')
                        pya.keyDown('w')
                        time.sleep(0.35)
                        pya.keyDown('space')
                        time.sleep(0.2)
                        pya.keyUp('space')
                        time.sleep(0.05)
                        pya.keyUp('a')
                        pya.keyUp('w')
                        print('right side shot bottom')
                    else:
                        pya.keyDown('a')
                        pya.keyDown('s')
                        time.sleep(0.35)
                        pya.keyDown('space')
                        time.sleep(0.2)
                        pya.keyUp('space')
                        time.sleep(0.05)
                        pya.keyUp('a')
                        pya.keyUp('s')
                        print('right side shot top')


            if logo_left != None:
                if radar_new < 1350:
                    if radar_dist <= -10:
                        pya.keyDown('d')
                        pya.keyDown('l')
                        time.sleep(0.4)
                        pya.keyUp('l')
                        pya.keyUp('d')
                        print('left side defend')

                    if radar_dist > -10:
                        x_dist_2 = 1500 - radar_new
                        npc = pyd.locateCenterOnScreen(npc_img, grayscale=True, confidence=0.75, region=(radar_new, 1100, x_dist_2, 400))
                        if npc != None:
                            if int(radar_coords['y']) <= 1200:
                                pya.keyDown('d')
                                pya.keyDown('s')
                                time.sleep(0.35)
                                pya.press('l')
                                time.sleep(0.05)
                                pya.keyUp('d')
                                pya.keyUp('s')
                                print('left side pass top')

                            elif int(radar_coords['y']) >= 1300:
                                pya.keyDown('d')
                                pya.keyDown('w')
                                time.sleep(0.35)
                                pya.keyDown('l')
                                time.sleep(0.05)
                                pya.keyUp('d')
                                pya.keyUp('w')
                                print('left side pass bottom')
                            else:
                                pya.keyDown('d')
                                time.sleep(0.35)
                                pya.press('l')
                                time.sleep(0.05)
                                pya.keyUp('d')
                                print('left side pass mid')
                        else:
                            if int(radar_coords['y']) <= 1200:
                                pya.keyDown('d')
                                pya.keyDown('s')
                                time.sleep(0.40)
                                pya.keyUp('d')
                                pya.keyUp('s')
                                print('left side move top')

                            elif int(radar_coords['y']) >= 1300:
                                pya.keyDown('d')
                                pya.keyDown('w')
                                time.sleep(0.40)
                                pya.keyUp('d')
                                pya.keyUp('w')
                                print('left side move bottom')
                            else:
                                pya.keyDown('d')
                                time.sleep(0.40)
                                pya.keyUp('d')
                                print('left side move mid')

                if radar_new >= 1350:
                    if int(radar_coords['y']) >= 1250:
                        pya.keyDown('d')
                        pya.keyDown('w')
                        time.sleep(0.35)
                        pya.keyDown('space')
                        time.sleep(0.2)
                        pya.keyUp('space')
                        time.sleep(0.05)
                        pya.keyUp('d')
                        pya.keyUp('w')
                        print('left side shot bottom')
                    else:
                        pya.keyDown('d')
                        pya.keyDown('s')
                        time.sleep(0.35)
                        pya.keyDown('space')
                        time.sleep(0.2)
                        pya.keyUp('space')
                        time.sleep(0.05)
                        pya.keyUp('d')
                        pya.keyUp('s')
                        print('left side shot top')

            radar_old = int(radar_coords['x'])
    if squad_battle == None:
        if diffcount in y:
            pya.press('enter')
            pya.press('l')

    battlecount += 1
    diffcount += 1






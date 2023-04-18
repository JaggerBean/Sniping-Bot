import numpy as np
import cv2
from PIL import ImageGrab, Image
import pyautogui as pyd
import pydirectinput as pya

radar_img = cv2.imread('radar.png',0)
h_r, w_r = radar_img.shape
logo_img = cv2.imread('logo.png',0)
h_l, w_l = logo_img.shape
PIB_img = cv2.imread('PIB.png',0)
h_p, w_p = PIB_img.shape
difficulty_img = cv2.imread('Difficulty.png',0)
h_d, w_d = difficulty_img.shape
squad_b_img = cv2.imread('squad_battle.png',0)
h_s, w_s = squad_b_img.shape
test_img = cv2.imread('test_pic.png', 0)
radar_img_cv = cv2.cvtColor(np.array(radar_img), cv2.COLOR_RGB2BGR)
logo_img_cv = cv2.cvtColor(np.array(logo_img), cv2.COLOR_RGB2BGR)
PIB_img_cv = cv2.cvtColor(np.array(PIB_img), cv2.COLOR_RGB2BGR)
difficulty_img_cv = cv2.cvtColor(np.array(difficulty_img), cv2.COLOR_RGB2BGR)
squad_b_img_cv = cv2.cvtColor(np.array(squad_b_img), cv2.COLOR_RGB2BGR)

methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED,
           cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]

# for method in methods:
#     print(method)
#     screen2 = screen_cv.copy()
#     print('screen2:', screen2.dtype, screen2.shape)
#     print('test_img:', test_img.dtype, test_img_cv.shape)
#     result = cv2.matchTemplate(screen2, test_img_cv, method)
#     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
#     if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
#         location = min_loc
#     else:
#         location = max_loc
#
#     bottom_right = (location[0] + w/2, location[1] + h/2)
#     print(bottom_right)
#     pyd.moveTo(bottom_right)

while 0 < 1:
    screen = ImageGrab.grab(bbox=(0, 0, 400, 400))
    screen_cv = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

    result = cv2.matchTemplate(screen_cv, logo_img_cv, methods[1])
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    location = min_loc

    bottom_right = (location[0] + w_l/2, location[1] + h_l/2)
    print(bottom_right)
    # pyd.moveTo(bottom_right)

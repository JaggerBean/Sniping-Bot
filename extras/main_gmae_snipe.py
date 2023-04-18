import random
import time
from PIL import Image
import pyautogui as pya
import pydirectinput as pyd
import cv2
import pytesseract
import re
import keyboard
import pandas as pd
import time
print('yo')
time.sleep(1)

expired_png = Image.open('../images/expired.png')
AB_png = Image.open('../images/AB.png')
expired = None
while 0 < 1:
    pyd.press('down')
    pyd.press('enter')
    pyd.press('down')
    pyd.press('left')
    pyd.press('d')

    
    time.sleep(0.9)
    pyd.press('enter')
    # time.sleep(0.03)
    pyd.press('down')
    # time.sleep(0.03)
    pyd.press('enter')
    # time.sleep(0.03)
    pyd.press('down')
    # time.sleep(0.03)
    pyd.press('enter')
    print('bought')
    time.sleep(2)
    expired = pya.locateCenterOnScreen(expired_png, confidence=0.7)
    AB = pya.locateCenterOnScreen(AB_png, confidence=0.7)
    print(f'AB {AB}')
    print(f'expired {expired}')
    time.sleep(2.5)
    if expired != None:
        print('exp loop')
        pya.press('enter')
        time.sleep(0.5)
        pya.press('escape')
        time.sleep(1)
        pya.press('escape')
        time.sleep(1)
    if AB != None:
        pyd.press('escape')
        time.sleep(0.5)
        pyd.press('up')
        time.sleep(0.5)
        pyd.press('up')
        time.sleep(0.5)
        pyd.press('escape')
        time.sleep(0.5)
        pyd.press('up')
        time.sleep(0.5)
    else:
        pyd.press('enter')
        time.sleep(2.5)
        pyd.press('e')
        time.sleep(2.5)
        pyd.press('escape')
        time.sleep(2.5)

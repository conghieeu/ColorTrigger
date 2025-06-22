import cv2
import numpy as np
import pyautogui
import mss
import time
from enum import Enum
from pynput.mouse import Listener as MouseListener

pyautogui.FAILSAFE = False
is_right_mouse_down = False
purple = [201, 47, 204]
yellow = [30, 255, 255]
cyan = [255, 255, 0] 
shot_count = 0

def on_mouse_click(x, y, button, pressed):
    global is_right_mouse_down
    if button == button.right:
        is_right_mouse_down = pressed
mouse_listener = MouseListener(on_click=on_mouse_click)
mouse_listener.start()

def get_color_limits(color):
    c = np.uint8([[color]])
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
    lowerLimit = hsvC[0][0][0] - 10, 100, 100
    upperLimit = hsvC[0][0][0] + 10, 255, 255
    lowerLimit = np.array(lowerLimit, dtype=np.uint8)
    upperLimit = np.array(upperLimit, dtype=np.uint8)
    return lowerLimit, upperLimit

def is_color_present(image, color):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_color, upper_color = get_color_limits(color)
    mask = cv2.inRange(hsv, lower_color, upper_color)
    return cv2.countNonZero(mask) > 0

def detect_and_shoot(purple, cyan):
    global is_right_mouse_down, shot_count
    with mss.mss() as sct:
        screen_width, screen_height = pyautogui.size()
        # Xác định vùng giữa màn hình với kích thước 5x5 pixel
        monitor = {
        "top": screen_height // 2 - 4,
        "left": screen_width // 2 - 4,
        "width": 8,
        "height": 8,
    }
        while True: 
            screenshot = sct.grab(monitor)
            image = np.array(screenshot)  
            if is_color_present(image, cyan) and is_color_present(image, purple) and is_right_mouse_down:
                pyautogui.press("J") 
                time.sleep(0.04)
                pyautogui.press("M") 
                shot_count += 1   
                print("SHOT " + str(shot_count))

detect_and_shoot(purple, cyan) 
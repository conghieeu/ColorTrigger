import cv2
import numpy as np
import pyautogui
import mss
import time
from enum import Enum
from pynput.mouse import Listener as MouseListener


# Biến toàn cục để theo dõi trạng thái chuột phải
is_right_mouse_down = False


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


def is_purple_present(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    purple = [201, 47, 204]
    lower_purple, upper_purple = get_color_limits(purple)
    mask = cv2.inRange(hsv, lower_purple, upper_purple)
    return cv2.countNonZero(mask) > 0


# nhận diện màu vàng
def is_yellow_present(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    yellow = [30, 255, 255]
    lower_yellow, upper_yellow = get_color_limits(yellow)
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    return cv2.countNonZero(mask) > 0


def main_logic():
    pyautogui.FAILSAFE = False  # Tắt tính năng an toàn (không khuyến khích)
    global is_right_mouse_down
    
    count = 0  # Thêm biến đếm

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
            # Quét màn hình
            screenshot = sct.grab(monitor)
            image = np.array(screenshot) 
            
            if is_yellow_present(image) and is_purple_present(image) and is_right_mouse_down:
                pyautogui.press("P") 
                time.sleep(0.05)
                pyautogui.press("M") 
                count += 1   
                print("SHOT " + str(count))  

main_logic()
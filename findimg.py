import cv2
import numpy as np
from PIL import Image
import pyautogui
import time
from lib import getWindow


window_title = "Administrator:  cmd_rokauto"
window = getWindow(window_title)
x, y = pyautogui.size()
new_x = x - 270
new_y = 200
window.move_window(x=new_x, y=new_y, width=270, height=300)

from pywinauto import Desktop
from pywinauto.findwindows import ElementNotFoundError
from PIL import Image
import time
from lib import capture_window_screenshot 

# Đặt tiêu đề cửa sổ
window_title = 'Rise of Kingdoms'

screenshot =  capture_window_screenshot(window_title)

screenshot.save("screenshot_5.png")

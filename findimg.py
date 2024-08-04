import cv2
import numpy as np
from PIL import Image
import pyautogui
from pywinauto import Application
import time
from lib import (
    PressKeyandRelease,
    find_image_in_image,
    filter_close_points,
    capture_window_screenshot,
)


window_title = "Rise of Kingdoms"

# Khởi tạo ứng dụng pywinauto
app = Application(backend="win32").connect(title=window_title)


# Kết nối với cửa sổ
window = app[window_title]

# Đưa cửa sổ lên phía trước và đợi để chắc chắn nó đã được kích hoạt
window.set_focus()


# img_find = Image.open("refurn_gather.png")
# locations, w, h = find_image_in_image(screenshot, img_find, threshold=0.9)
# if locations:
#     x = locations[0][0] + left
#     y = locations[0][1] + top

#     # pyautogui.click(x, y)
#     # print(locations[0][0], locations[0][1])
#     print(x, y)

screenshot, left, top, right, bottom = capture_window_screenshot(window_title)

screen_width, screen_height = pyautogui.size()

x = 1500
y = 170
width, height = screenshot.size

crop_coordinates = (1530, 200, 1600, 530)

# main_find = Image.open("ddd.png")

cropped_image = screenshot.crop(crop_coordinates)


image_width, image_height = cropped_image.size


part_height = image_height // 5

cropped_parts = []


farm = Image.open("./img/farm.png")
run = Image.open("./img/run.png")
stop = Image.open("dungchan.png")
re = Image.open("./img/return.png")


status = [
    {"name": "farm", "pil": farm},
    {"name": "run", "pil": run},
    {"name": "return", "pil": re},
    {"name": "stop", "pil": stop},
]

teams = []


for i in range(5):
    bottom = (i + 1) * part_height
    cropped_part = cropped_image.crop((0, i * part_height, image_width, bottom))
    # cropped_part.show()
    # cropped_part_path = f"cropped_part_{i+1}.png"
    img_find = Image.open("./img/farm.png")

    for item in status:
        # print(f"name: {item['name']}, pil: {item['pil']}")
        locations, w, h = find_image_in_image(cropped_part, item["pil"], threshold=0.7)
        # print(locations)
        if locations:
            x = locations[0][0] + left
            y = locations[0][1] + top
            print("farming gem")
            teams.append({"number": i, "status": item["name"]})

    # print(teams)



#dung tat ca cac team
for team in teams:
    match team['status']:
        case "return":
            print("return")

#go home

if len(teams) < 5:
    print("new team")
    img_find = Image.open("./img/home.png")
    locations, w, h = find_image_in_image(screenshot, item["pil"], threshold=0.7)
    if locations:
        x = locations[0][0] + left
        y = locations[0][1] + top
        print("map")
    else:
        print("home")


for team in teams:
    match team['status']:
        case "run":
            continue
        case "stop":
            print("stop")
        case "farm":
            continue
# time.sleep(60)
# yy = 100 * 2
# x = 1540 + left
# y = 260 + top + yy
# pyautogui.click(x, y)

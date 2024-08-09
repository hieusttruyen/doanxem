import cv2
import numpy as np
from PIL import Image, ImageEnhance
import pyautogui
import time
from lib import getWindow, FindImgInWindow, FindImg , window_capture


window_title = "Rise of Kingdoms"
window = getWindow(window_title)

window.move_window(0, 0)
window.set_focus()
time.sleep(2)


farming = Image.open("./img/farm.png")
run = Image.open("./img/run.png")
stop = Image.open("./img/dungchan.png")
re = Image.open("./img/return.png")
status = [
    {"name": "farming", "pil": farming},
    {"name": "run", "pil": run},
    {"name": "return", "pil": re},
    {"name": "stop", "pil": stop},
]


def CheckTeams(window):
    print("Kiểm tra quân dội...")
    try:
        screenshot = window_capture(window)
        # x, y = screenshot.size
        crop_coordinates = (1600 - 80, 180, 1600, 550)
        cropped_image = screenshot.crop(crop_coordinates)
        cropped_image.show()
        image_width, image_height = cropped_image.size
        part_height = image_height // 5
        teams = []
        team_number = 4  # int(sys.argv[2])

        for i in range(team_number + 1):
            bottom = (i + 1) * part_height
            cropped_part = cropped_image.crop((0, i * part_height, image_width, bottom))
            # cropped_part.show()
            for item in status:
                locations = FindImg(cropped_part, item["pil"], threshold=0.7)
                if locations:
                    teams.append({"number": i, "status": item["name"]})
        return teams
    except Exception as ex:
        print("ERROR: ", ex)


img_gem_map = Image.open("./img/1.png")
locations = FindImgInWindow(window, img_gem_map, threshold=0.7)
# screenshot = window.capture_as_image()
# screenshot.show()
# teams = CheckTeams(window)
print(locations)
if locations:
#     print("Yeah thấy mở gem rồi...")
    x, y = locations
    pyautogui.click(x, y)
    
    #     h, w = img_gem_map.size
    #     crop_coordinates = (x + 150, y - h , x + h + 30, y + w - 220)
    #     cropped_image = screenshot.crop(crop_coordinates)
    #     # cropped_image.show()
    #     # cropped_image.show()
    #     text = image_to_text(cropped_image)

    # print(locations)


# left, top = (
#     window.rectangle().left,
#     window.rectangle().top,
# )
# pyautogui.moveTo(left + 800, 450 + top)
# time.sleep(2)


# img_gem = Image.open("./img/gem.png")
# img_gem_2 = Image.open("./img/gem_2.png")
# img_gem_3 = Image.open("./img/gem_3.png")

# gems = [img_gem, img_gem_2, img_gem_3]
# for gem in gems:
#     locations = FindImgInWindow(window, gem, threshold=0.7)
#     if locations:
#         break
# print(locations)

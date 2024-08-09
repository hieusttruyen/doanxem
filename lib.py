from pywinauto import Desktop
import time
import cv2
import numpy as np
import pyautogui


import win32gui
import win32ui
import win32con
import win32api
from PIL import Image
import io


def window_capture():
    # Lấy handle của cửa sổ
    screenshot = pyautogui.screenshot()
    cropped_screenshot = screenshot.crop((0, 0, 1650, 920))
    # cropped_screenshot.show()
    # Trả về đối tượng PIL Image
    return cropped_screenshot


def getWindow(window_title):
    try:
        window = Desktop(backend="win32").window(title=window_title)
        if window.exists():
            return window
        else:
            return None
    except Exception as ex:
        print("ERROR: ", ex)


def find_image_in_image(
    screenshot, find_img, method=cv2.TM_CCOEFF_NORMED, threshold=0.8
):
    try:
        main_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        find_gray = cv2.cvtColor(np.array(find_img), cv2.COLOR_RGB2BGR)

        result = cv2.matchTemplate(main_gray, find_gray, method)
        loc = (
            np.where(result >= threshold)
            if method not in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]
            else np.where(result <= threshold)
        )
        locations = list(zip(*loc[::-1]))
        return filter_close_points(locations, min_distance=50)
    except Exception as ex:
        print("ERROR: ", ex)


# def find_image_in_image(
#     screenshot, find_img, method=cv2.TM_CCOEFF_NORMED, threshold=0.8
# ):
#     try:
#         # Đọc ảnh lớn và ảnh nhỏ
#         # large_image = cv2.imread(large_image_path)
#         main_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
#         find_gray = cv2.cvtColor(np.array(find_img), cv2.COLOR_RGB2BGR)

#         # large_gray_pil.show()
#         # Thực hiện so khớp mẫu
#         result = cv2.matchTemplate(main_gray, find_gray, method, threshold)

#         # Ngưỡng để xác định sự khớp chính xác
#         if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
#             loc = np.where(result <= threshold)
#         else:
#             loc = np.where(result >= threshold)

#         # Danh sách các vị trí khớp
#         locations = list(zip(*loc[::-1]))
#         filtered_locations = filter_close_points(locations, min_distance=50)

#         return filtered_locations
#     except Exception as ex:
#         print("ERROR: ", ex)


def filter_close_points(points, min_distance):
    try:
        filtered_points = []
        for p in points:
            if all(
                np.linalg.norm(np.array(p) - np.array(fp)) >= min_distance
                for fp in filtered_points
            ):
                filtered_points.append(p)
        return filtered_points
    except Exception as ex:
        print("ERROR: ", ex)


def FindImgInWindow(
    window,
    image,
    method=cv2.TM_CCOEFF_NORMED,
    threshold=0.8,
    min_distance=50,
):
    try:
        screenshot = window_capture()

        locations = find_image_in_image(screenshot, image, method, threshold)
        # print(locations)
        # # Lọc các vị trí gần nhau
        filtered_locations = filter_close_points(locations, min_distance)
        # screenshot.show()
        h, w = image.size
        if filtered_locations:
            a, b = filtered_locations[0][0], filtered_locations[0][1]
            print(a, b)
            x = filtered_locations[0][0] + (h / 2)
            y = filtered_locations[0][1] + (w / 2)
            return x, y
        else:
            return None
    except Exception as ex:
        print("ERROR: ", ex)


def FindImg(
    img_base,
    img_find,
    method=cv2.TM_CCOEFF_NORMED,
    threshold=0.8,
    min_distance=50,
):
    try:
        locations = find_image_in_image(img_base, img_find, method, threshold)
        # # Lọc các vị trí gần nhau
        filtered_locations = filter_close_points(locations, min_distance)

        h, w = img_find.size

        if filtered_locations:
            x = filtered_locations[0][0] + h / 2
            y = filtered_locations[0][1] + w / 2
            return x, y
        else:
            return None
    except Exception as ex:
        print("ERROR: ", ex)


def PressKey(key, delay=0):
    try:
        pyautogui.keyDown(key)
        time.sleep(delay)
        pyautogui.keyUp(key)
    except Exception as ex:
        print("ERROR: ", ex)

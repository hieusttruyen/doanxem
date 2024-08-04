import time
import pyautogui
import win32gui
from pywinauto import Application
from PIL import Image
from lib import (
    PressKeyandRelease,
    find_image_in_image,
    filter_close_points,
    capture_window_screenshot,
)


# # Hàm để liệt kê tất cả các cửa sổ và in ra tiêu đề của chúng
# def enum_windows_callback(hwnd, windows):
#     if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
#         windows.append((hwnd, win32gui.GetWindowText(hwnd)))


# windows = []
# win32gui.EnumWindows(enum_windows_callback, windows)

# # In ra tất cả các cửa sổ để kiểm tra tiêu đề chính xác
# for hwnd, title in windows:
#     print(f"Handle: {hwnd}, Title: {title}")

# # Đặt tiêu đề cửa sổ bạn muốn kích hoạt

window_title = "Rise of Kingdoms"

# Khởi tạo ứng dụng pywinauto
app = Application(backend="win32").connect(title=window_title)


# Kết nối với cửa sổ
window = app[window_title]

# Đưa cửa sổ lên phía trước và đợi để chắc chắn nó đã được kích hoạt
window.set_focus()
# time.sleep(2)  # Đợi 2 giây để cửa sổ được kích hoạt hoàn toàn

VK_RETURN = 0x0D
VK_PRIOR = 33
# Nhấn và nhả phím Enter
VK_LEFT = 37
VK_UP = 38
VK_RIGHT = 39
VK_DOWN = 40


# screenshot =  capture_window_screenshot(window_title)


def findGems():

    def findGem():
        screenshot, left, top, right, bottom = capture_window_screenshot(window_title)
        img_gem = Image.open("gem_3.png")
        locations, w, h = find_image_in_image(screenshot, img_gem, threshold=0.8)
        # filtered_locations = filter_close_points(locations, min_distance=50)
        if locations:
            # print(f"Found {len(locations)} match(es):")
            # Cắt khu vực tìm thấy
            screen_x, screen_y = locations[0][0], locations[0][1]

            x = screen_x + left
            y = screen_y + top
            pyautogui.click(x, y)
            time.sleep(1)
            screenshot, left, top, right, bottom = capture_window_screenshot(
                window_title
            )
            img_find = Image.open("gem_map.png")
            locations, w, h = find_image_in_image(screenshot, img_find, threshold=0.7)
            if locations:
                x = locations[0][0] + left + 10
                y = locations[0][1] + top + 10
                pyautogui.click(x, y)
                time.sleep(2)
                img_gather = Image.open("thuthap.png")
                find, left, top, right, bottom = capture_window_screenshot(window_title)
                locations, w, h = find_image_in_image(find, img_gather, threshold=0.9)

                if locations:
                    print("Found a gem mine")
                    return screen_x + left, screen_y + top
                else:
                    print("The gem mine has an owner")
                    PressKeyandRelease(33, 0.2)
                    time.sleep(2)
                    return None, None
            else:
                print("The gem mine has an owner")
                PressKeyandRelease(33, 0.2)
                time.sleep(2)
                return None, None

        else:
            print("No match found")
            return None, None

    dem = 1
    n = 0
    PressKeyandRelease(33, 0.2)
    time.sleep(2)
    while True:
        if dem > 2:
            dem = 1
        left = 2 * dem
        down = 1 * dem
        right = 2 * dem
        up = 2 * dem

        PressKeyandRelease(VK_LEFT, 0.3)
        time.sleep(2)
        x, y = findGem()
        if x and y:
            return x, y
            # break
        n = 0
        while n < down:
            PressKeyandRelease(VK_DOWN, 0.3)
            time.sleep(2)
            x, y = findGem()
            if x and y:
                print(x, y)
                # pyautogui.click([0], pos[1])
                return x, y
                # break
            else:
                n = n + 1

        n = 0
        while n < right:
            # print("right")
            PressKeyandRelease(VK_RIGHT, 0.3)
            time.sleep(2)

            x, y = findGem()
            if x and y:
                print(x, y)
                # pyautogui.click([0], pos[1])
                return x, y
                # break
            else:
                n = n + 1
            #   print ('Số thứ', n)
            #   n = n + 1
        n = 0
        while n < up:
            # print("up")
            PressKeyandRelease(VK_UP, 0.3)
            time.sleep(2)

            x, y = findGem()
            if x and y:
                print(x, y)
                # pyautogui.click([0], pos[1])
                return x, y
                # break
            else:
                n = n + 1
        n = 0
        while n < left:

            # print("left")
            PressKeyandRelease(VK_LEFT, 0.3)
            time.sleep(2)

            x, y = findGem()
            if x and y:
                print(x, y)
                # pyautogui.click([0], pos[1])
                return x, y
                # break
            else:
                n = n + 1

        PressKeyandRelease(VK_DOWN, 0.3)
        time.sleep(2)
        dem = dem + 1
        # return None, None


def farm(i):

    new = True
    img_gather = Image.open("thuthap.png")
    find, left, top, right, bottom = capture_window_screenshot(window_title)
    locations, w, h = find_image_in_image(find, img_gather, threshold=0.5)
    if locations:
        screen_x, screen_y = locations[0][0], locations[0][1]
        pyautogui.click(screen_x + left, screen_y + top)
    time.sleep(1)
    img_new = Image.open("new.png")
    find, left, top, right, bottom = capture_window_screenshot(window_title)
    locations, w, h = find_image_in_image(find, img_new, threshold=0.5)

    # new
    if locations:
        screen_x, screen_y = locations[0][0], locations[0][1]
        x = locations[0][0] + left
        y = locations[0][1] + top
        pyautogui.click(x, y)
        time.sleep(1)
        screenshot, left, top, right, bottom = capture_window_screenshot(window_title)
        img_find = Image.open("1.png")
        locations, w, h = find_image_in_image(screenshot, img_find, threshold=0.9)
        if locations:
            x = locations[0][0] + left
            y = locations[0][1] + top
            pyautogui.click(x, y)
            yy = 0
            for i in range(5):
                pyautogui.click(x, y + yy)
                yy = yy + 50

    else:
        new = False
        find, left, top, right, bottom = capture_window_screenshot(window_title)

        # w, h = cropped_part.size
        # new_find = cropped_part.crop((w // 2, 0, w, h // 2))
        # new_find.show()
        yy = 100 * i
        w, h = find.size
        x = 1540 + left
        y = 260 + top + yy

        # click mo gem
        pyautogui.click(x, y)
        print(x, y)
        time.sleep(1)

    if new:
        img_running = Image.open("running_new.png")
    else:
        img_running = Image.open("running.png")

    find, left, top, right, bottom = capture_window_screenshot(window_title)
    locations, w, h = find_image_in_image(find, img_running, threshold=0.8)
    if locations:
        # print(locations)
        screen_x, screen_y = locations[0][0], locations[0][1]
        x = locations[0][0] + left
        y = locations[0][1] + top
        pyautogui.click(x, y)
        return True
        # cropped_image.show()

    else:
        return False

        print(x, y)


def runfarming(i):
    x, y = findGems()
    if x and y:
        time.sleep(1)
        screenshot, left, top, right, bottom = capture_window_screenshot(window_title)
        img_find = Image.open("gem_map.png")
        locations, w, h = find_image_in_image(screenshot, img_find, threshold=0.7)
        if locations:
            x = locations[0][0] + left + 10
            y = locations[0][1] + top + 10
            # pyautogui.click(x, y)
            print("farm gem")
            time.sleep(2)
            check = farm(i)
            time.sleep(2)
            if check:
                pyautogui.click(x, y)
                while True:
                    screenshot, left, top, right, bottom = capture_window_screenshot(
                        window_title
                    )
                    img_find = Image.open("refurn_gather.png")
                    locations, w, h = find_image_in_image(
                        screenshot, img_find, threshold=0.9
                    )
                    if locations:
                        x = locations[0][0] + left
                        y = locations[0][1] + top
                        print("farming gem")
                        break
                    time.sleep(60)


farming = Image.open("./img/farm.png")
run = Image.open("./img/run.png")
stop = Image.open("dungchan.png")
re = Image.open("./img/return.png")


status = [
    {"name": "farming", "pil": farming},
    {"name": "run", "pil": run},
    {"name": "return", "pil": re},
    {"name": "stop", "pil": stop},
]


while True:
    screenshot, left, top, right, bottom = capture_window_screenshot(window_title)
    screen_width, screen_height = pyautogui.size()
    x = 1500
    y = 170
    width, height = screenshot.size
    crop_coordinates = (1530, 200, 1600, 530)
    cropped_image = screenshot.crop(crop_coordinates)
    image_width, image_height = cropped_image.size
    part_height = image_height // 5
    teams = []

    # check status team
    for i in range(5):
        bottom = (i + 1) * part_height
        cropped_part = cropped_image.crop((0, i * part_height, image_width, bottom))
        # cropped_part.show()
        for item in status:
            # print(f"name: {item['name']}, pil: {item['pil']}")
            locations, w, h = find_image_in_image(
                cropped_part, item["pil"], threshold=0.7
            )
            # print(locations)
            if locations:
                x = locations[0][0] + left
                y = locations[0][1] + top
                # print("farming gem")
                teams.append({"number": i, "status": item["name"]})

    # stop
    for team in teams:
        # print(team["status"])
        match team["status"]:
            case "return":
                print("return")
                yy = 65 * team["number"]
                x = 1550 + left
                y = 230 + top + yy
                # click mo gem
                print(i + 1)
                pyautogui.click(x, y)
                time.sleep(4)
                pyautogui.press("S")
                continue
    # new team
    if len(teams) < 5:
        print("new team")
        pil_home = Image.open("./img/home.png")
        locations, w, h = find_image_in_image(screenshot, pil_home, threshold=0.7)
        if locations:
            x = locations[0][0] + left
            y = locations[0][1] + top
            pyautogui.click(x, y)
            time.sleep(2)
            pyautogui.click(x, y)
            time.sleep(4)
            runfarming(0)
            print("map")
        else:
            x = locations[0][0] + left
            y = locations[0][1] + top
            print("home")
            pyautogui.click(x, y)

    else:
        for team in teams:
            match team["status"]:
                case "run":
                    continue
                case "stop":
                    yy = 65 * team["number"]
                    x = 1550 + left
                    y = 230 + top + yy
                    # click mo gem
                    # print(i + 1)
                    pyautogui.click(x, y)
                    time.sleep(4)
                    runfarming(team["number"])
                case "farm":
                    continue
    
    
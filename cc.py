import time
import pyautogui
import pygetwindow as gw
from PIL import Image
from lib import (
    PressKeyandRelease,
    find_image_in_image,
    filter_close_points,
    capture_window_screenshot,
)


VK_RETURN = 0x0D
VK_PRIOR = 33
# Nhấn và nhả phím Enter
VK_LEFT = 37
VK_UP = 38
VK_RIGHT = 39
VK_DOWN = 40


# screenshot =  capture_window_screenshot(window_title)

img_gem = Image.open("./img/gem.png")
img_gem_2 = Image.open("./img/gem_2.png")
img_gem_3 = Image.open("./img/gem_3.png")
farming = Image.open("./img/farm.png")
run = Image.open("./img/run.png")
stop = Image.open("dungchan.png")
re = Image.open("./img/return.png")


def press(key, delay=0):
    pyautogui.keyDown(key)
    time.sleep(delay)
    pyautogui.keyUp(key)


def checkPass():
    passs = Image.open("./img/pass_1.png")
    locations, w, h = find_image_in_image(screenshot, passs, threshold=0.7)
    print(locations)
    if locations:
        return True
    else:
        return False


def findGems(directions, new):
    global huong

    def findGem():
        screenshot, left, top, right, bottom = capture_window_screenshot(window_title)
        gems = [img_gem, img_gem_2, img_gem_3]

        for gem in gems:
            locations, x, y = find_image_in_image(screenshot, gem, threshold=0.7)
            if locations:
                break
        else:
            return None, None

        screen_x, screen_y = locations[0]
        if 0 < screen_x <= 600 and 800 < screen_y < 900:
            return None, None

        pyautogui.click(screen_x + left, screen_y + top)
        time.sleep(1)

        screenshot, left, top, right, bottom = capture_window_screenshot(window_title)
        img_find = Image.open("gem_map.png")
        locations, _, _ = find_image_in_image(screenshot, img_find, threshold=0.7)

        if locations:
            x, y = locations[0][0] + left + 10, locations[0][1] + top + 10
            pyautogui.click(x, y)
            time.sleep(2)

            find, left, top, right, bottom = capture_window_screenshot(window_title)
            img_gather = Image.open("thuthap.png")
            locations, _, _ = find_image_in_image(find, img_gather, threshold=0.9)

            if locations:
                print("Found a gem mine")
                return screen_x + left, screen_y + top
            else:
                print("The gem mine has an owner")
        else:
            print("The gem mine has an owner")

        press("pgup")
        time.sleep(2)
        return None, None

    def findMap(count, direction):
        for _ in range(count):
            press(direction, 0.25)
            time.sleep(2)
            x, y = findGem()
            if x and y:
                return x, y, direction, dem
        return None

    dem = 0
    n = 0
    press("pgup")
    time.sleep(2)
    while True:
        if dem > 5:
            dem = 0
        left, down, right, up = 2 + dem * 2, 1 + dem * 2, 1 + dem * 2, 2 + dem * 2

        for d in directions:
            if dem >= d["dem"]:
                if d["direction"] == "left":
                    left -= 2
                elif d["direction"] == "down":
                    down -= 2
                elif d["direction"] == "right":
                    right -= 2
                elif d["direction"] == "up":
                    up -= 2

        if new:
            direction_map = {
                "BOT": ("down", "RIGHT"),
                "RIGHT": ("right", "TOP"),
                "TOP": ("up", "LEFT"),
                "LEFT": ("left", "BOT"),
            }
            direction, next_direction = direction_map[huong]
            result = findMap(3, direction)
            huong = next_direction
            if result:
                return result

        for direction, count in [
            ("down", down),
            ("right", right),
            ("up", up),
            ("left", left),
        ]:
            result = findMap(count, direction)
            if result:
                return result
        dem += 1


def resetHome():

    pil_home = Image.open("./img/home.png")
    locations, w, h = find_image_in_image(screenshot, pil_home, threshold=0.7)
    if locations:
        x = locations[0][0] + left
        y = locations[0][1] + top
        press("space")
        time.sleep(1)
        press("space")
        time.sleep(4)
    else:
        press("space")
        time.sleep(4)


def farm(i):

    def newTeam():
        img_new = Image.open("new.png")
        find, left, top, right, bottom = capture_window_screenshot(window_title)
        locations, w, h = find_image_in_image(find, img_new, threshold=0.5)
        if locations:
            screen_x, screen_y = locations[0][0], locations[0][1]
            x = locations[0][0] + left
            y = locations[0][1] + top
            pyautogui.click(x, y)
            time.sleep(1)
            screenshot, left, top, right, bottom = capture_window_screenshot(
                window_title
            )
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
                return True
        else:
            return False

    new = True
    img_gather = Image.open("thuthap.png")
    find, left, top, right, bottom = capture_window_screenshot(window_title)
    locations, w, h = find_image_in_image(find, img_gather, threshold=0.5)
    # print("thuthap")
    if locations:
        # print("tim thay")
        screen_x, screen_y = locations[0][0], locations[0][1]
        # print("checkTeams")
        teams = checkTeams()
        pyautogui.click(screen_x + left, screen_y + top)
        time.sleep(2)
        if len(teams) < team_number:
            new = newTeam()
        else:
            new = False
            print("full")
            yy = 100 * i
            # w, h = find.size
            x = 1540 + left
            y = 260 + top + yy
            # click mo gem
            pyautogui.click(x, y)
            # print(x, y)
            time.sleep(1)

        if new:
            img_running = Image.open("running_new.png")
        else:
            img_running = Image.open("running.png")

        find, left, top, right, bottom = capture_window_screenshot(window_title)
        locations, w, h = find_image_in_image(find, img_running, threshold=0.8)
        print("img_running", locations)

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
    else:
        return False


def runfarming(base_x, base_y, number_team):

    d_left = 0
    d_down = 0
    d_right = 0
    d_up = 0
    directions = []
    while True:
        resetHome()
        new = False
        if base_x and base_y:
            pyautogui.click(base_x, base_y)
            time.sleep(2)
        else:
            new = True

        x, y, direction, dem = findGems(directions, new)
        if x and y:
            time.sleep(1)
            screenshot, left, top, right, bottom = capture_window_screenshot(
                window_title
            )
            # img_find = Image.open("gem_map.png")
            # locations, w, h = find_image_in_image(screenshot, img_find, threshold=0.7)
            # if locations:
            # x = locations[0][0] + left + 10
            # y = locations[0][1] + top + 10
            # pyautogui.click(x, y)
            print("farm gem")
            time.sleep(2)
            done = farm(number_team)

            if done:
                time.sleep(5)
                check = checkPass()
                time.sleep(2)
                if check:
                    match direction:
                        case "left":
                            if d_up == 2 and d_down == 2:
                                d_left = 2
                                directions.append({"direction": "left", "dem": dem})
                            directions.append({"direction": "up", "dem": dem})
                            d_up = 2
                        case "down":
                            d_down = 2
                            directions.append({"direction": "down", "dem": dem})
                        case "right":
                            if d_up == 2 and d_down == 2:
                                d_right = 2
                                directions.append({"direction": "right", "dem": dem})
                            d_down = 2
                            directions.append({"direction": "down", "dem": dem})

                        case "up":
                            d_up = 2
                            directions.append({"direction": "up", "dem": dem})

                else:
                    break
            else:
                print("bi ks rồi")


status = [
    {"name": "farming", "pil": farming},
    {"name": "run", "pil": run},
    {"name": "return", "pil": re},
    {"name": "stop", "pil": stop},
]


team_number = 4


def checkTeams():
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
    for i in range(team_number):

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
    return teams


huong = "TOP"


try:
    window_title = "Rise of Kingdoms"
    target_window = gw.getWindowsWithTitle(window_title)
    window = target_window[0]
    if target_window:
        window.activate()
        time.sleep(2)
        while True:
            # check status team
            teams = checkTeams()
            screenshot, left, top, right, bottom = capture_window_screenshot(
                window_title
            )
            # print(teams)
            # stop
            for team in teams:
                # print(team["status"])
                match team["status"]:
                    case "return":
                        # continue
                        print("return")
                        yy = 65 * team["number"]
                        x = 1550 + left
                        y = 230 + top + yy
                        # click mo gem
                        # print(i + 1)
                        pyautogui.click(x, y)
                        time.sleep(4)
                        pyautogui.press("S")
                        continue
            # new team

            if len(teams) < team_number:
                print("new team")
                x = 0
                y = 0
                runfarming(x, y, 0)

            else:
                for team in teams:
                    match team["status"]:
                        case "run":
                            continue
                        case "stop":
                            yy = 65 * team["number"]
                            x = 1550 + left
                            y = 230 + top + yy
                            runfarming(x, y, team["number"])
                        case "farm":
                            continue

    else:
        pyautogui.alert(
            text='Window titled "Rise of Kingdoms" not found.',
            title="Alert",
            button="OK",
        )
except:
    pyautogui.alert(
        text='Window titled "Rise of Kingdoms" not found.',
        title="Alert",
        button="OK",
    )

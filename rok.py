import time
import pyautogui
from PIL import Image
from lib import FindImgInWindow, FindImg, getWindow, PressKey, window_capture
from pywinauto.application import Application

pyautogui.FAILSAFE = False


def Reconnect(window):

    print("Kiểm tra kết nối...")
    try:
        point = FindImgInWindow(window, img_reconnect)
        if point:
            print("Đang kết nối lại...")
            x, y = point
            pyautogui.click(x, y)
            time.sleep(60)
            window_title = "Rise of Kingdoms"
            window = getWindow(window_title)
            if window:
                time.sleep(60)
                print("Kết nối thành công")
            else:
                StartRok(window_title)
    except Exception as ex:
        print("ERROR: ", ex)


def ScrollMap():
    delay = int(sys.argv[3])
    pyautogui.moveTo(800, 450)
    time.sleep(delay)
    pyautogui.scroll(-10)
    pyautogui.scroll(-10)
    # pyautogui.scroll(-10)


def StartRok(window_title):
    try:
        path = sys.argv[1] + "/launcher.exe"
        app = Application()
        print("Khởi động launcher")
        app.start(path)
        time.sleep(60)
        sc = pyautogui.screenshot()
        point = FindImg(sc, img_start)
        if point:
            print("Khởi động rok")
            x, y = point
            pyautogui.click(x, y)
            time.sleep(60)
            window = getWindow(window_title)
            while not window.exists():
                time.sleep(20)
                window = getWindow(window_title)
            window.set_focus()
            while not FindImgInWindow(window, img_map):
                time.sleep(20)
            print("Khởi động rok thành công")
    except Exception as ex:
        print("ERROR: ", ex)


def ResetHome(window):
    print("Reset zoom...")
    try:
        delay = int(sys.argv[3])
        locations = FindImgInWindow(window, pil_home, threshold=0.7)
        if locations:
            # PressKey("space",2)
            pyautogui.press("space")
            time.sleep(delay)
            pyautogui.press("space")
            # PressKey("space",2)
            time.sleep(delay)
        else:
            # PressKey("space",2)
            pyautogui.press("space")

            time.sleep(delay)
    except Exception as ex:
        print("ERROR: ", ex)


def CheckTeams(window):
    print("Kiểm tra quân dội...")
    try:
        screenshot = window_capture()
        # x, y = screenshot.size
        crop_coordinates = (1600 - 80, 180, 1600, 550)
        cropped_image = screenshot.crop(crop_coordinates)
        # cropped_image.show()
        image_width, image_height = cropped_image.size
        part_height = image_height // 5
        teams = []
        team_number = int(sys.argv[2])
        # print(team_number)
        for i in range(team_number + 1):
            bottom = (i + 1) * part_height
            cropped_part = cropped_image.crop((0, i * part_height, image_width, bottom))
            for item in status:
                locations = FindImg(cropped_part, item["pil"], threshold=0.7)
                if locations:
                    teams.append({"number": i, "status": item["name"]})
        return teams
    except Exception as ex:
        print("ERROR: ", ex)


def StartFarm(window):
    print("Bắt đầu farm...")

    try:
        # ResetHome(window)
        teams = CheckTeams(window)
        team_number = int(sys.argv[2])
        delay = int(sys.argv[3])
        # print(teams)
        for team in teams:
            match team["status"]:
                case "return":
                    print("Dừng quân đội...")
                    yy = 65 * team["number"]
                    y = 230 + yy
                    pyautogui.click(1600 - 50, y)
                    time.sleep(delay)
                    PressKey("S")
                    continue
        if len(teams) < team_number:
            RunFarm(window, 0, 0, 0)
        else:
            for team in teams:
                match team["status"]:
                    case "run", "farm":
                        continue
                    case "stop":
                        yy = 65 * team["number"]
                        y = 230 + yy
                        RunFarm(window, 1600 - 50, y, team["number"])
                        break
    except Exception as ex:
        print("ERROR: ", ex)


def CheckPass(window):
    try:
        locations = FindImgInWindow(window, img_passs, threshold=0.7)
        return bool(locations)
    except Exception as ex:
        print("ERROR: ", ex)


def FindGems(window, directions, new):
    try:

        delay = int(sys.argv[3])
        global huong
        d = 0.25
        def FindGem(window):
            try:
                gems = [img_gem, img_gem_2, img_gem_3]
                for gem in gems:
                    locations = FindImgInWindow(window, gem, threshold=0.7)
                    if locations:
                        break
                if not locations:
                    return None
                screen_x, screen_y = locations
                if 0 < screen_x <= 620 and 770 < screen_y < 900:
                    return locations
                pyautogui.click(screen_x, screen_y)
                time.sleep(delay)

                locations = FindImgInWindow(window, img_gem_map, threshold=0.7)
                if locations:
                    print("Yeah thấy mở gem rồi...")
                    x, y = locations
                    pyautogui.click(x, y)
                    time.sleep(delay)
                    locations = FindImgInWindow(window, img_gather, threshold=0.7)
                    if locations:
                        return locations
                    else:
                        print("T_T Mỏ gem này đã có chủ")
                        ScrollMap()
                        time.sleep(delay)
                        return None
                else:
                    print("T_T Mỏ gem này đã có chủ")
                    ScrollMap()
                    time.sleep(delay)
                    return None
            except Exception as ex:
                print("ERROR: ", ex)

        def FindMap(window, count, direction):

            try:
                for _ in range(count):
                    PressKey(direction, d)
                    time.sleep(delay)
                    point = FindGem(window)
                    if point:
                        return point, direction, dem
                return None
            except Exception as ex:
                print("ERROR: ", ex)

        print("Tìm mỏ gem...")
        dem = 0
        ScrollMap()
        time.sleep(delay)

        while True:
            Reconnect(window)
            if FindImgInWindow(window, img_earth):
                print("Lỗi zoom...")
                return None, None, None
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
                result = FindMap(window, 3, direction)
                huong = next_direction
                if result:
                    return result
            for direction, count in [
                ("down", down),
                ("right", right),
                ("up", up),
                ("left", left),
            ]:
                result = FindMap(window, count, direction)
                if result:
                    return result
            dem += 1
    except Exception as ex:
        print("ERROR: ", ex)


def Farming(window, i):
    team_number = int(sys.argv[2])
    delay = int(sys.argv[3])

    def NewTeam(window):

        locations = FindImgInWindow(window, img_new, threshold=0.5)
        if locations:
            x, y = locations
            time.sleep(delay)
            pyautogui.click(x, y)
            time.sleep(delay)
            locations = FindImgInWindow(window, img_1, threshold=0.7)
            if locations:
                x, y = locations
                pyautogui.click(x, y)
                time.sleep(delay)
                yy = 0
                for i in range(5):
                    pyautogui.click(x, y + yy)
                    time.sleep(delay)
                    # print(x, y + yy)
                    yy = yy + 49
                return True
        return False

    new = True

    locations = FindImgInWindow(window, img_gather, threshold=0.5)
    if locations:
        x, y = locations
        teams = CheckTeams(window)
        pyautogui.click(x, y)
        time.sleep(delay)
        if len(teams) < team_number:
            new = NewTeam(window)
        else:
            new = False
            # print("full")
            yy = 100 * i
            x = 1540
            y = 260 + yy
            pyautogui.click(x, y)
            time.sleep(delay)
        if new:
            img_f = img_running_new
        else:
            img_f = img_running
        locations = FindImgInWindow(window, img_f, threshold=0.6)
        if locations:
            x, y = locations
            pyautogui.click(x, y)
            return True
    return False


def RunFarm(window, base_x, base_y, number_team):
    delay = int(sys.argv[3])
    d_down = 0
    d_up = 0
    directions = []
    while True:
        Reconnect(window)
        ResetHome(window)
        new = base_x == 0 and base_y == 0
        if not new:
            pyautogui.click(base_x, base_y)
            time.sleep(delay)
        point, direction, dem = FindGems(window, directions, new)
        if point:
            time.sleep(delay)
            # print("farm gem")
            time.sleep(delay)
            if Farming(window, number_team):
                time.sleep(delay)
                if CheckPass(window):
                    print("Pass")
                    match direction:
                        case "left":
                            if d_up == 2 and d_down == 2:
                                directions.append({"direction": "left", "dem": dem})
                            directions.append({"direction": "up", "dem": dem})
                            d_up = 2
                        case "down":
                            d_down = 2
                            directions.append({"direction": "down", "dem": dem})
                        case "right":
                            if d_up == 2 and d_down == 2:
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


# image
img_gem = Image.open("./img/gem.png")
img_gem_2 = Image.open("./img/gem_2.png")
img_gem_3 = Image.open("./img/gem_3.png")
farming = Image.open("./img/farm.png")
run = Image.open("./img/run.png")
stop = Image.open("./img/dungchan.png")
re = Image.open("./img/return.png")
img_earth = Image.open("./img/earth.png")
img_gem_map = Image.open("./img/gem_map.png")
img_gather = Image.open("./img/thuthap.png")
img_start = Image.open("./img/start.png")
img_map = Image.open("./img/map.png")
pil_home = Image.open("./img/home.png")
img_reconnect = Image.open("./img/reconnect.png")
img_passs = Image.open("./img/pass_1.png")
img_new = Image.open("./img/new.png")
img_1 = Image.open("./img/1.png")
img_running_new = Image.open("./img/running_new.png")
img_running = Image.open("./img/running.png")

huong = "TOP"
status = [
    {"name": "farming", "pil": farming},
    {"name": "run", "pil": run},
    {"name": "return", "pil": re},
    {"name": "stop", "pil": stop},
]
# team_number = 4


def RunApp():

    try:
        while True:
            window_title = "Rise of Kingdoms"
            window = getWindow(window_title)

            window_title_cmd = "Administrator:  cmd_rokauto"
            window_cmd = getWindow(window_title_cmd)
            if window_cmd:
                x, y = pyautogui.size()
                new_x = x - 315
                new_y = 200
                window_cmd.move_window(x=new_x, y=new_y, width=315, height=300)
                # window_cmd.set_focus()
            if window:

                window.move_window(0, 0)
                # window.move_window(0, 0)
                window.set_focus()

                Reconnect(window)
                StartFarm(window)
                time.sleep(10)
            else:
                StartRok(window_title)
    except Exception as ex:
        print("ERROR: ", ex)


import sys

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: main.py <path> <team_number>")
        sys.exit(1)
    path = sys.argv[1]
    team_number = int(sys.argv[2])
    RunApp()

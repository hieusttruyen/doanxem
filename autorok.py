import time
import pyautogui
from PIL import Image
from lib import FindImgInWindow, FindImg, getWindow, PressKey, window_capture
from pywinauto.application import Application
import logging

pyautogui.FAILSAFE = False

# Thiết lập logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Handler để ghi log ra console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# Handler để ghi tất cả log ra file
file_handler = logging.FileHandler("rok_auto.log")
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


class RokAuto:
    image_cache = {}

    def __init__(self, app_path, total_teams, delay_time):
        self.app_path = app_path
        self.total_teams = total_teams
        self.delay_time = delay_time
        self.current_direction = "TOP"
        self.window = None
        self.zoom_error = False
        self.img_gem_1 = self.load_image("./img/gem.png")
        self.img_gem_2 = self.load_image("./img/gem_2.png")
        self.img_gem_3 = self.load_image("./img/gem_3.png")
        self.img_farming = self.load_image("./img/farm.png")
        self.img_running = self.load_image("./img/run.png")
        self.img_stopped = self.load_image("./img/dungchan.png")
        self.img_return = self.load_image("./img/return.png")
        self.img_earth = self.load_image("./img/earth.png")
        self.img_gem_map = self.load_image("./img/gem_map.png")
        self.img_gather = self.load_image("./img/thuthap.png")
        self.img_start_game = self.load_image("./img/start.png")
        self.img_map = self.load_image("./img/map.png")
        self.img_home = self.load_image("./img/home.png")
        self.img_reconnect = self.load_image("./img/reconnect.png")
        self.img_pass = self.load_image("./img/pass_1.png")
        self.img_new_team = self.load_image("./img/new.png")
        self.img_team_1 = self.load_image("./img/1.png")
        self.img_team_running_new = self.load_image("./img/running_new.png")
        self.img_team_running = self.load_image("./img/running.png")

        self.team_status = [
            {"name": "farming", "image": self.img_farming},
            {"name": "running", "image": self.img_running},
            {"name": "returning", "image": self.img_return},
            {"name": "stopped", "image": self.img_stopped},
        ]

    @classmethod
    def load_image(cls, image_path):
        if image_path not in cls.image_cache:
            cls.image_cache[image_path] = Image.open(image_path)
            logger.info(f"IMAGE LOADED: {image_path}")
        return cls.image_cache[image_path]

    def reconnect(self):
        logger.info("CHECK: Connection status...")
        try:
            point = FindImgInWindow(self.window, self.img_reconnect)
            if point:
                logger.info("ACTION: Reconnecting...")
                pyautogui.click(*point)
                time.sleep(60)
                self.window = getWindow("Rise of Kingdoms")
                if self.window:
                    time.sleep(60)
                    logger.info("STATUS: Reconnected successfully.")
                else:
                    self.start_game()
        except Exception as ex:
            logger.error("ERROR: Reconnect failed. %s", ex)

    def scroll_map(self):
        logger.info("ACTION: Scrolling the map...")
        pyautogui.moveTo(800, 450)
        time.sleep(self.delay_time)
        pyautogui.scroll(-10)  # Increase scroll amount to reduce calls
        pyautogui.scroll(-10)  # Increase scroll amount to reduce calls
        pyautogui.scroll(-10)  # Increase scroll amount to reduce calls

    def start_game(self):
        logger.info(f"ACTION: Starting launcher at path: {self.app_path}")
        try:
            app = Application().start(f"{self.app_path}/launcher.exe")
            time.sleep(30)
            screenshot = pyautogui.screenshot()
            point = FindImg(screenshot, self.img_start_game)
            if point:
                logger.info("ACTION: Starting Rise of Kingdoms...")
                pyautogui.click(*point)
                time.sleep(30*self.delay_time)
                self.window = getWindow("Rise of Kingdoms")
                while not self.window.exists():
                    time.sleep(20)
                    self.window = getWindow("Rise of Kingdoms")
                self.window.set_focus()
                while not FindImgInWindow(self.window, self.img_map):
                    time.sleep(20)
                logger.info("STATUS: Rise of Kingdoms started successfully.")
        except Exception as ex:
            logger.error("ERROR: Failed to start Rise of Kingdoms. %s", ex)

    def reset_zoom(self):
        logger.info("ACTION: Resetting zoom...")
        try:
            locations = FindImgInWindow(self.window, self.img_home, threshold=0.7)
            self.zoom_error = False
            if locations:
                PressKey("space", 2)
                time.sleep(self.delay_time)
                PressKey("space", 2)
                time.sleep(self.delay_time)
        except Exception as ex:
            logger.error("ERROR: Failed to reset zoom. %s", ex)

    def check_teams(self):
        logger.info("ACTION: Checking teams...")
        try:
            screenshot = window_capture()
            crop_coordinates = (1600 - 80, 180, 1600, 550)
            cropped_image = screenshot.crop(crop_coordinates)
            image_width, image_height = cropped_image.size
            part_height = image_height // 5
            teams = []
            for i in range(self.total_teams + 1):
                bottom = (i + 1) * part_height
                cropped_part = cropped_image.crop(
                    (0, i * part_height, image_width, bottom)
                )
                for status in self.team_status:
                    locations = FindImg(cropped_part, status["image"], threshold=0.7)
                    if locations:
                        teams.append({"number": i, "status": status["name"]})
                        break  # Break early if found
            logger.info(f"STATUS: {len(teams)} teams found.")
            return teams
        except Exception as ex:
            logger.error("ERROR: Failed to check teams. %s", ex)

    def start_farming(self):
        logger.info("PROCESS: Starting farming process...")
        try:
            teams = self.check_teams()
            for team in teams:
                if team["status"] == "returning":
                    logger.info(f"ACTION: Stopping team {team['number']}...")
                    y_position = 230 + 65 * team["number"]
                    pyautogui.click(1600 - 50, y_position)
                    time.sleep(self.delay_time)
                    PressKey("S")
            if len(teams) < self.total_teams:
                self.run_farming(0, 0, 0)
            else:
                for team in teams:
                    if team["status"] == "stopped":
                        y_position = 230 + 65 * team["number"]
                        self.run_farming(1600 - 50, y_position, team["number"])
                        break
        except Exception as ex:
            logger.error("ERROR: Failed to start farming. %s", ex)

    def check_pass(self):
        logger.info("ACTION: Checking for pass...")
        try:
            locations = FindImgInWindow(self.window, self.img_pass, threshold=0.7)
            pass_found = bool(locations)
            if pass_found:
                logger.info("STATUS: Pass found.")
            return pass_found
        except Exception as ex:
            logger.error("ERROR: Failed to check pass. %s", ex)

    def find_gems(self, directions, is_new):
        logger.info("PROCESS: Searching for gem mines...")
        try:
            move_duration = 0.25

            def find_gem_mine():
                try:
                    for gem in [self.img_gem_1, self.img_gem_2, self.img_gem_3]:
                        locations = FindImgInWindow(self.window, gem, threshold=0.7)
                        if locations:
                            break
                    if not locations:
                        return None
                    screen_x, screen_y = locations
                    if 0 < screen_x <= 620 and 770 < screen_y < 900:
                        return locations
                    pyautogui.click(screen_x, screen_y)
                    time.sleep(self.delay_time)
                    locations = FindImgInWindow(
                        self.window, self.img_gem_map, threshold=0.7
                    )
                    if locations:
                        logger.info("STATUS: Gem mine found.")
                        pyautogui.click(*locations)
                        time.sleep(self.delay_time)
                        locations = FindImgInWindow(
                            self.window, self.img_gather, threshold=0.9
                        )
                        if locations:
                            return locations
                        else:
                            logger.warning("WARNING: Gem mine is occupied.")
                            self.scroll_map()
                            time.sleep(self.delay_time)
                            return None
                    else:
                        logger.warning("WARNING: Gem mine is occupied.")
                        self.scroll_map()
                        time.sleep(self.delay_time)
                        return None
                except Exception as ex:
                    logger.error("ERROR: Failed to find gem mine. %s", ex)

            def search_map_area(count, direction):
                try:
                    for _ in range(count):
                        PressKey(direction, move_duration)
                        time.sleep(self.delay_time)
                        logger.info(f"ACTION: Searching direction {direction}...")
                        if FindImgInWindow(self.window, self.img_earth):
                            logger.error("ERROR: Zoom error detected.")
                            self.zoom_error = True
                            return None
                        point = find_gem_mine()
                        if point:
                            return point, direction
                    return None
                except Exception as ex:
                    logger.error("ERROR: Failed to search map. %s", ex)

            search_attempt = 0
            self.scroll_map()
            time.sleep(self.delay_time)

            while True:
                self.reconnect()
                self.window.set_focus()

                if FindImgInWindow(self.window, self.img_earth):
                    logger.error("ERROR: Zoom error detected.")
                    self.zoom_error = True
                if self.zoom_error:
                    return None, None, None
                if search_attempt > 5:
                    search_attempt = 0
                left, down, right, up = (
                    2 + search_attempt * 2,
                    1 + search_attempt * 2,
                    1 + search_attempt * 2,
                    2 + search_attempt * 2,
                )
                for direction in directions:
                    if search_attempt >= direction["attempt"]:
                        if direction["direction"] == "left":
                            left -= 2
                        elif direction["direction"] == "down":
                            down -= 2
                        elif direction["direction"] == "right":
                            right -= 2
                        elif direction["direction"] == "up":
                            up -= 2
                if is_new:
                    direction_map = {
                        "BOT": ("down", "RIGHT"),
                        "RIGHT": ("right", "TOP"),
                        "TOP": ("up", "LEFT"),
                        "LEFT": ("left", "BOT"),
                    }
                    direction, next_direction = direction_map[self.current_direction]
                    result = search_map_area(3, direction)
                    self.current_direction = next_direction
                    if result:
                        return *result, search_attempt
                else:
                    for direction, count in [
                        ("down", down),
                        ("right", right),
                        ("up", up),
                        ("left", left),
                    ]:
                        result = search_map_area(count, direction)
                        if result:
                            return *result, search_attempt
                search_attempt += 1
        except Exception as ex:
            logger.error("ERROR: Failed to find gems. %s", ex)

    def farming(self, team_index):
        logger.info(f"ACTION: Farming for team {team_index}...")

        def create_new_team():
            try:
                locations = FindImgInWindow(
                    self.window, self.img_new_team, threshold=0.9
                )
                if locations:
                    pyautogui.click(*locations)
                    time.sleep(self.delay_time)
                    locations = FindImgInWindow(
                        self.window, self.img_team_1, threshold=0.9
                    )
                    if locations:
                        pyautogui.click(*locations)
                        time.sleep(self.delay_time)
                        for offset in range(0, 245, 49):
                            pyautogui.click(locations[0], locations[1] + offset)
                            time.sleep(self.delay_time)
                        logger.info("STATUS: New team created.")
                        return True
                return False
            except Exception as ex:
                logger.error("ERROR: Failed to create new team. %s", ex)

        is_new_team = True
        try:
            locations = FindImgInWindow(self.window, self.img_gather, threshold=0.9)
            if locations:
                teams = self.check_teams()
                pyautogui.click(*locations)
                time.sleep(self.delay_time)
                if len(teams) < self.total_teams:
                    is_new_team = create_new_team()
                else:
                    is_new_team = False
                    offset_y = 100 * team_index
                    pyautogui.click(1540, 260 + offset_y)
                    time.sleep(self.delay_time)
                img_f = (
                    self.img_team_running_new if is_new_team else self.img_team_running
                )
                locations = FindImgInWindow(self.window, img_f, threshold=0.9)
                if locations:
                    pyautogui.click(*locations)
                    logger.info("STATUS: Farming initiated successfully.")
                    return True
            return False
        except Exception as ex:
            logger.error("ERROR: Farming fai    led. %s", ex)

    def run_farming(self, base_x, base_y, team_number):
        logger.info("PROCESS: Running farming routine...")
        down_attempts = 0
        up_attempts = 0
        search_directions = []
        while True:
            try:
                self.reconnect()
                self.reset_zoom()
                is_new_position = base_x == 0 and base_y == 0
                if not is_new_position:
                    pyautogui.click(base_x, base_y)
                    time.sleep(self.delay_time)
                point, direction, attempt = self.find_gems(
                    search_directions, is_new_position
                )
                if point:
                    time.sleep(self.delay_time)
                    if self.farming(team_number):
                        time.sleep(self.delay_time)
                        if self.check_pass():
                            logger.info("STATUS: Pass completed successfully.")
                            if direction == "left":
                                if up_attempts == 2 and down_attempts == 2:
                                    search_directions.append(
                                        {"direction": "left", "attempt": attempt}
                                    )
                                search_directions.append(
                                    {"direction": "up", "attempt": attempt}
                                )
                                up_attempts = 2
                            elif direction == "down":
                                down_attempts = 2
                                search_directions.append(
                                    {"direction": "down", "attempt": attempt}
                                )
                            elif direction == "right":
                                if up_attempts == 2 and down_attempts == 2:
                                    search_directions.append(
                                        {"direction": "right", "attempt": attempt}
                                    )
                                down_attempts = 2
                                search_directions.append(
                                    {"direction": "down", "attempt": attempt}
                                )
                            elif direction == "up":
                                up_attempts = 2
                                search_directions.append(
                                    {"direction": "up", "attempt": attempt}
                                )
                        else:
                            break
                    else:
                        logger.warning("WARNING: Farming interrupted (KS detected).")
            except Exception as ex:
                logger.error("ERROR: Farming routine failed. %s", ex)

    def run_app(self):
        logger.info("SYSTEM: Application started.")
        try:
            while True:
                self.window = getWindow("Rise of Kingdoms")

                cmd_window = getWindow("Administrator:  cmd_rokauto")
                if cmd_window:
                    screen_width, screen_height = pyautogui.size()
                    cmd_window.move_window(
                        x=screen_width - 315, y=200, width=315, height=300
                    )
                if self.window:
                    self.window.move_window(0, 0)
                    self.window.set_focus()
                    self.reconnect()
                    self.start_farming()
                    time.sleep(10)
                else:
                    self.start_game()
        except Exception as ex:
            logger.error("ERROR: Application failed. %s", ex)


import sys

if __name__ == "__main__":
    if len(sys.argv) != 4:
        logger.error(
            "ERROR: Invalid arguments. Usage: main.py <path> <team_number> <delay>"
        )
        sys.exit(1)
    app_path = sys.argv[1]
    total_teams = int(sys.argv[2])
    delay_time = int(sys.argv[3])
    logger.info(
        "SYSTEM: Initializing RokAuto with path: %s, team_number: %d, delay: %d",
        app_path,
        total_teams,
        delay_time,
    )
    rok_auto = RokAuto(app_path, total_teams, delay_time)
    rok_auto.run_app()

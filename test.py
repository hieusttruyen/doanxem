from autorok import RokAuto
from lib import getWindow, FindImgInWindow


def test_start_rok():
    path = "D:/Games/Rise of Kingdoms"
    team_number = 4
    delay = 2
    rok_auto = RokAuto(path, team_number, delay)

    # Giả lập việc không có cửa sổ Rise of Kingdoms nào mở
    rok_auto.window = None

    # Thực hiện phương thức start_rok
    rok_auto.start_rok("Rise of Kingdoms")

    assert rok_auto.window is not None, "Failed to start Rise of Kingdoms"


def test_farm():
    path = "D:/Games/Rise of Kingdoms"
    team_number = 4
    delay = 2
    rok_auto = RokAuto(path, team_number, delay)

    rok_auto.window = getWindow("Rise of Kingdoms")

    # Giả lập việc không có cửa sổ Rise of Kingdoms nào mở
    rok_auto.window.move_window(0, 0)

    rok_auto.window.set_focus()

    # Thực hiện phương thức start_rok
    locations = FindImgInWindow(rok_auto.window, rok_auto.img_team_running_new, threshold=0.9)


test_farm()

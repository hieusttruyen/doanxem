from pywinauto import Desktop
from pywinauto.findwindows import ElementNotFoundError
from PIL import ImageGrab, Image
import time
import cv2
import numpy as np
import ctypes


def capture_window_screenshot(window_title):
    """
    Chụp ảnh màn hình của cửa sổ với tiêu đề cụ thể và trả về đối tượng hình ảnh PIL.

    Args:
        window_title (str): Tiêu đề của cửa sổ cần chụp.

    Returns:
        PIL.Image.Image: Đối tượng hình ảnh PIL của ảnh chụp màn hình cửa sổ.
    """
    try:
        # Lấy cửa sổ theo tiêu đề
        window = Desktop(backend="win32").window(title=window_title)

        # Đưa cửa sổ lên phía trước và đợi để chắc chắn nó đã được kích hoạt
        window.set_focus()
        time.sleep(2)  # Đợi 2 giây để cửa sổ được kích hoạt hoàn toàn

        # Lấy vị trí và kích thước của cửa sổ
        left, top, right, bottom = (
            window.rectangle().left,
            window.rectangle().top,
            window.rectangle().right,
            window.rectangle().bottom,
        )

        # print(left, top, right, bottom)
        # Sử dụng ImageGrab để chụp ảnh màn hình của khu vực cửa sổ
        screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))

        return screenshot, left, top, right, bottom

    except ElementNotFoundError:
        print(f"Cửa sổ với tiêu đề '{window_title}' không tìm thấy")
        return None

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
        return None


def find_and_get_coordinates(
    large_image_path,
    small_image_path,
    method=cv2.TM_CCOEFF_NORMED,
    threshold=0.8,
    min_distance=50,
):
    """
    Tìm kiếm hình ảnh con trong hình ảnh lớn, lọc các vị trí gần nhau và trả về các tọa độ tìm thấy.

    Args:
        large_image_path (str): Đường dẫn tới ảnh lớn.
        small_image_path (str): Đường dẫn tới ảnh mẫu.
        method (int): Phương pháp so khớp mẫu của OpenCV.
        threshold (float): Ngưỡng để xác định sự khớp chính xác.
        min_distance (int): Khoảng cách tối thiểu giữa các vị trí tìm thấy để lọc các điểm gần nhau.

    Returns:
        list: Danh sách các tọa độ (x, y) của các vị trí tìm thấy sau khi lọc.
    """

    def find_image_in_image(
        large_image_path, small_image_path, method=cv2.TM_CCOEFF_NORMED, threshold=0.8
    ):
        # Đọc ảnh lớn và ảnh nhỏ
        large_image = cv2.imread(large_image_path)
        small_image = cv2.imread(small_image_path)

        # Chuyển ảnh sang grayscale
        large_gray = cv2.cvtColor(large_image, cv2.COLOR_BGR2GRAY)
        small_gray = cv2.cvtColor(small_image, cv2.COLOR_BGR2GRAY)

        # Thực hiện so khớp mẫu
        result = cv2.matchTemplate(large_gray, small_gray, method)

        # Ngưỡng để xác định sự khớp chính xác
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            loc = np.where(result <= threshold)
        else:
            loc = np.where(result >= threshold)

        # Danh sách các vị trí khớp
        locations = list(zip(*loc[::-1]))

        return locations, small_image.shape[1], small_image.shape[0]

    def filter_close_points(points, min_distance):
        filtered_points = []
        for p in points:
            if all(
                np.linalg.norm(np.array(p) - np.array(fp)) >= min_distance
                for fp in filtered_points
            ):
                filtered_points.append(p)
        return filtered_points

    # Tìm kiếm hình ảnh con trong hình ảnh lớn
    locations, w, h = find_image_in_image(
        large_image_path, small_image_path, method, threshold
    )

    # Lọc các vị trí gần nhau
    filtered_locations = filter_close_points(locations, min_distance)

    return filtered_locations


# Sử dụng SendInput để gửi phím Enter
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL),
    ]


class HardwareInput(ctypes.Structure):
    _fields_ = [
        ("uMsg", ctypes.c_ulong),
        ("wParamL", ctypes.c_short),
        ("wParamH", ctypes.c_short),
    ]


class MouseInput(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL),
    ]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput), ("mi", MouseInput), ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("ii", Input_I)]


def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(hexKeyCode, 0x48, 0, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(hexKeyCode, 0x48, 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def PressKeyandRelease(hexKeyCode, delay=0.1):
    PressKey(hexKeyCode)
    time.sleep(delay)
    ReleaseKey(hexKeyCode)


def find_image_in_image(
    screenshot, find_img, method=cv2.TM_CCOEFF_NORMED, threshold=0.8
):
    # Đọc ảnh lớn và ảnh nhỏ
    # large_image = cv2.imread(large_image_path)
    main_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    find_gray = cv2.cvtColor(np.array(find_img), cv2.COLOR_RGB2BGR)

    # # Chuyển ảnh sang grayscale
    # large_gray = cv2.cvtColor(large_image, cv2.COLOR_BGR2GRAY)
    # small_gray = cv2.cvtColor(small_image, cv2.COLOR_BGR2GRAY)

    # large_gray_pil.show()
    # Thực hiện so khớp mẫu
    result = cv2.matchTemplate(main_gray, find_gray, method, 0.7)

    # Ngưỡng để xác định sự khớp chính xác
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        loc = np.where(result <= threshold)
    else:
        loc = np.where(result >= threshold)

    # Danh sách các vị trí khớp
    locations = list(zip(*loc[::-1]))
    filtered_locations = filter_close_points(locations, min_distance=50)

    return filtered_locations, find_gray.shape[1], find_gray.shape[0]


def filter_close_points(points, min_distance):
    filtered_points = []
    for p in points:
        if all(
            np.linalg.norm(np.array(p) - np.array(fp)) >= min_distance
            for fp in filtered_points
        ):
            filtered_points.append(p)
    return filtered_points

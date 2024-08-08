import cv2
import numpy as np
from PIL import Image, ImageEnhance
import pyautogui
import time
from lib import getWindow, FindImgInWindow
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\HieuEpoh\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)


def preprocess_image(img):
    # Chuyển đổi sang grayscale
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)

    # Áp dụng Gaussian Blur để làm mờ hình ảnh
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Áp dụng ngưỡng nhị phân hóa
    _, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return binary


def enhance_image(pil_img):
    # Tăng độ tương phản và độ sắc nét của hình ảnh
    enhancer = ImageEnhance.Contrast(pil_img)
    pil_img = enhancer.enhance(2)

    enhancer = ImageEnhance.Sharpness(pil_img)
    pil_img = enhancer.enhance(2)

    return pil_img


def upscale_image(image, scale_percent=200):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    # Resize hình ảnh
    return cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)


def image_to_text(img):
    # Open the image file
    # img = Image.open(image_path)
    processed_image = preprocess_image(img)
    # Tăng độ phân giải hình ảnh
    # upscaled_image = upscale_image(processed_image)

    # Chuyển đổi hình ảnh từ OpenCV sang định dạng PIL
    pil_img = Image.fromarray(processed_image)

    # Tăng cường hình ảnh
    # pil_img = enhance_image(pil_img)

    # pil_img.show()
    # Use pytesseract to do OCR on the image
    custom_config = r"--oem 3 --psm 6 -c tessedit_char_whitelist=.0123456789MB"
    text = pytesseract.image_to_string(img, config=custom_config)

    return text


window_title = "Rise of Kingdoms"
window = getWindow(window_title)
window.set_focus()
time.sleep(2)
# img_gem_map = Image.open("./img//Screenshot 2024-08-08 122500.png")
# locations = FindImgInWindow(window, img_gem_map, threshold=0.7)
# screenshot = window.capture_as_image()

# if locations:
#     print("Yeah thấy mở gem rồi...")
#     x, y = locations
#     h, w = img_gem_map.size
#     crop_coordinates = (x + 150, y - h , x + h + 30, y + w - 220)
#     cropped_image = screenshot.crop(crop_coordinates)
#     # cropped_image.show()
#     # cropped_image.show()
#     text = image_to_text(cropped_image)
#     print(text)
img_gem_map = Image.open("./img//Screenshot 2024-08-08 122500.png")
text = image_to_text(img_gem_map)
print(text)

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

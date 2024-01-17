import pytesseract
import cv2
from PIL import Image



img = cv2.imread("splited/00.png")
custom_config = r'--oem 3 --psm 10'
res = pytesseract.image_to_string(img, config=custom_config)
print("\"" + res + "\"")





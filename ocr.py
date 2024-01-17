import pytesseract
import cv2


IMAGE_BASE_FOLDER = "splited/"


def ocr_image(image_name):
    img = cv2.imread(IMAGE_BASE_FOLDER + image_name)
    result_str = pytesseract.image_to_string(img, config='--psm 10 --oem 3 -c tessedit_char_whitelist=123456789')
    return result_str

def ocr_image_to_GridObj(grid):
    
    for i in range(9):
        for j in range(9):
            ocr_result_string = ocr_image(f"{i}{j}.jpg")

            print(i, j, " : ","\"" + ocr_result_string + "\"")

            if ocr_result_string != "":
                num = int(ocr_result_string)
                if num > 10:
                    num %= 10

                grid.add_number(i, j, num)

  



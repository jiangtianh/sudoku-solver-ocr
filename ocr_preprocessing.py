import cv2
import numpy as np


'''
Invert the image 's colors 
input:
    image -> image to be inverted as a numpy array
'''
def invert(image):
    return cv2.bitwise_not(image)

'''
Perform a series of operations to preprocess the image for better OCR results
input:
    img_name -> The file path of the image to be preprocessed as a string 
'''
def preprocessing(img_name):
    img = cv2.imread(img_name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    gray = cv2.adaptiveThreshold(gray, 255, 1, 1, 11, 2)
    gray = binarize(gray)

    return gray

'''
This method is used to locate the sudoku puzzle in the image. Take the np array of the image as input, and finds the corners for the actual Sudoku puzzle. 
input:
    h -> The np array of the image
output:
    hnew -> The np array of the corners of the sudoku puzzle as a np array
'''
def rectify(h):
    h = h.reshape((4, 2))
    hnew = np.zeros((4, 2), dtype = np.float32)
    add = h.sum(axis = 1)
    hnew[0] = h[np.argmin(add)]
    hnew[2] = h[np.argmax(add)]
    diff = np.diff(h, axis = 1)
    hnew[1] = h[np.argmin(diff)]
    hnew[3] = h[np.argmax(diff)]
    return hnew

'''
This func finds the general area where your sudoku puzzle is located and return a new image with only the puzzle in it.
input:
    img_name -> The file path of the image to be preprocessed as a string
output:
    warp -> The image of the puzzle only
'''
def locate_puzzle(img_name):
    gray = preprocessing(img_name)
    contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    biggest = None 
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 100:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    
    if biggest is not None:
        biggest = rectify(biggest)
        h = np.array([[0, 0], [449, 0], [449, 449], [0, 449]], np.float32)
        retval = cv2.getPerspectiveTransform(biggest, h)
        warp = cv2.warpPerspective(gray, retval, (450, 450))
        return warp
    else:
        print("Error while locating puzzle")
        return None 

'''
This method splits the sudoku puzzle into 81 individual cells and return a dictionary of the cells.
input:
    img_name -> The file path of the image to be preprocessed as a string
output:
    d -> The dictionary of the cells as a nested dictionary with the format d[row][col] = cell
'''
def split_sudoku_cells(img_name):
    d = {}
    warp = locate_puzzle(img_name)
    for i in range(9):
        d[i] = {}
        for j in range(9):
            d[i][j] = []

    arr = np.split(warp, 9)
    for i in range(9):
        for j in range(9):
            for a in range(len(arr[i])):
                cells = np.split(arr[i][a], 9)
                d[i][j].append(np.array(cells[j]))

            d[i][j] = thin_font(np.array(d[i][j]))
    return d

'''
This method binarizes the image. 
input:
    image -> The image to be binarized as a numpy array
output:
    im_bw -> The binarized image as a numpy array
'''
def binarize(image):
    thresh, im_bw = cv2.threshold(image, 180, 230, cv2.THRESH_BINARY)
    return im_bw


'''
This method will first call the split_sudoku_cells method to get the dictionary of the cells, then it will write the cells to the splited folder.
input:
    image_name -> The file path of the image to be preprocessed as a string
'''
def write_image_to_file(image_name):
    dictionary = split_sudoku_cells(image_name)
    for i in range(9):
        for j in range(9):
            cv2.imwrite(f"splited/{i}{j}.jpg", dictionary[i][j])
                
'''
This method will remove the borders of the image, if it finds any. 
input:
    image -> The image to be processed as a numpy array
output:
    image -> The image without borders as a numpy array
'''
def remove_borders(image):
    contours, heiarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntSorted = sorted(contours, key=lambda x:cv2.contourArea(x))
    cnt = cntSorted[-1]
    x, y, w, h = cv2.boundingRect(cnt)
    return image[y:y+h, x:x+w]

'''
This method will make the font of the image thinner.
input:
    image -> The image to be processed as a numpy array
output:
    image -> The image with thinned font as a numpy array
'''
def thin_font(image):
    image = cv2.bitwise_not(image)
    kernel = np.ones((2,2),np.uint8)
    image = cv2.bitwise_not(image)
    return cv2.erode(image, kernel, iterations = 1)









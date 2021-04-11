import cv2
import numpy as np
import time

# captures a video
capture = cv2.VideoCapture(0) 

# suspending execution for 3 seconds
time.sleep(3) 

background = 0

# capturing frame by frame
for i in range(30):
    ret, background = capture.read() 

# flipping the background horizontally
background = np.flip(background, axis=1) 

while (capture.isOpened()):
    ret, img = capture.read()
 
    # flipping the image horizontally
    img = np.flip(img, axis=1)
 
    # converting image to HSV color space.
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    value = (35, 35)

    # convolving image with gaussian filter
    blurred = cv2.GaussianBlur(hsv, value, 0)
 
    # defining lower range for red color detection.
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
 
    # defining upper range for red color detection
    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)
 
    # addition of the two masks to generate the final mask.
    mask = mask1 + mask2
    
    # removing noise
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8), iterations=2)
    
    # increases the smoothness of the image
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((5, 5), np.uint8), iterations=1)
 
    # replacing pixels corresponding to cloak with the background pixels.
    img[np.where(mask == 255)] = background[np.where(mask == 255)]
    
    # displaying the image
    cv2.imshow('Display', img)
    
    
    k = cv2.waitKey(10)
    
    # pressing Esc Key stops the program
    if k == 27:
        break

# releasing the video
capture.release()

#destroys all the windows we created
cv2.destroyAllWindows() 


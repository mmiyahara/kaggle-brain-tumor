# https://docs.opencv.org/master/db/deb/tutorial_display_image.html
import cv2 as cv
import os, sys

file_abs_dir = os.path.dirname(os.path.abspath(__file__))
img = cv.imread(os.path.join(file_abs_dir, "lenna.png"))
if img is None:
    sys.exit("Could not read the image.")

cv.imshow("Display window", img)
k = cv.waitKey(0)

if k == ord("s"):
    cv.imwrite(os.path.join(file_abs_dir, "lenna_write.png"), img)

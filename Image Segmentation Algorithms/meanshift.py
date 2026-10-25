import cv2

image = cv2.imread(r"C:\Users\Vaibhav.S.P\Downloads\IPCV Lab\IPCV Lab\03_13_07_2026_IPCV\Image Segmentation Algorithms\image.png")

shift = cv2.pyrMeanShiftFiltering(image,20,40)

cv2.imshow("Mean Shift",shift)
cv2.waitKey(0)
import cv2

image = cv2.imread(r"C:\Users\Vaibhav.S.P\Downloads\IPCV Lab\IPCV Lab\03_13_07_2026_IPCV\Image Segmentation Algorithms\image.png",0)

edges = cv2.Canny(image,100,200)

cv2.imshow("Edges",edges)
cv2.waitKey(0)

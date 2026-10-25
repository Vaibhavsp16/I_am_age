import cv2

# Option A: Load the image directly as grayscale
image = cv2.imread(r"C:\Users\Vaibhav.S.P\Downloads\IPCV Lab\IPCV Lab\03_13_07_2026_IPCV\Image Segmentation Algorithms\image.png", cv2.IMREAD_GRAYSCALE)

# Option B (Alternative): Load normally and convert to grayscale
# image = cv2.imread(r"C:\Users\Vaibhav.S.P\Downloads\IPCV Lab\IPCV Lab\03_13_07_2026_IPCV\Image Segmentation Algorithms\image.png")
# image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

adaptive = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

cv2.imshow("Adaptive Threshold", adaptive)
cv2.waitKey(0)
cv2.destroyAllWindows()
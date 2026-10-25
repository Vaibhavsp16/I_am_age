import cv2

# Load the image directly in grayscale
image = cv2.imread(r"C:\Users\Vaibhav.S.P\Downloads\IPCV Lab\IPCV Lab\03_13_07_2026_IPCV\Image Segmentation Algorithms\image.png", cv2.IMREAD_GRAYSCALE)

_, otsu = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

cv2.imshow("Otsu", otsu)
cv2.waitKey(0)
cv2.destroyAllWindows()
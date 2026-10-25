import cv2
import matplotlib.pyplot as plt

image = cv2.imread(r"C:\Users\Vaibhav.S.P\Downloads\IPCV Lab\IPCV Lab\03_13_07_2026_IPCV\Image Segmentation Algorithms\image.png")

_,segmented = cv2.threshold(image,127,255,cv2.THRESH_BINARY)

plt.subplot(1,2,1)
plt.imshow(image,cmap="gray")
plt.title("Original")

plt.subplot(1,2,2)
plt.imshow(segmented,cmap="gray")
plt.title("Segmented")

plt.show()


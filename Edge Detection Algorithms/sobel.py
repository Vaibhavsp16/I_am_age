import cv2
import matplotlib.pyplot as plt

image = cv2.imread("image.png",0)

sobelx = cv2.Sobel(image,cv2.CV_64F,1,0,ksize=3)
sobely = cv2.Sobel(image,cv2.CV_64F,0,1,ksize=3)

plt.imshow(sobelx,cmap="gray")
plt.title("Sobel X Edge")
plt.show()

plt.imshow(sobely,cmap="gray")
plt.title("Sobel Y Edge")
plt.show()
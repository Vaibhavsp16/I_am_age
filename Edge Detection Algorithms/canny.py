import cv2
import matplotlib.pyplot as plt

image = cv2.imread("image.png",0)

canny = cv2.Canny(image,100,200)

plt.imshow(canny,cmap="gray")
plt.title("Canny")
plt.show()
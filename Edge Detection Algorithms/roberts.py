import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread("image.png",0)

kernelx = np.array([[1,0],[0,-1]])
kernely = np.array([[0,1],[-1,0]])

robertsx = cv2.filter2D(image,-1,kernelx)
robertsy = cv2.filter2D(image,-1,kernely)

plt.imshow(robertsx,cmap="gray")
plt.title("Roberts X")
plt.show()

plt.imshow(robertsy,cmap="gray")
plt.title("Roberts Y")
plt.show()
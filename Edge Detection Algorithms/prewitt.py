import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread("image.png",0)

kernelx = np.array([[1,0,-1],[1,0,-1],[1,0,-1]])
kernely = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])

prewittx = cv2.filter2D(image,-1,kernelx)
prewitty = cv2.filter2D(image,-1,kernely)

plt.imshow(prewittx,cmap="gray")
plt.title("Prewitt X")
plt.show()

plt.imshow(prewitty,cmap="gray")
plt.title("Prewitt Y")
plt.show()
import cv2
import matplotlib.pyplot as plt

image = cv2.imread("image.png",0)

laplacian = cv2.Laplacian(image,cv2.CV_64F)

plt.imshow(laplacian,cmap="gray")
plt.title("Laplacian")
plt.show()
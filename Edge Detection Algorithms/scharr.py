import cv2
import matplotlib.pyplot as plt

image = cv2.imread("image.png",0)

scharrx = cv2.Scharr(image,cv2.CV_64F,1,0)
scharry = cv2.Scharr(image,cv2.CV_64F,0,1)

plt.imshow(scharrx,cmap="gray")
plt.title("Scharr X")
plt.show()

plt.imshow(scharry,cmap="gray")
plt.title("Scharr Y")
plt.show()
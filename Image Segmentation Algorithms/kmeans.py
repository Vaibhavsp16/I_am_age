import cv2
import numpy as np

image = cv2.imread(r"C:\Users\Vaibhav.S.P\Downloads\IPCV Lab\IPCV Lab\03_13_07_2026_IPCV\Image Segmentation Algorithms\image.png")

Z = image.reshape((-1,3))
Z = np.float32(Z)

criteria = (
    cv2.TERM_CRITERIA_EPS+
    cv2.TERM_CRITERIA_MAX_ITER,
    10,
    1.0
)

K = 4

ret, label, center = cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

center = np.uint8(center)

result = center[label.flatten()]
result = result.reshape(image.shape)

cv2.imshow("KMeans",result)
cv2.waitKey(0)
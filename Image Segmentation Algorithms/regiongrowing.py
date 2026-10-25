from skimage.segmentation import flood
from skimage import io
import matplotlib.pyplot as plt

image = io.imread(r"C:\Users\Vaibhav.S.P\Downloads\IPCV Lab\IPCV Lab\03_13_07_2026_IPCV\Image Segmentation Algorithms\image.png",as_gray=True)

segmented = flood(image,(100,100),tolerance=0.1)

plt.imshow(segmented,cmap="gray")
plt.show()

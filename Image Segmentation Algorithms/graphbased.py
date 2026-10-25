from skimage.segmentation import felzenszwalb
from skimage import io
import matplotlib.pyplot as plt

image = io.imread(r"C:\Users\Vaibhav.S.P\Downloads\IPCV Lab\IPCV Lab\03_13_07_2026_IPCV\Image Segmentation Algorithms\image.png")

segments = felzenszwalb(
    image,
    scale=100,
    sigma=0.5,
    min_size=50
)

plt.imshow(segments)
plt.show()

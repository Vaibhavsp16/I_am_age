import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# Read image
path = os.path.join(os.path.dirname(__file__), "image3.png")
img = cv2.imread(path, 0)

if img is None:
    raise FileNotFoundError("image3.png not found")

# Histogram equalization
eq = cv2.equalizeHist(img)

def string_art(img):
    edges = cv2.Canny(img, 50, 150)

    lines = cv2.HoughLinesP(
        edges, 1, np.pi / 180, 50,
        minLineLength=30, maxLineGap=10
    )

    art = np.ones_like(img) * 255

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.flatten()
            cv2.line(art, (x1, y1), (x2, y2), 0, 1)

    return art

art1 = string_art(img)
art2 = string_art(eq)

plt.figure(figsize=(10, 6))

plt.subplot(2, 3, 1)
plt.imshow(img, cmap="gray")
plt.title("Original")
plt.axis("off")

plt.subplot(2, 3, 2)
plt.hist(img.ravel(), 256)
plt.title("Original Histogram")

plt.subplot(2, 3, 3)
plt.imshow(art1, cmap="gray")
plt.title("String Art")
plt.axis("off")

plt.subplot(2, 3, 4)
plt.imshow(eq, cmap="gray")
plt.title("Equalized")
plt.axis("off")

plt.subplot(2, 3, 5)
plt.hist(eq.ravel(), 256)
plt.title("Equalized Histogram")

plt.subplot(2, 3, 6)
plt.imshow(art2, cmap="gray")
plt.title("String Art After Equalization")
plt.axis("off")

plt.tight_layout()
plt.show()
import cv2
import matplotlib.pyplot as plt

image = cv2.imread(r"C:\Users\Vaibhav.S.P\Downloads\IPCV Lab\IPCV Lab\02_06_07_2026_IPCV\black_square.jpg")

if image is None:
    raise FileNotFoundError("Image not found.")

# Convert BGR to RGB
image_rgb = image[:, :, ::-1]

negative = 255 - image_rgb

plt.subplot(1, 2, 1)
plt.imshow(image_rgb)
plt.title("Original")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(negative)
plt.title("Negative")
plt.axis("off")

plt.show()
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read selfie
img = cv2.imread(r"C:\Users\Vaibhav.S.P\Downloads\IPCV Lab\IPCV Lab\07_24_08_2026_IPCV\q10\selfie.jpg")

if img is None:
    raise FileNotFoundError("Image not found")

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

h, w = img.shape[:2]


# Function to apply a 2D transformation matrix manually
def transform(img, M):
    h, w = img.shape[:2]

    # Center of image
    cx, cy = w / 2, h / 2

    result = np.zeros_like(img)

    # Inverse transformation
    inv = np.linalg.inv(M)

    for y in range(h):
        for x in range(w):

            # Move origin to center
            p = np.array([x - cx, y - cy, 1])

            # Apply inverse transformation
            q = inv @ p

            # Move origin back
            xx = int(round(q[0] + cx))
            yy = int(round(q[1] + cy))

            if 0 <= xx < w and 0 <= yy < h:
                result[y, x] = img[yy, xx]

    return result


# 1. Rotation matrix - 30 degrees
theta = np.radians(30)

R = np.array([
    [np.cos(theta), -np.sin(theta), 0],
    [np.sin(theta),  np.cos(theta), 0],
    [0,              0,             1]
])


# 2. Scaling matrix
S = np.array([
    [1.5, 0,   0],
    [0,   1.5, 0],
    [0,   0,   1]
])


# 3. Shearing matrix
Sh = np.array([
    [1, 0.5, 0],
    [0, 1,   0],
    [0, 0,   1]
])


# Apply transformations
rotated = transform(img, R)
scaled = transform(img, S)
sheared = transform(img, Sh)


# Display
plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.imshow(img)
plt.title("Original")
plt.axis("off")

plt.subplot(2, 2, 2)
plt.imshow(rotated)
plt.title("Rotation")
plt.axis("off")

plt.subplot(2, 2, 3)
plt.imshow(scaled)
plt.title("Scaling")
plt.axis("off")

plt.subplot(2, 2, 4)
plt.imshow(sheared)
plt.title("Shearing")
plt.axis("off")

plt.tight_layout()
plt.show()
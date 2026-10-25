import numpy as np
import cv2
import matplotlib.pyplot as plt

# -----------------------------
# 1. Create image with triangles
# -----------------------------
H, W = 500, 700
img = np.zeros((H, W), dtype=np.uint8)

# Triangle size
side = 50
height = int(np.sqrt(3) * side / 2)

# Spacing between triangles
gap_x = 30
gap_y = 30

# Draw same-size, non-overlapping triangles
for row, y in enumerate(range(40, H - height, height + gap_y)):
    for col, x in enumerate(range(30, W - side, side + gap_x)):

        # Alternate triangle orientation
        if (row + col) % 2 == 0:
            pts = np.array([
                [x, y + height],
                [x + side, y + height],
                [x + side // 2, y]
            ], np.int32)
        else:
            pts = np.array([
                [x, y],
                [x + side, y],
                [x + side // 2, y + height]
            ], np.int32)

        # Fill triangle with white
        cv2.fillPoly(img, [pts], 255)


# -----------------------------------
# 2. Define convolutional kernel
# -----------------------------------
# 8-neighbor Laplacian / edge detector
kernel = np.array([
    [-1, -1, -1],
    [-1,  8, -1],
    [-1, -1, -1]
], dtype=np.float32)


# -----------------------------
# 3. Perform convolution
# -----------------------------
output = cv2.filter2D(img, ddepth=cv2.CV_32F, kernel=kernel)

# Convert result to displayable image
output = np.abs(output)
output = np.clip(output, 0, 255).astype(np.uint8)


# -----------------------------
# 4. Display results
# -----------------------------
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.imshow(img, cmap='gray')
plt.title("Original Image - Triangles")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(output, cmap='gray')
plt.title("Convolution Output")
plt.axis("off")

plt.tight_layout()
plt.show()
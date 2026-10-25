import numpy as np
import cv2
import matplotlib.pyplot as plt

# -------------------------------------------------------------
# Register Number Analysis:
# Register Number: 3122235002146
# 3122235002146 % 2 == 0 -> Divisible by 2 -> Non-Overlapping Circles (Same Size)
# -------------------------------------------------------------
reg_no = 3122235002146

# -----------------------------
# 1. Create image with circles
# -----------------------------
H, W = 500, 700
img = np.zeros((H, W), dtype=np.uint8)

# Circle parameters (same size)
radius = 25
diameter = 2 * radius

# Spacing between circles to ensure non-overlapping
gap_x = 30
gap_y = 30

# Draw same-size, non-overlapping circles in a grid
for y in range(radius + 35, H - radius, diameter + gap_y):
    for x in range(radius + 35, W - radius, diameter + gap_x):
        # Draw filled circle with white color (255)
        cv2.circle(img, (x, y), radius, 255, -1)


# -----------------------------------
# 2. Define convolutional kernel
# -----------------------------------
# 8-neighbor Laplacian kernel (Isotropic edge detector, ideal for circular boundaries)
kernel = np.array([
    [-1, -1, -1],
    [-1,  8, -1],
    [-1, -1, -1]
], dtype=np.float32)


# -----------------------------
# 3. Perform convolution
# -----------------------------
# cv2.filter2D performs spatial convolution/correlation with the kernel
output = cv2.filter2D(img, ddepth=cv2.CV_32F, kernel=kernel)

# Convert result to displayable uint8 image
output = np.abs(output)
output = np.clip(output, 0, 255).astype(np.uint8)


# -----------------------------
# 4. Display results
# -----------------------------
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.imshow(img, cmap='gray')
plt.title(f"Original Image - Circles (Reg No: {reg_no} % 2 == 0)")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(output, cmap='gray')
plt.title("Convolution Output (Laplacian Edge Kernel)")
plt.axis("off")

plt.tight_layout()
plt.show()

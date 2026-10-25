import cv2
import numpy as np

img = cv2.imread(r"C:\Users\Vaibhav.S.P\Downloads\IPCV Lab\IPCV Lab\03_13_07_2026_IPCV\q8\selfie.jpg")

# 1. Convert the input image to a float array first to prevent uint8 overflow
img_float = img.astype(np.float32)

max_val = np.max(img_float)

# 2. Check for a completely black image to avoid dividing by zero
if max_val == 0:
    log_transformed = np.zeros_like(img, dtype=np.uint8)
else:
    # 3. Perform calculations safely using the float array
    c = 255.0 / np.log(1.0 + max_val)
    log_transformed_float = c * np.log(1.0 + img_float)

    # 4. Use np.clip to guarantee values stay strictly between 0 and 255
    log_transformed_clipped = np.clip(log_transformed_float, 0, 255)

    # 5. Cast safely back to uint8 without any warnings
    log_transformed = log_transformed_clipped.astype(np.uint8)


cv2.imwrite('log_transformed.jpg', log_transformed)

import cv2
import numpy as np

img = cv2.imread(r"selfie.jpg", 0)

negative_img = 255 - img

cv2.imshow('Original Image', img)
cv2.imshow('Negative Image', negative_img)

cv2.waitKey(0)
cv2.destroyAllWindows()

import cv2
import numpy as np

# Open the image.
img = cv2.imread(r"C:\Users\Vaibhav.S.P\Downloads\IPCV Lab\IPCV Lab\03_13_07_2026_IPCV\q8\selfie.jpg")

# Trying 4 gamma values.
for gamma in [0.1, 0.5, 1.2, 2.2]:
    
    # Apply gamma correction.
    gamma_corrected = np.array(255*(img / 255) ** gamma, dtype = 'uint8')

    # Save edited images.
    cv2.imwrite('gamma_transformed'+str(gamma)+'.jpg', gamma_corrected)

import cv2
import numpy as np

# Function to map each intensity level to output intensity level
def pixelVal(pix, r1, s1, r2, s2):
    if 0 <= pix <= r1:
        return (s1 / r1) * pix
    elif r1 < pix <= r2:
        return ((s2 - s1) / (r2 - r1)) * (pix - r1) + s1
    else:
        return ((255 - s2) / (255 - r2)) * (pix - r2) + s2

# Read the image
img = cv2.imread(r"C:\Users\Vaibhav.S.P\Downloads\IPCV Lab\IPCV Lab\03_13_07_2026_IPCV\q8\selfie.jpg")

# Check if image is loaded successfully
if img is None:
    raise FileNotFoundError("Image 'selfie.jpg' not found.")

# Define parameters
r1 = 70
s1 = 0
r2 = 140
s2 = 255

# Vectorize the function
pixelVal_vec = np.vectorize(pixelVal)

# Apply contrast stretching
contrast_stretched = pixelVal_vec(img, r1, s1, r2, s2)

# Convert output to uint8
contrast_stretched = np.clip(contrast_stretched, 0, 255).astype(np.uint8)

# Save the result
cv2.imwrite("contrast_stretch.jpg", contrast_stretched)

# Display original and processed images
cv2.imshow("Original Image", img)
cv2.imshow("Contrast Stretched Image", contrast_stretched)

cv2.waitKey(0)
cv2.destroyAllWindows()
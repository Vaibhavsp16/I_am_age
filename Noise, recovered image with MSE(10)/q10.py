import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import uniform_filter

# 1. Load your own image
image_path = r"C:\Users\Vaibhav.S.P\Downloads\IPCV Lab\IPCV Lab\07_24_08_2026_IPCV\q10\selfie.jpg"

# Load image in color
original_img = cv2.imread(image_path)

if original_img is None:
    raise FileNotFoundError(
        f"Could not load image at path: {image_path}. Check the filename."
    )

# OpenCV loads images in BGR format.
# Convert BGR to RGB for displaying correctly with matplotlib.
original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)

# Convert to float64 for precise mathematical calculations
original_img = original_img.astype(np.float64)

# 2. Generate the Gaussian noise matrix
# Mean = 110, Sigma = 5
mean = 110
sigma = 5

noise_matrix = np.random.normal(
    loc=mean,
    scale=sigma,
    size=original_img.shape
)

# 3. Add noise matrix to original image matrix
noisy_img = original_img + noise_matrix

# Keep pixel values within valid image range [0, 255]
noisy_img = np.clip(noisy_img, 0, 255)

# 4. Apply the (5x5) averaging filter/kernel
# (5, 5, 1) means:
# 5x5 spatial averaging, without mixing RGB channels
recovered_img = uniform_filter(
    noisy_img,
    size=(5, 5, 1),
    mode='reflect'
)

# 5. Calculate Mean Square Error (MSE)
def calculate_mse(matrix_a, matrix_b):
    return np.mean((matrix_a - matrix_b) ** 2)

mse_noisy = calculate_mse(original_img, noisy_img)
mse_recovered = calculate_mse(original_img, recovered_img)

# 6. Display evaluation metrics
print(f"--- Assignment Results for {image_path} ---")
print(f"Original image shape: {original_img.shape}")
print(f"MSE (Original vs Noisy Image):     {mse_noisy:.2f}")
print(f"MSE (Original vs Recovered Image): {mse_recovered:.2f}")

# 7. Visualise the results
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.title("1. Original Selfie")
plt.imshow(original_img.astype(np.uint8))
plt.axis('off')

plt.subplot(1, 3, 2)
plt.title("2. Noisy Image")
plt.imshow(noisy_img.astype(np.uint8))
plt.axis('off')

plt.subplot(1, 3, 3)
plt.title("3. Recovered Image")
plt.imshow(recovered_img.astype(np.uint8))
plt.axis('off')

plt.tight_layout()
plt.show()
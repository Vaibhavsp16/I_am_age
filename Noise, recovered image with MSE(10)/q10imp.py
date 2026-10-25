# -------------------------------------------------------------
# Question 10: Gaussian Noise, 5x5 Averaging Filter & MSE Calculation
# Pure Python Implementation (NO IMPORT MODULES USED)
# -------------------------------------------------------------

# 1. Pure Python Random Number Generator (LCG)
# Generates uniform float in (0, 1)
lcg_seed = 42

def uniform_random():
    global lcg_seed
    lcg_seed = (1103515245 * lcg_seed + 12345) & 0x7FFFFFFF
    return lcg_seed / 2147483648.0

# Standard Normal Random Variable N(0, 1) via Central Limit Theorem
# (Sum of 12 uniform random variables - 6 has mean 0 and variance 1)
def gaussian_random():
    return sum(uniform_random() for _ in range(12)) - 6.0

# 2. Sample 10x10 Original Grayscale Image
# Clean synthetic image with distinct structural regions
H, W = 10, 10
original_img = [
    [ 50,  50,  50,  50,  50, 200, 200, 200, 200, 200],
    [ 50,  50,  50,  50,  50, 200, 200, 200, 200, 200],
    [ 50,  50, 100, 100,  50, 200, 200, 200, 200, 200],
    [ 50,  50, 100, 100,  50, 200, 200, 150, 200, 200],
    [ 50,  50,  50,  50,  50, 200, 200, 200, 200, 200],
    [ 80,  80,  80,  80,  80, 120, 120, 120, 120, 120],
    [ 80,  80,  80,  80,  80, 120, 120, 120, 120, 120],
    [ 80,  80, 120, 120,  80, 120, 120, 180, 120, 120],
    [ 80,  80,  80,  80,  80, 120, 120, 120, 120, 120],
    [ 80,  80,  80,  80,  80, 120, 120, 120, 120, 120]
]

# 3. Add Gaussian Noise (Mean = 110, Sigma = 5)
mean = 110
sigma = 5

noisy_img = [[0.0 for _ in range(W)] for _ in range(H)]
for i in range(H):
    for j in range(W):
        # Generate Gaussian noise value
        noise = mean + sigma * gaussian_random()
        # Add to original and clip to valid image intensity range [0, 255]
        val = original_img[i][j] + noise
        noisy_img[i][j] = min(255.0, max(0.0, val))

# 4. Apply 5x5 Averaging Filter / Kernel (Spatial Mean Filter)
# Each pixel is replaced by the average of all valid pixels in its 5x5 neighborhood
recovered_img = [[0.0 for _ in range(W)] for _ in range(H)]
for i in range(H):
    for j in range(W):
        total = 0.0
        count = 0
        for di in range(-2, 3):
            for dj in range(-2, 3):
                ni, nj = i + di, j + dj
                if 0 <= ni < H and 0 <= nj < W:
                    total += noisy_img[ni][nj]
                    count += 1
        recovered_img[i][j] = total / count

# 5. Calculate Mean Square Error (MSE)
def calculate_mse(matrix_a, matrix_b):
    total_sq_err = 0.0
    h = len(matrix_a)
    w = len(matrix_a[0])
    for i in range(h):
        for j in range(w):
            diff = matrix_a[i][j] - matrix_b[i][j]
            total_sq_err += diff * diff
    return total_sq_err / (h * w)

mse_noisy = calculate_mse(original_img, noisy_img)
mse_recovered = calculate_mse(original_img, recovered_img)

# 6. Display Evaluation Metrics
print("=" * 65)
print(" QUESTION 10: GAUSSIAN NOISE, 5x5 AVERAGING FILTER & MSE")
print("=" * 65)
print(f"Image Dimensions                   : {H} x {W}")
print(f"Noise Parameters                   : Mean = {mean}, Sigma = {sigma}")
print(f"MSE (Original vs. Noisy Image)     : {mse_noisy:.2f}")
print(f"MSE (Original vs. Recovered Image) : {mse_recovered:.2f}")
print("=" * 65)

# 7. Print matrices sample comparison (Center 4x4 region)
print("\n--- Center (4x4) Original Image Pixels ---")
for r in range(3, 7):
    print("  ", [f"{int(original_img[r][c]):3d}" for c in range(3, 7)])

print("\n--- Center (4x4) Noisy Image Pixels (Original + Noise) ---")
for r in range(3, 7):
    print("  ", [f"{int(noisy_img[r][c]):3d}" for c in range(3, 7)])

print("\n--- Center (4x4) Recovered Image Pixels (5x5 Mean Filtered) ---")
for r in range(3, 7):
    print("  ", [f"{int(recovered_img[r][c]):3d}" for c in range(3, 7)])

print("\nConclusion: 5x5 averaging smooths out local high-frequency noise.")
print("=" * 65)

# -------------------------------------------------------------
# Question 13: Histogram Equalization & String Art / Edge Output
# Pure Python Implementation (NO IMPORT MODULES USED)
# -------------------------------------------------------------

# Histogram Equalization Algorithm:
# 1. Compute frequency of each gray level: n_k for k in [0, 255]
# 2. Compute Cumulative Distribution Function: CDF(k) = sum_{j=0}^k n_j
# 3. Compute equalized mapping: s_k = round((CDF(k) - CDF_min) / (Total - CDF_min) * 255)
#    or standard: s_k = round((CDF(k) / Total) * 255)
# 4. Map original pixel values to equalized pixel values

# 1. Pure Python Histogram Calculation
def compute_histogram(image_matrix):
    hist = [0] * 256
    for row in image_matrix:
        for pix in row:
            hist[pix] += 1
    return hist

# 2. Pure Python Histogram Equalization
def equalize_histogram(image_matrix):
    H = len(image_matrix)
    W = len(image_matrix[0])
    total_pixels = H * W
    
    hist = compute_histogram(image_matrix)
    
    # Cumulative Distribution Function (CDF)
    cdf = [0] * 256
    running_sum = 0
    for k in range(256):
        running_sum += hist[k]
        cdf[k] = running_sum
        
    # Transformation mapping table
    mapping = [0] * 256
    for k in range(256):
        mapping[k] = int(round((cdf[k] / total_pixels) * 255.0))
        
    # Map input pixels to equalized pixels
    equalized_img = [[mapping[pix] for pix in row] for row in image_matrix]
    equalized_hist = compute_histogram(equalized_img)
    
    return equalized_img, hist, equalized_hist, mapping

# 3. Pure Python Sobel Edge Detection (String Art / Outline Feature)
def detect_edges(image_matrix):
    H = len(image_matrix)
    W = len(image_matrix[0])
    
    # Sobel kernels
    # Gx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    # Gy = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
    edges = [[255 for _ in range(W)] for _ in range(H)]  # White canvas
    
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            gx = (
                -1 * image_matrix[y-1][x-1] + 1 * image_matrix[y-1][x+1] +
                -2 * image_matrix[y][x-1]   + 2 * image_matrix[y][x+1] +
                -1 * image_matrix[y+1][x-1] + 1 * image_matrix[y+1][x+1]
            )
            gy = (
                -1 * image_matrix[y-1][x-1] - 2 * image_matrix[y-1][x] - 1 * image_matrix[y-1][x+1] +
                 1 * image_matrix[y+1][x-1] + 2 * image_matrix[y+1][x] + 1 * image_matrix[y+1][x+1]
            )
            grad = (gx * gx + gy * gy) ** 0.5
            # Draw dark lines (string art style) on strong edges
            if grad > 80:
                edges[y][x] = 0
                
    return edges

# 4. Sample Low-Contrast Image (clustered in dark-mid gray levels [40-80])
# 8x8 low-contrast sample
low_contrast_image = [
    [52, 55, 60, 62, 59, 56, 53, 50],
    [54, 58, 65, 70, 68, 62, 57, 52],
    [58, 65, 75, 80, 78, 72, 63, 55],
    [60, 68, 78, 85, 82, 75, 67, 58],
    [59, 66, 76, 82, 80, 74, 65, 57],
    [56, 62, 71, 78, 75, 69, 61, 54],
    [53, 57, 64, 69, 67, 63, 56, 51],
    [50, 53, 58, 62, 60, 57, 52, 48]
]

# Run histogram equalization
equalized_img, hist_orig, hist_eq, map_table = equalize_histogram(low_contrast_image)

# Edge detection
edges_orig = detect_edges(low_contrast_image)
edges_eq = detect_edges(equalized_img)

# 5. Display Results
print("=" * 65)
print(" QUESTION 13: HISTOGRAM EQUALIZATION & EDGE STRING ART")
print("=" * 65)

print("\n--- Original Low-Contrast Image (8x8) ---")
for row in low_contrast_image:
    print("  ", [f"{p:3d}" for p in row])

print("\n--- Equalized High-Contrast Image (8x8) ---")
for row in equalized_img:
    print("  ", [f"{p:3d}" for p in row])

# 6. Display Non-Zero Histogram Bins (Before vs After)
print("\n--- Histogram Comparison (Non-Zero Intensity Bins) ---")
print(f"{'Intensity':<12} {'Original Count':<18} {'Equalized Mapping -> Intensity':<32}")
print("-" * 65)
for k in range(256):
    if hist_orig[k] > 0:
        print(f"{k:<12} {hist_orig[k]:<18} {k} -> {map_table[k]}")

# 7. ASCII Visualization of Equalization
print("\n--- ASCII Visual: Original Low Contrast ---")
for row in low_contrast_image:
    print("  " + " ".join("." if p < 60 else "-" if p < 75 else "#" for p in row))

print("\n--- ASCII Visual: Equalized High Contrast ---")
for row in equalized_img:
    print("  " + " ".join("." if p < 80 else "-" if p < 180 else "#" for p in row))

print("\n--- ASCII Visual: String Art Edges on Equalized Image ('#' = line) ---")
for row in edges_eq:
    print("  " + " ".join("#" if p == 0 else "." for p in row))

# Save output PGM files
try:
    with open("hist_original.pgm", "w") as f:
        f.write(f"P2\n8 8\n255\n")
        for row in low_contrast_image:
            f.write(" ".join(str(val) for val in row) + "\n")
    with open("hist_equalized.pgm", "w") as f:
        f.write(f"P2\n8 8\n255\n")
        for row in equalized_img:
            f.write(" ".join(str(val) for val in row) + "\n")
    print("\nSaved image files: 'hist_original.pgm' and 'hist_equalized.pgm'")
except Exception:
    pass

print("=" * 65)

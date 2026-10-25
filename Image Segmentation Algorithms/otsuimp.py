# -------------------------------------------------------------
# Otsu's Thresholding Segmentation
# Pure Python Implementation (NO IMPORT MODULES USED)
# -------------------------------------------------------------

# Otsu's Algorithm:
# Maximizes between-class variance sigma_B^2(t):
# sigma_B^2(t) = w0(t) * w1(t) * (mu0(t) - mu1(t))^2
# where:
#   w0(t) = probability of background class (pixels <= t)
#   w1(t) = probability of foreground class (pixels > t)
#   mu0(t) = mean intensity of background
#   mu1(t) = mean intensity of foreground

def otsu_threshold(image):
    H = len(image)
    W = len(image[0])
    total_pixels = H * W
    
    # 1. Compute Histogram
    hist = [0] * 256
    for row in image:
        for val in row:
            hist[val] += 1
            
    # 2. Total mean
    sum_total = sum(i * hist[i] for i in range(256))
    
    w0 = 0
    sum_background = 0
    max_variance = -1.0
    optimal_thresh = 0
    
    for t in range(256):
        w0 += hist[t]
        if w0 == 0:
            continue
        w1 = total_pixels - w0
        if w1 == 0:
            break
            
        sum_background += t * hist[t]
        
        mu0 = sum_background / w0
        mu1 = (sum_total - sum_background) / w1
        
        # Between-class variance
        variance_between = float(w0) * float(w1) * ((mu0 - mu1) ** 2)
        
        if variance_between > max_variance:
            max_variance = variance_between
            optimal_thresh = t
            
    # 3. Apply Threshold
    segmented = [[255 if image[r][c] >= optimal_thresh else 0 for c in range(W)] for r in range(H)]
    return optimal_thresh, segmented

# Sample Bimodal 8x8 Image (Dark mode around ~30, bright mode around ~180)
sample_image = [
    [ 28,  32,  25,  30,  35,  22,  29,  31],
    [ 30,  26, 175, 185, 180, 190,  34,  28],
    [ 25, 180, 195, 205, 200, 185, 178,  30],
    [ 32, 170, 200, 210, 215, 195, 182,  27],
    [ 29, 185, 190, 205, 200, 190, 175,  33],
    [ 24,  31, 180, 185, 190, 180,  28,  26],
    [ 33,  28,  25,  32,  30,  27,  31,  29],
    [ 27,  30,  34,  28,  26,  33,  25,  32]
]

best_t, otsu_seg = otsu_threshold(sample_image)

print("=" * 65)
print(" OTSU'S THRESHOLDING SEGMENTATION (Pure Python - Zero Imports)")
print("=" * 65)

print("\n--- Original Grayscale Image (8x8) ---")
for row in sample_image:
    print("  ", [f"{p:3d}" for p in row])

print(f"\nCalculated Optimal Otsu Threshold: T* = {best_t}")

print("\n--- Segmented Binary Image (Otsu Thresholded) ---")
for row in otsu_seg:
    print("  ", [f"{p:3d}" for p in row])

print("\n--- ASCII Visual of Segmented Object ('#' = Foreground, '.' = Background) ---")
for row in otsu_seg:
    print("  " + " ".join("#" if p == 255 else "." for p in row))
print("=" * 65)

# -------------------------------------------------------------
# Global Thresholding Segmentation
# Pure Python Implementation (NO IMPORT MODULES USED)
# -------------------------------------------------------------

# Formula:
# g(x, y) = 255 if f(x, y) >= T else 0
# Basic Global Threshold Algorithm:
# 1. Select an initial estimate for threshold T (e.g. mean image intensity or 127).
# 2. Segment image using T into G1 (pixels >= T) and G2 (pixels < T).
# 3. Compute mean intensities m1 of G1 and m2 of G2.
# 4. Compute new threshold: T_new = 0.5 * (m1 + m2).
# 5. Repeat until |T - T_new| < delta (convergence).

def global_threshold(image, T=127):
    H = len(image)
    W = len(image[0])
    segmented = [[255 if image[r][c] >= T else 0 for c in range(W)] for r in range(H)]
    return segmented

def iterative_optimal_threshold(image, delta=0.5):
    H = len(image)
    W = len(image[0])
    
    # Initial estimate: average intensity
    total_sum = sum(sum(row) for row in image)
    T = total_sum / (H * W)
    
    while True:
        g1 = []
        g2 = []
        for r in range(H):
            for c in range(W):
                val = image[r][c]
                if val >= T:
                    g1.append(val)
                else:
                    g2.append(val)
                    
        m1 = sum(g1) / len(g1) if g1 else 0
        m2 = sum(g2) / len(g2) if g2 else 0
        
        T_new = 0.5 * (m1 + m2)
        if abs(T - T_new) < delta:
            break
        T = T_new
        
    return T, global_threshold(image, T)

# Sample 8x8 image with distinct dark background (20-40) and bright object (180-220)
sample_image = [
    [ 25,  30,  35,  20,  25,  30,  20,  25],
    [ 20, 200, 210, 190, 205, 195,  35,  30],
    [ 30, 195, 220, 215, 225, 200,  40,  25],
    [ 25, 205, 215, 220, 210, 190,  30,  20],
    [ 35, 190, 200, 205, 195, 185,  25,  35],
    [ 20,  40,  30,  25,  35,  20,  30,  40],
    [ 30,  25,  20,  35,  30,  25,  20,  30],
    [ 25,  30,  35,  20,  25,  30,  35,  25]
]

T_opt, segmented_opt = iterative_optimal_threshold(sample_image)
segmented_127 = global_threshold(sample_image, T=127)

print("=" * 65)
print(" GLOBAL THRESHOLDING SEGMENTATION (Pure Python - Zero Imports)")
print("=" * 65)

print("\n--- Original Grayscale Image (8x8) ---")
for row in sample_image:
    print("  ", [f"{p:3d}" for p in row])

print(f"\nFixed Global Threshold T = 127:")
for row in segmented_127:
    print("  ", [f"{p:3d}" for p in row])

print(f"\nIterative Optimal Threshold T* = {T_opt:.2f}:")
for row in segmented_opt:
    print("  ", [f"{p:3d}" for p in row])

print("\n--- ASCII Visual of Segmented Object ('#' = Object, '.' = Background) ---")
for row in segmented_opt:
    print("  " + " ".join("#" if p == 255 else "." for p in row))
print("=" * 65)

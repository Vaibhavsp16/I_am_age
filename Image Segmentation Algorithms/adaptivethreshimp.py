# -------------------------------------------------------------
# Adaptive (Local) Thresholding Segmentation
# Pure Python Implementation (NO IMPORT MODULES USED)
# -------------------------------------------------------------

# Adaptive Thresholding Algorithm:
# Computes a separate threshold T(x, y) for every pixel based on its local neighborhood:
# T(x, y) = Local_Mean(x, y) - C
# g(x, y) = 255 if f(x, y) > T(x, y) else 0
# Effective for images with non-uniform illumination or shadows.

def adaptive_threshold(image, block_size=5, C=2):
    H = len(image)
    W = len(image[0])
    pad = block_size // 2
    
    output = [[0 for _ in range(W)] for _ in range(H)]
    
    for y in range(H):
        for x in range(W):
            # Compute local neighborhood mean
            total = 0.0
            count = 0
            for dy in range(-pad, pad + 1):
                for dx in range(-pad, pad + 1):
                    ny = y + dy
                    nx = x + dx
                    if 0 <= ny < H and 0 <= nx < W:
                        total += image[ny][nx]
                        count += 1
                        
            local_mean = total / count
            local_threshold = local_mean - C
            
            output[y][x] = 255 if image[y][x] > local_threshold else 0
            
    return output

# Sample Image with non-uniform background illumination (intensity gradient from left to right)
# but containing distinct foreground dark and bright patches
sample_image = [
    [ 40,  55,  70,  85, 100, 115, 130, 145],
    [ 45, 120, 130,  90, 105, 180, 190, 150],
    [ 50, 125, 135,  95, 110, 185, 195, 155],
    [ 55,  65,  80,  95, 115, 125, 140, 160],
    [ 60,  70,  85, 100, 120, 130, 145, 165],
    [ 65,  75,  90, 105, 125, 135, 150, 170],
    [ 70,  80,  95, 110, 130, 140, 155, 175],
    [ 75,  85, 100, 115, 135, 145, 160, 180]
]

adaptive_seg = adaptive_threshold(sample_image, block_size=3, C=10)

print("=" * 65)
print(" ADAPTIVE THRESHOLDING SEGMENTATION (Pure Python - Zero Imports)")
print("=" * 65)

print("\n--- Original Image with Uneven Illumination Gradient (8x8) ---")
for row in sample_image:
    print("  ", [f"{p:3d}" for p in row])

print("\n--- Adaptive Threshold Output (Block Size = 3, C = 10) ---")
for row in adaptive_seg:
    print("  ", [f"{p:3d}" for p in row])

print("\n--- ASCII Visual of Segmented Local Features ('#' = Foreground, '.' = Background) ---")
for row in adaptive_seg:
    print("  " + " ".join("#" if p == 255 else "." for p in row))
print("=" * 65)

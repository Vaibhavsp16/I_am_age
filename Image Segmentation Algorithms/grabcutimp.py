# -------------------------------------------------------------
# GrabCut Interactive Foreground/Background Segmentation
# Pure Python Implementation (NO IMPORT MODULES USED)
# -------------------------------------------------------------

# GrabCut Algorithm Concept:
# 1. User/System specifies a bounding box containing the object of interest:
#    (r_min, c_min, r_max, c_max).
# 2. Definite Background: all pixels strictly outside the bounding box.
# 3. Probable Foreground: all pixels initially inside the bounding box.
# 4. Statistical Modeling:
#    Compute mean and variance for the background and foreground pixel sets.
# 5. Energy Minimization / Likelihood Assignment:
#    For each pixel inside the box, evaluate Gaussian likelihood P(pixel | FG) vs P(pixel | BG).
#    Assign pixel to the class with higher likelihood.
# 6. Output foreground segmentation mask.

def grabcut_segmentation(image, rect, iterations=3):
    H = len(image)
    W = len(image[0])
    r1, c1, r2, c2 = rect
    
    # Mask labels:
    # 0 = Definite Background
    # 1 = Definite/Probable Foreground
    mask = [[0 for _ in range(W)] for _ in range(H)]
    for r in range(r1, r2 + 1):
        for c in range(c1, c2 + 1):
            if 0 <= r < H and 0 <= c < W:
                mask[r][c] = 1
                
    for it in range(iterations):
        bg_pixels = []
        fg_pixels = []
        
        for r in range(H):
            for c in range(W):
                if mask[r][c] == 0:
                    bg_pixels.append(image[r][c])
                else:
                    fg_pixels.append(image[r][c])
                    
        if not bg_pixels or not fg_pixels:
            break
            
        mean_bg = sum(bg_pixels) / len(bg_pixels)
        var_bg = sum((p - mean_bg) ** 2 for p in bg_pixels) / len(bg_pixels) + 1e-4
        
        mean_fg = sum(fg_pixels) / len(fg_pixels)
        var_fg = sum((p - mean_fg) ** 2 for p in fg_pixels) / len(fg_pixels) + 1e-4
        
        # Re-classify pixels inside the bounding box
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                if 0 <= r < H and 0 <= c < W:
                    val = image[r][c]
                    # Log-likelihood / Mahalanobis distance
                    dist_bg = ((val - mean_bg) ** 2) / var_bg
                    dist_fg = ((val - mean_fg) ** 2) / var_fg
                    
                    if dist_fg <= dist_bg:
                        mask[r][c] = 1
                    else:
                        mask[r][c] = 0
                        
    # Segmented masked image: image * mask
    result = [[image[r][c] if mask[r][c] == 1 else 0 for c in range(W)] for r in range(H)]
    return mask, result

# Sample 10x10 Image with a bright object inside a bounding box, with some background noise inside the box
sample_image = [
    [ 25,  30,  28,  32,  27,  33,  29,  31,  26,  30],
    [ 28,  32,  29,  31,  26,  30,  28,  32,  27,  33],
    [ 30,  27,  28, 195, 205, 200, 190,  30,  32,  28],
    [ 26,  31,  30, 200, 215, 210, 195,  32,  29,  31],
    [ 32,  28,  29, 205, 220, 215, 200,  31,  28,  30],
    [ 27,  33,  31, 190, 210, 205, 195,  29,  30,  27],
    [ 29,  30,  28,  27, 200, 195,  30,  32,  26,  32],
    [ 31,  26,  32,  29,  31,  28,  30,  27,  33,  29],
    [ 28,  32,  27,  33,  29,  31,  26,  30,  28,  31],
    [ 30,  28,  31,  26,  30,  27,  32,  29,  31,  28]
]

# Bounding box containing the foreground object: rows 2 to 6, cols 2 to 7
rect = (2, 2, 6, 7)
fg_mask, segmented_fg = grabcut_segmentation(sample_image, rect)

print("=" * 65)
print(" GRABCUT FOREGROUND / BACKGROUND SEGMENTATION")
print(" Pure Python Implementation (NO IMPORT MODULES USED)")
print("=" * 65)

print("\n--- Original Input Image (10x10) ---")
for row in sample_image:
    print("  ", [f"{p:3d}" for p in row])

print(f"\nUser-specified Bounding Box Rect: (r1={rect[0]}, c1={rect[1]}, r2={rect[2]}, c2={rect[3]})")

print("\n--- GrabCut Binary Segmentation Mask (1 = Foreground, 0 = Background) ---")
for row in fg_mask:
    print("  ", row)

print("\n--- Segmented Foreground Image (Background Zeroed Out) ---")
for row in segmented_fg:
    print("  ", [f"{p:3d}" for p in row])

print("\n--- ASCII Visual of Segmented Object ('#' = Extracted Foreground, '.' = Background) ---")
for row in fg_mask:
    print("  " + " ".join("#" if p == 1 else "." for p in row))
print("=" * 65)

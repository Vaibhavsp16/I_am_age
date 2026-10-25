# -------------------------------------------------------------
# Mean Shift Image Segmentation
# Pure Python Implementation (NO IMPORT MODULES USED)
# -------------------------------------------------------------

# Mean Shift Algorithm:
# Non-parametric clustering technique that locates the maxima (modes) of a density function:
# 1. For each pixel (r, c) with intensity I:
#    Consider all neighbor pixels within spatial bandwidth hs and range/color bandwidth hr.
# 2. Compute the new center of mass (spatial mean, intensity mean).
# 3. Shift the current point to this mean.
# 4. Repeat until convergence (shift < epsilon).
# 5. Group points whose converged modes are close together into identical segments.

def mean_shift_segmentation(image, hs=2, hr=30, max_iter=10, eps=0.5):
    H = len(image)
    W = len(image[0])
    
    # Store the segmented intensity for each pixel
    filtered = [[0 for _ in range(W)] for _ in range(H)]
    
    for r in range(H):
        for c in range(W):
            curr_r = float(r)
            curr_c = float(c)
            curr_i = float(image[r][c])
            
            for it in range(max_iter):
                sum_r = 0.0
                sum_c = 0.0
                sum_i = 0.0
                total_weight = 0.0
                
                # Check neighborhood within spatial window [-hs, hs]
                min_r = max(0, int(curr_r - hs))
                max_r = min(H, int(curr_r + hs + 1))
                min_c = max(0, int(curr_c - hs))
                max_c = min(W, int(curr_c + hs + 1))
                
                for nr in range(min_r, max_r):
                    for nc in range(min_c, max_c):
                        d_spatial_sq = (nr - curr_r) ** 2 + (nc - curr_c) ** 2
                        if d_spatial_sq <= hs * hs:
                            pix_val = float(image[nr][nc])
                            d_range = abs(pix_val - curr_i)
                            if d_range <= hr:
                                # Uniform or flat kernel weight
                                weight = 1.0
                                sum_r += nr * weight
                                sum_c += nc * weight
                                sum_i += pix_val * weight
                                total_weight += weight
                                
                if total_weight == 0:
                    break
                    
                new_r = sum_r / total_weight
                new_c = sum_c / total_weight
                new_i = sum_i / total_weight
                
                shift = ((new_r - curr_r)**2 + (new_c - curr_c)**2 + (new_i - curr_i)**2) ** 0.5
                curr_r, curr_c, curr_i = new_r, new_c, new_i
                
                if shift < eps:
                    break
                    
            filtered[r][c] = int(round(curr_i))
            
    return filtered

# Sample Image with noise added to two distinct regions
sample_image = [
    [ 30,  35,  28,  32, 190, 195, 205, 200],
    [ 28,  32,  30,  34, 195, 200, 198, 202],
    [ 34,  29,  31,  33, 200, 205, 202, 198],
    [ 32,  30,  28,  35, 192, 198, 200, 204],
    [ 30,  34,  32,  30,  28,  32,  30,  35],
    [ 28,  30,  34,  28,  30,  34,  28,  32],
    [ 32,  28,  30,  32,  34,  30,  32,  30],
    [ 30,  32,  28,  30,  32,  28,  30,  32]
]

segmented_img = mean_shift_segmentation(sample_image, hs=2, hr=40)

print("=" * 65)
print(" MEAN SHIFT IMAGE SEGMENTATION")
print(" Pure Python Implementation (NO IMPORT MODULES USED)")
print("=" * 65)

print("\n--- Original Noisy Input Image (8x8) ---")
for row in sample_image:
    print("  ", [f"{p:3d}" for p in row])

print("\n--- Mean Shift Segmented (Smooth Mode Clustered) Image ---")
for row in segmented_img:
    print("  ", [f"{p:3d}" for p in row])

print("\n--- ASCII Visual of Mean Shift Segments ('#' = High Mode, '.' = Low Mode) ---")
for row in segmented_img:
    print("  " + " ".join("#" if p > 100 else "." for p in row))
print("=" * 65)

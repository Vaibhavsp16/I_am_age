# -------------------------------------------------------------
# Region Growing Segmentation
# Pure Python Implementation (NO IMPORT MODULES USED)
# -------------------------------------------------------------

# Region Growing Algorithm:
# 1. Start from a chosen seed point (r0, c0) with initial intensity I_seed.
# 2. Maintain a queue of frontier pixels and a visited/segmented mask.
# 3. For each pixel in the queue, inspect its 4-neighbors (or 8-neighbors).
# 4. If neighbor is unvisited and |I(neighbor) - I_seed| <= tolerance:
#       Mark neighbor as part of segmented region (255)
#       Add neighbor to queue
# 5. Repeat until no more matching pixels can be appended.

def region_growing(image, seed, tolerance=25):
    H = len(image)
    W = len(image[0])
    
    seed_r, seed_c = seed
    seed_val = image[seed_r][seed_c]
    
    segmented = [[0 for _ in range(W)] for _ in range(H)]
    visited = [[False for _ in range(W)] for _ in range(H)]
    
    # Breadth-first search queue using pure Python list
    queue = [(seed_r, seed_c)]
    visited[seed_r][seed_c] = True
    segmented[seed_r][seed_c] = 255
    
    # 4-connectivity neighbor offsets: Up, Down, Left, Right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    head = 0
    while head < len(queue):
        curr_r, curr_c = queue[head]
        head += 1
        
        for dr, dc in directions:
            nr = curr_r + dr
            nc = curr_c + dc
            
            if 0 <= nr < H and 0 <= nc < W:
                if not visited[nr][nc]:
                    visited[nr][nc] = True
                    # Similarity criterion: difference from seed intensity <= tolerance
                    if abs(image[nr][nc] - seed_val) <= tolerance:
                        segmented[nr][nc] = 255
                        queue.append((nr, nc))
                        
    return segmented, len(queue)

# Sample 8x8 image containing an object with similar intensities (190-210) surrounded by background (20-40)
sample_image = [
    [ 25,  30,  35,  20,  25,  30,  20,  25],
    [ 20, 200, 205, 195, 205, 195,  35,  30],
    [ 30, 195, 200, 205, 200, 200,  40,  25],
    [ 25, 205, 200, 200, 205, 190,  30,  20],
    [ 35, 190, 200, 205, 195,  25,  25,  35],
    [ 20,  40,  30,  25,  35,  20,  30,  40],
    [ 30,  25,  20,  35,  30,  25,  20,  30],
    [ 25,  30,  35,  20,  25,  30,  35,  25]
]

seed_point = (2, 2)  # Inside the object (pixel value = 200)
segmented_region, region_size = region_growing(sample_image, seed=seed_point, tolerance=20)

print("=" * 65)
print(" REGION GROWING SEGMENTATION (Pure Python - Zero Imports)")
print("=" * 65)

print("\n--- Original Grayscale Image (8x8) ---")
for row in sample_image:
    print("  ", [f"{p:3d}" for p in row])

print(f"\nSeed Point Location: {seed_point} (Intensity = {sample_image[seed_point[0]][seed_point[1]]})")
print(f"Tolerance Value    : +/- 20")
print(f"Total Region Pixels: {region_size}")

print("\n--- Segmented Region Mask (255 = Grown Region, 0 = Background) ---")
for row in segmented_region:
    print("  ", [f"{p:3d}" for p in row])

print("\n--- ASCII Visual of Grown Region ('#' = Object, '.' = Background) ---")
for row in segmented_region:
    print("  " + " ".join("#" if p == 255 else "." for p in row))
print("=" * 65)

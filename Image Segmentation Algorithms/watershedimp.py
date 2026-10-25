# -------------------------------------------------------------
# Watershed Image Segmentation
# Pure Python Implementation (NO IMPORT MODULES USED)
# -------------------------------------------------------------

# Watershed Segmentation Algorithm:
# 1. Binarize the image (foreground objects vs background).
# 2. Distance Transform: compute distance of each foreground pixel to the nearest background pixel.
# 3. Local Maxima Detection: pixels with peak distances become distinct object seeds (markers: 1, 2, ...).
# 4. Flooding / Label Propagation: Priority queue / multi-level dilation floods markers uphill.
# 5. Watershed Ridge Lines: When two different marker labels meet, a watershed boundary line (dam) is formed.

def distance_transform(binary_mask):
    H = len(binary_mask)
    W = len(binary_mask[0])
    inf = 999999
    
    # Initialize distances
    dist = [[0.0 if binary_mask[r][c] == 0 else inf for c in range(W)] for r in range(H)]
    
    # Forward pass (Top-Left to Bottom-Right)
    for r in range(H):
        for c in range(W):
            if binary_mask[r][c] != 0:
                min_d = dist[r][c]
                if r > 0:
                    min_d = min(min_d, dist[r - 1][c] + 1.0)
                if c > 0:
                    min_d = min(min_d, dist[r][c - 1] + 1.0)
                if r > 0 and c > 0:
                    min_d = min(min_d, dist[r - 1][c - 1] + 1.414)
                dist[r][c] = min_d
                
    # Backward pass (Bottom-Right to Top-Left)
    for r in range(H - 1, -1, -1):
        for c in range(W - 1, -1, -1):
            if binary_mask[r][c] != 0:
                min_d = dist[r][c]
                if r < H - 1:
                    min_d = min(min_d, dist[r + 1][c] + 1.0)
                if c < W - 1:
                    min_d = min(min_d, dist[r][c + 1] + 1.0)
                if r < H - 1 and c < W - 1:
                    min_d = min(min_d, dist[r + 1][c + 1] + 1.414)
                dist[r][c] = min_d
                
    return dist

def watershed_segmentation(binary_mask, markers):
    H = len(binary_mask)
    W = len(binary_mask[0])
    
    labels = [[markers[r][c] for c in range(W)] for r in range(H)]
    
    # Queue for BFS propagation: (r, c)
    queue = []
    for r in range(H):
        for c in range(W):
            if labels[r][c] > 0:
                queue.append((r, c))
                
    head = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while head < len(queue):
        r, c = queue[head]
        head += 1
        curr_label = labels[r][c]
        if curr_label == -1:  # boundary line
            continue
            
        for dr, dc in directions:
            nr = r + dr
            nc = c + dc
            if 0 <= nr < H and 0 <= nc < W and binary_mask[nr][nc] == 255:
                if labels[nr][nc] == 0:
                    labels[nr][nc] = curr_label
                    queue.append((nr, nc))
                elif labels[nr][nc] > 0 and labels[nr][nc] != curr_label:
                    # Conflict: two different expanding basins meet! Form watershed boundary line
                    labels[nr][nc] = -1  # Boundary dam
                    
    return labels

# Sample 10x12 binary image with two touching circular objects
mask = [
    [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
    [  0,   0, 255, 255, 255,   0,   0, 255, 255, 255,   0,   0],
    [  0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,   0],
    [  0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,   0],
    [  0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,   0],
    [  0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,   0],
    [  0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,   0],
    [  0,   0, 255, 255, 255,   0,   0, 255, 255, 255,   0,   0],
    [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
    [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0]
]

H = len(mask)
W = len(mask[0])

# 1. Compute Distance Transform
dist_map = distance_transform(mask)

# 2. Markers for the two distinct object centers (basins)
markers = [[0 for _ in range(W)] for _ in range(H)]
markers[4][3] = 1   # Center of Object 1
markers[4][8] = 2   # Center of Object 2

# 3. Run Watershed
segmented_labels = watershed_segmentation(mask, markers)

print("=" * 65)
print(" WATERSHED IMAGE SEGMENTATION")
print(" Pure Python Implementation (NO IMPORT MODULES USED)")
print("=" * 65)

print("\n--- 1. Input Binary Mask (Two Touching Objects) ---")
for row in mask:
    print("  " + " ".join("#" if p == 255 else "." for p in row))

print("\n--- 2. Distance Transform Map (Distance to Background) ---")
for row in dist_map:
    print("  ", [f"{d:3.1f}" for d in row])

print("\n--- 3. Watershed Segmented Labels ---")
print("  (1 = Object 1, 2 = Object 2, -1 = Watershed Boundary Dam, 0 = Background)")
for row in segmented_labels:
    print("  ", [f"{p:2d}" for p in row])

print("\n--- ASCII Visual of Watershed Separation ---")
for row in segmented_labels:
    line = []
    for p in row:
        if p == 1:
            line.append("A")
        elif p == 2:
            line.append("B")
        elif p == -1:
            line.append("|")  # Dividing boundary dam
        else:
            line.append(".")
    print("  " + " ".join(line))
print("=" * 65)

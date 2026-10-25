# -------------------------------------------------------------
# K-Means Clustering Image Segmentation
# Pure Python Implementation (NO IMPORT MODULES USED)
# -------------------------------------------------------------

# K-Means Segmentation Algorithm:
# 1. Choose K cluster centroids (e.g. K = 3 or 4).
# 2. Assign each pixel to the closest centroid: argmin_k |pixel - centroid_k|.
# 3. Recalculate each centroid as the arithmetic mean of all pixels assigned to it.
# 4. Repeat until centroids converge (change is below tolerance) or max iterations reached.
# 5. Form the segmented image by replacing each pixel with its cluster center value.

def kmeans_segmentation(image, K=3, max_iter=20, tolerance=0.5):
    H = len(image)
    W = len(image[0])
    
    # Flatten all pixels
    pixels = [image[r][c] for r in range(H) for c in range(W)]
    
    # Initialize K centroids evenly spaced across data range
    min_val = min(pixels)
    max_val = max(pixels)
    step = (max_val - min_val) / (K + 1)
    centroids = [min_val + (k + 1) * step for k in range(K)]
    
    for iteration in range(max_iter):
        # Create K empty clusters
        clusters = [[] for _ in range(K)]
        
        # Assignment Step
        for p in pixels:
            # Find nearest centroid
            best_k = 0
            best_dist = abs(p - centroids[0])
            for k in range(1, K):
                dist = abs(p - centroids[k])
                if dist < best_dist:
                    best_dist = dist
                    best_k = k
            clusters[best_k].append(p)
            
        # Update Step
        new_centroids = []
        max_shift = 0.0
        for k in range(K):
            if clusters[k]:
                new_c = sum(clusters[k]) / len(clusters[k])
            else:
                new_c = centroids[k]
            shift = abs(new_c - centroids[k])
            if shift > max_shift:
                max_shift = shift
            new_centroids.append(new_c)
            
        centroids = new_centroids
        if max_shift < tolerance:
            break
            
    # Assign each pixel in the 2D image to its nearest cluster center
    segmented = [[0 for _ in range(W)] for _ in range(H)]
    labels = [[0 for _ in range(W)] for _ in range(H)]
    
    for r in range(H):
        for c in range(W):
            p = image[r][c]
            best_k = 0
            best_dist = abs(p - centroids[0])
            for k in range(1, K):
                dist = abs(p - centroids[k])
                if dist < best_dist:
                    best_dist = dist
                    best_k = k
            labels[r][c] = best_k
            segmented[r][c] = int(round(centroids[best_k]))
            
    return centroids, labels, segmented

# Sample Image with 3 distinct intensity layers (Dark background ~30, Midtones ~120, Highlights ~220)
sample_image = [
    [ 25,  30,  35,  25,  30,  35,  25,  30],
    [ 25, 120, 125, 115, 125, 120,  30,  25],
    [ 30, 125, 215, 220, 225, 125,  35,  30],
    [ 35, 120, 220, 230, 220, 120,  30,  35],
    [ 30, 115, 210, 225, 215, 115,  35,  30],
    [ 25, 120, 125, 120, 125, 120,  30,  25],
    [ 30,  25,  35,  30,  25,  35,  30,  25],
    [ 25,  30,  25,  35,  30,  25,  35,  30]
]

K = 3
final_centers, labels, segmented = kmeans_segmentation(sample_image, K=K)

print("=" * 65)
print(f" K-MEANS CLUSTERING IMAGE SEGMENTATION (K = {K})")
print(" Pure Python Implementation (NO IMPORT MODULES USED)")
print("=" * 65)

print("\n--- Original Image (8x8) ---")
for row in sample_image:
    print("  ", [f"{p:3d}" for p in row])

print("\nConverged Cluster Centroids:")
for k, c in enumerate(final_centers):
    print(f"  Cluster {k}: Center = {c:.2f} (approx {int(round(c))})")

print("\n--- Cluster Labels (0 to K-1) ---")
for row in labels:
    print("  ", row)

print("\n--- Segmented Quantized Image ---")
for row in segmented:
    print("  ", [f"{p:3d}" for p in row])

print("\n--- ASCII Visual of Clusters (' ' = Dark, '-' = Mid, '#' = Bright) ---")
symbols = [" ", "-", "#"]
for row in labels:
    print("  " + " ".join(symbols[label % len(symbols)] for label in row))
print("=" * 65)

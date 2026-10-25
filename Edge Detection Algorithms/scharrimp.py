# -------------------------------------------------------------
# Scharr Edge Detection
# Pure Python Implementation (NO IMPORT MODULES USED)
# -------------------------------------------------------------

# Scharr Kernels (3x3 - Optimized for rotational symmetry):
# Gx detects vertical edges:
#   [[ -3,  0,  3],
#    [-10,  0, 10],
#    [ -3,  0,  3]]
#
# Gy detects horizontal edges:
#   [[ -3, -10, -3],
#    [  0,   0,  0],
#    [  3,  10,  3]]

def convolve2d(image, kernel):
    H = len(image)
    W = len(image[0])
    kH = len(kernel)
    kW = len(kernel[0])
    pad_y = kH // 2
    pad_x = kW // 2
    
    out = [[0.0 for _ in range(W)] for _ in range(H)]
    
    for i in range(H):
        for j in range(W):
            total = 0.0
            for ki in range(kH):
                for kj in range(kW):
                    ni = i + ki - pad_y
                    nj = j + kj - pad_x
                    if 0 <= ni < H and 0 <= nj < W:
                        total += image[ni][nj] * kernel[ki][kj]
            out[i][j] = total
    return out

def scharr_edge_detector(image):
    H = len(image)
    W = len(image[0])
    
    Gx = [
        [ -3,  0,  3],
        [-10,  0, 10],
        [ -3,  0,  3]
    ]
    
    Gy = [
        [ -3, -10, -3],
        [  0,   0,  0],
        [  3,  10,  3]
    ]
    
    scharr_x = convolve2d(image, Gx)
    scharr_y = convolve2d(image, Gy)
    
    magnitude = [[0 for _ in range(W)] for _ in range(H)]
    sx_disp = [[0 for _ in range(W)] for _ in range(H)]
    sy_disp = [[0 for _ in range(W)] for _ in range(H)]
    
    for i in range(H):
        for j in range(W):
            gx = scharr_x[i][j]
            gy = scharr_y[i][j]
            mag = (gx * gx + gy * gy) ** 0.5
            magnitude[i][j] = int(min(255, max(0, mag / 4.0)))  # Scaled for display
            sx_disp[i][j] = int(min(255, max(0, abs(gx) / 4.0)))
            sy_disp[i][j] = int(min(255, max(0, abs(gy) / 4.0)))
            
    return sx_disp, sy_disp, magnitude

sample_image = [
    [ 20,  20,  20,  20,  20,  20,  20,  20,  20,  20],
    [ 20,  20,  20,  20,  20,  20,  20,  20,  20,  20],
    [ 20,  20, 220, 220, 220, 220, 220, 220,  20,  20],
    [ 20,  20, 220, 220, 220, 220, 220, 220,  20,  20],
    [ 20,  20, 220, 220, 220, 220, 220, 220,  20,  20],
    [ 20,  20, 220, 220, 220, 220, 220, 220,  20,  20],
    [ 20,  20, 220, 220, 220, 220, 220, 220,  20,  20],
    [ 20,  20, 220, 220, 220, 220, 220, 220,  20,  20],
    [ 20,  20,  20,  20,  20,  20,  20,  20,  20,  20],
    [ 20,  20,  20,  20,  20,  20,  20,  20,  20,  20]
]

sx, sy, mag = scharr_edge_detector(sample_image)

print("=" * 65)
print(" SCHARR EDGE DETECTION (Pure Python - Zero Imports)")
print("=" * 65)

print("\n--- Scharr X (Vertical Edges) ---")
for row in sx:
    print("  ", [f"{p:3d}" for p in row])

print("\n--- Scharr Y (Horizontal Edges) ---")
for row in sy:
    print("  ", [f"{p:3d}" for p in row])

print("\n--- Combined Scharr Magnitude ---")
for row in mag:
    print("  ", [f"{p:3d}" for p in row])

print("\n--- ASCII Visual of Scharr Edges ('#' = Edge, '.' = Background) ---")
for row in mag:
    print("  " + " ".join("#" if p > 80 else "." for p in row))
print("=" * 65)

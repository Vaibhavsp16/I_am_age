# -------------------------------------------------------------
# Prewitt Edge Detection
# Pure Python Implementation (NO IMPORT MODULES USED)
# -------------------------------------------------------------

# Prewitt Kernels (3x3):
# Gx detects vertical edges:
#   [[ 1, 0, -1],
#    [ 1, 0, -1],
#    [ 1, 0, -1]]
#
# Gy detects horizontal edges:
#   [[ 1,  1,  1],
#    [ 0,  0,  0],
#    [-1, -1, -1]]

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

def prewitt_edge_detector(image):
    H = len(image)
    W = len(image[0])
    
    Gx = [
        [ 1, 0, -1],
        [ 1, 0, -1],
        [ 1, 0, -1]
    ]
    
    Gy = [
        [ 1,  1,  1],
        [ 0,  0,  0],
        [-1, -1, -1]
    ]
    
    prewitt_x = convolve2d(image, Gx)
    prewitt_y = convolve2d(image, Gy)
    
    magnitude = [[0 for _ in range(W)] for _ in range(H)]
    px_disp = [[0 for _ in range(W)] for _ in range(H)]
    py_disp = [[0 for _ in range(W)] for _ in range(H)]
    
    for i in range(H):
        for j in range(W):
            gx = prewitt_x[i][j]
            gy = prewitt_y[i][j]
            mag = (gx * gx + gy * gy) ** 0.5
            magnitude[i][j] = int(min(255, max(0, mag)))
            px_disp[i][j] = int(min(255, max(0, abs(gx))))
            py_disp[i][j] = int(min(255, max(0, abs(gy))))
            
    return px_disp, py_disp, magnitude

# Sample 10x10 Image with a bright rectangular region
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

px, py, mag = prewitt_edge_detector(sample_image)

print("=" * 65)
print(" PREWITT EDGE DETECTION (Pure Python - Zero Imports)")
print("=" * 65)

print("\n--- Prewitt X (Vertical Edges) ---")
for row in px:
    print("  ", [f"{p:3d}" for p in row])

print("\n--- Prewitt Y (Horizontal Edges) ---")
for row in py:
    print("  ", [f"{p:3d}" for p in row])

print("\n--- Combined Prewitt Magnitude ---")
for row in mag:
    print("  ", [f"{p:3d}" for p in row])

print("\n--- ASCII Visual of Prewitt Edges ('#' = Edge, '.' = Background) ---")
for row in mag:
    print("  " + " ".join("#" if p > 100 else "." for p in row))
print("=" * 65)

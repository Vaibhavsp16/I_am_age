# -------------------------------------------------------------
# Sobel Edge Detection
# Pure Python Implementation (NO IMPORT MODULES USED)
# -------------------------------------------------------------

# Sobel Kernels (3x3):
# Gx detects vertical edges (horizontal gradient):
#   [[-1, 0, 1],
#    [-2, 0, 2],
#    [-1, 0, 1]]
#
# Gy detects horizontal edges (vertical gradient):
#   [[-1, -2, -1],
#    [ 0,  0,  0],
#    [ 1,  2,  1]]

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

def sobel_edge_detector(image):
    H = len(image)
    W = len(image[0])
    
    Gx = [
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ]
    
    Gy = [
        [-1, -2, -1],
        [ 0,  0,  0],
        [ 1,  2,  1]
    ]
    
    sobel_x = convolve2d(image, Gx)
    sobel_y = convolve2d(image, Gy)
    
    # Gradient magnitude: G = sqrt(Gx^2 + Gy^2)
    magnitude = [[0 for _ in range(W)] for _ in range(H)]
    sobel_x_disp = [[0 for _ in range(W)] for _ in range(H)]
    sobel_y_disp = [[0 for _ in range(W)] for _ in range(H)]
    
    for i in range(H):
        for j in range(W):
            gx = sobel_x[i][j]
            gy = sobel_y[i][j]
            mag = (gx * gx + gy * gy) ** 0.5
            magnitude[i][j] = int(min(255, max(0, mag)))
            sobel_x_disp[i][j] = int(min(255, max(0, abs(gx))))
            sobel_y_disp[i][j] = int(min(255, max(0, abs(gy))))
            
    return sobel_x_disp, sobel_y_disp, magnitude

# Sample 10x10 Image with a bright rectangular box (intensity 200 on background 30)
sample_image = [
    [ 30,  30,  30,  30,  30,  30,  30,  30,  30,  30],
    [ 30,  30,  30,  30,  30,  30,  30,  30,  30,  30],
    [ 30,  30, 200, 200, 200, 200, 200, 200,  30,  30],
    [ 30,  30, 200, 200, 200, 200, 200, 200,  30,  30],
    [ 30,  30, 200, 200, 200, 200, 200, 200,  30,  30],
    [ 30,  30, 200, 200, 200, 200, 200, 200,  30,  30],
    [ 30,  30, 200, 200, 200, 200, 200, 200,  30,  30],
    [ 30,  30, 200, 200, 200, 200, 200, 200,  30,  30],
    [ 30,  30,  30,  30,  30,  30,  30,  30,  30,  30],
    [ 30,  30,  30,  30,  30,  30,  30,  30,  30,  30]
]

sx, sy, mag = sobel_edge_detector(sample_image)

print("=" * 65)
print(" SOBEL EDGE DETECTION (Pure Python - Zero Imports)")
print("=" * 65)

print("\n--- Original Image (10x10) ---")
for row in sample_image:
    print("  ", [f"{p:3d}" for p in row])

print("\n--- Sobel X Edge Magnitudes (Vertical Edges) ---")
for row in sx:
    print("  ", [f"{p:3d}" for p in row])

print("\n--- Sobel Y Edge Magnitudes (Horizontal Edges) ---")
for row in sy:
    print("  ", [f"{p:3d}" for p in row])

print("\n--- Combined Sobel Gradient Magnitude (Total Edges) ---")
for row in mag:
    print("  ", [f"{p:3d}" for p in row])

print("\n--- ASCII Visual of Detected Edges ('#' = Edge, '.' = Background) ---")
for row in mag:
    print("  " + " ".join("#" if p > 100 else "." for p in row))
print("=" * 65)

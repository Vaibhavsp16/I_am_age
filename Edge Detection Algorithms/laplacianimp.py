# -------------------------------------------------------------
# Laplacian Edge Detection
# Pure Python Implementation (NO IMPORT MODULES USED)
# -------------------------------------------------------------

# Laplacian Kernel (3x3 second-order isotropic derivative):
# 4-neighbor Laplacian:
#   [[ 0,  1,  0],
#    [ 1, -4,  1],
#    [ 0,  1,  0]]
#
# 8-neighbor Laplacian:
#   [[-1, -1, -1],
#    [-1,  8, -1],
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

def laplacian_edge_detector(image):
    H = len(image)
    W = len(image[0])
    
    # Standard 4-neighbor Laplacian kernel
    kernel_4 = [
        [ 0,  1,  0],
        [ 1, -4,  1],
        [ 0,  1,  0]
    ]
    
    # 8-neighbor Laplacian kernel
    kernel_8 = [
        [-1, -1, -1],
        [-1,  8, -1],
        [-1, -1, -1]
    ]
    
    raw_lap4 = convolve2d(image, kernel_4)
    raw_lap8 = convolve2d(image, kernel_8)
    
    lap4_disp = [[int(min(255, max(0, abs(raw_lap4[i][j])))) for j in range(W)] for i in range(H)]
    lap8_disp = [[int(min(255, max(0, abs(raw_lap8[i][j])))) for j in range(W)] for i in range(H)]
    
    return lap4_disp, lap8_disp

sample_image = [
    [ 10,  10,  10,  10,  10,  10,  10,  10,  10,  10],
    [ 10,  10,  10,  10,  10,  10,  10,  10,  10,  10],
    [ 10,  10, 210, 210, 210, 210, 210, 210,  10,  10],
    [ 10,  10, 210, 210, 210, 210, 210, 210,  10,  10],
    [ 10,  10, 210, 210, 210, 210, 210, 210,  10,  10],
    [ 10,  10, 210, 210, 210, 210, 210, 210,  10,  10],
    [ 10,  10, 210, 210, 210, 210, 210, 210,  10,  10],
    [ 10,  10, 210, 210, 210, 210, 210, 210,  10,  10],
    [ 10,  10,  10,  10,  10,  10,  10,  10,  10,  10],
    [ 10,  10,  10,  10,  10,  10,  10,  10,  10,  10]
]

lap4, lap8 = laplacian_edge_detector(sample_image)

print("=" * 65)
print(" LAPLACIAN EDGE DETECTION (Pure Python - Zero Imports)")
print("=" * 65)

print("\n--- 4-Neighbor Laplacian Output ---")
for row in lap4:
    print("  ", [f"{p:3d}" for p in row])

print("\n--- 8-Neighbor Laplacian Output ---")
for row in lap8:
    print("  ", [f"{p:3d}" for p in row])

print("\n--- ASCII Visual of Laplacian Edges ('#' = Edge, '.' = Background) ---")
for row in lap8:
    print("  " + " ".join("#" if p > 100 else "." for p in row))
print("=" * 65)

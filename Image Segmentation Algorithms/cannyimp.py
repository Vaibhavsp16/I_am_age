# -------------------------------------------------------------
# Canny Edge-Based Image Segmentation
# Pure Python Implementation (NO IMPORT MODULES USED)
# -------------------------------------------------------------

# Canny Edge-Based Segmentation Pipeline:
# 1. Gaussian Smoothing for noise reduction.
# 2. Gradient Calculation (Sobel Gx, Gy -> Magnitude & Direction).
# 3. Non-Maximum Suppression (thins boundaries to 1 pixel).
# 4. Hysteresis Double Thresholding (identifies continuous region boundaries).
# 5. Output segmented boundary contours separating distinct image regions.

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

gaussian_3x3 = [
    [1.0 / 16.0, 2.0 / 16.0, 1.0 / 16.0],
    [2.0 / 16.0, 4.0 / 16.0, 2.0 / 16.0],
    [1.0 / 16.0, 2.0 / 16.0, 1.0 / 16.0]
]

def pure_atan2_deg(y, x):
    if x == 0:
        return 90.0 if y > 0 else 270.0
    r = abs(y) / (abs(x) + 1e-9)
    if r <= 1.0:
        angle = 45.0 * r
    else:
        angle = 90.0 - (45.0 / r)
    if x < 0:
        angle = 180.0 - angle
    if y < 0:
        angle = 360.0 - angle
    return angle % 180.0

def canny_segmentation(image, low_thresh=40, high_thresh=100):
    H = len(image)
    W = len(image[0])
    
    # 1. Blur
    blurred = convolve2d(image, gaussian_3x3)
    
    # 2. Sobel Gradients
    Gx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    Gy = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
    
    grad_x = convolve2d(blurred, Gx)
    grad_y = convolve2d(blurred, Gy)
    
    mag = [[0.0 for _ in range(W)] for _ in range(H)]
    angle = [[0.0 for _ in range(W)] for _ in range(H)]
    
    for i in range(H):
        for j in range(W):
            gx = grad_x[i][j]
            gy = grad_y[i][j]
            mag[i][j] = (gx * gx + gy * gy) ** 0.5
            angle[i][j] = pure_atan2_deg(gy, gx)
            
    # 3. Non-Maximum Suppression
    nms = [[0.0 for _ in range(W)] for _ in range(H)]
    for i in range(1, H - 1):
        for j in range(1, W - 1):
            theta = angle[i][j]
            q, r = 255.0, 255.0
            
            if (0 <= theta < 22.5) or (157.5 <= theta <= 180):
                q = mag[i][j + 1]
                r = mag[i][j - 1]
            elif 22.5 <= theta < 67.5:
                q = mag[i + 1][j - 1]
                r = mag[i - 1][j + 1]
            elif 67.5 <= theta < 112.5:
                q = mag[i + 1][j]
                r = mag[i - 1][j]
            elif 112.5 <= theta < 157.5:
                q = mag[i - 1][j - 1]
                r = mag[i + 1][j + 1]
                
            if mag[i][j] >= q and mag[i][j] >= r:
                nms[i][j] = mag[i][j]
            else:
                nms[i][j] = 0.0

    # 4. Double Thresholding & Hysteresis
    res = [[0 for _ in range(W)] for _ in range(H)]
    strong_val = 255
    weak_val = 50
    
    for i in range(H):
        for j in range(W):
            v = nms[i][j]
            if v >= high_thresh:
                res[i][j] = strong_val
            elif v >= low_thresh:
                res[i][j] = weak_val
            else:
                res[i][j] = 0
                
    for i in range(1, H - 1):
        for j in range(1, W - 1):
            if res[i][j] == weak_val:
                has_strong = any(
                    res[i + di][j + dj] == strong_val
                    for di in (-1, 0, 1) for dj in (-1, 0, 1)
                )
                res[i][j] = strong_val if has_strong else 0
                
    return res

sample_image = [
    [ 20,  20,  20,  20,  20,  20,  20,  20,  20,  20],
    [ 20,  20,  20,  20,  20,  20,  20,  20,  20,  20],
    [ 20,  20, 210, 210, 210, 210, 210, 210,  20,  20],
    [ 20,  20, 210, 210, 210, 210, 210, 210,  20,  20],
    [ 20,  20, 210, 210, 210, 210, 210, 210,  20,  20],
    [ 20,  20, 210, 210, 210, 210, 210, 210,  20,  20],
    [ 20,  20, 210, 210, 210, 210, 210, 210,  20,  20],
    [ 20,  20, 210, 210, 210, 210, 210, 210,  20,  20],
    [ 20,  20,  20,  20,  20,  20,  20,  20,  20,  20],
    [ 20,  20,  20,  20,  20,  20,  20,  20,  20,  20]
]

canny_boundaries = canny_segmentation(sample_image, low_thresh=40, high_thresh=100)

print("=" * 65)
print(" CANNY EDGE-BASED SEGMENTATION (Pure Python - Zero Imports)")
print("=" * 65)

print("\n--- Segmented Boundary Contours (1-Pixel Width) ---")
for row in canny_boundaries:
    print("  ", [f"{p:3d}" for p in row])

print("\n--- ASCII Visual of Boundary Segmentation ('#' = Boundary, '.' = Interior) ---")
for row in canny_boundaries:
    print("  " + " ".join("#" if p == 255 else "." for p in row))
print("=" * 65)

# -------------------------------------------------------------
# Canny Edge Detection
# Pure Python Implementation (NO IMPORT MODULES USED)
# -------------------------------------------------------------

# Canny Edge Detector 5-Step Pipeline:
# 1. Gaussian Blur (noise reduction)
# 2. Gradient Calculation (Sobel Gx, Gy -> Magnitude & Direction)
# 3. Non-Maximum Suppression (thins edges along gradient normal)
# 4. Double Thresholding (identifies strong, weak, and non-edges)
# 5. Edge Tracking by Hysteresis (preserves weak edges connected to strong)

PI = 3.141592653589793

# 1. 2D Convolution Helper
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

# 2. Pure Python Gaussian Filter (3x3 kernel)
gaussian_3x3 = [
    [1.0 / 16.0, 2.0 / 16.0, 1.0 / 16.0],
    [2.0 / 16.0, 4.0 / 16.0, 2.0 / 16.0],
    [1.0 / 16.0, 2.0 / 16.0, 1.0 / 16.0]
]

# 3. Fast pure-python atan2 approximation for angles in [0, 180)
def pure_atan2_deg(y, x):
    if x == 0:
        return 90.0 if y > 0 else 270.0
    # ratio
    r = abs(y) / (abs(x) + 1e-9)
    # rational approximation: deg ~= r * (45 - (r - 1) * (14 + 3.83 * r))
    if r <= 1.0:
        angle = 45.0 * r
    else:
        angle = 90.0 - (45.0 / r)
    if x < 0:
        angle = 180.0 - angle
    if y < 0:
        angle = 360.0 - angle
    # return normalized in [0, 180)
    return angle % 180.0

def canny_detector(image, low_thresh=30, high_thresh=70):
    H = len(image)
    W = len(image[0])
    
    # Step 1: Gaussian Smoothing
    blurred = convolve2d(image, gaussian_3x3)
    
    # Step 2: Sobel Gradients
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
            
    # Step 3: Non-Maximum Suppression (NMS)
    nms = [[0.0 for _ in range(W)] for _ in range(H)]
    for i in range(1, H - 1):
        for j in range(1, W - 1):
            theta = angle[i][j]
            q, r = 255.0, 255.0
            
            # 0 degrees (horizontal / east-west)
            if (0 <= theta < 22.5) or (157.5 <= theta <= 180):
                q = mag[i][j + 1]
                r = mag[i][j - 1]
            # 45 degrees (northeast-southwest)
            elif 22.5 <= theta < 67.5:
                q = mag[i + 1][j - 1]
                r = mag[i - 1][j + 1]
            # 90 degrees (vertical / north-south)
            elif 67.5 <= theta < 112.5:
                q = mag[i + 1][j]
                r = mag[i - 1][j]
            # 135 degrees (northwest-southeast)
            elif 112.5 <= theta < 157.5:
                q = mag[i - 1][j - 1]
                r = mag[i + 1][j + 1]
                
            if mag[i][j] >= q and mag[i][j] >= r:
                nms[i][j] = mag[i][j]
            else:
                nms[i][j] = 0.0

    # Step 4: Double Thresholding
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
                
    # Step 5: Edge Tracking by Hysteresis
    for i in range(1, H - 1):
        for j in range(1, W - 1):
            if res[i][j] == weak_val:
                # Check if connected to any strong edge pixel in 8-neighborhood
                has_strong = any(
                    res[i + di][j + dj] == strong_val
                    for di in (-1, 0, 1) for dj in (-1, 0, 1)
                )
                res[i][j] = strong_val if has_strong else 0
                
    return res

sample_image = [
    [ 20,  20,  20,  20,  20,  20,  20,  20,  20,  20],
    [ 20,  20,  20,  20,  20,  20,  20,  20,  20,  20],
    [ 20,  20, 200, 200, 200, 200, 200, 200,  20,  20],
    [ 20,  20, 200, 200, 200, 200, 200, 200,  20,  20],
    [ 20,  20, 200, 200, 200, 200, 200, 200,  20,  20],
    [ 20,  20, 200, 200, 200, 200, 200, 200,  20,  20],
    [ 20,  20, 200, 200, 200, 200, 200, 200,  20,  20],
    [ 20,  20, 200, 200, 200, 200, 200, 200,  20,  20],
    [ 20,  20,  20,  20,  20,  20,  20,  20,  20,  20],
    [ 20,  20,  20,  20,  20,  20,  20,  20,  20,  20]
]

canny_edges = canny_detector(sample_image, low_thresh=40, high_thresh=100)

print("=" * 65)
print(" CANNY EDGE DETECTION (Pure Python - Zero Imports)")
print("=" * 65)

print("\n--- Detected Canny Binary Edges (1-Pixel Thin) ---")
for row in canny_edges:
    print("  ", [f"{p:3d}" for p in row])

print("\n--- ASCII Visual of Canny Edges ('#' = Edge, '.' = Background) ---")
for row in canny_edges:
    print("  " + " ".join("#" if p == 255 else "." for p in row))
print("=" * 65)

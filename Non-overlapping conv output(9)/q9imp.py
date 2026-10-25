# -------------------------------------------------------------
# Question 9: Non-Overlapping Triangles & 2D Convolution Output
# Pure Python Implementation (NO IMPORT MODULES USED)
# -------------------------------------------------------------

# 1. Image canvas dimensions (e.g. 35 x 45 grid for fast pure-python rasterization)
H, W = 35, 45
image = [[0 for _ in range(W)] for _ in range(H)]

# 2. Rasterize non-overlapping triangles into the 2D grid
# Point-in-triangle test using cross-product / half-plane sign test
def point_in_triangle(px, py, x1, y1, x2, y2, x3, y3):
    d1 = (px - x2) * (y1 - y2) - (x1 - x2) * (py - y2)
    d2 = (px - x3) * (y2 - y3) - (x2 - x3) * (py - y3)
    d3 = (px - x1) * (y3 - y1) - (x3 - x1) * (py - y1)
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    return not (has_neg and has_pos)

# Triangle parameters
side = 8
height = 7
gap_x = 5
gap_y = 5

for row_idx, y in enumerate(range(3, H - height, height + gap_y)):
    for col_idx, x in enumerate(range(3, W - side, side + gap_x)):
        # Alternate orientation
        if (row_idx + col_idx) % 2 == 0:
            # Upward triangle
            pts = (x, y + height, x + side, y + height, x + side // 2, y)
        else:
            # Downward triangle
            pts = (x, y, x + side, y, x + side // 2, y + height)
            
        x1, y1, x2, y2, x3, y3 = pts
        # Fill triangle pixels with 255
        for py in range(y, min(H, y + height + 1)):
            for px in range(x, min(W, x + side + 1)):
                if point_in_triangle(px, py, x1, y1, x2, y2, x3, y3):
                    image[py][px] = 255

# 3. Define 3x3 8-neighbor Laplacian convolution kernel
kernel = [
    [-1, -1, -1],
    [-1,  8, -1],
    [-1, -1, -1]
]

# 4. Pure Python 2D Convolution Function
def convolve2d(img, kern):
    h = len(img)
    w = len(img[0])
    kh = len(kern)
    kw = len(kern[0])
    pad_y = kh // 2
    pad_x = kw // 2
    
    out = [[0 for _ in range(w)] for _ in range(h)]
    
    for i in range(h):
        for j in range(w):
            val = 0.0
            for ki in range(kh):
                for kj in range(kw):
                    ni = i + ki - pad_y
                    nj = j + kj - pad_x
                    if 0 <= ni < h and 0 <= nj < w:
                        val += img[ni][nj] * kern[ki][kj]
            # Absolute value and clip to [0, 255]
            out[i][j] = int(min(255, max(0, abs(val))))
    return out

conv_output = convolve2d(image, kernel)

# 5. Display ASCII Visualization of Original Image and Convolution Result
print("=" * 65)
print(" QUESTION 9: NON-OVERLAPPING TRIANGLES & 2D CONVOLUTION (LAPLACIAN)")
print("=" * 65)

print("\n--- 1. Original Image (Triangles, '#' = 255, '.' = 0) ---")
for r in range(0, H, 2):  # Step by 2 for compact console display
    print("".join("#" if image[r][c] > 127 else "." for c in range(W)))

print("\n--- 2. Convolution Output (Laplacian Edges) ---")
for r in range(0, H, 2):
    print("".join("*" if conv_output[r][c] > 100 else "." for c in range(W)))

# 6. Save as .pgm image
try:
    with open("triangles_original.pgm", "w") as f:
        f.write(f"P2\n{W} {H}\n255\n")
        for row in image:
            f.write(" ".join(str(val) for val in row) + "\n")
            
    with open("triangles_conv_output.pgm", "w") as f:
        f.write(f"P2\n{W} {H}\n255\n")
        for row in conv_output:
            f.write(" ".join(str(val) for val in row) + "\n")
    print("\nSaved output image files: 'triangles_original.pgm' & 'triangles_conv_output.pgm'")
except Exception:
    pass

print("=" * 65)

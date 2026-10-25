# -------------------------------------------------------------
# Question 9 (qn9): Non-Overlapping Circles & 2D Convolution Output
# Register Number: 3122235002146 (3122235002146 % 2 == 0 -> Circles)
# Pure Python Implementation (NO IMPORT MODULES USED)
# -------------------------------------------------------------

reg_no = 3122235002146
shape_type = "Circles" if (reg_no % 2 == 0) else "Triangles"

# 1. Image canvas dimensions (35 rows x 45 columns)
H, W = 35, 45
image = [[0 for _ in range(W)] for _ in range(H)]

# 2. Draw non-overlapping circles in a regular grid
radius = 4
diameter = 2 * radius
gap_x = 4
gap_y = 4

for y in range(radius + 2, H - radius, diameter + gap_y):
    for x in range(radius + 2, W - radius, diameter + gap_x):
        # Draw filled circle with 255
        for py in range(y - radius, y + radius + 1):
            for px in range(x - radius, x + radius + 1):
                if (px - x) ** 2 + (py - y) ** 2 <= radius ** 2:
                    if 0 <= py < H and 0 <= px < W:
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
            out[i][j] = int(min(255, max(0, abs(val))))
    return out

conv_output = convolve2d(image, kernel)

# 5. Display ASCII Visualization of Original Image and Convolution Result
print("=" * 65)
print(f" QUESTION 9 (qn9): NON-OVERLAPPING CIRCLES (Reg No: {reg_no})")
print(f" Condition: {reg_no} % 2 == 0 -> {shape_type}")
print("=" * 65)

print("\n--- 1. Original Image (Circles, '#' = 255, '.' = 0) ---")
for r in range(0, H, 2):  # Compact console display
    print("".join("#" if image[r][c] > 127 else "." for c in range(W)))

print("\n--- 2. Convolution Output (Laplacian Circular Edge Detection) ---")
for r in range(0, H, 2):
    print("".join("*" if conv_output[r][c] > 100 else "." for c in range(W)))

# 6. Save as .pgm image
try:
    with open("circles_original.pgm", "w") as f:
        f.write(f"P2\n{W} {H}\n255\n")
        for row in image:
            f.write(" ".join(str(val) for val in row) + "\n")
            
    with open("circles_conv_output.pgm", "w") as f:
        f.write(f"P2\n{W} {H}\n255\n")
        for row in conv_output:
            f.write(" ".join(str(val) for val in row) + "\n")
    print("\nSaved output image files: 'circles_original.pgm' & 'circles_conv_output.pgm'")
except Exception:
    pass

print("=" * 65)

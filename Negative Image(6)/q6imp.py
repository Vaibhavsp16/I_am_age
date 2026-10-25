# -------------------------------------------------------------
# Question 6: Negative of an Image
# Pure Python Implementation (NO IMPORT MODULES USED)
# -------------------------------------------------------------

# Formula:
# For an L-level grayscale image (0 to L-1, where L = 256):
# s = (L - 1) - r = 255 - r

# Function to compute image negative for a 2D matrix (grayscale)
def negative_grayscale(img_matrix):
    return [[255 - pixel for pixel in row] for row in img_matrix]

# Function to compute image negative for a 3D matrix (RGB color)
def negative_rgb(img_matrix):
    return [[[255 - c for c in pixel] for pixel in row] for row in img_matrix]

# Function to save a 2D matrix as an uncompressed Netpbm PGM (P2 ASCII) image
# Pure Python file writing without any external libraries
def save_pgm(matrix, filename):
    h = len(matrix)
    w = len(matrix[0])
    with open(filename, 'w') as f:
        f.write(f"P2\n{w} {h}\n255\n")
        for row in matrix:
            f.write(" ".join(str(int(val)) for val in row) + "\n")

# 1. Grayscale Image Negative Demonstration
# Simulated 6x6 grayscale image (e.g. gradient with a bright square inside)
original_gray = [
    [  0,   0,   0,   0,   0,   0],
    [  0, 100, 100, 100, 100,   0],
    [  0, 100, 255, 255, 100,   0],
    [  0, 100, 255, 255, 100,   0],
    [  0, 100, 100, 100, 100,   0],
    [  0,   0,   0,   0,   0,   0],
]

negative_gray = negative_grayscale(original_gray)

print("=" * 60)
print(" QUESTION 6: IMAGE NEGATIVE TRANSFORMATION (s = 255 - r)")
print("=" * 60)

print("\n--- Original Grayscale Matrix (6x6) ---")
for row in original_gray:
    print("  ", [f"{p:3d}" for p in row])

print("\n--- Negative Grayscale Matrix (6x6) ---")
for row in negative_gray:
    print("  ", [f"{p:3d}" for p in row])

# 2. RGB Image Negative Demonstration
# Sample 2x2 RGB pixel block [[R, G, B]]
original_rgb = [
    [[255,   0,   0], [  0, 255,   0]],  # Red, Green
    [[  0,   0, 255], [255, 255,   0]]   # Blue, Yellow
]

negative_rgb_img = negative_rgb(original_rgb)

print("\n--- Original RGB Image (2x2) ---")
for row in original_rgb:
    print("  ", row)

print("\n--- Negative RGB Image (2x2) [Cyan, Magenta, Yellow, Blue] ---")
for row in negative_rgb_img:
    print("  ", row)

# 3. Save as standard .pgm image file (can be opened in any image viewer)
try:
    save_pgm(original_gray, "original.pgm")
    save_pgm(negative_gray, "negative.pgm")
    print("\nSaved image files successfully: 'original.pgm' and 'negative.pgm'")
except Exception as e:
    pass

print("=" * 60)

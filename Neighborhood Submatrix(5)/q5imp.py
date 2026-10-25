# -------------------------------------------------------------
# Question 5: Neighborhood Submatrix (3x3 and 5x5 Neighborhoods)
# Pure Python Implementation (NO IMPORT MODULES USED)
# -------------------------------------------------------------

# Sample image matrix (8x8 grayscale image with distinct pixel intensity values)
# In image processing, an image is represented as a 2D matrix of pixel values [0-255].
image = [
    [ 10,  15,  20,  25,  30,  35,  40,  45],
    [ 20,  35,  50,  65,  80,  95, 110, 125],
    [ 30,  55,  80, 105, 130, 155, 180, 205],
    [ 40,  75, 110, 145, 180, 215, 250, 240],
    [ 50,  95, 140, 185, 230, 245, 220, 210],
    [ 60, 115, 170, 225, 240, 215, 190, 175],
    [ 70, 135, 200, 235, 210, 185, 160, 145],
    [ 80, 155, 230, 215, 190, 165, 140, 125]
]

H = len(image)
W = len(image[0])

# Choose a pixel with sufficient margin from borders (so neighborhoods fit)
# For a 5x5 neighborhood (radius 2), row in [2, H-3], col in [2, W-3]
target_row = 3
target_col = 4

pixel_val = image[target_row][target_col]

print("=" * 55)
print(f" Image Dimensions : {H} rows x {W} columns")
print(f" Target Pixel Loc : (row = {target_row}, col = {target_col})")
print(f" Target Pixel Val : {pixel_val}")
print("=" * 55)

# -------------------------------------------------------------
# 1. 8-Neighbourhood (3x3 submatrix centered at row, col)
# -------------------------------------------------------------
# Neighborhood consists of the center pixel + its 8 surrounding pixels:
# (r-1, c-1) to (r+1, c+1)
neighborhood_8 = [
    [image[r][c] for c in range(target_col - 1, target_col + 2)]
    for r in range(target_row - 1, target_row + 2)
]

print("\n--- 3x3 Submatrix (8-Neighbourhood) ---")
for r in neighborhood_8:
    print("  ", [f"{val:3d}" for val in r])
print(f"Shape: ({len(neighborhood_8)}, {len(neighborhood_8[0])})")

# -------------------------------------------------------------
# 2. 5x5 Neighbourhood (24 surrounding pixels + center)
# -------------------------------------------------------------
# Pixels within Chebyshev distance <= 2:
# (r-2, c-2) to (r+2, c+2)
neighborhood_24 = [
    [image[r][c] for c in range(target_col - 2, target_col + 3)]
    for r in range(target_row - 2, target_row + 3)
]

print("\n--- 5x5 Submatrix (Extended Neighbourhood) ---")
for r in neighborhood_24:
    print("  ", [f"{val:3d}" for val in r])
print(f"Shape: ({len(neighborhood_24)}, {len(neighborhood_24[0])})")

# -------------------------------------------------------------
# 3. 4-Neighbourhood (Cross / Von Neumann Neighbourhood)
# -------------------------------------------------------------
# Top, Bottom, Left, Right
neighbors_4 = {
    "Center": (target_row, target_col, image[target_row][target_col]),
    "Top"   : (target_row - 1, target_col, image[target_row - 1][target_col]),
    "Bottom": (target_row + 1, target_col, image[target_row + 1][target_col]),
    "Left"  : (target_row, target_col - 1, image[target_row][target_col - 1]),
    "Right" : (target_row, target_col + 1, image[target_row][target_col + 1])
}

print("\n--- 4-Neighbourhood Pixels ---")
for direction, (r, c, v) in neighbors_4.items():
    print(f"  {direction:<7}: Location ({r}, {c}) -> Value = {v}")
print("=" * 55)

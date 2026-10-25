# -------------------------------------------------------------
# Question 1: All Possible Images for a 3x2 (6-pixel) Binary Camera
# Pure Python Implementation (NO IMPORT MODULES USED)
# -------------------------------------------------------------

# A 3x2 camera has 3 rows and 2 columns = 6 total pixels.
# Each pixel can be binary: 0 (black) or 1 (white).
# Total combinations = 2^6 = 64 possible images.

rows, cols = 3, 2
num_pixels = rows * cols
total_combinations = 1 << num_pixels  # 2^6 = 64

# Generate all 64 binary combinations
combinations = []
for i in range(total_combinations):
    # Extract 6 bits (from most significant bit 5 down to 0)
    combo = [(i >> (num_pixels - 1 - b)) & 1 for b in range(num_pixels)]
    combinations.append(combo)

print(f"Total combinations generated for a {rows}x{cols} camera: {len(combinations)}")
print("=" * 60)

# Reshape 1D list of 6 elements into a 3x2 matrix
def reshape_to_3x2(flat_list):
    return [
        [flat_list[0], flat_list[1]],
        [flat_list[2], flat_list[3]],
        [flat_list[4], flat_list[5]]
    ]

# Display all 64 images formatted as 3x2 matrices
# We display them side-by-side in rows of 8 images (8 x 8 = 64)
grid_cols = 8

for group_start in range(0, total_combinations, grid_cols):
    group = combinations[group_start : group_start + grid_cols]
    
    # Print headers (Image indices)
    headers = [f"Img {idx+1:02d}:" for idx in range(group_start, group_start + len(group))]
    print("   ".join(headers))
    
    # Print the 3 rows for each image in the current group side by side
    matrices = [reshape_to_3x2(c) for c in group]
    for r in range(rows):
        row_str = "   ".join(f"[{m[r][0]} {m[r][1]}]   " for m in matrices)
        print(row_str)
    print("-" * 60)

print(f"\nSuccessfully generated and displayed all {total_combinations} possible 3x2 binary images.")

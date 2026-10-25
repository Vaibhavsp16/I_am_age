# -------------------------------------------------------------
# Question 4: Coin Percentage Calculation
# Pure Python Implementation (NO IMPORT MODULES USED)
# -------------------------------------------------------------

# Formula:
# Coin Area = pi * r^2
# Image Area = Height * Width
# Percentage Area = (Coin Area / Image Area) * 100

PI = 3.141592653589793

# 1. Function to calculate percentage area from image matrix using thresholding
def calculate_coin_percentage_matrix(image_matrix, threshold=127):
    """
    Counts pixels above threshold (coin pixels) and calculates percentage.
    """
    total_pixels = len(image_matrix) * len(image_matrix[0])
    coin_pixels = 0
    for row in image_matrix:
        for pixel in row:
            if pixel > threshold:
                coin_pixels += 1
    percentage = (coin_pixels / total_pixels) * 100.0
    return coin_pixels, total_pixels, percentage

# 2. Demonstration on a simulated 20x20 grayscale image containing a circular coin
grid_h, grid_w = 20, 20
center_x, center_y = 10, 10
sim_radius = 5

simulated_image = [[0 for _ in range(grid_w)] for _ in range(grid_h)]
for y in range(grid_h):
    for x in range(grid_w):
        # Distance squared from center
        if (x - center_x) ** 2 + (y - center_y) ** 2 <= sim_radius ** 2:
            simulated_image[y][x] = 255  # Coin pixel (white)
        else:
            simulated_image[y][x] = 20   # Background pixel (dark)

coin_px, total_px, pct = calculate_coin_percentage_matrix(simulated_image, threshold=127)

print("=" * 65)
print(" PART 1: Threshold-based Coin Pixel Percentage on 2D Matrix")
print("=" * 65)
print(f"Image Dimensions : {grid_h} x {grid_w} ({total_px} pixels)")
print(f"Coin Pixels Found: {coin_px}")
print(f"Percentage Area  : {pct:.2f}%")

print("\nVisual preview (C = coin, . = background):")
for row in simulated_image:
    print(" ".join("C" if p > 127 else "." for p in row))

# 3. Part 2: Distance vs Percentage Area calculation for standard lab values
# In optics, object size in image r is inversely proportional to distance: r ~ focal_length * R / d
# Area ~ pi * r^2 ~ 1 / d^2
print("\n" + "=" * 65)
print(" PART 2: Capturing Distance vs. Percentage Area Occupied")
print("=" * 65)

# Standard experimental distances (cm) and corresponding detected coin radii (pixels)
# in a 640x480 (307,200 pixel) camera sensor:
img_h, img_w = 480, 640
img_total_pixels = img_h * img_w

lab_data = [
    # (Distance in cm, Coin radius in pixels)
    (10, 150),
    (20,  80),
    (30,  55),
    (40,  42),
    (50,  34),
    (60,  28),
    (70,  24),
    (80,  21),
    (90,  19),
    (100, 17)
]

print(f"{'Distance (cm)':<15} {'Radius (px)':<15} {'Coin Area (px^2)':<18} {'Percentage Area (%)'}")
print("-" * 65)

distances = []
percentages = []

for dist, r in lab_data:
    coin_area = PI * (r ** 2)
    percentage = (coin_area / img_total_pixels) * 100.0
    distances.append(dist)
    percentages.append(percentage)
    print(f"{dist:<15} {r:<15} {coin_area:<18.1f} {percentage:.2f}%")

# 4. Text/ASCII Plot: Distance vs Percentage Area
print("\n" + "=" * 65)
print(" ASCII PLOT: Distance vs. Percentage Area Occupied")
print("=" * 65)
max_pct = max(percentages)
plot_width = 40

for d, p in zip(distances, percentages):
    bar_len = int((p / max_pct) * plot_width)
    bar = "#" * bar_len
    print(f"{d:3d} cm | {bar:<40} {p:5.2f}%")
print("       " + "-" * 42)
print("       0%                                     Max%")

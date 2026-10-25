# -------------------------------------------------------------
# Question 8: Intensity Transformations & Power Law (Gamma) Transformations
# Pure Python Implementation (NO IMPORT MODULES USED)
# -------------------------------------------------------------

# Algorithms Implemented:
# 1. Log Transformation: s = c * ln(1 + r)
# 2. Image Negative: s = 255 - r
# 3. Power Law (Gamma) Transformation: s = 255 * (r / 255) ** gamma
# 4. Contrast Stretching (Piecewise Linear Transformation)

# Pure Python Natural Log function (ln) without importing math
def pure_ln(x):
    if x <= 0:
        return 0.0
    # Range reduction using ln(m * 2^k) = ln(m) + k * ln(2)
    ln2 = 0.6931471805599453
    k = 0
    while x > 2.0:
        x /= 2.0
        k += 1
    while x < 1.0:
        x *= 2.0
        k -= 1
    # Series expansion for y = (x - 1) / (x + 1)
    y = (x - 1.0) / (x + 1.0)
    y2 = y * y
    res = 0.0
    term = y
    for n in range(1, 15, 2):
        res += term / n
        term *= y2
    return 2.0 * res + k * ln2

# 1. Log Transformation
def log_transform(image):
    # Find max pixel value
    max_val = max(max(row) for row in image)
    if max_val == 0:
        return [[0 for _ in row] for row in image]
    c = 255.0 / pure_ln(1.0 + max_val)
    return [[int(min(255, max(0, c * pure_ln(1.0 + r)))) for r in row] for row in image]

# 2. Negative Transformation
def negative_transform(image):
    return [[255 - r for r in row] for row in image]

# 3. Power Law (Gamma) Transformation
def gamma_transform(image, gamma):
    return [
        [int(min(255, max(0, 255.0 * ((r / 255.0) ** gamma)))) for r in row]
        for row in image
    ]

# 4. Contrast Stretching (Piecewise Linear Transformation)
def contrast_stretch_pixel(pix, r1=70, s1=0, r2=140, s2=255):
    if 0 <= pix <= r1:
        return int((s1 / r1) * pix) if r1 != 0 else 0
    elif r1 < pix <= r2:
        return int(((s2 - s1) / (r2 - r1)) * (pix - r1) + s1) if r2 != r1 else s1
    else:
        return int(((255 - s2) / (255 - r2)) * (pix - r2) + s2) if r2 != 255 else s2

def contrast_stretch(image, r1=70, s1=0, r2=140, s2=255):
    return [
        [int(min(255, max(0, contrast_stretch_pixel(r, r1, s1, r2, s2)))) for r in row]
        for row in image
    ]

# ----------------- Demonstration on Sample 5x5 Image -----------------
sample_image = [
    [ 15,  35,  70, 110, 150],
    [ 30,  55,  85, 125, 175],
    [ 45,  75, 100, 140, 200],
    [ 60,  95, 115, 160, 225],
    [ 80, 110, 130, 180, 250]
]

print("=" * 65)
print(" QUESTION 8: POWER LAW & INTENSITY TRANSFORMATIONS")
print("=" * 65)

print("\n--- Original Input Image (5x5) ---")
for row in sample_image:
    print("  ", [f"{p:3d}" for p in row])

# 1. Log Transform
log_img = log_transform(sample_image)
print("\n--- 1. Log Transformed Image ---")
for row in log_img:
    print("  ", [f"{p:3d}" for p in row])

# 2. Negative Image
neg_img = negative_transform(sample_image)
print("\n--- 2. Negative Transformed Image ---")
for row in neg_img:
    print("  ", [f"{p:3d}" for p in row])

# 3. Gamma Transformations for gamma in [0.1, 0.5, 1.2, 2.2]
print("\n--- 3. Power Law (Gamma) Transformations ---")
for g in [0.1, 0.5, 1.2, 2.2]:
    g_img = gamma_transform(sample_image, g)
    print(f"\nGamma = {g}:")
    for row in g_img:
        print("  ", [f"{p:3d}" for p in row])

# 4. Contrast Stretching
cs_img = contrast_stretch(sample_image, r1=70, s1=0, r2=140, s2=255)
print("\n--- 4. Contrast Stretched Image (r1=70, s1=0, r2=140, s2=255) ---")
for row in cs_img:
    print("  ", [f"{p:3d}" for p in row])

print("=" * 65)

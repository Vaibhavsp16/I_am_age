# -------------------------------------------------------------
# Question 11: Differential Matrix Operators (Rotation, Scaling, Shearing)
# Pure Python Implementation (NO IMPORT MODULES USED)
# -------------------------------------------------------------

# 1. Pure Python 3x3 Matrix Inversion (via Determinant & Adjugate Matrix)
def invert_3x3(m):
    det = (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) -
        m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) +
        m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )
    if abs(det) < 1e-9:
        raise ValueError("Singular matrix cannot be inverted.")
    
    invdet = 1.0 / det
    return [
        [
            (m[1][1] * m[2][2] - m[1][2] * m[2][1]) * invdet,
            (m[0][2] * m[2][1] - m[0][1] * m[2][2]) * invdet,
            (m[0][1] * m[1][2] - m[0][2] * m[1][1]) * invdet
        ],
        [
            (m[1][2] * m[2][0] - m[1][0] * m[2][2]) * invdet,
            (m[0][0] * m[2][2] - m[0][2] * m[2][0]) * invdet,
            (m[0][2] * m[1][0] - m[0][0] * m[1][2]) * invdet
        ],
        [
            (m[1][0] * m[2][1] - m[1][1] * m[2][0]) * invdet,
            (m[0][1] * m[2][0] - m[0][0] * m[2][1]) * invdet,
            (m[0][0] * m[1][1] - m[0][1] * m[1][0]) * invdet
        ]
    ]

# 2. Pure Python 3x3 Matrix x Vector Multiplication: M @ v
def mat_vec_mul(m, v):
    return [
        m[0][0] * v[0] + m[0][1] * v[1] + m[0][2] * v[2],
        m[1][0] * v[0] + m[1][1] * v[1] + m[1][2] * v[2],
        m[2][0] * v[0] + m[2][1] * v[1] + m[2][2] * v[2]
    ]

# 3. Geometric Transformation Function (Inverse Mapping around Center)
def transform(img, M):
    h = len(img)
    w = len(img[0])
    cx = w / 2.0
    cy = h / 2.0
    
    inv_M = invert_3x3(M)
    result = [[0 for _ in range(w)] for _ in range(h)]
    
    for y in range(h):
        for x in range(w):
            # Shift origin to center
            p = [x - cx, y - cy, 1.0]
            # Apply inverse transformation
            q = mat_vec_mul(inv_M, p)
            # Shift back
            xx = int(round(q[0] + cx))
            yy = int(round(q[1] + cy))
            
            if 0 <= xx < w and 0 <= yy < h:
                result[y][x] = img[yy][xx]
                
    return result

# 4. Construct Transformation Matrices
# (a) Rotation 30 degrees (cos(30 deg) = sqrt(3)/2 ~= 0.866025, sin(30 deg) = 0.5)
cos_30 = 0.8660254037844386
sin_30 = 0.5000000000000000

R = [
    [ cos_30, -sin_30, 0.0],
    [ sin_30,  cos_30, 0.0],
    [    0.0,     0.0, 1.0]
]

# (b) Scaling Matrix (sx = 1.5, sy = 1.5)
S = [
    [1.5, 0.0, 0.0],
    [0.0, 1.5, 0.0],
    [0.0, 0.0, 1.0]
]

# (c) Shearing Matrix (shx = 0.5, shy = 0.0)
Sh = [
    [1.0, 0.5, 0.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.0, 1.0]
]

# 5. Create a sample 11x11 image with an 'F' / 'T' shape for clear visual verification
H, W = 11, 11
original_img = [[0 for _ in range(W)] for _ in range(H)]
# Draw a distinctive asymmetric 'T' / cross shape
for x in range(2, 9):
    original_img[3][x] = 255  # Horizontal bar
for y in range(3, 9):
    original_img[y][5] = 255  # Vertical stem

# Apply transformations
rotated = transform(original_img, R)
scaled = transform(original_img, S)
sheared = transform(original_img, Sh)

# 6. Display Results
def print_ascii_matrix(mat, title):
    print(f"\n--- {title} ---")
    for row in mat:
        print("  " + " ".join("#" if val > 127 else "." for val in row))

print("=" * 65)
print(" QUESTION 11: GEOMETRIC TRANSFORMATIONS (ROTATION, SCALING, SHEARING)")
print("=" * 65)

print("\n1. Transformation Matrices:")
print("Rotation Matrix (30 deg):")
for r in R:
    print("  ", [f"{v:6.3f}" for v in r])

print("\nScaling Matrix (sx=1.5, sy=1.5):")
for r in S:
    print("  ", [f"{v:6.3f}" for v in r])

print("\nShearing Matrix (shx=0.5):")
for r in Sh:
    print("  ", [f"{v:6.3f}" for v in r])

print_ascii_matrix(original_img, "Original Image ('T' Shape)")
print_ascii_matrix(rotated, "Rotated Image (30 degrees)")
print_ascii_matrix(scaled, "Scaled Image (1.5x zoom)")
print_ascii_matrix(sheared, "Sheared Image (shx=0.5)")

print("=" * 65)

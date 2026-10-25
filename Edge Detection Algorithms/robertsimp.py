# -------------------------------------------------------------
# Roberts Cross Edge Detection
# Pure Python Implementation (NO IMPORT MODULES USED)
# -------------------------------------------------------------

# Roberts Cross Kernels (2x2 diagonal differences):
# Gx:
#   [[ 1,  0],
#    [ 0, -1]]
#
# Gy:
#   [[ 0,  1],
#    [-1,  0]]

def convolve_roberts(image):
    H = len(image)
    W = len(image[0])
    
    rx = [[0 for _ in range(W)] for _ in range(H)]
    ry = [[0 for _ in range(W)] for _ in range(H)]
    magnitude = [[0 for _ in range(W)] for _ in range(H)]
    
    for y in range(H - 1):
        for x in range(W - 1):
            # Gx = image[y, x] - image[y+1, x+1]
            gx = float(image[y][x] - image[y + 1][x + 1])
            # Gy = image[y, x+1] - image[y+1, x]
            gy = float(image[y][x + 1] - image[y + 1][x])
            
            mag = (gx * gx + gy * gy) ** 0.5
            
            rx[y][x] = int(min(255, max(0, abs(gx))))
            ry[y][x] = int(min(255, max(0, abs(gy))))
            magnitude[y][x] = int(min(255, max(0, mag)))
            
    return rx, ry, magnitude

sample_image = [
    [ 25,  25,  25,  25,  25,  25,  25,  25,  25,  25],
    [ 25,  25,  25,  25,  25,  25,  25,  25,  25,  25],
    [ 25,  25, 200, 200, 200, 200, 200, 200,  25,  25],
    [ 25,  25, 200, 200, 200, 200, 200, 200,  25,  25],
    [ 25,  25, 200, 200, 200, 200, 200, 200,  25,  25],
    [ 25,  25, 200, 200, 200, 200, 200, 200,  25,  25],
    [ 25,  25, 200, 200, 200, 200, 200, 200,  25,  25],
    [ 25,  25, 200, 200, 200, 200, 200, 200,  25,  25],
    [ 25,  25,  25,  25,  25,  25,  25,  25,  25,  25],
    [ 25,  25,  25,  25,  25,  25,  25,  25,  25,  25]
]

rx, ry, mag = convolve_roberts(sample_image)

print("=" * 65)
print(" ROBERTS CROSS EDGE DETECTION (Pure Python - Zero Imports)")
print("=" * 65)

print("\n--- Roberts X Magnitudes (Diagonal \\ Edges) ---")
for row in rx:
    print("  ", [f"{p:3d}" for p in row])

print("\n--- Roberts Y Magnitudes (Diagonal / Edges) ---")
for row in ry:
    print("  ", [f"{p:3d}" for p in row])

print("\n--- Combined Roberts Magnitude ---")
for row in mag:
    print("  ", [f"{p:3d}" for p in row])

print("\n--- ASCII Visual of Roberts Edges ('#' = Edge, '.' = Background) ---")
for row in mag:
    print("  " + " ".join("#" if p > 80 else "." for p in row))
print("=" * 65)

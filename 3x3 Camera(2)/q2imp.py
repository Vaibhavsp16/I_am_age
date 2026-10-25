# -------------------------------------------------------------
# Question 2: 3x3 Camera Sensible Geometric Shape Recognition
# Pure Python Implementation (NO IMPORT MODULES USED)
# -------------------------------------------------------------

# 1. Define a dictionary of "sensible" geometric shapes (3x3 templates)
sensible_shapes = {
    "Horizontal Top Line":  [[1, 1, 1], [0, 0, 0], [0, 0, 0]],
    "Horizontal Mid Line":  [[0, 0, 0], [1, 1, 1], [0, 0, 0]],
    "Horizontal Bot Line":  [[0, 0, 0], [0, 0, 0], [1, 1, 1]],
    "Vertical Left Line":   [[1, 0, 0], [1, 0, 0], [1, 0, 0]],
    "Vertical Mid Line":    [[0, 1, 0], [0, 1, 0], [0, 1, 0]],
    "Vertical Right Line":  [[0, 0, 1], [0, 0, 1], [0, 0, 1]],
    "Plus Cross (+)":       [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
    "Diagonal Line (\\)":   [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
    "Diagonal Line (/)":    [[0, 0, 1], [0, 1, 0], [1, 0, 0]],
    "Outer Border Frame":   [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
}

# 2. Pure Python Linear Congruential Generator (LCG) for generating random bits
# Seed is initialized; no random module needed
prng_state = 987654321

def get_random_bit():
    global prng_state
    # Standard 31-bit LCG parameters
    prng_state = (1103515245 * prng_state + 12345) & 0x7FFFFFFF
    return (prng_state >> 16) & 1

def generate_random_3x3():
    return [
        [get_random_bit(), get_random_bit(), get_random_bit()],
        [get_random_bit(), get_random_bit(), get_random_bit()],
        [get_random_bit(), get_random_bit(), get_random_bit()]
    ]

def matrices_equal(m1, m2):
    for r in range(3):
        for c in range(3):
            if m1[r][c] != m2[r][c]:
                return False
    return True

# 3. Loop until a generated random matrix matches one of our templates
attempts = 0
matched_shape_name = ""
final_matrix = None

while True:
    attempts += 1
    random_matrix = generate_random_3x3()
    
    found_match = False
    for name, template in sensible_shapes.items():
        if matrices_equal(random_matrix, template):
            matched_shape_name = name
            final_matrix = random_matrix
            found_match = True
            break
            
    if found_match:
        break

# 4. Display the results
print("=============================================================")
print(f"Success! Found a sensible image after {attempts} random attempts.")
print(f"Pattern recognized: '{matched_shape_name}'")
print("=============================================================")
print("Recognized 3x3 Matrix:")
for row in final_matrix:
    print("  ", row)

print("\nVisual Representation (1 = '#', 0 = '.'):")
for row in final_matrix:
    print("   " + " ".join("#" if val == 1 else "." for val in row))

# -------------------------------------------------------------
# Question 3: 5x5 Binary Matrix Canvas (Toggle 0 / 1)
# Pure Python Implementation (NO IMPORT MODULES USED)
# -------------------------------------------------------------

# Initialize 5x5 binary matrix with 0s
size = 5
matrix = [[0 for _ in range(size)] for _ in range(size)]

def print_grid(mat, title="Current 5x5 Matrix"):
    print("\n" + "=" * 35)
    print(f" {title} ")
    print("=" * 35)
    # Column indices header
    print("    Col:  0   1   2   3   4")
    print("        ---------------------")
    for r in range(size):
        row_str = f"Row {r} | " + "   ".join(str(mat[r][c]) for c in range(size))
        # Add visual representation
        visual_str = "   [" + " ".join("#" if mat[r][c] == 1 else "." for c in range(size)) + "]"
        print(row_str + visual_str)
    print("=" * 35)

def toggle_pixel(mat, r, c):
    if 0 <= r < size and 0 <= c < size:
        mat[r][c] = 1 - mat[r][c]
        print(f"-> Toggled pixel at ({r}, {c}) to {mat[r][c]}")
        return True
    else:
        print(f"-> Error: Row and Col must be between 0 and {size - 1}.")
        return False

# 1. Demonstrate initial state
print_grid(matrix, "Initial 5x5 Binary Matrix (All 0s)")

# 2. Automated demonstration of toggling pixels (e.g. Plus cross pattern)
demo_toggles = [(0, 2), (1, 2), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (3, 2), (4, 2)]
print("\nDemonstrating pixel toggles (forming a Plus '+' pattern):")
for r, c in demo_toggles:
    toggle_pixel(matrix, r, c)

print_grid(matrix, "Matrix After Toggling '+' Pattern")

# 3. Interactive prompt for user
print("\nInteractive Mode: Enter 'row col' (e.g., '1 3') to toggle, or 'q' to finish.")
while True:
    try:
        cmd = input("Enter 'row col' to toggle (or 'q' to quit): ").strip()
        if not cmd or cmd.lower() in ('q', 'quit', 'exit', 'done'):
            break
        parts = cmd.split()
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            r, c = int(parts[0]), int(parts[1])
            toggle_pixel(matrix, r, c)
            print_grid(matrix)
        else:
            print("Invalid input. Please enter two numbers separated by space (e.g., '2 3').")
    except (EOFError, KeyboardInterrupt):
        # Automatically exit cleanly when non-interactive or end of input
        break

print("\nFinal 5x5 Matrix:")
for row in matrix:
    print(row)

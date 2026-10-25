import numpy as np
import matplotlib.pyplot as plt

# 1. Define a dictionary of "sensible" geometric shapes (3x3 templates)
sensible_shapes = {
    "Horizontal Top Line":  np.array([[1,1,1], [0,0,0], [0,0,0]]),
    "Horizontal Mid Line":  np.array([[0,0,0], [1,1,1], [0,0,0]]),
    "Horizontal Bot Line":  np.array([[0,0,0], [0,0,0], [1,1,1]]),
    "Vertical Left Line":   np.array([[1,0,0], [1,0,0], [1,0,0]]),
    "Vertical Mid Line":    np.array([[0,1,0], [0,1,0], [0,1,0]]),
    "Vertical Right Line":  np.array([[0,0,1], [0,0,1], [0,0,1]]),
    "Plus Cross (+)":       np.array([[0,1,0], [1,1,1], [0,1,0]]),
    "Diagonal Line (\\)":   np.array([[1,0,0], [0,1,0], [0,0,1]]),
    "Diagonal Line (/)":    np.array([[0,0,1], [0,1,0], [1,0,0]]),
    "Outer Border Frame":   np.array([[1,1,1], [1,0,1], [1,1,1]]),
}

attempts = 0
matched_shape_name = ""
final_matrix = None

# 2. Loop until a generated matrix matches one of our templates
while True:
    attempts += 1
    # Generate a random 3x3 matrix of 0s and 1s
    random_matrix = np.random.choice([0, 1], size=(3, 3))
    
    # Check if this random matrix matches any sensible shape
    found_match = False
    for name, template in sensible_shapes.items():
        if np.array_equal(random_matrix, template):
            matched_shape_name = name
            final_matrix = random_matrix
            found_match = True
            break
            
    if found_match:
        break

# 3. Display the successful matrix as an image
print(f"Success! Found a sensible image after {attempts} random attempts.")
print(f"Pattern recognized: {matched_shape_name}")

plt.figure(figsize=(4, 4))
plt.imshow(final_matrix, cmap='gray', vmin=0, vmax=1)
plt.title(f"\"{matched_shape_name}\"\nFound on attempt #{attempts}")
plt.axis('off')
plt.show()
import numpy as np
import matplotlib.pyplot as plt
import itertools

# 1. Generate all possible 2^6 (64) combinations of 0s and 1s
combinations = list(itertools.product([0, 1], repeat=6))

# 2. Set up the camera configuration (3 rows, 2 columns)
rows, cols = 3, 2
total_images = len(combinations)

# 3. Initialize the visualization grid 
grid_size = 8  # 8x8 grid fits 64 images perfectly
fig, axes = plt.subplots(grid_size, grid_size, figsize=(8, 8))
fig.suptitle('All 64 Possible Images for a 3x2 (6-pixel) Camera', fontsize=14)

# 4. Iterate through all combinations and plot each as a 2D array
for i in range(grid_size):
    for j in range(grid_size):
        idx = i * grid_size + j
        
        # Reshape the 1D array of 6 pixels into a 3x2 matrix
        img_array = np.array(combinations[idx]).reshape(rows, cols)
        
        # Plot the matrix on the correct subplot
        ax = axes[i, j]
        ax.imshow(img_array, cmap='gray', vmin=0, vmax=1)
        
        # Format the subplot for better clarity
        # ax.axis('off')  # Hide the axes
        ax.set_xticks([])
        ax.set_yticks([])

plt.tight_layout()
plt.show()

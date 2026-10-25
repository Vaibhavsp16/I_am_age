import numpy as np
import matplotlib.pyplot as plt

# 5 x 5 binary matrix
matrix = np.zeros((5, 5), dtype=int)

# Create window
fig, ax = plt.subplots(figsize=(5, 5))


def draw_grid():
    ax.clear()

    # Display the matrix
    ax.imshow(
        matrix,
        cmap="gray_r",
        vmin=0,
        vmax=1,
        interpolation="nearest"
    )

    # Draw grid lines
    ax.set_xticks(np.arange(-0.5, 5, 1))
    ax.set_yticks(np.arange(-0.5, 5, 1))
    ax.grid(True, color="black", linewidth=2)

    # Remove tick labels
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    ax.set_title("Click a pixel to toggle 0 / 1")

    fig.canvas.draw()


def mouse_click(event):

    # Only respond to clicks inside the grid
    if event.inaxes != ax:
        return

    if event.xdata is None or event.ydata is None:
        return

    # Find clicked column and row
    col = int(round(event.xdata))
    row = int(round(event.ydata))

    # Check that the click is inside the 5 x 5 matrix
    if 0 <= row < 5 and 0 <= col < 5:

        # Toggle the pixel
        matrix[row, col] = 1 - matrix[row, col]

        # Update display
        draw_grid()

        # Print current matrix
        print("\nCurrent matrix:")
        print(matrix)


# Connect mouse click to function
fig.canvas.mpl_connect(
    "button_press_event",
    mouse_click
)

# Initial display
draw_grid()

plt.show()

# Print final matrix after closing the window
print("\nFinal 5 x 5 matrix:")
print(matrix)
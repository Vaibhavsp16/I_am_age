import cv2
import numpy as np
import random

# Read image
img = cv2.imread(r"C:\Users\Vaibhav.S.P\Downloads\IPCV Lab\IPCV Lab\02_06_07_2026_IPCV\black_square.jpg")   # Replace with your image path

if img is None:
    raise FileNotFoundError("Image not found.")

# Image dimensions
h, w = img.shape[:2]

# Choose a random pixel (avoid borders so neighborhoods fit)
row = random.randint(2, h - 3)
col = random.randint(2, w - 3)

# Access the random pixel
pixel = img[row, col]

print("Random pixel location:", (row, col))
print("Pixel value (BGR):", pixel)

# ---------------------------
# 8-neighbourhood (3x3 matrix)
# ---------------------------
neighborhood_8 = img[row-1:row+2, col-1:col+2]

print("\n3x3 (8-neighbourhood):")
print(neighborhood_8)

# ---------------------------
# 16-neighbourhood (5x5 matrix)
# Center + 24 surrounding pixels
# If you mean pixels within distance 2.
# ---------------------------
neighborhood_16 = img[row-2:row+3, col-2:col+3]

print("\n5x5 neighborhood:")
print(neighborhood_16)

print("\nShapes:")
print("3x3:", neighborhood_8.shape)
print("5x5:", neighborhood_16.shape)
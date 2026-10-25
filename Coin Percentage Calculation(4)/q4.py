# import os
# import cv2
# import matplotlib.pyplot as plt
# import numpy as np

# # Prepare Your Images
# # Take your 10 photos and rename them exactly image_10.jpg, image_20.jpg, 
# # etc., based on the distance in centimeters.
# # Place all 10 images into a single folder on your Windows PC

# # Defined distances corresponding to your image file names
# distances = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
# percentage_areas = []
# valid_distances = []

# for dist in distances:
#     filename = f"image_{dist}.jpg"
    
#     if not os.path.exists(filename):
#         print(f"Skipping: {filename} not found.")
#         continue

#     # 1. Load image in grayscale
#     img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    
#     # 2. Total number of pixels in the image
#     total_pixels = img.shape[0] * img.shape[1]

#     # 3. Threshold the image to isolate the coin
#     # Adjust the '127' value if your background is dark or light
#     # Use cv2.THRESH_BINARY_INV if the coin is dark and background is light
#     _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

#     # 4. Count coin pixels (white pixels in the thresholded image)
#     coin_pixels = cv2.countNonZero(thresh)

#     # 5. Calculate percentage area
#     percentage = (coin_pixels / total_pixels) * 100
#     percentage_areas.append(percentage)
#     valid_distances.append(dist)
    
#     print(f"{filename} -> Coin Area: {percentage:.2f}%")

# # Plotting the real data
# if percentage_areas:
#     plt.figure(figsize=(8, 5))
#     plt.plot(valid_distances, percentage_areas, marker='o', linestyle='-', color='crimson')
#     plt.title('Actual Capturing Distance vs. Percentage Area Occupied')
#     plt.xlabel('Distance (cm)')
#     plt.ylabel('Percentage Area (%)')
#     plt.grid(True, linestyle='--')
    
#     for d, p in zip(valid_distances, percentage_areas):
#         plt.annotate(f"{p:.1f}%", (d, p), textcoords="offset points", xytext=(0,10), ha='center')
        
#     plt.show()
# else:
#     print("No images were found to process.")

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

images = [
    (os.path.join("q4img", f"4_{i}.jpeg"), 7 + i) for i in range(1, 11)
]

distances = []
percentages = []

folder = os.path.dirname(os.path.abspath(__file__))

for filename, distance in images:

    path = os.path.join(folder, filename)
    img = cv2.imread(path)

    if img is None:
        print("Could not read:", filename)
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (9, 9), 2)

    h, w = gray.shape

    # Search only around the center
    x1 = int(w * 0.25)
    x2 = int(w * 0.75)
    y1 = int(h * 0.25)
    y2 = int(h * 0.75)

    crop = gray[y1:y2, x1:x2]

    circles = cv2.HoughCircles(
        crop,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=50,
        param1=100,
        param2=30,
        minRadius=30,
        maxRadius=400
    )

    if circles is None:
        print("Coin not detected:", filename)
        continue

    circles = np.round(circles[0]).astype(int)

    # Select largest detected circle
    x, y, r = max(circles, key=lambda c: c[2])

    # Convert coordinates back to original image
    x += x1
    y += y1

    coin_area = np.pi * r * r
    image_area = h * w

    percentage = (coin_area / image_area) * 100

    distances.append(distance)
    percentages.append(percentage)

    print(
        f"{filename}: Distance = {distance} cm, "
        f"Radius = {r} pixels, "
        f"Percentage Area = {percentage:.2f}%"
    )

    output = img.copy()

    cv2.circle(output, (x, y), r, (0, 255, 0), 3)
    cv2.circle(output, (x, y), 3, (0, 0, 255), -1)

    cv2.imshow("Coin Detection", output)
    cv2.waitKey(500)

cv2.destroyAllWindows()

if distances:
    plt.figure(figsize=(8, 5))
    plt.plot(distances, percentages, 'o-', color='crimson')

    plt.xlabel("Capturing Distance (cm)")
    plt.ylabel("Percentage Area Occupied (%)")
    plt.title("Distance vs Percentage Area Occupied by Coin")

    for d, p in zip(distances, percentages):
        plt.annotate(f"{p:.2f}%", (d, p), textcoords="offset points", xytext=(0, 10), ha='center')

    plt.grid(True, linestyle='--')
    plt.show()
else:
    print("No valid coins detected to plot.")
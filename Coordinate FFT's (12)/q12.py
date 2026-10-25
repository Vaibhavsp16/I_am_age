import cv2
import numpy as np
import matplotlib.pyplot as plt

cap = cv2.VideoCapture(r"C:\Users\Vaibhav.S.P\Downloads\IPCV Lab\IPCV Lab\07_24_08_2026_IPCV\q12\leaf.py.mp4")

fps = cap.get(cv2.CAP_PROP_FPS)
skip = int(fps * 0.5)       # take one frame every 0.5 seconds

row = []
col = []
frame_no = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Process only every 0.5 second
    if frame_no % skip != 0:
        frame_no += 1
        continue

    clicked = []

    def mouse(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            clicked.append((x, y))

    cv2.namedWindow("Leaf")
    cv2.setMouseCallback("Leaf", mouse)

    while True:
        cv2.imshow("Leaf", frame)

        if clicked:
            x, y = clicked[0]

            col.append(x)
            row.append(y)
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            exit()

    frame_no += 1

cap.release()
cv2.destroyAllWindows()

# Convert to arrays
row = np.array(row)
col = np.array(col)

print("Number of samples:", len(row))

# ---------------- 1D FFT ----------------

row_fft = np.abs(np.fft.fft(row))
col_fft = np.abs(np.fft.fft(col))

# ---------------- 2D FFT ----------------

data = np.vstack((row, col))
fft2 = np.abs(np.fft.fft2(data))

# ---------------- Display ----------------

plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.plot(row)
plt.title("Row Coordinate vs Frame")
plt.xlabel("Frame")
plt.ylabel("Row")

plt.subplot(2, 2, 2)
plt.plot(col)
plt.title("Column Coordinate vs Frame")
plt.xlabel("Frame")
plt.ylabel("Column")

plt.subplot(2, 2, 3)
plt.plot(row_fft)
plt.title("1D FFT - Row Coordinate")
plt.xlabel("Frequency")
plt.ylabel("Magnitude")

plt.subplot(2, 2, 4)
plt.plot(col_fft)
plt.title("1D FFT - Column Coordinate")
plt.xlabel("Frequency")
plt.ylabel("Magnitude")

plt.tight_layout()
plt.show()

# 2D FFT
plt.imshow(fft2, cmap="gray", aspect="auto")
plt.title("2D FFT")
plt.xlabel("Frequency")
plt.ylabel("Signal")
plt.colorbar()
plt.show()

print("\nRow coordinates:")
print(row)

print("\nColumn coordinates:")
print(col)
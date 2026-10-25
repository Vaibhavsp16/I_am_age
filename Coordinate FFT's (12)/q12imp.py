# -------------------------------------------------------------
# Question 12: 1D and 2D Discrete Fourier Transform (FFT / DFT) of Coordinates
# Pure Python Implementation (NO IMPORT MODULES USED)
# -------------------------------------------------------------

PI = 3.141592653589793

# Pure Python Cosine and Sine using Taylor Series Expansion (zero imports)
def pure_cos(x):
    # Normalize x to [-pi, pi]
    twopi = 2.0 * PI
    x = x % twopi
    if x > PI:
        x -= twopi
    # Taylor expansion: 1 - x^2/2! + x^4/4! - x^6/6! + x^8/8!
    x2 = x * x
    return 1.0 - x2/2.0 + (x2*x2)/24.0 - (x2*x2*x2)/720.0 + (x2*x2*x2*x2)/40320.0

def pure_sin(x):
    twopi = 2.0 * PI
    x = x % twopi
    if x > PI:
        x -= twopi
    # Taylor expansion: x - x^3/3! + x^5/5! - x^7/7! + x^9/9!
    x2 = x * x
    return x * (1.0 - x2/6.0 + (x2*x2)/120.0 - (x2*x2*x2)/5040.0 + (x2*x2*x2*x2)/362880.0)

# 1. 1D Discrete Fourier Transform (DFT)
# X[k] = sum_{n=0}^{N-1} x[n] * [cos(2*pi*k*n / N) - j * sin(2*pi*k*n / N)]
def dft_1d(signal):
    N = len(signal)
    magnitudes = []
    complex_out = []
    
    for k in range(N):
        real_part = 0.0
        imag_part = 0.0
        for n in range(N):
            angle = (2.0 * PI * k * n) / N
            real_part += signal[n] * pure_cos(angle)
            imag_part -= signal[n] * pure_sin(angle)
            
        mag = (real_part * real_part + imag_part * imag_part) ** 0.5
        magnitudes.append(mag)
        complex_out.append((real_part, imag_part))
        
    return magnitudes, complex_out

# 2. 2D Discrete Fourier Transform (DFT2)
# Apply 1D DFT to rows, then to columns
def dft_2d(matrix_2d):
    rows = len(matrix_2d)
    cols = len(matrix_2d[0])
    
    # Step 1: 1D DFT across each row
    row_transformed = []
    for r in range(rows):
        _, c_row = dft_1d(matrix_2d[r])
        row_transformed.append(c_row)
        
    # Step 2: 1D DFT down each column
    mag_2d = [[0.0 for _ in range(cols)] for _ in range(rows)]
    for c in range(cols):
        col_signal_real = [row_transformed[r][c][0] for r in range(rows)]
        col_signal_imag = [row_transformed[r][c][1] for r in range(rows)]
        
        for k in range(rows):
            real_total = 0.0
            imag_total = 0.0
            for n in range(rows):
                angle = (2.0 * PI * k * n) / rows
                c_val = pure_cos(angle)
                s_val = pure_sin(angle)
                # (a + j*b) * (cos - j*sin) = (a*cos + b*sin) + j*(b*cos - a*sin)
                real_total += col_signal_real[n] * c_val + col_signal_imag[n] * s_val
                imag_total += col_signal_imag[n] * c_val - col_signal_real[n] * s_val
            mag_2d[k][c] = (real_total * real_total + imag_total * imag_total) ** 0.5
            
    return mag_2d

# 3. Leaf coordinate trajectories sampled across frames
# (16 time frames capturing object movement)
row_coords = [150.0, 155.0, 162.0, 175.0, 190.0, 210.0, 225.0, 235.0,
              230.0, 215.0, 195.0, 180.0, 165.0, 158.0, 152.0, 150.0]

col_coords = [100.0, 115.0, 135.0, 160.0, 190.0, 220.0, 250.0, 275.0,
              290.0, 295.0, 285.0, 260.0, 225.0, 185.0, 145.0, 115.0]

N = len(row_coords)

# Compute 1D FFT/DFT
row_mag, _ = dft_1d(row_coords)
col_mag, _ = dft_1d(col_coords)

# Compute 2D FFT/DFT on the 2 x N coordinate matrix
data_2d = [row_coords, col_coords]
fft2_mag = dft_2d(data_2d)

# 4. Display Results
print("=" * 65)
print(" QUESTION 12: 1D AND 2D DISCRETE FOURIER TRANSFORM OF COORDINATES")
print("=" * 65)
print(f"Number of Frame Samples : {N}")
print(f"Row Coordinates         : {[int(x) for x in row_coords]}")
print(f"Col Coordinates         : {[int(x) for x in col_coords]}")
print("=" * 65)

print("\n--- 1D DFT Magnitudes (Frequency vs Magnitude) ---")
print(f"{'Freq (k)':<10} {'Row Mag |X_row(k)|':<25} {'Col Mag |X_col(k)|'}")
print("-" * 55)
for k in range(N):
    print(f"{k:<10} {row_mag[k]:<25.2f} {col_mag[k]:.2f}")

print("\n--- ASCII Spectrum: Row Coordinate 1D DFT ---")
max_row_mag = max(row_mag)
for k in range(N):
    bar = "=" * int((row_mag[k] / max_row_mag) * 35)
    print(f"k={k:2d} | {bar:<35} {row_mag[k]:.1f}")

print("\n--- 2D DFT Magnitude Matrix (2 x 16) ---")
print("Row 0 (Row Coord Component):")
print("  ", [f"{v:7.1f}" for v in fft2_mag[0]])
print("Row 1 (Col Coord Component):")
print("  ", [f"{v:7.1f}" for v in fft2_mag[1]])
print("=" * 65)

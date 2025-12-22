import numpy as np
import matplotlib.pyplot as plt

# ======================================================
# 1. Membuat Objek 2D (Persegi Panjang)
# ======================================================
shape = np.array([
    [0, 0, 1],
    [4, 0, 1],
    [4, 2, 1],
    [0, 2, 1],
    [0, 0, 1]  # kembali ke titik awal agar tertutup
])

# ======================================================
# 2. Fungsi untuk Plot
# ======================================================
def plot_shape(original, transformed, title):
    plt.figure(figsize=(6,6))
    plt.plot(original[:,0], original[:,1], label="Original", linewidth=2)
    plt.plot(transformed[:,0], transformed[:,1], label="Transformed", linestyle='--')
    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.legend()
    plt.axis('equal')
    plt.show()

# ======================================================
# 3. Fungsi Transformasi 2D
# ======================================================

# A. Translasi
def translate(points, tx, ty):
    T = np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0,  1]
    ])
    return points @ T

# B. Rotasi
def rotate(points, angle_deg):
    theta = np.radians(angle_deg)
    R = np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta),  np.cos(theta), 0],
        [0, 0, 1]
    ])
    return points @ R

# C. Skala
def scale(points, sx, sy):
    S = np.array([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ])
    return points @ S

# D. Refleksi sumbu-Y
def reflect_y(points):
    R = np.array([
        [-1, 0, 0],
        [ 0, 1, 0],
        [ 0, 0, 1]
    ])
    return points @ R

# ======================================================
# 4. Menjalankan Semua Transformasi
# ======================================================

# 4.1 Translasi
translated = translate(shape, 5, 3)
plot_shape(shape, translated, "Translasi (5, 3)")

# 4.2 Rotasi
rotated = rotate(shape, 45)
plot_shape(shape, rotated, "Rotasi 45°")

# 4.3 Skala
scaled = scale(shape, 2, 1.5)
plot_shape(shape, scaled, "Skala (2x, 1.5x)")

# 4.4 Refleksi
reflected = reflect_y(shape)
plot_shape(shape, reflected, "Refleksi terhadap Sumbu-Y")

# 4.5 Komposisi Transformasi: Translasi → Rotasi → Skala
combined = scale(rotate(translate(shape, 4, 2), 30), 1.5, 1.5)
plot_shape(shape, combined, "Translasi → Rotasi → Skala")

# ======================================================
# Selesai
# ======================================================

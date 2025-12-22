import numpy as np
import matplotlib.pyplot as plt

#buat objek 2d persegi
shape = np.array([
    [0, 0, 1],
    [4, 0, 1],
    [4, 2, 1],
    [0, 2, 1],
    [0, 0, 1]  # kembali ke titik awal agar tertutup
    ])

def plot_shape(original, transformed, title):
    plt.figure(figsize=(6,6))
    plt.plot(original[:,0], original[:,1], label="Original", linewidth=3) #inewidth=3 -> ketebalan garis
    plt.plot(transformed[:,0], transformed[:,1], label="Transformed", linestyle='--')
    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.legend()
    plt.axis('equal')
    plt.show()

#fungsi transformasi 2d
# Translasi
def translate(points, tx, ty):
    T = np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0,  1]
    ])
    return points @ T

#Untuk menjalankan
# Translasi
translated = translate(shape, 5, 3)
plot_shape(shape, translated, "Translasi (5, 3)")
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
# skala
def scale(points, sx, sy):
    S = np.array([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ])
    return points @ S

#Untuk menjalankan
# skala
scaled = scale(shape, 2, 2) #(shape, nilai untuk kelipatan, nilai untuk ukurannya)
plot_shape(shape, scaled, "Skala (2x, 1.5x)")



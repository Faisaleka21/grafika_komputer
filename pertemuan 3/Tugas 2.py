# TUGAS A (Ruster)
# Buat program Python yang menampilkan grid 10×10
# piksel menggunakan ".".
# Ganti piksel di posisi (4,6) menjadi "X".
print('======= Tugas 2 =======')
print('===== Soal 1 =====')
lebar = 10
tinggi = 10
# koordinat piksel
x = 4
y = 6
for i in range(lebar):
    for k in range(tinggi):
        if i == x and k == y:
            print('X', end='')
        else:
            print('.', end='')
    print()
print('')

# TUGAS B (Vektor)
# Buat program Python yang menggambar garis dari titik
# (0,0) ke (5,3) dengan menghitung titik-titik koordinatnya
# (seperti vektor).
print('===== Soal 2 =====')
x1,y1 = 0,0
x2,y2 = 5,3
n=5

for i in range(n+1):
    x = x1+(x2-x1)*i/n
    y = y1+(y2-x1)*i/n
    print(f'Titik {i} : ({x:.1f},{y:.1f})') #: .1f itu diberi karena untuk menghapus nilai 0 yg banyak
print('')



# TUGAS C
# Buat tabel perbandingan raster dan vektor berdasarkan
# hasil praktikum Anda.
print('===== Soal 3 =====')

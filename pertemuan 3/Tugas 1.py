# praktikum koordinat

print('===== Soal 1 =====')
import math
x1 = int(input('Masukkan x1 : '))
y1 = int(input('Masukkan y1 : '))
x2 = int(input('Masukkan x2 : '))
y2 = int(input('Masukkan y2 : '))

print('======= Hasill =======')
jarak = math.sqrt((x2-x1)**2+(y2-y1)**2)    
hasil=jarak
print(f'Jarak antara dua titik : {hasil}')

# tentukan kuadran
if x1<0 and y1<0:
    kuadran='Kuadran 1'
elif x1>0 and y1>0:
    kuadran='Kuadran 2'
elif x1<0 and y1>0:
    kuadran='Kuadran 3'
elif x1>0 and y1<0:
    kuadran='Kuadran 4'
elif x1==0 and y1==0:
    kuadran='Titik pusat (0,0)'
elif x1<0 == 0:
    kuadran='Berada di Sumbu Y'
else:
    kuadran='Berada di Sumbu X'
print(f'Titik pertama berada di: {kuadran}')

print('===== Soal 2 =====')
# Simulasikan sistem koordinat layar berukuran 10x5 piksel menggunakan simbol ".",
# dan tampilkan posisi titik (x=3, y=2) dengan karakter "X".

lebar = 10
tinggi = 5
x = 3
y = 2
for baris in range (tinggi, 0,-1):
    for kolom in range (1, lebar + 1):
        if x == 2 and y == 3:
            print('X', end='')
        else:
            print('.', end='')
    print()

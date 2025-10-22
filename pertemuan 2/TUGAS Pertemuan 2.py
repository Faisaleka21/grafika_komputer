#Tugas1

#Praktikum 1
print('Tugas 1')
print('==== A ====')
x=50
y=100
merah='Merah'
print(f'Koordinat titik ({x},{y}) dengan warna',merah) #kalau pakai kurung kurawa. depan awalan petik dikasih f
print('')

#Praktikum 2
print('==== B ====')
x = int(input('Masukkan nilai x: '))
y = int(input('Masukkan nilai y: '))
warna = input('Masukkan warna titik : ')
print(f'Titik berada di ({x},{y}) dan berwarna {warna}')
print('')

#Praktikum 3
print('==== C ====')
x = int(input('Masukkan nilai x: '))
print('Hasilnya : ',x)
if (x>0):
    print('Titik di Kanan layar')
elif(x==0):
    print('Titik di Tengah')
else:
    print('Titik di Kiri Layar')
print('==============')
print('Perulangan 1-5')
print('--------------')
for i in range(1,6):
    print(f'Titik ke-{i}')
print('')

#Praktikum 4
import math
print('==== D ====')
def hitung_jarak(x1,y1,x2,y2):
    jarak = math.sqrt((x2-x1)**2+(y2-y1)**2)
    return jarak
hasil=hitung_jarak(0,0,3,4)
print(f'Jarak antara dua titik : {hasil}')

#Praktikum 5
print('\n==== E ====')
print('1. List')
titik_list = [(0,0),(50,50),(100,0)]
for titik in titik_list:
    print(titik)
print('-------------')
print('2. Tuple')
pusat=(0,0)
print('Titik Pusat',pusat)
print('-------------')
print('3. Dictionary')
objek = {'x':10,'y':20,'warna':'biru'}
print(f"Titik ({objek['x']},{objek['y']}) berwarna {objek['warna']}.")

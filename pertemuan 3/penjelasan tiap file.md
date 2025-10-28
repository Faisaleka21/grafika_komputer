<h1 align=center>PENJELASAN DARI TIAP FILE PADA PERTEMUAN 3</h1>

## 1. Praktikum1.py

Pada file <b><i>Praktikum1.py</i></b> ini berisi terkait kode praktik dari contoh Classroom. Berikut kodenya:

    for y in range (0,5):
        for x in range (0,10):
            print('x ',end='')
        print()

Hasil dari kode dia atas maka hasilnya ini :

<p align=center>
<img width="230" height="189" alt="image" src="https://github.com/user-attachments/assets/12711d5e-c701-4f87-8dfa-7f837a30e5f7" />
</p>

-----------------------------------------------------------------

## 2.Tugas1.py

Pada file Tugas1.py terdapat 2 tugas yaitu 

1. Soal 1:

      Buat program Python untuk:
      
      a. Menerima input dua titik (x1, y1) dan (x2, y2).
      
      b. Hitung jarak antara kedua titik.
      
      c. Tentukan di kuadran mana titik pertama berada (berdasarkan sistem Kartesius).

Dari soal diatas, berikut kodenya :

        print('===== Soal 1 =====')
        import math
        x1 = int(input('Masukkan x1 : '))
        y1 = int(input('Masukkan y1 : '))
        x2 = int(input('Masukkan x2 : '))
        y2 = int(input('Masukkan y2 : '))
        
        print('======= Hasill =======')
        print(f'Titik Pertama : ({x1:.1f}, {y1:.1f})')
        print(f'Titik Kedua : ({x2:.1f}, {y2:.1f})')
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

Penjelasan dari kode diatas:

        SADASDASD

Hasil dari kode diatas sbg berikut:

<p align=center>
    <img width="512" height="264" alt="image" src="https://github.com/user-attachments/assets/2ea89332-159e-4899-bdd7-978c644b24c3" />
</p>

2. Soal 2:

      a. Simulasikan sistem koordinat layar berukuran 10x5 piksel menggunakan simbol ".",
      
      b. Tampilkan posisi titik (x=3, y=2) dengan karakter "X".

Berikut adalah kodenya :

        print('===== Soal 2 =====')
        # Simulasikan sistem koordinat layar berukuran 10x5 piksel menggunakan simbol ".",
        # dan tampilkan posisi titik (x=3, y=2) dengan karakter "X".
        
        lebar = 10
        tinggi = 5
        x = 3
        y = 2
        for baris in range (0,tinggi):
            for kolom in range (0, lebar + 1):
                if kolom == x and baris == y:
                    print('X', end='')
                else:
                    print('.', end='')
            print()
    
Penjelasan dari kode diatas:

<i>"
Untuk penjelasannnya bahwa variabel lebar bernilai 10 dan tinggi bernilai 5, untuk x 
"</i>

<i>" 
    
"</i>

Hasil dari kode diatas:

<p align=center>
    
</p>

-----------------------------------------------------------------
## 3. Tugas2.py

Pada file Tugas2.py terdapat 3 tugas yaitu 

1. Soal 1:
   
   sdf
   
3. Soal 2:
4. Soal 3:


| Nama | Jurusan |
|------|----------|
| <img width="688" height="287" alt="image" src="https://github.com/user-attachments/assets/76dbab14-d250-4ff0-9ec0-1e1294499dee" /> | <img width="688" height="287" alt="image" src="https://github.com/user-attachments/assets/51330fa8-63f1-4a1d-b2a6-faf6a3052126" /> |
   

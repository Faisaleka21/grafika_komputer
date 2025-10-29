<h1 align=center> 🗒️ PENJELASAN DARI TIAP FILE PADA PERTEMUAN 3</h1>


## ⚙️ 1. Praktikum1.py

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

## ⚙️2.Tugas1.py

Pada file Tugas1.py terdapat 2 tugas yaitu 

1. Soal 1: 📖 <br>
      Buat program Python untuk: <br>
      a. Menerima input dua titik (x1, y1) dan (x2, y2). <br>
      b. Hitung jarak antara kedua titik. <br>
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

<blockquote><p align=justify><i>"
&nbsp;Untuk penjelasannya terdapat sebuah 4 inputan harus bernilai Integer yaitu x1,x2,y1, dan y2. Dan keempat inputan itu untuk menyimpan sebuah nilai untuk koordinat titik pertama dan kedua. Dalam kode ini : <mark>{(x1:.1f)}</mark> maksudnya nilai dari x1 akan ditampilkan dalam bentuk float dengan menampilkan 1 angka debelakang koma. Untuk menghitung jarak dengan menggunakan rumus sesuai kode diatas <mark> math.sqrt((x2-x1)**2+(y2-y1)**2) </mark>, kemudian disimpan dalam variabel hasil. <br>
&nbsp; Untuk menentukan kuadran pada titik pertama dengan menggunakan logika percabangan. Jika nilai x1 dan y1 kurang dari 0 atau negatif maka berada di Kuadran 1, jika kedua nilai x1 dan y1 positif/lebih dari 0 maka di kuadran 2, jika x1 negatif dan y1 positif maka di kuadran 3, dan sebaliknya jika x1 positif dan y1 negatif maka di kuadran 4. Jika x1 dan y1 bernilai 0 maka berada di Titik Pusat (0,0), jika x1 dan y1 nya bernilai 0 maka titik berada di sumbu X atau Y. 
"</i></p></blockquote>

Hasil dari kode diatas sbg berikut:

<p align=center>
    <img width="512" height="264" alt="image" src="https://github.com/user-attachments/assets/2ea89332-159e-4899-bdd7-978c644b24c3" />
</p>

2. Soal 2: 📖<br>
      a. Simulasikan sistem koordinat layar berukuran 10x5 piksel menggunakan simbol ".",<br>
      b. Tampilkan posisi titik (x=3, y=2) dengan karakter "X".

Berikut adalah kodenya :

    print('===== Soal 2 =====')
    # Simulasikan sistem koordinat layar berukuran 10x5 piksel menggunakan simbol ".",
    # dan tampilkan posisi titik (x=3, y=2) dengan karakter "X".
        
    lebar = 10
    tinggi = 5
    for y in range (tinggi):
        for x in range (lebar):
            if x == 3 and y == 2:
                 print('X', end='')
            else:
                 print('.', end='')
        print()
    
Penjelasan dari kode diatas:

<blockquote><p align=justify><i>"
&nbsp; Untuk penjelasannnya bahwa variabel lebar bernilai 10 dan tinggi bernilai 5. Untuk perulangan bahwa y dengan urutan bernilai sebanyak tinggi jadi tingginya berderet 0-9 dan x dengan urutan bernilai sebanyak lebar yaitu 0-4. Kemudian jika x sama dengan 3 maka menyampingnya berada pada koordinat (3,0) dan y sama dengan 2 maka koordinatnya (0,2) maka akan mencetak x.
"</i></p></blockquote>

Hasil dari kode diatas:

<p align=center>
    <img width="243" height="218" alt="image" src="https://github.com/user-attachments/assets/63ed8dd8-a39b-4d00-aeb7-c411ecf36b1d" />
</p>

-----------------------------------------------------------------
## ⚙️3. Tugas2.py

Pada file Tugas2.py terdapat 3 tugas yaitu 

1. Soal 1: 📖<br>
    a. Buat program Python yang menampilkan grid 10×10 piksel menggunakan ".". <br>
    b. Ganti piksel di posisi (4,6) menjadi "X".

Kodenya sebagai berikut: 

    print('======= Tugas 2 =======')
    print('===== Soal 1 =====')
    lebar = 10
    tinggi = 10
    
    for y in range(tinggi):
        for x in range(lebar):
            if x == 4 and y == 6:
                print('X', end='')
            else:
                print('.', end='')
        print()

Untuk penjelasannya sama dengan penjelasan pada Soal ke-2 pada Tugas1.py. Yang berbeda cuma nilainya.
   
2. Soal 2: 📖<br>
    Buat program Python yang menggambar garis dari titik (0,0) ke (5,3) dengan menghitung titik titik koordinatnya (seperti vektor).

Kodenya sebagai berikut : 



Untuk penjelasan kode diatas :

<blockquote><p align=justify><i>"
   
"</i></p></blockquote>

3. Soal 3: 📋<br>
    Buat tabel perbandingan raster dan vektor berdasarkan hasil praktikum Anda.
<div align=center>

| Raster | Vektor |
|------|----------|
| <img width="259" height="233" alt="image" src="https://github.com/user-attachments/assets/9cfa5140-e4f9-4858-b620-d901ffb2b191" /> | <img width="233" height="143" alt="image" src="https://github.com/user-attachments/assets/84727acd-4716-4de5-a2a1-441427fac8a6" /> |

</div>

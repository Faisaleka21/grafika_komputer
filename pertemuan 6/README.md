# 🎮 TransformBot  
### Media Pembelajaran Transformasi Grafika Komputer 2D

TransformBot merupakan sebuah aplikasi edukasi berbasis **Python dan PyGame** yang dibuat untuk memvisualisasikan konsep **transformasi grafika komputer 2D**, yaitu **translasi, rotasi, skala, dan refleksi**.  
Aplikasi ini dikembangkan sebagai **tugas/UAS Mata Kuliah Grafika Komputer**.

Program dirancang dalam bentuk **game 2D interaktif**, sehingga pengguna dapat memahami hubungan antara **rumus matematis** dan **perubahan visual objek secara langsung**.

---

## 📌 Tujuan Program

Tujuan dari pengembangan TransformBot adalah:
- Memvisualisasikan transformasi grafika komputer secara nyata
- Membantu pemahaman konsep matematis transformasi 2D
- Memberikan pengalaman belajar yang interaktif
- Menghubungkan teori grafika komputer dengan implementasi program

---

## 🖼️ Contoh Tampilan Aplikasi

Berikut merupakan **contoh tampilan dari aplikasi/program TransformBot**, yang menampilkan kondisi permainan pada beberapa level transformasi:


![Contoh tampilan menu awal dan level permainan](https://github.com/user-attachments/assets/7d6ca854-67f4-43d8-8dc2-d17ede218621)

![Contoh tampilan level translasi dengan platform dan player](https://github.com/user-attachments/assets/40f23ab3-6fde-405b-b6b6-9c579e8e0456)

![Contoh tampilan level rotasi dengan platform miring](https://github.com/user-attachments/assets/5896af2b-c991-4ae4-9672-213964893c08)

![Contoh tampilan level skala dengan perubahan ukuran platform](https://github.com/user-attachments/assets/ad769624-c5af-4881-bbdc-3c604ff14d61)

![Contoh tampilan level refleksi dengan cermin pemantul](https://github.com/user-attachments/assets/fa057e6c-8641-4de5-ba78-633fd1ab7dd7)

Gambar-gambar di atas menunjukkan bagaimana objek, platform, dan player berubah secara visual sesuai dengan transformasi yang diterapkan pada setiap level.

🧠 Konsep Transformasi yang Diimplementasikan

Aplikasi ini terdiri dari empat level utama, di mana setiap level merepresentasikan satu jenis transformasi grafika komputer 2D.

🔹 Level 1 – Translasi

Translasi merupakan proses perpindahan posisi objek tanpa mengubah bentuk dan orientasi.

Rumus Translasi:

x' = x + dx
y' = y + dy


Implementasi pada program:

Posisi player dan platform diubah dengan menambahkan nilai kecepatan

Platform bergerak otomatis sebagai contoh translasi

Grid koordinat ditampilkan untuk memperjelas perpindahan posisi

🔹 Level 2 – Rotasi

Rotasi merupakan transformasi yang memutar objek terhadap suatu titik pusat dengan sudut tertentu.

Matriks Rotasi 2D:

[ cosθ  -sinθ ]
[ sinθ   cosθ ]


Implementasi pada program:

Platform digambar sebagai polygon

Titik sudut platform diputar menggunakan fungsi trigonometri

Sudut rotasi dapat dikontrol oleh pengguna

🔹 Level 3 – Skala

Skala adalah transformasi untuk mengubah ukuran objek secara proporsional.

Rumus Skala:

x' = s · x
y' = s · y


Implementasi pada program:

Ukuran platform diperbesar atau diperkecil

Titik pusat objek tetap dipertahankan

Digunakan untuk membantu player mencapai tujuan

🔹 Level 4 – Refleksi

Refleksi adalah transformasi yang memantulkan objek terhadap suatu garis cermin.

Rumus Refleksi:

Refleksi vertikal:

x' = 2c - x


Refleksi horizontal:

y' = 2c - y


Implementasi pada program:

Player dipantulkan terhadap cermin vertikal atau horizontal

Posisi dan arah gerak player dibalik secara matematis

Efek visual digunakan untuk menandai proses refleksi

🎮 Kontrol Program
Tombol	Fungsi
A / D atau ← / →	Bergerak kiri / kanan
SPACE / W / ↑	Lompat
Q / E	Rotasi objek
Z / X	Skala objek
F	Refleksi
R	Reset level
N	Lanjut ke level berikutnya
ESC	Keluar dari program
⚙️ Teknologi yang Digunakan

Bahasa Pemrograman: Python

Library: PyGame

Grafika: 2D Rendering

Paradigma: Object-Oriented Programming (OOP)

▶️ Cara Menjalankan Program

Pastikan Python telah terinstal

Install PyGame:

pip install pygame


Jalankan program:

python main.py

📚 Kesimpulan

Berdasarkan hasil implementasi, TransformBot mampu memvisualisasikan konsep transformasi grafika komputer 2D secara interaktif.
Aplikasi ini membantu pengguna memahami keterkaitan antara rumus matematis dan perubahan visual objek, sehingga cocok digunakan sebagai media pembelajaran grafika komputer.

# 🏠 Mini Scene Rumah 2D – Grafika Komputer

## 👤 Informasi Proyek
- **Mata Kuliah** : Grafika Komputer  
- **Jenis Proyek** : Mini Project Grafika 2D  
- **Bahasa** : Python

---

## 📌 A. Judul Proyek
**Mini Scene Rumah 2D dengan Animasi Menggunakan Algoritma Grafika Komputer**

---

## 🎨 B. Konsep Grafika yang Digunakan
Proyek ini menampilkan sebuah **mini scene grafika 2D** berupa lingkungan rumah yang dibuat menggunakan **Python Turtle Graphics**.  
Scene terdiri dari berbagai objek grafis seperti **rumah, pohon, kincir angin, mobil, awan, matahari, bulan, bintang, dan kupu-kupu**.

Aplikasi ini bersifat **dinamis (animated)** dengan fitur:
- 🌞 Pergantian **siang dan malam**
- 🚗 Mobil bergerak dua arah di jalan
- 🌬️ Kincir angin berputar
- ☁️ Awan bergerak dari kiri ke kanan
- 🦋 Kupu-kupu terbang dengan efek skala

Tujuan utama proyek ini adalah untuk menerapkan **algoritma grafika dasar** dan **transformasi geometri 2D** dalam satu aplikasi visual interaktif.

---

## 🖼️ C. Tampilan Program

### 1️⃣ Tampilan Keseluruhan Scene
<img width="1358" height="701" alt="image" src="https://github.com/user-attachments/assets/a5d9ebee-8465-4e69-9630-17560a5524b2" />

**Penjelasan:**  
Gambar ini menunjukkan tampilan utama aplikasi yang berisi rumah, pohon, jalan, mobil, kincir angin, serta elemen langit.

---

### 2️⃣ Animasi Siang dan Malam
<img width="1362" height="701" alt="image" src="https://github.com/user-attachments/assets/b82a1d71-24b8-427a-9874-cb627c11fbc8" />

**Penjelasan:**  
Animasi ini memperlihatkan pergerakan matahari dan bulan yang menandakan pergantian waktu dari siang ke malam, termasuk munculnya bintang pada malam hari.

---

### 3️⃣ Mobil Bergerak di Jalan

<p align=center>
  
<img width="714" height="245" alt="image" src="https://github.com/user-attachments/assets/2b69dbd6-6cc0-47e9-9e79-66af3ed5ba87" />

<img width="701" height="238" alt="image" src="https://github.com/user-attachments/assets/627aaa77-2aa9-45e5-b70f-5e4f8b910784" />


</p>

**Penjelasan:**  
Mobil bergerak secara horizontal menggunakan transformasi translasi dan refleksi, serta berpindah jalur saat arah berubah.

---

### 4️⃣ Kincir Angin Berputar

<p align=center>

<img width="239" height="299" alt="image" src="https://github.com/user-attachments/assets/b139e380-f60a-488e-b1ef-2ddf4ef34805" />

<img width="195" height="281" alt="image" src="https://github.com/user-attachments/assets/e83ca706-d807-4fa3-91c8-44a77b70e9c2" />

</p>

**Penjelasan:**  
Baling-baling kincir angin berputar menggunakan transformasi rotasi terhadap titik pusat tertentu.

---

### 5️⃣ Kupu-Kupu Terbang

<p align=center>

<img width="543" height="448" alt="image" src="https://github.com/user-attachments/assets/559521f2-80cb-469b-97fc-ad3c1082ad75" />

<img width="438" height="427" alt="image" src="https://github.com/user-attachments/assets/e41f17f4-5484-4296-abbf-974085192a21" />

</p>

**Penjelasan:**  
Kupu-kupu bergerak maju-mundur menggunakan translasi dan mengalami perubahan ukuran menggunakan transformasi skala.

---

## 🧠 D. Algoritma yang Digunakan

### ✏️ 1. Algoritma Garis DDA (Digital Differential Analyzer)
Digunakan untuk:
- Membuat marka jalan
- Menggambar garis lurus secara bertahap berdasarkan perhitungan dx dan dy

---

### ⚪ 2. Algoritma Lingkaran Midpoint
Digunakan untuk:
- Jendela rumah
- Jendela kincir angin
- Elemen lingkaran lainnya

---

### 🔺 3. Algoritma Poligon (Scanline Fill)
Digunakan untuk:
- Daun pohon
- Badan mobil
- Sayap kupu-kupu

---

### 🔄 4. Transformasi Geometri 2D
Transformasi yang diterapkan meliputi:

- **Translasi** → mobil, awan, kupu-kupu  
- **Rotasi** → baling-baling kincir angin  
- **Skala** → animasi kupu-kupu  
- **Refleksi** → perubahan arah mobil

---

## ▶️ E. Cara Menjalankan Program

1. Pastikan **Python** telah terinstall.
2. Gunakan Python versi yang sudah mendukung `turtle`.
3. Siapkan folder **assets/** dengan isi:
   - `matahari.gif`
   - `bulan.gif`
   - `awan.gif`
   - `awan_kecil.gif`
4. Jalankan program dengan perintah:
   ```bash
   python minischene.py

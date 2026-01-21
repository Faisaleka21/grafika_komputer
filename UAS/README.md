# UAS Grafika Komputer  
## Simulasi Scene 3D Jembatan Modern dengan Animasi Dinamis

## 📌 Deskripsi Umum
Program ini merupakan implementasi scene grafika komputer 3D menggunakan **Python, Pygame, dan OpenGL**. Scene yang dibangun menampilkan sebuah **jembatan modern** lengkap dengan lingkungan sekitarnya, seperti kendaraan, perahu, air sungai, serta sistem **siang dan malam** yang berjalan secara dinamis berdasarkan waktu simulasi.

Program dirancang untuk menerapkan konsep-konsep utama dalam grafika komputer, antara lain transformasi 3D, hierarchical modeling, animasi berbasis waktu, pencahayaan, tekstur, serta kontrol kamera interaktif.

---

## 🖼️ Hasil Tampilan Program
Berikut merupakan hasil visualisasi dari program yang dijalankan:

![Hasil Program](https://github.com/user-attachments/assets/79f53287-4905-49be-ae34-c4e8f0c40124)

---

## 🎮 Fitur dan Hasil Implementasi

### 1. Scene 3D Jembatan
- Jembatan dimodelkan menggunakan objek dasar OpenGL seperti **cube** dan **line**.
- Struktur jembatan terdiri dari jalan utama, tiang penyangga, serta kabel.
- Sisi kiri jembatan dibuat menggunakan **refleksi geometris** (`glScalef(-1, 1, 1)`) untuk menghasilkan bentuk simetris.

---

### 2. Kendaraan Bergerak (Mobil)
- Mobil bergerak maju dan mundur di atas jembatan menggunakan animasi translasi berbasis waktu (`world_time`).
- Roda mobil dianimasikan dengan rotasi untuk memberikan kesan realistis.
- Beberapa mobil memiliki arah berlawanan yang dihasilkan melalui transformasi refleksi posisi.

---

### 3. Perahu di Bawah Jembatan
- Perahu bergerak secara horizontal di atas permukaan air.
- Asap pada cerobong perahu dianimasikan menggunakan fungsi sinus sehingga terlihat dinamis.
- Model perahu dibangun dengan kombinasi objek kubus, silinder, dan segitiga.

---

### 4. Air Sungai
- Permukaan air menggunakan **texture mapping**.
- Diberikan animasi naik-turun sederhana menggunakan fungsi sinus untuk mensimulasikan gelombang air.
- Air bersifat transparan ringan dengan blending.

---

### 5. Sistem Siang dan Malam
- Sistem siang dan malam dikendalikan oleh variabel waktu global (`world_time`).
- Langit dibuat menggunakan **sky dome** dengan dua tekstur:
  - Langit siang
  - Langit malam
- Transisi siang dan malam dilakukan secara halus menggunakan alpha blending.
- Intensitas cahaya ambient berubah sesuai waktu (lebih terang di siang hari, lebih redup di malam hari).

---

### 6. Pencahayaan (Lighting)
- Menggunakan dua sumber cahaya utama:
  - **Directional Light** sebagai matahari dan bulan
  - **Point Light** sebagai lampu jalan
- Lampu jalan hanya aktif saat kondisi malam hari.
- Pencahayaan mempengaruhi warna dan kedalaman objek sehingga meningkatkan kesan realistis.

---

### 7. Kamera Interaktif
- Kamera dapat digerakkan secara bebas menggunakan keyboard.
- Mendukung pergerakan maju, mundur, ke samping, naik, dan turun.
- Sudut pandang kamera dapat diputar untuk melihat scene dari berbagai arah.

---

## 🧠 Konsep Grafika Komputer yang Diterapkan
- Transformasi 3D (translasi, rotasi, skala, refleksi)
- Hierarchical modeling
- Animasi berbasis waktu (*time-based animation*)
- Texture mapping
- Pencahayaan dan shading
- Alpha blending (transparansi)
- Kamera perspektif (3D view)

---

## ✅ Kesimpulan
Program ini berhasil menampilkan sebuah scene 3D interaktif yang menggabungkan berbagai konsep grafika komputer secara terpadu. Dengan adanya animasi objek, sistem siang dan malam, serta kontrol kamera, program ini mampu memberikan visualisasi lingkungan jembatan modern yang dinamis dan realistis sesuai dengan tujuan tugas UAS Grafika Komputer.

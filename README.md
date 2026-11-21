# Dashboard Sistem Pendukung Keputusan (SPK) - Metode SMART

Aplikasi web **Sistem Pendukung Keputusan (SPK)** interaktif berbasis **Single Page Dashboard** yang mengimplementasikan metode **SMART (Simple Multi-Attribute Rating Technique)**.

Dibangun menggunakan **Python**, **Streamlit**, **Pandas**, **NumPy**, dan **Plotly** dengan standar desain UI/UX modern, minimalis, dan profesional.

---

## 🎨 Karakteristik Desain & Tema
- **Warna Utama**: Hijau Forest (`#15803D`)
- **Background**: Putih Bersih (`#FFFFFF`)
- **Aksen / Secondary**: Hijau Muda Segar (`#DCFCE7`)
- **Warna Teks**: Gelap Elegan (`#1E293B`)
- **Struktur Halaman**: Single Vertical Page (Semua input, kalkulasi langkah demi langkah, dan hasil berada dalam satu halaman tanpa navigasi sidebar/multi-page).

---

## 📐 6 Bagian Utama Dashboard

1. **01. Data Alternatif**: Manajemen opsi yang dievaluasi (Tambah, edit langsung pada tabel, hapus, validasi kode unik).
2. **02. Data Kriteria**: Manajemen kriteria dengan klasifikasi **Benefit** (semakin tinggi semakin baik) dan **Cost** (semakin rendah semakin baik).
3. **03. Pembobotan Kriteria**: Pengaturan tingkat kepentingan kriteria ($w_j > 0$). Bobot fleksibel dan tidak wajib berjumlah 100 karena dinormalisasi otomatis.
4. **04. Normalisasi Bobot**: Perhitungan bobot relatif ($W_j = w_j / \sum w_k$) lengkap dengan rumus LaTeX dan substitusi angka otomatis.
5. **05. Proses Perhitungan SMART**:
   - **A. Input Matriks Penilaian**: Matriks nilai awal ($C_{out}$) dengan pendeteksian otomatis nilai ekstrem ($C_{min}$ dan $C_{max}$).
   - **B. Perhitungan Nilai Utility ($U_{ij}$)**: Transformasi ke skala 0 – 1 berdasarkan kriteria Benefit atau Cost.
   - **C. Perhitungan Nilai Akhir ($V_i$)**: Perkalian matriks utility dengan bobot normalisasi ($V_i = \sum W_j \times U_{ij}$).
6. **06. Hasil Akhir & Rekomendasi Keputusan**: 
   - Banner pemenang (Peringkat 1) dengan skor akhir.
   - Tabel ranking lengkap beserta keterangan rekomendasi.
   - Tombol download hasil keputusan ke file `.CSV`.
   - Visualisasi Bar Chart interaktif (Plotly) dan Radar Chart profil kriteria.

---

## 🚀 Cara Menjalankan Aplikasi

1. Pastikan dependensi telah terinstal:
   ```bash
   pip install -r requirements.txt
   ```

2. Jalankan dashboard Streamlit:
   ```bash
   streamlit run app.py
   ```

3. Buka browser pada alamat lokal yang ditampilkan (biasanya `http://localhost:8501`).

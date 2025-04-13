# Studi Komparatif Model Machine Learning untuk Klasifikasi Warna RGB Daun Selada

## Deskripsi Proyek
Penelitian ini bertujuan untuk membandingkan kinerja beberapa model machine learning dalam mengklasifikasikan warna daun selada hidroponik (*Lactuca sativa L.*) yang dipengaruhi oleh pemberian pupuk Silika Quantum Dots (Si-QDs). Warna daun diukur menggunakan sensor Arduino Uno TCS34725 dalam bentuk data RGB, yang kemudian digunakan sebagai fitur untuk klasifikasi.

## Ruang Lingkup Penelitian
### Dataset
- **Total Data**: 1.441 data dari 4 kelas (Kelas 0, 1, 2, 3).
- **Fitur Awal**: R (Red), G (Green), B (Blue).
- **Statistik Fitur**:  
  - **R**: Mean 147.11, Std Dev 7.78.  
  - **G**: Mean 149.73, Std Dev 7.15.  
  - **B**: Mean 114.23, Std Dev 16.19.  
- **Distribusi Data**: Kelas relatif seimbang.

### Model Machine Learning
- Random Forest (RF).
- XGBoost.
- Artificial Neural Network (ANN).
- Adaptive Neuro-Fuzzy Inference System (ANFIS).

### Tahapan Penelitian
1. **Preprocessing**:
   - Transformasi ruang warna (HSV, Lab).
   - Perhitungan rasio warna (R/G, G/B).
2. **Klasifikasi**:
   - Implementasi dan pelatihan model.
3. **Optimasi**:
   - Hyperparameter tuning menggunakan Grid Search atau metode lainnya.
4. **Evaluasi**:
   - Menggunakan metrik akurasi, precision, recall, F1-score, dan ROC-AUC.

## Tujuan
Menentukan model terbaik dalam mengklasifikasikan warna daun selada berdasarkan data RGB untuk mengevaluasi pengaruh pemberian pupuk Silika Quantum Dots.

## Struktur File
- `data/`: Dataset penelitian.
- `src/`: Implementasi kode untuk preprocessing, training, dan evaluasi model.
- `notebooks/`: Eksplorasi awal dan analisis dataset.
- `results/`: Hasil klasifikasi dan evaluasi model.
- `README.md`: Dokumentasi singkat proyek (file ini).

## Cara Penggunaan
1. Pastikan semua dependensi telah terpasang (Python, library machine learning, dsb).
2. Jalankan preprocessing untuk mengubah data mentah menjadi format siap pakai.
3. Lakukan pelatihan model dengan menjalankan skrip di folder `src/`.
4. Evaluasi hasil klasifikasi dan analisis performa model.

## Teknologi yang Digunakan
- **Hardware**: Arduino Uno TCS34725 Sensor.
- **Software**: Python, Scikit-learn, TensorFlow/PyTorch, MATLAB (untuk ANFIS).
- **Library**: Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, XGBoost, TensorFlow/PyTorch.

## Penulis
Penelitian ini dilakukan oleh [Nama Anda], mahasiswa semester akhir Program Studi Informatika, sebagai bagian dari penyelesaian tugas akhir.

## Lisensi
Proyek ini dibuat untuk keperluan akademik dan penelitian. Data dan kode dapat digunakan dengan izin dari penulis.
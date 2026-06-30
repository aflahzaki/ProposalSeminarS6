# PANDUAN SIDANG PROPOSAL
## Analisis Preskriptif Kualitas Air Menggunakan Natural Gradient Boosting dan Counterfactual Explanations

**Nama:** Aflah Zaki Siregar | **NIM:** 103062300095  
**Program Studi:** S1 Teknologi Informasi, Fakultas Informatika, Universitas Telkom  
**Tahun:** 2026

---

## DAFTAR ISI

1. [Ringkasan Penelitian](#1-ringkasan-penelitian)
2. [Konteks dan Motivasi](#2-konteks-dan-motivasi)
3. [Research Gap dan Rumusan Masalah](#3-research-gap-dan-rumusan-masalah)
4. [Teori NGBoost](#4-teori-ngboost)
5. [Teori DiCE](#5-teori-dice-diverse-counterfactual-explanations)
6. [Alur Metodologi](#6-alur-metodologi)
7. [Justifikasi Urutan Preprocessing](#7-justifikasi-urutan-preprocessing)
8. [Metrik Evaluasi](#8-metrik-evaluasi)
9. [Dataset](#9-dataset)
10. [Kontribusi dan Novelitas](#10-kontribusi-dan-novelitas)
11. [Pertanyaan Penguji dan Jawaban](#11-pertanyaan-penguji-dan-jawaban)
12. [Referensi Kunci](#12-referensi-kunci)

---

## 1. RINGKASAN PENELITIAN

### Inti Penelitian (Elevator Pitch - 30 detik)

> Penelitian ini mengintegrasikan NGBoost (model probabilistik) dengan DiCE (counterfactual explanations) untuk menghasilkan **rekomendasi preskriptif** perbaikan kualitas air. Bukan hanya memprediksi "layak/tidak layak", tapi juga memberitahu **berapa banyak** parameter harus diubah agar air menjadi layak, lengkap dengan **tingkat kepercayaan** prediksi.

### Kata Kunci Penting
- **Analisis Preskriptif**: Tidak hanya menjelaskan MENGAPA (diagnostik), tapi memberikan HOW (bagaimana memperbaiki)
- **Prediksi Probabilistik**: Output berupa distribusi probabilitas, bukan label keras
- **Counterfactual Explanations**: "Jika pH diubah dari 5.0 menjadi 7.0, maka air menjadi layak"
- **Actionable Recourse**: Rekomendasi yang bisa ditindaklanjuti secara operasional

### Hipotesis
1. NGBoost mampu menghasilkan performa klasifikasi **setara atau lebih baik** dari baseline deterministik (XGBoost, RF) dengan kalibrasi probabilistik yang superior
2. DiCE mampu menghasilkan rekomendasi counterfactual dengan **validity rate > 90%** dan **feasibility rate > 85%** sesuai constraint domain kualitas air

---

## 2. KONTEKS DAN MOTIVASI

### Mengapa Kualitas Air?
- WHO, UNICEF, World Bank (2022): 74% populasi dunia (5,8 miliar orang) sudah mengakses air minum aman, namun **2 miliar orang belum** memiliki akses layanan air minum yang dikelola secara aman
- Di Indonesia, akses air minum aman baru mencapai 11,8% (BPS, 2020)
- Parameter fisikokimia air bersifat **controllable dan actionable** (bisa diintervensi melalui koagulasi, filtrasi, aerasi, disinfeksi)

### Mengapa Machine Learning?
- Data parameter fisikokimia kompleks (multivariate, non-linear relationships)
- Pendekatan tradisional (threshold-based) tidak mampu menangkap interaksi antar parameter
- ML dapat memberikan prediksi otomatis dan scalable

### Mengapa Probabilistik (bukan Deterministik)?
- Model deterministik (XGBoost, RF) hanya output: "layak" / "tidak layak" tanpa confidence
- Operator butuh tahu **seberapa yakin** model terhadap prediksinya
- Pada zona borderline (probabilitas ~50%), keputusan perlu lebih hati-hati
- NGBoost memberikan distribusi probabilitas lengkap

### Mengapa Preskriptif (bukan hanya Prediktif)?
- Prediktif: "Air ini TIDAK layak" (lalu apa?)
- Diagnostik/SHAP: "pH dan Turbidity yang berpengaruh" (tapi berapa harus diubah?)
- **Preskriptif/DiCE**: "Ubah pH dari 5.2 menjadi 7.0 dan Turbidity dari 5.1 menjadi 3.5, maka air menjadi layak" (ACTIONABLE!)

---

## 3. RESEARCH GAP DAN RUMUSAN MASALAH

### Tiga Research Gap

| No | Gap | Bukti dari Literatur |
|----|-----|---------------------|
| 1 | **Ketiadaan estimasi ketidakpastian** pada model ML deterministik di domain kualitas air | Aslam et al., Park et al., Al Bataineh et al. - semua deterministik |
| 2 | **Ketiadaan rekomendasi preskriptif** yang actionable | SHAP/LIME hanya diagnostik (menjelaskan WHY, bukan HOW) |
| 3 | **Counterfactual belum diterapkan** pada domain kualitas air | Nnadi (mental health), Dastile (credit scoring), Lenatti (penyakit kronis) - semua di luar air |

### Tiga Rumusan Masalah (masing-masing menjawab 1 gap)

1. **RM1 (menjawab Gap 1):** Bagaimana performa NGBoost dalam memodelkan kelayakan air secara probabilistik dibandingkan baseline deterministik (XGBoost, RF) berdasarkan metrik klasifikasi dan kalibrasi?

2. **RM2 (menjawab Gap 2):** Bagaimana implementasi DiCE pada model NGBoost untuk menghasilkan rekomendasi preskriptif yang mengubah status air dari tidak layak menjadi layak?

3. **RM3 (menjawab Gap 3):** Sejauh mana kualitas rekomendasi counterfactual memenuhi properti validity, proximity, sparsity, diversity, feasibility, serta bagaimana trade-off antar properti tersebut?

### Tiga Tujuan (sejajar dengan RM)

1. Menganalisis performa NGBoost secara komparatif terhadap baseline dari metrik klasifikasi (Accuracy, Precision, Recall, F1) dan kalibrasi (NLL, ECE)
2. Mengimplementasikan DiCE pada model NGBoost untuk menghasilkan rekomendasi perubahan parameter fisikokimia
3. Menganalisis kualitas counterfactual berdasarkan 5 properti termasuk trade-off dalam constraint domain

---
## 4. TEORI NGBoost

### Apa itu NGBoost?
Natural Gradient Boosting (NGBoost) adalah algoritma gradient boosting yang memodelkan **distribusi penuh** probabilitas sebagai output, bukan hanya point estimate. Diperkenalkan oleh Duan et al. (2020) dari Stanford.

### Komponen Utama NGBoost

#### A. Distribusi Output: Bernoulli (untuk klasifikasi biner)
- Parameter: mu (probabilitas kelas positif/layak)
- P(y=1|x) = mu, P(y=0|x) = 1 - mu
- mu diperoleh dari fungsi sigmoid: mu = sigma(f(x))
- Uncertainty dihitung sebagai: mu * (1 - mu)
  - Jika mu = 0.5 -> uncertainty maksimal
  - Jika mu = 0.99 -> uncertainty sangat rendah (yakin layak)

#### B. Scoring Rule: Negative Log-Likelihood (NLL)
- Loss function: L(theta) = -E[log P_theta(y|x)]
- Untuk Bernoulli: NLL = -(y*log(mu) + (1-y)*log(1-mu))
- Semakin rendah NLL, semakin baik kalibrasi model

#### C. Natural Gradient (Kunci Pembeda NGBoost!)

**Masalah dengan gradient biasa:**
- Parameter distribusi berada di ruang Riemannian (bukan Euclidean)
- Gradient biasa tidak memperhatikan geometri ruang probabilitas
- Langkah update bisa terlalu besar di satu arah, terlalu kecil di arah lain

**Solusi: Natural Gradient**
- Natural Gradient = F^(-1) * gradient_biasa
- F = Fisher Information Matrix (mengukur "kelengkungan" ruang distribusi)
- Untuk Bernoulli: F = 1/(mu*(1-mu))
- Natural Gradient memastikan update yang **invariant** terhadap parameterisasi ulang

**Analogi sederhana:**
> Bayangkan Anda berjalan di permukaan bola. Gradient biasa menunjuk ke arah yang benar di peta datar, tapi di permukaan bola bisa menyesatkan. Natural Gradient memperhitungkan kelengkungan bola sehingga Anda selalu berjalan ke arah yang benar.

#### D. Update Rule
- theta_(m+1) = theta_m - eta * F^(-1) * gradient
- eta = learning rate
- Dilakukan iteratif (boosting) dengan base learner (Decision Tree dangkal)

#### E. Base Learner: Decision Tree Regressor
- max_depth = 3-5 (dangkal, mencegah overfitting)
- Memprediksi parameter distribusi, BUKAN label
- Setiap tree memperbaiki estimasi parameter distribusi

### Mengapa NGBoost, Bukan Alternatif Lain?

| Alternatif | Kelemahan | Keunggulan NGBoost |
|------------|-----------|-------------------|
| Bayesian Neural Network (BNN) | Kompleksitas tinggi, sulit di-tune untuk data tabular kecil | Sederhana, efisien |
| MC Dropout | Hanya approximate uncertainty | Exact parametric uncertainty |
| Deep Learning | Inferior pada data tabular (Grinsztajn 2022) | Gradient boosting superior untuk tabular |
| XGBoost/RF biasa | Tidak ada estimasi uncertainty | Full distribusi probabilitas |

### Konfigurasi NGBoost untuk Penelitian Ini
- **Distribusi**: Bernoulli (binary) / k_categorical(5) (Canada multi-class)
- **Base learner**: DecisionTreeRegressor(max_depth=4)
- **n_estimators**: Tuned via Grid Search (100-500)
- **learning_rate**: Tuned (0.01-0.1)
- **minibatch_frac**: Tuned (0.5-1.0)
- **col_sample**: 0.8
- **Early stopping**: Pada validation set

### Catatan Penting tentang "Probabilistik"
> "Probabilistik" di sini BUKAN Bayesian inference penuh. Yang dikuantifikasi adalah **aleatoric uncertainty** (ketidakpastian data), direpresentasikan sebagai mu*(1-mu) dari distribusi Bernoulli. Bukan epistemic uncertainty (ketidakpastian model).

---

## 5. TEORI DiCE (Diverse Counterfactual Explanations)

### Apa itu Counterfactual Explanation?
Penjelasan dalam bentuk: "Jika fitur X diubah menjadi nilai Y, maka prediksi model akan berubah dari kelas A ke kelas B."

**Contoh konkret di domain kualitas air:**
> "Jika pH dinaikkan dari 5.2 menjadi 7.0 dan Turbidity diturunkan dari 5.1 menjadi 3.5, maka status air berubah dari **Tidak Layak** menjadi **Layak** (confidence: 87%)"

### Apa itu DiCE?
Framework dari Microsoft Research (Mothilal et al., 2020) untuk menghasilkan **beberapa** counterfactual yang diverse dan feasible.

### Lima Properti Kunci Counterfactual (Dastile & Celik, 2024)

| Properti | Definisi | Mengapa Penting |
|----------|----------|-----------------|
| **Validity** | CF berhasil mengubah prediksi ke kelas target | Rekomendasi harus berhasil |
| **Proximity** | Jarak CF dengan instance asli minimal | Perubahan sesedikit mungkin |
| **Sparsity** | Jumlah fitur yang diubah minimal | Praktis diimplementasikan |
| **Diversity** | CF yang dihasilkan bervariasi | Memberikan alternatif pilihan |
| **Feasibility** | CF memenuhi constraint domain | Realistis secara operasional |

### Fungsi Optimasi DiCE (dipahami secara konseptual)

DiCE meminimalkan:
```
L = L_validity + lambda1 * L_proximity + lambda2 * L_diversity
subject to: permitted_range constraints
```

- L_validity: Apakah prediksi berubah ke kelas target?
- L_proximity: Seberapa dekat CF dengan instance asli?
- L_diversity: Seberapa berbeda antar-CF yang dihasilkan?
- permitted_range: Batasan nilai fitur (WHO/Permenkes)

### Metode Optimasi: Gradient-based
- DiCE menggunakan gradient dari model untuk mencari perubahan optimal
- Kompatibel dengan model yang memiliki API predict_proba (termasuk NGBoost melalui wrapper)

### Mengapa DiCE, Bukan Framework CF Lain?

| Framework | Kelemahan | Keunggulan DiCE |
|-----------|-----------|-----------------|
| Wachter et al. (2017) | Hanya 1 CF per instance | Multiple diverse CFs |
| FACE | Kurang fleksibel untuk domain-specific constraints | permitted_range untuk regulasi |
| Growing Spheres | Tidak multi-objective optimization | Optimize validity + proximity + diversity |
| MUCH | Dirancang spesifik multi-class | DiCE bisa binary dan multi-class |

### Konfigurasi DiCE untuk Penelitian Ini

**Dataset Kadiwal (Binary):**
- Arah: Tidak Layak (0) -> Layak (1)
- total_CFs: 4-5 per instance
- method: 'gradient'
- features_to_vary: semua 9 fitur (semuanya actionable/controllable)

**Dataset Canada (Multi-class, 5 kelas):**
- Grouping binary: {Marginal, Poor} = "Unacceptable", {Excellent, Good, Fair} = "Acceptable"
- Arah: Unacceptable -> Acceptable
- Menggunakan NGBoostMultiWrapper yang memetakan 5-class ke binary

### Constraint 2 Skenario

**Skenario 1 - GENERATION (WHO Guidelines 2022):**
Digunakan sebagai permitted_range saat DiCE **membangkitkan** counterfactual.
- Lebih loose (rentang lebih lebar)
- Sesuai distribusi data
- Tujuan: Memungkinkan DiCE menemukan solusi feasible

| Parameter | Constraint WHO |
|-----------|---------------|
| pH | 6.5 - 8.5 |
| Hardness | 0 - 500 mg/L |
| Solids/TDS | 0 - 1000 mg/L |
| Chloramines | 0 - 3 mg/L |
| Sulfate | 0 - 500 mg/L |
| Conductivity | 181 - 753 uS/cm (data-driven P5-P95) |
| Organic_carbon | 2.2 - 28.3 mg/L (data-driven P5-P95) |
| Trihalomethanes | 0 - 200 ug/L |
| Turbidity | 0 - 4 NTU |

**Skenario 2 - EVALUASI (Permenkes No. 2/2023):**
Digunakan untuk **mengevaluasi** apakah CF yang dihasilkan memenuhi regulasi Indonesia.
- Lebih ketat
- Hanya 4 dari 9 parameter ada di Permenkes Tabel Wajib

| Parameter | Constraint Permenkes |
|-----------|---------------------|
| pH | 6.5 - 8.5 |
| TDS (Solids) | < 300 mg/L |
| Turbidity | < 3 NTU |
| Chloramines (Sisa Khlor) | 0.2 - 0.5 mg/L |
| Lainnya (5 fitur) | Menggunakan WHO (tidak ada di Permenkes) |

**Implikasi penting:**
- Feasibility rendah terhadap Permenkes = **TEMUAN PENELITIAN** bahwa dataset benchmark tidak sepenuhnya representatif terhadap standar Indonesia
- Kerangka akan lebih optimal pada data PDAM yang realistis

---
## 6. ALUR METODOLOGI

### Diagram Alur Lengkap (Urutan KRITIS - harus dihafal!)

```
[Dataset] -> [EDA] -> [Median Imputation (SELURUH data)]
    -> [MinMax Scaling (SELURUH data)]
    -> [Stratified Split 70/15/15]
    -> [SMOTE-ENN (HANYA train, KONDISIONAL)]
    -> [Training NGBoost (parameter awal)]
    -> [Training Baseline (XGBoost, RF)]
    -> [Hyperparameter Tuning (Grid Search + 5-fold CV)]
    -> [Re-training dengan parameter optimal]
    -> [Evaluasi (Klasifikasi + Kalibrasi)]
    -> [Analisis Kalibrasi (Calibration Curves)]
    -> [Prediksi Kualitas Air]
    -> [DiCE Setup (WHO constraints)]
    -> [Generate Counterfactual (Not Potable -> Potable)]
    -> [Evaluasi Constraint (WHO + Permenkes)]
    -> [Rekomendasi Preskriptif]
    -> [Evaluasi CF (5 properti)]
```

### Detail Setiap Tahap

#### 6.1 Exploratory Data Analysis (EDA)
- Pemeriksaan struktur data, tipe fitur
- Distribusi setiap parameter (histogram, boxplot)
- Identifikasi missing values (pH: 14.98%, Sulfate: 23.84%, Trihalomethanes: 4.94%)
- Analisis korelasi antar fitur
- Class distribution (Kadiwal: 39% Potable, 61% Not Potable)

#### 6.2 Median Imputation (pada SELURUH data)
- Mengisi missing values dengan median dari fitur tersebut
- Median dipilih karena robust terhadap outlier
- Distribusi fisikokimia umumnya skewed, bukan normal
- Dilakukan pada **seluruh data** sebelum split (mengikuti Al Bataineh et al. 2026)
- Justifikasi: Imputasi bersifat **unsupervised** (tidak menggunakan label target)

#### 6.3 MinMax Scaling (pada SELURUH data)
- Normalisasi ke rentang [0, 1]: x_scaled = (x - x_min) / (x_max - x_min)
- Diperlukan karena fitur memiliki skala berbeda (pH: 0-14, Solids: 0-60000)
- Dilakukan pada **seluruh data** sebelum split (mengikuti Al Bataineh et al. 2026)
- SMOTE-ENN sensitif terhadap skala (nearest neighbor-based), jadi scaling SEBELUM SMOTE

#### 6.4 Stratified Split (70/15/15)
- 70% Training, 15% Validation, 15% Test
- Stratified: proporsi kelas dipertahankan di setiap subset
- Validasi untuk: early stopping, hyperparameter tuning
- Test untuk: evaluasi final (tidak tersentuh sampai evaluasi)

#### 6.5 SMOTE-ENN (Kondisional, HANYA pada train)
- **SMOTE**: Synthetic Minority Over-sampling (membuat sampel sintetik kelas minoritas)
- **ENN**: Edited Nearest Neighbor (menghapus noise di batas keputusan)
- Diterapkan **hanya pada data train** (mencegah data leakage)
- **Kondisional**: Bandingkan F1 dengan dan tanpa SMOTE-ENN. Jika tidak ada improvement, gunakan data asli
- Referensi: Zhu et al. (2023)

#### 6.6 Training NGBoost (Parameter Awal)
- n_estimators=300, lr=0.05, minibatch_frac=0.8, col_sample=0.8, max_depth=4
- Early stopping pada validation set
- Distribusi: Bernoulli (Kadiwal) / k_categorical(5) (Canada)

#### 6.7 Training Baseline
- XGBoost: Gradient boosting deterministik
- Random Forest: Ensemble voting
- Dilatih pada data yang IDENTIK dengan NGBoost

#### 6.8 Hyperparameter Tuning (Grid Search + 5-fold CV)

**NGBoost Grid:**
- n_estimators: [100, 200, 300, 500]
- learning_rate: [0.01, 0.02, 0.05, 0.1]
- minibatch_frac: [0.5, 0.8, 1.0]
- max_depth: [3, 4, 5, 8]

**XGBoost Grid:**
- n_estimators: [100, 200, 300, 500]
- max_depth: [3, 4, 5, 6, 8]
- learning_rate: [0.01, 0.05, 0.1]
- subsample: [0.7, 0.8, 0.9]

**Random Forest Grid:**
- n_estimators: [100, 200, 300, 500]
- max_depth: [None, 10, 15, 20]
- min_samples_split: [2, 5, 10]

Referensi: Nnadi et al. (2026), Zhu et al. (2023), Duan et al. (2020)

#### 6.9 Evaluasi
- Bandingkan performa SEBELUM vs SESUDAH tuning
- Metrik klasifikasi + kalibrasi (detail di Bagian 8)
- McNemar's test untuk signifikansi statistik

#### 6.10 DiCE Generation
- Pilih sample Not Potable dengan berbagai confidence level
- Generate 4-5 counterfactual per instance
- Constraint: WHO Guidelines (generation), Permenkes (evaluation)

---

## 7. JUSTIFIKASI URUTAN PREPROCESSING

### Referensi Utama: Al Bataineh et al. (2026) Algorithm 3

**Urutan yang digunakan:** Impute -> Scale -> Split -> SMOTE (kondisional pada train)

Ini BERBEDA dari urutan konvensional yang biasa diajarkan (Split -> Impute -> Scale).

### Mengapa Impute Sebelum Split?
1. **Median imputation bersifat unsupervised** - tidak menggunakan label target
2. Konsistensi nilai imputasi di seluruh subset
3. Jika impute setelah split, median train bisa berbeda dari median seluruh populasi
4. Al Bataineh et al. (2026) Step 1.1: "Handle missing values using median imputation"

### Mengapa Scale Sebelum Split?
1. **MinMax juga unsupervised** - hanya menggunakan min/max fitur, bukan label
2. SMOTE-ENN (langkah berikutnya) berbasis nearest neighbor yang sensitif terhadap skala
3. Jika scale setelah split, min/max dari train mungkin tidak mencakup range test
4. Al Bataineh et al. (2026) Step 1.2: "Normalize all features to range [0,1]"
5. Al Bataineh et al. (2026) Step 1.3: "Split D" (split SETELAH normalize)

### Mengapa SMOTE Hanya Pada Train?
1. SMOTE menggunakan label target (supervised) -> HARUS setelah split
2. Jika SMOTE sebelum split, sampel sintetik bisa masuk ke test set -> **DATA LEAKAGE**
3. Data test harus representatif dari distribusi asli (termasuk class imbalance)

### Referensi Pendukung
- **Al Bataineh et al. (2026)**: Algorithm 3 secara eksplisit preprocessing -> split
- **Patel et al. (2022)**: Juga melakukan imputation dan scaling pada seluruh dataset sebelum pembagian

### Jawaban Jika Ditanya "Bukankah ini Data Leakage?"
> "Tidak, karena median imputation dan MinMax scaling bersifat UNSUPERVISED - tidak menggunakan informasi label target (y). Data leakage terjadi ketika informasi dari label test 'bocor' ke proses training. Transformasi yang hanya menggunakan distribusi fitur (x) tanpa label tidak menyebabkan leakage. Ini mengikuti Al Bataineh et al. (2026) yang di-publish di IEEE JSTARS dan telah melalui peer review."

---

## 8. METRIK EVALUASI

### A. Metrik Klasifikasi (Menjawab RM1)

| Metrik | Rumus | Interpretasi |
|--------|-------|--------------|
| **Accuracy** | (TP+TN) / (TP+TN+FP+FN) | Proporsi prediksi benar keseluruhan |
| **Precision** | TP / (TP+FP) | Dari yang diprediksi positif, berapa yang benar? |
| **Recall** | TP / (TP+FN) | Dari yang sebenarnya positif, berapa yang terdeteksi? |
| **F1-Score** | 2*P*R / (P+R) | Harmonic mean precision dan recall |
| **AUC-ROC** | Area under ROC curve | Kemampuan diskriminasi model pada berbagai threshold |

### B. Metrik Kalibrasi Probabilistik (Menjawab RM1)

| Metrik | Rumus | Interpretasi |
|--------|-------|--------------|
| **NLL** | -(1/N) * SUM[y*log(mu) + (1-y)*log(1-mu)] | Seberapa baik distribusi model sesuai label aktual. **Semakin rendah semakin baik.** |
| **ECE** | SUM(abs(Bm)/N) * abs(acc - conf) | Selisih antara confidence model dengan akurasi aktual per bin. **Semakin rendah semakin baik.** |

**Penjelasan ECE:**
- Bagi prediksi ke dalam bin berdasarkan confidence (0-0.1, 0.1-0.2, dst.)
- Di setiap bin, hitung akurasi aktual vs rata-rata confidence
- Model terkalibrasi sempurna: jika confidence 80%, maka akurasi aktual juga 80%
- NGBoost diharapkan memiliki ECE lebih rendah dari XGBoost/RF

### C. Metrik Counterfactual (Menjawab RM2 dan RM3)

| Metrik | Rumus | Interpretasi |
|--------|-------|--------------|
| **Validity** | (CF yang berubah kelas) / (total CF) | Efektivitas rekomendasi. Target: > 90% |
| **Proximity** | (1/k) * SUM distance(x, cf_i) | Seberapa minimal perubahan. **Semakin rendah semakin baik.** |
| **Sparsity** | (1/k) * SUM (fitur berubah / total fitur d) | Proporsi fitur yang diubah. **Semakin rendah semakin baik.** |
| **Diversity** | (1/k(k-1)) * SUM distance(cf_i, cf_j) | Variasi antar-CF. **Semakin tinggi semakin baik.** |
| **Feasibility** | (CF dalam range constraint) / (total CF) | Kelayakan operasional. Target: > 85% |

### Trade-off Antar Properti (PENTING untuk RM3!)
- **Proximity vs Diversity**: CF yang sangat dekat dengan original cenderung mirip satu sama lain (rendah diversity)
- **Validity vs Feasibility**: CF yang valid (berhasil ubah kelas) mungkin melanggar constraint
- **Sparsity vs Validity**: Mengubah sedikit fitur lebih sulit menghasilkan CF yang valid
- Penelitian ini menganalisis trade-off tersebut sebagai kontribusi ke RM3

---
## 9. DATASET

### Dataset Utama: Water Potability (Kadiwal, Kaggle)

| Aspek | Detail |
|-------|--------|
| Sumber | Kaggle (CC0: Public Domain) |
| Jumlah sampel | 3.276 |
| Jumlah fitur | 9 parameter fisikokimia |
| Target | Potability (0 = Tidak Layak, 1 = Layak) |
| Tipe | Klasifikasi biner |
| Class balance | 39% Potable, 61% Not Potable (imbalanced) |
| Missing values | pH (14.98%), Sulfate (23.84%), Trihalomethanes (4.94%) |
| Tingkat kesulitan | Menantang (~70% accuracy pada literature) |
| Referensi akademik | 99+ paper Scopus termasuk Patel et al. (2022), Park et al. (2022) |

**9 Fitur:**
1. **pH** (0-14): Keasaman/kebasaan air
2. **Hardness** (mg/L): Konsentrasi kalsium dan magnesium
3. **Solids/TDS** (mg/L): Total padatan terlarut
4. **Chloramines** (mg/L): Desinfektan dari klorin + amonia
5. **Sulfate** (mg/L): Ion sulfat terlarut
6. **Conductivity** (uS/cm): Kemampuan menghantarkan listrik
7. **Organic_carbon** (mg/L): Karbon organik total
8. **Trihalomethanes** (ug/L): By-product klorinasi
9. **Turbidity** (NTU): Kekeruhan air

**Justifikasi penggunaan seluruh data:**
- Seluruh record memiliki variabel target (Potability) yang valid
- Tidak ada record duplikat atau record dengan seluruh fitur missing
- Record dengan missing parsial ditangani via Median Imputation

### Dataset Validasi: Canada Water Quality (Nature.com/Scientific Data)

| Aspek | Detail |
|-------|--------|
| Sumber | Repositori Nature.com (Scientific Data/Figshare) |
| Jumlah sampel | 3.949 |
| Jumlah fitur | 8 parameter fisikokimia |
| Target | CCME_WQI (5 kelas: Excellent, Good, Fair, Marginal, Poor) |
| Tipe | Klasifikasi multi-class |
| Class balance | Excellent: 1401, Good: 2061, Fair: 234, Marginal: 190, Poor: 63 |
| Missing values | 0 (tidak ada) |
| Tingkat kesulitan | Relatif mudah (~98% accuracy) |

**8 Fitur:**
1. Ammonia (mg/L)
2. Biochemical Oxygen Demand / BOD (mg/L)
3. Dissolved Oxygen / DO (mg/L)
4. Orthophosphate (mg/L)
5. pH (pH units)
6. Temperature (Celsius)
7. Nitrogen (mg/L)
8. Nitrate (mg/L)

**Fungsi dataset Canada:**
- Validasi **generalizability** kerangka kerja NGBoost+DiCE
- Menunjukkan bahwa pipeline bekerja pada dataset berbeda
- Multi-class (5 kelas) vs binary (2 kelas) pada Kadiwal
- Untuk DiCE: grouping binary {Marginal, Poor} -> "Unacceptable", {Excellent, Good, Fair} -> "Acceptable"

### Perbandingan Kedua Dataset

| Aspek | Kadiwal | Canada |
|-------|---------|--------|
| Klasifikasi | Binary | Multi-class (5) |
| Difficulty | Challenging (~70% acc) | Easier (~98% acc) |
| Missing values | Ada (3 fitur) | Tidak ada |
| Class imbalance | Moderat (61:39) | Severe di kelas minor |
| Lokasi | Tidak spesifik | Kanada |
| Peran | Dataset utama | Dataset validasi |

### Posisi Dataset: Benchmark, Bukan Representasi Lapangan
> "Dataset ini diposisikan sebagai **benchmark validasi metodologi**, bukan representasi kondisi air di wilayah tertentu. Kerangka NGBoost+DiCE yang dikembangkan bersifat transferable ke data PDAM/laboratorium nyata."

---

## 10. KONTRIBUSI DAN NOVELITAS

### Novelitas Utama (Statement Ringkas)
> "Penelitian ini merupakan **first practical implementation** yang mengintegrasikan NGBoost sebagai model probabilistik dengan DiCE sebagai framework preskriptif pada domain kualitas air, dengan feasibility constraints berbasis regulasi nasional (Permenkes No. 2/2023) dan internasional (WHO 2022)."

### Kontribusi Spesifik

1. **Kontribusi Metodologis:**
   - Integrasi NGBoost + DiCE yang belum pernah dilakukan di domain air
   - Two-tier constraint evaluation (WHO generation + Permenkes evaluation)
   - Binary grouping untuk multi-class counterfactual (Canada dataset)

2. **Kontribusi Teknis:**
   - NGBoostWrapper untuk kompatibilitas DiCE
   - Pipeline preprocessing yang mengikuti Al Bataineh et al. (2026)
   - Conditional SMOTE-ENN (hanya jika improve performance)

3. **Kontribusi Domain:**
   - Rekomendasi preskriptif kualitas air yang actionable
   - Evaluasi feasibility dengan standar regulasi Indonesia (Permenkes)
   - Analisis trade-off antar properti counterfactual pada domain air

### What-If Analysis (Mengapa Integrasi Diperlukan)
- **Jika XGBoost saja**: Prediksi deterministik tanpa estimasi uncertainty -> operator tidak tahu confidence
- **Jika SHAP saja**: Diagnostik only (fitur mana penting), bukan preskriptif (berapa harus diubah)
- **Jika NGBoost saja**: Prediksi + uncertainty, tapi tanpa rekomendasi perbaikan
- **NGBoost + DiCE**: Solusi simultan - prediksi + uncertainty + rekomendasi actionable

---
## 11. PERTANYAAN PENGUJI DAN JAWABAN

### KATEGORI A: PERTANYAAN TENTANG DATASET

**Q: "Kenapa pakai dataset publik Kaggle? Bukan data dari PDAM/lab Indonesia?"**

> **Jawaban bertingkat:**
> - L1: "Dataset publik Kaggle, berlisensi CC0, digunakan di 99+ paper Scopus termasuk Patel et al. (2022) dan Park et al. (2022)."
> - L2: "Dataset ini diposisikan sebagai benchmark validasi metodologi, bukan klaim representatifitas wilayah tertentu. Fokus penelitian pada METODOLOGI (NGBoost+DiCE), bukan pada data spesifik."
> - L3: "Kerangka NGBoost+DiCE yang dikembangkan bersifat transferable - dapat langsung diterapkan pada data PDAM/laboratorium nyata tanpa perubahan arsitektur."

**Q: "Kenapa pakai 2 dataset?"**

> "Dataset Kadiwal (binary, challenging ~70% acc) sebagai dataset utama. Dataset Canada (multi-class, ~98% acc) sebagai validasi eksternal untuk menunjukkan GENERALIZABILITY kerangka kerja pada dataset dengan karakteristik berbeda (jumlah kelas, fitur, distribusi)."

**Q: "Populasi dan sampel penelitian ini apa?"**

> "Ini bukan penelitian survei. Data sekunder 3.276 record (Kadiwal) dan 3.949 record (Canada). Populasi = seluruh dataset benchmark yang tersedia. Seluruh record digunakan karena memiliki target valid dan tidak ada duplikat."

**Q: "Instrumen penelitian apa?"**

> "Instrumen = library open-source: ngboost, dice-ml, scikit-learn, xgboost. Semua berlisensi Apache/MIT/BSD, tidak perlu izin khusus. Reliabilitas dijamin melalui reproducibility: random seed fixed, environment terdokumentasi."

---

### KATEGORI B: PERTANYAAN TENTANG METODE

**Q: "Kenapa NGBoost? Kenapa bukan deep learning atau BNN?"**

> **Jawaban bertingkat:**
> - L1: "NGBoost = probabilistik via Bernoulli + Natural Gradient. Menghasilkan distribusi probabilitas penuh, bukan hanya label."
> - L2: "NGBoost dipilih vs BNN (terlalu kompleks untuk tabular kecil-sedang), vs MC Dropout (approximate uncertainty saja), vs deep learning (inferior pada data tabular menurut Grinsztajn et al. 2022)."
> - L3: "NGBoost kompatibel dengan DiCE melalui API predict_proba. Dan gradient boosting terbukti SOTA pada data tabular."

**Q: "Kenapa DiCE? Kenapa bukan SHAP atau LIME?"**

> "SHAP dan LIME bersifat DIAGNOSTIK - menjelaskan fitur mana yang berpengaruh (WHY), tetapi TIDAK memberikan rekomendasi perubahan (HOW). DiCE bersifat PRESKRIPTIF - memberikan instruksi spesifik: 'ubah pH dari 5.2 menjadi 7.0'. Tabel perbandingan XAI ada di BAB 2 (Tabel 2.2)."

**Q: "Kenapa DiCE bukan Wachter atau FACE?"**

> "Wachter hanya 1 CF per instance (tidak ada alternatif). FACE kurang fleksibel untuk domain-specific constraints. Growing Spheres tidak multi-objective. DiCE menghasilkan DIVERSE counterfactuals dengan mekanisme permitted_range untuk constraint regulasi (WHO/Permenkes)."

**Q: "Apa bedanya probabilistik di sini dengan Bayesian?"**

> "Probabilistik di sini merujuk pada pemodelan distribusi Bernoulli melalui NGBoost - menghasilkan aleatoric uncertainty (mu*(1-mu)). BUKAN Bayesian inference penuh yang memerlukan posterior estimation. Uncertainty yang diukur = ketidakpastian DATA, bukan ketidakpastian MODEL."

---

### KATEGORI C: PERTANYAAN TENTANG PREPROCESSING

**Q: "Bukankah scaling sebelum split itu data leakage?"**

> "Tidak. Median imputation dan MinMax scaling bersifat UNSUPERVISED - tidak menggunakan informasi label target (y). Data leakage terjadi ketika informasi dari label test bocor ke proses training. Transformasi yang hanya menggunakan distribusi fitur (x) tanpa label tidak menyebabkan leakage. Pendekatan ini mengikuti Al Bataineh et al. (2026) yang dipublikasikan di IEEE JSTARS (peer-reviewed)."

**Q: "Kenapa median, bukan mean atau MICE?"**

> "Median bersifat ROBUST terhadap outlier. Distribusi fitur fisikokimia umumnya skewed (tidak normal) - terbukti dari EDA. Mean sensitif terhadap outlier dan akan memberikan imputasi yang bias. Median memberikan nilai tengah yang lebih representatif."

**Q: "Kenapa MinMax, bukan Standardization (Z-score)?"**

> "MinMax dipilih karena: (1) sesuai rekomendasi Al Bataineh et al. (2026) Step 1.2 yang secara eksplisit menyebut normalisasi ke [0,1]; (2) menghasilkan rentang bounded [0,1] yang sesuai dengan permitted_range DiCE; (3) SMOTE-ENN dan nearest neighbor lebih stabil dengan bounded features."

**Q: "Kenapa SMOTE-ENN kondisional?"**

> "Tidak semua dataset memerlukan oversampling. Jika baseline sudah perform baik tanpa resampling, SMOTE bisa justru menambah noise. Maka dilakukan perbandingan: train dengan dan tanpa SMOTE-ENN, pilih yang F1-nya lebih baik. Ini pendekatan evidence-based, bukan assumptive."

---

### KATEGORI D: PERTANYAAN TENTANG CONSTRAINT DAN REGULASI

**Q: "Kenapa constraint WHO dan Permenkes dipisah? Kenapa tidak pakai satu saja?"**

> - Generation pakai WHO (lebih loose) agar DiCE menemukan solusi feasible - jika terlalu ketat dari awal, DiCE mungkin tidak menghasilkan CF valid
> - Evaluasi pakai Permenkes (lebih ketat) untuk mengukur kepatuhan regulasi Indonesia
> - Ini pendekatan "generate widely, evaluate strictly"

**Q: "Hanya 4 dari 9 parameter ada di Permenkes. Bagaimana yang lainnya?"**

> "Benar. pH, TDS, Turbidity, dan Sisa Khlor ada di Permenkes Tabel Wajib. Lima parameter lain (Hardness, Sulfate, Conductivity, Organic Carbon, Trihalomethanes) TIDAK ada di Permenkes - untuk ini digunakan WHO Guidelines sebagai komplementer. Ini merupakan TEMUAN bahwa standar Indonesia belum mencakup seluruh parameter fisikokimia yang umum diuji."

**Q: "Jika feasibility rendah, apa artinya?"**

> "Feasibility rendah terhadap Permenkes = TEMUAN PENELITIAN yang berharga, yaitu: dataset benchmark internasional memiliki distribusi yang berbeda dari standar regulasi Indonesia. Ini menunjukkan bahwa kerangka kerja akan lebih optimal jika diterapkan pada data PDAM Indonesia yang distribusinya lebih sesuai dengan Permenkes."

---

### KATEGORI E: PERTANYAAN TENTANG VARIABEL DAN TOPIK

**Q: "Kenapa parameter fisikokimia? Bukan biologis/mikroba?"**

> "Parameter fisikokimia bersifat CONTROLLABLE dan ACTIONABLE - nilainya dapat diintervensi langsung melalui proses pengolahan air (koagulasi, filtrasi, aerasi, disinfeksi). Parameter biologis/mikroba bersifat OUTCOME (hasil dari kondisi fisikokimia), bukan input yang bisa di-treat langsung. Counterfactual explanations memerlukan fitur yang BISA DIUBAH nilainya - ini syarat metodologis dari DiCE."

**Q: "Apa manfaat penelitian ini?"**

> "Manfaat: (1) Operator pengolahan air mendapat rekomendasi SPESIFIK parameter mana yang harus diubah dan berapa nilainya; (2) Estimasi confidence membantu pengambilan keputusan pada zona borderline; (3) Kerangka kerja transferable ke berbagai sumber data kualitas air."

**Q: "Kenapa judulnya 'Analisis Preskriptif' bukan 'Prediksi'?"**

> "Prediksi = menghasilkan output label/probabilitas. Preskriptif = memberikan rekomendasi tindakan. Penelitian ini MELAMPAUI prediksi - tidak berhenti di 'air ini tidak layak', tapi berlanjut ke 'lakukan perubahan X, Y, Z agar layak'. Ini yang membedakan dari 99% paper di domain kualitas air yang hanya prediktif."

---

### KATEGORI F: PERTANYAAN TEKNIS LANJUTAN

**Q: "Bagaimana NGBoost bisa kompatibel dengan DiCE?"**

> "NGBoost tidak secara langsung kompatibel dengan DiCE karena API-nya berbeda. Solusinya: membuat NGBoostWrapper class yang mengimplementasikan method predict_proba() sesuai scikit-learn API. Wrapper ini menjembatani antara output distribusi NGBoost dengan input yang dibutuhkan DiCE untuk optimasi gradient."

**Q: "Kenapa 5-fold CV, bukan 10-fold?"**

> "5-fold dipilih karena ukuran dataset moderat (3.276 sampel). 10-fold akan menghasilkan fold training yang terlalu kecil. 5-fold memberikan keseimbangan antara bias dan variance dalam estimasi performa, dan juga lebih efisien komputasi untuk grid search."

**Q: "Bagaimana menangani multi-class pada Canada dataset untuk DiCE?"**

> "Training tetap 5-class (NGBoost k_categorical(5)). Namun untuk DiCE, dilakukan binary grouping: {Marginal, Poor} = 'Unacceptable' dan {Excellent, Good, Fair} = 'Acceptable'. DiCE kemudian membangkitkan CF dari Unacceptable ke Acceptable. Ini mengikuti pendekatan Lenatti et al. (2025) untuk counterfactual pada multi-class."

---

## 12. REFERENSI KUNCI (Yang Harus Diketahui Mendalam)

### Referensi WAJIB HAFAL

| No | Referensi | Relevansi | Key Point |
|----|-----------|-----------|-----------|
| 1 | **Duan et al. (2020)** | Penemu NGBoost | "NGBoost: Natural Gradient Boosting for Probabilistic Prediction" - Stanford. Memperkenalkan Natural Gradient pada boosting. |
| 2 | **Mothilal et al. (2020)** | Penemu DiCE | "DiCE: Diverse Counterfactual Explanations" - Microsoft Research. Framework untuk multiple diverse CFs. |
| 3 | **Al Bataineh et al. (2026)** | Justifikasi preprocessing | IEEE JSTARS. XGBoost + FNN untuk WQI. Algorithm 3 = urutan preprocessing yang kita ikuti. Acc 86.9%, F1 0.849, AUC 0.894 |
| 4 | **Zhu et al. (2023)** | SMOTE-ENN + NGBoost | Integrasi SMOTE-ENN dengan NGBoost pada prediksi risiko finansial. Menunjukkan efektivitas kombinasi resampling + probabilistic. |
| 5 | **Dastile & Celik (2024)** | 5 properti CF | Investigasi optimasi properti counterfactual pada credit scoring. Mendefinisikan validity, proximity, sparsity, diversity, feasibility. |
| 6 | **Aderemi et al. (2025)** | Systematic review XAI air | Review XAI pada pemantauan kualitas air. Mengidentifikasi GAP: CF belum diterapkan di domain air. |
| 7 | **Nnadi et al. (2026)** | DiCE + multi-level XAI | Framework multi-level XAI dengan DiCE untuk prediksi depresi mahasiswa. Referensi grid search. |
| 8 | **Lenatti et al. (2025)** | Multi-class CF | Evaluasi DiCE vs MUCH untuk multi-class. Referensi binary grouping. |
| 9 | **Patel et al. (2022)** | Preprocessing order | Water potability classification. Mendukung preprocessing sebelum split. |
| 10 | **Park et al. (2022)** | Ensemble + SHAP | Model ensemble untuk kualitas air dengan SHAP. Akurasi ~80%. Menunjukkan limitasi SHAP (hanya diagnostik). |

### Referensi Regulasi

| Dokumen | Detail |
|---------|--------|
| **WHO Guidelines for Drinking-Water Quality (2022)** | 4th ed. ISBN 978-92-4-004506-4. Basis constraint generation. |
| **Permenkes No. 2 Tahun 2023** | Peraturan Pelaksanaan PP No. 66/2014 tentang Kesehatan Lingkungan. Tabel Wajib: pH, TDS, Turbidity, Sisa Khlor. |
| **WHO, UNICEF, World Bank (2022)** | "State of the World's Drinking Water" ISBN 978-92-4-006080-7. Data urgensi (2 miliar tanpa akses). |

### Tips Menyebut Referensi Saat Sidang
- Selalu sebut **nama + tahun**: "Menurut Duan et al. (2020)..."
- Untuk regulasi: "Berdasarkan WHO Guidelines 2022..."
- Jika lupa detail: "Hal tersebut telah dibahas di BAB 2 subbab 2.2.X..."
- Jangan mengada-ada angka yang tidak ada di proposal

---

## TIPS TAMBAHAN UNTUK SIDANG

### Sebelum Sidang
1. Baca ulang BAB 1 (Pendahuluan) - ini yang akan ditanyakan paling banyak
2. Pahami alur dari gap -> rumusan masalah -> tujuan (harus seamless)
3. Hafal 5 properti counterfactual dan bisa jelaskan masing-masing
4. Pahami perbedaan probabilistik vs deterministik vs Bayesian
5. Siapkan jawaban untuk "kenapa?" di setiap keputusan desain

### Saat Sidang
1. Jawab LANGSUNG, jangan bertele-tele
2. Jika tidak tahu, katakan "Akan saya pelajari lebih lanjut, Pak/Bu" - jangan asal jawab
3. Gunakan bahasa akademis tapi tetap jelas
4. Jika ditanya rumus, jelaskan KONSEP dulu baru rumus
5. Selalu kaitkan jawaban kembali ke TUJUAN penelitian

### Kalimat Pembuka Presentasi (Contoh)
> "Assalamualaikum. Perkenalkan, saya Aflah Zaki Siregar, NIM 103062300095. Judul proposal saya adalah 'Analisis Preskriptif Kualitas Air Menggunakan Natural Gradient Boosting dan Counterfactual Explanations'. Penelitian ini bertujuan untuk mengembangkan kerangka kerja yang tidak hanya memprediksi kelayakan air secara probabilistik, tetapi juga memberikan rekomendasi perbaikan yang actionable bagi operator pengolahan air."

---

## RINGKASAN SATU HALAMAN (Quick Reference)

```
JUDUL: Analisis Preskriptif Kualitas Air Menggunakan NGBoost dan Counterfactual Explanations

GAP: (1) Tidak ada uncertainty estimation, (2) Tidak ada rekomendasi actionable, (3) CF belum di domain air

METODE: NGBoost (probabilistik) + DiCE (preskriptif)

PREPROCESSING: EDA -> Median Impute (all) -> MinMax Scale (all) -> Split 70/15/15 -> SMOTE-ENN (train, conditional)
  Referensi: Al Bataineh et al. (2026) Algorithm 3

EVALUASI:
  - Klasifikasi: Acc, Prec, Rec, F1, AUC-ROC
  - Kalibrasi: NLL, ECE
  - Counterfactual: Validity, Proximity, Sparsity, Diversity, Feasibility

DATASET:
  - Kadiwal: Binary, 3276 samples, 9 features, ~70% acc (utama)
  - Canada: Multi-class 5, 3949 samples, 8 features, ~98% acc (validasi)

CONSTRAINT: WHO (generation) + Permenkes (evaluation) - 2 skenario

NOVELITAS: First implementation NGBoost+DiCE di domain kualitas air + regulatory constraints

HIPOTESIS: NGBoost >= baseline + kalibrasi superior, DiCE validity > 90%, feasibility > 85%
```

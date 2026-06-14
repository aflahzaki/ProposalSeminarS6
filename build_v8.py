"""Build REVISI_PROPOSAL_AFLAH.docx v8 - FINAL"""
# Strategy: read build_v6.py source, apply v7 replacements then v8 replacements, exec.

with open('/projects/sandbox/ProposalSeminarS6/build_v6.py', 'r') as f:
    src = f.read()

# ============================================================
# SECTION A: All v7 replacements (from build_v7.py)
# ============================================================

# v7 1. Title/description
src = src.replace(
    '"""Build REVISI_PROPOSAL_AFLAH.docx v6 - Final revision guide (28 revisions)."""',
    '"""Build REVISI_PROPOSAL_AFLAH.docx v8 - FINAL."""'
)
src = src.replace(
    "PANDUAN REVISI PROPOSAL TUGAS AKHIR (v6 - Final)",
    "PANDUAN REVISI PROPOSAL TUGAS AKHIR (v8 - FINAL)"
)
src = src.replace(
    "Dokumen panduan revisi final (28 revisi). Versi 6 menambahkan perbaikan BAB 2: justifikasi metode NGBoost dan DiCE, tabel perbandingan XAI, batasan konsep probabilistik, what-if analysis, dan novelitas statement.",
    "Dokumen panduan revisi FINAL (28 revisi + koreksi constraint). Versi 8: koreksi angka Permenkes, narasi 2 skenario constraint, konsolidasi referensi."
)

# v7 2. Lokasi replacements
src = src.replace(
    "doc.add_paragraph('Lokasi: Halaman i, ganti seluruh paragraf dan kata kunci')",
    "doc.add_paragraph('Lokasi: Halaman i. GANTI seluruh konten antara heading ABSTRAK dan Daftar Isi.')"
)

src = src.replace(
    """doc.add_paragraph('Lokasi: Paragraf "Untuk mengatasi kompleksitas data tersebut..."')""",
    """doc.add_paragraph('Lokasi: Hal.1 par.3. GANTI paragraf DIMULAI "Untuk mengatasi kompleksitas data tersebut" BERAKHIR "...penjelasan logis mengenai alasan di balik suatu klasifikasi kelayakan air."')"""
)

src = src.replace(
    """doc.add_paragraph('Lokasi: BAB 1, Paragraf PERTAMA Latar Belakang (halaman 1), SISIPKAN setelah kalimat pertama "Kualitas air minum yang memenuhi standar kelayakan merupakan aspek fundamental dalam menjaga kesehatan masyarakat sekaligus mendukung keberlanjutan ekosistem perairan."')""",
    """doc.add_paragraph('Lokasi: Hal.1 par.1. SISIPKAN SETELAH "...mendukung keberlanjutan ekosistem perairan." SEBELUM "Penentuan kelayakan konsumsi air bergantung..."')"""
)

src = src.replace(
    """doc.add_paragraph('Lokasi: BAB 1, Paragraf ke-2 Latar Belakang (halaman 1), SISIPKAN setelah kalimat "Parameter-parameter tersebut saling memengaruhi secara kompleks, sehingga status kelayakan air tidak dapat ditentukan melalui pendekatan sederhana dan memerlukan analisis data yang lebih mendalam."')""",
    """doc.add_paragraph('Lokasi: Hal.1 par.2. SISIPKAN SETELAH "...memerlukan analisis data yang lebih mendalam." SEBELUM "Selain itu, karakteristik data kualitas air..."')"""
)

src = src.replace(
    "doc.add_paragraph('Lokasi: Sub-bab 2.2.4 (sisipkan sebagai tabel perbandingan)')",
    """doc.add_paragraph('Lokasi: Hal.13 sub-bab 2.2.4. SISIPKAN SETELAH "...bergeser ke kondisi yang diinginkan [9]." SEBELUM "Pada penelitian ini, pendekatan preskriptif lebih relevan..."')"""
)

src = src.replace(
    "doc.add_paragraph('Lokasi: Akhir sub-bab 2.2.3 (tambahkan paragraf justifikasi)')",
    """doc.add_paragraph('Lokasi: Hal.13 akhir sub-bab 2.2.3. TAMBAHKAN SETELAH "...prediksi probabilistik lebih terkalibrasi." SEBELUM heading 2.2.4')"""
)

src = src.replace(
    "doc.add_paragraph('Lokasi: Akhir sub-bab 2.2.5 (tambahkan paragraf justifikasi)')",
    """doc.add_paragraph('Lokasi: Hal.14 akhir sub-bab 2.2.5. TAMBAHKAN SETELAH "...diprioritaskan berdasarkan parameter yang paling berpengaruh." SEBELUM heading 2.2.6')"""
)

src = src.replace(
    "doc.add_paragraph('Lokasi: Sub-bab 2.2.3 (sisipkan di awal atau setelah penjelasan NGBoost)')",
    """doc.add_paragraph('Lokasi: Hal.12-13 sub-bab 2.2.3. SISIPKAN SETELAH paragraf rumus Natural Gradient, SEBELUM paragraf justifikasi (Revisi 24). Urutan: rumus -> Revisi 26 -> Revisi 24')"""
)

src = src.replace(
    "doc.add_paragraph('Lokasi: Sub-bab 2.3 (sisipkan sebelum paragraf penutup)')",
    """doc.add_paragraph('Lokasi: Hal.15 sub-bab 2.3. SISIPKAN SETELAH "...NGBoost pada data kualitas air masih merupakan area yang belum terjamah." SEBELUM "Berdasarkan kajian terhadap penelitian-penelitian terdahulu..."')"""
)

src = src.replace(
    "doc.add_paragraph('Lokasi: Kalimat terakhir sub-bab 2.3')",
    """doc.add_paragraph('Lokasi: Hal.15 sub-bab 2.3. GANTI kalimat penutup "Karena itu, penelitian ini mengisi gap..." sampai akhir sub-bab 2.3')"""
)

# v7 3. Italic format notes
src = src.replace(
    "doc.add_page_break()\n\n# === REVISI",
    "p_italic = doc.add_paragraph()\nr_italic = p_italic.add_run('FORMAT: Teks revisi di atas harus ditulis ITALIC di dokumen final untuk membedakan dari teks asli.')\nr_italic.italic = True\n\ndoc.add_page_break()\n\n# === REVISI"
)

src = src.replace(
    "doc.add_page_break()\n\n# === STRATEGI SIDANG",
    "p_italic = doc.add_paragraph()\nr_italic = p_italic.add_run('FORMAT: Teks revisi di atas harus ditulis ITALIC di dokumen final untuk membedakan dari teks asli.')\nr_italic.italic = True\n\ndoc.add_page_break()\n\n# === STRATEGI SIDANG"
)

# v7 4. Output message
src = src.replace(
    'print("DONE: REVISI_PROPOSAL_AFLAH.docx v6 created successfully.")',
    'print("DONE: REVISI_PROPOSAL_AFLAH.docx v8 created successfully.")'
)

# ============================================================
# SECTION B: v8-specific replacements
# ============================================================

# --- v8 Change 3: Replace REVISI 15 constraint table entirely ---
old_revisi15 = """# === REVISI 15 ===
doc.add_heading('REVISI 15: CONSTRAINT DOMAIN', level=2)
doc.add_paragraph('Lokasi: Sub-bab 3.5.2')
doc.add_paragraph()
doc.add_paragraph('Feasibility constraints berdasarkan Permenkes No. 2/2023 (primary) + WHO Guidelines 2022 (komplementer untuk Conductivity dan Organic Carbon).')
doc.add_paragraph()

headers15 = ['Parameter','Sumber','Range','Catatan']
rows15 = [
    ['pH','Permenkes','6.5-8.5','Langsung'],
    ['Hardness','Permenkes','0-500 mg/L','CaCO3'],
    ['TDS','Permenkes','0-1000 mg/L','Langsung'],
    ['Chloramines','Permenkes*','0-5 mg/L','*Dari Sisa Klor'],
    ['Sulfate','Permenkes','0-400 mg/L','Langsung'],
    ['Conductivity','WHO(2022)','0-1500 uS/cm','Tidak di Permenkes'],
    ['Organic Carbon','WHO(2022)','0-25 mg/L','Tidak langsung(KMnO4)'],
    ['Trihalomethanes','Permenkes','0-80 ug/L','Langsung'],
    ['Turbidity','Permenkes','0-5 NTU','Langsung'],
]
add_table(doc, headers15, rows15)

doc.add_paragraph('Catatan: Distribusi dataset melampaui batas regulasi (TDS hingga 61.227 vs max 1.000). Instance jauh dari range menghasilkan feasibility rendah - ini menjadi temuan penelitian.')"""

new_revisi15 = """# === REVISI 15 ===
doc.add_heading('REVISI 15: CONSTRAINT DOMAIN (2 SKENARIO)', level=2)
doc.add_paragraph('Lokasi: Sub-bab 3.5.2')
doc.add_paragraph()
doc.add_paragraph('Constraint dibagi menjadi 2 skenario: GENERATION (WHO) dan EVALUASI (Permenkes).')
doc.add_paragraph()

p = doc.add_paragraph()
p.add_run('BAGIAN A: Tabel Constraint GENERATION (untuk DiCE - WHO Guidelines 2022)').bold = True
doc.add_paragraph()

headers15a = ['Parameter','WHO Guideline','Permitted Range DiCE','Catatan']
rows15a = [
    ['pH','6.5-8.5','6.5-8.5','Sama dgn Permenkes'],
    ['Hardness','<500 mg/L','0-500','Acceptability'],
    ['TDS (Solids)','<1000 mg/L (taste)','0-1000','Health: not concern'],
    ['Chloramines','3 mg/L','0-3','Guideline value'],
    ['Sulfate','<500 mg/L (taste)','0-500','No health-based GV'],
    ['Conductivity','No formal GV','Data-driven (P5-P95)','Tidak ada standar formal'],
    ['Organic Carbon','No formal GV','Data-driven (P5-P95)','Tidak ada standar formal'],
    ['Trihalomethanes','<200 ug/L (total THMs)','0-200','Sum of 4 THMs'],
    ['Turbidity','<4 NTU (disinfection)','0-4','Ideally <1'],
]
add_table(doc, headers15a, rows15a)

p = doc.add_paragraph()
p.add_run('BAGIAN B: Tabel Constraint EVALUASI (Permenkes No. 2 Tahun 2023 - Tabel 1 Parameter Wajib)').bold = True
doc.add_paragraph()

headers15b = ['Parameter','Permenkes Aktual','Sumber','Status di Dataset']
rows15b = [
    ['pH','6.5-8.5','Tabel 1 No.8','Banyak di luar range (0-14)'],
    ['TDS','<300 mg/L','Tabel 1 No.4','SELURUH data melebihi (min 321)'],
    ['Kekeruhan/Turbidity','<3 NTU','Tabel 1 No.5','Sebagian melebihi'],
    ['Sisa Khlor/Chloramines','0.2-0.5 mg/L','Tabel 1 No.14','Hampir semua melebihi'],
    ['Hardness','TIDAK ADA','Tidak di Tabel Wajib','Gunakan WHO'],
    ['Sulfate','TIDAK ADA','Tidak di Tabel Wajib','Gunakan WHO'],
    ['Conductivity','TIDAK ADA','Tidak di Tabel Wajib/Khusus','Gunakan WHO/data-driven'],
    ['Organic Carbon','TIDAK ADA*','*Tabel 2: Hidrokarbon poliaromatik 0.0007 (beda konteks)','Gunakan WHO/data-driven'],
    ['Trihalomethanes','TIDAK ADA','Tidak di Tabel Wajib/Khusus','Gunakan WHO'],
]
add_table(doc, headers15b, rows15b)

doc.add_paragraph(
    'NARASI 2 SKENARIO (tambahkan di sub-bab 3.5.2):\\n'
    'Evaluasi feasibility dilakukan dengan 2 skenario:\\n'
    'Skenario 1 (Generation): DiCE membangkitkan counterfactual dengan constraint berdasarkan WHO Guidelines for Drinking-Water Quality (2022) yang memiliki range lebih permissive dan sesuai dengan distribusi data benchmark.\\n'
    'Skenario 2 (Evaluasi Regulasi): Counterfactual yang dihasilkan kemudian dievaluasi terhadap standar Permenkes No. 2/2023 untuk mengukur seberapa compliant rekomendasi terhadap regulasi Indonesia.\\n'
    'Analisis gap antara feasibility Skenario 1 dan Skenario 2 menghasilkan insight tentang kesesuaian distribusi dataset benchmark terhadap standar regulasi Indonesia. Jika feasibility Skenario 2 jauh lebih rendah, ini mengindikasikan bahwa kerangka kerja akan lebih optimal jika diaplikasikan pada data aktual yang distribusinya mendekati standar Permenkes.'
)"""

src = src.replace(old_revisi15, new_revisi15)

# --- v8 Change 4: Replace Revisi 20 text ---
old_revisi20_text = (
    "'Menurut WHO (2022), sekitar 2 miliar orang di seluruh dunia masih menggunakan sumber air minum yang terkontaminasi. '\n"
    "    'Di Indonesia, data Badan Pusat Statistik (2023) menunjukkan bahwa akses terhadap air minum layak belum merata di seluruh wilayah, dengan disparitas signifikan antara perkotaan dan perdesaan. '\n"
    "    'Kondisi ini menegaskan kebutuhan akan sistem monitoring dan evaluasi kualitas air yang tidak hanya akurat dalam memprediksi kelayakan, tetapi juga mampu memberikan rekomendasi perbaikan yang spesifik dan dapat ditindaklanjuti oleh operator pengolahan air.'"
)

new_revisi20_text = (
    "'Menurut laporan WHO, UNICEF, dan World Bank (2022), meskipun 74% populasi dunia (5,8 miliar orang) telah mengakses air minum yang dikelola secara aman pada tahun 2020, masih terdapat 2 miliar orang yang belum memiliki akses terhadap layanan air minum yang aman [NEW_REF_WHO_SOWD]. '\n"
    "    'Di Indonesia, tantangan serupa dihadapi oleh Perusahaan Daerah Air Minum (PDAM) yang mengalami keterbatasan infrastruktur sehingga hanya mampu melayani sebagian kecil rumah tangga di wilayah layanannya [NEW_REF_WHO_SOWD, hal. 92]. '\n"
    "    'Kondisi ini menegaskan kebutuhan akan sistem evaluasi kualitas air yang tidak hanya akurat dalam memprediksi kelayakan, tetapi juga mampu memberikan rekomendasi perbaikan yang spesifik dan dapat ditindaklanjuti oleh operator pengolahan air.'"
)

src = src.replace(old_revisi20_text, new_revisi20_text)

# Replace the CATATAN PENTING after Revisi 20
old_catatan20 = """p = doc.add_paragraph()
p.add_run('CATATAN PENTING:').bold = True
p.add_run(' Verifikasi angka dan tahun dari sumber resmi:')
doc.add_paragraph('- WHO: "Drinking-water Key Facts" (2022/2023) - https://www.who.int/news-room/fact-sheets/detail/drinking-water')
doc.add_paragraph('- BPS: "Statistik Lingkungan Hidup Indonesia" atau "Indikator Perumahan dan Kesehatan Lingkungan" edisi terbaru')
doc.add_paragraph('- Pastikan sitasi sesuai format IEEE yang digunakan di proposal')"""

new_catatan20 = """p = doc.add_paragraph()
p.add_run('CATATAN PENTING:').bold = True
p.add_run(' Data di atas berasal dari WHO, UNICEF, World Bank, "State of the World\\'s Drinking Water," 2022, ISBN 978-92-4-006080-7 (hal. 11 Executive Summary dan hal. 92 Box 29). Tidak perlu data BPS.')"""

src = src.replace(old_catatan20, new_catatan20)

# --- v8 Change 5: Add "Pertanyaan Constraint 2 Skenario" in STRATEGI SIDANG ---
old_strategi_constraint = """doc.add_heading('Pertanyaan Constraint Regulasi', level=3)
doc.add_paragraph('L1: "Permenkes No. 2/2023 + WHO untuk 2 parameter yang tidak ter-cover."')
doc.add_paragraph('L2: "Conductivity dan Organic Carbon tidak di Permenkes, gunakan WHO komplementer."')
doc.add_paragraph('L3: "Distribusi dataset melampaui regulasi = temuan bahwa kerangka lebih cocok untuk data real."')"""

new_strategi_constraint = """doc.add_heading('Pertanyaan Constraint Regulasi', level=3)
doc.add_paragraph('L1: "Permenkes No. 2/2023 + WHO untuk 2 parameter yang tidak ter-cover."')
doc.add_paragraph('L2: "Conductivity dan Organic Carbon tidak di Permenkes, gunakan WHO komplementer."')
doc.add_paragraph('L3: "Distribusi dataset melampaui regulasi = temuan bahwa kerangka lebih cocok untuk data real."')

doc.add_heading('Pertanyaan Constraint 2 Skenario', level=3)
doc.add_paragraph('L1: "Constraint generation pakai WHO (lebih loose, sesuai distribusi data), evaluasi feasibility pakai Permenkes (lebih ketat)."')
doc.add_paragraph('L2: "Hanya 4 dari 9 parameter ada di Permenkes Tabel Wajib (pH, TDS, Turbidity, Sisa Khlor). Sisanya tidak ada - harus pakai WHO."')
doc.add_paragraph('L3: "Feasibility rendah terhadap Permenkes = TEMUAN PENELITIAN bahwa dataset benchmark tidak representatif terhadap standar Indonesia. Kerangka akan optimal pada data PDAM yang lebih realistis."')"""

src = src.replace(old_strategi_constraint, new_strategi_constraint)

# --- v8 Change 6: Add KONSOLIDASI REFERENSI FINAL before CHECKLIST ---
old_checklist_start = """# === CHECKLIST ===
doc.add_heading('CHECKLIST REVISI (28 Item)', level=2)"""

new_checklist_start = """# === KONSOLIDASI REFERENSI FINAL ===
doc.add_heading('KONSOLIDASI REFERENSI FINAL', level=2)

p = doc.add_paragraph()
p.add_run('REFERENSI YANG DITAMBAHKAN:').bold = True
doc.add_paragraph('[NEW_5] M. Yurtsever and M. Emec, "Potable Water Quality Prediction Using AI and ML Algorithms for Better Sustainability," Ege Academic Review, vol. 23, no. 2, pp. 265-278, 2023, doi: 10.21121/eab.1252167.')
doc.add_paragraph('[NEW_PATEL] (nomor sesuai urutan) - S. Patel et al., Computational Intelligence and Neuroscience, 2022, doi: 10.1155/2022/9283293.')
doc.add_paragraph('[NEW_WHO_SOWD] WHO, UNICEF, World Bank, "State of the World\\'s Drinking Water," 2022, ISBN 978-92-4-006080-7.')
doc.add_paragraph('[NEW_WHO_GDW] WHO, "Guidelines for Drinking-Water Quality," 4th ed., 2022, ISBN 978-92-4-004506-4.')
doc.add_paragraph('[NEW_PERMENKES] Kementerian Kesehatan RI, "Permenkes No. 2 Tahun 2023 tentang Peraturan Pelaksanaan PP No. 66 Tahun 2014 tentang Kesehatan Lingkungan," Berita Negara RI No. 55, 2023.')

doc.add_paragraph()
p = doc.add_paragraph()
p.add_run('REFERENSI YANG DIHAPUS:').bold = True
doc.add_paragraph('[5] Li et al. (2026) soil moisture -> DIGANTI dengan Yurtsever & Emec (2023) sebagai [5] baru')

doc.add_paragraph()
p = doc.add_paragraph()
p.add_run('REFERENSI YANG DIPERTAHANKAN:').bold = True
doc.add_paragraph('[2] Al Bataineh et al. (2026) -> TETAP (terverifikasi IEEE JSTARS Vol.19). Metrik: Acc 86.9%, F1 0.849, AUC 0.894')
doc.add_paragraph('[16] Duan et al. (2020) NGBoost -> TETAP sebagai ref utama NGBoost')

doc.add_paragraph()
doc.add_paragraph('CATATAN: Semua referensi [NEW_xxx] harus diberi nomor urut yang sesuai saat dimasukkan ke daftar pustaka proposal. Penomoran mengikuti urutan kemunculan pertama dalam teks.')

doc.add_page_break()

# === CHECKLIST ===
doc.add_heading('CHECKLIST REVISI (28 Item)', level=2)"""

src = src.replace(old_checklist_start, new_checklist_start)

# --- v8 Change 7: Update catatan penting item 12 -> add item 13 ---
old_catatan_12 = "doc.add_paragraph('12. Justifikasi metode (NGBoost, DiCE) harus EKSPLISIT di BAB 2 - jangan hanya deskripsi teori tanpa alasan pemilihan. Siapkan jawaban 3 level untuk pertanyaan \"kenapa metode ini?\"')"

new_catatan_12_13 = """doc.add_paragraph('12. Justifikasi metode (NGBoost, DiCE) harus EKSPLISIT di BAB 2 - jangan hanya deskripsi teori tanpa alasan pemilihan. Siapkan jawaban 3 level untuk pertanyaan "kenapa metode ini?"')
doc.add_paragraph('13. Constraint Permenkes HANYA mencakup 4 parameter (pH, TDS, Turbidity, Sisa Khlor). 5 parameter lainnya TIDAK ADA di Permenkes Tabel Wajib - gunakan WHO Guidelines.')"""

src = src.replace(old_catatan_12, new_catatan_12_13)

# Also update heading to reflect 13 items
src = src.replace(
    "doc.add_heading('CATATAN PENTING (12 item)', level=2)",
    "doc.add_heading('CATATAN PENTING (13 item)', level=2)"
)

# Execute the modified source
exec(compile(src, 'build_v8_generated.py', 'exec'))

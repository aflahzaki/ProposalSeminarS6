"""Build REVISI_PROPOSAL_AFLAH.docx v7 - lokasi spesifik + format italic."""
# Strategy: read build_v6.py source, apply targeted replacements, exec the result.

with open('/projects/sandbox/ProposalSeminarS6/build_v6.py', 'r') as f:
    src = f.read()

# 1. Title/description changes
src = src.replace(
    '"""Build REVISI_PROPOSAL_AFLAH.docx v6 - Final revision guide (28 revisions)."""',
    '"""Build REVISI_PROPOSAL_AFLAH.docx v7 - lokasi spesifik + format italic."""'
)
src = src.replace(
    "PANDUAN REVISI PROPOSAL TUGAS AKHIR (v6 - Final)",
    "PANDUAN REVISI PROPOSAL TUGAS AKHIR (v7 - Lokasi Spesifik)"
)
src = src.replace(
    "Dokumen panduan revisi final (28 revisi). Versi 6 menambahkan perbaikan BAB 2: justifikasi metode NGBoost dan DiCE, tabel perbandingan XAI, batasan konsep probabilistik, what-if analysis, dan novelitas statement.",
    "Dokumen panduan revisi final (28 revisi). Versi 7 menambahkan lokasi spesifik (halaman, paragraf, kalimat anchor) + format italic untuk teks revisi."
)

# 2. Lokasi replacements

# Revisi 1
src = src.replace(
    "doc.add_paragraph('Lokasi: Halaman i, ganti seluruh paragraf dan kata kunci')",
    "doc.add_paragraph('Lokasi: Halaman i. GANTI seluruh konten antara heading ABSTRAK dan Daftar Isi.')"
)

# Revisi 2
src = src.replace(
    """doc.add_paragraph('Lokasi: Paragraf "Untuk mengatasi kompleksitas data tersebut..."')""",
    """doc.add_paragraph('Lokasi: Hal.1 par.3. GANTI paragraf DIMULAI "Untuk mengatasi kompleksitas data tersebut" BERAKHIR "...penjelasan logis mengenai alasan di balik suatu klasifikasi kelayakan air."')"""
)

# Revisi 20
src = src.replace(
    """doc.add_paragraph('Lokasi: BAB 1, Paragraf PERTAMA Latar Belakang (halaman 1), SISIPKAN setelah kalimat pertama "Kualitas air minum yang memenuhi standar kelayakan merupakan aspek fundamental dalam menjaga kesehatan masyarakat sekaligus mendukung keberlanjutan ekosistem perairan."')""",
    """doc.add_paragraph('Lokasi: Hal.1 par.1. SISIPKAN SETELAH "...mendukung keberlanjutan ekosistem perairan." SEBELUM "Penentuan kelayakan konsumsi air bergantung..."')"""
)

# Revisi 21
src = src.replace(
    """doc.add_paragraph('Lokasi: BAB 1, Paragraf ke-2 Latar Belakang (halaman 1), SISIPKAN setelah kalimat "Parameter-parameter tersebut saling memengaruhi secara kompleks, sehingga status kelayakan air tidak dapat ditentukan melalui pendekatan sederhana dan memerlukan analisis data yang lebih mendalam."')""",
    """doc.add_paragraph('Lokasi: Hal.1 par.2. SISIPKAN SETELAH "...memerlukan analisis data yang lebih mendalam." SEBELUM "Selain itu, karakteristik data kualitas air..."')"""
)

# Revisi 23
src = src.replace(
    "doc.add_paragraph('Lokasi: Sub-bab 2.2.4 (sisipkan sebagai tabel perbandingan)')",
    """doc.add_paragraph('Lokasi: Hal.13 sub-bab 2.2.4. SISIPKAN SETELAH "...bergeser ke kondisi yang diinginkan [9]." SEBELUM "Pada penelitian ini, pendekatan preskriptif lebih relevan..."')"""
)

# Revisi 24
src = src.replace(
    "doc.add_paragraph('Lokasi: Akhir sub-bab 2.2.3 (tambahkan paragraf justifikasi)')",
    """doc.add_paragraph('Lokasi: Hal.13 akhir sub-bab 2.2.3. TAMBAHKAN SETELAH "...prediksi probabilistik lebih terkalibrasi." SEBELUM heading 2.2.4')"""
)

# Revisi 25
src = src.replace(
    "doc.add_paragraph('Lokasi: Akhir sub-bab 2.2.5 (tambahkan paragraf justifikasi)')",
    """doc.add_paragraph('Lokasi: Hal.14 akhir sub-bab 2.2.5. TAMBAHKAN SETELAH "...diprioritaskan berdasarkan parameter yang paling berpengaruh." SEBELUM heading 2.2.6')"""
)

# Revisi 26
src = src.replace(
    "doc.add_paragraph('Lokasi: Sub-bab 2.2.3 (sisipkan di awal atau setelah penjelasan NGBoost)')",
    """doc.add_paragraph('Lokasi: Hal.12-13 sub-bab 2.2.3. SISIPKAN SETELAH paragraf rumus Natural Gradient, SEBELUM paragraf justifikasi (Revisi 24). Urutan: rumus -> Revisi 26 -> Revisi 24')"""
)

# Revisi 27
src = src.replace(
    "doc.add_paragraph('Lokasi: Sub-bab 2.3 (sisipkan sebelum paragraf penutup)')",
    """doc.add_paragraph('Lokasi: Hal.15 sub-bab 2.3. SISIPKAN SETELAH "...NGBoost pada data kualitas air masih merupakan area yang belum terjamah." SEBELUM "Berdasarkan kajian terhadap penelitian-penelitian terdahulu..."')"""
)

# Revisi 28
src = src.replace(
    "doc.add_paragraph('Lokasi: Kalimat terakhir sub-bab 2.3')",
    """doc.add_paragraph('Lokasi: Hal.15 sub-bab 2.3. GANTI kalimat penutup "Karena itu, penelitian ini mengisi gap..." sampai akhir sub-bab 2.3')"""
)

# 3. Add italic format notes before each doc.add_page_break() that follows a revision
# We insert a FORMAT ITALIC note before page breaks for revisions that have "Teks Revisi"
# Strategy: after each "p.add_run('Teks Revisi:').bold = True" block, the revision text should be italic
# Simpler approach: add a note paragraph before each page_break

italic_note = """
p_italic = doc.add_paragraph()
r_italic = p_italic.add_run('FORMAT: Teks revisi di atas harus ditulis ITALIC di dokumen final untuk membedakan dari teks asli.')
r_italic.italic = True
"""

# Insert italic note before every doc.add_page_break() 
# But only for revision sections (not for title page or strategy/checklist)
# We'll insert before page breaks that come after revision content

# Count occurrences - we want to add before page breaks for revisi 1-28
# Skip: first page_break (after title), and page breaks after strategy/checklist sections
# Simpler: add before ALL page breaks, they all benefit from the note

src = src.replace(
    "doc.add_page_break()\n\n# === REVISI",
    "p_italic = doc.add_paragraph()\nr_italic = p_italic.add_run('FORMAT: Teks revisi di atas harus ditulis ITALIC di dokumen final untuk membedakan dari teks asli.')\nr_italic.italic = True\n\ndoc.add_page_break()\n\n# === REVISI"
)

# Also for the last revision (28) before STRATEGI SIDANG
src = src.replace(
    "doc.add_page_break()\n\n# === STRATEGI SIDANG",
    "p_italic = doc.add_paragraph()\nr_italic = p_italic.add_run('FORMAT: Teks revisi di atas harus ditulis ITALIC di dokumen final untuk membedakan dari teks asli.')\nr_italic.italic = True\n\ndoc.add_page_break()\n\n# === STRATEGI SIDANG"
)

# 4. Fix the output message
src = src.replace(
    'print("DONE: REVISI_PROPOSAL_AFLAH.docx v6 created successfully.")',
    'print("DONE: REVISI_PROPOSAL_AFLAH.docx v7 created successfully.")'
)

# Execute the modified source
exec(compile(src, 'build_v7_generated.py', 'exec'))

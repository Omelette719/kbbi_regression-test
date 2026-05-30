# Automation Regression Testing - KBBI VI Daring
> Tugas PPKPL — Pengujian Perangkat Lunak

## Informasi Proyek

| Item | Detail |
|------|--------|
| **Website** | KBBI VI Daring |
| **URL** | https://kbbi.kemendikdasmen.go.id |
| **Jenis Testing** | Regression Testing |
| **Tools** | Python 3, Selenium WebDriver, unittest |

---

## Struktur Proyek

```
kbbi_test/
├── README.md
├── requirements.txt
└── test_kbbi.py       # 20 skenario (40 fungsi: 20 positif + 20 negatif)
```

---

## Cara Install & Menjalankan

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Jalankan semua test
```bash
python -m unittest test_kbbi.py -v
```

### 3. Jalankan satu skenario tertentu
```bash
python -m unittest test_kbbi.KBBIVIDaringRegressionTestSuite.test_s01_pos_navigate_to_register -v
```

---

## Daftar Skenario Test (20 Skenario / 40 Fungsi)

### Fase 1: Registrasi Akun Baru (S01–S06)

| No | Skenario | Fungsi Positif | Fungsi Negatif |
|----|----------|---------------|----------------|
| S01 | Akses Form Register | `test_s01_pos_navigate_to_register` | `test_s01_neg_register_submit_empty` |
| S02 | Validasi Field Nama Lengkap | `test_s02_pos_verify_register_fields` | `test_s02_neg_reg_validate_nama_lengkap_required` |
| S03 | Validasi Field Nama Tampilan | `test_s03_pos_verify_register_nama_tampilan_visibility` | `test_s03_neg_reg_validate_nama_tampilan_required` |
| S04 | Validasi Field Pos-el Register | `test_s04_pos_verify_register_posel_visibility` | `test_s04_neg_reg_validate_posel_required` |
| S05 | Validasi Format Pos-el Register | `test_s05_pos_verify_register_posel_attribute` | `test_s05_neg_reg_validate_posel_format` |
| S06 | Validasi Aturan Kata Sandi | `test_s06_pos_verify_register_password_match_rule` | `test_s06_neg_reg_validate_katasandi_min_length` |

### Fase 2: Masuk Akun / Login (S07–S12)

| No | Skenario | Fungsi Positif | Fungsi Negatif |
|----|----------|---------------|----------------|
| S07 | Akses Form Login | `test_s07_pos_navigate_to_login` | `test_s07_neg_login_submit_empty` |
| S08 | Validasi Field Pos-el Login | `test_s08_pos_verify_login_fields` | `test_s08_neg_login_validate_posel_required` |
| S09 | Validasi Field Kata Sandi | `test_s09_pos_verify_login_password_visibility` | `test_s09_neg_login_validate_katasandi_required` |
| S10 | Fitur Ingat Saya & Keamanan Form | `test_s10_pos_login_toggle_remember_me` | `test_s10_neg_verify_login_form_action` |
| S11 | Bantuan & Format Email | `test_s11_pos_verify_forgot_password_link` | `test_s11_neg_login_validate_posel_format` |
| S12 | Jalur Alternatif & Proteksi Login | `test_s12_pos_navigate_to_register_via_login` | `test_s12_neg_login_invalid_email_no_domain` |

### Fase 3: Beranda & Fitur Pencarian (S13–S20)

| No | Skenario | Fungsi Positif | Fungsi Negatif |
|----|----------|---------------|----------------|
| S13 | Navigasi Logo Navbar | `test_s13_pos_click_logo_to_return_home` | `test_s13_neg_access_broken_url` |
| S14 | Menu Tambahan & Validasi ID | `test_s14_pos_navigate_to_seputar_laman` | `test_s14_neg_verify_no_duplicate_search_id` |
| S15 | Pencarian Kata Standar | `test_s15_pos_search_standard_word` | `test_s15_neg_search_empty_input` |
| S16 | Pencarian Huruf Kapital | `test_s16_pos_search_uppercase_word` | `test_s16_neg_search_spaces_only` |
| S17 | Pencarian Huruf Campuran & Simbol | `test_s17_pos_search_mixed_case` | `test_s17_neg_search_special_characters` |
| S18 | Pencarian Kata Berulang & Emoji | `test_s18_pos_search_hyphenated_word` | `test_s18_neg_search_emojis` |
| S19 | Keamanan Input & HTML Injection | `test_s19_pos_search_compound_word` | `test_s19_neg_search_html_injection` |
| S20 | Validasi Footer & SQL Injection | `test_s20_pos_verify_footer_elements` | `test_s20_neg_search_sql_injection` |

---

## Sumber Referensi

- https://www.datacamp.com/tutorial/regression-testing
- https://www.geeksforgeeks.org/software-engineering/software-engineering-regression-testing/

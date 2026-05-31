# Automation Regression Testing — KBBI VI Daring
> Tugas PPKPL | Python + Selenium WebDriver

**Website:** https://kbbi.kemendikdasmen.go.id

---

## Struktur Project

```
kbbi_final/
├── config.py            ← Konfigurasi URL & kredensial akun test
├── base_test.py         ← Base class WebDriver (setup & teardown)
├── requirements.txt
├── README.md
└── tests/
    ├── test_register.py ← S01–S06: Validasi form registrasi
    ├── test_login.py    ← S07–S12: Login beneran + validasi
    └── test_beranda.py  ← S13–S20: Navigasi & pencarian
```

---

## Install & Jalankan

```bash
pip install -r requirements.txt

# Jalankan semua test
python -m unittest discover -s tests -v

# Per file
python -m unittest tests.test_register -v
python -m unittest tests.test_login -v
python -m unittest tests.test_beranda -v
```

---

## Daftar 20 Skenario (40 Test Case)

> Setiap skenario menguji **hal yang sama** dengan kondisi berbeda (positif vs negatif)

### 📋 test_register.py
| Skenario | Hal yang Diuji | Positif | Negatif |
|----------|---------------|---------|---------|
| S01 | Akses halaman register | Via klik navbar | Via URL langsung |
| S02 | Field Nama Lengkap | Input valid diterima | Field kosong → form ditolak |
| S03 | Field Nama Tampilan | Input valid diterima | Field kosong → form ditolak |
| S04 | Format Pos-el (email) | Email valid diterima | Email format salah → ditolak |
| S05 | Panjang Kata Sandi | ≥6 karakter diterima | <6 karakter → ditolak |
| S06 | Konfirmasi Kata Sandi | Password sama → diterima | Password beda → ditolak |

### 🔐 test_login.py
| Skenario | Hal yang Diuji | Positif | Negatif |
|----------|---------------|---------|---------|
| S07 | Login dengan kredensial | Email & password valid → masuk | Email & password salah → ditolak |
| S08 | Email pada login | Email terdaftar → berhasil | Email tidak terdaftar → ditolak |
| S09 | Password pada login | Password benar → berhasil | Password salah → ditolak |
| S10 | Checkbox Ingat Saya | Diklik → tercentang | Tidak diklik → tidak tercentang |
| S11 | Lupa Kata Sandi | Klik link → ke ForgotPassword | Submit kosong → ditolak |
| S12 | Format email login | Format benar → diproses | Format salah → ditolak |

### 🏠 test_beranda.py
| Skenario | Hal yang Diuji | Positif | Negatif |
|----------|---------------|---------|---------|
| S13 | Navigasi logo navbar | Dari login → beranda | Dari register → beranda |
| S14 | Menu Seputar Laman | Via klik navbar | Via URL langsung |
| S15 | Pencarian kata | Kata ada di KBBI → ditemukan | Kata tidak ada → tidak ditemukan |
| S16 | Validasi input pencarian | Input terisi → diproses | Input kosong → pesan error |
| S17 | Pencarian huruf campuran | Huruf campuran → ditemukan | Huruf kapital → ditemukan |
| S18 | Pencarian tanda baca | Kata berulang 'kupu-kupu' | Karakter simbol → tidak error |
| S19 | Keamanan input (injection) | HTML tag → tidak dirender | SQL injection → tidak error server |
| S20 | Komponen footer | Link Android tampil | Link iOS tampil |

---

## Catatan Penting

- **Register:** Tidak bisa diotomasi penuh karena Google reCAPTCHA. Skenario fokus pada validasi form.
- **Login:** Menggunakan akun nyata yang sudah terdaftar di KBBI VI Daring.
- **Pencarian:** Dapat diakses tanpa login dari halaman utama.

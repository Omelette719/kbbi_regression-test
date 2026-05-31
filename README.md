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

## Catatan Penting

- **Register:** Tidak bisa diotomasi penuh karena Google reCAPTCHA. Skenario fokus pada validasi form.
- **Login:** Menggunakan akun nyata yang sudah terdaftar di KBBI VI Daring.
- **Pencarian:** Dapat diakses tanpa login dari halaman utama.

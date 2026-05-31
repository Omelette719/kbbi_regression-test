# test_register.py
# Fase 1: Registrasi Akun Baru (S01 - S06)
#
# Catatan: Register tidak dapat diotomasi sepenuhnya karena Google reCAPTCHA.
# Skenario fokus pada validasi form — setiap skenario positif dan negatif
# menguji hal yang SAMA dengan kondisi yang berbeda (valid vs tidak valid).

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.base_test import BaseTest


class RegisterTest(BaseTest):

    # =========================================================================
    # SKENARIO 01: Akses Halaman Register
    # Hal yang diuji : Navigasi ke halaman register
    # Positif : Klik 'Daftar Baru' di navbar → berhasil masuk halaman register
    # Negatif : Akses langsung URL /Account/Register → halaman tetap termuat
    # =========================================================================

    def test_s01_pos_navigate_register_via_navbar(self):
        """Positif: Klik link 'Daftar Baru' di navbar berhasil mengarah ke halaman register."""
        self.driver.find_element(By.ID, "registerLink").click()
        self.assertIn("/Account/Register", self.driver.current_url)

    def test_s01_neg_direct_url_register_loads(self):
        """Negatif: Akses langsung URL /Account/Register tanpa klik navbar tetap berhasil dimuat."""
        self.driver.get(f"{self.base_url}/Account/Register")
        self.assertIn("/Account/Register", self.driver.current_url)
        self.assertTrue(self.driver.find_element(By.ID, "NamaLengkap").is_displayed())

    # =========================================================================
    # SKENARIO 02: Validasi Field Nama Lengkap
    # Hal yang diuji : Input field Nama Lengkap
    # Positif : Mengisi Nama Lengkap dengan nilai valid → field menerima input
    # Negatif : Mengosongkan Nama Lengkap lalu submit → form ditolak
    # =========================================================================

    def test_s02_pos_nama_lengkap_accepts_valid_input(self):
        """Positif: Field Nama Lengkap menerima input teks yang valid."""
        self.driver.get(f"{self.base_url}/Account/Register")
        field = self.driver.find_element(By.ID, "NamaLengkap")
        field.send_keys("Azwin Hakim")
        self.assertEqual(field.get_attribute("value"), "Azwin Hakim")

    def test_s02_neg_nama_lengkap_empty_form_rejected(self):
        """Negatif: Submit form register dengan Nama Lengkap kosong ditolak, tetap di halaman register."""
        self.driver.get(f"{self.base_url}/Account/Register")
        # Isi field lain, biarkan NamaLengkap kosong
        self.driver.find_element(By.ID, "NamaTampilan").send_keys("azwin")
        self.driver.find_element(By.ID, "Posel").send_keys("azwin@email.com")
        self.driver.find_element(By.ID, "KataSandi").send_keys("password123")
        self.driver.find_element(By.ID, "KonfirmasiKataSandi").send_keys("password123")
        self.driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Daftarkan']").click()
        self.assertIn("/Account/Register", self.driver.current_url)

    # =========================================================================
    # SKENARIO 03: Validasi Field Nama Tampilan
    # Hal yang diuji : Input field Nama Tampilan
    # Positif : Mengisi Nama Tampilan dengan nilai valid → field menerima input
    # Negatif : Mengosongkan Nama Tampilan lalu submit → form ditolak
    # =========================================================================

    def test_s03_pos_nama_tampilan_accepts_valid_input(self):
        """Positif: Field Nama Tampilan menerima input teks yang valid."""
        self.driver.get(f"{self.base_url}/Account/Register")
        field = self.driver.find_element(By.ID, "NamaTampilan")
        field.send_keys("azwin")
        self.assertEqual(field.get_attribute("value"), "azwin")

    def test_s03_neg_nama_tampilan_empty_form_rejected(self):
        """Negatif: Submit form register dengan Nama Tampilan kosong ditolak, tetap di halaman register."""
        self.driver.get(f"{self.base_url}/Account/Register")
        # Isi field lain, biarkan NamaTampilan kosong
        self.driver.find_element(By.ID, "NamaLengkap").send_keys("Azwin Hakim")
        self.driver.find_element(By.ID, "Posel").send_keys("azwin@email.com")
        self.driver.find_element(By.ID, "KataSandi").send_keys("password123")
        self.driver.find_element(By.ID, "KonfirmasiKataSandi").send_keys("password123")
        self.driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Daftarkan']").click()
        self.assertIn("/Account/Register", self.driver.current_url)

    # =========================================================================
    # SKENARIO 04: Validasi Format Pos-el (Email)
    # Hal yang diuji : Input Pos-el dengan format benar vs salah
    # Positif : Mengisi Pos-el dengan format email valid → field menerima input
    # Negatif : Mengisi Pos-el format tidak valid lalu submit → form ditolak
    # =========================================================================

    def test_s04_pos_posel_accepts_valid_email_format(self):
        """Positif: Field Pos-el menerima input dengan format email yang valid."""
        self.driver.get(f"{self.base_url}/Account/Register")
        field = self.driver.find_element(By.ID, "Posel")
        field.send_keys("azwin@email.com")
        self.assertEqual(field.get_attribute("value"), "azwin@email.com")

    def test_s04_neg_posel_invalid_format_form_rejected(self):
        """Negatif: Submit form register dengan Pos-el format tidak valid ditolak."""
        self.driver.get(f"{self.base_url}/Account/Register")
        self.driver.find_element(By.ID, "NamaLengkap").send_keys("Azwin Hakim")
        self.driver.find_element(By.ID, "NamaTampilan").send_keys("azwin")
        self.driver.find_element(By.ID, "Posel").send_keys("emailsalah@tanpadomain")
        self.driver.find_element(By.ID, "KataSandi").send_keys("password123")
        self.driver.find_element(By.ID, "KonfirmasiKataSandi").send_keys("password123")
        self.driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Daftarkan']").click()
        self.assertIn("/Account/Register", self.driver.current_url)

    # =========================================================================
    # SKENARIO 05: Validasi Panjang Kata Sandi
    # Hal yang diuji : Input Kata Sandi dengan panjang cukup vs terlalu pendek
    # Positif : Kata Sandi ≥ 6 karakter → field menerima input
    # Negatif : Kata Sandi < 6 karakter lalu submit → form ditolak
    # =========================================================================

    def test_s05_pos_katasandi_min_length_accepted(self):
        """Positif: Field Kata Sandi menerima input dengan panjang minimal 6 karakter."""
        self.driver.get(f"{self.base_url}/Account/Register")
        field = self.driver.find_element(By.ID, "KataSandi")
        field.send_keys("pass12")  # tepat 6 karakter
        self.assertEqual(len(field.get_attribute("value")), 6)

    def test_s05_neg_katasandi_too_short_form_rejected(self):
        """Negatif: Submit form register dengan Kata Sandi kurang dari 6 karakter ditolak."""
        self.driver.get(f"{self.base_url}/Account/Register")
        self.driver.find_element(By.ID, "NamaLengkap").send_keys("Azwin Hakim")
        self.driver.find_element(By.ID, "NamaTampilan").send_keys("azwin")
        self.driver.find_element(By.ID, "Posel").send_keys("azwin@email.com")
        self.driver.find_element(By.ID, "KataSandi").send_keys("abc")  # kurang dari 6
        self.driver.find_element(By.ID, "KonfirmasiKataSandi").send_keys("abc")
        self.driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Daftarkan']").click()
        self.assertIn("/Account/Register", self.driver.current_url)

    # =========================================================================
    # SKENARIO 06: Validasi Konfirmasi Kata Sandi
    # Hal yang diuji : Kesesuaian Kata Sandi dan Konfirmasi Kata Sandi
    # Positif : KataSandi dan KonfirmasiKataSandi sama → field menerima input
    # Negatif : KataSandi dan KonfirmasiKataSandi berbeda lalu submit → form ditolak
    # =========================================================================

    def test_s06_pos_konfirmasi_katasandi_match_accepted(self):
        """Positif: Field KonfirmasiKataSandi menerima input yang sama dengan KataSandi."""
        self.driver.get(f"{self.base_url}/Account/Register")
        self.driver.find_element(By.ID, "KataSandi").send_keys("password123")
        field_konfirmasi = self.driver.find_element(By.ID, "KonfirmasiKataSandi")
        field_konfirmasi.send_keys("password123")
        self.assertEqual(field_konfirmasi.get_attribute("value"), "password123")

    def test_s06_neg_konfirmasi_katasandi_mismatch_rejected(self):
        """Negatif: Submit form register dengan KonfirmasiKataSandi berbeda dari KataSandi ditolak."""
        self.driver.get(f"{self.base_url}/Account/Register")
        self.driver.find_element(By.ID, "NamaLengkap").send_keys("Azwin Hakim")
        self.driver.find_element(By.ID, "NamaTampilan").send_keys("azwin")
        self.driver.find_element(By.ID, "Posel").send_keys("azwin@email.com")
        self.driver.find_element(By.ID, "KataSandi").send_keys("password123")
        self.driver.find_element(By.ID, "KonfirmasiKataSandi").send_keys("passwordBEDA")
        self.driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Daftarkan']").click()
        self.assertIn("/Account/Register", self.driver.current_url)


if __name__ == "__main__":
    unittest.main(verbosity=2)

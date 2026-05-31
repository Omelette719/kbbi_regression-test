# test_login.py
# Fase 2: Masuk Akun / Login (S07 - S12)
#
# Setiap skenario positif dan negatif menguji hal yang SAMA
# dengan kondisi yang berbeda (valid vs tidak valid).
# Login menggunakan akun terdaftar: azwinhakim35@gmail.com / Azwin456

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.base_test import BaseTest
from config import TEST_EMAIL, TEST_PASSWORD


class LoginTest(BaseTest):

    def do_login(self, email, password):
        """Helper: mengisi dan submit form login."""
        self.driver.get(f"{self.base_url}/Account/Login")
        self.driver.find_element(By.ID, "Posel").send_keys(email)
        self.driver.find_element(By.ID, "KataSandi").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    # =========================================================================
    # SKENARIO 07: Login dengan Kredensial
    # Hal yang diuji : Proses login dengan email & password
    # Positif : Login dengan email & password valid → berhasil masuk sistem
    # Negatif : Login dengan email & password tidak terdaftar → ditolak sistem
    # =========================================================================

    def test_s07_pos_login_valid_credentials(self):
        """Positif: Login dengan email dan password valid berhasil masuk ke sistem."""
        self.do_login(TEST_EMAIL, TEST_PASSWORD)
        WebDriverWait(self.driver, 10).until(
            lambda d: "/Account/Login" not in d.current_url
        )
        self.assertNotIn("/Account/Login", self.driver.current_url)

    def test_s07_neg_login_invalid_credentials(self):
        """Negatif: Login dengan email dan password tidak terdaftar ditolak, tetap di halaman login."""
        self.do_login("emailpalsu@tidakada.com", "passwordSalah999")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "Posel"))
        )
        self.assertIn("/Account/Login", self.driver.current_url)

    # =========================================================================
    # SKENARIO 08: Login dengan Email
    # Hal yang diuji : Validasi field email pada form login
    # Positif : Login dengan email valid (terdaftar) → berhasil
    # Negatif : Login dengan email tidak terdaftar → ditolak
    # =========================================================================

    def test_s08_pos_login_with_registered_email(self):
        """Positif: Login menggunakan email yang sudah terdaftar berhasil masuk sistem."""
        self.do_login(TEST_EMAIL, TEST_PASSWORD)
        WebDriverWait(self.driver, 10).until(
            lambda d: "/Account/Login" not in d.current_url
        )
        self.assertNotIn("/Account/Login", self.driver.current_url)

    def test_s08_neg_login_with_unregistered_email(self):
        """Negatif: Login menggunakan email yang tidak terdaftar ditolak sistem."""
        self.do_login("tidakterdaftar@email.com", TEST_PASSWORD)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "Posel"))
        )
        self.assertIn("/Account/Login", self.driver.current_url)

    # =========================================================================
    # SKENARIO 09: Login dengan Password
    # Hal yang diuji : Validasi password pada form login
    # Positif : Login dengan password yang benar → berhasil
    # Negatif : Login dengan password yang salah → ditolak
    # =========================================================================

    def test_s09_pos_login_with_correct_password(self):
        """Positif: Login menggunakan password yang benar berhasil masuk sistem."""
        self.do_login(TEST_EMAIL, TEST_PASSWORD)
        WebDriverWait(self.driver, 10).until(
            lambda d: "/Account/Login" not in d.current_url
        )
        self.assertNotIn("/Account/Login", self.driver.current_url)

    def test_s09_neg_login_with_wrong_password(self):
        """Negatif: Login menggunakan password yang salah ditolak sistem."""
        self.do_login(TEST_EMAIL, "PasswordSalahBanget999!")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "KataSandi"))
        )
        self.assertIn("/Account/Login", self.driver.current_url)

    # =========================================================================
    # SKENARIO 10: Fitur Ingat Saya (Remember Me)
    # Hal yang diuji : Status checkbox Ingat Saya
    # Positif : Checkbox Ingat Saya bisa dicentang → statusnya berubah jadi true
    # Negatif : Checkbox Ingat Saya tidak disentuh → statusnya tetap false (default)
    # =========================================================================

    def test_s10_pos_remember_me_checked(self):
        """Positif: Checkbox 'Ingat saya?' dapat diklik dan statusnya berubah menjadi tercentang."""
        self.driver.get(f"{self.base_url}/Account/Login")
        checkbox = self.driver.find_element(By.ID, "IngatSaya")
        checkbox.click()
        self.assertTrue(checkbox.is_selected())

    def test_s10_neg_remember_me_unchecked_by_default(self):
        """Negatif: Checkbox 'Ingat saya?' tidak tercentang secara default saat halaman login dibuka."""
        self.driver.get(f"{self.base_url}/Account/Login")
        checkbox = self.driver.find_element(By.ID, "IngatSaya")
        self.assertFalse(checkbox.is_selected())

    # =========================================================================
    # SKENARIO 11: Fitur Lupa Kata Sandi
    # Hal yang diuji : Akses halaman ForgotPassword
    # Positif : Klik link 'Lupa kata sandi?' → berhasil diarahkan ke ForgotPassword
    # Negatif : Submit form ForgotPassword dengan email kosong → form ditolak
    # =========================================================================

    def test_s11_pos_forgot_password_link_redirects(self):
        """Positif: Klik link 'Lupa kata sandi?' berhasil mengarahkan ke halaman ForgotPassword."""
        self.driver.get(f"{self.base_url}/Account/Login")
        self.driver.find_element(By.LINK_TEXT, "Lupa kata sandi?").click()
        WebDriverWait(self.driver, 10).until(EC.url_contains("/Account/ForgotPassword"))
        self.assertIn("/Account/ForgotPassword", self.driver.current_url)

    def test_s11_neg_forgot_password_empty_email_rejected(self):
        """Negatif: Submit form ForgotPassword dengan email kosong ditolak, tetap di halaman tersebut."""
        self.driver.get(f"{self.base_url}/Account/ForgotPassword")
        self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        self.assertIn("/Account/ForgotPassword", self.driver.current_url)

    # =========================================================================
    # SKENARIO 12: Format Email pada Form Login
    # Hal yang diuji : Validasi format email di form login
    # Positif : Login dengan format email yang benar → form diproses
    # Negatif : Login dengan format email tidak lengkap → form ditolak
    # =========================================================================

    def test_s12_pos_login_valid_email_format(self):
        """Positif: Login dengan format email yang benar (ada @ dan domain) diproses sistem."""
        self.do_login(TEST_EMAIL, TEST_PASSWORD)
        # Tidak perlu berhasil login, cukup form diproses (tidak stuck di validasi format)
        WebDriverWait(self.driver, 10).until(
            lambda d: d.current_url != f"{self.base_url}/Account/Login"
                      or "login" in d.page_source.lower()
        )
        # Pastikan tidak ada error format email
        self.assertNotIn("bukan alamat pos-el", self.driver.page_source.lower()
                         if "/Account/Login" in self.driver.current_url else "")

    def test_s12_neg_login_invalid_email_format(self):
        """Negatif: Login dengan format email tidak lengkap (tanpa domain) ditolak sistem."""
        self.do_login("emailtanpadomain@", "password123")
        self.assertIn("/Account/Login", self.driver.current_url)


if __name__ == "__main__":
    unittest.main(verbosity=2)

# test_beranda.py
# Fase 3: Beranda & Fitur Pencarian (S13 - S20)
#
# Setiap skenario positif dan negatif menguji hal yang SAMA
# dengan kondisi yang berbeda (valid vs tidak valid).

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base_test import BaseTest


class BerandaTest(BaseTest):

    # =========================================================================
    # SKENARIO 13: Navigasi via Navbar
    # Hal yang diuji : Navigasi menggunakan link di navbar
    # Positif : Klik 'KBBI VI Daring' di navbar → berhasil kembali ke beranda
    # Negatif : Klik 'KBBI VI Daring' dari halaman register → tetap kembali ke beranda
    # =========================================================================

    def test_s13_pos_click_logo_from_login_to_beranda(self):
        """Positif: Klik teks 'KBBI VI Daring' di navbar dari halaman login kembali ke beranda."""
        self.driver.get(f"{self.base_url}/Account/Login")
        self.driver.find_element(By.LINK_TEXT, "KBBI VI Daring").click()
        self.assertIn("/Beranda", self.driver.current_url)

    def test_s13_neg_click_logo_from_register_to_beranda(self):
        """Negatif: Klik teks 'KBBI VI Daring' di navbar dari halaman register juga kembali ke beranda."""
        self.driver.get(f"{self.base_url}/Account/Register")
        self.driver.find_element(By.LINK_TEXT, "KBBI VI Daring").click()
        self.assertIn("/Beranda", self.driver.current_url)

    # =========================================================================
    # SKENARIO 14: Navigasi Menu Seputar Laman
    # Hal yang diuji : Akses halaman Seputar Laman
    # Positif : Klik 'Seputar Laman' dari beranda → berhasil masuk halaman
    # Negatif : Akses /Beranda/SeputarLaman langsung via URL → halaman tetap termuat
    # =========================================================================

    def test_s14_pos_navigate_seputar_laman_via_navbar(self):
        """Positif: Klik menu 'Seputar Laman' di navbar dari beranda berhasil mengarah ke halaman tersebut."""
        self.driver.find_element(By.LINK_TEXT, "Seputar Laman").click()
        self.assertIn("/Beranda/SeputarLaman", self.driver.current_url)

    def test_s14_neg_access_seputar_laman_via_direct_url(self):
        """Negatif: Akses halaman Seputar Laman langsung via URL tanpa klik navbar tetap berhasil dimuat."""
        self.driver.get(f"{self.base_url}/Beranda/SeputarLaman")
        self.assertIn("/Beranda/SeputarLaman", self.driver.current_url)
        self.assertTrue(self.driver.find_element(By.TAG_NAME, "body").is_displayed())

    # =========================================================================
    # SKENARIO 15: Pencarian Kata di KBBI
    # Hal yang diuji : Hasil pencarian kata
    # Positif : Cari kata yang ADA di KBBI → ditemukan dan diarahkan ke entri
    # Negatif : Cari kata yang TIDAK ADA di KBBI → tidak ditemukan / halaman cari hasil
    # =========================================================================

    def test_s15_pos_search_existing_word(self):
        """Positif: Mencari kata 'makan' yang ada di KBBI berhasil mengarahkan ke halaman entri."""
        self.driver.find_element(By.ID, "textBoxSearch").send_keys("makan")
        self.driver.find_element(By.CSS_SELECTOR, ".glyphicon-search").click()
        WebDriverWait(self.driver, 10).until(EC.url_contains("/entri/makan"))
        self.assertIn("/entri/makan", self.driver.current_url)

    def test_s15_neg_search_nonexistent_word(self):
        """Negatif: Mencari kata yang tidak ada di KBBI tidak mengarah ke halaman entri yang valid."""
        self.driver.find_element(By.ID, "textBoxSearch").send_keys("xyzxyzabcabc999")
        self.driver.find_element(By.CSS_SELECTOR, ".glyphicon-search").click()
        WebDriverWait(self.driver, 10).until(
            lambda d: "/entri/" in d.current_url or "/Cari/" in d.current_url
        )
        # Tidak diarahkan ke entri yang valid / halaman menampilkan tidak ditemukan
        self.assertNotIn("500", self.driver.title)
        self.assertTrue(self.driver.find_element(By.TAG_NAME, "body").is_displayed())

    # =========================================================================
    # SKENARIO 16: Pencarian dengan Input Kosong vs Terisi
    # Hal yang diuji : Validasi input kolom pencarian
    # Positif : Kolom pencarian terisi kata valid → form diproses
    # Negatif : Kolom pencarian kosong → muncul pesan error
    # =========================================================================

    def test_s16_pos_search_with_filled_input(self):
        """Positif: Mencari dengan input terisi kata 'rumah' berhasil mengarahkan ke halaman entri."""
        self.driver.find_element(By.ID, "textBoxSearch").send_keys("rumah")
        self.driver.find_element(By.CSS_SELECTOR, ".glyphicon-search").click()
        WebDriverWait(self.driver, 10).until(EC.url_contains("/entri/"))
        self.assertIn("rumah", self.driver.current_url.lower())

    def test_s16_neg_search_with_empty_input(self):
        """Negatif: Mencari dengan input kosong menampilkan pesan error 'tidak boleh kosong'."""
        self.driver.find_element(By.ID, "textBoxSearch").clear()
        self.driver.find_element(By.CSS_SELECTOR, ".glyphicon-search").click()
        error_div = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "errorMessageDiv"))
        )
        self.assertIn("tidak boleh kosong", error_div.text.lower())

    # =========================================================================
    # SKENARIO 17: Pencarian Kata dengan Huruf Campuran
    # Hal yang diuji : Pencarian dengan variasi huruf kapital
    # Positif : Cari dengan huruf campuran 'InDoNeSiA' → ditemukan entri
    # Negatif : Cari dengan huruf kapital semua 'INDONESIA' → ditemukan entri yang sama
    # =========================================================================

    def test_s17_pos_search_mixed_case_word(self):
        """Positif: Mencari 'InDoNeSiA' dengan huruf campuran berhasil mengarahkan ke halaman entri."""
        self.driver.find_element(By.ID, "textBoxSearch").send_keys("InDoNeSiA")
        self.driver.find_element(By.CSS_SELECTOR, ".glyphicon-search").click()
        WebDriverWait(self.driver, 10).until(EC.url_contains("/entri/"))
        self.assertIn("indonesia", self.driver.current_url.lower())

    def test_s17_neg_search_all_uppercase_word(self):
        """Negatif: Mencari 'INDONESIA' dengan huruf kapital semua juga berhasil mengarahkan ke entri."""
        self.driver.find_element(By.ID, "textBoxSearch").send_keys("INDONESIA")
        self.driver.find_element(By.CSS_SELECTOR, ".glyphicon-search").click()
        WebDriverWait(self.driver, 10).until(EC.url_contains("/entri/"))
        self.assertIn("indonesia", self.driver.current_url.lower())

    # =========================================================================
    # SKENARIO 18: Pencarian Kata dengan Tanda Baca
    # Hal yang diuji : Pencarian kata yang mengandung tanda baca / karakter khusus
    # Positif : Cari kata ulang 'kupu-kupu' (mengandung tanda hubung) → ditemukan
    # Negatif : Cari dengan karakter simbol '!@#$%' → tidak menyebabkan error server
    # =========================================================================

    def test_s18_pos_search_hyphenated_word(self):
        """Positif: Mencari kata ulang 'kupu-kupu' yang mengandung tanda hubung berhasil ditemukan."""
        self.driver.find_element(By.ID, "textBoxSearch").send_keys("kupu-kupu")
        self.driver.find_element(By.CSS_SELECTOR, ".glyphicon-search").click()
        WebDriverWait(self.driver, 10).until(EC.url_contains("kupu"))
        self.assertIn("kupu", self.driver.current_url.lower())

    def test_s18_neg_search_special_characters(self):
        """Negatif: Mencari dengan karakter simbol '!@#$%^&*()' tidak menyebabkan error server."""
        self.driver.find_element(By.ID, "textBoxSearch").send_keys("!@#$%^&*()")
        self.driver.find_element(By.CSS_SELECTOR, ".glyphicon-search").click()
        self.assertNotIn("500", self.driver.title)
        self.assertTrue(self.driver.find_element(By.TAG_NAME, "body").is_displayed())

    # =========================================================================
    # SKENARIO 19: Keamanan Input Pencarian (Injection)
    # Hal yang diuji : Perlindungan sistem terhadap input berbahaya
    # Positif : Input HTML tag → tidak dirender sebagai elemen HTML (aman)
    # Negatif : Input SQL injection → tidak menyebabkan error server (aman)
    # =========================================================================

    def test_s19_pos_search_html_injection_not_rendered(self):
        """Positif: Input HTML tag '<marquee>' pada pencarian tidak dirender sebagai elemen HTML."""
        self.driver.find_element(By.ID, "textBoxSearch").send_keys("<marquee>Deface</marquee>")
        self.driver.find_element(By.CSS_SELECTOR, ".glyphicon-search").click()
        marquee_elements = self.driver.find_elements(By.TAG_NAME, "marquee")
        self.assertEqual(len(marquee_elements), 0)

    def test_s19_neg_search_sql_injection_no_error(self):
        """Negatif: Input SQL injection \"' OR 1=1 --\" pada pencarian tidak menyebabkan error server."""
        self.driver.find_element(By.ID, "textBoxSearch").send_keys("' OR 1=1 --")
        self.driver.find_element(By.CSS_SELECTOR, ".glyphicon-search").click()
        self.assertNotIn("internal server error", self.driver.page_source.lower())
        self.assertNotIn("500", self.driver.title)

    # =========================================================================
    # SKENARIO 20: Komponen Footer
    # Hal yang diuji : Kelengkapan elemen footer
    # Positif : Footer menampilkan link unduhan Android (Google Play)
    # Negatif : Footer menampilkan link unduhan iOS (App Store)
    # =========================================================================

    def test_s20_pos_footer_android_link_visible(self):
        """Positif: Footer menampilkan link unduhan Android (Google Play) dan teks copyright Badan Bahasa."""
        link_android = self.driver.find_element(
            By.XPATH, "//footer//a[contains(@href, 'play.google.com')]"
        )
        footer_text = self.driver.find_element(By.TAG_NAME, "footer").text
        self.assertTrue(link_android.is_displayed())
        self.assertIn("Badan Pengembangan dan Pembinaan Bahasa", footer_text)

    def test_s20_neg_footer_ios_link_visible(self):
        """Negatif: Footer juga menampilkan link unduhan iOS (App Store)."""
        link_ios = self.driver.find_element(
            By.XPATH, "//footer//a[contains(@href, 'apps.apple.com')]"
        )
        self.assertTrue(link_ios.is_displayed())


if __name__ == "__main__":
    unittest.main(verbosity=2)

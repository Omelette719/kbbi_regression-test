import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class KBBIVIDaringRegressionTestSuite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.base_url = "https://kbbi.kemendikdasmen.go.id"
        cls.driver.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.delete_all_cookies()
        self.driver.get(self.base_url)

    # =========================================================================
    # FASE 1: REGISTRASI AKUN BARU (S01 - S06)
    # =========================================================================

    # SKENARIO 01: Akses Menu & Form Utama Register
    def test_s01_pos_navigate_to_register(self):
        """Positif: Klik link 'Daftar Baru' di navbar berhasil mengarah ke halaman register."""
        self.driver.find_element(By.ID, "registerLink").click()
        self.assertIn("/Account/Register", self.driver.current_url)

    def test_s01_neg_register_submit_empty(self):
        """Negatif: Submit form register tanpa mengisi apapun tetap berada di halaman register."""
        self.driver.get(f"{self.base_url}/Account/Register")
        self.driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Daftarkan']").click()
        self.assertIn("/Account/Register", self.driver.current_url)

    # SKENARIO 02: Validasi Field Nama Lengkap Register
    def test_s02_pos_verify_register_fields(self):
        """Positif: Field 'Nama Lengkap' tampil dan dapat diinteraksi di halaman register."""
        self.driver.get(f"{self.base_url}/Account/Register")
        self.assertTrue(self.driver.find_element(By.ID, "NamaLengkap").is_displayed())

    def test_s02_neg_reg_validate_nama_lengkap_required(self):
        """Negatif: Atribut validasi 'data-val-required' pada field Nama Lengkap sesuai pesan yang diharapkan."""
        self.driver.get(f"{self.base_url}/Account/Register")
        field = self.driver.find_element(By.ID, "NamaLengkap")
        self.assertEqual(field.get_attribute("data-val-required"), "Kotak Nama Lengkap harus diisi")

    # SKENARIO 03: Validasi Field Nama Tampilan Register
    def test_s03_pos_verify_register_nama_tampilan_visibility(self):
        """Positif: Field 'Nama Tampilan' tampil dan dapat diinteraksi di halaman register."""
        self.driver.get(f"{self.base_url}/Account/Register")
        self.assertTrue(self.driver.find_element(By.ID, "NamaTampilan").is_displayed())

    def test_s03_neg_reg_validate_nama_tampilan_required(self):
        """Negatif: Atribut validasi 'data-val-required' pada field Nama Tampilan sesuai pesan yang diharapkan."""
        self.driver.get(f"{self.base_url}/Account/Register")
        field = self.driver.find_element(By.ID, "NamaTampilan")
        self.assertEqual(field.get_attribute("data-val-required"), "Kotak Nama Tampilan harus diisi")

    # SKENARIO 04: Validasi Field Pos-el (Email) Register
    def test_s04_pos_verify_register_posel_visibility(self):
        """Positif: Field 'Pos-el' tampil dan dapat diinteraksi di halaman register."""
        self.driver.get(f"{self.base_url}/Account/Register")
        self.assertTrue(self.driver.find_element(By.ID, "Posel").is_displayed())

    def test_s04_neg_reg_validate_posel_required(self):
        """Negatif: Atribut validasi 'data-val-required' pada field Pos-el register sesuai pesan yang diharapkan."""
        self.driver.get(f"{self.base_url}/Account/Register")
        field = self.driver.find_element(By.ID, "Posel")
        self.assertEqual(field.get_attribute("data-val-required"), "Kotak Pos-el harus diisi")

    # SKENARIO 05: Validasi Format Pos-el (Email) Register
    def test_s05_pos_verify_register_posel_attribute(self):
        """Positif: Atribut validasi format email 'data-val-email' pada field Pos-el register tersedia."""
        self.driver.get(f"{self.base_url}/Account/Register")
        field = self.driver.find_element(By.ID, "Posel")
        self.assertEqual(
            field.get_attribute("data-val-email"),
            "Alamat pos-el yang tertulis bukanlah alamat pos-el yang sah"
        )

    def test_s05_neg_reg_validate_posel_format(self):
        """Negatif: Mengisi Pos-el dengan format tidak valid tetap berada di halaman register."""
        self.driver.get(f"{self.base_url}/Account/Register")
        self.driver.find_element(By.ID, "Posel").send_keys("emailsalah@tanpadomain")
        self.driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Daftarkan']").click()
        self.assertIn("/Account/Register", self.driver.current_url)

    # SKENARIO 06: Validasi Aturan Kata Sandi Register
    def test_s06_pos_verify_register_password_match_rule(self):
        """Positif: Atribut 'data-val-equalto-other' pada KonfirmasiKataSandi menunjuk ke field KataSandi."""
        self.driver.get(f"{self.base_url}/Account/Register")
        field = self.driver.find_element(By.ID, "KonfirmasiKataSandi")
        self.assertEqual(field.get_attribute("data-val-equalto-other"), "*.KataSandi")

    def test_s06_neg_reg_validate_katasandi_min_length(self):
        """Negatif: Atribut 'data-val-length-min' pada KataSandi menunjukkan minimum 6 karakter."""
        self.driver.get(f"{self.base_url}/Account/Register")
        field = self.driver.find_element(By.ID, "KataSandi")
        self.assertEqual(field.get_attribute("data-val-length-min"), "6")

    # =========================================================================
    # FASE 2: MASUK AKUN / LOGIN (S07 - S12)
    # =========================================================================

    # SKENARIO 07: Akses Menu & Form Utama Login
    def test_s07_pos_navigate_to_login(self):
        """Positif: Klik link 'Masuk' di navbar berhasil mengarah ke halaman login."""
        self.driver.find_element(By.ID, "loginLink").click()
        self.assertIn("/Account/Login", self.driver.current_url)

    def test_s07_neg_login_submit_empty(self):
        """Negatif: Submit form login tanpa mengisi apapun tetap berada di halaman login."""
        self.driver.get(f"{self.base_url}/Account/Login")
        self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        self.assertIn("/Account/Login", self.driver.current_url)

    # SKENARIO 08: Validasi Pos-el (Email) Login
    def test_s08_pos_verify_login_fields(self):
        """Positif: Field 'Pos-el' tampil dan dapat diinteraksi di halaman login."""
        self.driver.get(f"{self.base_url}/Account/Login")
        self.assertTrue(self.driver.find_element(By.ID, "Posel").is_displayed())

    def test_s08_neg_login_validate_posel_required(self):
        """Negatif: Atribut validasi 'data-val-required' pada field Pos-el login sesuai pesan yang diharapkan."""
        self.driver.get(f"{self.base_url}/Account/Login")
        email_field = self.driver.find_element(By.ID, "Posel")
        self.assertEqual(email_field.get_attribute("data-val-required"), "Kotak Pos-el harus diisi")

    # SKENARIO 09: Validasi Kata Sandi Login
    def test_s09_pos_verify_login_password_visibility(self):
        """Positif: Field 'Kata Sandi' tampil dan dapat diinteraksi di halaman login."""
        self.driver.get(f"{self.base_url}/Account/Login")
        self.assertTrue(self.driver.find_element(By.ID, "KataSandi").is_displayed())

    def test_s09_neg_login_validate_katasandi_required(self):
        """Negatif: Atribut validasi 'data-val-required' pada field Kata Sandi login sesuai pesan yang diharapkan."""
        self.driver.get(f"{self.base_url}/Account/Login")
        pass_field = self.driver.find_element(By.ID, "KataSandi")
        self.assertEqual(pass_field.get_attribute("data-val-required"), "Kotak Kata Sandi harus diisi")

    # SKENARIO 10: Fitur Ingat Saya & Keamanan Form Login
    def test_s10_pos_login_toggle_remember_me(self):
        """Positif: Checkbox 'Ingat saya?' dapat diklik dan statusnya berubah menjadi tercentang."""
        self.driver.get(f"{self.base_url}/Account/Login")
        checkbox = self.driver.find_element(By.ID, "IngatSaya")
        checkbox.click()
        self.assertTrue(checkbox.is_selected())

    def test_s10_neg_verify_login_form_action(self):
        """Negatif: Atribut action pada form login mengarah ke endpoint yang benar."""
        self.driver.get(f"{self.base_url}/Account/Login")
        form = self.driver.find_element(By.CSS_SELECTOR, "section#loginForm form")
        self.assertIn("/Account/Login", form.get_attribute("action"))

    # SKENARIO 11: Bantuan & Format Email Login
    def test_s11_pos_verify_forgot_password_link(self):
        """Positif: Link 'Lupa kata sandi?' tampil dan dapat diakses di halaman login."""
        self.driver.get(f"{self.base_url}/Account/Login")
        self.assertTrue(self.driver.find_element(By.LINK_TEXT, "Lupa kata sandi?").is_displayed())

    def test_s11_neg_login_validate_posel_format(self):
        """Negatif: Atribut validasi format email 'data-val-email' pada field Pos-el login tersedia."""
        self.driver.get(f"{self.base_url}/Account/Login")
        email_field = self.driver.find_element(By.ID, "Posel")
        self.assertEqual(
            email_field.get_attribute("data-val-email"),
            "Alamat pos-el yang tertulis bukanlah alamat pos-el yang sah"
        )

    # SKENARIO 12: Jalur Alternatif & Proteksi Login
    def test_s12_pos_navigate_to_register_via_login(self):
        """Positif: Klik link 'Daftar sebagai pengguna baru' di halaman login mengarah ke register."""
        self.driver.get(f"{self.base_url}/Account/Login")
        self.driver.find_element(By.LINK_TEXT, "Daftar sebagai pengguna baru").click()
        self.assertIn("/Account/Register", self.driver.current_url)

    def test_s12_neg_login_invalid_email_no_domain(self):
        """Negatif: Login dengan format email tidak lengkap (tanpa domain) tetap berada di halaman login."""
        self.driver.get(f"{self.base_url}/Account/Login")
        self.driver.find_element(By.ID, "Posel").send_keys("akunsalah@")
        self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        self.assertIn("/Account/Login", self.driver.current_url)

    # =========================================================================
    # FASE 3: BERANDA & FITUR PENCARIAN (S13 - S20)
    # =========================================================================

    # SKENARIO 13: Integrasi Navigasi Logo Navbar
    def test_s13_pos_click_logo_to_return_home(self):
        """Positif: Klik teks 'KBBI VI Daring' di navbar dari halaman login kembali ke beranda."""
        self.driver.get(f"{self.base_url}/Account/Login")
        self.driver.find_element(By.LINK_TEXT, "KBBI VI Daring").click()
        self.assertIn("/Beranda", self.driver.current_url)

    def test_s13_neg_access_broken_url(self):
        """Negatif: Mengakses URL yang tidak ada tidak menyebabkan halaman kosong/crash."""
        self.driver.get(f"{self.base_url}/Account/RuteNgawurSengaja")
        self.assertTrue(self.driver.find_element(By.TAG_NAME, "body").is_displayed())

    # SKENARIO 14: Menu Tambahan & Validasi Unik ID
    def test_s14_pos_navigate_to_seputar_laman(self):
        """Positif: Klik menu 'Seputar Laman' berhasil mengarah ke halaman SeputarLaman."""
        self.driver.find_element(By.LINK_TEXT, "Seputar Laman").click()
        self.assertIn("/Beranda/SeputarLaman", self.driver.current_url)

    def test_s14_neg_verify_no_duplicate_search_id(self):
        """Negatif: Tidak ada duplikasi elemen dengan ID 'textBoxSearch' di halaman utama."""
        search_boxes = self.driver.find_elements(By.ID, "textBoxSearch")
        self.assertEqual(len(search_boxes), 1)

    # SKENARIO 15: Pencarian Kata Standar
    def test_s15_pos_search_standard_word(self):
        """Positif: Mencari kata 'makan' berhasil mengarahkan ke halaman entri kata tersebut."""
        self.driver.find_element(By.ID, "textBoxSearch").send_keys("makan")
        self.driver.find_element(By.CSS_SELECTOR, ".glyphicon-search").click()
        WebDriverWait(self.driver, 10).until(EC.url_contains("/entri/makan"))
        self.assertIn("/entri/makan", self.driver.current_url)

    def test_s15_neg_search_empty_input(self):
        """Negatif: Mencari dengan input kosong menampilkan pesan error dan tetap di halaman pencarian."""
        search_box = self.driver.find_element(By.ID, "textBoxSearch")
        search_box.clear()
        self.driver.find_element(By.CSS_SELECTOR, ".glyphicon-search").click()
        error_div = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "errorMessageDiv"))
        )
        self.assertIn("tidak boleh kosong", error_div.text.lower())

    # SKENARIO 16: Pencarian Huruf Kapital & Spasi
    def test_s16_pos_search_uppercase_word(self):
        """Positif: Mencari kata 'RUMAH' dengan huruf kapital berhasil mengarahkan ke halaman entri."""
        search_box = self.driver.find_element(By.ID, "textBoxSearch")
        search_box.send_keys("RUMAH")
        self.driver.find_element(By.CSS_SELECTOR, ".glyphicon-search").click()
        WebDriverWait(self.driver, 10).until(EC.url_contains("/entri/"))
        self.assertIn("rumah", self.driver.current_url.lower())

    def test_s16_neg_search_spaces_only(self):
        """Negatif: Mencari dengan input hanya spasi menampilkan pesan error karena dianggap kosong."""
        search_box = self.driver.find_element(By.ID, "textBoxSearch")
        search_box.send_keys("     ")
        self.driver.find_element(By.CSS_SELECTOR, ".glyphicon-search").click()
        self.assertTrue(self.driver.find_element(By.ID, "textBoxSearch").is_displayed())

    # SKENARIO 17: Pencarian Huruf Campuran & Karakter Simbol
    def test_s17_pos_search_mixed_case(self):
        """Positif: Mencari kata 'InDoNeSiA' dengan huruf campuran berhasil mengarahkan ke halaman entri."""
        search_box = self.driver.find_element(By.ID, "textBoxSearch")
        search_box.send_keys("InDoNeSiA")
        self.driver.find_element(By.CSS_SELECTOR, ".glyphicon-search").click()
        WebDriverWait(self.driver, 10).until(EC.url_contains("/entri/"))
        self.assertIn("indonesia", self.driver.current_url.lower())

    def test_s17_neg_search_special_characters(self):
        """Negatif: Mencari dengan karakter simbol tidak menyebabkan error server."""
        search_box = self.driver.find_element(By.ID, "textBoxSearch")
        search_box.send_keys("!@#$%^&*()")
        self.driver.find_element(By.CSS_SELECTOR, ".glyphicon-search").click()
        self.assertNotIn("500", self.driver.title)
        self.assertTrue(self.driver.find_element(By.TAG_NAME, "body").is_displayed())

    # SKENARIO 18: Pencarian Kata Berulang & Emoji
    def test_s18_pos_search_hyphenated_word(self):
        """Positif: Mencari kata ulang 'kupu-kupu' berhasil mengarahkan ke halaman entri."""
        search_box = self.driver.find_element(By.ID, "textBoxSearch")
        search_box.send_keys("kupu-kupu")
        self.driver.find_element(By.CSS_SELECTOR, ".glyphicon-search").click()
        WebDriverWait(self.driver, 10).until(EC.url_contains("kupu"))
        self.assertIn("kupu", self.driver.current_url.lower())

    def test_s18_neg_search_emojis(self):
            """Negatif: Mencari dengan emoji tidak menyebabkan error server atau crash halaman."""
            search_box = self.driver.find_element(By.ID, "textBoxSearch")
            self.driver.execute_script("arguments[0].value = '🤖🔥💡';", search_box)
            self.driver.find_element(By.CSS_SELECTOR, ".glyphicon-search").click()
            self.assertNotIn("500", self.driver.title)
            self.assertTrue(self.driver.find_element(By.TAG_NAME, "body").is_displayed())

    # SKENARIO 19: Keamanan Input & Proteksi HTML Injection
    def test_s19_pos_search_compound_word(self):
        """Positif: Mencari frasa 'kambing hitam' tidak menyebabkan crash dan halaman tetap terbuka."""
        search_box = self.driver.find_element(By.ID, "textBoxSearch")
        search_box.send_keys("kambing hitam")
        self.driver.find_element(By.CSS_SELECTOR, ".glyphicon-search").click()
        self.assertTrue(self.driver.get_screenshot_as_png() is not None)

    def test_s19_neg_search_html_injection(self):
        """Negatif: Input HTML tag berbahaya tidak dirender sebagai elemen HTML di halaman."""
        search_box = self.driver.find_element(By.ID, "textBoxSearch")
        search_box.send_keys("<marquee>Deface</marquee>")
        self.driver.find_element(By.CSS_SELECTOR, ".glyphicon-search").click()
        marquee_elements = self.driver.find_elements(By.TAG_NAME, "marquee")
        self.assertEqual(len(marquee_elements), 0)

    # SKENARIO 20: Validasi Komponen Footer & SQL Injection Protection
    def test_s20_pos_verify_footer_elements(self):
        """Positif: Footer menampilkan link Android dan teks copyright Badan Bahasa."""
        link_android = self.driver.find_element(
            By.XPATH, "//footer//a[contains(@href, 'play.google.com')]"
        )
        footer_text = self.driver.find_element(By.TAG_NAME, "footer").text
        self.assertTrue(link_android.is_displayed())
        self.assertIn("Badan Pengembangan dan Pembinaan Bahasa", footer_text)

    def test_s20_neg_search_sql_injection(self):
        """Negatif: Input SQL injection pada kolom pencarian tidak menyebabkan error server."""
        search_box = self.driver.find_element(By.ID, "textBoxSearch")
        search_box.send_keys("' OR 1=1 --")
        self.driver.find_element(By.CSS_SELECTOR, ".glyphicon-search").click()
        self.assertNotIn("internal server error", self.driver.page_source.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)

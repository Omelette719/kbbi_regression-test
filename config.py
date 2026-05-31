# config.py - Konfigurasi global untuk semua test
# Kredensial dibaca dari file .env (tidak hardcode di sini)

import os
from dotenv import load_dotenv

# Load variabel dari file .env
load_dotenv()

BASE_URL      = os.getenv("BASE_URL", "https://kbbi.kemendikdasmen.go.id")
TEST_EMAIL    = os.getenv("TEST_EMAIL")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")

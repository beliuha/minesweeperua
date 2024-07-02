from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import json
import gspread
import os

# Завантаження змінних середовища з файлу .env
load_dotenv()
# Отримання JSON-рядка сервісного облікового запису Google з змінних середовища
service_account_info_str = os.getenv('GOOGLE_SERVICE_ACCOUNT_KEY')
# Парсинг JSON-рядка у Python об'єкт
service_account_info = json.loads(service_account_info_str)
# ІD таблиці
SHEET_ID = os.getenv("SHEET_ID")

# Налаштування доступу до Google Sheets
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
client = gspread.authorize(creds)

sheet = client.open_by_key(SHEET_ID)

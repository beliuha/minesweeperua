import aiofiles
import json
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from app.onetimesecret import OneTimeSecret

# Асинхронна функція для генерації пароля
async def generate_password():
    # Генеруємо новий ключ (шифрування пароля)
    return Fernet.generate_key()

# Асинхронна функція для читання JSON файлу
async def read_json(file):
    try:
        async with aiofiles.open(file, "r") as f:
            data = await f.read()
            return json.loads(data)
    except FileNotFoundError:
        return {"passwords": []}

# Асинхронна функція для запису JSON файлу
async def write_json(file, data):
    async with aiofiles.open(file, "w") as f:
        await f.write(json.dumps(data, indent=4))

# Асинхронна функція для створення пароля
async def create_pass():
    data = await read_json('passwords.json')

    # Генеруємо новий пароль
    password = await generate_password()

    # Передаємо зашифрований пароль
    onetime = OneTimeSecret().create(password)

    # Додаємо новий зашифрований пароль до списку
    data["passwords"].append({
        "password": onetime.decode('utf-8'),
        "time": datetime.today().strftime('%d.%m.%Y %H:%M:%S'),
    })

    # Зберігаємо оновлений список паролів у файлі JSON
    await write_json('passwords.json', data)

    print(f"Новий пароль успішно збережено в 'passwords.json'")

    return password

class Crypto():
    def __init__(self):
        self.password = None

    async def initialize(self):
        print("Генеруємо новий пароль")
        self.password = await create_pass()

    async def check_password(self):
        data = await read_json('passwords.json')

        # Перевіряємо актуальність
        if data["passwords"]:
            last_password_time = datetime.strptime(data["passwords"][-1]["time"], '%d.%m.%Y %H:%M:%S')
            current_time = datetime.today()
            if current_time - last_password_time < timedelta(hours=24):
                print("Last password is still valid")
            else:
                await self.initialize()

    async def encrypt(self, plaintext):
        if self.password is None:
            await self.initialize()
        
        cipher_suite = Fernet(self.password)
        plaintext_bytes = plaintext.encode('cp1251')
        encrypted_text = cipher_suite.encrypt(plaintext_bytes)
        return encrypted_text.decode('cp1251')

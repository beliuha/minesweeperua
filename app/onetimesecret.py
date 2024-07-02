from dotenv import load_dotenv
import requests
import base64
import os

load_dotenv()

class OneTimeSecret():
    def __init__(self):
        self.email = os.getenv('ONE_TIME_EMAIL')
        self.api = os.getenv('ONE_TIME_API')

    def status(self):
        # Перевіряємо доступність api
        respounce = requests.get('https://onetimesecret.com/api/v1/status')

        if respounce.status_code == 200:
            status = True
        else:
            status = False

        return status
    
    def create(self, secret):
        if self.status:
            # Дані, які ви надсилаєте
            url = 'https://onetimesecret.com/api/v1/share'
            data = {
                'secret': secret,
                'ttl': 3600
            }

            # Шифруємо в base64
            credentials = f'{self.email}:{self.api}'
            encoded_credentials = base64.b64encode(credentials.encode()).decode('utf-8')
            # Створення headers для авторизації
            headers = {
                'Authorization': f'Basic {encoded_credentials}'
            }

            # Виконання POST-запиту з використанням headers і даних
            response = requests.post(url, data=data, headers=headers)

            # Виведення результату запиту
            if response.status_code == 200:
                link = f'https://onetimesecret.com/secret/{response.json()["secret_key"]}'
                return base64.b64encode(link.encode())
            else:
                print('Помилка створення')
        else:
            print("OneTimeSecret API недоступний")

    def get_secret(self):
        # Якщо буде потреба - додам
        # Можна буде пакетно вивантажувати ключі
        if self.status:
            pass

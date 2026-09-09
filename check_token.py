import requests

# Вставь сюда свой токен (только для проверки!)
token = '8840994282:AAFmZw7hSCHVL5P7EWWyZSVANUh6OEEwcZs'
url = f'https://api.telegram.org/bot{token}/getMe'

r = requests.get(url)
print('Статус код:', r.status_code)
print(r.json())

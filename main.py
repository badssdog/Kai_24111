import requests

# Базовый URL запущенного FastAPI-приложения
BASE_URL = "http://127.0.0.1:8000"

# Данные нового пользователя
user_data = {
    "username": "salavat_user",
    "password": "secure_password_123"
}

print("1. Регистрация пользователя...")
reg_response = requests.post(f"{BASE_URL}/register", json=user_data)
if reg_response.status_code == 201:
    print("Успешно зарегистрирован:", reg_response.json())
else:
    print("Ответ регистрации:", reg_response.json())

print("\n2. Получение JWT-токена (логин)...")
# FastAPI OAuth2PasswordRequestForm ожидает данные в формате form-urlencoded
token_payload = {
    "username": user_data["username"],
    "password": user_data["password"]
}
token_response = requests.post(f"{BASE_URL}/token", data=token_payload)

if token_response.status_code == 200:
    token_data = token_response.json()
    access_token = token_data.get("access_token")
    print("Токен успешно получен!")
else:
    print("Ошибка авторизации:", token_response.text)
    exit()

# Заголовки с передачей Bearer-токена для защищенных эндпоинтов
headers = {
    "Authorization": f"Bearer {access_token}"
}

print("\n3. Создание новой задачи...")
new_task = {
    "title": "Написать скрипт на Python",
    "description": "Проверить работу FastAPI бэкенда через requests",
    "priority": 3,
    "deadline": "2026-11-01"
}
task_response = requests.post(f"{BASE_URL}/tasks/", json=new_task, headers=headers)
print("Созданная задача:", task_response.json())

print("\n4. Получение списка задач текущего пользователя...")
tasks_response = requests.get(f"{BASE_URL}/tasks/", headers=headers)
print("Список задач:", tasks_response.json())
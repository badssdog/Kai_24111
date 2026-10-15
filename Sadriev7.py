import asyncio
import aiohttp

# 1. Список URL-адресов
urls = [
    'https://www.python.org',
    'https://www.google.com',
    'https://non-existent-domain-12345.org'
]


# 2. Корутина check_status для выполнения GET-запроса
async def check_status(session, url):
    try:
        async with session.get(url) as response:
            # 3. Проверяем код ответа
            if response.status == 200:
                return f"{url}: OK"
            else:
                return f"{url}: Ошибка {response.status}"
    except Exception:
        # 4. Перехватываем ошибки соединения (например, если домен не существует)
        return f"{url}: Не удалось подключиться"


# Главная функция программы
async def main():
    # Создаем общую сессию aiohttp
    async with aiohttp.ClientSession() as session:
        # 5. Создаем список задач и запускаем их одновременно с помощью asyncio.gather
        tasks = [check_status(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

        # Выводим результаты на экран
        for result in results:
            print(result)


if __name__ == "__main__":
    asyncio.run(main())
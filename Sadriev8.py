import asyncio


# 1. Создаем корутину long_running_task, которая имитирует долгую операцию
async def long_running_task():
    print("Фоновая задача начала работу...")
    await asyncio.sleep(5)  # Ждем 5 секунд
    print("Фоновая задача завершена.")


# Главная функция программы
async def main():
    # 2. Запускаем long_running_task в фоне с помощью asyncio.create_task()
    task = asyncio.create_task(long_running_task())

    # 3. Сразу после запуска фоновой задачи печатаем сообщение
    print("Основная программа продолжает работу...")

    # Цикл: 3 раза с интервалом в 1 секунду печатает сообщение
    for i in range(3):
        await asyncio.sleep(1)
        print("Основная программа работает...")

    # Дожидаемся завершения фоновой задачи в конце
    await task


if __name__ == "__main__":
    asyncio.run(main())
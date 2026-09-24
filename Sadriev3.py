import random
import string


def get_yes_no(prompt):
    """Вспомогательная функция для запроса да/нет."""
    while True:
        choice = input(prompt + " (д/н): ").strip().lower()
        if choice in ["д", "да", "y", "yes"]:
            return True
        elif choice in ["н", "нет", "n", "no"]:
            return False
        print("Пожалуйста, введите 'д' (да) или 'н' (нет).")


def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    """Генерация пароля с учетом длины и выбранных наборов символов."""
    pools = []

    if use_upper:
        pools.append(string.ascii_uppercase)
    if use_lower:
        pools.append(string.ascii_lowercase)
    if use_digits:
        pools.append(string.digits)
    if use_symbols:
        pools.append(string.punctuation)

    # Проверка: выбран ли хотя бы один набор
    if not pools:
        print("\nОшибка: должен быть выбран хотя бы один тип символов!")
        return None

    all_chars = "".join(pools)
    password_chars = []

    # Если длина позволяет, гарантируем по одному символу каждого типа
    if length >= len(pools):
        for pool in pools:
            password_chars.append(random.choice(pool))

    # Заполняем оставшуюся (или всю) длину случайными символами из общего набора
    for _ in range(length - len(password_chars)):
        password_chars.append(random.choice(all_chars))

    # Перемешиваем символы между собой
    random.shuffle(password_chars)

    return "".join(password_chars)


def main():
    print("=== Консольный генератор паролей ===")

    # Запрос длины пароля
    while True:
        try:
            length = int(input("\nВведите желаемую длину пароля: "))
            if length <= 0:
                print("Длина пароля должна быть больше 0.")
                continue
            break
        except ValueError:
            print("Ошибка: введите целое число.")

    # Запрос категорий символов
    print("\nВыберите типы символов:")
    use_upper = get_yes_no("Использовать заглавные буквы (A-Z)?")
    use_lower = get_yes_no("Использовать строчные буквы (a-z)?")
    use_digits = get_yes_no("Использовать цифры (0-9)?")
    use_symbols = get_yes_no("Использовать спецсимволы (!@#$%...)?")

    # Генерация
    password = generate_password(
        length, use_upper, use_lower, use_digits, use_symbols
    )

    if password:
        print("\n" + "=" * 35)
        print(f"Сгенерированный пароль: {password}")
        print("=" * 35)


if __name__ == "__main__":
    main()
import csv
import time
import requests
from bs4 import BeautifulSoup


def parse_habr_news(pages_count=2):
    # Заголовки, чтобы сервер не блокировал простой скрипт
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    scraped_data = []

    print("--- Начинаем сбор данных ---")

    for page in range(1, pages_count + 1):
        url = f"https://habr.com/ru/articles/page{page}/"
        print(f"Обработка страницы {page}: {url}")

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Ошибка при запросе страницы {page}: {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        # Находим все карточки статей
        articles = soup.find_all("article", class_="tm-articles-list__item")

        for article in articles:
            # 1. Извлечение заголовка и ссылки
            title_tag = article.find("a", class_="tm-title__link")
            if not title_tag:
                continue

            title = title_tag.get_text(strip=True)  # Очистка от пробелов
            link = "https://habr.com" + title_tag.get("href", "")

            # 2. Извлечение автора
            author_tag = article.find("a", class_="tm-user-info__username")
            author = (
                author_tag.get_text(strip=True) if author_tag else "Не указан"
            )

            # 3. Извлечение времени публикации
            time_tag = article.find("time")
            publication_time = (
                time_tag.get("title")
                if time_tag and time_tag.has_attr("title")
                else "Не указано"
            )

            # Сохранение очищенной записи
            scraped_data.append(
                {
                    "title": title,
                    "author": author,
                    "publication_time": publication_time,
                    "link": link,
                }
            )

        # Вежливая пауза между запросами (этика веб-скрейпинга)
        time.sleep(1.5)

    print(f"Сбор завершен. Найдено записей: {len(scraped_data)}")
    return scraped_data


def save_to_csv(data, filename="habr_articles.csv"):
    if not data:
        print("Нет данных для сохранения.")
        return

    # Запись в CSV с правильной кодировкой для кириллицы (utf-8-sig)
    fieldnames = ["title", "author", "publication_time", "link"]

    with open(filename, mode="w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"Данные успешно сохранены в файл: {filename}")


if __name__ == "__main__":
    # Сбор данных с первых 2 страниц
    news = parse_habr_news(pages_count=2)
    save_to_csv(news)
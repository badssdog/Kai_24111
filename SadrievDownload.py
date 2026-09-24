import os
import shutil
from pathlib import Path

# Автоматическое определение папки Загрузки текущего пользователя
DOWNLOADS_DIR = Path.home() / "Downloads"

# Категории и входящие в них расширения
CATEGORIES = {
    "Изображения": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".bmp", ".ico"],
    "Документы": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv", ".epub", ".djvu"],
    "Видео": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"],
    "Аудио": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Архивы": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".iso"],
    "Программы": [".exe", ".msi", ".dmg", ".pkg", ".deb"],
    "Код и Данные": [".py", ".js", ".html", ".css", ".json", ".xml", ".sql", ".sh", ".ipynb"],
}

# Расширения недокачанных файлов, которые нужно пропускать
IGNORE_EXTENSIONS = {".crdownload", ".part", ".tmp", ".download"}


def get_unique_path(target_path: Path) -> Path:
    """Генерирует уникальное имя файла, если в папке назначения уже есть файл с таким же именем."""
    if not target_path.exists():
        return target_path

    stem = target_path.stem
    suffix = target_path.suffix
    parent = target_path.parent
    counter = 1

    while True:
        new_path = parent / f"{stem}_{counter}{suffix}"
        if not new_path.exists():
            return new_path
        counter += 1


def organize_downloads():
    if not DOWNLOADS_DIR.exists():
        print(f"Ошибка: папка не найдена по адресу {DOWNLOADS_DIR}")
        return

    moved_count = 0

    for item in DOWNLOADS_DIR.iterdir():
        # Пропускаем вложенные директории и скрытые файлы
        if item.is_dir() or item.name.startswith("."):
            continue

        extension = item.suffix.lower()

        # Пропускаем файлы в процессе скачивания
        if extension in IGNORE_EXTENSIONS or not extension:
            continue

        # Поиск подходящей категории
        target_folder_name = "Другое"
        for category, extensions in CATEGORIES.items():
            if extension in extensions:
                target_folder_name = category
                break

        # Создание целевой папки при необходимости
        target_dir = DOWNLOADS_DIR / target_folder_name
        target_dir.mkdir(exist_ok=True)

        # Безопасное перемещение
        destination = get_unique_path(target_dir / item.name)
        shutil.move(str(item), str(destination))
        print(f"✓ {item.name} -> {target_folder_name}/")
        moved_count += 1

    print(f"\nГотово! Перемещено файлов: {moved_count}")


if __name__ == "__main__":
    organize_downloads()

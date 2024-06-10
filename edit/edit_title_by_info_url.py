import os
import re
from transliterate import translit
from bs4 import BeautifulSoup
from tqdm import tqdm
import multiprocessing

"""
Скрипт извлекает имя папки из пути папки в кокоторой лежит html
транслитерирует его на русский, добавляет " - Новости на ЕТВ" и обновляет тег <title>
"_" и "-" преобразовываются в пробел
если в названии одно слово, то берется еще папка на один уровень выше
"""

def process_file(file_path):
    # Извлекаем имя папки из пути к файлу
    folder_name = os.path.basename(os.path.dirname(file_path))
    parent_folder_name = os.path.basename(os.path.dirname(os.path.dirname(file_path)))

    # Проверяем количество слов в имени папки
    if len(re.split(r'[_\- ]+', folder_name)) < 2:
        combined_name = f"{parent_folder_name} {folder_name}"
    else:
        combined_name = folder_name

    # Заменяем _ и - на пробелы и транслитерируем имя папки на русский
    combined_name = combined_name.replace('_', ' ').replace('-', ' ')
    transliterated_name = translit(combined_name, 'ru').capitalize()
    # Создаем текст для тега <title>
    title_text = f"{transliterated_name} - Новости на ЕТВ"

    try:
        # Открываем и читаем HTML файл
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

        # Обновляем или создаем тег <title>
        if soup.title:
            soup.title.string = title_text
        else:
            new_title_tag = soup.new_tag("title")
            new_title_tag.string = title_text
            soup.head.append(new_title_tag)

        # Сохраняем изменения в HTML файл
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))

        return True
    except Exception as e:
        print(f"Ошибка при обработке {file_path}: {e}")
        return False


def main():
    # Читаем пути к файлам из all_html.txt
    with open('all_directory.txt', 'r', encoding='utf-8') as file:
        file_paths = [line.strip() for line in file.readlines()]

    # Используем многопроцессорный пул для параллельной обработки файлов
    with multiprocessing.Pool() as pool:
        results = list(tqdm(pool.imap(process_file, file_paths), total=len(file_paths)))

    print(f"Успешно обработано {results.count(True)} из {len(file_paths)} файлов.")


if __name__ == "__main__":
    main()


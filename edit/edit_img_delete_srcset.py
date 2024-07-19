# Импорт необходимых модулей
import os
from tqdm import tqdm
from bs4 import BeautifulSoup

# Этот скрипт читает файл all_directory.txt, который содержит пути к HTML файлам.
# Для каждого файла он удаляет атрибуты srcset из тегов img и сохраняет изменения.
# В консоли выводится индикатор прогресса для всех файлов.

# Путь к файлу со списком HTML файлов
file_list_path = 'all_directory.txt'

# Чтение списка файлов
with open(file_list_path, 'r', encoding='utf-8') as f:
    file_paths = f.read().splitlines()

# Обработка каждого HTML файла
for file_path in tqdm(file_paths, desc='Processing files'):
    # Проверка, существует ли файл
    if os.path.exists(file_path):
        # Чтение содержимого HTML файла
        with open(file_path, 'r', encoding='utf-8') as html_file:
            soup = BeautifulSoup(html_file, 'html.parser')

        # Поиск всех тегов img и удаление атрибута srcset
        for img in soup.find_all('img'):
            if 'srcset' in img.attrs:
                del img.attrs['srcset']

        # Запись изменений обратно в файл
        with open(file_path, 'w', encoding='utf-8') as html_file:
            html_file.write(str(soup))
    else:
        print(f'File not found: {file_path}')

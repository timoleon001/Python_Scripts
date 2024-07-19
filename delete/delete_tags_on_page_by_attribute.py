# Импорт необходимых библиотек
import os
from bs4 import BeautifulSoup
from tqdm import tqdm

# Этот скрипт обрабатывает HTML файлы, указанные в all_directory.txt,
# и удаляет из них теги <link> с атрибутом rel='shortlink'.

# Путь к файлу со списком HTML файлов
file_list_path = 'all_directory.txt'


# Функция для удаления тегов <link rel='shortlink'> из HTML файла
def remove_shortlink_tag(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

        # Найти и удалить все теги <link> с атрибутом rel='shortlink'
        for tag in soup.find_all('link', rel='shortlink'):
            tag.decompose()

        # Перезаписать файл с изменениями
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))
    except Exception as e:
        print(f"Ошибка при обработке файла {file_path}: {e}")


# Чтение списка файлов из all_directory.txt
with open(file_list_path, 'r', encoding='utf-8') as file_list:
    files = file_list.read().splitlines()

# Обработка файлов с индикатором прогресса
for file_path in tqdm(files, desc="Обработка HTML файлов"):
    remove_shortlink_tag(file_path)

# Импорт необходимых библиотек
import os
from bs4 import BeautifulSoup
from tqdm import tqdm

# Этот скрипт обрабатывает HTML файлы, указанные в all_directory.txt,
# и удаляет из них теги <link> с атрибутом rel='shortlink'.

# Путь к файлу со списком HTML файлов
file_list_path = 'all_directory.txt'
# Тег и атрибут для удаления
tag_to_remove = 'link'
attribute_key = 'type'
attribute_value = 'application/json+oembed'


# Функция для удаления тегов с определенным атрибутом из HTML файла
def remove_tag_with_attribute(file_path, tag, attr_key, attr_value):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

        # Найти и удалить все теги с указанным атрибутом
        for tag in soup.find_all(tag, {attr_key: attr_value}):
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
    remove_tag_with_attribute(file_path, tag_to_remove, attribute_key, attribute_value)

import os
import re
from tqdm import tqdm

# Скрипт ищет теги <img> с атрибутом src, который заканчивается на '/', и удаляет его.
# Отредактированные пути к изображениям сохраняются в файл 'all_edit_images.txt'

# Путь к каталогу
directory = 'D://OSPanel//domains//ekburg.tv'

# Регулярное выражение для поиска тега <img> с src, заканчивающимся на /
img_tag_pattern = re.compile(r'(<img[^>]*src="([^"]*/))"[^>]*>', re.IGNORECASE)

# Список для хранения путей всех отредактированных изображений
edited_images = []

# Функция для обработки html файлов
def process_html_file(file_path):
    global edited_images
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Найти все совпадения
    matches = img_tag_pattern.findall(content)
    if matches:
        # Удалить слеш в конце
        new_content = img_tag_pattern.sub(lambda m: m.group(0).replace(m.group(2), m.group(2)[:-1]), content)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        # Добавить отредактированные пути в список
        edited_images.extend([match[1][:-1] for match in matches])

# Функция для обхода всех html файлов в каталоге с учетом вложенности
def process_directory(directory):
    # Подсчёт количества html файлов для tqdm
    file_count = sum(len(files) for _, _, files in os.walk(directory) if any(file.endswith('.html') for file in files))
    with tqdm(total=file_count, desc="Processing HTML files") as pbar:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.html'):
                    process_html_file(os.path.join(root, file))
                    pbar.update(1)

# Обработка директории
process_directory(directory)

# Запись отредактированных изображений в файл
with open('all_edit_images.txt', 'w', encoding='utf-8') as file:
    for image_path in edited_images:
        file.write(image_path + '\n')

print("Processing complete. Edited image sources saved in all_edit_images.txt.")

import os
import urllib.parse
from bs4 import BeautifulSoup
from tqdm import tqdm

def load_and_decode_urls(file_path):
    """Загрузка строк из файла и декодирование URL-символов."""
    decoded_urls = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            decoded_line = urllib.parse.unquote(line.strip())
            decoded_urls.append(decoded_line.lower())
    return decoded_urls

def normalize_url(url):
    """Удаление только протоколов из URL."""
    if url:
        url = url.lower().strip()
        return url
    return url

def ensure_full_url(url):
    """Убеждаемся, что URL содержит нужный базовый адрес или уже является полным URL."""
    if not url.startswith(('http://', 'https://')):
        return f"https://ekburg.tv{url}"
    return url

def replace_attribute_values(html_file_path, values_590, values_280, modified_files, global_index_280):
    """Замена значений href в тегах <a> HTML файла, если они присутствуют в values_590."""
    if not os.path.exists(html_file_path):
        print(f"File not found: {html_file_path}")
        return 0, global_index_280

    with open(html_file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')

    # Ищем только <a> элементы с href атрибутом
    elements = soup.find_all('a', href=True)
    matched_count = 0  # Для подсчета совпадений

    for element in elements:
        url_value = element['href']
        if url_value:
            url_value = ensure_full_url(url_value)
            normalized_url = normalize_url(url_value)
            if normalized_url in values_590:
                new_url_value = values_280[global_index_280 % len(values_280)]
                element['href'] = new_url_value
                global_index_280 += 1
                matched_count += 1

    if matched_count > 0:
        with open(html_file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))
        modified_files.append(html_file_path)  # Добавляем измененный файл в список

    return matched_count, global_index_280

# Example usage:
values_590 = load_and_decode_urls('others.txt')  # Содержит список URL, которые имеют код ответа 404 или 301 и будут заменены
values_280 = load_and_decode_urls('file_no_frog.txt')  # Содержит список новых значений URL, которыми заменяются найденные в others.txt
html_files_paths = load_and_decode_urls('files_for_editing.txt')  # Список путей к HTML-файлам, которые найдены краулингом и будут изменены скриптом

total_files = len(html_files_paths)
modified_files = []  # Список для хранения измененных файлов
global_index_280 = 0  # Глобальный индекс для значений из values_280

# Использование tqdm для обновления прогресса на одной строке
with tqdm(total=total_files, desc="Processing HTML files", unit="file") as pbar:
    for html_file_path in html_files_paths:
        _, global_index_280 = replace_attribute_values(html_file_path, values_590, values_280, modified_files, global_index_280)
        pbar.update(1)  # Обновление прогресса на одну единицу

# Запись измененных файлов в modified_files.txt
with open('modified_files.txt', 'w', encoding='utf-8') as file:
    for modified_file in modified_files:
        file.write(f"{modified_file}\n")

print(f"Total modified files: {len(modified_files)}")

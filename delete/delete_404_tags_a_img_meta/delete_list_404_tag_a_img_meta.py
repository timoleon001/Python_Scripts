import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from tqdm import tqdm
from multiprocessing import Pool, Manager

# Конфигурация: включить/выключить удаление тегов
REMOVE_A_TAGS = True
REMOVE_IMG_TAGS = True
REMOVE_META_TAGS = True
REMOVE_LINK_TAGS = True

# Каталог для сканирования
directory_to_scan = "D:\\OSPanel\\domains\\vokzal-simferopol.info"
# Файл с URL-адресами для удаления
urls_file_path = "urls_for_delete.txt"

def get_absolute_url(base_url, relative_url):
    return requests.compat.urljoin(base_url, relative_url)

def load_urls_to_remove(file_path):
    urls_to_remove = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                url = line.strip()
                if url:
                    urls_to_remove.append(url)
    except FileNotFoundError:
        print(f"Файл '{file_path}' не найден.")

    return urls_to_remove

def normalize_url(url):
    parsed = urlparse(url.lower())
    normalized = parsed._replace(netloc=parsed.netloc.replace('www.', '')).geturl()
    return normalized

def remove_tag_with_matching_attr(file_path, normalized_urls_to_remove, deleted_tags, tag_name, attr_name):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')

    tags_to_remove = []

    for tag in soup.find_all(tag_name):
        attr_value = normalize_url(tag.get(attr_name, ''))
        if attr_value in normalized_urls_to_remove:
            tags_to_remove.append(tag)
            deleted_tags.append(str(tag))  # Добавляем в список

    if tags_to_remove:
        for tag in tags_to_remove:
            tag.decompose()

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))

    return len(tags_to_remove) > 0  # Возвращаем True, если были удалены какие-либо теги, иначе False

def process_file(args):
    file_path, normalized_urls_to_remove, deleted_a_tags, deleted_img_tags, deleted_meta_tags, deleted_link_tags = args
    if REMOVE_A_TAGS:
        remove_tag_with_matching_attr(file_path, normalized_urls_to_remove, deleted_a_tags, 'a', 'href')
    if REMOVE_IMG_TAGS:
        remove_tag_with_matching_attr(file_path, normalized_urls_to_remove, deleted_img_tags, 'img', 'src')
    if REMOVE_META_TAGS:
        remove_tag_with_matching_attr(file_path, normalized_urls_to_remove, deleted_meta_tags, 'meta', 'content')
    if REMOVE_LINK_TAGS:
        remove_tag_with_matching_attr(file_path, normalized_urls_to_remove, deleted_link_tags, 'link', 'href')

def scan_directory_and_remove(directory_path, urls_to_remove, deleted_link_tags=None):
    normalized_urls_to_remove = [normalize_url(url) for url in urls_to_remove]
    all_files = []

    for root, _, files in os.walk(directory_path, topdown=True):
        for file in files:
            if file.lower().endswith(('.html', '.htm', '.xhtml', '.php')):
                all_files.append(os.path.join(root, file))

    manager = Manager()
    deleted_a_tags = manager.list()
    deleted_img_tags = manager.list()
    deleted_meta_tags = manager.list()
    if deleted_link_tags is None:
        deleted_link_tags = manager.list()

    with Pool() as pool:
        list(tqdm(pool.imap_unordered(process_file, [(file, normalized_urls_to_remove, deleted_a_tags, deleted_img_tags, deleted_meta_tags, deleted_link_tags) for file in all_files]), total=len(all_files)))

    # Преобразуем списки в множества для удаления дубликатов, затем обратно в списки
    unique_deleted_a_tags = list(set(deleted_a_tags))
    unique_deleted_img_tags = list(set(deleted_img_tags))
    unique_deleted_meta_tags = list(set(deleted_meta_tags))
    unique_deleted_link_tags = list(set(deleted_link_tags))

    if REMOVE_A_TAGS:
        with open('all_deleted_a_tag.txt', 'w', encoding='utf-8') as file:
            for tag in sorted(unique_deleted_a_tags):  # Опционально сортируем для улучшения читаемости
                file.write(f"{tag}\n")

    if REMOVE_IMG_TAGS:
        with open('all_deleted_img_tag.txt', 'w', encoding='utf-8') as file:
            for tag in sorted(unique_deleted_img_tags):  # Опционально сортируем для улучшения читаемости
                file.write(f"{tag}\n")

    if REMOVE_META_TAGS:
        with open('all_deleted_meta_tag.txt', 'w', encoding='utf-8') as file:
            for tag in sorted(unique_deleted_meta_tags):  # Опционально сортируем для улучшения читаемости
                file.write(f"{tag}\n")

    if REMOVE_LINK_TAGS:  # Добавлено
        with open('all_deleted_link_tag.txt', 'w', encoding='utf-8') as file:  # Добавлено
            for tag in sorted(unique_deleted_link_tags):
                file.write(f"{tag}\n")

    print(f"Обработано {len(all_files)} файлов.")
    if REMOVE_A_TAGS:
        print(f"Удалено {len(unique_deleted_a_tags)} ссылок.")
    if REMOVE_IMG_TAGS:
        print(f"Удалено {len(unique_deleted_img_tags)} изображений.")
    if REMOVE_META_TAGS:
        print(f"Удалено {len(unique_deleted_meta_tags)} мета-тегов.")
    if REMOVE_LINK_TAGS:
        print(f"Удалено {len(unique_deleted_link_tags)} тегов ссылок.")

if __name__ == "__main__":
    # Загрузите URL-адреса из файла
    urls_to_remove = load_urls_to_remove(urls_file_path)

    # Вызовите функцию для сканирования директории и удаления соответствующих тегов
    scan_directory_and_remove(directory_to_scan, urls_to_remove)


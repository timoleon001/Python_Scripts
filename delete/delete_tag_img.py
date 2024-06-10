import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from tqdm import tqdm
from multiprocessing import Pool, Manager

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
        print(f"File '{file_path}' not found.")

    return urls_to_remove

def normalize_url(url):
    parsed = urlparse(url.lower())
    normalized = parsed._replace(netloc=parsed.netloc.replace('www.', '')).geturl()
    return normalized

def remove_img_with_matching_src(file_path, normalized_urls_to_remove, deleted_imgs):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')

    imgs_to_remove = []

    for img in soup.find_all('img'):
        src = normalize_url(img.get('src', ''))
        if src in normalized_urls_to_remove:
            imgs_to_remove.append(img)
            deleted_imgs.append(src)  # Append to list

    if imgs_to_remove:
        for img in imgs_to_remove:
            img.decompose()

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))

    return len(imgs_to_remove) > 0  # Return True if any images were removed, else False

def process_file(args):
    file_path, normalized_urls_to_remove, deleted_imgs = args
    return remove_img_with_matching_src(file_path, normalized_urls_to_remove, deleted_imgs)

def scan_directory_and_remove(directory_path, urls_to_remove):
    normalized_urls_to_remove = [normalize_url(url) for url in urls_to_remove]
    all_files = []

    for root, _, files in os.walk(directory_path, topdown=True):
        for file in files:
            if file.lower().endswith(('.html', '.htm', '.xhtml', 'php')):
                all_files.append(os.path.join(root, file))

    manager = Manager()
    deleted_imgs = manager.list()

    with Pool() as pool:
        list(tqdm(pool.imap_unordered(process_file, [(file, normalized_urls_to_remove, deleted_imgs) for file in all_files]), total=len(all_files)))

    # Convert list to set to remove duplicates, then back to list
    unique_deleted_imgs = list(set(deleted_imgs))

    with open('all_delete_images.txt', 'w', encoding='utf-8') as file:
        for img in sorted(unique_deleted_imgs):  # Optionally sort for better readability
            file.write(f"{img}\n")

    print(f"Processed {len(all_files)} files.")
    print(f"Removed {len(unique_deleted_imgs)} images.")

if __name__ == "__main__":
    directory_to_scan = "D:\\OSPanel\\domains\\ekburg.tv"
    urls_file_path = "urls_for_delete.txt"  # Укажите путь к вашему файлу с URL-адресами

    # Загрузите URL-адреса из файла
    urls_to_remove = load_urls_to_remove(urls_file_path)

    # Вызовите функцию для сканирования директории и удаления соответствующих блоков
    scan_directory_and_remove(directory_to_scan, urls_to_remove)

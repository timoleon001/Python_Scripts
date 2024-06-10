import os
import multiprocessing
from tqdm import tqdm
from bs4 import BeautifulSoup
from functools import partial

# Удаляет завершающий слеш из URL в атрибутах src тегов <img> и href тегов <a>,
# если URL находится в заданном списке urls_for_edit_image.txt.

def process_html_file(file_path, url_list):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    modified = False

    # Обработка тегов <img>
    for img_tag in soup.find_all('img'):
        img_src = img_tag.get('src')
        if img_src in url_list:
            if img_src.endswith('/'):
                img_tag['src'] = img_src[:-1]  # Удаление слеша в конце
                modified = True

    # Обработка тегов <a>
    for a_tag in soup.find_all('a'):
        a_href = a_tag.get('href')
        if a_href in url_list:
            if a_href.endswith('/'):
                a_tag['href'] = a_href[:-1]  # Удаление слеша в конце
                modified = True

    if modified:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))

def main():
    directory = r'D://OSPanel//domains//ekburg.tv'
    url_list_file = 'urls_for_edit_image.txt'
    with open(url_list_file, 'r') as f:
        url_list = [line.strip() for line in f]

    html_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        for _ in tqdm(pool.imap_unordered(partial(process_html_file, url_list=url_list), html_files, chunksize=10), total=len(html_files), desc="Обработка HTML-файлов"):
            pass

if __name__ == "__main__":
    main()

import os
import urllib.parse
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests


def load_and_decode_urls(file_path):
    """Загрузка строк из файла и декодирование URL-символов."""
    decoded_urls = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            decoded_line = urllib.parse.unquote(line.strip())
            decoded_urls.append(decoded_line)
    return decoded_urls


def get_title(url):
    """Получение заголовка страницы по URL."""
    try:
        response = requests.get(url, verify=False)  # Игнорирование ошибок SSL сертификата
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string if soup.title else 'No Title'
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        title = 'No Title'
    return title


def load_files_for_editing(file_path):
    """Загрузка путей к HTML файлам для изменения из файла."""
    file_paths = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            file_paths.append(line.strip())
    return file_paths


def insert_snippets_to_html(html_file_path, snippets):
    """Вставка блоков в элемент с id='body-content'."""
    if not os.path.exists(html_file_path):
        print(f"File not found: {html_file_path}")
        return False

    with open(html_file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')

    body_content = soup.find(id='body-content')
    if not body_content:
        return False

    # Проверяем наличие класса 'item_popular_articles' и 'item_popular_links'
    if body_content.find('div', class_='item_popular_articles') or body_content.find('div', class_='item_popular_links'):
        return False

    # Создаем новый блок с двумя классами
    new_block = soup.new_tag('div', **{'class': 'centered dashboard_list item_popular_links'})
    popular_list = soup.new_tag('div', **{'class': 'popular-list'})
    h2_tag = soup.new_tag('h2')
    h2_tag.string = 'Популярное'
    popular_list.append(h2_tag)
    new_block.append(popular_list)

    # Добавляем сниппеты
    for snippet in snippets:
        snippet_div = soup.new_tag('div', **{'class': 'snippet snippet--material'})
        a_tag = soup.new_tag('a', **{'class': 'snippet--material__link', 'href': snippet['url']})
        span_tag = soup.new_tag('span', **{'class': 'snippet--material__title'})
        span_tag.string = snippet['title']
        a_tag.append(span_tag)
        snippet_div.append(a_tag)
        new_block.append(snippet_div)

    body_content.append(new_block)

    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    return True


def main():
    # Определяем пути
    FILES_FOR_EDITING_PATH = 'files_for_editing.txt'
    MODIFIED_FILES_PATH = 'modified_files.txt'
    FILE_NO_FROG_PATH = 'file_no_frog.txt'

    # Загружаем URL из файла
    urls = load_and_decode_urls(FILE_NO_FROG_PATH)
    print(f"Loaded {len(urls)} URLs.")

    # Проверка на наличие достаточного количества URL
    if len(urls) < 3:
        print("Not enough URLs to process even one HTML file. Please add more URLs to file_no_frog.txt.")
        return

    # Загружаем пути к HTML файлам для изменения
    html_files = load_files_for_editing(FILES_FOR_EDITING_PATH)
    print(f"Loaded {len(html_files)} HTML files for editing.")

    modified_files = []  # Список для хранения измененных файлов

    snippets_per_file = 3
    required_files_to_modify = len(urls) // snippets_per_file
    files_processed = 0

    # Использование tqdm для обновления прогресса на одной строке
    with tqdm(total=required_files_to_modify, desc="Processing HTML files", unit="file") as pbar:
        for html_file_path in html_files:
            if not urls:
                break  # Прекращаем, если закончились URL-адреса

            if files_processed >= required_files_to_modify:
                break  # Прекращаем, если обработали нужное количество файлов

            # Формируем список сниппетов из трех URL
            snippets = []
            for _ in range(snippets_per_file):
                if not urls:
                    break
                url = urls.pop(0)
                title = get_title(url)
                snippets.append({'url': url, 'title': title})

            if snippets:  # Проверяем, есть ли сниппеты для вставки
                if insert_snippets_to_html(html_file_path, snippets):
                    modified_files.append(html_file_path)
                    files_processed += 1
                    pbar.update(1)  # Обновление прогресса на одну единицу

    # Запись измененных файлов в modified_files.txt
    with open(MODIFIED_FILES_PATH, 'w', encoding='utf-8') as file:
        for modified_file in modified_files:
            file.write(f"{modified_file}\n")

    print(f"Total modified files: {len(modified_files)}")


if __name__ == '__main__':
    # Отключение предупреждений об SSL
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    main()

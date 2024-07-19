import os
from tqdm import tqdm
from bs4 import BeautifulSoup
from multiprocessing import Pool, cpu_count

# Cкрипт удаляет и добавляет теги meta (viewport и robots), link (canonical x-default )
# URL-адрес для тегов генерируется из пути файла. Если не удается обработать файл, создается error_add_tags.txt.


# Параметры для формирования URL
BASE_URL = "https://vokzal-simferopol.info/"
REMOVE_PREFIX = "D:\\OSPanel\\domains\\vokzal-simferopol.info\\"
REMOVE_SUFFIX = "/index.html"
ADD_SUFFIX = "/"


def get_canonical_url(file_path):
    relative_path = os.path.relpath(file_path, start=REMOVE_PREFIX).replace('\\', '/')
    if relative_path.endswith(REMOVE_SUFFIX):
        relative_path = relative_path[:-len(REMOVE_SUFFIX)]
    return BASE_URL + relative_path + ADD_SUFFIX


def process_html_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

        url_page = get_canonical_url(file_path)

        # Удаление старых тегов
        for tag in soup.find_all(['link', 'meta']):
            if tag.get('rel') in [['canonical'], ['alternate1']] or tag.get('name', '').lower() in ['viewport',
                                                                                                   'robots']:
                tag.decompose()

        # Добавление новых тегов перед <title>
        title_tag = soup.find('title')
        if title_tag:
            new_tags = [
                soup.new_tag('link', href=url_page, rel='canonical'),
                soup.new_tag('link', href=url_page, rel='alternate', hreflang='ru'),
                soup.new_tag('link', href=url_page, rel='alternate', hreflang='x-default'),
                soup.new_tag('meta', content="width=device-width, initial-scale=1, minimum-scale=1",
                             attrs={'name': "viewport"}),
                soup.new_tag('meta', attrs={'name': "robots", 'content': "index, follow"}),
                soup.new_tag('meta', attrs={'name': "yandex", 'content': "index, follow"}),
                soup.new_tag('meta', attrs={'name': "googlebot",
                                            'content': "index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1"})
            ]

            for new_tag in reversed(new_tags):
                title_tag.insert_before(new_tag)

            # Запись изменений в файл
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(str(soup))
        else:
            # Запись файла в список неудачных редактирований
            with open('error_add_meta_and_link_tags.txt', 'a', encoding='utf-8') as error_file:
                error_file.write(f"{file_path}\n")

        return True, file_path
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False, file_path


def main():
    error_files = []
    with open('all_directory.txt', 'r', encoding='utf-8') as file:
        file_paths = file.read().splitlines()

    num_workers = cpu_count()
    with Pool(num_workers) as pool:
        results = list(tqdm(pool.imap(process_html_file, file_paths), total=len(file_paths), desc="Processing files"))

    for success, file_path in results:
        if not success:
            error_files.append(file_path)

    if error_files:
        with open('error_add_tags.txt', 'w', encoding='utf-8') as error_file:
            for error_file_path in error_files:
                error_file.write(f"{error_file_path}\n")


if __name__ == "__main__":
    main()

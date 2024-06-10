import os
from tqdm import tqdm
from bs4 import BeautifulSoup
from concurrent.futures import ProcessPoolExecutor

# Cскрипт проверяет теги <a> и добавляет слеш в конец href, если он отсутствует.
# После обработки файлов скрипт записывает измененные ссылки в файл all_edit_href.txt.

# Задаем кодировку utf-8
os.environ['PYTHONIOENCODING'] = 'UTF-8'

# Путь к каталогу
directory = 'D://OSPanel//domains//ekburg.tv'


# Функция для обработки одного html файла
def process_html_file(file_path):
    edited_hrefs = []
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Создаем объект BeautifulSoup для парсинга html
    soup = BeautifulSoup(content, 'html.parser')

    # Находим все теги <a>
    for a_tag in soup.find_all('a'):
        href = a_tag.get('href')
        if href and not href.endswith('/') and not href.endswith('#') and not href.startswith('mailto:'):
            # Добавляем слеш к href, если его там нет и не заканчивается на '#' и не начинается с 'mailto:'
            new_href = href + '/'
            # Заменяем старый href на новый
            a_tag['href'] = new_href
            # Добавляем измененную ссылку в список
            edited_hrefs.append((href, new_href))

    # Если не было изменений, возвращаем None
    if not edited_hrefs:
        return None

    # Записываем изменения в файл
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    return edited_hrefs


# Функция для обработки всех html файлов в каталоге с учетом вложенности
def process_directory(directory):
    edited_hrefs = []
    with ProcessPoolExecutor() as executor:
        # Получаем список файлов
        html_files = [os.path.join(root, file) for root, _, files in os.walk(directory) for file in files if
                      file.endswith('.html')]
        total_files = len(html_files)

        # Используем tqdm для отслеживания прогресса
        with tqdm(total=total_files, desc="Processing HTML files") as pbar:
            # Запускаем обработку файлов в нескольких процессах
            for result in executor.map(process_html_file, html_files):
                if result:
                    edited_hrefs.extend(result)
                pbar.update(1)

    return edited_hrefs


# Обработка директории
if __name__ == "__main__":
    edited_hrefs = process_directory(directory)

    # Запись измененных ссылок в файл
    output_file = 'all_edit_href.txt'
    if edited_hrefs:
        with open(output_file, 'w', encoding='utf-8') as file:
            for old_href, new_href in edited_hrefs:
                file.write(f"Old href: {old_href}, New href: {new_href}\n")
        print("Processing complete. Edited hrefs saved in", output_file)
        print("Number of edited links:", len(edited_hrefs))
    else:
        print("No changes were made. No new entries in", output_file)

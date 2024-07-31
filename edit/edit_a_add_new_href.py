import os
from bs4 import BeautifulSoup
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

# Скрипт обрабатывает все HTML файлы в заданной папке, заменяя в них все ссылки <a>
# на фиксированный адрес. Используется мультипроцессорный подход для ускорения обработки.

# Путь к папке с файлами
INPUT_FOLDER = r'D:\\OSPanel\\domains\\www.strootmanofficial.com'
# Новое значение href
NEW_HREF = 'https://www.strootmanofficial.com/'


def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')
    links = soup.find_all('a')

    for link in links:
        link['href'] = NEW_HREF

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))


def main():
    # Получаем список всех HTML файлов в директории
    files = [os.path.join(INPUT_FOLDER, file) for file in os.listdir(INPUT_FOLDER) if file.endswith('.html')]

    # Используем пул процессов для параллельной обработки файлов
    with Pool(processes=cpu_count()) as pool:
        for _ in tqdm(pool.imap_unordered(process_file, files), total=len(files)):
            pass


if __name__ == '__main__':
    main()

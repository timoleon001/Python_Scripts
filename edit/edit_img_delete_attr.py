import os
from tqdm import tqdm
import multiprocessing
from bs4 import BeautifulSoup

# Скрипт удаляет атрибут data-icon у тегов <img>, если такой атрибут существует.

# Устанавливаем кодировку UTF-8
os.environ['PYTHONIOENCODING'] = 'utf-8'

def process_html_file(file_path, progress_queue):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')
    images = soup.find_all('img', attrs={'data-icon': True})
    if not images:
        progress_queue.put(1)
        return

    for img in images:
        del img['data-icon']

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    progress_queue.put(1)

def worker(files, progress_queue):
    for file_path in files:
        process_html_file(file_path, progress_queue)

def get_all_html_files(directory):
    html_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files

if __name__ == '__main__':
    directory = "D://OSPanel//domains//ekburg.tv"
    html_files = get_all_html_files(directory)

    cpu_count = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(cpu_count)
    manager = multiprocessing.Manager()
    progress_queue = manager.Queue()

    # Разбиваем список файлов на части для параллельной обработки
    chunk_size = len(html_files) // cpu_count + 1
    chunks = [html_files[i:i + chunk_size] for i in range(0, len(html_files), chunk_size)]

    # Создаем общий индикатор прогресса
    progress_bar = tqdm(total=len(html_files), desc="Processing HTML files")

    # Запускаем процессы
    results = []
    for chunk in chunks:
        results.append(pool.apply_async(worker, (chunk, progress_queue)))

    # Обновляем индикатор прогресса
    processed_files = 0
    while processed_files < len(html_files):
        progress_queue.get()
        processed_files += 1
        progress_bar.update(1)

    # Дожидаемся завершения всех процессов
    for result in results:
        result.wait()

    pool.close()
    pool.join()

    progress_bar.close()

import os
from bs4 import BeautifulSoup
from tqdm import tqdm
import concurrent.futures

#Удаление Блоков по списку селекторов
#Реализован механизм мультипроцессор для обработки сразу нескольких файлов
# num_processes=21 - максимальное количество одновременных процессов
def process_html(html, selectors):
    soup = BeautifulSoup(html, 'html.parser')

    # Удаление элементов по заданным селекторам
    for selector in selectors:
        elements = soup.select(selector)
        for element in elements:
            element.decompose()

    # Возврат обновленного HTML
    return str(soup)

def process_html_file(file_path, error_log_path, selectors):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        updated_html = process_html(html_content, selectors)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_html)

    except UnicodeDecodeError:
        # Запись ошибки в лог-файл
        with open(error_log_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f"Ошибка декодирования в файле: {file_path}\n")

    except Exception as e:
        # Запись других ошибок в лог-файл
        with open(error_log_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f"Ошибка при обработке файла: {file_path} - {e}\n")

def process_html_files_in_directory(directory, selectors, num_processes=21):
    error_log_path = os.path.join(directory, 'error_log.txt')
    all_html_files = []

    # Собираем все HTML-файлы в указанной директории
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.lower().endswith('.html'):
                file_path = os.path.join(root, file_name)
                all_html_files.append(file_path)

    # Используем tqdm для отображения индикатора прогресса
    with tqdm(total=len(all_html_files), desc=f"Обработка файлов в {directory}") as pbar:
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
            futures = {executor.submit(process_html_file, file_path, error_log_path, selectors): file_path for file_path in all_html_files}
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as exc:
                    with open(error_log_path, 'a', encoding='utf-8') as log_file:
                        log_file.write(f"Ошибка при обработке файла: {futures[future]} - {exc}\n")
                pbar.update(1)

def main():
    # Пример использования
    directory_path = 'D:\\OSPanel\\domains\\ekburg.tv'  # Путь к директории
    selectors = ['.video-content', 'iframe']  # Список селекторов для удаления
    process_html_files_in_directory(directory_path, selectors, num_processes=21)  # Указано максимальное количество процессов

if __name__ == '__main__':
    main()

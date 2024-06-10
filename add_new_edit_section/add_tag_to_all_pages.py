import os
import re
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

# сканирует все html файлы по каталогу и добавляет заданный тег на всех найденных страницах

# Путь к каталогу
directory = 'D://OSPanel//domains//ekburg.tv'


# Функция для обработки одного файла
def process_file(file_path):
    # Прочитать содержимое файла
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Добавить подключение перед </head>
    if '</head>' in content:
        new_content = re.sub(r'(</head>)', r'<link href="/styles_new.css" rel="stylesheet">\1', content,
                             flags=re.IGNORECASE)

        # Записать измененное содержимое обратно в файл
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        return True
    return False


# Функция для рекурсивного поиска всех html файлов в каталоге
def find_html_files(directory):
    html_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files


# Главная функция
def main():
    html_files = find_html_files(directory)
    total_files = len(html_files)

    if total_files == 0:
        print("No HTML files found.")
        return

    print(f"Found {total_files} HTML files. Processing...")

    # Используем пул процессов для обработки файлов
    with Pool(processes=cpu_count()) as pool:
        # Используем tqdm для отображения прогресса
        results = list(tqdm(pool.imap(process_file, html_files), total=total_files))

    processed_files = sum(results)
    print(f"Processing completed. {processed_files} files were modified.")


if __name__ == "__main__":
    main()

import os

# Определяем базовые пути
BASE_DISK_PATH = 'D:\\OSPanel\\domains\\vokzal-simferopol.info'
BASE_URL_PATH = 'https://vokzal-simferopol.info'

def get_html_files_with_paths(directory):
    """
    Находит все HTML файлы в заданной директории, исключая те, что содержат 'feed' или 'page' в пути,
    и записывает их пути в 'all_html_list_full_urls_disk.txt'.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Получаем путь к текущему скрипту
    full_directory_path = os.path.join(script_dir, directory)  # Строим полный путь к директории

    html_file_list = []
    for root, dirs, files in os.walk(full_directory_path):
        for filename in files:
            if filename.endswith('.html'):
                file_path = os.path.join(root, filename)
                if 'feed' in file_path or 'page' in file_path:
                    continue  # Пропускаем файлы, путь которых содержит "feed" или "page"
                html_file_list.append(file_path)

    with open('all_html_list_full_urls_disk.txt', 'w', encoding='utf-8') as file:
        for html_file in html_file_list:
            file.write(f"{html_file}\n")

    return html_file_list

def process_file(input_file, output_file, base_disk_path, base_url_path):
    """
    Заменяет пути в файле с дисковых на URL и записывает результат в новый файл.
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    with open(output_file, 'w', encoding='utf-8') as output_f:
        for line in lines:
            line = line.strip()
            if line:
                line = line.replace(base_disk_path, base_url_path)
                if line.endswith('index.html'):
                    line = line[:-len('index.html')]
                line = line.replace('\\', '/')
                output_f.write(line + '\n')

def main():
    # Пример использования
    directory_path = BASE_DISK_PATH

    html_files = get_html_files_with_paths(directory_path)
    for html_file in html_files:
        print(html_file)
    print(f"Total HTML files: {len(html_files)}")

    input_file = "all_html_list_full_urls_disk.txt"
    output_file = "all_html_list.txt"

    process_file(input_file, output_file, BASE_DISK_PATH, BASE_URL_PATH)

if __name__ == '__main__':
    main()

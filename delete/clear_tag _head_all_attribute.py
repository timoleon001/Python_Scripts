import os
from bs4 import BeautifulSoup

# Функция для удаления атрибутов у тега <head>
def remove_head_attributes(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    head_tag = soup.find('head')
    if head_tag:
        attrs_to_remove = list(head_tag.attrs.keys()) # Создание копии ключей атрибутов
        for attr in attrs_to_remove:
            del head_tag[attr]
    return str(soup)


# Функция для обхода всех HTML-файлов в указанной директории
def process_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    html_content = f.read()
                modified_html = remove_head_attributes(html_content)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(modified_html)
                print(f"Атрибуты у тега <head> в файле {file_path} удалены.")

# Указать путь к каталогу
directory_path = r"D:\OSPanel\domains\ekburg.tv"

# Запустить обработку файлов
process_files(directory_path)

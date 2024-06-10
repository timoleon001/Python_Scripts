import os
from bs4 import BeautifulSoup
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

# Обрабатывает все HTML файлы в указанной директории и удаляет внешние ссылки, перезаписывая файлы с изменениями
# Удаление внешних ссылок: Удаляет все теги <script>, <link>, <img> и <a>, которые содержат внешние ссылки.
# Позволяет включать или отключать удаление определенных типов тегов
# Позволяет указать, что считать внутренней ссылкой для различных типов тегов
# Записывает удаленные теги в соответствующие текстовые файлы для последующего анализа.

# Указываем каталог с HTML файлами
directory = "D://OSPanel//domains//ekburg.tv"

# Указываем файлы для записи удаленных тегов
deleted_scripts_file = "delete_scripts.txt"
deleted_links_file = "delete_external_link.txt"
deleted_images_file = "delete_external_images.txt"
deleted_anchors_file = "deletee_external_a.txt"

# Настройки для включения/отключения удаления различных типов тегов
remove_scripts = True
remove_links = True
remove_images = True
remove_anchors = True

# Функция для проверки является ли ссылка внутренней для тегов <script> и <link>
def is_internal_link_generic(url):
    return url.startswith("https://www.ekburg.tv") or url.startswith("https://ekburg.tv") or url.startswith("/")


# Функция для проверки является ли ссылка внутренней для тегов <a>
def is_internal_link_anchor(url):
    return (url.startswith("mailto:") or
            url.startswith("#") or
            url.startswith("/") or
            url.startswith("https://ekburg.tv") or
            url.startswith("https://www.ekburg.tv") or
            url.startswith("https://static.ekburg.tv"))


# Функция для проверки является ли ссылка внутренней для тегов <img>
def is_internal_link_image(url):
    return (url.startswith("") or
            url.startswith("/") or
            url.startswith("https://ekburg.tv") or
            url.startswith("https://static.ekburg.tv") or
            url.startswith("https://dev.ekburg.tv") or
            url.startswith("https://www.ekburg.tv"))


# Функция для обработки одного HTML файла
def process_file(file_path, unique_deleted_scripts, unique_deleted_links, unique_deleted_images,
                 unique_deleted_anchors):
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    scripts_to_delete = []
    links_to_delete = []
    images_to_delete = []
    anchors_to_delete = []

    # Находим и обрабатываем теги <script>
    if remove_scripts:
        scripts = soup.find_all("script", src=True)
        for script in scripts:
            src = script.get("src")
            if not is_internal_link_generic(src):
                script_str = str(script)
                if script_str not in unique_deleted_scripts:
                    unique_deleted_scripts.add(script_str)
                    scripts_to_delete.append(script)

    # Находим и обрабатываем теги <link>
    if remove_links:
        links = soup.find_all("link", href=True)
        for link in links:
            href = link.get("href")
            if not is_internal_link_generic(href):
                link_str = str(link)
                if link_str not in unique_deleted_links:
                    unique_deleted_links.add(link_str)
                    links_to_delete.append(link)

    # Находим и обрабатываем теги <img>
    if remove_images:
        images = soup.find_all("img", src=True)
        for img in images:
            src = img.get("src")
            if not is_internal_link_image(src):
                img_str = str(img)
                if img_str not in unique_deleted_images:
                    unique_deleted_images.add(img_str)
                    images_to_delete.append(img)

    # Находим и обрабатываем теги <a>
    if remove_anchors:
        anchors = soup.find_all("a", href=True)
        for anchor in anchors:
            href = anchor.get("href")
            if not is_internal_link_anchor(href):
                anchor_str = str(anchor)
                if anchor_str not in unique_deleted_anchors:
                    unique_deleted_anchors.add(anchor_str)
                    anchors_to_delete.append(anchor)

    # Удаляем найденные внешние теги и записываем их в соответствующие файлы
    if scripts_to_delete:
        with open(deleted_scripts_file, "a", encoding="utf-8") as f_del_scripts:
            for script in scripts_to_delete:
                f_del_scripts.write(str(script) + "\n")
                script.decompose()

    if links_to_delete:
        with open(deleted_links_file, "a", encoding="utf-8") as f_del_links:
            for link in links_to_delete:
                f_del_links.write(str(link) + "\n")
                link.decompose()

    if images_to_delete:
        with open(deleted_images_file, "a", encoding="utf-8") as f_del_images:
            for img in images_to_delete:
                f_del_images.write(str(img) + "\n")
                img.decompose()

    if anchors_to_delete:
        with open(deleted_anchors_file, "a", encoding="utf-8") as f_del_anchors:
            for anchor in anchors_to_delete:
                f_del_anchors.write(str(anchor) + "\n")
                anchor.decompose()

    # Перезаписываем HTML файл с удаленными тегами
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))


# Подсчет общего количества файлов
total_files = sum([len(files) for _, _, files in os.walk(directory) if any(file.endswith(".html") for file in files)])

# Множества для хранения уникальных удаленных тегов
unique_deleted_scripts = set()
unique_deleted_links = set()
unique_deleted_images = set()
unique_deleted_anchors = set()

# Используем ThreadPoolExecutor для многопоточности
with ThreadPoolExecutor() as executor:
    futures = []
    with tqdm(total=total_files, desc="Processing HTML files") as pbar:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".html"):
                    file_path = os.path.join(root, file)
                    futures.append(
                        executor.submit(process_file, file_path, unique_deleted_scripts, unique_deleted_links,
                                        unique_deleted_images, unique_deleted_anchors))
                    pbar.update(1)

        # Ожидаем завершения всех задач
        for future in futures:
            future.result()

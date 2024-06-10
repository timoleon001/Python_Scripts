# Импорт необходимых библиотек
import os


def convert_url_to_path(source_file, target_file):
    # Заменяемый и заменяющий пути
    url_prefix = "https://ekburg.tv"
    local_path_prefix = "D:\\OSPanel\\domains\\ekburg.tv"

    # Открытие исходного файла для чтения и целевого файла для записи
    with open(source_file, 'r', encoding='utf-8') as file_read, open(target_file, 'w', encoding='utf-8') as file_write:
        for line in file_read:
            # Удаление лишних пробелов и переносов строк
            clean_line = line.strip()

            # Определение нового пути
            if clean_line == url_prefix:
                # Специальный случай для корневого URL
                new_path = os.path.join(local_path_prefix, "index.html")
            else:
                # Замена URL на локальный путь и добавление index.html
                part_after_domain = clean_line[len(url_prefix):] if clean_line.startswith(url_prefix) else clean_line
                full_path = local_path_prefix + part_after_domain + "index.html"
                new_path = os.path.join(local_path_prefix, full_path.replace('/', '\\'))

            # Запись преобразованного пути в новый файл
            file_write.write(new_path + '\n')


# Отключение выполнения функции
convert_url_to_path("urls.txt", "directory.txt")

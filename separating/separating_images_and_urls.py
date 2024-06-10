# Определяем функцию для проверки, содержит ли строка расширение изображения
def contains_image_extension(line, extensions=None):
    if extensions is None:
        extensions = ['.jpg', '.png', '.gif', '.jpeg', '.js', '.JPG', '.css']
    return any(ext in line for ext in extensions)


# Функция для обработки файла
def process_file(input_file, output_file_images, output_file_others):
    # Открываем исходный файл для чтения
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Открываем файлы для записи
    with open(output_file_images, 'w', encoding='utf-8') as f_images, \
            open(output_file_others, 'w', encoding='utf-8') as f_others:
        # Перебираем строки из исходного файла
        for line in lines:
            # Убираем пробельные символы в начале и конце строки
            line = line.strip()
            # Проверяем, содержит ли строка расширение изображения
            if contains_image_extension(line):
                # Если да, записываем в файл для изображений
                f_images.write(line + '\n')
            else:
                # Иначе, записываем в файл для остальных строк
                f_others.write(line + '\n')


# Пути к файлам
input_file = 'url_404.txt'  # Путь к исходному файлу
output_file_images = 'images.txt'  # Файл для строк с расширениями изображений
output_file_others = 'others.txt'  # Файл для остальных строк

# Вызываем функцию обработки файла
process_file(input_file, output_file_images, output_file_others)

import os

# Сканируе файлы по писку

def scan_files(input_file):
    # Чтение списка файлов из файла
    with open(input_file, 'r') as f:
        files = f.readlines()
    # Удаление символов новой строки из путей к файлам
    files = [file.strip() for file in files]
    return files

def check_popularity(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Проверка наличия id="body-content" и <h2>Популярное</h2>
        if 'id="body-content"' in content:
            if '<h2>Популярное</h2>' in content:
                return 'true'
            else:
                return 'false'
        return 'not_found'
    except FileNotFoundError:
        return 'file_not_found'

def main():
    input_file = 'scan_files.txt'
    false_pupular_file = 'false_pupular.txt'
    true_pupular_file = 'true_pupular.txt'

    files = scan_files(input_file)
    total_files = len(files)
    processed_files = 0

    # Создание или очистка файлов для записи результатов
    with open(false_pupular_file, 'w') as f_false, open(true_pupular_file, 'w') as f_true:
        for file in files:
            result = check_popularity(file)
            # Запись результата в соответствующий файл
            if result == 'true':
                f_true.write(file + '\n')
            elif result == 'false':
                f_false.write(file + '\n')
            elif result == 'file_not_found':
                print(f'Файл не найден: {file}')
            processed_files += 1
            # Вывод процента выполнения в консоль
            percentage = (processed_files / total_files) * 100
            print(f'Выполнено: {percentage:.2f}%')

if __name__ == "__main__":
    main()

#Замена урла на адрес файла
def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    with open(output_file, 'w', encoding='utf-8') as output_f:
        for line in lines:
            line = line.strip()
            if line:
                # Откинуть часть, которая относится как путь к каталогу
                line = line.replace('D:\\OSPanel\\domains\\ekburg.tv', 'https://ekburg.tv')

                # Проверить, оканчивается ли на "index.html"
                if line.endswith('index.html'):
                    line = line[:-len('index.html')]

                # Заменить обратные слеши на прямые
                line = line.replace('\\', '/')

                output_f.write(line + '\n')

if __name__ == "__main__":
    input_file = "directory.txt"  # Замените на путь к вашему входному файлу
    output_file = "urls.txt"  # Замените на путь к вашему выходному файлу

    process_file(input_file, output_file)

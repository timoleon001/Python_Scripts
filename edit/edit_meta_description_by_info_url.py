import os
from bs4 import BeautifulSoup
from tqdm import tqdm
import multiprocessing

# Скрипт обновляет или создает тег <meta name="description"> для каждого HTML файла,
# используя данные из файла all_urls.txt и формируя содержимое на основе содержимого тега <title>.

def process_file(file_path):
    try:
        # Открываем и читаем HTML файл
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

            # Извлекаем текст из тега <title>
            title_text = soup.title.get_text().strip()

            # Отбрасываем текст после последнего тире, если он есть
            if '-' in title_text:
                description_text = title_text.rsplit('-', 1)[0].strip()
            else:
                description_text = title_text

            # Обновляем или создаем тег <meta name="description">
            meta_description_tag = soup.find("meta", {"name": "description"})
            if meta_description_tag:
                meta_description_tag['content'] += f' {description_text}'
            else:
                new_meta_tag = soup.new_tag("meta", attrs={"name": "description", "content": f"{description_text}. Лучшие новости города Екатеринбург"})
                if soup.title:
                    soup.title.insert_after(new_meta_tag)
                else:
                    soup.head.append(new_meta_tag)

            # Сохраняем изменения в HTML файл
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(str(soup))

            return True
    except Exception as e:
        print(f"Ошибка при обработке {file_path}: {e}")
        return False


def main():
    # Читаем пути к файлам из all_urls.txt
    with open('all_directory.txt', 'r', encoding='utf-8') as file:
        file_paths = [line.strip() for line in file.readlines()]

    # Используем многопроцессорный пул для параллельной обработки файлов
    with multiprocessing.Pool() as pool:
        results = list(tqdm(pool.imap(process_file, file_paths), total=len(file_paths)))

    print(f"Успешно обработано {results.count(True)} из {len(file_paths)} файлов.")


if __name__ == "__main__":
    main()

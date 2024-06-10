import os
from multiprocessing import Pool
from bs4 import BeautifulSoup
from tqdm import tqdm


# Этот скрипт обрабатывает HTML файлы, указанные в all_urls.txt,
# добавляет отсутствующие атрибуты alt и title к <img> элементам,
# и сохраняет информацию об измененных изображениях в файл editing_imagas_alt_title.txt

# Функция для обработки одного HTML файла
def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    images = soup.find_all('img')
    modified = False
    changes = set()

    for img in images:
        alt = img.get('alt')
        title = img.get('title')
        original_img = str(img)

        if not alt:
            img['alt'] = "Новости на ЕТВ"
            modified = True
            changes.add(f"{file_path}: {original_img}")

        if not title:
            img['title'] = img['alt'] if img.get('alt') else "Новости на ЕТВ"
            modified = True
            changes.add(f"{file_path}: {original_img}")

    if modified:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))

    return list(changes)


# Функция для обработки всех файлов в all_urls.txt
def main():
    with open('all_directory.txt', 'r', encoding='utf-8') as f:
        files = [line.strip() for line in f]

    total_files = len(files)
    results = set()

    with Pool() as pool:
        for result in tqdm(pool.imap_unordered(process_file, files), total=total_files):
            results.update(result)

    # Запись изменений в файл
    with open('editing_imagas_alt_title.txt', 'w', encoding='utf-8') as f:
        for change in results:
            f.write(change + '\n')


if __name__ == '__main__':
    main()

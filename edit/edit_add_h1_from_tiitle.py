import os
import re
from bs4 import BeautifulSoup
from tqdm import tqdm


# Cкрипт изменяет содержимое тега <h1> на текст из тега <title>, обрезанный до первого тире.
# Если тег <h1> отсутствует, он добавляется после заднного селектора.
# Неудавшиеся изменения записываются в файл no_add_h1_page.txt.

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

        title_tag = soup.find('title')
        if not title_tag or not title_tag.string:
            return file_path, 'No title tag found'

        new_text = re.split(r' - ', title_tag.string)[0].strip() + " - EKBTV"

        h1_tag = soup.find('h1')
        if h1_tag:
            h1_tag.string = new_text
        else:
            stream_header = soup.select_one('.h1-light.stream-header') or soup.select_one('.page-block-header')
            if stream_header:
                new_h1_tag = soup.new_tag('h1', **{'class': 'page-block-header'})
                new_h1_tag.string = new_text
                stream_header.insert_after(new_h1_tag)
            else:
                return file_path, 'No suitable insertion point found'

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))

        return file_path, 'Processed successfully'
    except Exception as e:
        return file_path, f'Error: {str(e)}'


def main():
    with open('all_directory.txt', 'r', encoding='utf-8') as f:
        file_paths = [line.strip() for line in f if line.strip()]

    results = []
    with tqdm(total=len(file_paths), desc="Processing files") as pbar:
        for file_path in file_paths:
            result = process_file(file_path)
            results.append(result)
            pbar.update(1)

    with open('no_add_h1_page.txt', 'w', encoding='utf-8') as no_add_file:
        for result in results:
            if 'Processed successfully' not in result[1]:
                no_add_file.write(f"{result[0]}: {result[1]}\n")


if __name__ == '__main__':
    main()

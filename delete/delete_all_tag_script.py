import os
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
from bs4 import BeautifulSoup

# Этот скрипт находит все теги <script> в HTML файлах и удаляет их, используя многопроцессорный подход для ускорения обработки

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')
    [s.extract() for s in soup('script')]

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))

def process_files(file_paths):
    with Pool(cpu_count()) as pool:
        list(tqdm(pool.imap(process_file, file_paths), total=len(file_paths)))

if __name__ == "__main__":
    with open('all_directory.txt', 'r', encoding='utf-8') as f:
        file_paths = [line.strip() for line in f.readlines()]

    process_files(file_paths)

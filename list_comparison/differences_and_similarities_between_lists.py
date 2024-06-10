from tqdm import tqdm

# Сравнение двух списков и запись результатов совпадения (result_matches.txt), различия (result_shortage.txt)
# и элементов из file_b.txt, которые не вошли в result_matches.txt (result_additional.txt)
def read_file_to_list(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]

# Чтение содержимого файлов
file_a_list = read_file_to_list('file_a.txt')
file_b_list = read_file_to_list('file_b.txt')

# Нахождение общих элементов и различий
matches = []
shortages = []
for item in tqdm(file_a_list, desc="Сравнение списков"):
    if item in file_b_list:
        matches.append(item)
    else:
        shortages.append(item)

# Запись совпадений в файл
with open('result_matches.txt', 'w', encoding='utf-8') as matches_file:
    for item in tqdm(matches, desc="Запись совпадений"):
        matches_file.write(f"{item}\n")

# Запись различий в файл
with open('result_shortage.txt', 'w', encoding='utf-8') as shortage_file:
    for item in tqdm(shortages, desc="Запись различий"):
        shortage_file.write(f"{item}\n")

# Нахождение элементов из file_b.txt, которые не вошли в result_matches.txt
additional_items = [item for item in file_b_list if item not in matches]

# Запись элементов, которые не вошли в result_matches.txt, в файл
with open('result_additional.txt', 'w', encoding='utf-8') as additional_file:
    for item in tqdm(additional_items, desc="Запись дополнительных элементов"):
        additional_file.write(f"{item}\n")

print("Результаты записаны в файлы result_matches.txt, result_shortage.txt и result_additional.txt")

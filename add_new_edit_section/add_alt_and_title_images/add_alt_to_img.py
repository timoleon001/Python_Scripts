import os
from bs4 import BeautifulSoup


def process_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Обработка тегов img
    img_tags = soup.find_all('img')
    for img_tag in img_tags:
        if 'alt' not in img_tag.attrs or not img_tag['alt']:
            img_tag['alt'] = 'Железнодорожный вокзал Симферополь'
            print(img_tag)

    # Обработка тегов button
    button_tags = soup.find_all('button')
    for button_tag in button_tags:
        if 'title' not in button_tag.attrs or not button_tag['title']:
            button_tag['title'] = 'Button Clicked'
            print(button_tag)

    # Вернуть обновленный HTML
    return str(soup)


def process_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    updated_html = process_html(html_content)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(updated_html)


def process_html_files_in_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith('.html'):
                file_path = os.path.join(root, file_name)
                print(file_path)
                process_html_file(file_path)


def main():
    directory_path = 'D:\\OSPanel\\domains\\vokzal-simferopol.info'
    process_html_files_in_directory(directory_path)


if __name__ == '__main__':
    main()


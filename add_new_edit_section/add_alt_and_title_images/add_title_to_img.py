import os
from bs4 import BeautifulSoup

def process_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Обработка тегов img
    img_tags = soup.find_all('img')
    for img_tag in img_tags:
        alt_text = img_tag.get('alt', '')
        title_text = alt_text if alt_text else 'Железнодорожный вокзал Симферополь'
        img_tag['title'] = title_text

    # Вернуть обновленный HTML
    # return str(soup)
    return soup.prettify(formatter=None)


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

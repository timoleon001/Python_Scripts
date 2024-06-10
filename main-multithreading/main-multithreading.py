from urllib.parse import urlparse, urljoin, urlsplit
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import concurrent.futures
import urllib3

# Отключение предупреждений о несертифицированных HTTPS-запросах
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})


def get_response(link):
    try:
        return session.get(link, verify=False, allow_redirects=True)
    except requests.exceptions.RequestException as e:
        raise e


def is_absolute_url(url):
    return bool(urlparse(url).netloc)


def get_absolute_url(base_url, relative_url):
    return urljoin(base_url, relative_url)


def check_broken_images_and_resources(response):
    if response is None:
        return "Failed to fetch the URL."

    broken_images_and_resources = []
    soup = BeautifulSoup(response.content, 'html.parser')

    for img_tag in soup.find_all('img'):
        img_url = img_tag.get('src')
        if not img_url:
            continue

        if img_url.startswith('//'):
            img_url = 'https:' + img_url  # Добавляем схему 'https'

        if not is_absolute_url(img_url):
            img_url = get_absolute_url(response.url, img_url)

        img_response = session.get(img_url, verify=False)
        if img_response.status_code != 200:
            broken_images_and_resources.append(img_url)

    for resource_tag in soup.find_all(['script', 'link']):
        resource_url = resource_tag.get('src') or resource_tag.get('href')
        if not resource_url:
            continue

        if resource_url.startswith('//'):
            resource_url = 'https:' + resource_url  # Добавляем схему 'https'

        if not is_absolute_url(resource_url):
            resource_url = get_absolute_url(response.url, resource_url)

        resource_response = session.get(resource_url, verify=False)
        if resource_response.status_code != 200:
            broken_images_and_resources.append(resource_url)

    if broken_images_and_resources:
        return f"Broken Images and Resources: {' '.join(broken_images_and_resources)}"
    return None


def has_russian_chars(text):
    return any(ord(char) > 127 for char in text)


def check_canonical_url(response, link):
    if response is None:
        return "Failed to fetch the URL."

    soup = BeautifulSoup(response.content, 'html.parser')
    canonical_tag = soup.find('link', attrs={'rel': lambda x: x and x.lower() == 'canonical'})

    if canonical_tag:
        canonical_url = canonical_tag.get('href')
        link_scheme, link_netloc, link_path, _, _ = urlsplit(link)
        canonical_scheme, canonical_netloc, canonical_path, _, _ = urlsplit(canonical_url)

        # Проверяем наличие русских символов в ссылках, и исключаем их из проверки canonical_url
        if has_russian_chars(link) or has_russian_chars(canonical_url):
            return None

        link_path = link_path.rstrip('/')
        canonical_path = canonical_path.rstrip('/')

        if (link_scheme.lower() == canonical_scheme.lower() and
                link_netloc.lower() == canonical_netloc.lower() and
                link_path == canonical_path):
            return None
        else:
            return "Invalid Canonical URL"

    return None


def check_title(response):
    if response is None:
        return "Failed to fetch the URL."

    soup = BeautifulSoup(response.content, 'html.parser')
    title_tag = soup.find('title')
    return "Title Not Found" if not title_tag or not title_tag.text.strip() else None


def check_description(response):
    if response is None:
        return "Failed to fetch the URL."

    soup = BeautifulSoup(response.content, 'html.parser')
    meta_descriptions = soup.find_all('meta', attrs={'name': lambda x: x and x.lower() == 'description'})
    meta_descriptions = [meta.get('content', '').strip() for meta in meta_descriptions]
    if not all(meta_descriptions):
        return "Description Not Found"

    return None


def check_keywords(response):
    if response is None:
        return "Failed to fetch the URL."

    soup = BeautifulSoup(response.content, 'html.parser')
    meta_keywords = soup.find_all('meta', attrs={'name': lambda x: x and x.lower() == 'keywords'})
    meta_keywords = [meta.get('content', '').strip() for meta in meta_keywords]
    if not all(meta_keywords):
        return "Keywords Not Found"

    return None


def check_h1(response):
    if response is None:
        return "Failed to fetch the URL."

    soup = BeautifulSoup(response.content, 'html.parser')
    h1_tags = soup.find_all('h1')
    if not any(h1_tag.text.strip() for h1_tag in h1_tags):
        return "H1 Not Found"

    return None


def check_image_alt(response):
    if response is None:
        return "Failed to fetch the URL."

    soup = BeautifulSoup(response.content, 'html.parser')
    img_tags = soup.find_all('img')
    for img_tag in img_tags:
        alt_text = img_tag.get('alt', '').strip()
        img_url = img_tag.get('src', '').strip()
        if img_url and not alt_text:
            return f"Image Alt Not Found {img_url}"

    return None


def check_link(link):
    response = get_response(link)
    error_reason = check_canonical_url(response, link)
    title_reason = check_title(response)
    description_reason = check_description(response)
    keywords_reason = check_keywords(response)
    h1_reason = check_h1(response)
    image_alt_reason = check_image_alt(response)
    broken_images_and_resources_reason = check_broken_images_and_resources(response)

    reasons = [reason for reason in
               [error_reason, title_reason, description_reason, keywords_reason, h1_reason, image_alt_reason,
                broken_images_and_resources_reason] if reason]

    if reasons:
        return link, "  ".join(reasons)

    return None


def check_links_status(file_path_param):
    error_links = []

    with open(file_path_param, encoding='utf-8') as f:
        links = f.read().splitlines()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(tqdm(executor.map(check_link, links), total=len(links), desc="Checking Links", unit="link"))

    for result in results:
        if result:
            error_links.append(result)

    if error_links:
        with open("result.txt", "w", encoding="utf-8") as result_file:
            result_file.write("Ссылки, которые не прошли проверку:\n")
            for link, reasons in error_links:
                result_file.write(f"{link}  {reasons}\n")
        print("Ссылки с ошибками записаны в файл result.txt")
    else:
        print("Все ссылки работают корректно.")


if __name__ == "__main__":
    file_path = 'all_urls.txt'
    check_links_status(file_path)

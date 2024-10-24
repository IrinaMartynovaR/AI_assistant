from bs4 import BeautifulSoup
import requests

def extract_urls_from_html(html_content, base_url, max_urls=5): #извлекает URL-адреса статей из HTML-содержимого и сохраняет их в файл
    soup = BeautifulSoup(html_content, 'html.parser')
    urls = []    
    # найдём все теги 'a', которые ведут на статьи
    for link in soup.find_all('a', href=True):
        href = link['href']
        # игнорируем главную ссылку на раздел
        if "obrazovanie" in href != '/obrazovanie':
            # делаем её абсолютной
            if href.startswith('/'):
                full_url = base_url + href
            else:
                full_url = href
            # сохраняем уникальные ссылки на статьи
            if full_url not in urls and len(urls) < max_urls:
                urls.append(full_url)    
    # сохранение URL-адресов в файл
    with open("sourcedocs.txt", "w", encoding="utf-8") as f:
        for url in urls:
            f.write(f"{url}\n")
    print(f"Сохранено {len(urls)} ссылок на статьи в файл sourcedocs.txt.")


def fetch_and_extract_urls(site_url): #извлекаем ссылки на статьи
    try:
        response = requests.get(site_url)
        response.raise_for_status()  # статус ответа
        extract_urls_from_html(response.content, site_url)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке страницы: {e}")



import os
import requests
from bs4 import BeautifulSoup

#чтение текста из HTML по URL
def read_text_from_url(url):
    response = requests.get(url)  # запрос к URL
    response.raise_for_status()  # проверка на ошибки, если код не 200
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')        
    text = soup.get_text(separator="\n") #извлечение текста и удаление лишних пробелов    
    text = "\n".join(line.strip() for line in text.splitlines() if line.strip()) # удаление лишних пробелов и пустых строк   
    return text


# функция для сохранения распарсенного текста в файл
def save_text_to_file(text, output_filename):
    os.makedirs('txt_files', exist_ok=True)  
    full_path = os.path.join('txt_files', output_filename)
    with open(full_path, 'w', encoding='utf-8') as f:  
        f.write(text)
    print(f"Текст успешно сохранен в {full_path}")

# функция для чтения URL-адресов из файла
def read_urls_from_file():
    with open('sourcedocs.txt', 'r', encoding='utf-8') as f:
        urls = f.readlines()
    return [url.strip() for url in urls]

# главная функция для обработки каждого URL
def process_urls():
    urls = read_urls_from_file()  
    for i, url in enumerate(urls):
        print(f"Обработка URL {i+1}/{len(urls)}: {url}")
        parsed_text = read_text_from_url(url)          
        if parsed_text:  # проверяем, что текст не пустой
            output_filename = f"parsed_content_{i+1}.txt"  # генерация уникального имени файла
            save_text_to_file(parsed_text, output_filename)  # сохранение в файл
        else:
            print(f"Содержимое не было найдено для {url}")


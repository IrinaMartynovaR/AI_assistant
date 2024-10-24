import os
import requests
from dotenv import load_dotenv  # Импортируем библиотеку

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем значение GPT_TOKEN из переменных окружения
gpt_key = os.environ.get("GPT_TOKEN")

def generate_blog_text(news_content):
    url = "https://chatgpt-42.p.rapidapi.com/gpt4"

    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are an assistant that creates blog posts based on news articles, aimed at a target audience of mothers."
            },
            {
                "role": "user",
                "content": f"Please write a brief and clear blog post based on the following news, ensuring it is easy to understand. Do all of this in Russian: {news_content}"
            }
        ],
        "web_access": False,
        "max_tokens": 150  # Можно увеличить при необходимости
    }

    headers = {
        "x-rapidapi-key": gpt_key,  # Замените на ваш ключ
        "x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        json_response = response.json()

        return json_response.get('result', "Не удалось сгенерировать текст блога.").strip()

    except requests.exceptions.RequestException as e:
        return f"Ошибка при запросе к API: {e}"
    except Exception as e:
        return f"Произошла непредвиденная ошибка: {e}"


def save_blog_text(blog_text, output_filename):
    os.makedirs('blog', exist_ok=True)  
    full_path = os.path.join('blog', output_filename)
    with open(full_path, 'w', encoding='utf-8') as f:  
        f.write(blog_text)
    print(f"Текст для блога успешно сохранен в {full_path}")


def read_text_files_from_folder(folder):
    text_contents = []
    for filename in os.listdir(folder):
        if filename.endswith('.txt'):
            with open(os.path.join(folder, filename), 'r', encoding='utf-8') as f:
                text_contents.append(f.read())
    return text_contents

# функция для обработки каждого текстового файла
def process_text_files():
    folder = 'txt_files'  # папка, где хранятся исходные текстовые файлы
    text_files = read_text_files_from_folder(folder)  # чтение текстов из папки

    for i, content in enumerate(text_files):
        print(f"Обрабатывается файл {i + 1}/{len(text_files)}")
        
        if content.strip():  # проверяем, что текст не пустой
            # генерация текста для блога
            blog_text = generate_blog_text(content)  
            output_filename = f"blog_post_{i + 1}.txt"  
            save_blog_text(blog_text, output_filename)  
        else:
            print(f"Не обнаружено содержимое для файла {i + 1}")


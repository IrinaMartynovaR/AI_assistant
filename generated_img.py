import json
import time
import requests
import os
import re
import base64

class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }


    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        print(f"Available models: {data}")
        return data[0]['id']


    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        print(f"Response from generate: {data}")
        return data.get('uuid')


    def check_generation(self, request_id, attempts=30, delay=30):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            print(f"Generation status: {data}")
            
            if data['status'] == 'DONE':
                images_base64 = data.get('images', [])
                return images_base64

            attempts -= 1
            time.sleep(delay)
        return None


    def save_images_locally(self, images_base64, folder='generated_images'):
        if not os.path.exists(folder):
            os.makedirs(folder)

        for i, image_base64 in enumerate(images_base64):
            try:
                image_data = base64.b64decode(image_base64)  # Декодируем Base64
                image_path = os.path.join(folder, f'image_{i + 1}.png')
                with open(image_path, 'wb') as image_file:
                    image_file.write(image_data)  # Сохраняем декодированные данные как изображение
                print(f"Изображение сохранено в: {image_path}")
            except Exception as e:
                print(f"Ошибка при сохранениии {i + 1}: {e}")


def extract_sentences(text):
    # Регулярное выражение для нахождения предложений
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text) #проверка на перечисления
    # Возвращаем первые три предложения
    return ' '.join(sentences[:4])

    
def promt_text(txt_folder_path):
    # Обработка файлов в папке txt_folder_path
    txt_files = [f for f in os.listdir(txt_folder_path) if f.endswith('.txt')]
    for i, file_name in enumerate(txt_files):
        file_path = os.path.join(txt_folder_path, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Извлечение предложений и запись обратно в файл
        processed_text = extract_sentences(text)
        
        # Сохраняем обработанный текст в новый файл с именем promt{i+1}.txt
        new_file_name = f'promt{i + 1}.txt'
        new_file_path = os.path.join(txt_folder_path, new_file_name)
        with open(new_file_path, 'w', encoding='utf-8') as f:
            f.write(processed_text)
        
        # Удаляем исходный файл
        os.remove(file_path)

def read_txt_files(folder):
    txt_files = [f for f in os.listdir(folder) if f.endswith('.txt')]
    prompts = []

    for txt_file in txt_files:
        with open(os.path.join(folder, txt_file), 'r', encoding='utf-8') as file:
            text = file.read()
            prompt = extract_sentences(text)
            prompts.append(prompt)

    return prompts




from adress import fetch_and_extract_urls
from scraper import process_urls  
from generated_blog import process_text_files  
from generated_img import Text2ImageAPI, read_txt_files
from txttodoc import convert_txt_to_docx
import os
from dotenv import load_dotenv 


load_dotenv()
kandinsky_api  = os.environ.get("Kandinsky_API")
kandinsky_key  = os.environ.get("Kandinsky_KEY")

def main():
    # Базовый URL для получения ссылок
    site_url = "https://letidor.ru"
    # Шаг 1: Извлечение ссылок на статьи и сохранение
    fetch_and_extract_urls(site_url)
    # Шаг 2: Извлечение текста из статьи и сохранение
    process_urls()    
    # Шаг 3: Обработка текстов статей и генерация блогов
    process_text_files()
    txt_folder_path = 'blog'  
    docx_folder_path = 'blog'
    convert_txt_to_docx(txt_folder_path, docx_folder_path)
    #Шаг 4:Генерация изображений по промту 
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', kandinsky_api, kandinsky_key) # инициализация API    
    model_id = api.get_model()# Получаем ID модели
    folder_path = 'blog'    
    prompts = read_txt_files(folder_path)# Чтение текстов из файлов и извлечение первых трёх предложений
    # Генерация изображений для каждого текстового файла
    for i, prompt in enumerate(prompts):
        print(f"Генерируется изображение {i + 1} по промту: {prompt}")        
        uuid = api.generate(prompt, model_id)
        if uuid:
            # Проверка статуса генерации и получение изображения в Base64
            images_base64 = api.check_generation(uuid)
            if images_base64:
                # Сохраняем изображения локально
                api.save_images_locally(images_base64, folder=f'generated_images_{i + 1}')
            else:
                print(f"Изображения для запроса не сгенерированы.{i + 1}.")
        else:
            print(f"Не удалось сгенерировать запрос для промта {i + 1}.")


main()

#
# Script Start huggingface AI model | v1.1
# in Cursus (Unesell Studio)
# Потребление: RAM: 11Гб | ROM: 12Гб
#
# загрузка токенизатора и модели | https://huggingface.co/models?pipeline_tag=conversational
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration, MarianMTModel, MarianTokenizer
from diffusers import StableDiffusionPipeline
from langdetect import detect
from urllib.parse import urlencode
import requests, time, torch, sys, random

# Loading: Blenderbot 1B
tokenizer = BlenderbotTokenizer.from_pretrained('facebook/blenderbot-1B-distill')
model = BlenderbotForConditionalGeneration.from_pretrained('facebook/blenderbot-1B-distill')
# Loading model compleate: Blenderbot 1B

# Loading: Helsinki-NLP
translator = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-ru-en")
tokenizer_translate = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-ru-en")
model_name = 'Helsinki-NLP/opus-mt-en-ru'  # Модель перевода с английского на русский
tokenizer_translate_en_ru = MarianTokenizer.from_pretrained(model_name)
model_translate = MarianMTModel.from_pretrained(model_name)
# Loading model compleate: Helsinki-NLP

# Loading: openjourney
model_id = "prompthero/openjourney"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")
# Loading model compleate: openjourney

mode = "online" # -local or -online
if(mode == ""): mode = "local"
print("Сессия активна. mode: {}".format (mode))

# Parametrs
API_URL = "https://unesell.com/api/"
translate = False
translate_engine = "nothing" # yandex - ru | nothing - en
top_k = 50
machine = "Colab" # На чём запущен сейчас ИИ.

def StableDiffusion(prompt, id, user):
    temp = random.randint(10000000, 90000000)
    name = "./img_sd_" + user + "_im_" + str(temp) + ".png"

    language = detect(prompt)
    if language != "en":
      translation_input = tokenizer_translate(prompt, truncation=True, padding='longest', return_tensors='pt').to(translator.device)
      translated = translator.generate(**translation_input)
      prompt = tokenizer_translate.batch_decode(translated, skip_special_tokens=True)[0]

    output = pipe(prompt)

    image = output.images[0]
    image.save(name)

    # Отправка изображения на сервер через PHP
    upload_image_to_server(name)
    img = "img_sd_" + user + "_im_" + str(temp) + ".png";
    img_encoded = urlencode({'msg': img})
    requests.get(API_URL + "AI/send_img.php?msg_id=" + str(id) + "&user=" + user + "&" + img_encoded)
    print('Изображение отправлено на сервер.')

    return True

def upload_image_to_server(image_path):
    # Загрузка изображения на сервер через PHP
    url = 'https://unesell.com/app/cursus/ai.upload.php'
    files = {'file': open(image_path, 'rb')}
    response = requests.post(url, files=files)

    if response.status_code == 200:
        print('Изображение успешно загружено на сервер')
        return True
    else:
        print('Ошибка загрузки изображения на сервер')
        return False

def AI(user_text, id, user):

    language = detect(user_text)
    if language != "en":
        translate = True
    else:
        translate = False

    # Переменнные, влияющие на качесвто ответа
    temperature = random.uniform(1.3, 1.5)
    top_p = random.uniform(0.8, 1.2)

    user_input = user_text
    # Перевод текста, если необходимо
    if translate:
      # Переводим user_input с русского на английский
      translation_input = tokenizer_translate(user_input, truncation=True, padding='longest', return_tensors='pt').to(translator.device)
      translated = translator.generate(**translation_input)
      user_input = tokenizer_translate.batch_decode(translated, skip_special_tokens=True)[0]

    if(mode == "online"):
        print("User >> " + user_input)

    # Generate bot response
    input_ids = tokenizer.encode(user_input, return_tensors='pt')
    bot_output = model.generate(input_ids, max_new_tokens=1000, pad_token_id=tokenizer.eos_token_id, temperature=temperature, top_p=top_p, top_k=top_k)
    bot_response = tokenizer.decode(bot_output[0], skip_special_tokens=True)

    if translate:
        translation_input = tokenizer_translate_en_ru(bot_response, truncation=True, padding='longest', return_tensors='pt').to(model_translate.device)
        translated = model_translate.generate(**translation_input)
        bot_response = tokenizer_translate_en_ru.batch_decode(translated, skip_special_tokens=True)[0]

        #print("(Temp: " + str(temperature) + " | Top_P: " + str(top_p) + ")")
        print("GPT >>>" + bot_response)
        if(mode == "online"):
            requests.get(API_URL + "AI/send.php?msg_id=" + id + "&user=" + user + "&msg=" + bot_response)
    else:
        print("(Temp: " + str(temperature) + " | Top_P: " + str(top_p) + ")")
        print("GPT >>>" + bot_response)
        bot_response = bot_response.replace("'", "`")
        if(mode == "online"):
            requests.get(API_URL + "AI/send.php?msg_id=" + id + "&user=" + user + "&msg=" + bot_response)

    return True

while True:
    if(mode == "online"):
        messages = requests.get(API_URL + "AI/input.php");

        data = messages.json()
        if messages.text != "null":

          if data['msg'] == "/help":
            help = "Cursus Bot - " + machine + " Run <br><br><strong>Основные команды:</strong><br><small>/translate [ru | en] to [ru | en] {ваш текст}</small><br><small>/help</small><br>"
            help_encoded = urlencode({'msg': help})
            requests.get(API_URL + "AI/send.php?msg_id=" + data['msg_id'] + "&user=" + data['outgoing_msg_id'] + "&" + help_encoded)
          elif data['msg'].startswith("/translate ru to en"):
            text = data['msg'].replace('/translate ru to en ', '')
            print("Перевод строки: " + text);
            translation_input = tokenizer_translate(text, truncation=True, padding='longest', return_tensors='pt').to(translator.device)
            translated = translator.generate(**translation_input)
            translation_result = tokenizer_translate.batch_decode(translated, skip_special_tokens=True)[0]
            translation_result = translation_result.replace("'", "`")
            translation_result_encoded = urlencode({'msg': '<small>Перевод:</small><br>' + translation_result})
            print("Перевод строки: " + translation_result);

            response = requests.get(API_URL + "AI/send.php?msg_id=" + data['msg_id'] + "&user=" + data['outgoing_msg_id'] + "&" + translation_result_encoded)
            print(response.text)

          elif data['msg'].startswith("/imageline "):
            text = data['msg'].replace('/imageline ', '')
            print("Генерация изображения: " + text);
            StableDiffusion(data['msg'], data['msg_id'], data['outgoing_msg_id'])

          elif data['msg'].startswith("/translate en to ru"):
            text = data['msg'].replace('/translate en to ru ', '')
            print("Перевод строки: " + text);
            translation_input = tokenizer_translate_en_ru(text, truncation=True, padding='longest', return_tensors='pt').to(model_translate.device)
            translated = model_translate.generate(**translation_input)
            translation_result = tokenizer_translate_en_ru.batch_decode(translated, skip_special_tokens=True)[0]

            translation_result_encoded = urlencode({'msg': '<small>Translation:</small><br>' + translation_result})
            print("Перевод строки: " + translation_result);

            response = requests.get(API_URL + "AI/send.php?msg_id=" + data['msg_id'] + "&user=" + data['outgoing_msg_id'] + "&" + translation_result_encoded)
            print(response.text)

          else:
            try:
              # Генерация ответа ИИ
              AI(data['msg'], data['msg_id'], data['outgoing_msg_id'])
            except:
              requests.get(API_URL + "AI/send.php?msg_id=" + data['msg_id'] + "&user=" + data['outgoing_msg_id'] + "&msg=" + "Error. Please, input any text.")

            time.sleep(1)

        else:
            time.sleep(1)
    else:
        AI(input("User >> "), 0, 0)
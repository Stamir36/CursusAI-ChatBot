#
# Script Start huggingface AI model
# in Cursus (Unesell Studio)
#
# загрузка токенизатора и модели | https://huggingface.co/models?pipeline_tag=conversational
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
tokenizer = BlenderbotTokenizer.from_pretrained('facebook/blenderbot-400M-distill')
model = BlenderbotForConditionalGeneration.from_pretrained('facebook/blenderbot-400M-distill')
# Loading model compleate: Blenderbot 400M
from langdetect import detect
import requests, time, torch, sys, random

mode = sys.argv[1] # -local or -online
if(mode == ""): mode = "local"
print("Сессия активна. mode: {}".format (mode))

# Parametrs
API_URL = "https://unesell.com/api/"
translate = False
translate_engine = "yandex" # yandex - ru | nothing - en
top_k = 50

# Переводчик яндекса
def ya_translate(text, locale):
    IAM_TOKEN = 't1.9euelZqMlMaKicmXxo2QjpmZl5SdjO3rnpWaiZCOj5aVisqNzoyTno-Zycvl9Pd_EgRf-e89LXz73fT3P0EBX_nvPS18-w.qUFUt5TbDZHYwEugJJ40YOnEwTv-iZjJRmT7cXFYrlkaOU7jVYVykhs47LsMAtT11_79iN-AqPKL6s3E0-dGDw'
    folder_id = 'b1gfkjimuv1169e8sen5'
    target_language = locale

    body = {
        "targetLanguageCode": target_language,
        "texts": text,
        "folderId": folder_id,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(IAM_TOKEN)
    }

    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
        json = body,
        headers = headers
    )
    response.encoding = 'utf-8'
    data = response.json()
    return data['translations'][0]['text']

def AI(user_text, id, user):

    language = detect(user_text)
    if language != "en":
        translate = True
    else:
        translate = False

    # Переменнные, влияющие на качесвто ответа
    temperature = random.uniform(1.3, 1.5)
    top_p = random.uniform(0.8, 1.2)

    # получаем вопрос от пользователя
    if translate_engine == "yandex" and translate:
        user_input = ya_translate(user_text, "en")
    else:
        user_input = user_text
    
    if(mode == "online"):
        print("User >> " + user_text)
    
    # Generate bot response
    input_ids = tokenizer.encode(user_input, return_tensors='pt')
    bot_output = model.generate(input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id, temperature=temperature, top_p=top_p, top_k=top_k)
    bot_response = tokenizer.decode(bot_output[0], skip_special_tokens=True)

    if translate_engine == "yandex" and translate:
        bot_response = ya_translate(bot_response, "ru")
        #print("(Temp: " + str(temperature) + " | Top_P: " + str(top_p) + ")")
        print("GPT >>>" + bot_response)
        if(mode == "online"):
            requests.get(API_URL + "AI/send.php?msg_id=" + id + "&user=" + user + "&msg=" + bot_response)
    else:
        #print("(Temp: " + str(temperature) + " | Top_P: " + str(top_p) + ")")
        print("GPT >>>" + bot_response)
        if(mode == "online"):
            requests.get(API_URL + "AI/send.php?msg_id=" + id + "&user=" + user + "&msg=" + bot_response)
    
    return True

while True:
    if(mode == "online"):
        messages = requests.get(API_URL + "AI/input.php");

        data = messages.json()
        if messages.text != "null":
            AI(data['msg'], data['msg_id'], data['outgoing_msg_id'])
            time.sleep(1)
        else:
            time.sleep(1)
    else:
        AI(input("User >> "), 0, 0)
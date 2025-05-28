import telebot
import pickle
import time
import os
from dotenv import load_dotenv


load_dotenv(override=True)

def post_msg():
    token = os.getenv('TOKEN')
    chat_id = os.getenv('CHAT_ID')
    bot = telebot.TeleBot(token)

    with open('link_list_fx.pickle', 'rb') as file:
        link_list = pickle.load(file)

    count = 1
    while True:
        try:
            for i in range(len(link_list)):
                bot.send_message(chat_id=chat_id, text=link_list[count-1])
                print(f'Sent {count}/{len(link_list)} messages! ({round(count / len(link_list) * 100, 2)}%)')
                time.sleep(0.5)
                count += 1
                if count == (len(link_list)):
                    break
        except telebot.apihelper.ApiTelegramException as e:
            print('Error 429: Too Many Requests\n', e)
            time.sleep(5)
        except IndexError:
            print('List index out of range, but it is alright, job is done!')
            break
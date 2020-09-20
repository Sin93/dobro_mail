from BotLogic.Bot import Bot
from config import TOKEN, VK_GROUP_ID
from flask import Flask, request
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

import json
import socket


# app = Flask(__name__)
#
#
# @app.route('/', methods=['POST'])
# def server():
#     if 'type' not in data.keys():
#         return 'not vk'
#     if data['type'] == 'confirmation':
#         return confirmation_token
#     elif data['type'] == 'message_new':
#         event = json.loads(request.data)
#         user_id = event.object.message['from_id']
#         user_message = event.object.message['text']
#         information = event.object.message.get('payload')
#
#         Bot(user_id, user_message, information)
#
#         return 'ok'
#
#
# if __name__ == '__main__':
#
#     app.run(debug=True)


def main():
    vk_session = VkApi(token=TOKEN)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, VK_GROUP_ID)

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            print(event.object)
            user_id = event.object.message['from_id']
            user_message = event.object.message['text']
            if 'carousel' in event.object.client_info:
                user_can_read_carusel = True
            else:
                user_can_read_carusel = False
            information = event.object.message.get('payload')

            # создаётся эктемпляр класса, который управляет логикой бота
            Bot(user_id, user_message, information, user_can_read_carusel)

if __name__ == '__main__':
    main()

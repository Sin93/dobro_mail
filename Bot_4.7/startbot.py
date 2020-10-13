from BotLogic.Bot import Bot
from BotLogic.TaskManager import set_interval, start_new_thread, SendRemindMessage, UpdateDatabase, ClearDatabase
from config import TOKEN, VK_GROUP_ID, REMIND_TIME, UPDATE_DATABASE_TIME, DELETE_PROJECTS_AND_MSG_TIME
# from flask import Flask, request
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

# import json


# app = Flask(__name__)

#
# @app.route('/', methods=['POST'])
# def server():
#     data = json.loads(request.data)
#     if 'type' not in data.keys():
#         return 'not vk'
#     if data['type'] == 'confirmation':
#         return confirmation_token
#     elif data['type'] == 'message_new':
#         event = json.loads(request.data)
#         user_id = event['object']['message']['from_id']
#         user_message = event['object']['message']['text']
#         if 'carousel' in event.object.client_info:
#             user_can_read_carusel = True
#         else:
#             user_can_read_carusel = False
#         information = event['object']['message'].get('payload')
#
#         Bot(user_id, user_message, information, user_can_read_carusel)
#
#
# if __name__ == '__main__':
#     set_interval(time=REMIND_TIME, function=start_new_thread, counter=15, thread=SendRemindMessage)
#     set_interval(time=UPDATE_DATABASE_TIME, function=start_new_thread, counter=15, thread=UpdateDatabase)
#     app.run(debug=True)

def main():
    vk_session = VkApi(token=TOKEN)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, VK_GROUP_ID)

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            print(f'event = {event.object}')
            user_id = event.object.message['from_id']
            user_message = event.object.message['text']
            user_can_read_carusel = event.object.client_info.get('carousel')
            information = event.object.message.get('payload')

            # создаётся эктемпляр класса, который управляет логикой бота
            Bot(user_id, user_message, information, user_can_read_carusel)


if __name__ == '__main__':
    # создание нового потока для напоминания о проектах. Counter = 15 => Сработает 15 раз
    set_interval(time=REMIND_TIME, function=start_new_thread, counter=15, thread=SendRemindMessage)
    # создание нового потока для обновления базы данных
    set_interval(time=UPDATE_DATABASE_TIME, function=start_new_thread, counter=15, thread=UpdateDatabase)
    # создание нового потока для удаления неактивных проектов и устаревших сообщений. Counter=None => работает всегда
    set_interval(time=DELETE_PROJECTS_AND_MSG_TIME, function=start_new_thread, counter=None, thread=ClearDatabase)
    main()

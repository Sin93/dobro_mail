from config import TOKEN, VK_GROUP_ID
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

import requests
import vk_api


def write_msg(user_id, message):
    random_id = vk_api.utils.get_random_id()
    vk.messages.send(
        user_id=user_id,
        message=message,
        random_id=random_id
    )


vk_session = VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, VK_GROUP_ID)

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        from_user_id = event.object.message['from_id']
        print(event.object)

        write_msg(from_user_id, 'Ответ бота')

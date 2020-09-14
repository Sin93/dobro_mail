from config import TOKEN, VK_GROUP_ID
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from BotLogic.Bot import Bot


def main():
    vk_session = VkApi(token=TOKEN)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, VK_GROUP_ID)

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            print(event.object)
            user_id = event.object.message['from_id']
            user_message = event.object.message['text']
            information = event.object.message.get('payload')

            # создаётся эктемпляр класса, который управляет логикой бота
            Bot(user_id, user_message, information)

if __name__ == '__main__':
    main()

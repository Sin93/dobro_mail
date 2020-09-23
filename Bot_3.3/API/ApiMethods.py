import requests

from config import TOKEN, BASE_DIR
from vk_api import VkApi, utils
from typing import Optional

import json


class ApiMethodsClass():
    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message
        self.json_keyboard = self.create_json_keyboard(self.message['keyboard'], self.message['inline'])
        ApiMethodsClass.send_msg_and_keyboard(user_id, message['message'], message['attachment'], self.json_keyboard)

    def create_json_keyboard(self, keyboard, inline=False):
        """Принимает список кнопок, и где их располагать (inline=True - в сообщении, =False - в клавиатуре внизу)
        генерирует из них словарь, а затем переводит в json.
        Возвращает строку с json объектом."""
        keyboard_for_send = {
            "one_time": False,
            "buttons": []
        }

        if inline:
            keyboard_for_send['inline'] = True

        for button in keyboard:
            new_button = [{
                "action": {
                    "type": button['type'],
                    "label": button['label'],
                    "payload": button['payload'],
                },
                "color": button['color']
            }]

            if button['link'] is not None:
                new_button[0]['action']['link'] = button['link']
                new_button[0]['color'] = None

            keyboard_for_send["buttons"].append(new_button)

        return json.dumps(keyboard_for_send)


    @staticmethod
    def send_msg_and_keyboard(
        user_id: int,
        message: str,
        attachment: str,
        keyboard: Optional[str]=None):

        vk_session = VkApi(token=TOKEN)
        vk = vk_session.get_api()
        random_id = utils.get_random_id()
        if keyboard is not None:
            vk.messages.send(
                user_id=user_id,
                message=message,
                keyboard=keyboard,
                random_id=random_id,
                attachment=attachment
            )
        else:
            vk.messages.send(
                user_id=user_id,
                message=message,
                random_id=random_id,
                attachment=attachment
            )

    @staticmethod
    def photoUploadServer():
        vk_session = VkApi(token=TOKEN)
        vk = vk_session.get_api()
        response = vk.photos.getMessagesUploadServer(peer_id = 0)
        return response

    @staticmethod
    def savePhoto(photo, server, hash):
        vk_session = VkApi(token=TOKEN)
        vk = vk_session.get_api()

        return vk.photos.saveMessagesPhoto(
            photo=photo,
            server=server,
            hash=hash
        )
# test photo = photo-198392433_457239036
# owner_id = -198392433
# media_id = 457239036
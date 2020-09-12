from config import TOKEN
from vk_api import VkApi, utils
from typing import Optional

import json


class ApiMethodsClass():
    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message
        print(self.message)
        self.json_keyboard = self.create_json_keyboard(self.message['keyboard'], self.message['inline'])
        ApiMethodsClass.send_msg_and_keyboard(user_id, message['message'], self.json_keyboard)

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
                },
                "color": button['color'],
            }]

            # if payload:
            #     new_button[0]['action']['payload'] = payload

            keyboard_for_send["buttons"].append(new_button)

        return json.dumps(keyboard_for_send)


    @staticmethod
    def send_msg_and_keyboard(
        user_id: int,
        message: str,
        keyboard: Optional[str]=None):

        vk_session = VkApi(token=TOKEN)
        vk = vk_session.get_api()

        random_id = utils.get_random_id()
        if keyboard is not None:
            vk.messages.send(
                user_id=user_id,
                message=message,
                keyboard=keyboard,
                random_id=random_id
            )
        else:
            vk.messages.send(
                user_id=user_id,
                message=message,
                random_id=random_id
            )

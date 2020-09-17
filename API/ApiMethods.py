from config import TOKEN, ACCESS_TOKEN, API_LINK, API_VERSION, VK_GROUP_ID, GROUP_PHOTO_ALBUM_ID, PHOTOS_DIR
from vk_api import VkApi, utils
from typing import Optional, List

import json
import os
import requests


class ApiMethodsClass():
    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message
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

    @staticmethod
    def get_upload_server():
        response = requests.get(
            API_LINK.format(method_name='photos.getUploadServer'),
            params={
                'access_token': ACCESS_TOKEN,
                'album_id': GROUP_PHOTO_ALBUM_ID,
                'group_id': VK_GROUP_ID,
                'v': API_VERSION
            }
        ).json()

        print(response)

        return response['response']['upload_url']



    @staticmethod
    def send_carousel(elements: List):
        pass

    @staticmethod
    def upload_image():
        upload_url = ApiMethodsClass.get_upload_server()

        all_photo = os.listdir(PHOTOS_DIR)

        for photo in all_photo:
            file = {'file1': open(f'{PHOTOS_DIR}{photo}', 'rb')}
            upload_response = requests.post(upload_url, files=file).json()
            save_photo_in_album = requests.get(
                API_LINK.format(method_name='photos.save'),
                params={
                    'access_token': ACCESS_TOKEN,
                    'album_id': GROUP_PHOTO_ALBUM_ID,
                    'group_id': VK_GROUP_ID,
                    'server': upload_response['server'],
                    'photos_list': upload_response['photos_list'],
                    'hash': upload_response['hash']
                }
            ).json()

        return


    @staticmethod
    def crete_album():
        pass

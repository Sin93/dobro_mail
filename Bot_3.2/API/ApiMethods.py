from config import TOKEN, API_LINK, GROUP_PHOTO_ALBUM_ID, VK_GROUP_ID, ACCESS_TOKEN, API_VERSION
from vk_api import VkApi, utils
from vk_api.keyboard import *
from typing import Optional, List

import json
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

        line_number = 0
        for line in keyboard:
            if line == []:
                print('Клавиатура пустая')
                return json.dumps([])

            if isinstance(line, list):
                keyboard_for_send["buttons"].append([])
                for button in line:
                    new_button = {
                        "action": {
                            "type": button['type'],
                            "label": button['label'],
                            "payload": button['payload']
                        },
                        "color": button['color']
                    }

                    if button['link'] is not None:
                        new_button[0]['action']['link'] = button['link']
                        new_button[0]['color'] = None

                    keyboard_for_send["buttons"][line_number].append(new_button)
                line_number += 1
            elif isinstance(line, dict):
                button = line
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
        keyboard: Optional[str]=None,
        template: Optional[str]=None,
        photo_id: Optional[str]=None):

        vk_session = VkApi(token=TOKEN)
        vk = vk_session.get_api()

        random_id = utils.get_random_id()
        if template is not None:
            vk.messages.send(
                user_id=user_id,
                message=message,
                template=template,
                random_id=random_id
            )
        if keyboard is not None:
            vk.messages.send(
                user_id=user_id,
                message=message,
                keyboard=keyboard,
                random_id=random_id,
                attachment=f'photo{photo_id}_{TOKEN}'
            )
        else:
            vk.messages.send(
                user_id=user_id,
                message=message,
                random_id=random_id,
                attachment=f'photo{photo_id}_{TOKEN}'
            )


    @staticmethod
    def send_carousel(user_id, elements):
        random_id = utils.get_random_id()


    @staticmethod
    def create_json_carusel(elements_list: List):
        carusel = {
            'type': 'carousel',
            'elements': []
        }

        for element in elements_list:
            carusel['elements'].append(element)

        return json.dumps(carusel)


    @staticmethod
    def create_carusel_element(
        title: str,
        description: str,
        project_link='https://dobro.mail.ru',
        payload={"project":"3119"},  # убрать этот хардкод
        photo_id='-198392433_457239035',  # убрать этот хардкод
        action='open_photo'):
        """Создаёт элемент карусели.
        title - заголовок, можно передавать строку, но максимум 80 символов
        description - подзаголовок, можно передавать строку, но так-же 80 символов
        buttons - список кнопок, максимум 3, каждая кнопка - словарь ...
        action - что должно происходить при нажатии на элемент карусели,
            по умолчанию - 'open_photo' - открывает фото элемента карусели,
            есть ещё тип 'open_link', который открывает ссылку, можно и его
            добавить но мне кажется, open_photo нам будет достаточно,
            ссылку лучше с кнопкой передать
        photo_id - id фото проекта из группы вк (строкой, например '-198392433_457239028'),
            фото должно быть строго 13:8, минимальный размер фото 221х136
        """

        # чтоб не передать случайно больше 80 символов, сразу обрезаем
        title = title[:80]
        description = description[:80]

        element = {
            'title': title,
            'description': description,
            'photo_id': photo_id,
            "action": {
                "type": 'open_photo',
            },
            'buttons': [
                {
                "action": {
                    "type": "text",
                    "label": "Подробнее",
                    "payload": payload
                    }
                },
                {
                "action": {
                    "type": "text",
                    "label": "Пожертвовать",
                    "payload": payload
                    }
                },
            ]
        }
        return element

    """Тут загрузка фотографий в альбом, основная проблема с тем, что требуется
    авторизация админа группы и его токен, но как это сделать в автоматическом
    режиме - пока не придумал"""
    @staticmethod
    def get_upload_server():
        response = requests.get(
            API_LINK.format(method_name='photos.getUploadServer'),
            params={
                'album_id': GROUP_PHOTO_ALBUM_ID,
                'group_id': VK_GROUP_ID,
                'access_token': ACCESS_TOKEN,
                'v': API_VERSION
            }
        ).json()

        print(response)

        return response


    # @staticmethod
    # def upload_image():
    #     upload_url = ApiMethodsClass.get_upload_server()
    #
    #     all_photo = os.listdir(PHOTOS_DIR)
    #
    #     for photo in all_photo:
    #         file = {'file1': open(f'{PHOTOS_DIR}{photo}', 'rb')}
    #         upload_response = requests.post(upload_url, files=file).json()
    #         save_photo_in_album = requests.get(
    #             API_LINK.format(method_name='photos.save'),
    #             params={
    #                 'access_token': ACCESS_TOKEN,
    #                 'album_id': GROUP_PHOTO_ALBUM_ID,
    #                 'group_id': VK_GROUP_ID,
    #                 'server': upload_response['server'],
    #                 'photos_list': upload_response['photos_list'],
    #                 'hash': upload_response['hash']
    #             }
    #         ).json()
    #
    #     return

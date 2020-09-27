import requests

from config import TOKEN, BASE_DIR, ACCESS_TOKEN, GROUP_PHOTO_ALBUM_ID, VK_GROUP_ID
from vk_api import VkApi, utils, upload
from typing import Optional, List

import json


class ApiMethodsClass():
    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message
        self.json_keyboard = self.create_json_keyboard(self.message['keyboard'], self.message['inline'])
        ApiMethodsClass.send_msg_and_keyboard(
            user_id=self.user_id,
            message=message['message'],
            keyboard=self.json_keyboard,
            photo_id=message['attachment']
        )

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

    # @staticmethod
    # def send_msg_and_keyboard(
    #     user_id: int,
    #     message: str,
    #     attachment: str,
    #     keyboard: Optional[str]=None):
    #
    #     vk_session = VkApi(token=TOKEN)
    #     vk = vk_session.get_api()
    #     random_id = utils.get_random_id()
    #     if keyboard is not None:
    #         vk.messages.send(
    #             user_id=user_id,
    #             message=message,
    #             keyboard=keyboard,
    #             random_id=random_id,
    #             attachment=attachment
    #         )
    #     else:
    #         vk.messages.send(
    #             user_id=user_id,
    #             message=message,
    #             random_id=random_id,
    #             attachment=attachment
    #         )


    # @staticmethod
    # def send_carousel(user_id, elements):
    #     random_id = utils.get_random_id()


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

    @staticmethod
    def upload_photo(link_to_photo='/home/maxim/projects/project_images/1710.jpg'):
        vk_session = VkApi(token=ACCESS_TOKEN)
        vk = vk_session.get_api()

        up_photo = upload.VkUpload(vk_session).photo(
            photos=link_to_photo,
            album_id=GROUP_PHOTO_ALBUM_ID,
            group_id=VK_GROUP_ID)

        return up_photo

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

    @staticmethod
    def checkUserActivity(user_id):
        vk_session = VkApi(token=TOKEN)
        vk = vk_session.get_api()

        return vk.messages.getLastActivity(user_id=user_id)

# test photo = photo-198392433_457239036
# owner_id = -198392433
# media_id = 457239036

import requests

from config import TOKEN, BASE_DIR
from vk_api import VkApi, utils
from typing import Optional, List

import json


class ApiMethodsClass():
    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message
        self.json_keyboard = self.create_json_keyboard(self.message['keyboard'], self.message['inline'])
        print(self.message['carousel'])
        self.template = self.create_json_carusel(self.message['carousel']) if self.message['carousel'] is not None else None
        ApiMethodsClass.send_msg_and_keyboard(
            user_id=self.user_id,
            message=message['message'],
            keyboard=self.json_keyboard,
            template=self.template,
            attachment=message['attachment'] # В attachment передается строка типа photo{project.picture.owner_id}_{project.picture.media_id}'
            # photo_id=message['attachment']
        )

    # функция преобразования в json для кнопок
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
        attachment: Optional[str]=None,
        # photo_id: Optional[str]=None
    ):
        """Отправляет сообщение, если в template передать элемент карусели,
        то к сообщению будет подключена "карусель", важно проверять,
        что пользователь может считывать карусель на своём устройстве"""

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
                attachment=attachment
                # attachment=f'photo{photo_id}_{TOKEN}'
            )
        else:
            vk.messages.send(
                user_id=user_id,
                message=message,
                random_id=random_id,
                attachment=attachment
                # attachment=f'photo{photo_id}_{TOKEN}'
            )

    @staticmethod
    def create_json_carusel(elements_list: List):
        """Формирует карусель, готовую к отправке в сообщении.
        На вход принимает список элементов карусели, каждый отдельный элемент
        можно сделать с помощью метода create_carusel_element"""
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
        project_link: str,
        payload: dict,
        photo_id: str,
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
    def photoUploadServer():
        """
        Возвращает данные сервера для зарузки фото
        :return:
        """
        vk_session = VkApi(token=TOKEN)
        vk = vk_session.get_api()
        response = vk.photos.getMessagesUploadServer(peer_id=0)
        return response

    @staticmethod
    def savePhoto(photo, server, hash):
        """
        Возвращает информацию о сохраненной фотографии
        :param photo:
        :param server:
        :param hash:
        :return:
        """
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
# tesy_img -198392433_457239204
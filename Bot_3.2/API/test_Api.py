from API.ApiMethods import *


class ApiMethodsClassTest:

    def __init__(self):
        # self.message = message['message']
        # print(f'send to {user_id} - {self.message}')

        # тест отправки карусели
        # elements = []
        # el = ApiMethodsClass.create_carusel_element(title='я первый элемент', description='я описание первого элемента', project_link='vk.com')
        # elements.append(el)
        # el = ApiMethodsClass.create_carusel_element(title='я второй элемент', description='я описание второго элемента', project_link='vk.com')
        # elements.append(el)
        # car = ApiMethodsClass.create_json_carusel(elements)
        # ApiMethodsClass.send_msg_and_keyboard(user_id=9812280,message='test с каруселью',template=car)

        # тест кнопки в массиве
        keyboard = [
            [
                {
                    'type': 'text',
                    'label': 'Первая кнопка',
                    'color': 'positive',
                    'payload': None,
                    'link': None
                },
                {
                    'type': 'text',
                    'label': 'вторая кнопка',
                    'color': 'positive',
                    'payload': None,
                    'link': None
                }
            ],
            [
                {
                    'type': 'text',
                    'label': 'третья кнопка',
                    'color': 'positive',
                    'payload': None,
                    'link': None
                },
                {
                    'type': 'text',
                    'label': 'четвертая кнопка',
                    'color': 'positive',
                    'payload': None,
                    'link': None
                }
            ]
        ]

        keyboard = ApiMethodsClass.create_json_keyboard(keyboard=keyboard, inline=False)
        print(keyboard)

        ApiMethodsClass.send_msg_and_keyboard(user_id=9812280,message='test с клавиатурой',keyboard=keyboard)

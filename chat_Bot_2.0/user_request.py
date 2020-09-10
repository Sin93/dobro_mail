from BotResponse import BotResponse
from ApiMethods import ApiMethodsClass
import config


class Bot(BotResponse):
    def __init__(self, user_id, user_message, information):
        super().__init__(user_id, user_message, information, xml_url=None)
        self.generate_response()
        self.create_answer()
        self.send_answer()

    def send_answer(self):

        for message in self.response_data['messages']:

            ApiMethodsClass(
                user_id = self.user_id,
                message=message,
            )

        pass

    def create_answer(self):

        if self.response_data['projects'] is None:
            self.response_data['messages'].append(self.create_message(self.error_message))
        else:
            if len(self.response_data['projects']) != 0:

                message = f'По вашему запросу найдено {len(self.response_data["projects"])} проекта\n'
                self.response_data['messages'].append(self.create_message(message))
                for project in self.response_data["projects"]:
                    print(project.get_project_info())
                    self.response_data['messages'].append(self.create_message(project.get_project_info(), 'project', True))
            else:
                self.response_data['messages'].append(self.create_message('Другое'))

    @staticmethod
    def create_message(self, message, keyboard_type=None, inline=False):

        return {
            'message' : message,
            'keyboard': self.create_keyboard(keyboard_type),
            'inline': inline
        }

    @staticmethod
    def create_keyboard(self, type):
        keyboard = []

        if type == 'project':
            keyboard.append(self.create_button(type="text", label='Подробнее'))
            keyboard.append(self.create_button(type='text', label='Пожертвовать', link=config.PAYMENT_LINK))


            # keyboard = [
            #     {
            #         'type': 'Text',
            #         'label': 'Подробнее про проект'
            #         'payload': 3119
            #     },
            #     {
            #         'type': 'Open Link',
            #         'label': 'На сайт'
            #         'link': 'https://dobro.mail.ru/projects/pomogi-uchitsya/'
            #     }
            # ]

        return keyboard

    @staticmethod
    def create_button(self, type=None, label=None, payload=None, link=None):

        button = {
            'type': type,
            'label': label,
            'payload': payload,
            'link': link,
            "color": "positive"
        }

        return button

    def __str__(self):

        if self.response_data is None:
            answer = self.error_message
        else:
            if len(self.response_data['projects']) != 0:
                answer = f'По вашему запросу найдено {len(self.response_data["projects"])}\n'
                for project in self.response_data["projects"]:
                    answer += project.get_project_info()
            else:
                answer = 'Другое'

        return answer




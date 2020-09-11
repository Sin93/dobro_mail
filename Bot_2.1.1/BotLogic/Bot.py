from BotLogic.BotResponse.BotResponse import BotResponse
from API.ApiMethods import ApiMethodsClass
import config
from .BotResponse.Validation.DataSets.DataSet import PROJECT_NAMES


class Bot(BotResponse):
    def __init__(self, user_id, user_message, information):
        super().__init__(user_id, user_message, information, xml_url=None)
        self.create_answer()
        self.send_answer()
        self.save_info()

    def send_answer(self):

        for message in self.response_data['messages']:
            ApiMethodsClass(
                user_id=self.user_id,
                message=message,
            )

    def create_answer(self):
        if len(self.response_data['stack']) == 0:
            self.response_data['messages'].append(self.create_message(self.error_message))
        else:
            prev_key = None
            for key, item in self.response_data['stack'].items():

                if key == 'GRATITUDE':
                    self.response_data['messages'].append(self.create_message('Всегда рад помочь'))

                if key == 'START':
                    message = 'Чем я могу вам помочь?'
                    self.response_data['messages'].append(self.create_message('Здравствуйте'))
                    self.response_data['messages'].append(self.create_message(message, 'start'))

                if key == 'WELCOME':
                    self.response_data['messages'].append(self.create_message(item))
                if key == 'INFO' and prev_key == 'ACTION':
                    if self.response_data['stack'].get('PROJECTS') is None:
                        message = "О каком или каких проектах вы хотели бы узнать?"
                        self.response_data['messages'].append(self.create_message(message, 'projects'))

                if key == 'PROJECTS':
                    if self.response_data['projects'] is None:
                        self.response_data['messages'].append(self.create_message(self.error_message))
                    else:
                        message = f'По вашему запросу найдено {len(self.response_data["projects"])} проекта\n'
                        self.response_data['messages'].append(self.create_message(message))
                        for project in self.response_data["projects"]:
                            self.response_data['messages'].append(self.create_message(project.get_project_info(), 'project', True))

                prev_key = key

            if len(self.response_data['messages']) <= 1:
                if prev_key == 'WELCOME':
                    message = 'Чем я могу вам помочь?'
                    self.response_data['messages'].append(self.create_message(message))
                elif prev_key == 'ACTION':
                    self.response_data['messages'].append(self.create_message(self.error_message))

    def save_info(self):
        pass

    @staticmethod
    def create_message(message, keyboard_type=None, inline=False):

        return {
            'message' : message,
            'keyboard': Bot.create_keyboard(keyboard_type),
            'inline': inline
        }

    @staticmethod
    def create_keyboard(type):
        keyboard = []

        if type == 'project':
            keyboard.append(Bot.create_button(type="text", label='Подробнее'))
            keyboard.append(Bot.create_button(type='text', label='Пожертвовать', link=config.PAYMENT_LINK))

        if type == 'projects':
            for name in PROJECT_NAMES:
                keyboard.append(Bot.create_button(type='text', label=name.title()))

        if type == 'start':
            keyboard.append(Bot.create_button(type='text', label='Узнать о доступных проектах'))

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
    def create_button(type=None, label=None, payload=None, link=None):

        button = {
            'type': type,
            'label': label,
            'payload': payload,
            'link': link,
            "color": "positive"
        }

        return button



#test = Bot(1, 'Добрый день! Я бы хотел узнать информацию о проекте природа', '')
#test = Bot(1, 'Добрый день! Я бы хотел узнать информацию', '')
#test = Bot(1, 'Что-нибудь связанное с природой', '')

# Не работает. Можно связатьь с историей запросов. Если изначально ее не было или был конец разговора то тогда можно предоставлять общую информацию
#test = Bot(1, 'Добрый день! Я бы хотел узнать чуть подробнее о том что вы делаете', '')
#test = Bot(1, 'Хм. звучит интересно. думаю что я хотел бы помочь в этом деле', '')
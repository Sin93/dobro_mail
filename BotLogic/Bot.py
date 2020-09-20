from BotLogic.BotResponse.BotResponse import BotResponse
from API.ApiMethods import ApiMethodsClass
from .BotResponse.XML.XML import HTML
from .BotResponse.XML.ProjectClasses.Projects import UPLOAD_PROJECTS, CATEGORY_PROJECTS
import config
from .BotResponse.Validation.DataSets.DataSet import PROJECT_NAMES
import json


class Bot(BotResponse):
    def __init__(self, user_id, user_message, information):
        super().__init__(user_id, user_message, xml_url=config.XML_URL)
        print(type(information))
        self.information = information
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

        if self.information is not None:
            self.information = json.loads(self.information.replace("'", '"'))
            project_id = self.information.get('project')
            if self.user_text == 'Подробнее':
                HTML(project_id)
                message = UPLOAD_PROJECTS.get(project_id).get_full_project_info()
                self.response_data['messages'].append(self.create_message(message, 'info', False, payload=UPLOAD_PROJECTS.get(project_id)))
            if self.user_text == 'Назад':
                if project_id is not None:
                    for offer_id in CATEGORY_PROJECTS.get(project_id):
                        print(offer_id)
                        project = UPLOAD_PROJECTS.get(offer_id)
                        self.response_data['messages'].append(self.create_message(project.get_project_info(), 'project', True, payload=project))
                    message = 'Если вы хотите посмотреть проекты из других категорий нажмите кнопку Отмена'
                    self.response_data['messages'].append(self.create_message(message, 'back', False, payload=0))
                else:
                    self.check_history(search='', key='', add_key=None, message_num=1)
                    for message in self.previous_messages:
                        self.response_data['messages'].append(message)

            if self.user_text == 'Отмена':
                message = "О каком или каких проектах вы хотели бы узнать?"
                self.response_data['messages'].append(self.create_message(message, 'projects'))

            if self.user_text == 'Пожертвовать':
                message = 'Какую сумму вы хотели бы внести? \n Выберите или введите вручную'
                self.response_data['messages'].append(self.create_message(message, 'payment', False, payload=UPLOAD_PROJECTS.get(project_id)))


        else:

            if len(self.response_data['stack']) == 0:
                print('here')
                if self.check_history('пожертвовать', 'ACTION', add_key=None, limit=5):
                    error = False
                    for word in self.parsed_text:
                        try:
                            price = float(word)
                            error = False
                            break
                        except ValueError:
                            error = True

                    if error:
                        self.check_history(search='', key='', add_key=None, limit=20)
                        self.response_data['messages'].append(self.create_message(self.error_message, 'end', keyboard=self.previous_messages[-1]['keyboard']))
                    else:
                        message = 'Для оплаты перейдите по ссылке'
                        project_id = json.loads(self.previous_messages[0]['keyboard'][-2]['payload']).get('project')
                        project = UPLOAD_PROJECTS.get(project_id)
                        self.response_data['messages'].append(self.create_message(message, 'paylink', True, payload=project.url))
                        self.response_data['messages'].append(self.create_message('Спасибо за ваше пожертвование!', 'start', payload='0'))

                else:
                    self.check_history(search='', key='', add_key=None, limit=20)
                    self.response_data['messages'].append(self.create_message(self.error_message, 'end', keyboard=self.previous_messages[-1]['keyboard']))

            else:
                prev_key = None
                for key, item in self.response_data['stack'].items():

                    if key == 'GRATITUDE':
                        self.response_data['messages'].append(self.create_message('Всегда рад помочь', 'end', False))

                    if key == 'END':
                        self.response_data['messages'].append(self.create_message('Всего доброго', 'begin', False))

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
                                self.response_data['messages'].append(self.create_message(project.get_project_info(), 'project', True, payload=project))
                            message = 'Если вы хотите посмотреть проекты из других категорий нажмите кнопку Отмена'
                            self.response_data['messages'].append(self.create_message(message,'back', False, payload=0))

                    prev_key = key

                if len(self.response_data['messages']) <= 1:
                    if prev_key == 'WELCOME':
                        message = 'Чем я могу вам помочь?'
                        self.response_data['messages'].append(self.create_message(message, 'start'))
                    elif prev_key == 'ACTION':
                        self.check_history(search='', key='', add_key=None, limit=20)
                        self.response_data['messages'].append(self.create_message(self.error_message, 'end', keyboard=self.previous_messages[-1]['keyboard']))

    @staticmethod
    def create_message(message, keyboard_type=None, inline=False, payload=None, keyboard=None):

        return {
            'message' : message,
            'keyboard': Bot.create_keyboard(keyboard_type, payload) if keyboard is None else keyboard,
            'inline': inline
        }

    @staticmethod
    def create_keyboard(type, payload):
        keyboard = []
        #payload = f"{{\"offer_id\": \"{payload}\"}}"
        if type == 'project':
            keyboard.append(Bot.create_button(type="text", label='Подробнее', payload=f"{{\"project\": \"{payload.offer_id}\"}}"))
            keyboard.append(Bot.create_button(type='text', label='Пожертвовать', payload=f"{{\"project\": \"{payload.offer_id}\"}}"))

        if type == 'projects':
            for name in PROJECT_NAMES:
                keyboard.append(Bot.create_button(type='text', label=name.title()))
            keyboard.append(Bot.create_button(type='text', label='Закончить', color='primary'))

        if type == 'start':
            if payload is not None:
                keyboard.append(Bot.create_button(type='text', label='Назад',color='secondary', payload=f"{{\"messages\": \"{payload}\"}}"))
                pass
            keyboard.append(Bot.create_button(type='text', label='Узнать о доступных проектах'))
            keyboard.append(Bot.create_button(type='text', label='Закончить', color='primary'))

        if type == 'info':
            keyboard.append(Bot.create_button(type='text', label='Пожертвовать', payload=f"{{\"project\": \"{payload.offer_id}\"}}"))
            keyboard.append(Bot.create_button(type='text', label='Назад', color="secondary", payload=f'{{\"project\": \"{payload.category_id}\"}}'))
            keyboard.append(Bot.create_button(type='text', label='Выбрать другую категорию', color='negative', payload=f'{{\"project\": \"{payload.offer_id}\"}}'))
            keyboard.append(Bot.create_button(type='text', label='Закончить', color='primary'))

        if type == 'back':
            keyboard.append(Bot.create_button(type='text', label='Отмена', color='negative', payload=f"{{\"button\": \"{payload}\"}}"))
            keyboard.append(Bot.create_button(type='text', label='Закончить', color='primary'))

        if type == 'begin':
            keyboard.append(Bot.create_button(type='text', label='Начать', color='primary'))

        if type == 'end':
            keyboard.append(Bot.create_button(type='text', label='Закончить', color='primary'))

        if type == 'payment':
            keyboard.append(Bot.create_button(type='text', label='50' ))
            keyboard.append(Bot.create_button(type='text', label='100'))
            keyboard.append(Bot.create_button(type='text', label='150'))
            keyboard.append(Bot.create_button(type='text', label='300'))
            keyboard.append(Bot.create_button(type='text', label='500'))
            keyboard.append(Bot.create_button(type='text', label='Назад', color="secondary", payload=f'{{\"project\": \"{payload.category_id}\"}}'))
            keyboard.append(Bot.create_button(type='text', label='Отмена', color='negative', payload=f'{{\"project\": \"{payload.offer_id}\"}}'))
            keyboard.append(Bot.create_button(type='text', label='Закончить', color='primary'))

        if type == 'paylink':
            keyboard.append(Bot.create_button(type='open_link', label='Внести пожертвование', link=f'{payload}', payload='0'))

        return keyboard

    @staticmethod
    def create_button(type=None, label=None, payload=None, link=None, color='positive'):

        button = {
            'type': type,
            'label': label,
            'payload': payload,
            'link': link,
            "color": color
        }

        return button

    def check_history(self, search, key, add_key=None, message_num=0, limit=10, in_one=False):
        index = 1
        message_index = message_num
        with open(config.LOG_DIR + f'{self.user_id}.txt', 'a+', encoding='utf-8') as logs:
            logs.seek(0)
            log = logs.readlines()
            if len(log) != 0:
                while index != limit:
                    history_data = json.loads(log[-index])
                    if history_data['error_message'] == '':
                        self.previous_messages = history_data['messages']
                        action_type = history_data['stack'].get(key)
                        if action_type is not None and action_type.lower() == search:
                            if add_key is None:
                                return True if len(history_data['stack']) == 1 else False
                            elif history_data['stack'].get(add_key) is not None:
                                return True
                        elif search == '' and message_index == 0:
                            return True
                        else:
                            message_index -= 1
                            index += 1
                    else:
                        index += 1
        return False



#test = Bot(1, 'Добрый день! Я бы хотел узнать информацию о проекте природа', '')
#test = Bot(1, 'Добрый день! Я бы хотел узнать информацию', '')
#test = Bot(1, 'Что-нибудь связанное с природой', '')

# Не работает. Можно связатьь с историей запросов. Если изначально ее не было или был конец разговора то тогда можно предоставлять общую информацию
#test = Bot(1, 'Добрый день! Я бы хотел узнать чуть подробнее о том что вы делаете', '')
#test = Bot(1, 'Хм. звучит интересно. думаю что я хотел бы помочь в этом деле', '')
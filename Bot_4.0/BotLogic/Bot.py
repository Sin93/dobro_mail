import datetime

from BotLogic.BotResponse.BotResponse import BotResponse
from API.ApiMethods import ApiMethodsClass
from BotLogic.DatabaseMethods.bot_methods import Database
import config
import json


class Bot(BotResponse):
    def __init__(self, user_id, user_message, information, user_can_read_carusel):
        super().__init__(user_id, user_message)
        self.information = information
        self.user_can_read_carusel = user_can_read_carusel
        self.proceed_validation()
        self.generate_response()
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

            if self.user_text == 'Получать уведомления':
                Database.update_user(self.user_id, can_send_reminds=0)
                self.check_history(search='', key='', add_key=None, limit=5)
                self.response_data['messages'].append(self.create_message('Уведомления включены', keyboard=self.previous_messages[-1]['keyboard']))

            if self.user_text == 'Не получать уведомлений':
                Database.update_user(self.user_id, can_send_reminds=0)
                self.check_history(search='', key='', add_key=None, limit=5)
                self.response_data['messages'].append(self.create_message('Уведомления отключены', keyboard=self.previous_messages[-1]['keyboard']))

            if self.user_text == 'Подробнее':
                # Change to database
                project = Database.get_project(project_id=project_id)
                Database.update_user(self.user_id, last_project=project.offer_id)
                message = project.get_full_project_info()
                photo = f'photo{project.picture.owner_id}_{project.picture.media_id}'
                self.response_data['messages'].append(self.create_message(message, 'info', False, payload=project, attachment=photo))

            if self.user_text == 'Назад':
                if project_id is not None:
                    # Change to database
                    projects = Database.get_projects_by_category(category_id=project_id, amount=config.PROJECTS_AMOUNT)
                    for project in projects:
                        self.response_data['messages'].append(self.create_message(project.get_project_info(), 'project', True, payload=project))
                    payload = {
                        'category': projects[0].category.category_id,
                        'page': 1
                    }
                    self.response_data['messages'].append(self.create_message('Страница 1','pagination',True, payload=payload))
                    message = 'Если вы хотите посмотреть проекты из других категорий нажмите кнопку Отмена'
                    self.response_data['messages'].append(self.create_message(message, 'back', False, payload=0))
                else:
                    self.check_history(search='', key='', add_key=None, message_num=1)
                    for message in self.previous_messages:
                        self.response_data['messages'].append(message)

            if self.user_text == chr(187) or self.user_text == chr(171):# self.user_text == '<<' or '>>'
                page = self.information.get('page')
                category = self.information.get('category')
                self.response_data['projects'] = Database.get_projects_by_category(category, amount=config.PROJECTS_AMOUNT, page=page)
                if len(self.response_data['projects']) != 0:
                    for project in self.response_data['projects']:
                        self.response_data['messages'].append(self.create_message(project.get_project_info(),'project', True, payload=project))
                    # pagination here
                    if int(page) + 1 == 0:
                        page = 0
                    payload = {
                        'category': self.response_data['projects'][0].category.category_id,
                        'page': page
                    }
                    print(payload)
                    self.response_data['messages'].append(self.create_message(f'Страница {int(page)+1}', 'pagination', True, payload=payload))
                    message = 'Если вы хотите посмотреть проекты из других категорий нажмите кнопку Отмена'
                    self.response_data['messages'].append(self.create_message(message, 'back', False, payload=0))
                else:
                    message = "В этой категории больше нету проектов"
                    self.response_data['messages'].append(self.create_message(message, 'back', False, payload=0))

            if self.user_text == 'Отмена' or self.user_text == 'Выбрать другую категорию':
                message = "О каком или каких проектах вы хотели бы узнать?"
                self.response_data['messages'].append(self.create_message(message, 'projects'))

            if self.user_text == 'Пожертвовать':
                # Change to database
                message = 'Какую сумму вы хотели бы внести? \n Выберите или введите вручную'
                project = Database.get_project(project_id=project_id)
                self.response_data['messages'].append(self.create_message(message, 'payment', False, payload=project))

        else:

            if len(self.response_data['stack']) == 0:
                if self.check_history('пожертвовать', 'ACTION', add_key=None, limit=5):
                    error = False
                    for word in self.parsed_text:
                        try:
                            price = float(word)
                            print(price)
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
                        project = Database.get_project(project_id=project_id)
                        self.response_data['messages'].append(self.create_message(message, 'paylink', True, payload=project.url))
                        user = Database.get_or_create_user(self.user_id)
                        print(user.user_id, user.can_send_reminds)
                        if not user.can_send_reminds:
                            message = 'Если вы хотите получать уведомления то нажмите кнопку'
                            self.response_data['messages'].append(self.create_message(message, 'activate_remind', True))
                        self.response_data['messages'].append(self.create_message('Спасибо за ваше пожертвование!', 'start', payload='0'))
                        Database.update_user(self.user_id, last_time_donation=datetime.datetime.now(), last_project=-1)

                else:
                    self.check_history(search='', key='', add_key=None, limit=20)
                    self.response_data['messages'].append(self.create_message(self.error_message, 'end', keyboard=self.previous_messages[-1]['keyboard']))

            else:
                prev_key = None
                for key, item in self.response_data['stack'].items():

                    if key == 'GRATITUDE':
                        self.response_data['messages'].append(self.create_message('Всегда рад помочь', 'end', False))

                    if key == 'END':
                        Database.update_user(self.user_id, is_active=0)
                        user = Database.get_or_create_user(self.user_id)
                        print(user.__dict__.get('__data__'))
                        print(user.is_active)
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
                            category = self.response_data['projects'][0].category.category_id
                            Database.update_user(self.user_id, last_category=category)
                            self.response_data['messages'].append(self.create_message(message))
                            for project in self.response_data["projects"]:
                                self.response_data['messages'].append(self.create_message(project.get_project_info(), 'project', True, payload=project))
                            # pagination here
                            payload = {
                                'category': category,
                                'page': 0
                            }
                            self.response_data['messages'].append(self.create_message('Страница 1', 'pagination', True, payload=payload))
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
    def create_message(message, keyboard_type=None, inline=False, payload=None, keyboard=None, attachment=None):

        return {
            'message': message,
            'keyboard': Bot.create_keyboard(keyboard_type, payload) if keyboard is None else keyboard,
            'inline': inline,
            'attachment': attachment
        }

    @staticmethod
    def create_keyboard(type, payload):
        keyboard = []
        if type == 'project':
            keyboard.append(Bot.create_button(type="text", label='Подробнее', payload=f"{{\"project\": \"{payload.offer_id}\"}}"))
            keyboard.append(Bot.create_button(type='text', label='Пожертвовать', payload=f"{{\"project\": \"{payload.offer_id}\"}}"))

        if type == 'projects':
            categories = Database.get_all_categories()
            for category in categories:
                keyboard.append(Bot.create_button(type='text', label=category.name.title()))
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

        if type == 'remind_info':
            keyboard.append(Bot.create_button(type='text', label='Пожертвовать', payload=f"{{\"project\": \"{payload.offer_id}\"}}"))

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

        if type == 'pagination':
            keyboard.append(Bot.create_button(type='text', label=' << ', payload=f'{{\"page\": \"{int(payload["page"]) - 1}\", \"category\": \"{payload["category"]}\"}}'))
            keyboard.append(Bot.create_button(type='text', label=' >> ', payload=f'{{\"page\": \"{int(payload["page"]) + 1}\", \"category\": \"{payload["category"]}\"}}'))

        if type == 'disable_remind':
            keyboard.append(Bot.create_button(type='text', label='Не получать уведомлений', payload=f'{{\"project\": 0}}'))

        if type == 'activate_remind':
            keyboard.append(
                Bot.create_button(type='text', label='Получать уведомления', payload=f'{{\"project\": 0}}'))

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
        logs_data = Database.get_logs(self.user_id, limit=limit)
        if len(logs_data) != 0:
            while index != limit:
                history_data = json.loads(logs_data[index-1].log)
                print(history_data['stack'])
                # print(index)
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
        # with open(config.LOG_DIR + f'{self.user_id}.txt', 'a+', encoding='utf-8') as logs:
        #     logs.seek(0)
        #     log = logs.readlines()
        #     if len(log) != 0:
        #         while index != limit:
        #             history_data = json.loads(log[-index])
        #             if history_data['error_message'] == '':
        #                 self.previous_messages = history_data['messages']
        #                 action_type = history_data['stack'].get(key)
        #                 if action_type is not None and action_type.lower() == search:
        #                     if add_key is None:
        #                         return True if len(history_data['stack']) == 1 else False
        #                     elif history_data['stack'].get(add_key) is not None:
        #                         return True
        #                 elif search == '' and message_index == 0:
        #                     return True
        #                 else:
        #                     message_index -= 1
        #                     index += 1
        #             else:
        #                 index += 1
        return False



#test = Bot(1, 'Добрый день! Я бы хотел узнать информацию о проекте природа', '')
#test = Bot(1, 'Добрый день! Я бы хотел узнать информацию', '')
#test = Bot(1, 'Что-нибудь связанное с природой', '')

# Не работает. Можно связатьь с историей запросов. Если изначально ее не было или был конец разговора то тогда можно предоставлять общую информацию
#test = Bot(1, 'Добрый день! Я бы хотел узнать чуть подробнее о том что вы делаете', '')
#test = Bot(1, 'Хм. звучит интересно. думаю что я хотел бы помочь в этом деле', '')

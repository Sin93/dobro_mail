import datetime
from BotLogic.BotResponse.BotResponse import BotResponse
from API.ApiMethods import ApiMethodsClass
from BotLogic.DatabaseMethods.bot_methods import Database
import config
import json


class Bot(BotResponse):
    """
    Основной класс бота
    """
    def __init__(self, user_id, user_message, information, user_can_read_carousel):
        super().__init__(user_id, user_message)

        self.user_can_read_carousel = user_can_read_carousel
        self.information = information

        self.proceed_validation()
        self.generate_response()
        self.create_answer()
        self.send_answer()
        self.save_info()

    def send_answer(self):

        for message in self.response_data['messages']:
            ApiMethodsClass(
                user_id=self.user_id,
                message=message
            )

    def create_answer(self):
        # Выполняется только если пользователь нажал кнопку и в кнопке был payload
        if self.information is not None:

            self.information = json.loads(self.information.replace("'", '"'))
            # по умолчанию в project может находиться либо id проекта либо его категории
            project_id = self.information.get('project')

            # При нажатии на кнопку пользователь вводит только определенные сообщения
            # Далее идет перечисление возможных ответов пользователя

            if self.user_text == 'Получать уведомления':
                Database.update_user(self.user_id, can_send_reminds=1)
                # Получаем клавиатуру с предыдущего не ошибочного сообщения в переменной previous_messages
                self.check_history(search='', key='', add_key=None, limit=5)
                self.response_data['messages'].append(self.create_message(message='Уведомления включены', keyboard=self.previous_messages[-1]['keyboard']))

            if self.user_text == 'Не получать уведомлений':
                Database.update_user(self.user_id, can_send_reminds=0)
                # Получаем клавиатуру с предыдущего не ошибочного сообщения в переменной previous_messages
                self.check_history(search='', key='', add_key=None, limit=5)
                self.response_data['messages'].append(self.create_message(message='Уведомления отключены', keyboard=self.previous_messages[-1]['keyboard']))

            if self.user_text == 'Подробнее':
                # Получаем подробную информацию о проекте
                project = Database.get_project(project_id=project_id)
                Database.update_user(self.user_id, last_project=project.offer_id)
                message = project.get_full_project_info()
                photo = f'photo{project.picture.owner_id}_{project.picture.media_id}'
                self.response_data['messages'].append(self.create_message(message=message, keyboard_type='info', inline=False, payload=project, attachment=photo))

            if self.user_text == 'Назад':
                # Can be simplify

                # В данном случае project_id => category_id
                # Если он есть => Возвращаемся к списку проектов категории
                if project_id is not None:
                    projects = Database.get_projects_by_category(category_id=project_id, amount=config.PROJECTS_AMOUNT)
                    if self.user_can_read_carousel:
                        message = f'По вашему запросу найдено проектов: {len(projects)}'
                        carousel = Bot.create_template(type='carousel', data=projects)
                        self.response_data['messages'].append(self.create_message(message=message, carousel=carousel))
                    else:
                        for project in projects:
                            self.response_data['messages'].append(self.create_message(message=project.get_project_info(), keyboard_type='project', inline=True, payload=project))
                    # Пагинация
                    payload = {
                        'category': projects[0].category.category_id,
                        'page': 1
                    }
                    self.response_data['messages'].append(self.create_message(message='Страница 1', keyboard_type='pagination', inline=True, payload=payload))
                    message = 'Если вы хотите посмотреть проекты из других категорий нажмите кнопку Отмена'
                    self.response_data['messages'].append(self.create_message(message=message, keyboard_type='back', inline=False, payload=0))
                else:
                    # В противном случае просто возвращаем предыдущее сообщение
                    self.check_history(search='', key='', add_key=None, message_num=1)
                    for message in self.previous_messages:
                        self.response_data['messages'].append(message)

            # Обработка пагинации
            if self.user_text == chr(187) or self.user_text == chr(171):# self.user_text == '<<' or '>>'
                page = self.information.get('page')
                category = self.information.get('category')
                self.response_data['projects'] = Database.get_projects_by_category(category, amount=config.PROJECTS_AMOUNT, page=page)
                if len(self.response_data['projects']) != 0:
                    if self.user_can_read_carousel:
                        message = f'По вашему запросу найдено проектов: {len(self.response_data["projects"])}'
                        carousel = Bot.create_template(type='carousel', data=self.response_data['projects'])
                        self.response_data['messages'].append(self.create_message(message=message, carousel=carousel))
                    else:
                        for project in self.response_data['projects']:
                            self.response_data['messages'].append(self.create_message(message=project.get_project_info(), keyboard_type='project', inline=True, payload=project))
                    # pagination here
                    if int(page) + 1 == 0:
                        page = 0
                    payload = {
                        'category': self.response_data['projects'][0].category.category_id,
                        'page': page
                    }
                    print(payload)
                    self.response_data['messages'].append(self.create_message(message=f'Страница {int(page)+1}', keyboard_type='pagination', inline=True, payload=payload))
                    message = 'Если вы хотите посмотреть проекты из других категорий нажмите кнопку Отмена'
                    self.response_data['messages'].append(self.create_message(message=message, keyboard_type='back', inline=False, payload=0))
                else:
                    message = "В этой категории больше нету проектов"
                    self.response_data['messages'].append(self.create_message(message=message, keyboard_type='back', inline=False, payload=0))

            # Возврат к списку категорий
            if self.user_text == 'Отмена' or self.user_text == 'Выбрать другую категорию':
                message = "О каком или каких проектах вы хотели бы узнать?"
                self.response_data['messages'].append(self.create_message(message=message, keyboard_type='projects'))

            # Пожертвования
            if self.user_text == 'Пожертвовать':
                message = 'Какую сумму вы хотели бы внести? \n Выберите или введите вручную'
                project = Database.get_project(project_id=project_id)
                self.response_data['messages'].append(self.create_message(message=message, keyboard_type='payment', inline=False, payload=project))

        else:
            # Здесь обрабатываются сообщения, введенные пользователем, или кнопки без payload

            # Если рабочий стек пустой то мы находимся в ветке оплаты
            if len(self.response_data['stack']) == 0:
                # проверяем что в предыдущем сообщении было введено слово пожертвовать
                if self.check_history(search='пожертвовать', key='ACTION', add_key=None, limit=5):
                    # Если правда то получаем введенную пользователем сумму
                    error = False
                    price = 0
                    for word in self.parsed_text:
                        try:
                            price = float(word)
                            error = False
                            break
                        except ValueError:
                            error = True

                    if error:
                        # Если возникла ошибка то выводим ошибочное сообщение
                        self.check_history(search='', key='', add_key=None, limit=20)
                        self.response_data['messages'].append(self.create_message(message=self.error_message, keyboard_type='end', keyboard=self.previous_messages[-1]['keyboard']))
                    else:
                        # Если ошибки нету то при вызове проверки истории у нас появится клавиатура последнего сообщения
                        # Получаем оттуда искомый проект
                        # Создаем ссылку для оплаты
                        message = 'Для оплаты перейдите по ссылке'
                        project_id = json.loads(self.previous_messages[0]['keyboard'][-2]['payload']).get('project')
                        project = Database.get_project(project_id=project_id)
                        payment_link = config.PAYMENT_LINK.format(
                            amount=price,
                            project_id=project_id,
                            user_id=self.user_id
                        )
                        goal_price = float(project.goal_price.split('р')[0].replace(' ', ''))
                        current_price = float(project.current_price.split('р')[0].replace(' ', ''))

                        if current_price + price >= goal_price:
                            Database.update_project(project_id=project_id, price=0, current_price=goal_price, available=0)
                        else:
                            Database.update_project(project_id=project_id, price = goal_price-(current_price+price), current_price=current_price+price)

                        self.response_data['messages'].append(self.create_message(message=message, keyboard_type='paylink', inline=True, payload=payment_link))
                        user = Database.get_or_create_user(self.user_id)
                        # Если пользователь отказался от уведомлений то предлагаем ему их включить
                        if not user.can_send_reminds:
                            message = 'Если вы хотите получать уведомления то нажмите кнопку'
                            self.response_data['messages'].append(self.create_message(message=message, keyboard_type='activate_remind', inline=True))
                        self.response_data['messages'].append(self.create_message(message='Спасибо за ваше пожертвование!', keyboard_type='start', payload='0'))
                        Database.update_user(self.user_id, last_time_donation=datetime.datetime.now(), last_project=-1)

                else:
                    # Выводим сообщение об ошибке если слова пожертвовать не было с последней активной клавиатурой
                    self.check_history(search='', key='', add_key=None, limit=20)
                    self.response_data['messages'].append(self.create_message(message=self.error_message, keyboard_type='end', keyboard=self.previous_messages[-1]['keyboard']))

            else:
                # Если рабочий стек не пустой то мы по ключу можем определить смысловое значение слова или слов
                prev_key = None
                for key, item in self.response_data['stack'].items():

                    # Если пользователь сказал слова благодарности
                    if key == 'GRATITUDE':
                        self.response_data['messages'].append(self.create_message(message='Всегда рад помочь', keyboard_type='end', inline=False))

                    # Если пользователь закончил общение
                    if key == 'END':
                        Database.update_user(self.user_id, is_active=0)
                        user = Database.get_or_create_user(self.user_id)
                        print(user.__dict__.get('__data__'))
                        print(user.is_active)
                        self.response_data['messages'].append(self.create_message(message='Всего доброго', keyboard_type='begin', inline=False))

                    # Если пользователь начал разговор ( Нажал кнопку начать )
                    if key == 'START':
                        message = 'Чем я могу вам помочь?'
                        self.response_data['messages'].append(self.create_message(message='Здравствуйте'))
                        self.response_data['messages'].append(self.create_message(message=message, keyboard_type='start'))

                    # Если пользователь поздоровался
                    if key == 'WELCOME':
                        self.response_data['messages'].append(self.create_message(message=item))

                    # Если пользователь хочет узнать информацию
                    if key == 'INFO' and prev_key == 'ACTION':
                        if self.response_data['stack'].get('PROJECTS') is None:
                            message = "О каком или каких проектах вы хотели бы узнать?"
                            self.response_data['messages'].append(self.create_message(message=message, keyboard_type='projects'))

                    # Если пользователь интересуется проектом или проектами из категории
                    if key == 'PROJECTS':
                        if self.response_data['projects'] is None:
                            self.response_data['messages'].append(self.create_message(message=self.error_message))
                        else:
                            message = f'По вашему запросу найдено проектов: {len(self.response_data["projects"])}\n'
                            category = self.response_data['projects'][0].category.category_id
                            Database.update_user(self.user_id, last_category=category)
                            print(f'carousel = {self.user_can_read_carousel}')
                            if self.user_can_read_carousel:
                                carousel = Bot.create_template(type='carousel', data=self.response_data['projects'])
                                self.response_data['messages'].append(self.create_message(message=message, carousel=carousel))
                            else:
                                self.response_data['messages'].append(self.create_message(message=message))
                                for project in self.response_data["projects"]:
                                    self.response_data['messages'].append(self.create_message(message=project.get_project_info(), keyboard_type='project', inline=True, payload=project))
                            payload = {
                                'category': category,
                                'page': 0
                            }
                            self.response_data['messages'].append(self.create_message(message='Страница 1', keyboard_type='pagination', inline=True, payload=payload))
                            message = 'Если вы хотите посмотреть проекты из других категорий нажмите кнопку Отмена'
                            self.response_data['messages'].append(self.create_message(message=message, keyboard_type='back', inline=False, payload=0))

                    prev_key = key

                # Обработка исключений
                if len(self.response_data['messages']) <= 1:
                    if prev_key == 'WELCOME':
                        message = 'Чем я могу вам помочь?'
                        self.response_data['messages'].append(self.create_message(message=message, keyboard_type='start'))
                    elif prev_key == 'ACTION':
                        self.check_history(search='', key='', add_key=None, limit=20)
                        self.response_data['messages'].append(self.create_message(message=self.error_message, keyboard_type='end', keyboard=self.previous_messages[-1]['keyboard']))

    @staticmethod
    def create_template(type, data=None):
        if type == 'carousel':
            carousel = []
            for project in data:
                carousel_element = ApiMethodsClass.create_carusel_element(
                    title='title',
                    description=project.short_desc,
                    project_link=project.url,
                    photo_id=f'-198392433_457239229',
                    # Тестовая фотография пока нету реальных того же размера загружена с http://placehold.it/221x136
                    payload={'project': project.offer_id}
                )
                carousel.append(carousel_element)
            return carousel
    @staticmethod
    def create_message(message, keyboard_type=None, inline=False, payload=None, keyboard=None, attachment=None, carousel=None):
        """
        Создает сообщения
        :param message: текстовое сообщение
        :param keyboard_type: тип клавиатуры
        :param inline: в сообщении или нет
        :param payload: доп информация
        :param keyboard: клавиатура(Если есть)
        :param attachment: дополнения
        :return:
        """

        return {
            'message' : message,
            'keyboard': Bot.create_keyboard(type=keyboard_type, payload=payload) if keyboard is None else keyboard,
            'inline': inline,
            'carousel': carousel,
            'attachment': attachment
        }

    @staticmethod
    def create_keyboard(type, payload):
        """
        Создает клавиатуру в соответствии с типом
        :param type: тип клавиатуры
        :param payload: доп информация
        :return:
        """
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
            keyboard.append(Bot.create_button(type='text', label='50'))
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
        """
        Создает кнопку
        :param type:
        :param label:
        :param payload:
        :param link:
        :param color:
        :return:
        """

        button = {
            'type': type,
            'label': label,
            'payload': payload,
            'link': link,
            "color": color
        }

        return button

    def check_history(self, search, key, add_key=None, message_num=0, limit=10, in_one=False):
        """
        Проверякт историю введенных сообщений пользователем
        :param search: слово для поиска
        :param key: ключевая область dataset для поиска
        :param add_key: дополнительная область для поиска связки
        :param message_num: какое сообщение нужно по счету( 0 - первое с конца , 1 - второе и тд)
        :param limit: Максимальное количество предыдущих сообщений для поиска
        :param in_one:
        :return: True если сообщение удовлетворяет критериям поиска, False в противном случае
        """
        index = 1
        message_index = message_num
        logs_data = Database.get_logs(self.user_id, limit=limit)
        if len(logs_data) != 0:
            while index != limit:
                history_data = json.loads(logs_data[index-1].log)
                if history_data['error_message'] == '':
                    self.previous_messages = history_data['messages']
                    action_type = history_data['stack'].get(key)
                    if action_type is not None and action_type.lower() == search.lower():
                        if add_key is None and message_index == 0:
                            return True if len(history_data['stack']) == 1 else False
                        elif history_data['stack'].get(add_key) is not None and message_index == 0:
                            return True
                        elif message_index != 0:
                            message_index -= 1
                    elif search == '' and message_index == 0:
                        return True
                    else:
                        message_index -= 1
                        index += 1
                else:
                    index += 1

        return False

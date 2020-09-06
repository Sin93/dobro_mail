from ApiMethods import ApiMethodsClass
import json

"""где-то должно храниться что мы отправили пользователю, то-есть
в каком состоянии сейчас находится диалог, возможно стоит использовать базу данных,
в базе хранить пользователя (user_id) и состояние"""

class Bot():
    def __init__(self, user_id, user_message, information):
        self.user_id = user_id
        self.user_message = user_message
        # information - дополнительная информация, которая может быть привязана
        # к кнопке (поле 'payload', см. метод create_new_keyboard в этом классе),
        # например так можно передавать id проекта
        self.information = information

        self.bot_answer = self.create_bot_answer()
        self.new_keyboard = self.create_new_keyboard()

        send_msg = ApiMethodsClass.send_msg_and_keyboard(
            user_id=self.user_id,
            message=self.bot_answer,
            keyboard=self.new_keyboard
        )


    def create_bot_answer(self) -> str:
        """Возвращает ответ бота в виде строки"""
        return 'Ответ бота'


    def create_new_keyboard(self):
        """сейчас я передал в метод и возвращаю из функции те данные, которые
        ждет ВК, но наверное лучше сделать, чтоб тут определялись основные
        параметры клавиатуры, которая будет добавлена к сообщению, а сам словарь
        и json, который ждёт вк, создавались в ApiMethodsClass.create_json_keyboard,
        наверное проще всего сделать это в виде списка словарей, в которых будет:

        'type' - тип кнопки ('Text' содержит текст, если нажать на нее, то отправится текст содержащийся в label
        и 'Open Link' - ссылка, при нажатии перекинет на указанную ссылку)
        'label' - текст на кнопке
        'color' - цвет (primary — синяя, secondary — белая, negative - красная, positive - зеленая)
        'link' - ссылка на сайт для типа 'Open Link'
        'payload' - дополнительная информация, она вернётся в событии

        и как отдельный параметр передавать:
        'inline' - True - если встроить в сообщение, False - если вывести как обычную клавиатуру"""

        # ниже не образец для работы, это нужно чтоб проверить,
        # что кнопка действительно отправляется
        keyboard = {
            "one_time": False,
            "buttons": [[{
                "action": {
                    "type": "text",
                    "label": 'Просто кнопка'
                },
                "color": "positive"
            }]]
        }

        # В реальности должно формироваться что-то типа:

        # keyboard = [
        #     {
        #     'type': 'Text',
        #     'label': 'Подробнее про проект'
        #     'payload': 3119
        #     },
        #     {
        #     'type': 'Open Link',
        #     'label': 'На сайт'
        #     'link': 'https://dobro.mail.ru/projects/pomogi-uchitsya/'
        #     }
        # ]
        # inline = True# keyboard = [
        #     {
        #     'type': 'Text',
        #     'label': 'Подробнее про проект'
        #     'payload': 3119
        #     },
        #     {
        #     'type': 'Open Link',
        #     'label': 'На сайт'
        #     'link': 'https://dobro.mail.ru/projects/pomogi-uchitsya/'
        #     }
        # ]
        #
        # inline = True
        #
        # keyboard_for_send = ApiMethodsClass.create_json_keyboard(keyboard, inline)
        #
        # return keyboard_for_send

        return json.dumps(keyboard)

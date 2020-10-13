import datetime
import re
from BotLogic.DatabaseMethods.bot_methods import Database
from config import PATTERN_MAX_ERROR
from .DataSets.DataSet import DataSet


class UserText:
    """Базовый класс пользователя"""

    def __init__(self, user_id=None):
        Database.update_user(user_id, is_active=1, updated_at=datetime.datetime.now())
        self.user_text = ''
        self.parsed_text = ''
        self.user_id = user_id
        self.validate_message = ''
        self.previous_messages = None
        self.error_message = "Не понял вас. Повторите снова"

    def writeText(self, message):
        self.user_text = message

    def getText(self):
        return self.validate_message

    def __str__(self):
        return f'user {self.user_id} write: {self.user_text}'


class ValidateText(UserText):
    """
    Класс валидации текста
    """
    DELETED_SYMBOLS = ['\.', '\:', '\;', '\,', '\?', '\!']

    def __init__(self, user_id, message):
        super().__init__(user_id)
        self.writeText(message)
        self.source_id = 32
        self.stack = {}

    def remove_symbols(self):
        """
        Функция на нахождения и удаления знаков препинания в тексте
        :return:
        """
        print(f'str {"|".join(ValidateText.DELETED_SYMBOLS)}')
        reg_exp = re.compile('|'.join(ValidateText.DELETED_SYMBOLS))
        print(f'reg_exp : {reg_exp}')
        print(f'find_expresions {reg_exp.findall(self.user_text)}')
        self.user_text = re.sub(pattern="|".join(ValidateText.DELETED_SYMBOLS), repl='', string=self.user_text)

    def proceed_validation(self):
        """
        функция для запуска вылидации введенного сообщения
        :return:
        """
        self.remove_symbols()
        self.parsed_text = self.user_text.split(' ')
        for word in self.parsed_text:
            if len(word) > 3:
                for key, item in DataSet.items():
                    info = ' '.join(item)
                    if self.word_validation(word=word, validation_text=info, type=key):
                        if self.stack.get(key) is None:
                            self.stack[key] = self.validate_message
                        else:
                            self.stack[key] += f' {self.validate_message}'
                        break
        print(f'stack: {self.stack}')

    def word_validation(self, word, validation_text, type=None):
        """
        Функция валидации слова
        :param word:
        :param validation_text:
        :param type:
        :return:
        """

        regExp = re.compile(f'{word}', flags=re.I + re.M)

        if regExp.search(validation_text):
            self.validate_message = word
            return True
        else:
            # Maybe mistake in writing
            validated_text = self.mistake_validation(validation_text=validation_text, regExp=regExp)
            if validated_text is None:
                return False
            else:
                self.validate_message = validated_text
                return True

    def mistake_validation(self, validation_text, regExp, first=True):
        """
        Функция проверки слова на возможные ошибки
        :param validation_text:
        :param regExp:
        :param first:
        :return:
        """

        # Можно добавить реализацию с делением не нацело чтобы увеличить количество общих паттернов

        # Если это первое обращение к функции
        if first:
            pattern_len = len(regExp.pattern)
            # Рекурсивно проверяем слово
            left_pattern = self.mistake_validation(validation_text=validation_text, regExp=re.compile(regExp.pattern[:pattern_len // 2]), first=False)
            right_pattern = self.mistake_validation(validation_text=validation_text, regExp=re.compile(regExp.pattern[pattern_len // 2:]), first=False)
            pattern = left_pattern + right_pattern

            # Если получившийся паттерн удовлетворяет условию
            if ValidateText.check_pattern(pattern):
                # Ищем слово в эталонном тексте
                regExp = re.compile(f'{pattern}', flags=re.I + re.M)

                final_text = regExp.findall(validation_text)

                # Обработка возможных исключений
                if len(final_text) > 1 or (len(final_text) == 1 and len(final_text[0].split(' '))) > 1:
                    for variant in final_text:
                        for var in variant.split(' '):
                            if regExp.match(var):
                                return var
                # Возвращаем получившееся слово
                return final_text[0] if len(final_text) > 0 else None

            else:
                return None

        # Генерация конечного паттерна для поиска
        match = regExp.findall(validation_text)
        if match:
            return regExp.pattern

        else:
            pattern_len = len(regExp.pattern)
            if pattern_len == 1:
                return regExp.pattern

            if pattern_len == 2:
                return '\w+'

            left_pattern = self.mistake_validation(validation_text=validation_text, regExp=re.compile(regExp.pattern[:pattern_len // 2]), first=False)
            right_pattern = self.mistake_validation(validation_text=validation_text, regExp=re.compile(regExp.pattern[pattern_len // 2:]), first=False)

            return left_pattern + right_pattern

    @staticmethod
    def check_pattern(pattern):
        """
        Функция проверки паттерна
        :param pattern:
        :return:
        """
        count = 0
        for char in pattern:
            if char == '+': # \\w+
                count += 3
        if count / len(pattern) >= PATTERN_MAX_ERROR:
            return False

        return True

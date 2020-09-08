import re
import datetime
from XML import XML
import bot_config


class UserText:

    def __init__(self, user_id = None):
        self.user_text = ''
        self.user_id = user_id
        self.validate_message = ''
        self.error_message = ''
        self.last_message_time = datetime.datetime.now()

    def writeText(self, message):
        self.user_text = message

    def getText(self):
        return self.validate_message

    def __str__(self):
        return f'user {self.user_id} write: {self.user_text}'


class ValidateText(UserText):
    validationText = 'Дети Взрослые Пожилые Природа Другое'

    possibleSource = {
        'Дети': 1,
        'Взрослые': 2,
        'Пожилые': 3,
        'Животные': 4,
        'Природа': 5,
        'Другое': 32
    }
        # 'Отмена' , 'Далее', 'Назад'

    def __init__(self, user_id, message):
        super().__init__(user_id)
        self.writeText(message)
        self.source_id = 32
        self.proceed_validation()

    def proceed_validation(self):

        regExp = re.compile(f'{self.user_text}', flags=re.I + re.M)

        if regExp.search(self.validationText):
            print("Success")
            print(f'Possible source id: {self.possibleSource[self.user_text.title()]}  {self.user_text.title()}')
            self.validate_message = self.user_text.title()
        else:
            # Maybe mistake in writing
            print(regExp)
            validated_text = self.mistake_validation(self.validationText, regExp)
            print(validated_text)
            if validated_text is None:
                self.error_message = "Не понял вас. Повторите снова"
                print('Не понял вас. Повторите снова')
            else:
                print(f'Possible source id: {self.possibleSource[validated_text]}  {validated_text}')
                self.validate_message = validated_text

        self.source_id = self.possibleSource[self.validate_message]

    def mistake_validation(self, validation_text, regExp, first=True):
        # Можно добавить реализацию с делением не нацело чтобы увеличить количество общих паттернов
        if first:
            pattern_len = len(regExp.pattern)
            left_pattern = self.mistake_validation(validation_text, re.compile(regExp.pattern[:pattern_len // 2]), False)
            right_pattern = self.mistake_validation(validation_text, re.compile(regExp.pattern[pattern_len // 2:]), False)

            pattern = left_pattern + right_pattern
            regExp = re.compile(f'{pattern}', flags=re.I + re.M)

            final_text = regExp.findall(validation_text)

            if len(final_text) > 1 or len(final_text) == 1 and len(final_text[0].split(' ')) > 1:
                for variant in final_text:
                    for var in variant.split(' '):
                        if regExp.match(var):
                            return var

            return final_text[0] if len(final_text) > 0 else None

        match = regExp.findall(validation_text)
        print(regExp.pattern)
        if match:
            return regExp.pattern

        else:
            pattern_len = len(regExp.pattern)
            if pattern_len == 1:
                return regExp.pattern

            if pattern_len == 2:
                return '.+'

            left_pattern = self.mistake_validation(validation_text, re.compile(regExp.pattern[:pattern_len // 2]), False)
            right_pattern =self.mistake_validation(validation_text, re.compile(regExp.pattern[pattern_len // 2:]), False)

            return left_pattern + right_pattern


class BotResponse(ValidateText, XML):

    def __init__(self, user_id, user_message, information, xml_url = None):
        ValidateText.__init__(self, user_id, user_message)
        XML.__init__(self, xml_url)
        self.response_data = None

    def generate_response(self):

        if self.error_message == '':
            self.get_projects(self.source_id, bot_config.PROJECTS_AMOUNT)
            self.response_data = [f'Даю по вашему запросу {len(self.projects)} проектов\n', self.projects]


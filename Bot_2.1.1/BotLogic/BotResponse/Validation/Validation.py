import re
import datetime
from config import PATTERN_MAX_ERROR
from .DataSets.DataSet import DataSet


class UserText:

    def __init__(self, user_id = None):
        self.user_text = ''
        self.user_id = user_id
        self.validate_message = ''
        self.error_message = "Не понял вас. Повторите снова"
        self.last_message_time = datetime.datetime.now()

    def writeText(self, message):
        self.user_text = message

    def getText(self):
        return self.validate_message

    def __str__(self):
        return f'user {self.user_id} write: {self.user_text}'


class ValidateText(UserText):

    def __init__(self, user_id, message):
        super().__init__(user_id)
        self.writeText(message)
        self.source_id = 32
        self.stack = {}
        self.proceed_validation()

    def proceed_validation(self):
        print(self.user_text)
        self.user_text = self.user_text.split(' ')
        for word in self.user_text:
            if len(word) > 3:
                for key, item in DataSet.items():
                   # print(key)
                    info = ' '.join(item)
                    print(info)
                    if self.word_validation(word, info, key):
                        if self.stack.get(key) is None:
                            self.stack[key] = self.validate_message
                        else:
                            self.stack[key] += f' {self.validate_message}'
                        break
        print(self.stack)

        # regExp = re.compile(f'{self.user_text}', flags=re.I + re.M)

        # if regExp.search(self.validationText):
        #     print("Success")
        #     print(f'Possible source id: {self.possibleSource[self.user_text.title()]}  {self.user_text.title()}')
        #     self.validate_message = self.user_text.title()
        # else:
        #     # Maybe mistake in writing
        #     print(regExp)
        #     validated_text = self.mistake_validation(self.validationText, regExp)
        #     print(validated_text)
        #     if validated_text is None:
        #         self.error_message = "Не понял вас. Повторите снова"
        #         self.validate_message = 'Другое'
        #         print('Не понял вас. Повторите снова')
        #     else:
        #         print(f'Possible source id: {self.possibleSource[validated_text]}  {validated_text}')
        #         self.validate_message = validated_text

        # self.source_id = self.possibleSource[self.validate_message]

    def word_validation(self, word, validation_text, type=None):

        regExp = re.compile(f'{word}', flags=re.I + re.M)

        if regExp.search(validation_text):
            print(f"Success {word} key = {type}")
            # print(f'Possible source id: {self.possibleSource[self.user_text.title()]}  {self.user_text.title()}')
            # self.validate_message = self.user_text.title()
            self.validate_message = word
            return True
        else:
            # Maybe mistake in writing
            #print(regExp)
            validated_text = self.mistake_validation(validation_text, regExp)
            #print(validated_text)
            if validated_text is None:
                # self.error_message = "Не понял вас. Повторите снова"
                # self.validate_message = 'Другое'
                #print(f'Не понял вас. Повторите снова key = {type}')
                return False
            else:
                # print(f'Possible source id: {self.possibleSource[validated_text]}  {validated_text}')
                # self.validate_message = validated_text
                print(f'{validated_text} key = {type}' )
                self.validate_message = validated_text
                return True

    def mistake_validation(self, validation_text, regExp, first=True):
        # Можно добавить реализацию с делением не нацело чтобы увеличить количество общих паттернов
        if first:
            pattern_len = len(regExp.pattern)
            left_pattern = self.mistake_validation(validation_text, re.compile(regExp.pattern[:pattern_len // 2]), False)
            right_pattern = self.mistake_validation(validation_text, re.compile(regExp.pattern[pattern_len // 2:]), False)
            pattern = left_pattern + right_pattern

            if self.check_pattern(pattern):
                regExp = re.compile(f'{pattern}', flags=re.I + re.M)

                final_text = regExp.findall(validation_text)

                if len(final_text) > 1 or len(final_text) == 1 and len(final_text[0].split(' ')) > 1:
                    for variant in final_text:
                        for var in variant.split(' '):
                            if regExp.match(var):
                                return var

                return final_text[0] if len(final_text) > 0 else None

            else:
                return None

        match = regExp.findall(validation_text)
        #print(regExp.pattern)
        if match:
            return regExp.pattern

        else:
            pattern_len = len(regExp.pattern)
            if pattern_len == 1:
                return regExp.pattern

            if pattern_len == 2:
                return '\w+'

            left_pattern = self.mistake_validation(validation_text, re.compile(regExp.pattern[:pattern_len // 2]), False)
            right_pattern =self.mistake_validation(validation_text, re.compile(regExp.pattern[pattern_len // 2:]), False)

            return left_pattern + right_pattern

    def check_pattern(self, pattern):
        count = 0
        for char in pattern:
            if char == '+': # \\w+
                count += 3
        #print(pattern, len(pattern), count / len(pattern))
        #print(count/ len(pattern))
        if count / len(pattern) >= PATTERN_MAX_ERROR:
            return False

        return True

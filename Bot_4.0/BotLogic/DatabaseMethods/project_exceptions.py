
class MissingUserError(Exception):
    def __init__(self):
        self.txt = 'Пользователь с id ... не найден'
        print('Пользователь с id ... не найден')


class EntryExistsError(Exception):
    def __init__(self):
        self.txt = 'Запись с таким id пользователя уже существует'

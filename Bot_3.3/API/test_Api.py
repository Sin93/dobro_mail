
class ApiMethodsClassTest:

    def __init__(self, user_id, message):
        self.message = message['message']
        print(f'send to {user_id} - {self.message}')
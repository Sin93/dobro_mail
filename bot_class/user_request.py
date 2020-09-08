from BotResponse import BotResponse
import bot_config


class Bot(BotResponse):

    users = []

    def __init__(self, user_id, user_message, information):
        self.current_user = None
        for user in Bot.users:
            if user.user_id == user_id:
                user.user_message = user_message
                user.proceed_validation()
                user.get_projects(user.source_id, bot_config.PROJECTS_AMOUNT)
                self.current_user = user
                break
        if self.current_user is None:
            super().__init__(user_id, user_message, information, xml_url=None)
            Bot.users.append(self)

        self.generate_response()

    def __str__(self):

        if self.response_data is None:
            answer = self.error_message
        else:
            answer = f'{self.response_data[0]}\n'
            for project in self.response_data[1]:
                answer += project.get_project_info()

        return answer



test = Bot(1, 'природа', '')
print(test)


import config
from .Validation.Validation import ValidateText
from ..DatabaseMethods.bot_methods import Database


class BotResponse(ValidateText):
    """Класс создающий ответ бота"""

    def __init__(self, user_id, user_message):
        ValidateText.__init__(self, user_id, user_message)
        self.response_data = None

    def generate_response(self):
        """
        Генерирует ответ бота
        :return:
        """
        self.response_data = {
            'projects': None,
            'stack': self.stack,
            'messages': []
        }

        project_names = self.stack.get('PROJECTS')
        print(f'Project_names: {project_names}')
        if project_names is not None:
            projects = []
            for project_name in project_names.split(' '):
                # Change to database
                category_id = Database.get_category_by_name(project_name)
                print(f'category_id = {category_id}')
                projects = Database.get_projects_by_category(category_id, config.PROJECTS_AMOUNT)

            self.response_data['projects'] = projects

    def save_info(self):
        """
        Сохраняет информацию сообщения
        :return:
        """
        log_data = {
            'stack': self.response_data['stack'],
            'user_text': self.user_text,
            'messages': self.response_data['messages'],
            'error_message': self.error_message if self.response_data['messages'][0]['message'] == self.error_message else '',
            'projects': []
        }

        if self.response_data['projects'] is not None:
            for project in self.response_data['projects']:
                log_data['projects'].append(project.offer_id)

        Database.save_log(log_data, self.user_id)


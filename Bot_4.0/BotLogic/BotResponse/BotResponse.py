import datetime
import json
import config
from .Validation.Validation import ValidateText
from .Validation.DataSets.DataSet import possibleProjectSource
from ..DatabaseMethods.bot_methods import Database


class BotResponse(ValidateText):

    def __init__(self, user_id, user_message):
        ValidateText.__init__(self, user_id, user_message)
        self.response_data = None

    def generate_response(self):
        self.response_data = {
            'projects': None,
            'stack': self.stack,
            'messages': []
        }

        project_names = self.stack.get('PROJECTS')
        print(project_names)
        if project_names is not None:
            projects = []
            for project_name in project_names.split(' '):
                # Change to database
                category_id = Database.get_category_by_name(project_name)
                projects = Database.get_projects_by_category(category_id, config.PROJECTS_AMOUNT)

            self.response_data['projects'] = projects

    def save_info(self):
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

        with open(config.LOG_DIR + f'{self.user_id}.txt', 'a', encoding='utf-8') as logs:
            logs.write(json.dumps(log_data))
            logs.write('\n')


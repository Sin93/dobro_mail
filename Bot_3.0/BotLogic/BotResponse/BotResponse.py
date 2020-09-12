import datetime
import json

from BotLogic.BotResponse.XML.XML import XML
import config
from .Validation.Validation import ValidateText
from .Validation.DataSets.DataSet import possibleProjectSource


class BotResponse(ValidateText, XML):

    def __init__(self, user_id, user_message, xml_url = None):
        ValidateText.__init__(self, user_id, user_message)
        XML.__init__(self, xml_url)
        self.response_data = None
        self.generate_response()

    def generate_response(self):
        self.response_data = {
            'projects': None,
            'stack': self.stack,
            'messages': []
        }

        project_names = self.stack.get('PROJECTS')
        print(project_names)
        if project_names is not None:
            for project_name in project_names.split(' '):
                self.get_projects(possibleProjectSource.get(project_name.lower()), config.PROJECTS_AMOUNT)

            self.response_data['projects'] = self.projects

        #self.response_data = [f'Даю по вашему запросу {len(self.projects)} проектов\n', self.projects]

    def save_info(self):
        log_data = {
            'stack': self.response_data['stack'],
            'user_text': self.user_text,
            'error_message': self.error_message if self.response_data['messages'][0]['message'] == self.error_message else '',
            'projects': [],
            'time': datetime.datetime.now().strftime("%H:%M:%S")
        }

        if self.response_data['projects'] is not None:
            for project in self.response_data['projects']:
                log_data['projects'].append(project.offer_id)

        with open(config.LOG_DIR + f'{self.user_id}.txt', 'a', encoding='utf-8') as logs:
            logs.write(json.dumps(log_data))
            logs.write('\n')


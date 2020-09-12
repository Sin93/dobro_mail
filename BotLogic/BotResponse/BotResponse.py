from BotLogic.BotResponse.XML.XML import XML
import config
from .Validation.Validation import ValidateText
from .Validation.DataSets.DataSet import possibleProjectSource


class BotResponse(ValidateText, XML):

    def __init__(self, user_id, user_message, information, xml_url = None):
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


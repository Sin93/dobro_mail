import requests
from bs4 import BeautifulSoup
from .ProjectClasses.Projects import Project
import config


class XML:

    def __init__(self, xml_url=None):
        self.xml_data = ''
        self.xml_url = xml_url
        self.projects = []
        self.get_xml_data()

    def get_xml_data(self):
        if self.xml_url is None:
            self.xml_data = requests.get(config.PROJECTS_DATA).text
        else:
            self.xml_data = requests.get(self.xml_url).text

    def get_projects(self, project_id, amount):
        projects = BeautifulSoup(self.xml_data, 'lxml').find_all('offer')

        for project in projects:
            if project['available'] and project_id == int(project.categoryid.text):
                self.projects.append(Project(project))
                if amount != 0:
                    amount -= 1
                else:
                    break

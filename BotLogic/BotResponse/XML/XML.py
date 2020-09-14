import requests
from bs4 import BeautifulSoup
from .ProjectClasses.Projects import Project, UPLOAD_PROJECTS
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
                print(amount)
                if amount > 1:
                    amount -= 1
                else:
                    break


class HTML:
    def __init__(self, offer_id):
        if UPLOAD_PROJECTS.get(offer_id).full_desc == '':
            self.offer_id = offer_id
            self.url = UPLOAD_PROJECTS.get(offer_id).url
            self.get_html_data()

    def get_html_data(self):
        html = requests.get(self.url).text
        soup = BeautifulSoup(html, 'html')
        current = soup.find(class_="p-money__money").text
        goal = soup.find(class_="p-money__money_goal").text
        info = soup.find(class_='p-project__lead').text
        project = UPLOAD_PROJECTS[self.offer_id]
        project.full_desc = info
        project.goal_price = goal
        project.current_price = current

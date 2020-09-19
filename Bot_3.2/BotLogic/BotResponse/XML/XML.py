import requests
from bs4 import BeautifulSoup
import config


class XML:

    def __init__(self, xml_url=None):
        self.xml_data = ''
        self.xml_url = xml_url
        self.projects = []
        self.get_xml_data()

    def get_xml_data(self):
        if self.xml_url is None:
            self.xml_data = BeautifulSoup(requests.get(config.PROJECTS_DATA).text, 'lxml')
        else:
            self.xml_data = BeautifulSoup(requests.get(self.xml_url).text, 'lxml')

    def get_project(self, project_id):
        return self.xml_data.find('offer', id=f'{project_id}')

    def get_category(self, category_id):
        return self.xml_data.find('category', id=f'{category_id}')

    def get_all_projects(self):
        return self.xml_data.find_all('offer')


class HTML:
    def __init__(self, html_url=None):
        self.html_data = ''
        self.url = html_url
        self.get_html_data()

    def get_html_data(self):
        if self.url is not None:
            html = requests.get(self.url).text
            self.html_data = BeautifulSoup(html, 'lxml')

    def get_current_price(self):
        try:
            current = self.html_data.find(class_="p-money__money").text
            return current
        except Exception:
            return '0 р'

    def get_goal_price(self):
        try:
            goal = self.html_data.find(class_="p-money__money_goal").text
            return goal
        except Exception:
            return '0 р'

    def get_full_description(self):
        try:
            info = self.html_data.find(class_='p-project__lead').text
            return info
        except Exception:
            return ''

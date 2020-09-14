from models import Projects
from bs4 import BeautifulSoup


def get_projects_data():
    with open('projects.xml', 'r') as file:
        data = file.read()
        projects = BeautifulSoup(data, 'lxml')
        projects_list = projects.find_all('offer')
        for project in projects_list:
            project_id = project['id']
            name = project.typeprefix.text
            available = project['available']
            url = project.url.text
            category = project.categoryid.text
            vendor = project.vendor.text
            short_name = project.model.text

            Projects(
                project_id=project_id,
                name=name,
                available=available,
                url=url,
                category=category,
                vendor=vendor,
                short_name=short_name
            ).save()

if __name__ == '__main__':
    get_projects_data()

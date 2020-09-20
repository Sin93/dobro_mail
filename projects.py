from bs4 import BeautifulSoup
from config import PROJECTS_DATA


import requests


def get_xml_data():
    return requests.get(PROJECTS_DATA).text


def write_projects_in_file(xml_data):
    with open('projects.xml', 'w') as file:
        file.write(xml_data)


def save_pictures(project_id, image_link):
    img = requests.get(image_link)
    if image_link.endswith('jpg'):
        image_name = f'images/{project_id}.jpg'
    elif image_link.endswith('png'):
        image_name = f'images/{project_id}.png'
    with open(image_name, 'wb') as image:
        image.write(img.content)


def get_projects_data():
    with open('projects.xml', 'r') as file:
        data = file.read()
        projects = BeautifulSoup(data, 'lxml')
        projects_list = projects.find_all('offer')
        for project in projects_list:
            save_pictures(project['id'], project.picture.text)


if __name__ == '__main__':
    get_projects_data()

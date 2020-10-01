import json
from BotLogic.BotResponse.XML.XML import XML, HTML
import config
from BotLogic.DatabaseMethods.models import Categories, Projects, History, ImageInfo, User
from BotLogic.BotResponse.Validation.DataSets.DataSet import DataSet
from PIL import Image


class Database:
    """
    Основной класс для работы с БД
    """

    @staticmethod
    def get_or_create_user(user_id):
        user = User.get_user_by_id(user_id=user_id)
        if user is None:
            user = User.create_user(user_id=user_id)
        return user

    @staticmethod
    def get_all_users():
        return User.select()

    @staticmethod
    def update_user(user_id, **kwargs):
        user = Database.get_or_create_user(user_id=user_id)
        user_data = user.__dict__.get('__data__')
        for key, item in kwargs.items():
            user_data.update({f'{key}': item})
        user.save()
        return user

    @staticmethod
    def create_project(project_id, xml_project=None, project_category=None):

        if xml_project is None:
            xml = XML(config.XML_URL)
            project = xml.get_project(project_id)
            category = xml.get_category(project.categoryid.text)
        else:
            category = project_category
            project = xml_project

        if Categories.get_category(int(project.categoryid.text)) is None:
            if category is None:
                xml = XML(config.XML_URL)
                category = xml.get_category(project.categoryid.text)
            Categories.create_category(category_id=int(project.categoryid.text), category_name=category.text)
            DataSet["PROJECTS"] = Database.get_all_category_names()

        html = HTML(project.url.text)
        project_data = {
            'offer_id': project['id'],
            'category': int(project.categoryid.text),
            'url': project.url.text,
            'price': float(project.price.text),
            'currency': project.currencyid.text,
            'picture': ImageInfo.create_img(project.picture.text),
            'available': 1 if project['available'] == 'true' else 0,
            'short_desc': project.typeprefix.text,
            'full_desc': html.get_full_description(),
            'goal_price': html.get_goal_price(),
            'current_price': html.get_current_price(),
            'city': html.get_city(),
            'model': project.model.text,
        }

        return Projects.create_project(project_data)

    @staticmethod
    def update_project_with_xml(xml_project, project_category=None, **kwargs):
        project = Database.get_project(int(xml_project['id']))
        if project is None:
            Database.create_project(project_id=int(xml_project['id']), xml_project=xml_project, project_category=project_category)
        else:
            price = xml_project.price.text
            available = 1 if xml_project['available'] == 'true' else 0
            goal_price = float(project.goal_price.split('р')[0].replace(' ', ''))
            current_price = goal_price - float(price)
            kwargs.update({'price': float(price), 'current_price': f'{current_price } р', 'available': available})
            Database.update_project(project=project, **kwargs)

    @staticmethod
    def update_project(project_id=None, project=None, **kwargs):
        if project is None:
            project = Database.get_project(project_id)

        project_data = project.__dict__.get('__data__')
        for key, item in kwargs.items():
            project_data.update({f'{key}': item})
        project.save()

    @staticmethod
    def update_all_projects(**kwargs):
        xml = XML(xml_url=config.XML_URL)
        xml_projects = xml.get_all_projects()
        for xml_project in xml_projects:
            category = xml.get_category(xml_project.categoryid.text)
            Database.update_project_with_xml(xml_project=xml_project, project_category=category, **kwargs)

    @staticmethod
    def delete_projects_with_xml():
        xml = XML(xml_url=config.XML_URL)
        projects = Projects.select()
        for project in projects:
            xml_project = xml.get_project(project_id=project.offer_id)
            if xml_project is None:
                Database.delete_project(project_id=project.offer_id, database_project=project)

    @staticmethod
    def delete_project(project_id, database_project=None):
        if database_project is None:
            project = Database.get_project(project_id)
        else:
            project = database_project

        if project is not None:
            project.available = 0
        project.save()

    @staticmethod
    def get_project(project_id):
        return Projects.get_projects_by_id(project_id)

    @staticmethod
    def get_or_create_project(project_id):
        project = Projects.get_projects_by_id(project_id)
        if project is None:
            return Database.create_project(project_id)
        else:
            return project

    @staticmethod
    def get_projects_by_category(category_id, amount=None, page=0):
        if amount is None:
            projects = Projects.select().where(Projects.category == category_id, Projects.available == 1)
        else:
            projects = Projects.select().where(Projects.category == category_id, Projects.available == 1).limit(amount).offset(int(page)*amount)

        return projects

    @staticmethod
    def create_category(category_id):
        xml = XML(xml_url=config.XML_URL)
        category = xml.get_category(category_id)
        Categories.create_category(category_id=category_id, category_name=category.text)
        DataSet['PROJECTS'] = Database.get_all_category_names()

    @staticmethod
    def get_category_by_name(category_name):
        try:
            print(f'category_name= {category_name}')
            category = Categories.get(name=category_name.title())
            return category.category_id
        except Exception:
            categories = Categories.select()
            for category in categories:
                if category.additional_names != '':
                    add_names = category.additional_names.split(',')[:-1]
                    for add_name in add_names:
                        if add_name.lower() == category_name.lower():
                            return category.category_id
            return -1

    @staticmethod
    def get_all_categories():
        return Categories.select()

    @staticmethod
    def update_category(category_id, **kwargs):
        category = Categories.get_category(category_id)
        category_data = category.__dict__.get('__data__')
        for key, item in kwargs.items():
            category_data.update({f'{key}': item})
        category.save()
        DataSet['PROJECTS'] = Database.get_all_category_names()

    @staticmethod
    def save_log(log_data, user_id):

        log = {
            'user_id': user_id,
            'log': json.dumps(log_data)
        }
        History.create_log(log)

    @staticmethod
    def get_logs(user_id, limit):
        data = History.select().where(History.user_id == user_id).order_by(-History.id).limit(limit)
        return data

    @staticmethod
    def get_all_category_names():
        names = []
        categories = Categories.select()
        for category in categories:
            additional = []
            if category.additional_names != '':
                additional = category.additional_names.split(',')[:-1]
            additional.append(category.name)
            names += additional

        return names

    @staticmethod
    def resize_img(img_id, new_size, database_project=None, img_url=None):
        if database_project is None:
            project = Projects.get(picture=img_id)
        else:
            project = database_project
        if img_url is None:
            xml = XML(xml_url=config.XML_URL)
            picture_url = xml.get_project(project_id=project.offer_id).picture.text
        else:
            picture_url = img_url
        filename = ImageInfo.get_img_content(url=picture_url)

        filename = ImageInfo.resize_image(filename=filename, new_size=new_size)

        data = ImageInfo.upload_photo(img_filename=filename)
        project.picture.template_owner_id = data.get('owner_id')
        project.picture.template_media_id = data.get('media_id')
        project.picture.save()

    @staticmethod
    def resize_all_img(new_size):
        xml = XML(xml_url=config.XML_URL)
        projects = Projects.select()
        for project in projects:
            try:
                img_url = xml.get_project(project_id=project.offer_id).picture.text
                Database.resize_img(img_id=project.picture, new_size=new_size, database_project=project, img_url=img_url)
            except AttributeError:
                Database.update_project(project_id=project.offer_id, available=0)


# Обновление данных при первом запуске
DataSet['PROJECTS'] = Database.get_all_category_names()

# Database.update_all_projects()

# placehold photo -198392433_457239229
# another placeholder photo id 172

# Database.resize_all_img(new_size=(221, 136))

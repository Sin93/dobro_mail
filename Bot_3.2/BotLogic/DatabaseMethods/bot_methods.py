from BotLogic.BotResponse.XML.XML import XML, HTML
import config
from BotLogic.DatabaseMethods.models import Categories, Projects


class Database:

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
        html = HTML(project.url.text)
        project_data = {
            'offer_id': project['id'],
            'category': int(project.categoryid.text),
            'url': project.url.text,
            'price': float(project.price.text),
            'currency': project.currencyid.text,
            'picture_link': project.picture.text,
            'available': project['available'],
            'short_desc': project.typeprefix.text,
            'full_desc': html.get_full_description(),
            'goal_price': html.get_goal_price(),
            'current_price': html.get_current_price(),
            'vendor_id': int(project.vendor.text),
            'model': project.model.text,
        }

        Projects.create_project(project_data)

    @staticmethod
    def update_project_with_xml(xml_project, project_category=None, **kwargs):
        project = Database.get_project(int(xml_project['id']))
        if project is None:
            Database.create_project(project_id=int(xml_project['id']), xml_project=xml_project, project_category=project_category)
        else:
            Database.update_project(project=project, **kwargs)

    @staticmethod
    def update_project(project_id=None, project=None, **kwargs):
        if project is None:
            project = Database.get_project(project_id)

        project_data = project.__dict__.get('__data__')
        for key, item in kwargs.items():
            project_data.update({f'{key}': f'{item}'})
        project.save()

    @staticmethod
    def update_all_projects(**kwargs):
        xml = XML(xml_url=config.XML_URL)
        xml_projects = xml.get_all_projects()
        for xml_project in xml_projects:
            category = xml.get_category(xml_project.categoryid.text)
            Database.update_project_with_xml(xml_project=xml_project, project_category=category, **kwargs)

    @staticmethod
    def delete_project(project_id):
        project = Database.get_project(project_id)
        if project is not None:
            project.available = False
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
    def get_projects_by_category(category_id, amount=None):
        if amount is None:
            projects = Projects.select().where(Projects.category == category_id)
        else:
            projects = Projects.select().where(Projects.category == category_id).limit(amount + 1)

        return projects

    @staticmethod
    def create_category(category_id):
        xml = XML(xml_url=config.XML_URL)
        category = xml.get_category(category_id)
        Categories.create_category(category_id=category_id, category_name=category.text)
        pass

    @staticmethod
    def update_category(category_id, **kwargs):
        category = Categories.get_category(category_id)
        category_data = category.__dict__.get('__data__')
        for key, item in kwargs.items():
            category_data.update({f'{key}': f'{item}'})
        category.save()


# Database.update_all_projects()

# projects = Projects.select()
#
# for project in projects:
#     print(project.goal_price)

UPLOAD_PROJECTS = {}
CATEGORY_PROJECTS = {}


class Project:

    def __init__(self, project_xml):
        self.offer_id = project_xml['id']
        self.category_id = project_xml.categoryid.text
        self.url = project_xml.url.text
        self.price = project_xml.price.text
        self.currency = project_xml.currencyid.text
        self.picture_link = project_xml.picture.text
        self.short_desc = project_xml.typeprefix.text
        self.full_desc = ''
        self.goal_price = 0
        self.current_price = 0
        self.image = None
        self.vendor_id = int(project_xml.vendor.text)
        self.model = project_xml.model.text
        Project.save_project(self)

    @staticmethod
    def save_project(project):
        if UPLOAD_PROJECTS.get(project.offer_id) is None:
            UPLOAD_PROJECTS[project.offer_id] = project
        else:
            UPLOAD_PROJECTS[project.offer_id] = project

        if CATEGORY_PROJECTS.get(project.category_id) is None:
            CATEGORY_PROJECTS[project.category_id] = {project.offer_id}
        else:
            CATEGORY_PROJECTS[project.category_id].add(project.offer_id)

    def get_project_info(self):

        return f'Цель - {self.short_desc}\nОсталось - {self.price} {self.currency}\nПродавец - {self.vendor_id}\n\n'

    def get_full_project_info(self):

        return f'Picture \n' \
               f' \n{self.full_desc} \n\n Нужно собрать - {self.goal_price} \n\n Собрано уже - {self.current_price} \n\n' \
               f'Более подробную информацию а так же все новости вы можете посмотреть по ссылке: \n {self.url}'

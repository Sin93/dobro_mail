
class Project:

    def __init__(self, project_xml):
        self.url = project_xml.url.text
        self.price = project_xml.price.text
        self.currency = project_xml.currencyid.text
        self.picture_link = project_xml.picture.text
        self.short_desc = project_xml.typeprefix.text
        self.vendor_id = int(project_xml.vendor.text)
        self.model = project_xml.model.text

    def get_project_info(self):

        return f'Цель - {self.short_desc}\nЦена - {self.price} {self.currency}\nПродавец - {self.vendor_id}\n\n'

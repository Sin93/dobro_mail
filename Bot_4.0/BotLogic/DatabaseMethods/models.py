import requests
from peewee import *
from datetime import datetime
from API.ApiMethods import ApiMethodsClass
from config import TOKEN, BASE_DIR
from playhouse.migrate import *

DB = SqliteDatabase('dobro.db')
migrator = SqliteMigrator(DB)


class BaseModel(Model):
    class Meta:
        database = DB


class User(BaseModel):
    id = IntegerField(primary_key=True)
    is_active = IntegerField(default=1)
    user_id = IntegerField(null=False, unique=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    last_category = IntegerField(null=True)
    last_project = IntegerField(null=True)
    last_time_donation = DateTimeField(default=datetime.now)
    can_send_reminds = BooleanField(default=True)

    @staticmethod
    def get_user_by_id(user_id):
        try:
            user = User.get(user_id = user_id)
            return user
        except Exception:
            return None


    @staticmethod
    def create_user(user_id):
        new_user = User(user_id=user_id)
        new_user.save()
        return new_user


class History(BaseModel):

    id = AutoField(primary_key=True, unique=True)
    user_id = IntegerField(unique=False)
    log = TextField()
    time = TimeField(default=datetime.now().strftime("%H:%M:%S"))

    @staticmethod
    def create_log(log):
        new_log = History.create(**log)
        new_log.save()


class Categories(BaseModel):
    id = IntegerField(primary_key=True)
    category_id = IntegerField(null=False, unique=True)
    name = CharField(max_length=100, unique=True, null=False)
    additional_names = CharField(max_length=255, null=True)

    @staticmethod
    def get_category(category_id):
        try:
            project = Categories.get(category_id=category_id)
            return project
        except Exception:
            return None

    @staticmethod
    def create_category(category_id, category_name):
        new_category = Categories(category_id=category_id, name=category_name)
        new_category.save()


class ImageInfo(BaseModel):
    id = IntegerField(primary_key=True)
    owner_id = IntegerField()
    media_id = IntegerField()

    @staticmethod
    def create_img(url):
        img = requests.get(url=url)
        img_data = img.content
        if url.endswith('jpg'):
            image_name = f'{BASE_DIR}/BotLogic/img/test.jpg'
        elif url.endswith('png'):
            image_name = f'{BASE_DIR}/BotLogic/img/test.png'
        with open(image_name, 'wb') as img:
            img.write(img_data)
        server_data = ApiMethodsClass.photoUploadServer()
        upload_url = server_data.get('upload_url')
        files = {'file': open(image_name, 'rb')}
        response = requests.post(url=upload_url, params={'access_token': TOKEN}, files=files)
        json_obj = response.json()
        photo = json_obj.get('photo')
        server = json_obj.get('server')
        hash_data = json_obj.get('hash')
        server_img_data = ApiMethodsClass.savePhoto(photo=photo, server=server, hash=hash_data)
        data = {
            'owner_id': server_img_data[0].get('owner_id'),
            'media_id': server_img_data[0].get('id')
        }
        new_img = ImageInfo.create(**data)
        new_img.save()
        return new_img.id


class Projects(BaseModel):

    id = IntegerField(primary_key=True)
    offer_id = IntegerField(null=False, unique=True)
    category = ForeignKeyField(Categories, field='category_id')
    url = CharField(max_length=255, unique=True, null=False)
    price = DecimalField(null=False)
    currency = CharField(max_length=15, null=False)
    picture = ForeignKeyField(ImageInfo, field='id')
    short_desc = TextField(null=False)
    full_desc = TextField(null=False)
    goal_price = CharField(max_length=20)
    current_price = CharField(max_length=20)
    city = CharField(max_length=50, null=True)
    model = CharField(max_length=255, null=True)
    available = IntegerField(null=False, default=1)

    def get_project_info(self):
        return f'Цель - {self.short_desc}\nОсталось - {self.price} {self.currency}\nГород - {self.city}\n\n'

    def get_full_project_info(self):
        return f'\n' \
               f' \n{self.full_desc} \n\n Нужно собрать - {self.goal_price} \n\n Собрано уже - {self.current_price} \n\n' \
               f'Более подробную информацию а так же все новости вы можете посмотреть по ссылке: {self.url} \n'

    @staticmethod
    def create_project(project_data):
        new_project = Projects(**project_data)
        new_project.save()
        return new_project

    @staticmethod
    def get_projects_by_id(project_id):
        try:
            project = Projects.get(offer_id=project_id)
            return project
        except Exception:
            return None



# DB.connect()
# # DB.drop_tables([User])
# # DB.create_tables([User])
# migrate(migrator.add_column('categories', 'additional_names', CharField(max_length=255, null=True, default='')))
# DB.close()

print(int(True))
print(int(False))
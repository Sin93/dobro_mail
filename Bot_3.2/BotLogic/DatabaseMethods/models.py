from peewee import *
from datetime import datetime

DB = SqliteDatabase('dobro.db')


class BaseModel(Model):
    class Meta:
        database = DB


class User(BaseModel):
    id = IntegerField(primary_key=True)
    vk_user_id = IntegerField(null=False, unique=True)
    chat_id = IntegerField(null=False, unique=True)
    created_at = DateTimeField(default=datetime.now)
    favorite_category = IntegerField(null=True, default=None)

    @staticmethod
    def get_user_by_id(user_id):
        user = User.get(vk_user_id = user_id)

        return user


    @staticmethod
    def create_user(user_id, chat_id):
        new_user = User(vk_user_id=user_id, chat_id=chat_id)
        new_user.save()


class History(BaseModel):
    id = AutoField(primary_key=True, unique=True)
    user_id = ForeignKeyField(User)
    datetime = DateTimeField(default=datetime.now)
    user_message = TextField(null=False)
    bot_answer = TextField(null=False)

    @staticmethod
    def add_entry(user_id, user_message, bot_answer):
        new_entry = History(user_id=user_id, user_message=user_message, bot_answer=bot_answer)
        new_entry.save()

    @staticmethod
    def get_last_user_entry(user_id):
        user_entries = History.filter(user_id=user_id).order_by(History.id.desc())
        return user_entries[0]


class Categories(BaseModel):
    id = IntegerField(primary_key=True)
    category_id = IntegerField(null=False, unique=True)
    name = CharField(max_length=100, unique=True, null=False)

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


class Projects(BaseModel):

    id = IntegerField(primary_key=True)
    offer_id = IntegerField(null=False, unique=True)
    category = ForeignKeyField(Categories, field='category_id')
    url = CharField(max_length=255, unique=True, null=False)
    price = DecimalField(null=False)
    currency = CharField(max_length=15, null=False)
    picture_link = CharField(max_length=255, null=False)
    short_desc = TextField(null=False)
    full_desc = TextField(null=False)
    goal_price = CharField(max_length=20)
    current_price = CharField(max_length=20)
    vendor_id = IntegerField()
    model = CharField(max_length=255, null=True)
    available = IntegerField(null=False, default=1)

    def get_project_info(self):
        return f'Цель - {self.short_desc}\nОсталось - {self.price} {self.currency}\nПродавец - {self.vendor_id}\n\n'

    def get_full_project_info(self):
        print(self.goal_price)
        return f'Picture \n' \
               f' \n{self.full_desc} \n\n Нужно собрать - {self.goal_price} \n\n Собрано уже - {self.current_price} \n\n' \
               f'Более подробную информацию а так же все новости вы можете посмотреть по ссылке: \n {self.url}'

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
# DB.create_tables([Projects, Categories])
# DB.close()

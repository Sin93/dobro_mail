from peewee import *
from datetime import datetime
from project_exceptions import MissingUserError


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
    def get_all_category():
        return Categories.select()


class Projects(BaseModel):
    id = IntegerField(primary_key=True)
    project_id = IntegerField(null=False, unique=True)
    name = CharField(max_length=255, unique=True, null=False)
    available = IntegerField(null=False, default=1)
    url = CharField(max_length=255, unique=True, null=False)
    category = ForeignKeyField(Categories, field='category_id')
    picture = TextField(null=True)
    vendor = IntegerField()
    short_name = CharField(max_length=100)
    description = TextField(null=True)


    @staticmethod
    def get_projects_by_id(project_id):
        return Projects.get(project_id=project_id)


    @staticmethod
    def get_projects_by_category_id(category_id):
        return Projects.filter(category=category_id).order_by(Projects.id)

from peewee import *
from datetime import datetime
from project_exceptions import MissingUserError


DB = SqliteDatabase('dobro.db')


class BaseModel(Model):
    class Meta:
        database = DB

class User(BaseModel):
    vk_id = IntegerField(primary_key=True, unique=True)
    chat_id = IntegerField(null=False, unique=True)
    created_at = DateTimeField(default=datetime.now)
    favorite_category = IntegerField(null=True, default=None)

    @property
    def get_user_by_id(self, user_id):
        user = User.get(vk_id = user_id)
        if user is None:
            raise MissingUserError

        return user

    @staticmethod
    def create_user(user_id, chat_id):
        new_user = User(vk_id=user_id, chat_id=chat_id)
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

    @property
    def get_last_user_entry(self):
        user_entries = History.filter(user_id=self.user_id).order_by(History.id.desc())
        return user_entries[0]


class Categories(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=100, unique=True, null=False)


class Projects(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=255, unique=True, null=False)
    available = IntegerField(null=False, default=1)
    url = CharField(max_length=255, unique=True, null=False)
    category = ForeignKeyField(Categories)
    picture = TextField(null=False)
    vendor = IntegerField()
    short_name = CharField(max_length=100)
    description = TextField()

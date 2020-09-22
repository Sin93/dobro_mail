import datetime
import random
from threading import Thread, Timer

import config
from BotLogic.DatabaseMethods.bot_methods import Database
from API.ApiMethods import ApiMethodsClass
from BotLogic.Bot import Bot


class SendRemindMessage(Thread):
    def __init__(self):
        super().__init__()

    @staticmethod
    def check_users():
        users = Database.get_all_users()
        time = datetime.datetime.now()
        for user in users:
            if user.can_send_reminds:
                if user.is_active == 0 \
                        and (time - user.updated_at).total_seconds() > config.REMIND_DELAY \
                        and (time - user.last_time_donation).total_seconds() > config.PAYMENT_DELAY:
                    user.updated_at = time
                    user.save()
                    messages = SendRemindMessage.generate_remind_message(user)
                    for message in messages:
                        ApiMethodsClass(user.user_id, message)

    @staticmethod
    def generate_remind_message(user):
        remind_messages = []
        if user.last_project != -1:
            project = Database.get_project(project_id=user.last_project)
            message = f'Последний просмотренный проект\n' \
                        f'{project.get_full_project_info()}'
            photo = f'photo{project.picture.owner_id}_{project.picture.media_id}'

            remind_messages.append(Bot.create_message(message=message, keyboard_type='remind_info', inline=True, payload=project, keyboard=None, attachment=photo))

        if user.last_category != -1:

            projects = Database.get_projects_by_category(user.last_category, config.PROJECTS_AMOUNT)
            index = random.randint(0, len(projects)-1)
            selected_project = projects[index]
            message = f'Проект из последней просмотренной категории\n' \
                        f'{selected_project.get_full_project_info()}'
            photo = f'photo{selected_project.picture.owner_id}_{selected_project.picture.media_id}'
            remind_messages.append(Bot.create_message(message=message, keyboard_type='remind_info', inline=True,
                                                payload=selected_project, keyboard=None, attachment=photo))

            message = 'Если вы не хотите получать уведомления то нажмите кнопку'
            remind_messages.append(Bot.create_message(message=message, keyboard_type='disable_remind', inline=True, payload=user.user_id))

        return remind_messages

    def run(self):
        SendRemindMessage.check_users()


class UpdateDatabase(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        Database.update_all_projects()


def set_interval(time, function, thread, counter=None):
    if counter is None:
        function(thread)
        timer = Timer(time, set_interval, args=[time, function, thread])
        timer.start()
    elif counter == 0:
        print('end of counter\n')
    else:
        function(thread)
        print(f'counter = {counter}\n')
        timer = Timer(time, set_interval, args=[time, function, thread, counter-1])
        timer.start()


def start_new_thread(thread):
    new_thread = thread()
    new_thread.start()

# set_interval(10, start_new_thread, 3, SendRemindMessage)
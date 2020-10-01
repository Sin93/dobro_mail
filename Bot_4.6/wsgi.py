from BotLogic.TaskManager import set_interval, start_new_thread, SendRemindMessage, UpdateDatabase
from config import REMIND_TIME, UPDATE_DATABASE_TIME
from startbot import app


if __name__ == '__main__':
    set_interval(time=REMIND_TIME, function=start_new_thread, counter=15, thread=SendRemindMessage)
    set_interval(time=UPDATE_DATABASE_TIME, function=start_new_thread, counter=15, thread=UpdateDatabase)
    app.run(debug=True)

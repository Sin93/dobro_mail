import os

API_LINK = 'https://api.vk.com/method/{method_name}'

API_VERSION = '5.124'

API_SECRET_KEY = 'ffac7be94d1a488e35d13eacaa05e66d47aee17eeb68b16530'

# Токен группы
TOKEN = '2ba9703dc3633922f2753422de186c352aaf5b28705eeb84aaa16ebb59b65594a6290431cfbf18efb16e3'

# Личный токен для загрузки фото, время жизни - сутки, после этого надо вручную обновлять
ACCESS_TOKEN = '0d28c309889e646ffeb42c7d398d790ca72174336a32f0a64f4930300af187e2a4757d39fb31f16223240'
# получение токена: https://oauth.vk.com/authorize?client_id=7603413&display=page&redirect_uri=http://35.226.30.8/&scope=photos,offline&response_type=token&v=5.124

APP_SEVICE_KEY = '486e62ac486e62ac486e62acbc481dd90e4486e486e62ac170cd2b8a84e928d100cda4f'

CONFIRMATION_TOKEN = '85ee715e'

API_APP = 'vkchatbot2'

API_KEY = '89551b60cb453ad3a0bcc6edc169ef1c6628ff99'

VK_GROUP_ID = 198392433

GROUP_PHOTO_ALBUM_ID = 277400019

PROJECTS_AMOUNT = 3

PROJECTS_DATA = 'https://dobro.mail.ru/projects/rss/target/'

PAYMENT_LINK = 'https://dobro.mail.ru/api/chatbot/create_payment/?api_app=vkchatbot2&api_key=89551b60cb453ad3a0bcc6edc169ef1c6628ff99&amount={amount}&project_id={project_id}&user_id={user_id}'
# вместо ссылки на проект надо подсунуть:
# link = config.PAYMENT_LINK.format(
#     amount=сумма пожертвования,
#     project_id=id проекта,
#     user_id=id пользователя)

XML_URL = None

PATTERN_MAX_ERROR = 0.6

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_DIR = os.path.join(BASE_DIR, "BotLogic/History/")

# Время через которое пользователь становится неактивным если он не совершал каких-либо действий
USER_MAX_ACTIVE_TIME_WITHOUT_ACTIVITY = 20 #seconds

# Время  через которое срабатывает действие
REMIND_TIME = 20 #seconds

# Время ограничивающее отправку пользователью по разнице текущего времени и времени последней активности пользователя в группе
REMIND_DELAY = 30 #seconds

# Время ограничивающее отправку по разнице текущего времени и времени последней оплаты
PAYMENT_DELAY = 50 #seconds

# Время через которое обновляется база данных
UPDATE_DATABASE_TIME = 86400 #seconds == 1 day

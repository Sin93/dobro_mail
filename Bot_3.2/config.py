import json
import os

API_LINK = 'https://api.vk.com/method/{method_name}'

API_VERSION = '5.124'

API_SECRET_KEY = 'ffac7be94d1a488e35d13eacaa05e66d47aee17eeb68b16530'

# Токен для API группы
TOKEN = '2ba9703dc3633922f2753422de186c352aaf5b28705eeb84aaa16ebb59b65594a6290431cfbf18efb16e3'

# Личный токен для загрузки фото, время жизни - сутки, после этого надо вручную обновлять
ACCESS_TOKEN = 'd6a64430d64e934ecd4e3f63ae61ed54562b35b034293984490eacecdcf51adf6c31016dceb505a68a46e'

CONFIRMATION_TOKEN = '85ee715e'

API_APP = ''

API_KEY = ''

VK_GROUP_ID = '198392433'

GROUP_PHOTO_ALBUM_ID = '-198392433_277400019'

PROJECTS_AMOUNT = 5

PROJECTS_DATA = 'https://dobro.mail.ru/projects/rss/target/'

PAYMENT_LINK = 'https://dobro.mail.ru/projects/'

XML_URL = None

PATTERN_MAX_ERROR = 0.6

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_DIR = os.path.join(BASE_DIR, "BotLogic/History/")

PHOTOS_DIR = os.path.join(BASE_DIR, "project_images/")

TEST_CARUSEL = {
    "type": "carousel",
    "elements": [{
            "photo_id": "-198392433_457239035",
            "title": "Title",
            "description": "Description",
            "action": {
                "type": "open_photo",
            },
            "buttons": [{
                "action": {
                        "type": "text",
                        "label": "Label"
                }
            }]
        },
        {
            "photo_id": "-198392433_457239035",
            "title": "Title",
            "description": "Description",
            "action": {
                "type": "open_photo",
            },
            "buttons": [{
                "action": {
                        "type": "text",
                        "label": "Label"
                }
            }]
        },
        {
            "photo_id": "-198392433_457239035",
            "title": "Title",
            "description": "Description",
            "action": {
                "type": "open_photo",
            },
            "buttons": [{
                "action": {
                        "type": "text",
                        "label": "Label"
                }
            }]
        },
    ]
}

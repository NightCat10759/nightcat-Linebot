from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *


def TRY():
    message = TextSendMessage(text="Just try import package")
    line_bot_api.reply_message(event.reply_token, message)
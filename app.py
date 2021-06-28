from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


#======這裡是呼叫的檔案內容=====
#from diary import *
from message import *
from Function import *
#======這裡是呼叫的檔案內容=====

#======python的函數庫==========
import tempfile, os
import datetime
import time
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi('Ckljepr0BT2hKmDWWtbdxBrMleH5Tfd7iBLu0Qqo8XnSxgzp4cNW0vnTLipxVrrqD7pTNl76+z4D3m+vVWpi24DoYh+IrXcLISMD+Y0bEj7zpjZZON41llCBzkpPo/HW1CgG3O9WY3PPKYWid/Em0gdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('175c69e4ddf653b140d3111e804bb566')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text #自己傳的訊息
    if '新增' in msg[0:2]:
        message = TextSendMessage(text=msg)
        line_bot_api.reply_message(event.reply_token, message)
    else:
        message = TextSendMessage(text="No Content")
        line_bot_api.reply_message(event.reply_token, message)



    #if '最新合作廠商' in msg:
    #    message = imagemap_message()
    #    line_bot_api.reply_message(event.reply_token, message)
   # elif '本本' in msg:
   #     message = buttons_message()
  #      line_bot_api.reply_message(event.reply_token, message)
  #  elif '註冊會員' in msg:
 #       message = Confirm_Template()
 #       line_bot_api.reply_message(event.reply_token, message)
 #   elif '旋轉木馬' in msg:
 #       message = Carousel_Template()
 #       line_bot_api.reply_message(event.reply_token, message)
 #   elif '功能列表' in msg:
 #       message = function_list()
 #       line_bot_api.reply_message(event.reply_token, message)
 #   elif '日記' in msg:
 #       message = diary()
 #       line_bot_api.reply_message(event.reply_token, message)
 #   else:
 #       message = TextSendMessage(text=msg)
 #       line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

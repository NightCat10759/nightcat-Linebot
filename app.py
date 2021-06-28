from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


#======這裡是呼叫的檔案內容=====
from TRY import *
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


#
#   待辦小工具: 1.可以新增待辦
#              2.可以刪除特定待辦
#              3.可以顯示全部待辦
#              4.可以插入待辦
#              5.可以移動待辦
#

# 使用手冊
def Help():
    message = TextSendMessage(text="輸入數字顯示該項目使用方法 \
        1.如何新增待辦?\n2.如何刪除待辦?\n3.如何插入待辦?\n4.如何顯示待辦?")
    line_bot_api.reply_message(event.reply_token, message)

    text="1.如何新增待辦? 格式(指令)(年月日)(內容) Ex:新增20190628今天要去買早餐\n \
        \
        2.如何刪除待辦? 格式(指令)(年月日)(內容) Ex:新增20190628今天要去買早餐\n \
        \
        3.如何插入待辦? 格式(指令)(選擇插入行數) Ex:輸入插入\n \
        \
        4.如何顯示待辦? 格式(指令) 第一步輸入:顯示 就會顯示出該行數以及內容 \
            Ex: 顯示\n \
            1.20180502:今天要做事 \n  \
            2.20180505:今天要出門  "


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #TRY()
    message = TextSendMessage(text="歡迎使用TODO機器人，如果不知道如何使用請輸入Help，\
    將會顯示相關資訊。")
    line_bot_api.reply_message(event.reply_token, message)
    msg = event.message.text #自己傳的訊息 , 型態為String
    if   '新增' in msg[0:2]:
        message = TextSendMessage(text=msg)
        line_bot_api.reply_message(event.reply_token, message)
    elif '刪除' in msg[0:2]:
        message = TextSendMessage(text=msg)
        line_bot_api.reply_message(event.reply_token, message)
    elif '插入' in msg[0:2]:
        message = TextSendMessage(text=msg)
        line_bot_api.reply_message(event.reply_token, message)
    elif '顯示' in msg:
        message = TextSendMessage(text=msg)
        line_bot_api.reply_message(event.reply_token, message)
    elif 'Help' in msg:
        Help()
    else:
        message = TextSendMessage(text="輸入失敗，如有不清楚的地方請輸入Help。")
        line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

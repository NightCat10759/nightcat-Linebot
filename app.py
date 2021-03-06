#####   這是一個待辦小工具:
#####                        1.可以新增待辦
#####                        2.可以刪除特定待辦
#####                        3.可以顯示全部待辦
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


#======這裡是呼叫的檔案內容=====
from Method import *
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
Todo_dict = {}
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text #自己傳的訊息 , 型態為String
    if  '新增' in msg[0:2]:
        message = IncreaseTodo(msg[2:6],msg[6:],Todo_dict) #(月日,內容,待辦表)
        line_bot_api.reply_message(event.reply_token, message)
    elif '刪除' in msg[0:2]:
        try:
            int(msg[7])
        except ValueError:
            message = TextSendMessage(text="行數必須為整數，詳細請輸入Help。")
            line_bot_api.reply_message(event.reply_token, message)
        try:
            Todo_dict[msg[2:6]]
            message = DeleteTodo(msg[2:6],msg[7],Todo_dict) #(月日,第幾個,待辦表)
            line_bot_api.reply_message(event.reply_token, message)
        except KeyError:
            message = TextSendMessage(text="本日沒有輸入資料，詳細請輸入Help。")
            line_bot_api.reply_message(event.reply_token, message)
    elif '顯示' in msg[0:2]:
        try:
            Todo_dict[msg[2:6]]
            message = ShowTodo(msg[2:6],Todo_dict) #(月日,待辦表)
            line_bot_api.reply_message(event.reply_token, message)
        except KeyError:
            message = TextSendMessage(text="本日沒有輸入資料，詳細請輸入Help。")
            line_bot_api.reply_message(event.reply_token, message)
    elif 'Help' in msg:
        message = Help_template()
        line_bot_api.reply_message(event.reply_token, message)
    else:
        message = TextSendMessage(text="歡迎使用TODO每日待辦機器人，如果不知道如何使用請輸入Help。")
        line_bot_api.reply_message(event.reply_token, message)
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

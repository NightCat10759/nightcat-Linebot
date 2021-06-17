#這個檔案的作用是：建立待辦列表

#===============這些是LINE提供的功能套組，先用import叫出來=============
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
#===============LINEAPI=============================================

#以下是本檔案的內容本文

#1.建立待辦訊息，名為diary(未來可以叫出此函數來使用)
#function_list的括號內是設定此函數呼叫時需要給函數的參數有哪些

def diary():
    message = TemplateSendMessage(
        alt_text='待辦唷～',
 #       schedule_dict = {},
        template=ButtonsTemplate(
            thumbnail_image_url="../IMG/TODO.jpg",
            title="是否要紀錄待辦？",
            text="選擇以下的操作",
            actions=[
                Show(
                    label="顯示全部待辦",
                    text="全部待辦"
                ),
                Add(
                    label="增加待辦",
                    text="增加待辦瞜!!!"
                ),
                Delete(
                    label="刪除待辦",
                    text="刪除指定待辦"
                )
            ]
        )
    )
    return message
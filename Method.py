from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

#TodoDict = 主程式傳來的dict
def Help_template():
    message = TemplateSendMessage(
        alt_text='一則旋轉木馬按鈕訊息',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://commons.wikimedia.org/w/index.php?search=book&title=Special:MediaSearch&go=Go&type=image',
                    title='待辦',
                    text='按下想知道的內容',
                    actions=[
                        PostbackTemplateAction(
                            label='如何新增待辦?',
                            text='Ans => 請輸入 : 新增(月日)(內容) Ex: 新增0522今天要去倒垃圾")'
                        ),
                        MessageTemplateAction(
                            label='如何顯示待辦?',
                            text='Ans => 請輸入:顯示(月日) Ex:顯示0522"'
                        ),
                        URITemplateAction(
                            label='如何刪除待辦?',
                            text='Ans => 請輸入 :刪除(月日)第(數字)個待辦 Ex: 刪除0526第5個待辦'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRuo7n2_HNSFuT3T7Z9PUZmn1SDM6G6-iXfRC3FxdGTj7X1Wr0RzA',
                    title='這是第二塊模板',
                    text='副標題可以自己改',
                    actions=[
                        PostbackTemplateAction(
                            label='回傳一個訊息',
                            data='這是ID=2'
                        ),
                        MessageTemplateAction(
                            label='用戶發送訊息',
                            text='我知道這是2'
                        ),
                        URITemplateAction(
                            label='進入2的網頁',
                            uri='https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Number_2_in_light_blue_rounded_square.svg/200px-Number_2_in_light_blue_rounded_square.svg.png'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Number_3_in_yellow_rounded_square.svg/200px-Number_3_in_yellow_rounded_square.svg.png',
                    title='這是第三個模塊',
                    text='最多可以放十個',
                    actions=[
                        PostbackTemplateAction(
                            label='回傳一個訊息',
                            data='這是ID=3'
                        ),
                        MessageTemplateAction(
                            label='用戶發送訊息',
                            text='我知道這是3'
                        ),
                        URITemplateAction(
                            label='uri2',
                            uri='https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Number_3_in_yellow_rounded_square.svg/200px-Number_3_in_yellow_rounded_square.svg.png'
                        )
                    ]
                )
            ]
        )
    )
    return message
#   如何新增待辦?    Ans:請輸入 新增(年月日)(內容) Ex: 新增0522今天要去倒垃圾
def IncreaseTodo(MonthDay,Content,TodoDict) :   #(月日,內容,待辦表)
    if Content is None:
        message = TextSendMessage(text="請輸入待辦內容")
    else:
        TodoDict.setdefault(MonthDay,[])
        TodoDict[MonthDay].append(Content)#把月日設為KEY值，把內容丟到後面的list。 <==新增成功
        Month=MonthDay[0:2]
        if MonthDay[0]==0:
                Month=MonthDay[1]
        message = TextSendMessage(text=Month+"月"+MonthDay[2:4]+"日待辦新增成功")  #顯示新增成功的資訊   <==內容丟回去
    return message
#   如何刪除待辦?    Ans:請輸入 刪除月日第(數字)個待辦 Ex: 刪除0522第5個待辦
def DeleteTodo(Monthday,num,TodoDict) : #(月日,第幾個,待辦表)
    num=int(num) # 將第幾個轉換成數字
    if num is None:
        message = TextSendMessage(text="請輸入要刪除的行數")
    else:
        numLocal=num-1
        del TodoDict[Monthday][numLocal]
        message = TextSendMessage(text="刪除第"+str(num)+"項成功")
    return message
#   如何顯示待辦?    Ans:請輸入 顯示(月日)
def ShowTodo(MonthDay,TodoDict) :   #(月日,待辦表)
    try:
        Count=0
        Str=""
        for k in TodoDict[MonthDay]:
            Count+=1
            Str+=MonthDay[1]+"月"+MonthDay[2:4]+"日 第%d項待辦:"%Count+str(k)+"\n"
            message = TextSendMessage(text=Str)
        if Count==0:
            Month=MonthDay[0:2]
            if MonthDay[0]==0:
                Month=MonthDay[1]
            message = TextSendMessage(text=Month+"月"+MonthDay[2:4]+"日沒有待辦")
        return message
    except KeyError:
        message = TextSendMessage(text="輸入錯誤的月日")
        return message
#   使用手冊
def Help() :
    message = TextSendMessage(text="此待辦機器人最多可以紀錄10行待辦，輸入數字顯示使用方法。\n \
    1.如何新增待辦?\n     2.如何刪除待辦?\n     3.如何顯示待辦?")
    return message
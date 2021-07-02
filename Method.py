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
                    thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Formules.JPG/640px-Formules.JPG',
                    title='待辦',
                    text='按下想知道的內容',
                    actions=[
                        MessageTemplateAction(
                            label='如何新增待辦?',
                            text='Ans => 請輸入 : 新增(月日)(內容) \nEx: 新增0522今天要去倒垃圾")'
                        ),
                        MessageTemplateAction(
                            label='如何顯示待辦?',
                            text='Ans => 請輸入:顯示(月日) \nEx:顯示0522"'
                        ),
                        MessageTemplateAction(
                            label='如何刪除待辦?',
                            text='Ans => 請輸入 :刪除(月日)第(數字)個待辦 \nEx: 刪除0526第5個待辦'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://imgs.gvm.com.tw/upload/gallery/20190911/68199010.jpg',
                    title='高科大網址',
                    text='按下以下標題可以進入該網址',
                    actions=[
                        URITemplateAction(
                            label='高科大首頁',
                            uri='https://www.nkust.edu.tw/'
                        ),
                        URITemplateAction(
                            label='高科大教學平台',
                            uri='https://elearning.nkust.edu.tw/mooc/index.php'
                        ),
                        URITemplateAction(
                            label='高科大資工系',
                            uri='http://www.csie.nkust.edu.tw/'
                        )
                    ]
                )
            ]
        )
    )
    return message
def MonthCheck(MonthDay) :
    # 偵測是否為整數
    if MonthDay.isdigit() :
        # 是否為4位數
        if len(MonthDay)!=4 :
            message = TextSendMessage(text="日期必須為四碼")
            return message
        else:
            return
    # 不是整數 break
    else:
        message = TextSendMessage(text="日期必須為整數")
        return message
#   如何新增待辦?    Ans:請輸入 新增(年月日)(內容) Ex: 新增0522今天要去倒垃圾
def IncreaseTodo(MonthDay,Content,TodoDict) :   #(月日,內容,待辦表)
    # 月份是否符合格式
    MonthCheck(MonthDay)
    if Content[0] is None:
        message = TextSendMessage(text="請輸入待辦內容")
        return message
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
    # 月份是否符合格式
    MonthCheck(MonthDay)
    num=int(num) # 將第幾個轉換成數字
    if num is None:
        message = TextSendMessage(text="請輸入要刪除的行數")
        return message
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
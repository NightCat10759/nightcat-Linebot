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
#   如何新增待辦?    Ans:請輸入 新增(年月日)(內容) Ex: 新增0522今天要去倒垃圾
def IncreaseTodo(MonthDay,Content,TodoDict) :   #(月日,內容,待辦表)

    # 偵測是否為整數
    if MonthDay.isdigit() :
        # 是否為4位數
        if len(MonthDay)!=4 :
            message = TextSendMessage(text="日期必須為四碼，詳細請打Help。")
            return message

    # 不是整數 break
    else:
        message = TextSendMessage(text="日期必須為整數，詳細請打Help。")
        return message

    # 檢查內容數
    if len(Content) == 0:
        message = TextSendMessage(text="請輸入待辦內容，詳細請打Help。")
        return message

    # 執行新增
    Month = MonthDay[0:2]
    Day   = MonthDay[2:4]
    TodoDict.setdefault(MonthDay,[])
    TodoDict[MonthDay].append(Content)#把月日設為KEY值，把內容丟到後面的list。 <==新增成功
    message = TextSendMessage(text=Month+"月"+Day+"日待辦新增成功") 

    return message
#   如何刪除待辦?    Ans:請輸入 刪除月日第(數字)個待辦 Ex: 刪除0522第5個待辦
def DeleteTodo(Monthday,num,TodoDict) : #(月日,第幾個,待辦表)
    # 執行刪除
    num=int(num) # 將第幾個轉換成數字
    numLocal=num-1
    del TodoDict[Monthday][numLocal]
    message = TextSendMessage(text="刪除第"+str(num)+"項成功")

    return message
#   如何顯示待辦?    Ans:請輸入 顯示(月日)
def ShowTodo(MonthDay,TodoDict) :   #(月日,待辦表)
    
     # 偵測本日有沒有待辦內容
    if len(TodoDict[MonthDay])==0:
        try:
            del TodoDict[MonthDay]
            if MonthDay[0]==0:
                message = TextSendMessage(text=Month+"月"+ Day +"日沒有待辦")
        except KeyError:
            message = TextSendMessage("本日沒有待辦")
    
    # 顯示
    Str=""
    Month = MonthDay[0:2]
    Day   = MonthDay[2:4]
    Count = 0
    for k in TodoDict[MonthDay]:
        Count += 1
        Str += Month+"月"+ Day +"日 第%d項待辦:"%Count+str(k)+"\n"
    message = TextSendMessage(text=Str)
    return message


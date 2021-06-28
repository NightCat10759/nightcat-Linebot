from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

#Todo = 主程式傳來的msg
#TodoDict = 主程式傳來的dict

#   如何新增待辦?    Ans:請輸入 新增(年月日)(內容) Ex: 新增0522今天要去倒垃圾
def IncreaseTodo(MonthDay,Content,TodoDict) :   #(月日,內容,待辦表)
    TodoDict[MonthDay]=[Content]    #把月日設為KEY值，把內容丟到後面的list。 <==新增成功
    message = TextSendMessage(text=MonthDay+"待辦新增成功")  #顯示新增成功的資訊   <==內容丟回去
    return message
"""
#   如何刪除待辦?    Ans:請輸入 刪除月日第(數字)個待辦 Ex: 刪除0522第5個待辦
def DeleteTodo(Monthday,num,TodoDict) : #(月日,第幾個,待辦表)
    numLocal=num-1
    del TodoDict[Monthday][numLocal]
    message = TextSendMessage(text="刪除第"+str(num)+"項成功")
    return message
"""
#   如何顯示待辦?    Ans:請輸入 顯示
def ShowTodo(Monthday,TodoDict) :   #(月日,待辦表)
    Count=1
    Str=""
    for k in TodoDict[Monthday]:
 #       Str+="第%d項"%Count+str(k)+"\n"
        Str+="第%d項"%Count+"\n"
        Count+=1
    message = TextSendMessage(text=Str)
    return message


#   使用手冊
def Help() :
    message = TextSendMessage(text="此待辦機器人最多可以紀錄10行待辦，輸入數字顯示使用方法。\n \
    1.如何新增待辦?\n2.如何刪除待辦?\n3.如何顯示待辦?")
    return message
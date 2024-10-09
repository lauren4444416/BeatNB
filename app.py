from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

#======python的函數庫==========
import tempfile, os
import datetime
import time
import traceback
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
# OPENAI API Key初始化設定


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
    def IsBig(num):
        return num >= 4
    def IsEven(num):
        return num == 2 or num == 4 or num == 6

    msg = event.message.text
    msg = msg[::-1][:29][::-1]

    one = msg.count("1")
    two = msg.count("2")
    three = msg.count("3")
    four = msg.count("4")
    five = msg.count("5")
    six = msg.count("6")

    small = one + two + three
    big = four + five + six

    odd = one + three + five
    even = two + four + six

    reply = "------\n"
    reply += "1: " + str(one) +"次\n" 
    reply += "2: " + str(two) +"次\n" 
    reply += "3: " + str(three) +"\n" 
    reply += "4: " + str(four) +"\n" 
    reply += "5: " + str(five) +"\n" 
    reply += "6: " + str(six) +"\n" 
    reply += "------\n"
    reply += "小: " + str(small) +"\n" 
    reply += "大: " + str(big) +"\n" 
    reply += "------\n"
    reply += "單: " + str(odd) +"\n" 
    reply += "雙: " + str(even) +"\n" 
    reply += "------\n"

    if small >= 10 or odd >= 10:
        if small >= 10 and not (IsBig(int(msg[-1])) and IsBig(int(msg[-3]))):
            reply += "建議可下注：小\n"
        else:
            reply += "不建議下注：小\n"
        if odd >= 10 and not (IsEven(int(msg[-1])) and IsEven(int(msg[-3]))):
            reply += "建議可下注：單\n"
        else:
            reply += "不建議下注：單\n"
    else:
        reply += "不建議下注\n"
    
    line_bot_api.reply_message(event.reply_token, TextSendMessage(reply))
        

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)



from linebot import LineBotApi
from linebot.models import TextSendMessage
import datetime

line_bot_api=LineBotApi('TT0Wqwwc4Sb///xBx6wagFJD3cozrSdpEXnaolKt2h2ks8UR5DZSnLSMYblKjkiH/80CtqEXNMcbceeXZq4K5eKaesR0KQoD0DiKYm6Cc6QDIDJcbk/uvv4/nbA/Jqlmj+ZBb4Z+RrbgxQl1UFFXfAdB04t89/1O/w1cDnyilFU=')
UserID='U8a38390ef3f99dce49c43876e09f4912'
text_message=TextSendMessage(text=str(datetime.datetime.now()))
line_bot_api.push_message(UserID,text_message)

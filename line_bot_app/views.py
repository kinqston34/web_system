from django.shortcuts import render,HttpResponse   #shortcuts 為收集一些常用工具

# line-bot-api 在django 中檢查的import
import logging
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseBadRequest   #HttpResponse 原始位置

from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

line_bot_api = LineBotApi(settings.CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.CHANNEL_SECRET)
logger = logging.getLogger("django")
# Create your views here.

def line_test(request):
    return HttpResponse("你好")

@csrf_exempt     #迴避csrf
def callback(request):    #檢查 LINE CHANNEL 回應
    if request.method == "POST":
        signature =  request.headers["X-Line-Signature"]  #signature 簽名 or 署名
        body = request.body.decode() # request.body 轉成text

        try:
            handler.handle(body,signature)
        except InvalidSignatureError:    #不合法的簽名 代表CHANNEL_ACCESS_TOKEN / CHANNEL_SECRET 有問題
            print("signature error: 請檢查 CHANNEL_ACCESS_TOKEN / CHANNEL_SECRET ")
            return HttpResponseBadRequest()

        return HttpResponse("OK")
    else:
        return HttpResponseBadRequest()

@handler.add(event=MessageEvent,message=TextMessage)
def handl_message(event):
    line_bot_api.reply_message(
        reply_token=event.reply_token,
        messages=TextSendMessage(text= event.message.text),
    )
from flask import Flask, request, abort
import os
import random

from linebot import (
    LineBotApi, WebhookHandler
)

from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerMessage, StickerSendMessage,
    TemplateSendMessage, ButtonsTemplate, PostbackAction
)

app = Flask(__name__)

#環境変数の呼び出し
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/")
def hello():
    return "here is inside of kumanosuke"

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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "あそぼ":
        line_bot_api.reply_message(
            event.reply_token,
             TemplateSendMessage(
                 alt_text='Buttons template',
                 template= ButtonsTemplate(
                     type="buttons",
                     title='なにする？',
                     text='えらんで！',
                     actions=[
                          {
                            "type": "uri",
                            "label": "Sing!",
                            "uri": "https://www.youtube.com/watch?v=A_UdprUxEZw"
                          },
                        {
                            "type": "uri",
                            "label": "Gaming!!",
                            "uri": "https://games.wkb.jp/ykg/?game_id=jellybears"
                        },
                        {
                            "type": "uri",
                            "label": "radio taisoooooooo!",
                            "uri": "https://www.youtube.com/watch?v=bjKexZvqQeg"
                        },
                                                {
                            "type": "uri",
                            "label": "Give me some friend?",
                            "uri": "https://www.steiff-onlineshop.com/"
                        }
                    ]
                 )
             )
        )
    else:
        comment_list = [
        "I'm Kumanosuke!", 
        "Have you eaten Cannelétte? You should! https://www.uha-mikakuto.co.jp/catalog/other/ot002.html",
        "aaaaa~~~~~",
        "nemui...",
        "bunny ear!()()",
        "Kuma! Kuma! Kuma~~~~!",
        "Bonjour!",
        "coffee or tea?", 
        "Let's go home~~ https://www.youtube.com/watch?v=dUXeJTzSCjc",
        "arigato--"
        ]
        comment_index = random.randint(0, 9)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=comment_list[comment_index])
        )


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    sticker_id_list = [
        10979904, 10979905, 10979907, 10979910, 10979923, 10979908, 10979926
    ]
    sticker_index = random.randint(0, 6)

    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(package_id=6325, sticker_id=sticker_id_list[sticker_index])
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)


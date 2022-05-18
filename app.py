from flask import Flask, request, abort
import os
import random
"""
# from dotenv import load_dotenv
# load_dotenv()
"""
from linebot import (
    LineBotApi, WebhookHandler
)
print()
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    # MessageEvent, TextMessage, TextSendMessage
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


#@handler.add(MessageEvent, message=TextMessage)

# def handle_message(event):
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text=event.message.text))

# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     comment_list = [
#         "Hello, I'm Kumanosuke!", 
#         "Have you eaten Cannelétte? You should! https://www.uha-mikakuto.co.jp/catalog/other/ot002.html",
#         "aaaaa~~~~~",
#         "nemui...",
#         "bunny ear!()()",
#         "Kuma! Kuma! Kuma~~~~! https://www.youtube.com/watch?v=A_UdprUxEZw",
#         "Bonjour!",
#         "coffee or tea?", 
#         "Let's go home~~ https://www.youtube.com/watch?v=dUXeJTzSCjc"
#     ]
#     comment_index = random.randint(0, 8)
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text=comment_list[comment_index])
#     )

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # buttons_template_message = TemplateSendMessage(
    # alt_text='Buttons template',
    # template=ButtonsTemplate(
    #     title='Menu',
    #     text='Please select',
    #     actions=[
    #         PostbackAction(
    #             label='postback',
    #             display_text='postback text',
    #             data='action=buy&itemid=1'
    #         )
    #     ]
    # )
    # )
    
    if event.message.text == "あそぼ":
        line_bot_api.reply_message(
            event.reply_token,
             TemplateSendMessage(
                 alt_text='Buttons template',
                 template= ButtonsTemplate(
                     type="buttons",
                     title='Menu',
                     text='Please select',
                     actions=[
                          {
                            "type": "postback",
                            "label": "Buy",
                            "data": "action=buy&itemid=123"
                          },
                        {
                            "type": "postback",
                            "label": "Add to cart",
                            "data": "action=add&itemid=123"
                        },
                        {
                            "type": "uri",
                            "label": "View detail",
                            "uri": "http://example.com/page/123"
                        }
                    ]
                 )
             )
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

"""
# if __name__ == "__main__":
    # port = int(os.getenv("PORT", 8080))
    # app.run(host="0.0.0.0", port=port)
    # app.run(port=os.environ.get('PORT', 8080))
    # app.run()
"""

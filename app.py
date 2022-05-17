from flask import Flask, request, abort
import os
# import random
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
    MessageEvent, TextMessage, TextSendMessage, StickerMessage, StickerSendMessage
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
@handler.add(MessageEvent, message=StickerMessage)

# def handle_message(event):
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text=event.message.text))


# def handle_message(event):

# reply comment
# comment_list = [
#         "Hello, I'm Kumanosuke!", 
#         "Have you eaten Cannelette? You should! https://www.uha-mikakuto.co.jp/catalog/other/ot002.html",
#         "aaaaa~~~~~",
#         "nemui...",
#         "bunny ear!()()",
#         "Kuma! Kuma! Kuma~~~~! https://www.youtube.com/watch?v=A_UdprUxEZw",
#         "Bonjour!",
#         "coffee or tea?"
#     ]
# index = random.randint(0, 6)

def handle_message(event):

    line_bot_api.reply_message(
        event.reply_token,
        StickerMessage(package_id=6325, sticker_id=10979909))

if __name__ == "__main__":
    app.run(debug=True, port=5000)

"""
# if __name__ == "__main__":
    # port = int(os.getenv("PORT", 8080))
    # app.run(host="0.0.0.0", port=port)
    # app.run(port=os.environ.get('PORT', 8080))
    # app.run()
"""

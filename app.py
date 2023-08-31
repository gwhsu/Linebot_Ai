from flask import Flask, request, abort

# from config import  line_channel_access_token, line_channel_secret
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from mongodb import *
from function import *
import os
from model_api import thin_plate_spline_motion

# ======setting=====
switch = False

# -----------------------------
app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

line_channel_access_token = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
line_channel_secret = os.environ.get('LINE_CHANNEL_SECRET')

# Channel Access Token
line_bot_api = LineBotApi(line_channel_access_token)
# Channel Secret
handler = WebhookHandler(line_channel_secret)


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
    global switch
    msg = event.message.text

    user_id = event.source.user_id
    print('get user id::', user_id)
    profile = line_bot_api.get_profile(user_id)
    print('get profile pass::', profile)

    # INFO -------------------------------
    print(profile.display_name)
    print(profile.user_id)
    print(profile.picture_url)
    print(profile.status_message)
    print('join')

    # need build a operation list (json)
    if 'Hello' in msg:
        message = 'Hello ' + str(profile.display_name)
        message = TextSendMessage(text=message)

    elif '!op' in msg:
        txt = '🔥 ' + 'Hello' + ' 🔥\n'
        txt += '🔥 ' + '占卜 @[str]' + ' 🔥\n'
        message = TextSendMessage(text=txt)

    # elif '占卜 @' in msg:
    #     message = procast(msg)

    # elif '抽卡' in msg:
    #     url, rd_img, title = get_pttinfo()
    #     message = ptt_drawcard(url, rd_img, title)

    elif '!Hulan' in msg:
        message = Hulan(msg)

    elif '!Switch' in msg:
        if(switch):
            switch = False
            txt = '關 :('
        else:
            switch = True
            txt = '開 :)'

        message = TextSendMessage(text=txt)
    # elif '!getlineid' in msg:
    #     lineid_mapping(profile.display_name, profile.user_id)
    #     message = TextSendMessage(text=profile.user_id)
    elif '!broadcast' in msg:
        message = msg.split(' ')[1]
        line_bot_api.broadcast(TextSendMessage(text=message))
    else:
        # set_msg in function.py
        message = set_msg(msg)

    line_bot_api.reply_message(event.reply_token, message)


@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    if switch:
        user_id = event.source.user_id
        image_message_id = event.message.id

        # 取得用戶上傳的圖片
        response = line_bot_api.get_message_content(image_message_id)
        with open("user_image.jpg", "wb") as f:
            for chunk in response.iter_content():
                f.write(chunk)

        video_url = thin_plate_spline_motion("user_image.jpg")
        video_message = VideoSendMessage(
            original_content_url=video_url,
            preview_image_url=video_url
        )

        line_bot_api.push_message(user_id, video_message)

@handler.add(JoinEvent)
def handle_join(event):
    newcoming_text = "開始報告"

    line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=newcoming_text)
        )
    print("JoinEvent =", JoinEvent)


@handler.add(LeaveEvent)
def handle_leave(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextMessage(text="Where I am , U r where ")
    )
    print("leave Event =", event)
    print("我被踢掉了QQ ", event.source)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
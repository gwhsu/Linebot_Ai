# Standard
import os

# Linebot relative
from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    VideoMessage,
    ImageMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    ImageMessageContent,
)

from function import *
from model_api import *
from config import line_channel_access_token, line_channel_secret
from mongodb import check_mode, mode_change

app = Flask(__name__)

configuration = Configuration(access_token=line_channel_access_token)
handler = WebhookHandler(line_channel_secret)

# ======setting=====
switch = False
video_tag_switch = False


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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    global switch, video_tag_switch

    msg = event.message.text
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        user_id = event.source.user_id
        # print('get user id::', user_id)
        # profile = line_bot_api.get_profile(user_id)
        # print('get profile pass::', profile)
        #
        # # INFO -------------------------------
        # print(profile.display_name)
        # print(profile.user_id)
        # print(profile.picture_url)
        # print(profile.status_message)
        # print('join')

        # need build a operation list (json)
        if 'Hello' in msg:
            message = 'Hello ' + str(profile.display_name)
            message = TextMessage(text=message)

        elif '!op' in msg:
            txt = '🔥 ' + 'Hello' + ' 🔥\n'
            txt += '🔥 ' + '占卜 @[str]' + ' 🔥\n'
            txt += '🔥 ' + 'Hulan [str] [Hulan size]' + ' 🔥\n'
            message = TextMessage(text=txt)

        elif '占卜 @' in msg:
            message = procast(msg)
        # elif '抽卡' in msg:
        #     url, rd_img, title = get_pttinfo()
        #     message = ptt_drawcard(url, rd_img, title)
        elif "安靜" or "說話" in msg:
            mode_change(msg)

        elif '!video_tag_switch' in msg:
            if video_tag_switch:
                video_tag_switch = False
            else:
                video_tag_switch = True

        elif '!Hulan' in msg:
            message = Hulan(msg)

        elif '!Switch' in msg:
            if(switch):
                switch = False
                txt = '關 :('
            else:
                switch = True
                txt = '開 :)'

            message = TextMessage(text=txt)
        # elif '!getlineid' in msg:
        #     lineid_mapping(profile.display_name, profile.user_id)
        #     message = TextSendMessage(text=profile.user_id)
        elif '!broadcast' in msg:
            print('broadcast')
            message = msg.split(' ')[1]
            # for user_id in user_ids:
            line_bot_api.push_message(user_id, messages=message)
            # line_bot_api.push_message(TextMessage(text=message))
        else:
            # Gemini Ai  in function.py
            print(check_mode())
            if(check_mode() != "quiet"):
                message = Gemini_msg(msg)

        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[message]
            )
        )

@handler.add(MessageEvent, message=ImageMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        if switch:
            user_id = event.source.user_id
            image_message_id = event.message.id

            # 取得用戶上傳的圖片
            response = line_bot_api.get_message_content(image_message_id)
            with open("user_image.jpg", "wb") as f:
                for chunk in response.iter_content():
                    f.write(chunk)

            video_url = thin_plate_spline_motion("user_image.jpg", video_tag_switch)
            video_message = VideoSendMessage(
                original_content_url=video_url,
                preview_image_url=get_img_url()
            )
            line_bot_api.reply_message(
                event.reply_token,
                [TextMessage(text='影片已生成：'), video_message]
            )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
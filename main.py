# -*- coding: UTF-8 -*-
import os
import tempfile 

import re

import sys
from google.cloud import automl_v1beta1 
from google.cloud.automl_v1beta1.proto import service_pb2 




from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,TemplateSendMessage,SpacerComponent,
    ImageCarouselTemplate,ImageCarouselColumn,DatetimePickerAction,TextComponent,ButtonComponent,ButtonsTemplate,
    ImageMessage, VideoMessage, AudioMessage,CarouselTemplate,CarouselColumn,SeparatorComponent,ConfirmTemplate,
    PostbackAction,MessageAction,URIAction,BubbleContainer,ImageComponent,BoxComponent,FlexSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('3tWacqgMaMS5tBUjh257Tz9FOb0ywKUPqcUh1W31EyggYYgMCW2lPvW3QivYWODr5KD61GKloTr6a/9zBVs889ppiBcaC6aUJdG6pPLJ/LceUU4Bt3+iSF6iQkHpMyN8DxbZwTWvB62y2/1jZK6XUgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('eec0ccba1eae61cec3bb8a3c731dfaea')

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp') 

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

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text  
    
        
    if text == 'new' or text == 'New' :
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://imgur.com/ag2SgQe.jpg',
                                action=URIAction(label='資訊',
                                                            uri='https://www.goodsmile.info/zh/product/7837/%E9%BB%8F%E5%9C%9F%E4%BA%BA+%E9%87%91.html',
                                                            )),
            ImageCarouselColumn(image_url='https://imgur.com/0ZhjqId.jpg',
                                action=URIAction(label='資訊',
                                                 uri='https://www.goodsmile.info/zh/product/7952/%E9%BB%8F%E5%9C%9F%E4%BA%BA+%E7%B6%A0%E9%96%93%E7%9C%9F%E5%A4%AA%E9%83%8E.html',
                                                ))
        ])
        template_message = TemplateSendMessage(
            alt_text='ImageCarousel alt text', template=image_carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'use':
        confirm_template = ConfirmTemplate(text='傳一張黏土人照片，將為您分析黏土人的編號，及官方網址。', actions=[
            MessageAction(label='知道啦', text='Yes!'),
            MessageAction(label='你確定', text='還是不知道!'),
        ])
        template_message = TemplateSendMessage(
            alt_text='Confirm alt text', template=confirm_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    else:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text))
    

def get_prediction(message_content, project_id, model_id):
    KEY_FILE = "v3-219812-ff97e541838f.json"
    prediction_client = automl_v1beta1.PredictionServiceClient()
    prediction_client = prediction_client.from_service_account_json(KEY_FILE)

    name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
    payload = {'image': {'image_bytes': message_content }}
    params = {}
    request = prediction_client.predict(name, payload, params)
    return request  # waits till request is returned

# Other Message Type
@handler.add(MessageEvent, message=(ImageMessage, VideoMessage, AudioMessage))
def handle_content_message(event):
    if isinstance(event.message, ImageMessage):
        ext = 'jpg'
    elif isinstance(event.message, VideoMessage):
        ext = 'mp4'
    elif isinstance(event.message, AudioMessage):
        ext = 'm4a'
    else:
        return

#save jpg    
    message_content = line_bot_api.get_message_content(event.message.id)
#save file.jpg  
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    dist_path = tempfile_path + '.' + ext
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)

    
    message_content = os.path.join('static', 'tmp', dist_name)
    with open(message_content,'rb') as ff:
        message_content=ff.read()
    
    
    print get_prediction(message_content,'v3-219812','ICN7521245635834906')
    abc = get_prediction(message_content,'v3-219812','ICN7521245635834906')
    a1 = str(abc)
    result = re.search('(?<=score: ).*(?=\n)',a1).group()
    result2 = re.search('(?<=display_name: ").*(?="\n)',a1).group()
    
    b01 = float(result)
    a1 = str(abc)
    a2 = a1[30:50]
    a3 = a1[55:79]
    print type(abc)
    print result
    
    if (result2=="tamaki" and b01>=0.8):
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://imgur.com/Vsi1nLt.jpg',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
                action=URIAction(uri='https://imgur.com/Vsi1nLt', label='label')
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text='926四葉環', weight='bold', size='xl'),
                    # review
                    
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='相近',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text=result2,
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='數值',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text=result,
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    # callAction, separator, websiteAction
                    SpacerComponent(size='sm'),
                    # callAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='好微笑看看', uri='https://www.goodsmile.info/zh/product/7240/%E9%BB%8F%E5%9C%9F%E4%BA%BA+%E5%9B%9B%E8%91%89%E7%92%B0.html'),
                    ),
                    # separator
                ]
            ),
        )
        message = FlexSendMessage(alt_text="感謝您的使用以下為你分析", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    
        
    
    elif (result2=="sogo" and b01>=0.8):
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://imgur.com/oP3mQNC.jpg',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
                action=URIAction(uri='https://imgur.com/oP3mQNC', label='label')
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text='905逢板壯五', weight='bold', size='xl'),
                    # review
                    
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='相近',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text=result2,
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='數值',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text=result,
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    # callAction, separator, websiteAction
                    SpacerComponent(size='sm'),
                    # callAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='好微笑看看', uri='https://www.goodsmile.info/zh/product/7175/%E9%BB%8F%E5%9C%9F%E4%BA%BA+%E9%80%A2%E5%9D%82%E5%A3%AF%E4%BA%94.html'),
                    ),
                    # separator
                ]
            ),
        )
        message = FlexSendMessage(alt_text="感謝您的使用以下為你分析", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
   
        
    
    

    elif (result2=="Kirby"):
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://imgur.com/ec1wSXs.jpg',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
                action=URIAction(uri='https://imgur.com/ec1wSXs', label='label')
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text='544星之卡比', weight='bold', size='xl'),
                    # review
                    
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='相近',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text=result2,
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='數值',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text=result,
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    # callAction, separator, websiteAction
                    SpacerComponent(size='sm'),
                    # callAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='好微笑看看', uri='https://www.goodsmile.info/zh/product/5207/%E9%BB%8F%E5%9C%9F%E4%BA%BA+%E5%8D%A1%E6%AF%94.html'),
                    ),
                    # separator
                ]
            ),
        )
        message = FlexSendMessage(alt_text="感謝您的使用以下為你分析", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
        
    elif (result2=="kirbyPirate" and b01>=0.8):
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://imgur.com/Q032z3A.jpg',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
                action=URIAction(uri='https://imgur.com/Q032z3A', label='label')
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    # title
                    TextComponent(text='此款有盜版嫌疑!!', weight='bold', size='xl'),
                    # review
                    
                    # info
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='相近',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text=result2,
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='數值',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text=result,
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    # callAction, separator, websiteAction
                    SpacerComponent(size='sm'),
                    # callAction
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='好微笑看看', uri='https://www.goodsmile.info/zh/product/7175/%E9%BB%8F%E5%9C%9F%E4%BA%BA+%E9%80%A2%E5%9D%82%E5%A3%AF%E4%BA%94.html'),
                    ),
                    # separator
                ]
            ),
        )
        message = FlexSendMessage(alt_text="感謝您的使用以下為你分析", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
        
    else:
        line_bot_api.reply_message(
        event.reply_token, [TextSendMessage(text='not find')])
    
    


if __name__ == "__main__":
    app.debug = True
    app.run(host=os.getenv('IP','0.0.0.0'),port=int(os.getenv('PORT','8080')))

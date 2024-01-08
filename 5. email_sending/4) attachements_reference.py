
# 이미지 첨부 외에 다양한 첨부 보내기
import os

from email.mime.multipart import MIMEMultipart

from email import encoders

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio

from email.mime.base import MIMEBase

msg_dict = {
    'text':{'maintype':'text', 'subtype':'plain', 'filename':'res/test.txt'},
    'image':{'maintype':'image', 'subtype':'jpg', 'filename':'res/test.jpg'},
    #'audio':{'maintype':'audio', 'subtype':'mp3', 'filename':'res/test.mp3'},
    #'vidoe':{'maintype':'video', 'subtype':'mp4', 'filename':'res/test.mp4'},
    'application':{'maintype':'application','subtype':'octect-stream','filename':'res/test.pdf'}
}

def make_multimsg(msg_dict):
    multi=MIMEMultipart(_subtype='mixed')

    for key, value in msg_dict.items():
        if key == 'text':
            with open(value['filename'], encoding='utf-8') as fp:
                msg = MIMEText(fp.read(), _subtype=value['subtype'])
        elif key == 'image':
            with open(value['filename'], 'rb') as fp:
                msg = MIMEImage(fp.read(), _subtype=value['subtype'])
        elif key == 'audio':
            with open(value['filename'], 'rb') as fp:
                msg = MIMEAudio(fp.read(), _subtype=value['subtype'])
        else:
            with open(value['filename'], 'rb') as fp:
                msg = MIMEBase(value['maintype'], _subtype=value['subtype'])
                msg.set_payload(fp.read())
                encoders.encode_base64(msg)
        msg.add_header('Content-Disposition', 'attachment',
                       filename=os.path.basename(value['filename']))
        multi.attach(msg)

    return multi





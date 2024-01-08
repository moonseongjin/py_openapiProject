# 이미지 첨부
"""
본 프로젝트는 주피터 노트북에서 실행하였기 때문에 
순서대로 이루어질 경우 가능.

이것만을 돌리기를 희망할 경우 함수 

1)에 있는 

함수, send_email와 

메일 전송 파라미터
smtp_info = dict({"smtp_server" : "smtp.naver.com", # SMPT 서버 주소
                  "smtp_user_id" : "@naver.com", # 송신자 메일 계정
                  "smtp_user_pw" : "", # 송신자 패스워드 / 이메일 비밀번호 말고 앱 비밀번호 
                  "smtp_port" : "587"}) # SMPT 서버 포트
가 필요함

"""
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

# 첨부파일 추가
def attach_multi(multi_info):

    # 3. 이메일 메시지에 다양한 형식을 담아내기 위한 객체 설정
    multi = MIMEMultipart(_subtype='mixed')
    
    # 4. 이미지 갯수만큼 반복
    for key, value in multi_info.items():
    
        # 이미지 타입 MIMEImage 함수 호출하여 msg 객체 생성   
        with open(value['filename'], 'rb') as fp:
            msg = MIMEImage(fp.read(), _subtype=value['subtype'])
        
        # 파일명을 첨부파일 제목으로 추가
        msg.add_header('Content-Disposition', 'attachment', filename=value['filename'])

        # 첨부파일 추가
        multi.attach(msg)
    
    return multi

# 1. 보낼 이미지 파라미터
multi_info = {
    'image' : {'maintype' : 'image', 'subtype' :'png', 'filename' : 'C:/Users/moonw/py_life/res/email_sending/test.png' }
}

# 전송할 메일 정보 작성
sender = send_info["send_user_id"]
receiver = "@naver.com"
title = "개발새발 보낸 메일 제목입니다"
content = "개발새발 보낸 메일 내용입니다"

# 메일 객체 생성
message = MIMEText(_text = content, _charset = "utf-8") # 메일 내용

# 2. 첨부파일 추가
multi = attach_multi(multi_info)

# 5. 첨부파일 추가한 객체에 정보 세팅
multi['subject'] = title # 메일 제목
multi['from'] = sender # 보낸사람
multi['to'] = receiver # 받는사람
multi.attach(message)

# 메일 전송 함수를 호출
send_email(send_info, multi)
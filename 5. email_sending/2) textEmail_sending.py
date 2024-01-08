# 텍스트 보내기
import smtplib
from email.mime.text import MIMEText

smtp_info = dict({"smtp_server" : "smtp.naver.com", # SMPT 서버 주소
                  "smtp_user_id" : "@naver.com", # 송신자 메일 계정
                  "smtp_user_pw" : "", # 송신자 패스워드 / 이메일 비밀번호 말고 앱 비밀번호 
                  "smtp_port" : "587"}) # SMPT 서버 포트

def send_email(send_info, msg):
    
    # SMTP 세션 생성
    with smtplib.SMTP(smtp_info["smtp_server"], smtp_info["smtp_port"]) as server:
        
        # TLS 보안 연결
        server.starttls()
        
        # 보내는사람 계정으로 로그인
        server.login(smtp_info["smtp_user_id"], smtp_info["smtp_user_pw"])

        # 로그인 된 서버에 이메일 전송
        response = server.sendmail(msg['from'], msg['to'], msg.as_string())

        # 이메일 전송 성공시
        if not response:
            print('이메일을 정상적으로 보냈습니다.')
        else:
            print(response)

# 메일 작성 내용
title = "기본 이메일입니다."
content = "메일 내용입니다."
sender = smtp_info['smtp_user_id'] # 송신자(sender) 이메일 계정
receiver = "moonwalk486@naver.com" # 수신자 이메일 계정

# 메일 객체 생성 : 메시지 내용에는 한글이 들어가기 때문에 한글을 지원하는 문자 쳬게, UTF-8을 명시해줍니다.

msg = MIMEText(_text = content, _charset='utf-8') # 본문 텍스트

msg['Subject'] = title # 메일 제목
msg['From'] = sender
msg['To'] = receiver

send_email(smtp_info, msg)



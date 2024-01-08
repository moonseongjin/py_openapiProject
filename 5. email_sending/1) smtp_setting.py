import smtplib

smtp_info = dict({"smtp_server" : "smtp.naver.com", # SMPT 서버 주소
                  "smtp_user_id" : "@naver.com", # 송신자 메일 계정
                  "smtp_user_pw" : "", # 송신자 패스워드 / 이메일 비밀번호 말고 앱 비밀번호 
                  "smtp_port" : "587"}) # SMPT 서버 포트

# 메일 전송
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
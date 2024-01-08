# 1 REST API와 REDIRECT URI를 활용하여 AuthorizationCode(인가코드) 발급받기

"""
https://kauth.kakao.com/oauth/authorize?client_id=<REST API 키>
&redirect_uri=<Redirect URI>&response_type=code&scope=talk_message
을 시크릿창에서 입력하면

1
?code=BeySlSWun-92ydFw_kQ5qsHgqwgvOrYLsc-zCMVbgJVGlJ-_P2x_lNA0I8S52Kw0fAAABi9yEQp98Pd5TpQ
토큰이 발급된다.(code가 토큰 번호임)

1. 한 번의 인증 과정에서만 사용되어야 하며, 사용 후에는 무효화, 이는 보안상의 이유
2. 따라서 이를 기반으로 Access Token을 요청하고 사용하는 것이 일반적인 플로우
"""

# 2 인가코드 발급받은 걸로 아래 내용 출력.
# access_token, token_type, refresh_token, expires_in, talk_message, refresh_token_expires_in
import requests

url = "https://kauth.kakao.com/oauth/token"

data = {
    "grant_type" : "authorization_code",
    "client_id" : "REST API 키",
    "redirect_uri" : "https://localhost.com",
    "code" : "인가코드"    
}

response = requests.post(url, data=data)

# 요청에 실패했다면,
if response.status_code !=200:
    print("error! because ", response.json())
else: # 요청에 성공했다면,
    tokens = response.json()
    print(tokens)

"""
# 2 엑세스 토큰, 리프레쉬 토큰 발급
{
'access_token': '비밀', 
'token_type': 'bearer', 
'refresh_token': '비밀', 
'expires_in': 21599, 
'scope': 'profile_nickname', 
'refresh_token_expires_in': 5183999
}

Access Token의 유효 기간이 21599초(약 6시간)
Refresh Token의 유효 기간이 5183999초(약 60일)
"""
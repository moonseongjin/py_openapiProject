"""
#==============================================================================================
#==============================================================================================
# 1 REST API와 REDIRECT URI를 활용하여 AuthorizationCode(인가코드) 발급받기

https://kauth.kakao.com/oauth/authorize?client_id=<REST API 키>
&redirect_uri=<Redirect URI>&response_type=code&scope=talk_message
을 시크릿창에서 입력하면

https://localhost.com/
?code=BjySlSWun-92ydFw_kQ5qsHvOTrYLsc-zCMVbgJVGlJ-_P2x_lNA0I8S524KKw0fAAABi9yEQFbC3p98Pd5TpQ
토큰이 발급된다.(code가 토큰 번호임)

1. 한 번의 인증 과정에서만 사용되어야 하며, 사용 후에는 무효화, 이는 보안상의 이유
2. 따라서 이를 기반으로 Access Token을 요청하고 사용하는 것이 일반적인 플로우
"""

#==============================================================================================
#==============================================================================================
# 2 인가코드 발급받은 걸로 아래 내용 출력.
# access_token, token_type, refresh_token, expires_in, talk_message, refresh_token_expires_in
import requests

url = "https://kauth.kakao.com/oauth/token"

data = {
    "grant_type" : "authorization_code",
    "client_id" : " REST API",
    "redirect_uri" : "https://localhost.com -내가 만든",
    "code" : "인가코드"    
}

response = requests.post(url, data=data)

# 요청에 실패했다면,
if response.status_code !=200:
    print("error! because ", response.json())
else: # 요청에 성공했다면,
    tokens = response.json()
    print(tokens)


#==============================================================================================
#==============================================================================================
# 저장 및 카카오 읽기 업데이트 전송 등

import requests
import json
import datetime
import os

# 카카오 토큰을 저장할 파일명
KAKAO_TOKEN_FILENAME = "res/kakao_token.json"

# 저장하는 함수
def save_tokens(filename, tokens):
    with open(filename, "w") as fp:
        json.dump(tokens, fp)
        
# 읽어오는 함수
def load_tokens(filename):
    with open(filename) as fp:
        tokens = json.load(fp)
        
    return tokens

# refresh_token으로 access_token 갱신하는 함수
def update_tokens(app_key, filename):
    tokens = load_tokens(filename)
    
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type" : "refresh_token",
        "client_id" : "REST API",
        "refresh_token" : tokens['refresh_token']
    }
    response = requests.post(url, data=data)
    
    # 요청에 실패했다면,
    if response.status_code != 200:
        print("error! because ", response.json())
        tokens = None
    else: # 요청에 성공했다면,
        print(response.json())
        # 기존 파일 백업
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = filename+"."+now
        os.rename(filename, backup_filename)
        # 갱신된 토큰 저장
        tokens['access_token'] = response.json()['access_token']
        save_tokens(filename, tokens)
        
    return tokens

def send_message(filename, template):
    tokens = load_tokens(filename)
    headers={
        "Authorization":"Bearer "+tokens['access_token']
    }
    payload = {
        "template_object":json.dumps(template)
    }
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    res = requests.post(url, data=payload, headers=headers)

    return res

# 토큰 저장
save_tokens(KAKAO_TOKEN_FILENAME, tokens)

#==============================================================================================
#==============================================================================================
# 6. 텍스트 템플릿으로 날씨 및 미세먼지 정보 전송하기

KAKAO_TOKEN_FILENAME = "res/kakao_token.json"
KAKAO_APP_KEY = "223d244c5f04dee77a107d484d57d36f"
update_tokens(KAKAO_APP_KEY, KAKAO_TOKEN_FILENAME)

address_name = "문래동"

weather_url = "https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query=%EB%82%A0%EC%94%A8" + address_name

text = f"""
기온: {data['weather']['tmp']}
기우: {data['weather']['state']}
미세먼지: {data['dust']['PM10']['value']} {data['dust']['PM10']['state']}
초미세먼지: {data['dust']['PM2.5']['value']} {data['dust']['PM2.5']['state']}
"""

template = {
    "object_type":"text",
    "text":text,
    "link":{
        "web_url":weather_url,
        "mobile_web_url":weather_url
    },
    "button_title":"날씨 상세보기"
}

res = send_message(KAKAO_TOKEN_FILENAME, template)
if res.json().get('result_code') == 0:
    print("성공적으로 보냄")
else:
    print("실패", res.json())


#==============================================================================================
#==============================================================================================
# 7. 리스트 템플릿으로 맛집 정보 전송하기

# 리스트 템플릿 
contents = []
template = {
    "object_type":"list",
    "header_title":"현재 날씨에 따른 음식 추천",
    "header_link":{
        "web_url":weather_url,
        "mobile_web_url":weather_url
    },
    "contents":contents,
    "buttons":[
        {
            "title":"날씨 정보 상세 보기",
            "link":{
                "web_url":weather_url,
                "mobile_web_url":weather_url
            }
        }
    ],
}


for place in recommands:
    title = place.get('title')
    title = title.replace("<b>","").replace("</b>","")
    category = place.get('category')
    telephone = place.get('telephone')
    address = place.get('address')

# 각 장소를 클릭할 때 네이버 검색으로 연결해주기 위해 작성된 코드
    enc_address = address + ' ' + title
    query = "query" + enc_address
    
    # 장소 카테고리가 카페이면 카페 이미지
    # 이외에는 음식 이미지
    if '카페' in category:
        # https://freesvg.org/ 무료 SVG 벡터 파일
        # 커피 이미지
        image_url = "https://freesvg.org/img/pitr_Coffee_cup_icon.png"
    else:
        # 도시락 이미지
        image_url = "https://freesvg.org/img/bentolunch.png?w=150&h=150&fit=fill"
    # 전화번호가 있다면 제목과 함께
    if telephone:
        title = title +"\ntel)" + telephone
        
    # 카카오톡 리스트 템플릿 형식에 맞춰줍니다.
    content = {
        "title" : "[" + category + "]" + title,
        "description" : ' '.join(address.split()[1:]),
        "image_url": image_url,
        "image_width": 50, "image_height": 50,
        "link":{
            "web_url": "https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query=" + enc_address,
            "mobile_web_url":"https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query=" + enc_address
        }
    }
    contents.append(content)

# 카카오톡 메시지 전송
res = send_message(KAKAO_TOKEN_FILENAME, template)
if res.json().get('result_code') == 0:
    print("맛집 정보 성공적으로 보냄")
else:
    print("실패", res.json())
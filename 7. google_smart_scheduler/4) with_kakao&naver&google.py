# =============================================================================
# =============================================================================
# 1.
## 필요한 라이브러리
from google_auth_oauthlib.flow import InstalledAppFlow
# 구글 캘린더 API 서비스 객체 생성
from googleapiclient.discovery import build
import datetime

# 구글 클라우드 콘솔에서 다운받은 OAuth 2.0 클라이언트 파일경로
creds_filename = 'credentials.json'

# 사용 권한 지정
# https://www.googleapis.com/auth/calendar	               캘린더 읽기/쓰기 권한
# https://www.googleapis.com/auth/calendar.readonly	       캘린더 읽기 권한
SCOPES = ['https://www.googleapis.com/auth/calendar']

# 파일에 담긴 인증 정보로 구글 서버에 인증하기
# 새 창이 열리면서 구글 로그인 및 정보 제공 동의 후 최종 인증이 완료됩니다.
flow = InstalledAppFlow.from_client_secrets_file(creds_filename, SCOPES)
creds = flow.run_local_server(port=0)

#객체 생성

service = build('calendar', 'v3', credentials=creds)

# =============================================================================
# =============================================================================
# 2.
# 구글 캘린더 일정 조회 및 데이터 정제하기

calendar_id = 'primary' # 사용할 캘린더 ID
today = datetime.date.today().strftime("%Y-%m-%d")
# 일정을 조회할 날짜 YYYY-mm-dd 포맷
time_min = today + 'T00:00:00+09:00' # 일정을 조회할 최소 날짜
time_max = today + 'T23:59:59+09:00' # 일정을 조회할 최대 날짜
max_results = 5 # 일정을 조회할 최대 개수
is_single_events = True # 반복 일정의 여부
orderby = 'startTime' # 일정 정렬

# 오늘 일정 가져오기
events_result = service.events().list(calendarId = calendar_id,
                                      timeMin = time_min,
                                      timeMax = time_max,
                                      maxResults = max_results,
                                      singleEvents = is_single_events,
                                      orderBy = orderby
                                     ).execute()
items = events_result.get('items')
print("==[일정 목록 출력]==")
print(items)
item = items[0] # 텍스트를 위해 오늘 일정에서 한 개만 가져옵니다.

# 일정 제목
gsummary = item.get('summary')
print(gsummary)
# 일정 제목에서 [식사 - 국민대]에서 카테고리와 장소를 추출합니다.
gcategory, glocation = gsummary[gsummary.index('[')+1 : gsummary.index(']')].split('-')

# 구글 캘린더 일정이 연결되어있는 링크입니다.
gevent_url = item.get('htmlLink')
print("\n\n===[일정 상세 정보 출력]===")
print("category : ", gcategory)
print("location : ", glocation)
print("gevent_url : ", gevent_url)

# =============================================================================
# =============================================================================
# 3.
# 네이버 지역 검색으로 맛집 검색하기
import requests

headers = {
    'X-Naver-Client-Id':'네이버 애플리케이션의 클라이언트 ID',
    'X-Naver-Client-Secret':'네이버 애플리케이션의 클라이언트 Sercret'
}

# 지역 검색 요청 파라미터 설정
query= glocation + " 맛집"
params = {
    'sort':'comment',
    'query':query,
    'display':3
}

naver_local_url = 'https://openapi.naver.com/v1/search/local.json'

res = requests.get(naver_local_url, headers=headers, params=params)

if res.status_code == 200:
    places = res.json().get('items')
    print(places)


# =============================================================================
# =============================================================================
# 4. 카카오 전송(이전 방법과 같은 것은 주석처리함)
"""
# 1 REST API와 REDIRECT URI를 활용하여 AuthorizationCode(인가코드) 발급받기

https://kauth.kakao.com/oauth/authorize?client_id=<REST API 키>
&redirect_uri=<Redirect URI>&response_type=code&scope=talk_message
을 시크릿창에서 입력하면

https://localhost.com/
?code=BjySlSWun-92ydFw_kQ5qsHvOTrYLsc-zCMVbgJVGlJ-_P2x_lNA0I8S524KKw0fAAABi9yEQFbC3p98Pd5TpQ
토큰이 발급된다.(code가 토큰 번호임)

1. 한 번의 인증 과정에서만 사용되어야 하며, 사용 후에는 무효화, 이는 보안상의 이유
2. 따라서 이를 기반으로 Access Token을 요청하고 사용하는 것이 일반적인 플로우


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
"""

# 카카오톡 활용하기
import json

KAKAO_TOKEN_FILENAME='res/kakao_token.json'
KAKAO_APP_KEY = 'REST API'
update_tokens(KAKAO_APP_KEY, KAKAO_TOKEN_FILENAME)

gaddr_url = 'https://search.naver.com/search.naver?query='+glocation + ' 맛집'
contents = []

template ={
    'object_type':'list',
    'header_title':gsummary + ' - 맛집추천',
    'header_link':{
        'web_url':gevent_url,
        'mobile_web_url':gevent_url
    },
    'contents':contents,
    'buttons':[
        {
            'title':'일정 자세히 보기',
            'link':{
                'web_url':gevent_url,
                'mobile_web_url':gevent_url
            }
        },
        {
            'title':'일정 장소 보기',
            'link':{
                'web_url':gaddr_url,
                'mobile_web_url':gaddr_url
            }
        }
    ],
}

for place in places:
    ntitle = place.get('title')
    ncategory = place.get('category')
    ntelephone = place.get('telephone')
    nlocation = place.get('address')

    query = nlocation + " "+ntitle

    if '카페' in ncategory:
        image_url = "https://freesvg.org/img/pitr_Coffee_cup_icon.png"
    else:
        image_url = "https://freesvg.org/img/bentolunch.png?2=150&h=150&fit=fill"

    if ntelephone:
        ntitle = ntitle + "\ntel)"+ntelephone

    content = {
        "title":"["+ncategory+"] "+ntitle,
        "description":' '.join(nlocation.split()[1:]),
        "image_url":image_url,
        "image_width":50, "image_height":50,
        "link":{
            "web_url":"https://search.naver.com/search.naver?query=" + query,
            "mobile_web_url":"https://search.naver.com/search.naver?query=" + query
        }
    }
    contents.append(content)

res = send_message(KAKAO_TOKEN_FILENAME, template)
if res.json().get('result_code') == 0:
    print("성공")
else:
    print("성공적으로 보내지 못했음.", res.json())


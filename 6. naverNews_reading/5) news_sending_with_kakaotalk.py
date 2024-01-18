"""
# =======================================================================
# =======================================================================
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

# =======================================================================
# =======================================================================
# 2 인가코드 발급받은 걸로 아래 내용 출력.
# access_token, token_type, refresh_token, expires_in, talk_message, refresh_token_expires_in
import requests

url = "https://kauth.kakao.com/oauth/token"

data = {
    "grant_type" : "AuthorizationCode",
    "client_id" : "<REST API 키>",
    "redirect_uri" : "https://localhost.com- 내가 정의한",
    "code" : "인가코드"    
}

response = requests.post(url, data=data)

# 요청에 실패했다면,
if response.status_code !=200:
    print("error! because ", response.json())
else: # 요청에 성공했다면,
    tokens = response.json()
    print(tokens)

# =======================================================================
# =======================================================================
# 3. 출력한 내용을 파일 형식으로 저장.
import requests
import json
import datetime
import os

# 카카오 토큰을 저장할 파일명
KAKAO_TOKEN_FILENAME = "C:/Users/moonw/py_life/res/kakao_token.json"

# 저장하는 함수
def save_tokens(filename, tokens):
    with open(filename, "w") as fp:
        json.dump(tokens, fp)
        
# 읽어오는 함수
def load_tokens(filename):
    with open(filename) as fp:
        tokens = json.load(fp)
        
    return tokens

def update_tokens(app_key, filename):
    tokens = load_tokens(filename)
    
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type" : "refresh_token",
        "client_id" : app_key,  
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
        new_tokens = response.json()
        tokens['access_token'] = new_tokens.get('access_token', tokens['access_token'])
        tokens['refresh_token'] = new_tokens.get('refresh_token', tokens['refresh_token'])
        save_tokens(filename, tokens)
        
    return tokens

def send_message(filename, template):
    tokens = load_tokens(filename)
    headers = {
        "Authorization": "Bearer " + tokens['access_token']  # 수정된 부분: 액세스 토큰을 헤더에 추가
    }
    payload = {
        "template_object": json.dumps(template)
    }
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    res = requests.post(url, data=payload, headers=headers)

    return res

# 토큰 저장
save_tokens(KAKAO_TOKEN_FILENAME, tokens)

# =======================================================================
# =======================================================================
# 4 이전 네이버 뉴스 크롤링 한 것.

import requests
from bs4 import BeautifulSoup
import bs4.element
import datetime

def get_soup_obj(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.151 Whale/3.14.134.62 Safari/537.36'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    return soup

def get_top3_news_info(sec, sid):
    default_img = "https://search.naver.com/search.naver?where=image&sm=tab_jum&query=naver#"

    sec_url = "https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=" + sid
    print("section url: ", sec_url)

    soup = get_soup_obj(sec_url)

    news_list3 = []
    lis3 = soup.find('ul', class_='type06_headline').find_all('li', limit=3)
    for li in lis3:
        news_info = {
            "title": li.img.attrs.get('alt') if li.img else li.a.text.replace('\n', "").replace('\t', '').replace(
                '\r', ''),
            "date": li.find(class_='date').text,
            "news_url": li.a.attrs.get('href'),
            "image_url": li.img.attrs.get('src') if li.img else default_img
        }
        news_list3.append(news_info)
    return news_list3

def get_news_contents(url):
    soup = get_soup_obj(url)
    
    body = soup.find('div', class_='newsct_article _article_body')

    news_contents = ''
    if body:
        for content in body.stripped_strings:
            if len(content) > 50:
                news_contents += content + ' '
    return news_contents

def get_naver_news_top3():
    news_dic = dict()
    sections = ['pol', 'eco', 'soc']
    section_ids = ['100', '101', '102']
    for sec, sid in zip(sections, section_ids):
        news_info = get_top3_news_info(sec, sid)
        for news in news_info:
            news_url = news['news_url']
            news_contents = get_news_contents(news_url)
            news['news_contents'] = news_contents
        news_dic[sec] = news_info
    return news_dic

news_dic = get_naver_news_top3()
print(news_dic['eco'][0])

# =======================================================================
# =======================================================================
# 4 이전 네이버 뉴스 크롤링 한 것 요약.

from summa import summarizer

# 뉴스 데이터 가져오기
news_dic = get_naver_news_top3()

# 섹션 지정
my_section = 'eco'
news_list3 = news_dic[my_section]

# 뉴스 요약하기
for news_info in news_list3:
    # words=20은 반환된 요약문에서 최소한 20개의 단어가 있어야 한다는 것을 의미
    # 이때는 요약하지 않고 본문에서 앞 3문장을 사용함.
    try:
        snews_contents = summarizer.summarize(news_info['news_contents'], words=20)
    except:
        snews_contents = None

    if not snews_contents:
        news_sentences = news_info['news_contents'].split('.')

        if len(news_sentences) > 3:
            snews_contents = '.'.join(news_sentences[:3])
        else:
            snews_contents = '.'.join(news_sentences)

    news_info['snews_contents'] = snews_contents

## 요약 결과 - 첫번째 뉴스
print("==== 첫번째 뉴스 원문 ====")
print(news_list3[0]['news_contents'])
print("\n==== 첫번째 뉴스 요약문 ====")
print(news_list3[0]['snews_contents'])
print()
## 요약 결과 - 두번째 뉴스
print("==== 두번째 뉴스 원문 ====")
print(news_list3[1]['news_contents'])
print("\n==== 두번째 뉴스 요약문 ====")
print(news_list3[1]['snews_contents'])

# =======================================================================
# =======================================================================
# 5 네이버 뉴스 크롤릭 요약 본 카톡으로 보내기

import json

KAKAO_TOKEN_FILENAME='C:/Users/moonw/py_life/res/kakao_token.json'
KAKAO_APP_KEY = 'REST API'
update_tokens(KAKAO_APP_KEY, KAKAO_TOKEN_FILENAME)

sections_ko = {'pol':'정치', 'eco':'경제','soc':'사회'}

navernews_url = "https://news.naver.com/main/home.nhn"
newsdatail_url = "https://www.daum.net/"

contents = []

template = {
    "object_type":"list",
    "header_title":sections_ko[my_section] + "분야 상위 뉴스 빅3",
    "header_link":{
        "web_url":navernews_url,
        "mobile_web_url":navernews_url
    },
    "contents":contents,
    "button_title":"네이버 뉴스 바로가기"
}

for news_info in news_list3:
    content = {
        "title":news_info.get('title'),
        "description":"작성일 : "+ news_info.get('date'),
        "image_url":news_info.get('image_url'),
        "image_width":50,
        "image_height":50,
        "link":{
            "web_url":news_info.get('news_url'),
            "mobile_web_url":news_info.get('news_url')
        }
    }
    contents.append(content)

res= send_message(KAKAO_TOKEN_FILENAME, template)


######################################################
# 위 코드 외에 텍스트 템플릿으로 보내는 코드

for ids, news_info in enumerate(news_list3):
    template = {
        "object_type":"text",
        "text":"#제목 :" + news_info.get('title')+'\n\n# 요약 : ' + news_info.get('snews_contents'),
        
        "link":{
            "web_url":news_info.get('news_url'),
            'mobile_web_url':news_info.get('news_url')
        },
        'button_title':'자세히 보기'
    }
   
    res = send_message(KAKAO_TOKEN_FILENAME, template)
    if res.json().get('result_code') == 0:
        print('뉴스를 성공적으로 보냈습니다.')
    else:
        print('뉴스를 성공적으로 보내지 못했습니다. 오류메시지 : ', res.json())

""" 
추가 사항

카카오 개발자 도메인에서 네이버 뉴스만을 추가하는게 아니라 n.news.naver.com을 추가해야지

상세 네이버 뉴스 페이지로 들어가짐.
"""
# 검색해보기

import requests

headers = {
    'X-Naver-Client-Id':'ClientID',
    'X-Naver-Client-Secret':'ClientSecret'
}

query='국민대 맛집'
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
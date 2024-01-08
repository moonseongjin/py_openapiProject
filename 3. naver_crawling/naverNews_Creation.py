""" 기존 네이버 영화 리뷰 댓글 크롤링 작업이지만, 
 네이버 영화가 현재시간으로 폐쇄되었기에 같은 방식으로 
 네이버 뉴스의 헤더부분을 읽는 크롤링 작업으로 창작함을 알림.
"""

import requests
from bs4 import BeautifulSoup

# 네이버 뉴스 링크
url = "https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=101&sid2=258"

# html 소스 가져오기
res = requests.get(url)

# html 파싱
soup = BeautifulSoup(res.text, 'lxml')

# 리뷰 리스트
ul = soup.find('ul', class_="type06_headline")
# class는 파이썬 예약어이므로 class_로 지정
lis = ul.find_all('li')

# 뉴스 제목 출력
count = 0
for li in lis: # 네이버 뉴스가 일부 이미지 포함하고 있어서 다음과 같이 작성
    count += 1 
    img_tag = li.find('img')
    if img_tag: # 이미지 있으면 이미지에 있는 alt의 내용 가져오기
        alt_text = img_tag.get('alt', '')
        print(f"[{count}th] {alt_text}")
    else: # 아닐경우 그냥 출력
        print(f"[{count}th] {li.a.string}")
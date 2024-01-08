import requests
from bs4 import BeautifulSoup
import bs4.element
import datetime

def get_soup_obj(url):
    headers = {'User-Agent' : '<복사한 user-agent 값 대체>'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    return soup

# 뉴스 이미지가 없는 뉴스가 있음. 임시 이미지로 다음을 세팅
# 임시 이미지는 네이버 로고
default_img = "https://search.naver.com/search.naver?where=image&sm=tab_jum&query=naver#"

# 100부터 107까지 반복 #107까지가 네이버 뉴스 끝
for sid in range(100, 108):
    # 해당 분야 상위 뉴스 목록 주소
    sec_url="https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1="+ str(sid)
    
    print("section url: ", sec_url)

    # 해당 분야 상위 뉴스 HTML 가져오기
    soup = get_soup_obj(sec_url)
    
    # 해당 분야 상위 뉴스 세 개 가져오기
    lis3 = soup.find('ul', class_='type06_headline').find_all('li', limit=3)
    for li in lis3:
        # title : 뉴스 제목, news_url : 뉴스, image_url : 이미지 url
        news_info = {
            "title": li.img.attrs.get('alt') if li.img else li.a.text.replace('\n', "").replace('\t','').replace('\r', ''),
            "date": li.find(class_='date').text,
            "news_url":li.a.attrs.get('href'),
            "image_url":li.img.attrs.get('src') if li.img else default_img
        }
        print(news_info)


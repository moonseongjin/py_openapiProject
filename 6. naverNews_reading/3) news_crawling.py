# 뉴스 크롤링 하기

import requests
from bs4 import BeautifulSoup

def get_soup_obj(url):
    headers = {'User-Agent' : '<복사한 user-agent 값 대체>'}
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
				# stripped_strings를 사용하면 텍스트가 불필요한 공백이나 
				# 개행 문자로 정리된 상태로 제공
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
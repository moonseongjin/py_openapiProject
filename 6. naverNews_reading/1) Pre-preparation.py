"""
pip install gensim BeautifulSoup4 lxml requests
--html 구조를 파싱하기 위해 BeautifulSoup4와 lxml 라이브러리 사용.

1. User-Agent 확인
2. 섹션별 접속 주소 확인
3. 상위 랭킹 세 개의 뉴스 메타 정보 확인
4. gensim으로 뉴스 요약하기

User-Agent 확인

https://vivoldi.com/tools/browser-useragent/
"""

# 해당 분야 상위 뉴스 HTML 가져오기

headers = {'User-Agent' : '<복사한 user-agent 값 대체>'}
# ex. 'User-Agent' :Mozilla/5.0 (Windows NT 10.0; Win64; x64)...

res = requests.get(news_link, headers =headers)
print(res.text)

# 각 분야별 접속 주소 구현
for sid in ['100', '101', '102']:
    # 해당 분야 상위 뉴스 목록 주소
    sec_url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=" + sid
    print("section url :", sec_url)


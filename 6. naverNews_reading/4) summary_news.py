# 뉴스 요약하기

# 섹션 지정
my_section = 'eco'

# 뉴스 데이터 가져오기(위 크롤링 한 내용)
news_list3 = news_dic[my_section]

# 뉴스 요약하기
for news_info in news_list3:

    # words=20은 반환된 요약문에서 최소한 20개의 단어가 있어야 한다는 것을 의미
    # 만약 문장 구성이 10이하라면, gensim의 sumarize()에서 오류를 return 실행이 멈춤. 
    # 따라서 try~execpt문으로 처리.
    try:
        snews_contents = summarizer.summarize(news_info['news_contents'], words=20)
    except:
        snews_contents = None

    # sumarize로 처리할 수 없을 경우 문장을 분리. 상위 세개의 문장을 사용.
    # 세개 문장 이하인 경우에는 전체 문장을 요약문으로 사용.(if len(news_sentences) > 3:)
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
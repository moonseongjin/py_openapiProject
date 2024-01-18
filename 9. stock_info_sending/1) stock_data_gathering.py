# 1. 주식 데이터 가져오기
import pandas as pd

def get_stock_code():
    # 종목코드 다운로드
    stock_code = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]
    
    # 필요없는 column들은 제외
    stock_code = stock_code[['회사명', '종목코드']]
    
    # 한글 컬럼명을 영어로 변경
    stock_code = stock_code.rename(columns={'회사명': 'company', '종목코드': 'code'})
    
    # 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌
    stock_code.code = stock_code.code.map('{:06d}'.format)
    
    return stock_code

stock_code = get_stock_code()
print(stock_code)

import pandas as pd
import requests
# frame.append 메소드 향후 버전의 pandas에서 더 이상 사용안됨. 
# 대신 pandas.concat 사용

# 2. 주식 데이터 틀로 가져오기
def get_stock(code):
    df_list = []
    for page in range(1, 21):
        # 일별 시세 url
        url = 'https://finance.naver.com/item/sise_day.nhn?code={code}&page={page}'.format(code=code, page=page)

        header = {'User-Agent': 'ㅇㅇㅇ'}

        res = requests.get(url, headers=header)
        
        # 테이블이 페이지에 존재하는지 확인
        tables = pd.read_html(res.text, header=0)
        if not tables:
            print(f"{page}페이지에서 테이블을 찾을 수 없습니다. 데이터 수집 중단.")
            break
        
        try:
            current_df = tables[0]
            df_list.append(current_df)
        except Exception as e:
            print(f"Error occurred on page {page}: {e}")

        df = pd.concat(df_list, ignore_index=True)
    return df

code = '005930'
df = get_stock(code)
print(df.head())
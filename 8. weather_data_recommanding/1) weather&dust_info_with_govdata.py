# 날씨 정보 가져오기
import requests
import json
import datetime

# 날씨 정보를 얻기 위한 request url
# 버전이 2.0으로 바뀜
vilage_weather_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?"

service_key = "동네예보조회의 인증키"
base_date = datetime.datetime.today().strftime("%Y%m%d")
base_time = "0800"
# 오전 8시
nx = "59"
ny = "126"

payload = "serviceKey="+service_key+"&"+"dataType=json"+"&" \
                                                        "base_date="+base_date +"&" \
                                                                                "base_time="+base_time+"&" \
                                                                                                       "nx="+nx+"&" \
                                                                                                                "ny="+ny
res = requests.get(vilage_weather_url + payload)
try:
    items = res.json().get('response').get('body').get('items')
    print(items)
except:
    print("날씨정보 요청 실패", res.text)



# 미세먼지 정보 가져오기
import requests
import json
import datetime

dust_url = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?"

service_key = "인증키"

payload = "serviceKey=" +service_key+"&" \
                                     "returnType=json"+"&" \
                                                       "sidoName=서울"+"&" \
                                                                     "ver=1.0"
"""
미세먼지는 직경에 따라 PM-10과 PM-2.5등으로 구분하며, 
PM-10은 1000분의 10mm보다 작은 먼지이며, 
PM-2.5는1000분의 2.5mm보다 작은 먼지

- 버전을 포함하지 않고 호출할 경우 : PM2.5 데이터가 포함되지 않은 원래 오퍼레이션 결과 표출.
- 버전 1.0을 호출할 경우 : PM2.5 데이터가 포함된 결과 표출.
- 버전 1.1을 호출할 경우 : PM10, PM2.5 24시간 예측이동 평균데이터가 포함된 결과 표출.
- 버전 1.2을 호출할 경우 : 측정망 정보 데이터가 포함된 결과 표출.
- 버전 1.3을 호출할 경우 : PM10, PM2.5 1시간 등급 자료가 포함된 결과 표출
- 버전 1.4을 호출할 경우 : 측정소 코드를 포함된 결과 표출
- 버전 1.5을 호출할 경우 : 측정값 소수점 아래 자리 수 확대 (CO : 1 → 2, O3/SO2/NO2 : 3 → 4)
""" 

res = requests.get(dust_url, payload)
result = res.json()
dust = dict()
if (res.status_code == 200) & (result['response']['header']['resultCode'] == '00'):
    dust['PM10'] = {'value':int(result['response']['body']['items'][0]['pm10Value'])}
    dust['PM2.5'] = {'value': int(result['response']['body']['items'][0]['pm25Value'])}
else:
    print("미세먼지 가져오기 실패 : ", result['response']['header']['resultMsg'])
print(dust)
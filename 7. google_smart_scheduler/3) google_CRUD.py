# 구글 CRUD

#==================================================================================
#==================================================================================
# 일정 생성(Insert) CREATE
event = {
        'summary': 'itsplay의 OpenAPI 수업', # 일정 제목
        'location': '서울특별시 성북구 정릉동 정릉로 77', # 일정 장소
        'description': 'itsplay와 OpenAPI 수업에 대한 설명입니다.', # 일정 설명
        'start': { # 시작 날짜
            'dateTime': today + 'T09:00:00', 
            'timeZone': 'Asia/Seoul',
        },
        'end': { # 종료 날짜
            'dateTime': today + 'T10:00:00', 
            'timeZone': 'Asia/Seoul',
        },
        'recurrence': [ # 반복 지정
            'RRULE:FREQ=DAILY;COUNT=2' # 일단위; 총 2번 반복
        ],
        'attendees': [ # 참석자
            {'email': 'lpage@example.com'},
            {'email': 'sbrin@example.com'},
        ],
        'reminders': { # 알림 설정
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60}, # 24 * 60분 = 하루 전 알림
                {'method': 'popup', 'minutes': 10}, # 10분 전 알림
            ],
        },
    }

# calendarId : 캘린더 ID. primary이 기본 값입니다.
event = service.events().insert(calendarId='primary', body=event).execute()
print('Event created: %s' % (event.get('htmlLink')))


#==================================================================================
#==================================================================================
# 일정 조회(Read)
import datetime

calendar_id = 'primary'
today = datetime.date.today().strftime("%Y-%m-%d")
time_min = today + 'T00:00:00+09:00'
time_max = today + 'T23:59:59+09:00'
max_results = 5
is_single_events = True
orderby = 'startTime'

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

#==================================================================================
#==================================================================================
# 일정 수정(Update)

event = events_result.get('items')[0]
event_id = event.get('id')

# 원하는 일정의 속성 값을 변경합니다.
event['summary'] = "(수정된)" + event['summary']

# 일정 수정 요청하기
updated_event = service.events().update(calendarId='primary', eventId=event_id, body=event).execute()


#==================================================================================
#==================================================================================
# 일정 삭제(Delete)
# 위에서 수정된 일정
updated_event

# eventId : 일정을 조회한 후 얻은 id 값을 말합니다.
eventId = updated_event.get('id')
service.events().delete(calendarId='primary', eventId=eventId).execute()
# 하루동안 전체종목의 데이터를 가져오기
# 필요한 컬럼만 가져오기
# 공휴일이나 주말에는 평일꺼를 가져오는 기능

import datetime
import pandas as pd
import openpyxl

class Today_Alldata_cls:
    
    def Itg_report(self):
        # nowDate = 현재날짜 ex) 20210929
        now = datetime.datetime.now()
        nowDate = now.strftime('%Y%m%d')
        
        # 요일 나타내기 weekDay = 요일
        # 월 = 0 ~ 일 = 6
        weekDay = datetime.datetime.today().weekday()
        
        # 토요일일 경우 -1, 일요일일 경우 -2를 실시하는 로직
        # 토요일, 일요일인 경우에는 주식이 개장하지 않으므로
        # 토요일에는 하루 전 데이터를, 일요일에는 이틀 전 데이터를 불러옴
        if weekDay == 5:
            nowDate = int(nowDate)
            nowDate = nowDate - 1
            nowDate = str(nowDate)
        elif weekDay == 6:
            nowDate = int(nowDate)
            nowDate = nowDate - 2
            nowDate = str(nowDate)
        else:
            pass
        
        # 주식 휴장일의 경우 -1을 해주기 - 1년에 한번씩 확인 후 업데이트해주기
        # 설날은 -2, 추석은 -2, -3 해주기
        Stock_Closing_Date = ["20210101", "20210211", "20210212", "20210505", "20210519", "20210816", "20210920", "20210921", "20210922", "20211004", "20211011", "20211231"]
        if nowDate in Stock_Closing_Date: 
            nowDate = int(nowDate)
            nowDate = nowDate - 1
            nowDate = str(nowDate)
            # -2를 해줘야 하는 들
            if nowDate == "20210212" or "20210921":
                nowDate = int(nowDate)
                nowDate = nowDate - 1
                nowDate = str(nowDate)
            # -3을 해줘야 하는 날들
            if nowDate == "20210922":
                nowDate = int(nowDate)
                nowDate = nowDate - 1
                nowDate = str(nowDate)  
        else: 
            pass
        
        # 데이터 테스트(1) - 임의변수지정
        nowDate = "20210622"
        
        # 오늘 csv파일 가져오기
        try:
            # 데이터 불러오기
            itg_csv_basicdata = pd.read_csv("F:/JusikData/oneday_csv/alldata/" + nowDate + ".csv", encoding='cp949')
            
            # 종목코드에 대괄호 넣기
            itg_csv_basicdata['종목코드'] = '[' + itg_csv_basicdata['종목코드'] + ']'
            
            # 데이터 테스트(2)
            #print(itg_csv_basicdata.columns)
            #print(itg_csv_basicdata)
            
            # 결과값 리턴
            return itg_csv_basicdata
        except:
            print('당일 날짜에 해당하는 파일을 다운로드 받아주세요.')
        #######################

# 실행 테스트
#conn = Report_Integrated()
#conn.Itg_report()
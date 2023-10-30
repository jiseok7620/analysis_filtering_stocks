import pandas as pd
import openpyxl
import os
import win32com.client
import pythoncom
import time

class ebestapi_t1927_cls:
    # 쿼리 상태 초기화
    query_state = 0

    # 데이터 받으면 해당 이벤트로 이동
    def OnReceiveData(self, code):
        ebestapi_t1927_cls.query_state = 1
        print(code, ' : t1927 데이터 수신 완료')
        
    # 실행 시 메세지 및 에러 받음
    def OnReceiveMessage(self, err, msgco, msg):
        print('t1927 에러발생 : ', err)
        print('t1927 메세지 : ', msg)

class t1927_cls:
    def exe_t1927(self, shcode, edate):
        # 쿼리 객체 생성
        object_t1927 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", ebestapi_t1927_cls)
        
        # Res 파일 등록
        object_t1927.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t1927.res"
        
        # InBlock에 값 설정
        object_t1927.SetFieldData("t1927InBlock", "shcode", 0, shcode)
        object_t1927.SetFieldData("t1927InBlock", "date", 0, "")
        object_t1927.SetFieldData("t1927InBlock", "sdate", 0, "")
        object_t1927.SetFieldData("t1927InBlock", "edate", 0, edate)
        
        # 데이터 요청
        object_t1927.Request(False)
        
        # 10분내 요청한 요청 횟수 취득
        count_limit = object_t1927.GetTRCountLimit("t1927")
        count_request = object_t1927.GetTRCountRequest("t1927")
        print('t1927 10분 당 제한 건수 : ', count_limit)
        print('t1927 10분 내 요청 횟수 : ', count_request)
        
        # 수신 대기
        while ebestapi_t1927_cls.query_state == 0:
            pythoncom.PumpWaitingMessages()
        
        # 연속조회시 개수 가져오기 => 연속 시 1을 붙여줌
        count = object_t1927.GetBlockCount("t1927OutBlock1")
        print('t1927 가져올 데이터의 수 : ',count)
        
        arr_date = [] # 일자
        arr_amt0000 = [] # 공매도수량
        arr_amt0001 = [] # 공매도대금
        arr_amt0002 = [] # 공매도거래비중
        arr_amt0003 = [] # 평균공매도단가
        
        # 필요한 필드 가져오기
        for i in range(count):
            date = object_t1927.GetFieldData("t1927OutBlock1", "date", i)
            gm_vo = object_t1927.GetFieldData("t1927OutBlock1", "gm_vo", i)
            gm_va = object_t1927.GetFieldData("t1927OutBlock1", "gm_va", i)
            gm_per = object_t1927.GetFieldData("t1927OutBlock1", "gm_per", i)
            gm_avg = object_t1927.GetFieldData("t1927OutBlock1", "gm_avg", i)
            
            arr_date.append(date)
            arr_amt0000.append(gm_vo)
            arr_amt0001.append(gm_va)
            arr_amt0002.append(gm_per)
            arr_amt0003.append(gm_avg)
            
        # 데이터 프레임으로 만들기
        data = pd.DataFrame({'일자' : arr_date, '공매도수량' : arr_amt0000, '공매도대금' : arr_amt0001, 
                             '공매도거래비중' : arr_amt0002, '평균공매도단가' : arr_amt0003
                             })
        
        # 인덱스 0 값 지우고, 인덱스 초기화하기
        # 0          일자      0      0      0      0         0  요런값이 나오기 때문에
        #data = data.drop(index=0, axis=0)
        #data.reset_index(drop=True, inplace=True)
        
        # 데이터프레임 리턴하기
        return data
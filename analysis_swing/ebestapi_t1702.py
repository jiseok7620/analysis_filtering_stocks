import pandas as pd
import openpyxl
import os
import win32com.client
import pythoncom
import time
from Invest.analysis_swing.ebestapi_login import login_cls

class ebestapi_t1702_cls:
    # 쿼리 상태 초기화
    query_state = 0

    # 데이터 받으면 해당 이벤트로 이동
    def OnReceiveData(self, code):
        ebestapi_t1702_cls.query_state = 1
        print(code, ' : t1702 데이터 수신 완료')
        
    # 실행 시 메세지 및 에러 받음
    def OnReceiveMessage(self, err, msgco, msg):
        print('t1702 에러발생 : ', err)
        print('t1702 메세지 : ', msg)

class t1702_cls:
    def exe_t1702(self, shcode, edate, sb):
        # 서버연결, 로그인
        login_cls.exe_login(self)
        
        # 쿼리 객체 생성
        object_t1702 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", ebestapi_t1702_cls)
        
        # Res 파일 등록
        object_t1702.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t1702.res"

        how = False
        cts_date = ""

        for i in range(2):
            # 쿼리 상태 초기화 
            ebestapi_t1702_cls.query_state = 0
            
            # InBlock에 값 설정
            object_t1702.SetFieldData("t1702InBlock", "shcode", 0, shcode)
            object_t1702.SetFieldData("t1702InBlock", "todt", 0, edate)
            object_t1702.SetFieldData("t1702InBlock", "volvalgb", 0, "1")
            object_t1702.SetFieldData("t1702InBlock", "msmdgb", 0, sb) # 0:순매수, 1:매수, 2:매도
            object_t1702.SetFieldData("t1702InBlock", "cumulgb", 0, "0")
            object_t1702.SetFieldData("t1702InBlock", "cts_date", 0, cts_date)
                
            # 데이터 요청
            aa = object_t1702.Request(how) # True : 연속데이터 조회로 요청
            
            # 수신 대기
            while ebestapi_t1702_cls.query_state == 0:
                pythoncom.PumpWaitingMessages()
                
            # 연속조회 OutBlock값
            cts_date = object_t1702.GetFieldData("t1702OutBlock", "cts_date", 0)
            how = True
            
            # 연속조회시 개수 가져오기 => 연속 시 1을 붙여줌
            count = object_t1702.GetBlockCount("t1702OutBlock1")
            print('t1702 가져올 데이터의 수 : ',count)
        
            arr_date = []
            arr_amt0000 = [] # 사모펀드
            arr_amt0001 = [] # 증권
            arr_amt0002 = [] # 보험
            arr_amt0003 = [] # 투신
            arr_amt0004 = [] # 은행
            arr_amt0005 = [] # 종금
            arr_amt0006 = [] # 기금
            arr_amt0007 = [] # 기타법인
            arr_amt0008 = [] # 개인
            arr_amt0009 = [] # 등록외국인
            arr_amt0010 = [] # 미등록외국인
            arr_amt0011 = [] # 국가외
            arr_amt0018 = [] # 기관
            arr_amt0088 = [] # 외인계(등록+미등록)
            arr_amt0099 = [] # 기타계(기타+국가)
            
            # 필요한 필드 가져오기
            for i in range(count):
                date = object_t1702.GetFieldData("t1702OutBlock1", "date", i)
                amt0000 = object_t1702.GetFieldData("t1702OutBlock1", "amt0000", i)
                amt0001 = object_t1702.GetFieldData("t1702OutBlock1", "amt0001", i)
                amt0002 = object_t1702.GetFieldData("t1702OutBlock1", "amt0002", i)
                amt0003 = object_t1702.GetFieldData("t1702OutBlock1", "amt0003", i)
                amt0004 = object_t1702.GetFieldData("t1702OutBlock1", "amt0004", i)
                amt0005 = object_t1702.GetFieldData("t1702OutBlock1", "amt0005", i)
                amt0006 = object_t1702.GetFieldData("t1702OutBlock1", "amt0006", i)
                amt0007 = object_t1702.GetFieldData("t1702OutBlock1", "amt0007", i)
                amt0008 = object_t1702.GetFieldData("t1702OutBlock1", "amt0008", i)
                amt0009 = object_t1702.GetFieldData("t1702OutBlock1", "amt0009", i)
                amt0010 = object_t1702.GetFieldData("t1702OutBlock1", "amt0010", i)
                amt0011 = object_t1702.GetFieldData("t1702OutBlock1", "amt0011", i)
                amt0018 = object_t1702.GetFieldData("t1702OutBlock1", "amt0018", i)
                amt0088 = object_t1702.GetFieldData("t1702OutBlock1", "amt0088", i)
                amt0099 = object_t1702.GetFieldData("t1702OutBlock1", "amt0099", i)
                
                arr_date.append(date)
                arr_amt0000.append(amt0000)
                arr_amt0001.append(amt0001)
                arr_amt0002.append(amt0002)
                arr_amt0003.append(amt0003)
                arr_amt0004.append(amt0004)
                arr_amt0005.append(amt0005)
                arr_amt0006.append(amt0006)
                arr_amt0007.append(amt0007)
                arr_amt0008.append(amt0008)
                arr_amt0009.append(amt0009)
                arr_amt0010.append(amt0010)
                arr_amt0011.append(amt0011)
                arr_amt0018.append(amt0018)
                arr_amt0088.append(amt0088)
                arr_amt0099.append(amt0099)
                
            # 데이터 프레임으로 만들기
            data = pd.DataFrame({'일자' : arr_date, '사모펀드' : arr_amt0000, '증권' : arr_amt0001, '보험' : arr_amt0002, '투신' : arr_amt0003, '은행' : arr_amt0004,
                                 '종금' : arr_amt0005, '기금' : arr_amt0006, '기타법인' : arr_amt0007, '개인' : arr_amt0008, '등록외국인' : arr_amt0009, 
                                 '미등록외국인' : arr_amt0010, '국가외'  : arr_amt0011, '기관' : arr_amt0018, '외인계(등록+미등록)' : arr_amt0088, '기타계(기타+국가)' : arr_amt0099                            
                                 })
            
            print(data)
        
        # 데이터프레임 리턴하기
        #return data
    
    
    
conn = t1702_cls()
conn.exe_t1702("005930", "20201216", "1")
        

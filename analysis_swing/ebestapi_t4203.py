import pandas as pd
import openpyxl
import os
import win32com.client
import pythoncom
import time

class ebestapi_t4203_cls:
    # 쿼리 상태 초기화
    query_state = 0

    # 데이터 받으면 해당 이벤트로 이동
    def OnReceiveData(self, code):
        ebestapi_t4203_cls.query_state = 1
        print(code, ' : t4203 데이터 수신 완료')
        
    # 실행 시 메세지 및 에러 받음
    def OnReceiveMessage(self, err, msgco, msg):
        print('t4203 에러발생 : ', err)
        print('t4203 메세지 : ', msg)

class t4203_cls:
    def exe_t4203(self, shcode, edate):
        ## 업종구분 파일이 없으면 만들기
        if os.path.isfile('F:/JusikData/API/업종구분/업종구분.xlsx'):
            pass
        else:
            ## 전체 업종 구분 csv로 저장하기 
            object_t8424 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", ebestapi_t4203_cls)
            
            # Res 파일 등록
            object_t8424.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t8424.res"
            
            # InBlock에 값 설정
            object_t8424.SetFieldData("t8424InBlock", "gubun1", 0, "")
            
            # 데이터 요청
            object_t8424.Request(False)
            
            # 수신 대기
            while ebestapi_t4203_cls.query_state == 0:
                pythoncom.PumpWaitingMessages()
                
            # 연속조회시 개수
            count = object_t8424.GetBlockCount("t8424OutBlock")
            
            arr_hname = []
            arr_upcode = []
            # 필요한 필드 가져오기
            for i in range(count):
                hname = object_t8424.GetFieldData("t8424OutBlock", "hname", i)
                upcode = object_t8424.GetFieldData("t8424OutBlock", "upcode", i)
                arr_hname.append(hname)
                arr_upcode.append(upcode)
                
            # 데이터 프레임으로 만들기
            data_up = pd.DataFrame({'업종명' : arr_hname, '업종코드' : arr_upcode})
            data_up['업종명'] = data_up['업종명'].str.replace(' ', '') # 공백 지우기
            
            # 데이터 프레임 엑셀로 저장
            data_up.to_excel('F:/JusikData/API/업종구분/업종구분.xlsx', sheet_name='sheet1', encoding='cp949', index=False)
        
        ##---------------------------------------------------------------------------------------##
        # 해당 종목의 업종 명 가져오기
        data1 = pd.read_csv("F:/JusikData/API/업종/kosdaq.csv", encoding='cp949')
        up_name = data1[data1["종목코드"] == shcode]["업종명"].values[0]
        print('업종명 : ',up_name)
        
        # 해당 업종 명의 업종코드 가져오기
        data_upjong = pd.read_excel('F:/JusikData/API/업종구분/업종구분.xlsx', engine='openpyxl')
        up_code = data_upjong[data_upjong["업종명"] == up_name]["업종코드"].values[0]
        print('업종코드 : ' ,up_code)
        
        if len(str(up_code)) == 1:
            up_code = "00" + str(up_code)
        elif len(str(up_code)) == 2:
            up_code = "0" + str(up_code)
            
        #----------------------------------------------------------------------------------------##
        # 쿼리 객체 생성
        object_t4203 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", ebestapi_t4203_cls)
        
        # Res 파일 등록
        object_t4203.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t4203.res"
        
        # InBlock에 값 설정
        object_t4203.SetFieldData("t4203InBlock", "shcode", 0, str(up_code))
        object_t4203.SetFieldData("t4203InBlock", "gubun", 0, "2")
        object_t4203.SetFieldData("t4203InBlock", "qrycnt", 0, "500")
        object_t4203.SetFieldData("t4203InBlock", "edate", 0, edate)
        
        # 데이터 요청
        object_t4203.Request(False)
        
        # 10분내 요청한 요청 횟수 취득
        count_limit = object_t4203.GetTRCountLimit("t4203")
        count_request = object_t4203.GetTRCountRequest("t4203")
        print('t4203 10분 당 제한 건수 : ', count_limit)
        print('t4203 10분 내 요청 횟수 : ', count_request)
        
        # 수신 대기
        while ebestapi_t4203_cls.query_state == 0:
            pythoncom.PumpWaitingMessages()
        
        # 연속조회시 개수 가져오기 => 연속 시 1을 붙여줌
        count = object_t4203.GetBlockCount("t4203OutBlock1")
        print('t4203 가져올 데이터의 수 : ',count)
        
        arr_date = []
        arr_open = []
        arr_high = []
        arr_low = []
        arr_close = []
        arr_jdiff_vol = []
        arr_value = []
        # 필요한 필드 가져오기
        for i in range(count):
            date = object_t4203.GetFieldData("t4203OutBlock1", "date", i)
            open = object_t4203.GetFieldData("t4203OutBlock1", "open", i)
            high = object_t4203.GetFieldData("t4203OutBlock1", "high", i)
            low = object_t4203.GetFieldData("t4203OutBlock1", "low", i)            
            close = object_t4203.GetFieldData("t4203OutBlock1", "close", i)
            volume = object_t4203.GetFieldData("t4203OutBlock1", "jdiff_vol", i)
            value = object_t4203.GetFieldData("t4203OutBlock1", "value", i)
            arr_date.append(date)
            arr_open.append(open)
            arr_high.append(high)
            arr_low.append(low)
            arr_close.append(close)
            arr_jdiff_vol.append(volume)
            arr_value.append(value)
            
        # 데이터 프레임으로 만들기
        data = pd.DataFrame({'일자' : arr_date, '시가' : arr_open, '고가' : arr_high,
                             '저가' : arr_low, '종가' : arr_close, '거래량' : arr_jdiff_vol,
                             '거래대금' : arr_value
                             })
        
        # 인덱스 0 값 지우고, 인덱스 초기화하기
        # 0          일자      0      0      0      0         0  요런값이 나오기 때문에
        #data = data.drop(index=0, axis=0)
        #data.reset_index(drop=True, inplace=True)
        
        # 데이터프레임 리턴하기
        return data
        
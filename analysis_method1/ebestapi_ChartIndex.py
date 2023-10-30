import pandas as pd
import openpyxl
import os
import win32com.client
import pythoncom
import time
from Invest.analysis_method1.ebestapi_login import ebestapi_login_cls

class ebestapi_ChartIndex_cls:
    # 쿼리 상태 초기화
    query_state = 0

    # 데이터 받으면 해당 이벤트로 이동
    def OnReceiveData(self, code):
        ebestapi_ChartIndex_cls.query_state = 1
        print(code, ' : 데이터 수신 완료')
        
    # 실행 시 메세지 및 에러 받음
    def OnReceiveMessage(self, err, msgco, msg):
        print('에러발생 : ', err)
        print('메세지 : ', msg)


# 쿼리 객체 생성
object_ChartIndex = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", ebestapi_ChartIndex_cls)

# Res 파일 등록
object_ChartIndex.ResFileName = "C:\\eBEST\\xingAPI\\Res\\ChartIndex.res"
#object_t4201.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\t4201.res")

# InBlock에 값 설정
object_ChartIndex.SetFieldData("ChartIndexInBlock", "indexname", 0, "")
object_ChartIndex.SetFieldData("ChartIndexInBlock", "market", 0, "1")
object_ChartIndex.SetFieldData("ChartIndexInBlock", "period", 0, "2")
object_ChartIndex.SetFieldData("ChartIndexInBlock", "shcode", 0, "005930")
object_ChartIndex.SetFieldData("ChartIndexInBlock", "qrycnt", 0, "100")
object_ChartIndex.SetFieldData("ChartIndexInBlock", "ncnt", 0, "")
object_ChartIndex.SetFieldData("ChartIndexInBlock", "sdate", 0, "20180401")
object_ChartIndex.SetFieldData("ChartIndexInBlock", "edate", 0, "20180601")
object_ChartIndex.SetFieldData("ChartIndexInBlock", "Isamend", 0, "1")
object_ChartIndex.SetFieldData("ChartIndexInBlock", "Isgab", 0, "0")
object_ChartIndex.SetFieldData("ChartIndexInBlock", "IsReal", 0, "0")

# 데이터 요청
#object_ChartIndex.Request(False)
# 차트인덱스는 RequestService로 요청해야함
object_ChartIndex.RequestService("ChartIndex", 0)

# 수신 대기
while ebestapi_ChartIndex_cls.query_state == 0:
    pythoncom.PumpWaitingMessages()

# 연속조회시 개수 가져오기 => 연속 시 1을 붙여줌
count = object_ChartIndex.GetBlockCount("ChartIndexOutBlock1")
print(count)

arr_date = []
arr_close = []
arr_trade = []
# 필요한 필드 가져오기
for i in range(count):
    date = object_ChartIndex.GetFieldData("ChartIndexOutBlock1", "date", i)
    close = object_ChartIndex.GetFieldData("ChartIndexOutBlock1", "close", i)
    trade = object_ChartIndex.GetFieldData("ChartIndexOutBlock1", "volume", i)
    arr_date.append(date)
    arr_close.append(close)
    arr_trade.append(trade)
    
# 데이터 프레임으로 만들기
data = pd.DataFrame({'일자' : arr_date, '종가' : arr_close, '거래량' : arr_trade})
print(data)

# 데이터프레임 리턴하기
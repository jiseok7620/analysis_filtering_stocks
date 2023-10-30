import pandas as pd
import openpyxl
import os
import win32com.client
import pythoncom
import time
from Invest.analysis_method1.ebestapi_login import ebestapi_login_cls

class ebestapi_t4201_cls:
    # 쿼리 상태 초기화
    query_state = 0

    # 데이터 받으면 해당 이벤트로 이동
    def OnReceiveData(self, code):
        ebestapi_t4201_cls.query_state = 1
        print(code, ' : 데이터 수신 완료')
        
    # 실행 시 메세지 및 에러 받음
    def OnReceiveMessage(self, err, msgco, msg):
        print('에러발생 : ', err)
        print('메세지 : ', msg)

# 엑셀 파일 만들기
if not os.path.isfile('F:/JusikData/API/ebest/test2.xlsx') :
    wb = openpyxl.Workbook()
    wb.active.title = "종목정보"
    new_excelfile = 'F:/JusikData/API/ebest/test2.xlsx'
    wb.save(new_excelfile)
    wb.close()

# 쿼리 객체 생성
object_t4201 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", ebestapi_t4201_cls)

# Res 파일 등록
object_t4201.ResFileName = "C:\\eBEST\\xingAPI\\Res\\t4201.res"
#object_t4201.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\t4201.res")

# InBlock에 값 설정
object_t4201.SetFieldData("t4201InBlock", "shcode", 0, "005930")
object_t4201.SetFieldData("t4201InBlock", "gubun", 0, "2")
object_t4201.SetFieldData("t4201InBlock", "qrycnt", 0, "500")
object_t4201.SetFieldData("t4201InBlock", "edate", 0, "20211223")

# 데이터 요청
object_t4201.Request(False)

# 수신 대기
while ebestapi_t4201_cls.query_state == 0:
    pythoncom.PumpWaitingMessages()

# 연속조회시 개수 가져오기 => 연속 시 1을 붙여줌
count = object_t4201.GetBlockCount("t4201OutBlock1")
print(count)

arr_date = []
arr_start = []
arr_close = []
# 필요한 필드 가져오기
for i in range(count):
    date = object_t4201.GetFieldData("t4201OutBlock1","date", i)
    close = object_t4201.GetFieldData("t4201OutBlock1","close", i)
    arr_date.append(date)
    arr_close.append(close)
    
# 데이터 프레임으로 만들기
data = pd.DataFrame({'일자' : arr_date, '종가' : arr_close})
print(data)

# 다른 데이터 가져와서 병합하기



# 추가할 엑셀 열기
excel_in = openpyxl.load_workbook('F:/JusikData/API/ebest/test2.xlsx')
sheet = excel_in.active
        
# 추가하기 => 리스트화해서 추가해야함
for i in range(len(data)):
    sheet.append(data.iloc[i].tolist())

# 저장하기
excel_in.save('F:/JusikData/API/ebest/test2.xlsx')
excel_in.close()

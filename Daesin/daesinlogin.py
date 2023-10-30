import win32com.client
#from pywinauto import application # pip install pywinauto
import os    
import locale
import time
locale.setlocale(locale.LC_ALL, 'ko_KR')
    
class Login_Daesin:
    # Check conenction
    def __init__(self):
        # instCpStockCode = 대신증권과 연결
        self.instCpStockCode = win32com.client.Dispatch('CpUtil.CpCybos')
    
    # 대신API로그인 화면 띄우기
    def connect(self): 
            print('여기는 daesinlogin 모듈')
            app = application.Application()
            # cybos plus를 정보 조회로만 사용했기 때문에 인증서 비밀번호는 입력하지 않았다. 
            app.start('C:\DAISHIN\STARTER\\ncStarter.exe')
            
    # 로그인 상태 조회
    def connect_state(self):
        if self.instCpStockCode.IsConnect == 1 :
            return "Connect"
        else:
            return "Disconnect"
            
    '''
    # 기존 CYBOS 프로세스 강제종료
    def kill_client(self): 
        print("########## 기존 CYBOS 프로세스 강제 종료") 
        os.system('taskkill /IM ncStarter* /F /T') 
        os.system('taskkill /IM CpStart* /F /T') 
        os.system('taskkill /IM DibServer* /F /T') 
        os.system('wmic process where "name like \'%ncStarter%\'" call terminate') 
        os.system('wmic process where "name like \'%CpStart%\'" call terminate') 
        os.system('wmic process where "name like \'%DibServer%\'" call terminate')
    '''

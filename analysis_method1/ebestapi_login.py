import win32com.client
import pythoncom
import time

class ebestapi_login_cls:
    login_state = 0

    def OnLogin(self, code, msg): # OnLogin으로 써야만 code, msg 정보를 리턴받을 수 있음
        if code == "0000":
            print(msg)
            ebestapi_login_cls.login_state = 1
        else:
            print(msg)
                
    def OnDisconnect(self):
        print('서버와 연결이 끊겼습니다.')
        
    def OnLogout(self):
        print('로그아웃 되었습니다.')
            
# 객체 생성하기
instXASession = win32com.client.DispatchWithEvents("XA_Session.XASession", ebestapi_login_cls)

# 연결 끊기
instXASession.DisconnectServer()

# 로그인 정보
id = ""
passwd = ""
cert_passwd = ""

# 로그인 서비 및 로그인
instXASession.ConnectServer("hts.ebestsec.co.kr", 20001)
blogin = instXASession.Login(id, passwd, cert_passwd, 0, 0) # 로그인 서버에 전송

# 수신(응답) 대기
while ebestapi_login_cls.login_state == 0:
    pythoncom.PumpWaitingMessages()

import sys
import pandas as pd
import os
import datetime
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *

## 대신, 이베스트 import ##
from Ebest.ebestlogin import *
from Daesin.daesinlogin import *

## screen1 import ##
from screen1.make_folder_alldata import *
from screen1.report_make import *
from screen1.report_roi import *
from screen1.today_alldata import *

## screen2 import ##
from screen2.debt_ratio import *
from screen2.hyengum_flow import *
from screen2.publish_jusik import *
from screen2.trade_receivable import *
from win32comext.shell.shellcon import ASSOCF_REMAPRUNDLL

form_class = uic.loadUiType("main.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #### 년도와 분기 자동 입력 ####
        # nowDate = 현재년도 ex) 2021
        now = datetime.datetime.now()
        nowDate = now.strftime('%Y%m%d')
        
        # 연도 변수 선언
        year = nowDate[0:4]
        
        # 일자 변수 선언
        day = nowDate[4:8]
        
        # 요일 나타내기 weekDay = 요일
        # 월 = 0 ~ 일 = 6
        dow = datetime.datetime.today().weekday()
        
        # 분기 계산하기 후 분기 변수 선언
        # 분기보고서 제출기한(1분기 : 1~3월, 3분기 : 7월~9월) = 분기 종료일로 부터 45일 이내
        # - 1분기 : 5월 15일
        # - 3분기 : 11월 15일
        # 반기보고서 제출기한(반기 : 1~6월) = 반기 종료일부터 45일 이내 
        # - 반기 : 8월 15일
        # 사업보고서 제출기한(1년 : 1월~12월) = 종료일 부터 90일 이내
        # - 사업 : 다음해 3월 31일까지
        # 4분기 : 3/31~5/15, 1분기 : 5/15~8/15, 2분기 : 8/15~11/15, 3분기 : 11/15~3/31
        if 331 <= int(nowDate[4:8]) < 515 :
            quarter = '4'
        elif 515 <= int(nowDate[4:8]) < 815:
            quarter = '1'
        elif 815 <= int(nowDate[4:8]) < 1115:
            quarter = '2'
        else:
            quarter = '3'
        
        # Line에 텍스트 넣기    
        self.Var_Year.setText(year)
        self.Var_Day.setText(day)
        self.Var_Quarter.setText(quarter)
        self.Var_Dow.setText(str(dow))
        ################################################################################
        #
        #
        #
        #
        #### 링크 연결 ####
        # https://opendart.fss.or.kr/disclosureinfo/fnltt/dwld/main.do = 사업보고서 다운로드 링크
        # 텍스트 (라벨)에 링크 추가하기
        self.Link_Dart.setText('<a href="https://opendart.fss.or.kr/disclosureinfo/fnltt/dwld/main.do">DART 공시 다운</a>')
        self.Link_Dart.setOpenExternalLinks(True)
        
        # http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020101 = 하루 종목 시세 다운로드 링크
        # 텍스트 (라벨)에 링크 추가하기
        self.Link_Krx.setText('<a href="http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020101">KRX 시세 다운</a>')
        self.Link_Krx.setOpenExternalLinks(True)
        ################################################################################
        #
        #
        #
        #
        ##### 다른 모듈의 객체 생성 모음 #####
        # daesinlogin.py를 연결하고 그 객체를 conn4으로 저장
        #self.Object_Login_Daesin = Login_Daesin()
        # ebestlogin.py를 연결하고 그 객체를 conn5으로 저장
        self.Object_Login_Ebest = Login_Ebest()
        # 이베스트의 로그인 상태 확인 클래스(XASessionEvents)의 객체 생성
        self.Object_XASessionEvents = XASessionEvents()
        # 화면1의 폴더에 하루데이터를 읽어서 등록하는 모듈의 객체 생성
        self.Object_make_folder_alldata_cls = make_folder_alldata_cls()
        # 화면1의 재무제표 상 필요한 데이터를 추출하여 csv로 만드는 모듈의 객체 생성
        self.Object_report_cls = report_cls()
        # 화면1의 증가율을 계산하여 csv로 만드는 모듈의 객체 생성
        self.Object_Report_Roi = Report_Roi()
        # 화면1의 하루 데이터 중 필요한 데이터를 가져오는 객체 생성
        self.Object_Today_Alldata_cls = Today_Alldata_cls()
        # 화면2의 부채비율 객체 형성
        self.Object_debt_ratio_cls = debt_ratio_cls()
        # 화면2의 현금흐름, 투자흐름, 재무흐름 객체 형성
        self.Object_hyen_flow_cls = hyen_flow_cls()
        # 화면2의 발행주식수 객체 형성
        self.Object_publish_jusik_cls = publish_jusik_cls()
        # 화면2의 매출채권회전율 객체 형성
        self.Object_trade_receivable_cls = trade_receivable_cls()
        ################################################################################
        #
        #
        #
        #
        ##### 버튼 클릭 시 함수와 연결 모음 #####
        # 대신로그인 버튼 클릭
        self.Btn_Login_Daesin.clicked.connect(self.Login_Daesin_clicked)
        # 이베스트로그인 버튼 클릭
        self.Btn_Login_Ebest.clicked.connect(self.Login_Ebest_clicked)
        # 연결상태확인 버튼 클릭 시
        self.Btn_Login_State.clicked.connect(self.Conn_State_clicked)
        # 1. 각종목폴더에데이터추가 버튼 클릭 시
        self.Btn_Make_Alldata.clicked.connect(self.Btn_Make_Alldata_clicked)
        # 2. 재무제표만들기 버튼 클릭 시
        self.Btn_Make_Jaemu.clicked.connect(self.Btn_Make_Jaemu_clicked)
        # 3. 증가율만들기 버튼 클릭 시
        self.Btn_Make_Roi.clicked.connect(self.Btn_Make_Roi_clicked)
        # 화면1에서 전체종목조회버튼 클릭 시
        self.Btn_Search_All.clicked.connect(self.Btn_Search_All_clicked)
        # 화면1에서 종목조회버튼 클릭 시
        self.Btn_Search_One.clicked.connect(self.Btn_Search_One_clicked)
        # 화면2에서 조회버튼 클릭 시
        self.Btn_Search_Del.clicked.connect(self.Btn_Search_Del_clicked)
        ################################################################################
        #
        #
        #
        #
        #### 테이블안의 셀 조작 ####
        # 화면1에서 셀의 내용 클릭 시
        self.Table_One.cellDoubleClicked.connect(self.Screen1_Cell_Double_Clicked)
        ################################################################################
        #
        #
        #
        #
        ##### 프로그램 시작 시 증권사와 연결 시에만 그 증권사의 기능버튼을 활성화#####
        # 대신증권과 연결되면 label_4에 연결되었습니다! 표시, 연결되면 버튼이 활성화 #
        #if self.Line_conn2.text() == "Disconnect" :
            #self.pushButton_3.setEnabled(False)
        #elif self.Line_conn2.text() == "Connect" :
            #self.pushButton_3.setEnabled(True)
        #else :
            #self.pushButton_3.setEnabled(False)
        ################################################################################
        #
        #
        #
        #
    ####################################################################################
    #### 셀 조작 함수 ####
    def Screen1_Cell_Double_Clicked(self):
        # 더블클릭한 곳의 행, 열 번호 조회
        row = self.Table_One.currentRow()
        col = self.Table_One.currentColumn()
        
        # 해당 행과 열의 값을 객체 형태로 가져오기
        result = self.Table_One.item(row, col)
        
        # 해당 셀의 내용을 변수로 저장하고 괄호 빼기
        aa = result.text()
        aa = aa.lstrip('[')
        aa = aa.rstrip(']')
        
        # 해당 셀의 내용을 조회 라인에 입력
        self.Line_Search.setText(aa)
    ################################################################################
    #
    #
    #
    #
    #### 버튼클릭시 함수 모음 ####
    # 대신로그인 버튼 클릭시 이벤트
    def Login_Daesin_clicked(self):
        self.Object_Login_Daesin.connect()
    
    # 이베스트로그인 버튼 클릭시 이벤트
    def Login_Ebest_clicked(self):
        self.Object_Login_Ebest.Login()
    
    # 연결상태확인 버튼 클릭 시 이벤트
    def Conn_State_clicked(self):
        # 대신증권 연결 상태를 Line_conn2 라인에디트에 표시
        result_daesin = self.Object_Login_Daesin.connect_state()
        self.Line_Daesin.setText(result_daesin)
        
        # 이베스트증권 연결 상태를 Line_conn3 라인에디트에 표시
        if self.Object_XASessionEvents.logInState == 1:
            self.Line_Ebest.setText("Connect")
        else:
            self.Line_Ebest.setText("Disconnect")
            
    # 1. 각종목폴더에데이터추가 버튼 클릭 시 이벤트
    def Btn_Make_Alldata_clicked(self):
        self.Object_make_folder_alldata_cls.createCsv()
    
    # 2. 재무제표만들기 버튼 클릭 시 이벤트
    def Btn_Make_Jaemu_clicked(self):
        self.Object_report_cls.Report_Make()
    
    # 3. 증가율만들기 버튼 클릭 시 이벤트   
    def Btn_Make_Roi_clicked(self):    
        self.Object_Report_Roi.Roi_Make()
    
    # 화면1에서 전체종목 조회버튼 클릭시 => 화면1의 테이블에 데이터 표시
    def Btn_Search_All_clicked(self):
        # screen1 패키지에서 하루종목전체데이터 가져오기
        Oneday_data = self.Object_Today_Alldata_cls.Itg_report()
        
        # Display_data는 화면에 표시할 데이터
        Display_data = Oneday_data
        
        # 체크박스에 체크가 된다면 해당 분기데이터는 이용함
        if self.Checkbox_Jaemu.isChecked() == True:
            Jaemu_data = pd.read_csv('report_csv/report_make/재무정보_'+self.Var_Quarter.text()+'분기.csv', encoding='cp949')
            # 병합 => 화면에 표시할 데이터!!
            Display_data = pd.merge(Display_data,Jaemu_data, how='outer', on=['종목코드'])
        
        if self.Checkbox_Roi.isChecked() == True:
            Roi_data = pd.read_csv('report_csv/report_roi/증가율_'+self.Var_Quarter.text()+'분기.csv', encoding='cp949')
            # 병합 => 화면에 표시할 데이터!!
            Display_data = pd.merge(Display_data,Roi_data, how='outer', on=['종목코드'])
        
        # 데이터 열 수 구하기
        Display_data_colunm_num = len(Display_data.columns)
        
        # 데이터의 행 수 구하기
        Display_data_row_num = len(Display_data)
        
        # 데이터의 컬럼을 배열로 저장
        Display_data_colunm_arr = Display_data.columns
        
        # 행수와 열수로 테이블 설정하기
        self.Table_One.setRowCount(Display_data_row_num)
        self.Table_One.setColumnCount(Display_data_colunm_num)
        
        # 컬럼명 지정하기
        self.Table_One.setHorizontalHeaderLabels(Display_data_colunm_arr)
        
        # 컬럼 사이즈를 조정하기위해 테이블의 헤더 설정
        header = self.Table_One.horizontalHeader()
        
        # 데이터 표시하기
        for i in range(len(Display_data.index)):
            for j in range(len(Display_data.columns)):
                # 컬럼 크기에 맞춰 너비 맞추기
                header.setSectionResizeMode(j, QHeaderView.ResizeToContents)
                
                # 데이터 넣기
                self.Table_One.setItem(i, j, QTableWidgetItem(str(Display_data.iloc[i, j])))
                
    # 화면1에서 종목조회버튼 클릭시
    def Btn_Search_One_clicked(self):
        # screen1 패키지에서 하루종목전체데이터 가져오기
        Oneday_data = self.Object_Today_Alldata_cls.Itg_report()
        
        # Display_data는 화면에 표시할 데이터
        Search_All_Data = Oneday_data
        
        # 체크박스에 체크가 된다면 해당 분기데이터는 이용함
        if self.Checkbox_Jaemu.isChecked() == True:
            Jaemu_data = pd.read_csv('report_csv/report_make/재무정보_'+self.Var_Quarter.text()+'분기.csv', encoding='cp949')
            # 병합 => 화면에 표시할 데이터!!
            Search_All_Data = pd.merge(Search_All_Data,Jaemu_data, how='outer', on=['종목코드'])
        
        if self.Checkbox_Roi.isChecked() == True:
            Roi_data = pd.read_csv('report_csv/report_roi/증가율_'+self.Var_Quarter.text()+'분기.csv', encoding='cp949')
            # 병합 => 화면에 표시할 데이터!!
            Search_All_Data = pd.merge(Search_All_Data,Roi_data, how='outer', on=['종목코드'])
        
        try:
            # 콤보박스가 종목코드, 종목명에 따라서 검색하기
            if self.Combo_Search.currentText() == '종목코드':
                aa = str(Search_All_Data[Search_All_Data['종목코드'] == '['+self.Line_Search.text()+']'].index.tolist())
                
            else:
                aa = str(Search_All_Data[Search_All_Data['종목명'] == self.Line_Search.text()].index.tolist())
                
            # 인덱스의 좌,우 괄호지우기
            aa = aa.lstrip('[')
            aa = aa.rstrip(']')
            
            # 데이터의 컬럼을 배열로 저장
            Search_All_Data_arr = Search_All_Data.columns
            
            # 행수와 열수로 테이블 설정하기
            self.Table_One.setRowCount(1)
            self.Table_One.setColumnCount(len(Search_All_Data.columns))
            
            # 컬럼명 지정하기
            self.Table_One.setHorizontalHeaderLabels(Search_All_Data_arr)
            
            # 컬럼 사이즈를 조정하기위해 테이블의 헤더 설정
            header = self.Table_One.horizontalHeader()
            
            # 테이블에 데이터 표시하기
            for j in range(len(Search_All_Data.columns)):
                # 컬럼 크기에 맞춰 너비 맞추기
                header.setSectionResizeMode(j, QHeaderView.ResizeToContents)
                
                # 데이터 넣기
                self.Table_One.setItem(0, j, QTableWidgetItem(str(Search_All_Data.iloc[int(aa), j])))
                    
        except:
            print('일치하는 항목이 없습니다.')
            
    # 화면2의 종목조회버튼 클릭 시 이벤트
    def Btn_Search_Del_clicked(self):
        
        # 변수 선언
        year = '2020' # 나중에 self.Var_Year.text()로 변경
        q = self.Var_Quarter.text()
        debt = self.Line_Debt.text()
        
        if self.Radio_Sales_Plus.isChecked():
            young = '영업(+)'
        if self.Radio_Sales_Minus.isChecked():
            young = '영업(-)'
        if self.Radio_Invest_Plus.isChecked():    
            to = '투자(+)'
        if self.Radio_Invest_Minus.isChecked():
            to = '투자(-)'
        if self.Radio_Finance_Plus.isChecked():
            jae = '재무(+)'
        if self.Radio_Finance_Minus.isChecked():            
            jae = '재무(-)'
            
        start_dd = self.Date_Fm.text()
        start_dd = start_dd.replace('-','')
        end_dd = self.Date_To.text()
        end_dd = end_dd.replace('-','')
        
        publ = self.Line_Publish.text()
        term = self.Line_Receivable.text()
        
        debt_arr = []
        hyen_arr = []
        publish_arr = []
        trade_arr = []
        
        # 배열에 결과 종목코드 넣기
        if self.CheckBox_Debt.isChecked():
            debt_arr = self.Object_debt_ratio_cls.result_debt(year, q, int(debt))
        
        if self.CheckBox_Hyengum.isChecked():
            hyen_arr = self.Object_hyen_flow_cls.result_flow(year, q, young, to, jae)
        
        if self.CheckBox_Publish.isChecked():
            try:
                publish_arr = self.Object_publish_jusik_cls.publish_jusik(start_dd, end_dd, int(publ))
            except:
                print('날짜를 다시 설정해주세요')
        
        if self.CheckBox_Receivable.isChecked():        
            trade_arr = self.Object_trade_receivable_cls.result_receivable(year, q, int(term))

        # 해당 위험종목 조건 중 하나라도 포함되는 종목들을 배열로 구하기
        result_arr = debt_arr + hyen_arr + publish_arr + trade_arr
        result_arr = set(result_arr) #집합set으로 변환
        result_arr = list(result_arr) #list로 변환
        print(len(result_arr))
        
        # 위험종목을 제외한 종목을 테이블에 표시하기
        OB = MyWindow()
        Display_data = OB.Common_Upload_All()
        
        print(len(Display_data))
        
        for i in result_arr:
            idx = Display_data[Display_data['종목코드'] == i].index
            Display_data.drop(idx, inplace=True)
        
        print(len(Display_data))
            
    ################################################################################    
           
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
import pandas as pd
from Invest.screen3.step1 import step1_cls
from Invest.screen3.step2 import step2_cls
from Invest.screen3.step3 import step3_cls
from Invest.screen3.step4 import step4_cls
from Invest.screen3.step4_2 import step4_2_cls
from Invest.screen3.step4_3 import step4_3_cls
from Invest.screen3.step5 import step5_cls
from Invest.screen3.step6 import step6_cls
import openpyxl

class stepall_cls:
    def do_step(self, number, tr, nday, nbar, nmore, dd, dnd, nb):
        
        # 스텝 1단계
        #step1_cls.make_step1(self, number, tr, nday)
        
        # 스탭 2단계
        step2_cls.make_step2(self, number, nbar, nmore)
        '''
        # 스탭 3단계
        step3_cls.make_step3(self, number, dd, dnd, nb)
        
        # 스탭 4단계
        step4_cls.make_step4(self,number)
        step4_2_cls.make_step4_2(self, number)
        step4_3_cls.make_step4_3(self, number)
        
        # 스탭 5단계
        step5_cls.make_step5(self, number)
        
        
        ## 엑셀에 조건 넣기 ##       
        # 엑셀 파일 열기
        wb = openpyxl.load_workbook('F:/JusikData/analysis_csv/step/step3/증가감소(추가)_'+str(number)+'.xlsx')
        
        # 시트 지정 하기
        sheet = wb['증가감소비교분석']
        
        # 조건 넣기
        sheet['B2'] = '거래량 : ' + str(tr) 
        sheet['C2'] = '최대값일자 : ' + str(nday)
        sheet['D2'] = '이후n봉동안 : ' + str(nbar)
        sheet['E2'] = 'd일 : ' + str(dd)
        sheet['F2'] = 'd+n일 : ' + str(dnd)
        sheet['G2'] = 'n%봉 개수 : ' + str(nb)
        
        # 저장
        wb.save('F:/JusikData/analysis_csv/step/step3/증가감소(추가)_'+str(number)+'.xlsx')
        wb.close()
        
        
        # 스탭 6단계
        # 증가한 종목의 기준일 파일.csv
        nameid = ['증가', '감소']
        
        for name in nameid:
            data = pd.read_excel('F:/JusikData/analysis_csv/step/step5/'+name+'(필터링)_'+str(number)+'.xlsx', engine='openpyxl')
            
            err = []
            print('동작시작')
            for index, row in data.iterrows():
                try:
                    # 시작 알림
                    print(row['종목명'],'_시작')
                    
                    # 해당 종목의 데이터 가져오기
                    data = pd.read_csv("F:/JusikData/oneday_csv/onedaydata/"+row['종목명']+"/"+row['종목명']+".csv", encoding='cp949')
                    data_day = data['일자'].tolist()
                    
                    # 일자리스트에서 기준일의 인덱스 가져오기
                    stday_index = data_day.index(row['기준일'])
                    
                    # 기준일 + n일의 인덱스에서 일자를 가져오기
                    n_index = stday_index
                    end_day = data_day[n_index]
                    end_day = str(end_day)[0:4] + '-' + str(end_day)[4:6] + '-' + str(end_day)[6:8]
                    
                    # row['기준일']의 형식을 변경하기
                    sl_date = str(row['기준일'])[0:4] + '-' + str(row['기준일'])[4:6] + '-' + str(row['기준일'])[6:8]
                    
                    # 함수 실행
                    step6_cls.make_step6(self, number, row['종목명'], sl_date, end_day, 20)
                except:
                    coment = row['종목명'] + sl_date + end_day + '_오류'
                    print(coment)
                    err.append(coment)
                
            print('에러는 : ', err)
            print('동작끝') 
            '''
        
# 객체 생성
conn = stepall_cls()

# 실행
'''
number : 파일이 몇번째인지
tr : 투자시점 - 거래량
nday : 투자시점 - 기준일 최대값이 몇일 전 최대값보다 클지
nbar : 매도시점 - 이후 n봉 동안 몇 %올랐을지
nmore : 최대증가율을 n이상, 이하로 구분하기
dd : d일
dnd : d+n일
nb : 봉이 몇 %
'''
conn.do_step(777, 10, 20, 60, 30, 20, 60, 15)


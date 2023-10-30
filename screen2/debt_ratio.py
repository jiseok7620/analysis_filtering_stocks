# 부채비율이 200% 이상인 기업 제외하기

import pandas as pd
import datetime

class debt_ratio_cls:
    def result_debt(self, year, q, debt):
        # csv를 데이터프레임으로 저장하기
        
        self.jaemu_data_y = pd.read_csv('F:/JusikData/report_csv/report/'+year+'_'+q+'_jaemu_y.csv', encoding='cp949')
        
        # 필요한 열만 가져오기
        self.jaemu_data_y = self.jaemu_data_y.iloc[:,[1,2,4,5,10,11,12]]
        
        ## 자본총계 가져오기 : ifrs-full_Equity##
        # 자본총계
        jaemu1_y = self.jaemu_data_y[self.jaemu_data_y['항목코드'].isin(['ifrs-full_Equity'])]
        jaemu1_y.rename(columns={ jaemu1_y.columns[6] : year+'_자본총계_'+q}, inplace=True)
        
        ## 부채총계 가져오기 : ifrs-full_Liabilities##
        # 부채총계
        jaemu2_y = self.jaemu_data_y[self.jaemu_data_y['항목코드'].isin(['ifrs-full_Liabilities'])]
        jaemu2_y.rename(columns={ jaemu2_y.columns[6] : year+'_부채총계_'+q}, inplace=True)
        jaemu2_y = jaemu2_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        
        # 병합
        jaemu_y = pd.merge(jaemu1_y,jaemu2_y,how='outer',on=['종목코드'])
        
        # 확인
        #print(jaemu_y)
        
        ## 부채율 구하기 ##
        # ,빼고 float으로 만들기
        jaemu_y.iloc[:,1:] = jaemu_y.iloc[:,1:].replace(',','',regex=True)
        
        # 전체를 numeric으로 변환하기
        a = 6
        row_count = len(jaemu_y.columns)
        exit = True
        
        while exit:
            jaemu_y.iloc[:,a] = pd.to_numeric(jaemu_y.iloc[:,a], downcast='float')
            a = a + 1
            if a == row_count:
                exit = False
            
        
        # 부채율 = 자본총액 / 부채총액 * 100
        jaemu_y[year+'_부채율_'+q] = (jaemu_y[year+'_자본총계_'+q] / jaemu_y[year+'_부채총계_'+q]) * 100
        
        # 확인
        #print(jaemu_y)
        
        # 부채율은 200 이하가 적정
        # 이것은 적정하지 못한 회사를 구하는 것
        jaemu_name_y = []
        for i in jaemu_y.index:
            if jaemu_y.loc[i,year+'_부채율_'+q] >= debt:
                jaemu_name_y.append(jaemu_y.loc[i,'종목코드'])

        # 확인
        #print(jaemu_name_y) 
        
        # 결과 리턴
        return jaemu_name_y

# 테스트
#conn = debt_ratio_cls()
#conn.result_debt('2020', '2', 200)               
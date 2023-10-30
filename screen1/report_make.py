# 1~4분기 보고서를 가져와서 필요한 데이터만 꺼내 데이터프레임 만들기

import pandas as pd
import openpyxl
import os
import datetime
import sys

class report_cls:
    def report(self, year, q):
        #### csv를 데이터프레임으로 저장하기####
        df_hyen = pd.read_csv('F:/JusikData/report_csv/report/'+year+'_'+q+'_hyen.csv', encoding='cp949')
        df_hyen_y = pd.read_csv('F:/JusikData/report_csv/report/'+year+'_'+q+'_hyen_y.csv', encoding='cp949')
        df_jaemu = pd.read_csv('F:/JusikData/report_csv/report/'+year+'_'+q+'_jaemu.csv', encoding='cp949')
        df_jaemu_y = pd.read_csv('F:/JusikData/report_csv/report/'+year+'_'+q+'_jaemu_y.csv', encoding='cp949')
        df_posonik = pd.read_csv('F:/JusikData/report_csv/report/'+year+'_'+q+'_posonik.csv', encoding='cp949')
        df_posonik_y = pd.read_csv('F:/JusikData/report_csv/report/'+year+'_'+q+'_posonik_y.csv', encoding='cp949')
        df_sonik = pd.read_csv('F:/JusikData/report_csv/report/'+year+'_'+q+'_sonik.csv', encoding='cp949')
        df_sonik_y = pd.read_csv('F:/JusikData/report_csv/report/'+year+'_'+q+'_sonik_y.csv', encoding='cp949')
        ########################################
        #
        #
        #
        #
        #### 데이터 정제하기(필요한 열만 추출) ####
        df_hyen = df_hyen.iloc[:,[1,2,4,5,10,11,12]]
        df_hyen_y = df_hyen_y.iloc[:,[1,2,4,5,10,11,12]]
        df_jaemu = df_jaemu.iloc[:,[1,2,4,5,10,11,12]]
        df_jaemu_y = df_jaemu_y.iloc[:,[1,2,4,5,10,11,12]]
        df_posonik = df_posonik.iloc[:,[1,2,4,5,10,11,12]]
        df_posonik_y = df_posonik_y.iloc[:,[1,2,4,5,10,11,12]]
        df_sonik = df_sonik.iloc[:,[1,2,4,5,10,11,12]]        
        df_sonik_y = df_sonik_y.iloc[:,[1,2,4,5,10,11,12]]
        #print(df_hyen.columns)
        #print(self.df_hyen_y.columns)
        #print(self.df_jaemu.columns)
        #print(self.df_jaemu_y.columns)
        #print(self.df_posonik.columns)
        #print(self.df_posonik_y.columns)
        #print(self.df_sonik.columns)
        #print(self.df_sonik_y.columns)
        ########################################
        #
        #
        #
        #
        #### 현금흐름표_연결에서 필요한 데이터만 가져오기 ####
        # 영업활동현금흐름
        hyen1_y = df_hyen_y[df_hyen_y['항목코드'].isin(['ifrs_CashFlowsFromUsedInOperatingActivities', 'ifrs-full_CashFlowsFromUsedInOperatingActivities'])]
        hyen1_y.rename(columns={ hyen1_y.columns[6] : year+'_영업활동현금흐름_'+q}, inplace=True)
        # 미연결
        hyen1 = df_hyen[df_hyen['항목코드'].isin(['ifrs_CashFlowsFromUsedInOperatingActivities', 'ifrs-full_CashFlowsFromUsedInOperatingActivities'])]
        hyen1.rename(columns={ hyen1.columns[6] : year+'_영업활동현금흐름(2)_'+q}, inplace=True)
        
        # 투자활동현금흐름
        hyen2_y = df_hyen_y[df_hyen_y['항목코드'].isin(['ifrs_CashFlowsFromUsedInInvestingActivities', 'ifrs-full_CashFlowsFromUsedInInvestingActivities'])]
        hyen2_y.rename(columns={ hyen2_y.columns[6] : year+'_투자활동현금흐름_'+q}, inplace=True)
        # 미연결
        hyen2 = df_hyen[df_hyen['항목코드'].isin(['ifrs_CashFlowsFromUsedInInvestingActivities', 'ifrs-full_CashFlowsFromUsedInInvestingActivities'])]
        hyen2.rename(columns={ hyen2.columns[6] : year+'_투자활동현금흐름(2)_'+q}, inplace=True)
        
        # 재무활동현금흐름
        hyen3_y = df_hyen_y[df_hyen_y['항목코드'].isin(['ifrs_CashFlowsFromUsedInFinancingActivities', 'ifrs-full_CashFlowsFromUsedInFinancingActivities'])]
        hyen3_y.rename(columns={ hyen3_y.columns[6] : year+'_재무활동현금흐름_'+q}, inplace=True)
        # 미연결
        hyen3 = df_hyen[df_hyen['항목코드'].isin(['ifrs_CashFlowsFromUsedInFinancingActivities', 'ifrs-full_CashFlowsFromUsedInFinancingActivities'])]
        hyen3.rename(columns={ hyen3.columns[6] : year+'_재무활동현금흐름(2)_'+q}, inplace=True)
        
        # 감가상각비
        hyen4_y = df_hyen_y[df_hyen_y['항목코드'].isin(['dart_AdjustmentsForDepreciationExpense'])]
        hyen4_y.rename(columns={ hyen4_y.columns[6] : year+'_감가상각비_'+q}, inplace=True)
        # 미연결
        hyen4 = df_hyen[df_hyen['항목코드'].isin(['dart_AdjustmentsForDepreciationExpense'])]
        hyen4.rename(columns={ hyen4.columns[6] : year+'_감가상각비(2)_'+q}, inplace=True)
        
        # 이자비용
        hyen5_y = df_hyen_y[df_hyen_y['항목코드'].isin(['dart_AdjustmentsForInterestExpenses'])]
        hyen5_y.rename(columns={ hyen5_y.columns[6] : year+'_이자비용_'+q}, inplace=True)
        
        # 퇴직급여
        hyen6_y = df_hyen_y[df_hyen_y['항목코드'].isin(['dart_AdjustmentsForProvisionForSeveranceIndemnities'])]
        hyen6_y.rename(columns={ hyen6_y.columns[6] : year+'_퇴직급여_'+q}, inplace=True)
        # 미연결
        hyen6 = df_hyen[df_hyen['항목코드'].isin(['dart_AdjustmentsForProvisionForSeveranceIndemnities'])]
        hyen6.rename(columns={ hyen6.columns[6] : year+'_퇴직급여(2)_'+q}, inplace=True)
        
        # 병합하기위해 필요없는 컬럼 제거
        hyen1_y = hyen1_y.drop(['항목명','항목코드'], axis=1)
        hyen1 = hyen1.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)
        hyen2_y = hyen2_y.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)
        hyen2 = hyen2.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)
        hyen3_y = hyen3_y.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)
        hyen3 = hyen3.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)
        hyen4_y = hyen4_y.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)
        hyen4 = hyen4.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)
        hyen5_y = hyen5_y.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)
        hyen6_y = hyen6_y.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)
        hyen6 = hyen6.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)
        
        # 병합
        hyen_y = pd.merge(hyen1_y,hyen1, how='outer', on=['회사명'])
        hyen_y = pd.merge(hyen_y,hyen2_y, how='outer', on=['회사명'])
        hyen_y = pd.merge(hyen_y,hyen2, how='outer', on=['회사명'])        
        hyen_y = pd.merge(hyen_y,hyen3_y, how='outer', on=['회사명'])
        hyen_y = pd.merge(hyen_y,hyen3, how='outer', on=['회사명'])        
        hyen_y = pd.merge(hyen_y,hyen4_y, how='outer', on=['회사명'])
        hyen_y = pd.merge(hyen_y,hyen4, how='outer', on=['회사명'])        
        hyen_y = pd.merge(hyen_y,hyen5_y, how='outer', on=['회사명'])
        hyen_y = pd.merge(hyen_y,hyen6_y, how='outer', on=['회사명'])
        hyen_y = pd.merge(hyen_y,hyen6, how='outer', on=['회사명'])        
        hyen_y = hyen_y.drop_duplicates(['회사명'])
        
        # 타입과 사이즈 확인
        #print(hyen_y.dtypes)
        #print(sys.getsizeof(hyen_y))
        
        # 데이터의 ,빼주기
        hyen_y.iloc[:,4:] = hyen_y.iloc[:,4:].replace(',','',regex=True)
        
        # float64를 32로 바꿔주기
        hyen_y = hyen_y.astype({'업종':'float32'})
        
        # 전체를 numeric으로 변환하기
        a = 4
        row_count = len(hyen_y.columns)
            
        while True:
            hyen_y.iloc[:,a] = pd.to_numeric(hyen_y.iloc[:,a], downcast='float')
            a = a + 1
            if a == row_count:
                break
            
        # 타입과 사이즈 확인
        #print(hyen_y.dtypes)
        #print(sys.getsizeof(hyen_y))
        
        # 확인
        # print(hyen_y).
        ########################################
        #
        #
        #
        #
        #### 재무상태표_연결에서 필요한 데이터만 가져오기 ####
        # 매출채권
        jaemu1_y = df_jaemu_y[df_jaemu_y['항목코드'].isin(['ifrs_TradeAndOtherCurrentReceivables', 'dart_ShortTermTradeReceivable'])]
        jaemu1_y.rename(columns={ jaemu1_y.columns[6] : year+'_매출채권(유동)_'+q}, inplace=True)
        
        # 재고자산
        jaemu2_y = df_jaemu_y[df_jaemu_y['항목코드'].isin(['ifrs_Inventories', 'ifrs-full_Inventories'])]
        jaemu2_y.rename(columns={ jaemu2_y.columns[6] : year+'_재고자산_'+q}, inplace=True)
        
        # 전환사채
        jaemu3_y = df_jaemu_y[df_jaemu_y['항목코드'].isin(['dart_CurrentPortionOfConvertibleBonds'])]
        jaemu3_y.rename(columns={ jaemu3_y.columns[6] : year+'_전환사채(유동)_'+q}, inplace=True)
        
        # 신주인수권부사채
        jaemu4_y = df_jaemu_y[df_jaemu_y['항목코드'].isin(['dart_CurrentPortionOfBondWithWarrant'])]
        jaemu4_y.rename(columns={ jaemu4_y.columns[6] : year+'_신주인수권부사채(유동)_'+q}, inplace=True)
        
        # 자산총계
        jaemu5_y = df_jaemu_y[df_jaemu_y['항목코드'].isin(['ifrs_Assets', 'ifrs-full_Assets'])]
        jaemu5_y.rename(columns={ jaemu5_y.columns[6] : year+'_자산총계_'+q}, inplace=True)
        
        # 유동자산
        jaemu5_1_y = df_jaemu_y[df_jaemu_y['항목코드'].isin(['ifrs_CurrentAssets', 'ifrs-full_CurrentAssets'])]
        jaemu5_1_y.rename(columns={ jaemu5_1_y.columns[6] : year+'_유동자산_'+q}, inplace=True)
        
        # 부채총계
        jaemu6_y = df_jaemu_y[df_jaemu_y['항목코드'].isin(['ifrs_Liabilities', 'ifrs-full_Liabilities'])]
        jaemu6_y.rename(columns={ jaemu6_y.columns[6] : year+'_부채총계_'+q}, inplace=True)

        # 유동부채
        jaemu7_y = df_jaemu_y[df_jaemu_y['항목코드'].isin(['ifrs_CurrentLiabilities', 'ifrs-full_CurrentLiabilities'])]
        jaemu7_y.rename(columns={ jaemu7_y.columns[6] : year+'_유동부채_'+q}, inplace=True)

        # 자본총계
        jaemu8_y = df_jaemu_y[df_jaemu_y['항목코드'].isin(['ifrs_Equity', 'ifrs-full_Equity'])]
        jaemu8_y.rename(columns={ jaemu8_y.columns[6] : year+'_자본총계_'+q}, inplace=True)
        
        # 자본금
        jaemu9_y = df_jaemu_y[df_jaemu_y['항목코드'].isin(['ifrs_IssuedCapital','ifrs-full_IssuedCapital','dart_ContributedEquity'])]
        jaemu9_y.rename(columns={ jaemu9_y.columns[6] : year+'_자본금_'+q}, inplace=True)
        
        # 이익잉여금
        jaemu10_y = df_jaemu_y[df_jaemu_y['항목코드'].isin(['ifrs_RetainedEarnings','ifrs-full_RetainedEarnings'])]
        jaemu10_y.rename(columns={ jaemu10_y.columns[6] : year+'_이익잉여금_'+q}, inplace=True)
        
        # 자본잉여금
        jaemu11_y = df_jaemu_y[df_jaemu_y['항목코드'].isin(['ifrs_SharePremium', 'ifrs-full_SharePremium', 'dart_CapitalSurplus'])]
        jaemu11_y.rename(columns={ jaemu11_y.columns[6] : year+'_자본잉여금_'+q}, inplace=True)
        
        
        # 병합하기위해 필요없는 컬럼 제거
        jaemu1_y = jaemu1_y.drop(['항목명','항목코드'], axis=1)
        jaemu2_y = jaemu2_y.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)
        jaemu3_y = jaemu3_y.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)
        jaemu4_y = jaemu4_y.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)
        jaemu5_y = jaemu5_y.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)
        jaemu5_1_y = jaemu5_1_y.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)
        jaemu6_y = jaemu6_y.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)
        jaemu7_y = jaemu7_y.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)
        jaemu8_y = jaemu8_y.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)
        jaemu9_y = jaemu9_y.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)
        jaemu10_y = jaemu10_y.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)
        jaemu11_y = jaemu11_y.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)        
        
        # 병합
        jaemu_y = pd.merge(jaemu1_y,jaemu2_y,how='outer',on=['회사명'])
        jaemu_y = pd.merge(jaemu_y,jaemu3_y,how='outer',on=['회사명'])
        jaemu_y = pd.merge(jaemu_y,jaemu4_y,how='outer',on=['회사명'])
        jaemu_y = pd.merge(jaemu_y,jaemu5_y,how='outer',on=['회사명'])
        jaemu_y = pd.merge(jaemu_y,jaemu5_1_y,how='outer',on=['회사명'])
        jaemu_y = pd.merge(jaemu_y,jaemu6_y,how='outer',on=['회사명'])
        jaemu_y = pd.merge(jaemu_y,jaemu7_y,how='outer',on=['회사명'])
        jaemu_y = pd.merge(jaemu_y,jaemu8_y,how='outer',on=['회사명'])
        jaemu_y = pd.merge(jaemu_y,jaemu9_y,how='outer',on=['회사명'])
        jaemu_y = pd.merge(jaemu_y,jaemu10_y,how='outer',on=['회사명'])
        jaemu_y = pd.merge(jaemu_y,jaemu11_y,how='outer',on=['회사명'])
        jaemu_y = jaemu_y.drop_duplicates(['회사명'])
        
        # 타입과 사이즈 확인
        #print(jaemu_y.dtypes)
        #print(sys.getsizeof(jaemu_y))
        
        # 데이터의 ,빼주기
        jaemu_y.iloc[:,4:] = jaemu_y.iloc[:,4:].replace(',','',regex=True)
        
        # float64를 32로 바꿔주기
        jaemu_y = jaemu_y.astype({'업종':'float32'})
        
        # 전체를 numeric으로 변환하기
        a = 4
        row_count = len(jaemu_y.columns)
            
        while True:
            jaemu_y.iloc[:,a] = pd.to_numeric(jaemu_y.iloc[:,a], downcast='float')
            a = a + 1
            if a == row_count:
                break
            
        # 타입과 사이즈 확인
        #print(jaemu_y.dtypes)
        #print(sys.getsizeof(jaemu_y))
        
        ########################################
        #
        #
        #
        #
        #### 재무상태표_연결에서 필요한 데이터만 가져오기 ####
        # 매출채권
        jaemu1 = df_jaemu[df_jaemu['항목코드'].isin(['ifrs_TradeAndOtherCurrentReceivables', 'dart_ShortTermTradeReceivable'])]
        jaemu1.rename(columns={ jaemu1.columns[6] : year+'_매출채권(유동)(2)_'+q}, inplace=True)
        
        # 재고자산
        jaemu2 = df_jaemu[df_jaemu['항목코드'].isin(['ifrs_Inventories', 'ifrs-full_Inventories'])]
        jaemu2.rename(columns={ jaemu2.columns[6] : year+'_재고자산(2)_'+q}, inplace=True)
        
        # 전환사채
        jaemu3 = df_jaemu[df_jaemu['항목코드'].isin(['dart_CurrentPortionOfConvertibleBonds'])]
        jaemu3.rename(columns={ jaemu3.columns[6] : year+'_전환사채(유동)(2)_'+q}, inplace=True)
        
        # 신주인수권부사채
        jaemu4 = df_jaemu[df_jaemu['항목코드'].isin(['dart_CurrentPortionOfBondWithWarrant'])]
        jaemu4.rename(columns={ jaemu4.columns[6] : year+'_신주인수권부사채(유동)(2)_'+q}, inplace=True)
        
        # 자산총계
        jaemu5 = df_jaemu[df_jaemu['항목코드'].isin(['ifrs_Assets', 'ifrs-full_Assets'])]
        jaemu5.rename(columns={ jaemu5.columns[6] : year+'_자산총계(2)_'+q}, inplace=True)
        
        # 유동자산
        jaemu5_1 = df_jaemu[df_jaemu['항목코드'].isin(['ifrs_CurrentAssets', 'ifrs-full_CurrentAssets'])]
        jaemu5_1.rename(columns={ jaemu5_1.columns[6] : year+'_유동자산(2)_'+q}, inplace=True)
        
        # 부채총계
        jaemu6 = df_jaemu[df_jaemu['항목코드'].isin(['ifrs_Liabilities', 'ifrs-full_Liabilities'])]
        jaemu6.rename(columns={ jaemu6.columns[6] : year+'_부채총계(2)_'+q}, inplace=True)

        # 유동부채
        jaemu7 = df_jaemu[df_jaemu['항목코드'].isin(['ifrs_CurrentLiabilities', 'ifrs-full_CurrentLiabilities'])]
        jaemu7.rename(columns={ jaemu7.columns[6] : year+'_유동부채(2)_'+q}, inplace=True)

        # 자본총계
        jaemu8 = df_jaemu[df_jaemu['항목코드'].isin(['ifrs_Equity', 'ifrs-full_Equity'])]
        jaemu8.rename(columns={ jaemu8.columns[6] : year+'_자본총계(2)_'+q}, inplace=True)
        
        # 자본금
        jaemu9 = df_jaemu[df_jaemu['항목코드'].isin(['ifrs_IssuedCapital','ifrs-full_IssuedCapital','dart_ContributedEquity'])]
        jaemu9.rename(columns={ jaemu9.columns[6] : year+'_자본금(2)_'+q}, inplace=True)
        
        # 이익잉여금
        jaemu10 = df_jaemu[df_jaemu['항목코드'].isin(['ifrs_RetainedEarnings','ifrs-full_RetainedEarnings'])]
        jaemu10.rename(columns={ jaemu10.columns[6] : year+'_이익잉여금(2)_'+q}, inplace=True)
        
        # 자본잉여금
        jaemu11 = df_jaemu[df_jaemu['항목코드'].isin(['ifrs_SharePremium', 'ifrs-full_SharePremium', 'dart_CapitalSurplus'])]
        jaemu11.rename(columns={ jaemu11.columns[6] : year+'_자본잉여금(2)_'+q}, inplace=True)
        
        
        # 병합하기위해 필요없는 컬럼 제거
        jaemu1 = jaemu1.drop(['항목명','항목코드'], axis=1)        
        jaemu2 = jaemu2.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)
        jaemu3 = jaemu3.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)        
        jaemu4 = jaemu4.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)        
        jaemu5 = jaemu5.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)        
        jaemu5_1 = jaemu5_1.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)        
        jaemu6 = jaemu6.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)        
        jaemu7 = jaemu7.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)        
        jaemu8 = jaemu8.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)        
        jaemu9 = jaemu9.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)        
        jaemu10 = jaemu10.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)        
        jaemu11 = jaemu11.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)                
        
        # 병합
        jaemu = pd.merge(jaemu1,jaemu2,how='outer',on=['회사명'])
        jaemu = pd.merge(jaemu,jaemu3,how='outer',on=['회사명'])        
        jaemu = pd.merge(jaemu,jaemu4,how='outer',on=['회사명'])        
        jaemu = pd.merge(jaemu,jaemu5,how='outer',on=['회사명'])        
        jaemu = pd.merge(jaemu,jaemu5_1,how='outer',on=['회사명'])        
        jaemu = pd.merge(jaemu,jaemu6,how='outer',on=['회사명'])        
        jaemu = pd.merge(jaemu,jaemu7,how='outer',on=['회사명'])        
        jaemu = pd.merge(jaemu,jaemu8,how='outer',on=['회사명'])        
        jaemu = pd.merge(jaemu,jaemu9,how='outer',on=['회사명'])        
        jaemu = pd.merge(jaemu,jaemu10,how='outer',on=['회사명'])        
        jaemu = pd.merge(jaemu,jaemu11,how='outer',on=['회사명'])        
        jaemu = jaemu.drop_duplicates(['회사명'])
        
        # 타입과 사이즈 확인
        #print(jaemu.dtypes)
        #print(sys.getsizeof(jaemu))
        
        # 데이터의 ,빼주기
        jaemu.iloc[:,4:] = jaemu.iloc[:,4:].replace(',','',regex=True)
        
        # float64를 32로 바꿔주기
        jaemu = jaemu.astype({'업종':'float32'})
        
        # 전체를 numeric으로 변환하기
        a = 4
        row_count = len(jaemu_y.columns)
            
        while True:
            jaemu.iloc[:,a] = pd.to_numeric(jaemu.iloc[:,a], downcast='float')
            a = a + 1
            if a == row_count:
                break
            
        # 타입과 사이즈 확인
        #print(jaemu.dtypes)
        #print(sys.getsizeof(jaemu))
        
        
        # jaemu_y과 jaemu를 합치기
        jaemu = jaemu.drop(['종목코드','업종','업종명'], axis=1)
        jaemu_y = pd.merge(jaemu_y,jaemu,how='outer',on=['회사명'])
        #print(jaemu_y.dtypes)
        #print(sys.getsizeof(jaemu_y))
        # 확인
        ########################################
        #
        #
        #
        #
        #### 손익계산서_연결 or포괄손익계산서_연결에서 필요한 데이터만 가져오기 ####
        # 매출액
        posonik1_y = df_posonik_y[df_posonik_y['항목코드'].isin(['ifrs_Revenue', 'ifrs-full_Revenue'])]
        posonik1_y.rename(columns={ posonik1_y.columns[6] : year+'_매출액_'+q}, inplace=True)
        # 미연결
        posonik1 = df_posonik[df_posonik['항목코드'].isin(['ifrs_Revenue', 'ifrs-full_Revenue'])]
        posonik1.rename(columns={ posonik1.columns[6] : year+'_매출액(2)_'+q}, inplace=True)
        
        # 매출원가
        posonik1_1_y = df_posonik_y[df_posonik_y['항목코드'].isin(['ifrs_CostOfSales', 'ifrs-full_CostOfSales'])]
        posonik1_1_y.rename(columns={ posonik1_1_y.columns[6] : year+'_매출원가_'+q}, inplace=True)
        # 미연결
        posonik1_1 = df_posonik[df_posonik['항목코드'].isin(['ifrs_CostOfSales', 'ifrs-full_CostOfSales'])]
        posonik1_1.rename(columns={ posonik1_1.columns[6] : year+'_매출원가(2)_'+q}, inplace=True)
        
        # 영업이익
        posonik2_y = df_posonik_y[df_posonik_y['항목코드'].isin(['dart_OperatingIncomeLoss'])]
        posonik2_y.rename(columns={ posonik2_y.columns[6] : year+'_영업이익_'+q}, inplace=True)
        # 미연결
        posonik2 = df_posonik[df_posonik['항목코드'].isin(['dart_OperatingIncomeLoss'])]
        posonik2.rename(columns={ posonik2.columns[6] : year+'_영업이익(2)_'+q}, inplace=True)
        
        # 당기순이익
        posonik3_y = df_posonik_y[df_posonik_y['항목코드'].isin(['ifrs_ProfitLoss', 'ifrs-full_ProfitLoss'])]
        posonik3_y.rename(columns={ posonik3_y.columns[6] : year+'_당기순이익_'+q}, inplace=True)
        # 미연결
        posonik3 = df_posonik[df_posonik['항목코드'].isin(['ifrs_ProfitLoss', 'ifrs-full_ProfitLoss'])]
        posonik3.rename(columns={ posonik3.columns[6] : year+'_당기순이익(2)_'+q}, inplace=True)
        
        # 비지배지분이익
        posonik4_y = df_posonik_y[df_posonik_y['항목코드'].isin(['ifrs_ComprehensiveIncomeAttributableToNoncontrollingInterests','ifrs_ProfitLossAttributableToNoncontrollingInterests','ifrs-full_ProfitLossAttributableToNoncontrollingInterests'])]
        posonik4_y.rename(columns={ posonik4_y.columns[6] : year+'_비지배지분이익_'+q}, inplace=True)
        # 미연결
        posonik4 = df_posonik[df_posonik['항목코드'].isin(['ifrs_ComprehensiveIncomeAttributableToNoncontrollingInterests','ifrs_ProfitLossAttributableToNoncontrollingInterests','ifrs-full_ProfitLossAttributableToNoncontrollingInterests'])]
        posonik4.rename(columns={ posonik4.columns[6] : year+'_비지배지분이익(2)_'+q}, inplace=True)
        
        # 병합하기위해 필요없는 컬럼 제거
        posonik1_y = posonik1_y.drop(['항목명','항목코드'], axis=1)
        posonik1 = posonik1.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)        
        posonik1_1_y = posonik1_1_y.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)
        posonik1_1 = posonik1_1.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)        
        posonik2_y = posonik2_y.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)
        posonik2 = posonik2.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)        
        posonik3_y = posonik3_y.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)
        posonik3 = posonik3.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)        
        posonik4_y = posonik4_y.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)
        posonik4 = posonik4.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)        
        
        # 병합
        posonik_y = pd.merge(posonik1_y,posonik1,how='outer',on=['회사명'])
        posonik_y = pd.merge(posonik_y,posonik1_1_y,how='outer',on=['회사명'])
        posonik_y = pd.merge(posonik_y,posonik1_1,how='outer',on=['회사명'])        
        posonik_y = pd.merge(posonik_y,posonik2_y,how='outer',on=['회사명'])
        posonik_y = pd.merge(posonik_y,posonik2,how='outer',on=['회사명'])        
        posonik_y = pd.merge(posonik_y,posonik3_y,how='outer',on=['회사명'])
        posonik_y = pd.merge(posonik_y,posonik3,how='outer',on=['회사명'])        
        posonik_y = pd.merge(posonik_y,posonik4_y,how='outer',on=['회사명'])
        posonik_y = pd.merge(posonik_y,posonik4,how='outer',on=['회사명'])        
        posonik_y = posonik_y.drop_duplicates(['회사명'])
        
        # 포괄손익에 없는것들 손익계산서에서 찾기
        sonik1_y = df_sonik_y[df_sonik_y['항목코드'].isin(['ifrs_Revenue', 'ifrs-full_Revenue'])]
        sonik1_y.rename(columns={ sonik1_y.columns[6] : year+'_매출액(손익)_'+q}, inplace=True)
        sonik1_1_y = df_sonik_y[df_sonik_y['항목코드'].isin(['ifrs_CostOfSales','ifrs-full_CostOfSales'])]
        sonik1_1_y.rename(columns={ sonik1_1_y.columns[6] : year+'_매출원가(손익)_'+q}, inplace=True)
        sonik2_y = df_sonik_y[df_sonik_y['항목코드'].isin(['dart_OperatingIncomeLoss'])]
        sonik2_y.rename(columns={ sonik2_y.columns[6] : year+'_영업이익(손익)_'+q}, inplace=True)
        sonik3_y = df_sonik_y[df_sonik_y['항목코드'].isin(['ifrs_ProfitLoss', 'ifrs-full_ProfitLoss'])]
        sonik3_y.rename(columns={ sonik3_y.columns[6] : year+'_당기순이익(손익)_'+q}, inplace=True)
        sonik4_y = df_sonik_y[df_sonik_y['항목코드'].isin(['ifrs_ComprehensiveIncomeAttributableToNoncontrollingInterests','ifrs_ProfitLossAttributableToNoncontrollingInterests','ifrs-full_ProfitLossAttributableToNoncontrollingInterests'])]
        sonik4_y.rename(columns={ sonik4_y.columns[6] : year+'_비지배지분이익(손익)_'+q}, inplace=True)
        sonik1_y = sonik1_y.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)
        sonik1_1_y = sonik1_1_y.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)
        sonik2_y = sonik2_y.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)
        sonik3_y = sonik3_y.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)
        sonik4_y = sonik4_y.drop(['종목코드','업종','업종명','항목명','항목코드'], axis=1)
        sonik_y = pd.merge(sonik1_y,sonik1_1_y,how='outer',on=['회사명'])
        sonik_y = pd.merge(sonik_y,sonik2_y,how='outer',on=['회사명'])        
        sonik_y = pd.merge(sonik_y,sonik3_y,how='outer',on=['회사명'])
        sonik_y = pd.merge(sonik_y,sonik4_y,how='outer',on=['회사명'])
        sonik_y = sonik_y.drop_duplicates(['회사명'])
        
        # 손익계산서와 포괄손익계산서 병합
        posonik_y = pd.merge(posonik_y,sonik_y,how='outer',on=['회사명'])
        
        # 타입과 사이즈 확인
        #print(posonik_y.dtypes)
        #print(sys.getsizeof(posonik_y))
        
        # 데이터의 ,빼주기
        posonik_y.iloc[:,4:] = posonik_y.iloc[:,4:].replace(',','',regex=True)
        
        # float64를 32로 바꿔주기
        posonik_y = posonik_y.astype({'업종':'float32'})
        
        # 전체를 numeric으로 변환하기
        a = 4
        row_count = len(posonik_y.columns)
            
        while True:
            posonik_y.iloc[:,a] = pd.to_numeric(posonik_y.iloc[:,a], downcast='float')
            a = a + 1
            if a == row_count:
                break
            
        # 타입과 사이즈 확인
        #print(posonik_y.dtypes)
        #print(sys.getsizeof(posonik_y))
                
        # 확인
        #print(posonik_y)
        ######################################################
        #
        #
        #
        #
        #
        #
        #
        #
        #### 전체데이터 합치기 ####
        # hyen_y, jaemu_y, posonik_y
        # 1. 데이터에서 필요없는 열 제거
        hyen_y = hyen_y.drop(['업종'], axis=1)
        jaemu_y = jaemu_y.drop(['종목코드','업종','업종명'], axis=1)
        posonik_y = posonik_y.drop(['종목코드','업종','업종명'], axis=1)
        
        # 2. 데이터 합치기
        # merge : pd.merge(데이터프레임1, 데이터프레임2, how='방법', on=None)
        # on=None 이면 교집합 조인을 하게됨
        final_data = pd.merge(hyen_y,jaemu_y,how='outer',on=['회사명'])
        final_data = pd.merge(final_data,posonik_y,how='outer',on=['회사명'])
        final_data = final_data.drop_duplicates(['회사명'])
        
        # 3. 확인
        #print(final_data)
        #print(final_data.dtypes)
        #print(sys.getsizeof(final_data))
        
        # 4. 결과 리턴하기
        return final_data
    
        ######################################################
        
    def Report_Make(self):
        print('재무제표 csv 파일 생성 시작')
        
        # 1~4분기 세기 변수 : q_num
        # while문을 계속할지 중단할지 변수 : go_on
        q_num = 0
        go_on = True
        
        # nowDate = 현재년도 ex) 2021
        now = datetime.datetime.now()
        nowDate = now.strftime('%Y')
        
        # 반복문의 실행 -> 1~4분기까지 반복
        while go_on:
            q_num = q_num + 1
            
            if q_num == 5 :
                break
            
            # 해당 경로에 해당 파일이 있으면 최신년도 해당분기를 포함해서 진행
            directory = "F:/JusikData/report_csv/report/" + nowDate + "_" + str(q_num) + "_jaemu_y.csv"
            
            if os.path.exists(directory):
                # 1년마다 최신화 -> 해당 년도 추가 필요
                # 년도별 데이터 프레임 만들기
                # 년마다 해당 년도 변수 만들기
                dd_2021 = report_cls.report(self,'2021',str(q_num))
                dd_2020 = report_cls.report(self,'2020',str(q_num))
                dd_2019 = report_cls.report(self,'2019',str(q_num))
                dd_2018 = report_cls.report(self,'2018',str(q_num))
                dd_2017 = report_cls.report(self,'2017',str(q_num))
                dd_2016 = report_cls.report(self,'2016',str(q_num))
                
                # 한개 제외하고 회사명, 업종명 모두 drop 해주기
                dd_2020 = dd_2020.drop(['종목코드','업종명'], axis=1)
                dd_2019 = dd_2019.drop(['종목코드','업종명'], axis=1)
                dd_2018 = dd_2018.drop(['종목코드','업종명'], axis=1)
                dd_2017 = dd_2017.drop(['종목코드','업종명'], axis=1)
                dd_2016 = dd_2016.drop(['종목코드','업종명'], axis=1)
                
                # 데이터 프레임 병합하기
                alldata = pd.merge(dd_2021,dd_2020,how='outer',on=['회사명'])
                alldata = pd.merge(alldata,dd_2019,how='outer',on=['회사명'])
                alldata = pd.merge(alldata,dd_2018,how='outer',on=['회사명'])
                alldata = pd.merge(alldata,dd_2017,how='outer',on=['회사명'])
                alldata = pd.merge(alldata,dd_2016,how='outer',on=['회사명'])
        
            else:
                dd_2020 = report_cls.report(self,'2020',str(q_num))
                dd_2019 = report_cls.report(self,'2019',str(q_num))
                dd_2018 = report_cls.report(self,'2018',str(q_num))
                dd_2017 = report_cls.report(self,'2017',str(q_num))
                dd_2016 = report_cls.report(self,'2016',str(q_num))
                
                # 한개 제외하고 회사명,업종명 모두 drop 해주기
                dd_2019 = dd_2019.drop(['종목코드','업종명'], axis=1)
                dd_2018 = dd_2018.drop(['종목코드','업종명'], axis=1)
                dd_2017 = dd_2017.drop(['종목코드','업종명'], axis=1)
                dd_2016 = dd_2016.drop(['종목코드','업종명'], axis=1)
                
                alldata = pd.merge(dd_2020,dd_2019,how='outer',on=['회사명'])
                alldata = pd.merge(alldata,dd_2018,how='outer',on=['회사명'])
                alldata = pd.merge(alldata,dd_2017,how='outer',on=['회사명'])
                alldata = pd.merge(alldata,dd_2016,how='outer',on=['회사명'])
        
            # csv로저장
            alldata.rename(columns={'회사명':'종목명'}, inplace=True)
            alldata.to_csv('F:/JusikData/report_csv/report_make/재무정보_'+str(q_num)+'분기.csv', encoding='cp949', index = False)
                
        print('재무제표 csv 파일 생성 완료')
   
# # 실행 테스트
# conn = report_cls()
# #conn.report('2017', '4')
# conn.Report_Make()

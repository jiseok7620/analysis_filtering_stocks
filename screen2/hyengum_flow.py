# 영업, 투자, 재무 현금흐름을 분석해서 투자에 부적정한 기업을 걸러내기
# 영업활동 현금흐름
# 2021년 : ifrs-full_CashFlowsFromUsedInOperatingActivities

# 투자활동 현금흐름
# 2021년 : ifrs-full_CashFlowsFromUsedInInvestingActivities

# 재무활동 현금흐름
# 2021년 : ifrs-full_CashFlowsFromUsedInFinancingActivities

import pandas as pd
import datetime

# 년도, 분기, 연결여부 별 데이터프레임 형성하기
class hyen_flow_cls:
    def result_flow(self,year,q, young, to, jae):
        # csv를 데이터프레임으로 저장하기
        self.df_hyen_y = pd.read_csv('F:/JusikData/report_csv/report/'+year+'_'+q+'_hyen_y.csv', encoding='cp949')
        
        # 필요한 열만 가져오기
        self.df_hyen_y = self.df_hyen_y.iloc[:,[1,2,4,5,10,11,12]]
        
        ## 연결 현금흐름표에서 데이터가져오기
        ## 가져온 데이터에서 영업, 투자, 재무만 가져오기
        hyen1_y = self.df_hyen_y[self.df_hyen_y['항목코드'].isin(['ifrs_CashFlowsFromUsedInOperatingActivities', 'ifrs-full_CashFlowsFromUsedInOperatingActivities'])]
        hyen1_y.rename(columns={ hyen1_y.columns[6] : year+'_영업활동현금흐름_'+q}, inplace=True)
        
        # 투자활동현금흐름
        hyen2_y = self.df_hyen_y[self.df_hyen_y['항목코드'].isin(['ifrs_CashFlowsFromUsedInInvestingActivities', 'ifrs-full_CashFlowsFromUsedInInvestingActivities'])]
        hyen2_y.rename(columns={ hyen2_y.columns[6] : year+'_투자활동현금흐름_'+q}, inplace=True)
        
        # 재무활동현금흐름
        hyen3_y = self.df_hyen_y[self.df_hyen_y['항목코드'].isin(['ifrs_CashFlowsFromUsedInFinancingActivities', 'ifrs-full_CashFlowsFromUsedInFinancingActivities'])]
        hyen3_y.rename(columns={ hyen3_y.columns[6] : year+'_재무활동현금흐름_'+q}, inplace=True)
            
        # 병합하기위해 필요없는 컬럼 제거
        hyen2_y = hyen2_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        hyen3_y = hyen3_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)    
        
        # 병합    
        hyen_y = pd.merge(hyen1_y,hyen2_y, how='outer', on=['종목코드'])
        hyen_y = pd.merge(hyen_y,hyen3_y, how='outer', on=['종목코드'])
        hyen_y = hyen_y.drop_duplicates(['종목코드'])
        
        # 데이터의 ','를 제거하고 float 형식으로 바꾸기
        hyen_y.iloc[:,1:] = hyen_y.iloc[:,1:].replace(',','',regex=True)
        
        bb = 6
        row_count = len(hyen_y.columns)
        exit = True
                
        while exit:
            hyen_y.iloc[:,bb] = pd.to_numeric(hyen_y.iloc[:,bb], downcast='float')
            bb = bb + 1
            if bb == row_count:
                exit = False
        
        #print(hyen_y.dtypes)
        #print(hyen_y)
        
        ## 연결 현금흐름표에서 위기종목 거르기
        # 영업 -, 투자 +, 재무 +
        # 영업 -, 투자 +, 재무 -
        flow_name_y = []        
        
        for i in hyen_y.index :
            if young == '영업(+)':
                if hyen_y.loc[i, year+'_영업활동현금흐름_'+q] > 0:
                    if to == '투자(+)':
                        if hyen_y.loc[i, year+'_투자활동현금흐름_'+q] > 0:
                            if jae == '재무(+)':
                                if hyen_y.loc[i, year+'_재무활동현금흐름_'+q] > 0:
                                    flow_name_y.append(hyen_y.loc[i,'종목코드'])
                            else:
                                if hyen_y.loc[i, year+'_재무활동현금흐름_'+q] < 0:
                                    flow_name_y.append(hyen_y.loc[i,'종목코드'])
                    else:
                        if hyen_y.loc[i, year+'_투자활동현금흐름_'+q] < 0:
                            if jae == '재무(+)':
                                if hyen_y.loc[i, year+'_재무활동현금흐름_'+q] > 0:
                                    flow_name_y.append(hyen_y.loc[i,'종목코드'])
                            else:
                                if hyen_y.loc[i, year+'_재무활동현금흐름_'+q] < 0:
                                    flow_name_y.append(hyen_y.loc[i,'종목코드'])
                        
            else:
                if hyen_y.loc[i, year+'_영업활동현금흐름_'+q] < 0:
                    if to == '투자(+)':
                        if hyen_y.loc[i, year+'_투자활동현금흐름_'+q] > 0:
                            if jae == '재무(+)':
                                if hyen_y.loc[i, year+'_재무활동현금흐름_'+q] > 0:
                                    flow_name_y.append(hyen_y.loc[i,'종목코드'])
                            else:
                                if hyen_y.loc[i, year+'_재무활동현금흐름_'+q] < 0:
                                    flow_name_y.append(hyen_y.loc[i,'종목코드'])
                    else:
                        if hyen_y.loc[i, year+'_투자활동현금흐름_'+q] < 0:
                            if jae == '재무(+)':
                                if hyen_y.loc[i, year+'_재무활동현금흐름_'+q] > 0:
                                    flow_name_y.append(hyen_y.loc[i,'종목코드'])
                            else:
                                if hyen_y.loc[i, year+'_재무활동현금흐름_'+q] < 0:
                                    flow_name_y.append(hyen_y.loc[i,'종목코드'])
        
        #print(flow_name_y)
        #print('연결현금흐름:',len(flow_name_y),'개')
        
        ## 리턴값 입력하기 ##
        return flow_name_y
        #################
        
# 테스트
#conn = hyen_flow_cls()
#conn.result_flow('2020', '2', '영업(+)', '투자(+)', '재무(+)')
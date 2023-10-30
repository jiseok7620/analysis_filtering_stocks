# 분기별 재무제표 데이터 중 증가율을 구할 데이터를 가져와서 증가율 계산하여 데이터 프레임 만들기

import pandas as pd
import os
import datetime
import openpyxl

class Report_Roi:
    def Report_Roi_Make(self, year, q):
        #### csv를 데이터프레임으로 저장하기####
        self.df_hyen_y = pd.read_csv('F:/JusikData/report_csv/report/'+year+'_'+q+'_hyen_y.csv', encoding='cp949')
        self.df_jaemu_y = pd.read_csv('F:/JusikData/report_csv/report/'+year+'_'+q+'_jaemu_y.csv', encoding='cp949')
        self.df_posonik_y = pd.read_csv('F:/JusikData/report_csv/report/'+year+'_'+q+'_posonik_y.csv', encoding='cp949')
        self.df_sonik_y = pd.read_csv('F:/JusikData/report_csv/report/'+year+'_'+q+'_sonik_y.csv', encoding='cp949')
        ########################################
        #
        #
        #
        #
        #### 데이터 정제하기(필요한 열만 추출) ####
        self.df_hyen_y = self.df_hyen_y.iloc[:,[1,2,4,5,10,11,12]]
        self.df_jaemu_y = self.df_jaemu_y.iloc[:,[1,2,4,5,10,11,12]]
        self.df_posonik_y = self.df_posonik_y.iloc[:,[1,2,4,5,10,11,12]]
        self.df_sonik_y = self.df_sonik_y.iloc[:,[1,2,4,5,10,11,12]]
        ########################################
        #
        #
        #
        #
        #### 재무상태표_연결에서 필요한 데이터만 가져오기 ####
        # 자산총계
        jaemu1_y = self.df_jaemu_y[self.df_jaemu_y['항목코드'].isin(['ifrs_Assets', 'ifrs-full_Assets'])]
        jaemu1_y.rename(columns={ jaemu1_y.columns[6] : year+'_자산총계_'+q}, inplace=True)
        
        # 부채총계
        jaemu2_y = self.df_jaemu_y[self.df_jaemu_y['항목코드'].isin(['ifrs_Liabilities', 'ifrs-full_Liabilities'])]
        jaemu2_y.rename(columns={ jaemu2_y.columns[6] : year+'_부채총계_'+q}, inplace=True)

        # 자본총계
        jaemu3_y = self.df_jaemu_y[self.df_jaemu_y['항목코드'].isin(['ifrs_Equity', 'ifrs-full_Equity'])]
        jaemu3_y.rename(columns={ jaemu3_y.columns[6] : year+'_자본총계_'+q}, inplace=True)
        
        # 병합하기위해 필요없는 컬럼 제거
        jaemu2_y = jaemu2_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        jaemu3_y = jaemu3_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        
        # 병합
        jaemu_y = pd.merge(jaemu1_y,jaemu2_y,how='outer',on=['종목코드'])
        jaemu_y = pd.merge(jaemu_y,jaemu3_y,how='outer',on=['종목코드'])
        jaemu_y = jaemu_y.drop_duplicates(['종목코드'])
        
        # 확인
        # print(jaemu_y)
        ########################################       
        #
        #
        #
        #
        #### 포괄손익계산서_연결에서 필요한 데이터만 가져오기 ####
        # 매출액
        posonik1_y = self.df_posonik_y[self.df_posonik_y['항목코드'].isin(['ifrs_Revenue', 'ifrs-full_Revenue'])]
        posonik1_y.rename(columns={ posonik1_y.columns[6] : year+'_매출액_'+q}, inplace=True)
        
        # 영업이익
        posonik2_y = self.df_posonik_y[self.df_posonik_y['항목코드'].isin(['dart_OperatingIncomeLoss'])]
        posonik2_y.rename(columns={ posonik2_y.columns[6] : year+'_영업이익_'+q}, inplace=True)
        
        # 당기순이익
        posonik3_y = self.df_posonik_y[self.df_posonik_y['항목코드'].isin(['ifrs_ProfitLoss', 'ifrs-full_ProfitLoss'])]
        posonik3_y.rename(columns={ posonik3_y.columns[6] : year+'_당기순이익_'+q}, inplace=True)
        
        # 병합하기위해 필요없는 컬럼 제거
        posonik2_y = posonik2_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        posonik3_y = posonik3_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        
        # 병합
        posonik_y = pd.merge(posonik1_y,posonik2_y,how='outer',on=['종목코드'])
        posonik_y = pd.merge(posonik_y,posonik3_y,how='outer',on=['종목코드'])
        posonik_y = posonik_y.drop_duplicates(['종목코드'])
        
        # 포괄손익에 없는것들 손익계산서에서 찾기
        sonik1_y = self.df_sonik_y[self.df_sonik_y['항목코드'].isin(['ifrs_Revenue', 'ifrs-full_Revenue'])]
        sonik1_y.rename(columns={ sonik1_y.columns[6] : year+'_매출액(손익)_'+q}, inplace=True)
        sonik2_y = self.df_sonik_y[self.df_sonik_y['항목코드'].isin(['dart_OperatingIncomeLoss'])]
        sonik2_y.rename(columns={ sonik2_y.columns[6] : year+'_영업이익(손익)_'+q}, inplace=True)
        sonik3_y = self.df_sonik_y[self.df_sonik_y['항목코드'].isin(['ifrs_ProfitLoss', 'ifrs-full_ProfitLoss'])]
        sonik3_y.rename(columns={ sonik3_y.columns[6] : year+'_당기순이익(손익)_'+q}, inplace=True)
        sonik1_y = sonik1_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        sonik2_y = sonik2_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        sonik3_y = sonik3_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        sonik_y = pd.merge(sonik1_y,sonik2_y,how='outer',on=['종목코드'])
        sonik_y = pd.merge(sonik_y,sonik3_y,how='outer',on=['종목코드'])
        sonik_y = sonik_y.drop_duplicates(['종목코드'])
        
        # 손익계산서와 포괄손익계산서 병합
        posonik_y = pd.merge(posonik_y,sonik_y,how='outer',on=['종목코드'])
        
        # 확인
        #print(posonik_y)
        ######################################################
        #
        #
        #
        #
        #### 전체데이터 합치기 ####
        # hyen_y, jaemu_y, posonik_y
        # 1. 데이터에서 필요없는 열 제거
        jaemu_y = jaemu_y.drop(['업종','업종명','항목명','항목코드'], axis=1)
        posonik_y = posonik_y.drop(['회사명','업종','업종명','항목명','항목코드'], axis=1)
        
        # 2. 데이터 합치기
        # merge : pd.merge(데이터프레임1, 데이터프레임2, how='방법', on=None)
        # on=None 이면 교집합 조인을 하게됨
        final_data = pd.merge(jaemu_y,posonik_y,how='outer',on=['종목코드'])
        final_data = final_data.drop_duplicates(['종목코드'])
        
        # 3. 확인
        #print(final_data)
        
        # 4. 리턴값
        return final_data
    
    #### 증가, 감소율을 구하는 함수 ####
    def Roi_Make(self):
        print('증가,감소 csv 파일 생성 시작')
        
        # 1~4분기 세기 변수 : q_num
        # while문을 계속할지 중단할지 변수 : go_on
        q_num = 0
        go_on = True
        
        # nowDate = 현재년도 ex) 2021
        now = datetime.datetime.now()
        nowDate = now.strftime('%Y')
        
        # 연도 변수 선언
        year = nowDate[0:4]
        
        # 반복문의 실행 -> 1~4분기까지 반복
        while go_on:
            q_num = q_num + 1
            
            if q_num == 5 :
                break
        
            # 해당 경로에 해당 파일이 있으면 최신년도 해당분기를 포함해서 증가율 계산 진행
            # 없다면 해당 분기는 제외하고 증가율 계산
            directory = "F:/JusikData/report_csv/report/" + nowDate + "_" + str(q_num) + "_jaemu_y.csv"
            
            if os.path.exists(directory):
                # 년도별 데이터 프레임 만들기
                # 년마다 해당 년도 변수 만들기
                dd_2021 = Report_Roi.Report_Roi_Make(self,'2021',str(q_num))
                dd_2020 = Report_Roi.Report_Roi_Make(self,'2020',str(q_num))
                dd_2019 = Report_Roi.Report_Roi_Make(self,'2019',str(q_num))
                dd_2018 = Report_Roi.Report_Roi_Make(self,'2018',str(q_num))
                dd_2017 = Report_Roi.Report_Roi_Make(self,'2017',str(q_num))
                dd_2016 = Report_Roi.Report_Roi_Make(self,'2016',str(q_num))
                
                # 한개 제외하고 회사명 모두 drop 해주기
                dd_2020 = dd_2020.drop(['회사명'], axis=1)
                dd_2019 = dd_2019.drop(['회사명'], axis=1)
                dd_2018 = dd_2018.drop(['회사명'], axis=1)
                dd_2017 = dd_2017.drop(['회사명'], axis=1)
                dd_2016 = dd_2016.drop(['회사명'], axis=1)
                
                # 데이터 프레임 병합하기
                alldata = pd.merge(dd_2021,dd_2020,how='outer',on=['종목코드'])
                alldata = pd.merge(alldata,dd_2019,how='outer',on=['종목코드'])
                alldata = pd.merge(alldata,dd_2018,how='outer',on=['종목코드'])
                alldata = pd.merge(alldata,dd_2017,how='outer',on=['종목코드'])
                alldata = pd.merge(alldata,dd_2016,how='outer',on=['종목코드'])
        
            else:
                dd_2020 = Report_Roi.Report_Roi_Make(self,'2020',str(q_num))
                dd_2019 = Report_Roi.Report_Roi_Make(self,'2019',str(q_num))
                dd_2018 = Report_Roi.Report_Roi_Make(self,'2018',str(q_num))
                dd_2017 = Report_Roi.Report_Roi_Make(self,'2017',str(q_num))
                dd_2016 = Report_Roi.Report_Roi_Make(self,'2016',str(q_num))
                
                # 한개 제외하고 회사명 모두 drop 해주기
                dd_2019 = dd_2019.drop(['회사명'], axis=1)
                dd_2018 = dd_2018.drop(['회사명'], axis=1)
                dd_2017 = dd_2017.drop(['회사명'], axis=1)
                dd_2016 = dd_2016.drop(['회사명'], axis=1)
                
                alldata = pd.merge(dd_2020,dd_2019,how='outer',on=['종목코드'])
                alldata = pd.merge(alldata,dd_2018,how='outer',on=['종목코드'])
                alldata = pd.merge(alldata,dd_2017,how='outer',on=['종목코드'])
                alldata = pd.merge(alldata,dd_2016,how='outer',on=['종목코드'])
        
            # 데이터의 ,빼주기
            alldata.iloc[:,2:] = alldata.iloc[:,2:].replace(',','',regex=True)
            
            # 전체를 numeric으로 변환하기
            a = 2
            row_count = len(alldata.columns)
            exit = True
            
            while exit:
                alldata.iloc[:,a] = pd.to_numeric(alldata.iloc[:,a], downcast='float')
                a = a + 1
                if a == row_count:
                    exit = False
            
            # 해당 경로에 해당 파일이 있으면 최신년도 해당분기를 포함해서 증가율 계산 진행
            if os.path.exists(directory):
                # 증가, 감소율 구하기
                # 1년마다 최신화 -> 해당 년도 추가 필요
                year_list = [('2017','2016'),('2018','2017'),('2019','2018'),('2020','2019'),('2021','2020')]
                resultdata = alldata[['종목코드','회사명']]
                
                for i,j in year_list :
                    resultdata[i+'_자산증가율_'+str(q_num)] = (alldata[i+'_자산총계_'+str(q_num)] - alldata[j+'_자산총계_'+str(q_num)]) / alldata[j+'_자산총계_'+str(q_num)] * 100
                    resultdata[i+'_부채증가율_'+str(q_num)] = (alldata[i+'_부채총계_'+str(q_num)] - alldata[j+'_부채총계_'+str(q_num)]) / alldata[j+'_부채총계_'+str(q_num)] * 100
                    resultdata[i+'_자본증가율_'+str(q_num)] = (alldata[i+'_자본총계_'+str(q_num)] - alldata[j+'_자본총계_'+str(q_num)]) / alldata[j+'_자본총계_'+str(q_num)] * 100
                    resultdata[i+'_매출액증가율_'+str(q_num)] = (alldata[i+'_매출액_'+str(q_num)] - alldata[j+'_매출액_'+str(q_num)]) / alldata[j+'_매출액_'+str(q_num)] * 100
                    resultdata[i+'_영업이익증가율_'+str(q_num)] = (alldata[i+'_영업이익_'+str(q_num)] - alldata[j+'_영업이익_'+str(q_num)]) / alldata[j+'_영업이익_'+str(q_num)] * 100
                    resultdata[i+'_당기순이익증가율_'+str(q_num)] = (alldata[i+'_당기순이익_'+str(q_num)] - alldata[j+'_당기순이익_'+str(q_num)]) / alldata[j+'_당기순이익_'+str(q_num)] * 100
                    resultdata[i+'_매출액증가율(손익)_'+str(q_num)] = (alldata[i+'_매출액(손익)_'+str(q_num)] - alldata[j+'_매출액(손익)_'+str(q_num)]) / alldata[j+'_매출액(손익)_'+str(q_num)] * 100
                    resultdata[i+'_영업이익증가율(손익)_'+str(q_num)] = (alldata[i+'_영업이익(손익)_'+str(q_num)] - alldata[j+'_영업이익(손익)_'+str(q_num)]) / alldata[j+'_영업이익(손익)_'+str(q_num)] * 100
                    resultdata[i+'_당기순이익증가율(손익)_'+str(q_num)] = (alldata[i+'_당기순이익(손익)_'+str(q_num)] - alldata[j+'_당기순이익(손익)_'+str(q_num)]) / alldata[j+'_당기순이익(손익)_'+str(q_num)] * 100
                
                resultdata.to_csv('F:/JusikData/report_csv/report_roi/증가율_'+str(q_num)+'분기.csv', encoding='cp949', index = False)

            else:
                # 증가, 감소율 구하기
                # 1년마다 최신화 -> 해당 년도 추가 필요
                year_list = [('2017','2016'),('2018','2017'),('2019','2018'),('2020','2019')]
                resultdata = alldata[['종목코드','회사명']]
                
                for i,j in year_list :
                    resultdata[i+'_자산증가율_'+str(q_num)] = (alldata[i+'_자산총계_'+str(q_num)] - alldata[j+'_자산총계_'+str(q_num)]) / alldata[j+'_자산총계_'+str(q_num)] * 100
                    resultdata[i+'_부채증가율_'+str(q_num)] = (alldata[i+'_부채총계_'+str(q_num)] - alldata[j+'_부채총계_'+str(q_num)]) / alldata[j+'_부채총계_'+str(q_num)] * 100
                    resultdata[i+'_자본증가율_'+str(q_num)] = (alldata[i+'_자본총계_'+str(q_num)] - alldata[j+'_자본총계_'+str(q_num)]) / alldata[j+'_자본총계_'+str(q_num)] * 100
                    resultdata[i+'_매출액증가율_'+str(q_num)] = (alldata[i+'_매출액_'+str(q_num)] - alldata[j+'_매출액_'+str(q_num)]) / alldata[j+'_매출액_'+str(q_num)] * 100
                    resultdata[i+'_영업이익증가율_'+str(q_num)] = (alldata[i+'_영업이익_'+str(q_num)] - alldata[j+'_영업이익_'+str(q_num)]) / alldata[j+'_영업이익_'+str(q_num)] * 100
                    resultdata[i+'_당기순이익증가율_'+str(q_num)] = (alldata[i+'_당기순이익_'+str(q_num)] - alldata[j+'_당기순이익_'+str(q_num)]) / alldata[j+'_당기순이익_'+str(q_num)] * 100
                    resultdata[i+'_매출액증가율(손익)_'+str(q_num)] = (alldata[i+'_매출액(손익)_'+str(q_num)] - alldata[j+'_매출액(손익)_'+str(q_num)]) / alldata[j+'_매출액(손익)_'+str(q_num)] * 100
                    resultdata[i+'_영업이익증가율(손익)_'+str(q_num)] = (alldata[i+'_영업이익(손익)_'+str(q_num)] - alldata[j+'_영업이익(손익)_'+str(q_num)]) / alldata[j+'_영업이익(손익)_'+str(q_num)] * 100
                    resultdata[i+'_당기순이익증가율(손익)_'+str(q_num)] = (alldata[i+'_당기순이익(손익)_'+str(q_num)] - alldata[j+'_당기순이익(손익)_'+str(q_num)]) / alldata[j+'_당기순이익(손익)_'+str(q_num)] * 100
                    
                resultdata.to_csv('F:/JusikData/report_csv/report_roi/증가율_'+str(q_num)+'분기.csv', encoding='cp949', index = False)
        
        print('증가,감소 csv 파일 생성 완료!')
                
# 실행 테스트
#aa = Report_Roi()
#aa.Roi_Make()
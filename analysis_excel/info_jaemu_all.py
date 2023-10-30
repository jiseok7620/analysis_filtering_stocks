import openpyxl
import pandas as pd

class info_jaemu_all_cls:
    def exe_info_jaemu_all(self,name,dd, q_num):
        ##---------------------------------------------------------------------##
        # dd의 년, 월, 일 나누기
        dd_y = int(str(dd)[0:4])
        dd_m = int(str(dd)[4:6])
        dd_d = int(str(dd)[6:8])
        
        # 년도, 분기 배열 만들기
        arr_yago = [dd_y,dd_y-1,dd_y-2,dd_y-3]
        arr_q = [1,2,3,4]
        
        for year in arr_yago:
            for q in arr_q :
                if year != dd_y and q <= q_num and year >= 2016:
                    ## csv를 데이터프레임으로 저장하기 ##
                    df_hyen = pd.read_csv('report_csv/report/'+str(year)+'_'+str(q)+'_hyen.csv', encoding='cp949')
                    df_hyen_y = pd.read_csv('report_csv/report/'+str(year)+'_'+str(q)+'_hyen_y.csv', encoding='cp949')
                    df_jaemu = pd.read_csv('report_csv/report/'+str(year)+'_'+str(q)+'_jaemu.csv', encoding='cp949')
                    df_jaemu_y = pd.read_csv('report_csv/report/'+str(year)+'_'+str(q)+'_jaemu_y.csv', encoding='cp949')
                    df_posonik = pd.read_csv('report_csv/report/'+str(year)+'_'+str(q)+'_posonik.csv', encoding='cp949')
                    df_posonik_y = pd.read_csv('report_csv/report/'+str(year)+'_'+str(q)+'_posonik_y.csv', encoding='cp949')
                    df_sonik = pd.read_csv('report_csv/report/'+str(year)+'_'+str(q)+'_sonik.csv', encoding='cp949')
                    df_sonik_y = pd.read_csv('report_csv/report/'+str(year)+'_'+str(q)+'_sonik_y.csv', encoding='cp949')
                    
                    ## 데이터 정제하기(필요한 열만 추출) ##
                    df_hyen = df_hyen.iloc[:,[0,1,2,4,5,10,11,12]]
                    df_hyen_y = df_hyen_y.iloc[:,[0,1,2,4,5,10,11,12]]
                    df_jaemu = df_jaemu.iloc[:,[0,1,2,4,5,10,11,12]]
                    df_jaemu_y = df_jaemu_y.iloc[:,[0,1,2,4,5,10,11,12]]
                    df_posonik = df_posonik.iloc[:,[0,1,2,4,5,10,11,12]]
                    df_posonik_y = df_posonik_y.iloc[:,[0,1,2,4,5,10,11,12]]
                    df_sonik = df_sonik.iloc[:,[0,1,2,4,5,10,11,12]]        
                    df_sonik_y = df_sonik_y.iloc[:,[0,1,2,4,5,10,11,12]]
                    
                    ## 새열 추가하기
                    df_hyen['구분'] = str(year) + '_' + str(q)
                    df_hyen_y['구분'] = str(year) + '_' + str(q)
                    df_jaemu['구분'] = str(year) + '_' + str(q)
                    df_jaemu_y['구분'] = str(year) + '_' + str(q)
                    df_posonik['구분'] = str(year) + '_' + str(q)
                    df_posonik_y['구분'] = str(year) + '_' + str(q)
                    df_sonik['구분'] = str(year) + '_' + str(q)
                    df_sonik_y['구분'] = str(year) + '_' + str(q)
                    
                    ## 컬럼명 일치시키기
                    df_hyen.columns = ['재무제표종류', '종목코드', '회사명', '업종', '업종명', '항목코드', '항목명', '당기', '구분']
                    df_hyen_y.columns = ['재무제표종류', '종목코드', '회사명', '업종', '업종명', '항목코드', '항목명', '당기', '구분']
                    df_jaemu.columns = ['재무제표종류', '종목코드', '회사명', '업종', '업종명', '항목코드', '항목명', '당기', '구분']
                    df_jaemu_y.columns = ['재무제표종류', '종목코드', '회사명', '업종', '업종명', '항목코드', '항목명', '당기', '구분']
                    df_posonik.columns = ['재무제표종류', '종목코드', '회사명', '업종', '업종명', '항목코드', '항목명', '당기', '구분']
                    df_posonik_y.columns = ['재무제표종류', '종목코드', '회사명', '업종', '업종명', '항목코드', '항목명', '당기', '구분']
                    df_sonik.columns = ['재무제표종류', '종목코드', '회사명', '업종', '업종명', '항목코드', '항목명', '당기', '구분']
                    df_sonik_y.columns = ['재무제표종류', '종목코드', '회사명', '업종', '업종명', '항목코드', '항목명', '당기', '구분']
                    
                    ## 회사명이 name인 것들만 추출
                    df_hyen = df_hyen[df_hyen['회사명'] == name]
                    df_hyen_y = df_hyen_y[df_hyen_y['회사명'] == name]
                    df_jaemu = df_jaemu[df_jaemu['회사명'] == name]
                    df_jaemu_y = df_jaemu_y[df_jaemu_y['회사명'] == name]
                    df_posonik = df_posonik[df_posonik['회사명'] == name]
                    df_posonik_y = df_posonik_y[df_posonik_y['회사명'] == name]
                    df_sonik = df_sonik[df_sonik['회사명'] == name]
                    df_sonik_y = df_sonik_y[df_sonik_y['회사명'] == name]
                    
                    ## 전체 합치기
                    data_part = pd.concat([df_hyen,df_hyen_y,df_jaemu,df_jaemu_y,df_posonik,df_posonik_y,df_sonik,df_sonik_y])
                    
                    ## 인덱스 초기화
                    data_part = data_part.reset_index(drop=True)
                    
                    # 시트명 만들기
                    sheet_name = str(year) + "_" + str(q)
                    
                    # 엑셀로 저장
                    with pd.ExcelWriter('analysis_csv/HJS/'+name+'_'+str(dd)+'.xlsx', mode='a', engine='openpyxl') as writer:
                        data_part.to_excel(writer, sheet_name=str(sheet_name))
                    
                    '''
                    if q == 1:
                        data_part1 = data_part
                    elif q == 2:
                        data_part2 = data_part
                    elif q == 3:
                        data_part3 = data_part
                    else :
                        data_part4 = data_part
                        
                # 파트 데이터 합치기
                if q_num == 1:
                    data_all = data_part1
                elif q_num == 2:
                    data_all = pd.concat([data_part1,data_part2])
                elif q_num == 3:
                    data_all = pd.concat([data_part1,data_part2,data_part3])
                elif q_num == 4:
                    data_all = pd.concat([data_part1,data_part2,data_part3,data_part4])
            
            
            ## 인덱스 초기화
            data_all = data_all.reset_index(drop=True)
            print(data_all)
            
            # 엑셀로 저장
            with pd.ExcelWriter('F:/JusikData/analysis_csv/HJS/'+name+'_'+str(dd)+'.xlsx', mode='a', engine='openpyxl') as writer:
                data_all.to_excel(writer, sheet_name=str(year))
            '''
            
        
#conn = info_jaemu_all_cls()
#conn.exe_info_jaemu_all('국동',20200226)
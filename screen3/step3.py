import pandas as pd
import os
import numpy as np
import csv
import datetime

class step3_cls:
    def make_step3(self, number, dd, dnd, nb):
        
        arr_name = ['증가', '감소'] # 두 csv파일 모두 돌리기 위해서
        #arr_name = ['증가'] # 두 csv파일 모두 돌리기 위해서


        
        for name in arr_name:
            dday = dd # d일 전
            dnday = dnd # d + n일 전
            nbar = nb # n%의 봉
            
            arr_move = []
            arr_trade1 = [] # 기준일의 거래량이 d일전 거래량 최대의 ????배
            arr_trade2 = [] # 기준일의 거래량이 d+n일전 거래량 최대의 ????배
            arr_trade3 = [] # d일전 기준일의 거래량보다 많은 거래량의 수 ????개
            arr_trade4 = [] # d+n일전 기준일의 거래량보다 많은 거래량의 수 ????개
            arr_trade5 = [] # 6개월전 기분일의 거래량보다 많은 거래량의 수 ????개
            arr_trade6 = [] # 1년전 기준일의 거래량보다 많은 거래량의 수 ????개
            arr_min1 = [] # 기준일 저가가 d일전 최소값의 ????배
            arr_min2 = [] # d일전 최소값이 d+n일전 최소값의 ????배
            arr_close1 = [] # 기준일의 종가가 d일전 최소값의 ????배
            arr_close2 = [] # 기준일의 종가가 d+n일 전 최소값의 ????배 
            arr_bar1 = [] # d일 사이에 n% 이상의 봉이 ????개 
            arr_bar2 = [] # d+n일 사이에 n% 이상의 봉이 ????개
            arr_bar3 = [] # 6개월 사이에 n% 이상의 봉이 ????개
            arr_bar4 = [] # 1년 사이에 n% 이상의 봉이 ????개
            arr_mibar1 = [] # d일 사이에 -n% 이하의 봉이 ????개
            arr_mibar2 = [] # d+n일 사이에 -n% 이하의 봉이 ????개
            arr_mibar3 = [] # 6개월 사이에 -n% 이하의 봉이 ????개
            arr_mibar4 = [] # 1년 사이에 -n% 이하의 봉이 ????개
            arr_fmlow = [] # 1년전(240봉)의 최소값 일자부터 기준일의 고가보다 높았던 가격의 봉 수 = ????
            arr_maxclmi1 = [] # 1년전의 최대값이 기준일 고가의 ????배
            arr_maxclmi2 = [] # 기준일 저가가 1년전의 최소값의 ????배
            arr_maxclmi3 = [] # 1년전 최대값과 1년전 최소값의 중간값이 기준일 종가의 ????배
            arr_maxmin1 = [] # 1년전의 최대값이 1년전의 최소값의 ????배 
            
            num = number
            #data = pd.read_csv('F:/JusikData/analysis_csv/step/step2/'+name+'_'+str(num)+'.csv', encoding='cp949')
            data = pd.read_excel('F:/JusikData/analysis_csv/step/step2/증가감소_'+str(num)+'.xlsx', sheet_name=name, engine='openpyxl')
        
            for i in data.index:
                print('step3_',data.iloc[i]['종목명'], '...진행중')
                
                # 자료가져오기
                data_ori = pd.read_csv("F:/JusikData/oneday_csv/onedaydata/"+data.iloc[i]['종목명']+'/'+data.iloc[i]['종목명']+'.csv', encoding='cp949')
                data_ori['5이평'] = data_ori['종가'].rolling(window=5).mean()
                data_ori['20이평'] = data_ori['종가'].rolling(window=20).mean()
                
                # 해당 기준일의 인덱스 구하기
                index_num = data_ori[data_ori['일자'] == data.iloc[i]['기준일']].index.tolist()
                
                
                
                ## 종가 > 5일 > 20일 확인하기 ##
                try:
                    if data_ori.iloc[index_num[0]]['20이평'] < data_ori.iloc[index_num[0]]['5이평'] and data_ori.iloc[index_num[0]]['5이평'] < data_ori.iloc[index_num[0]]['종가']:
                        arr_move.append('T')
                    else:    
                        arr_move.append('F')
                except Exception as e :
                    arr_move.append('Fail')
                    print('arr_move', e)
                    
                    
                    
                ## 기준일의 거래량이 더 많아야 하는지 확인 ##
                ## 기준일의 거래량이 많은건 언제까지 허용인지 확인 ##
                # 기준일의 거래량이 dday전 거래량 최대의 ????배
                nowday_trade = data_ori.iloc[index_num[0]]['거래량']
                dday_trade_max = data_ori[index_num[0]-dday:index_num[0]-1]['거래량'].max()
                dnday_trade_max = data_ori[index_num[0]-dnday:index_num[0]-1]['거래량'].max()
                
                try:
                    if index_num[0] > dday :
                        trade1 = nowday_trade / dday_trade_max
                        arr_trade1.append(trade1)
                    else :
                        arr_trade1.append('F')
                except Exception as e :
                    arr_trade1.append('Fail') 
                    print('arr_trade1', e)
                
                # 기준일의 거래량이 dnday전 거래량 최대의 ????배
                try:
                    if index_num[0] > dnday :
                        trade2 = nowday_trade / dnday_trade_max
                        arr_trade2.append(trade2)
                    else :   
                        arr_trade2.append('F') 
                except Exception as e:
                    arr_trade2.append('Fail') 
                    print('arr_trade2', e)
                
                # dday전동안 기준일의 거래량보다 많은 거래량의 수 ????개
                try:
                    if index_num[0] > dday :
                        data_part1 = data_ori[index_num[0]-dday:index_num[0]-1]
                        trade3 = len(data_part1[data_part1['거래량'] >= nowday_trade])
                        arr_trade3.append(trade3)
                    else :
                        arr_trade3.append('F')
                except Exception as e:
                    arr_trade3.append('Fail')
                    print('arr_trade3', e)     
                
                # dnday전동안 기준일의 거래량보다 많은 거래량의 수 ????개
                try:
                    if index_num[0] > dnday :
                        data_part2 = data_ori[index_num[0]-dnday:index_num[0]-1]
                        trade4 = len(data_part2[data_part2['거래량'] >= nowday_trade])
                        arr_trade4.append(trade4)
                    else :    
                        arr_trade4.append('F')
                except Exception as e:
                    arr_trade4.append('Fail') 
                    print('arr_trade4', e) 
        
                # 6개월(120)전동안 기준일의 거래량보다 많은 거래량의 수 ????개
                try:
                    if index_num[0] > 120 :
                        data_part3 = data_ori[index_num[0]-120:index_num[0]-1]
                        trade5 = len(data_part3[data_part3['거래량'] >= nowday_trade])
                        arr_trade5.append(trade5)
                    else :    
                        arr_trade5.append('F')
                except Exception as e:
                    arr_trade5.append('Fail')    
                    print('arr_trade5', e)     
                    
                # 1년전(240) 기준일의 거래량보다 많은 거래량의 수 ????개
                try:
                    if index_num[0] > 240 :
                        data_part4 = data_ori[index_num[0]-240:index_num[0]-1]
                        trade6 = len(data_part4[data_part4['거래량'] >= nowday_trade])
                        arr_trade6.append(trade6)
                    else :    
                        arr_trade6.append('F')
                except Exception as e:
                    arr_trade6.append('Fail')
                    print('arr_trade6', e) 
        
        
        
                ## d+n일, d일, 기준일 순으로 최소값이 점점 증가하는지 확인 ##
                # 기준일 저가가 dday전 최소값의 ????배
                nowday_low = data_ori.iloc[index_num[0]]['저가']
                dday_low_min = data_ori[index_num[0]-dday:index_num[0]-1]['저가'].min()
                dnday_low_min = data_ori[index_num[0]-dnday:index_num[0]-1]['저가'].min()
                
                try:
                    if index_num[0] > dday :
                        min1 = nowday_low / dday_low_min
                        arr_min1.append(min1)
                    else :
                        arr_min1.append('F')
                except Exception as e:
                    arr_min1.append('Fail')  
                    print('arr_min1', e)   
                
                # dday전 최소값이 dnday전 최소값의 ????배
                try:
                    if index_num[0] > dnday :
                        min2 = dday_low_min / dnday_low_min
                        arr_min2.append(min2)
                    else :
                        arr_min2.append('F')
                except Exception as e:
                    arr_min2.append('Fail')  
                    print('arr_min2', e)   
                
                
                ## 기준일의 종가가 d, d+n일 최소값에 비해 너무오르진 않았는지 확인 ##
                # 기준일의 종가가 dday전 최소값의 ????배
                nowday_close = data_ori.iloc[index_num[0]]['종가']
                try:
                    if index_num[0] > dday :
                        close1 = nowday_close / dday_low_min
                        arr_close1.append(close1)
                    else :
                        arr_close1.append('F')
                except Exception as e:
                    arr_close1.append('Fail')  
                    print('arr_close1', e) 
                
                # 기준일의 종가가 dnday일전 최소값의 ????배 
                try:
                    if index_num[0] > dnday :
                        close2 = nowday_close / dnday_low_min
                        arr_close2.append(close2)
                    else :
                        arr_close2.append('F')
                except Exception as e:
                    arr_close2.append('Fail')  
                    print('arr_close2', e) 
                    
                    
                ## n% 이상의 봉이 n일 사이에 많이 있으면 문제가 생기는지 확인 ## 
                # dday사이에 n% 이상의 봉이 ????개 
                try:
                    if index_num[0] > dday :
                        data_bar1 = data_ori[index_num[0]-dday:index_num[0]-1]
                        bar1 = len(data_bar1[data_bar1['등락률'] >= nbar])
                        arr_bar1.append(bar1)
                    else :
                        arr_bar1.append('F')
                except Exception as e:
                    arr_bar1.append('Fail')
                    print('arr_bar1', e) 
                    
                # dnday일 사이에 n% 이상의 봉이 ????개
                try:
                    if index_num[0] > dnday :
                        data_bar2 = data_ori[index_num[0]-dnday:index_num[0]-1]
                        bar2 = len(data_bar2[data_bar2['등락률'] >= nbar])
                        arr_bar2.append(bar2)
                    else :
                        arr_bar2.append('F')
                except Exception as e:
                    arr_bar2.append('Fail')
                    print('arr_bar2', e) 
                    
                # 6개월 사이에 n% 이상의 봉이 ????개
                try:
                    if index_num[0] > 120 :
                        data_bar3 = data_ori[index_num[0]-120:index_num[0]-1]
                        bar3 = len(data_bar3[data_bar3['등락률'] >= nbar])
                        arr_bar3.append(bar3)
                    else :
                        arr_bar3.append('F')
                except Exception as e:
                    arr_bar3.append('Fail')
                    print('arr_bar3', e) 
                        
                # 1년 사이에 n% 이상의 봉이 ????개     
                try:
                    if index_num[0] > 240 :
                        data_bar4 = data_ori[index_num[0]-240:index_num[0]-1]
                        bar4 = len(data_bar4[data_bar4['등락률'] >= nbar])
                        arr_bar4.append(bar4)
                    else :
                        arr_bar4.append('F')
                except Exception as e:
                    arr_bar4.append('Fail') 
                    print('arr_bar4', e)    
                
                
                ## -n% 이하의 봉이 n일 사이에 많이 있으면 문제가 생기는지 확인 ##
                # dday일 사이에 -n% 이하의 봉이 ????개
                try:
                    if index_num[0] > dday :
                        data_mibar1 = data_ori[index_num[0]-dday:index_num[0]-1]
                        mibar1 = len(data_mibar1[data_mibar1['등락률'] <= -nbar])
                        arr_mibar1.append(mibar1)
                    else :
                        arr_mibar1.append('F')
                except Exception as e:
                    arr_mibar1.append('Fail')  
                    print('arr_mibar1', e)  
                
                # dnday일 사이에 -n% 이하의 봉이 ????개
                try:
                    if index_num[0] > dnday :
                        data_mibar2 = data_ori[index_num[0]-dnday:index_num[0]-1]
                        mibar2 = len(data_mibar2[data_mibar2['등락률'] <= -nbar])
                        arr_mibar2.append(mibar2)
                    else :
                        arr_mibar2.append('F')
                except Exception as e:
                    arr_mibar2.append('Fail') 
                    print('arr_mibar2', e)
                
                # 6개월 사이에 -n% 이하의 봉이 ????개
                try:
                    if index_num[0] > 120 :
                        data_mibar3 = data_ori[index_num[0]-120:index_num[0]-1]
                        mibar3 = len(data_mibar3[data_mibar3['등락률'] <= -nbar])
                        arr_mibar3.append(mibar3)
                    else :
                        arr_mibar3.append('F')
                except Exception as e:
                    arr_mibar3.append('Fail') 
                    print('arr_mibar3', e)
                
                # 1년 사이에 -n% 이하의 봉이 ????개
                try:
                    if index_num[0] > 240 :
                        data_mibar4 = data_ori[index_num[0]-240:index_num[0]-1]
                        mibar4 = len(data_mibar4[data_mibar4['등락률'] <= -nbar])
                        arr_mibar4.append(mibar4)
                    else :
                        arr_mibar4.append('F')                
                except Exception as e:
                    arr_mibar4.append('Fail') 
                    print('arr_mibar4', e)
                
                
                ## 기준일의 고가보다 높았던 가격의 봉 수가 많다면 그만큼 고점을 뚫으려는 시도가 있었을 것임 ##
                # 10봉차이 미만들은 그룹화하면 좋을 텐데
                # 1년전(240봉)의 최소값 일자부터 기준일의 고가보다 높았던 가격의 봉 수 = ????
                try:
                    if index_num[0] > 240 :
                        data_fmlow = data_ori[index_num[0]-240:index_num[0]-1]
                        index_num2 = data_fmlow[data_fmlow['저가'] == data_fmlow['저가'].min()].index.tolist()
                        data_fmlow2 = data_ori[index_num2[0]:index_num[0]-1]                    
                        fmlow = len(data_fmlow2[data_fmlow2['고가'] >= data_ori.iloc[index_num[0]]['고가']])
                        arr_fmlow.append(fmlow)
                    else :
                        arr_fmlow.append('F')                
                except Exception as e:
                    arr_fmlow.append('Fail') 
                    print('arr_fmlow', e)
                   
                ## 기준일과 최대값, 기준일과 최소값의 차이를 보기 => 종가의 위치 파악가능 ##
                # 1년전의 최대값이 기준일 최대값의 ????배\
                nowday_max = data_ori.iloc[index_num[0]]['고가']
                nowday_min = data_ori.iloc[index_num[0]]['저가']
                year_high_max = data_ori[index_num[0]-240:index_num[0]-1]['고가'].max()
                year_low_min = data_ori[index_num[0]-240:index_num[0]-1]['저가'].min()
                try:
                    if index_num[0] > 240 :
                        maxclmi1 = year_high_max / nowday_max
                        arr_maxclmi1.append(maxclmi1)
                    else :
                        arr_maxclmi1.append('F')
                except Exception as e:
                    arr_maxclmi1.append('Fail') 
                    print('arr_maxclmi1', e)
                    
                # 기준일 최소값이 1년전의 최소값의 ????배  
                try:
                    if index_num[0] > 240 :
                        maxclmi2 = nowday_min / year_low_min 
                        arr_maxclmi2.append(maxclmi2)
                    else :
                        arr_maxclmi2.append('F')
                except Exception as e:
                    arr_maxclmi2.append('Fail')
                    print('arr_maxclmi2', e)
                
                # 1년전 최대값과 1년전 최소값의 중간값이 기준일 종가의 ????배
                try:
                    if index_num[0] > 240 :
                        maxclmi3 = ((year_low_min + year_high_max) / 2) / nowday_close
                        arr_maxclmi3.append(maxclmi3)
                    else :
                        arr_maxclmi3.append('F')
                except Exception as e:
                    arr_maxclmi3.append('Fail')
                    print('arr_maxclmi3', e)
                
                
                ## 1년전 최대 등락률을 알수있음 ##
                # 1년전의 최대값이 1년전의 최소값의 몇 % 증가분인지
                try:
                    if index_num[0] > 240 :
                        maxmin1 = ((year_high_max - year_low_min) / year_low_min) * 100
                        arr_maxmin1.append(maxmin1)
                    else :
                        arr_maxmin1.append('F')
                except Exception as e:
                    arr_maxmin1.append('Fail')
                    print('arr_maxmin1', e)
                    
                    
            data['이평종가배열'] = arr_move # 종가 > 5일 > 20일 확인
            data['기준일거래량_'+str(dday)+'전의_몇배'] = arr_trade1 # 기준일의 거래량이 d일전 거래량 최대의 ????배
            data['기준일거래량_'+str(dnday)+'전의_몇배'] = arr_trade2 # 기준일의 거래량이 d+n일전 거래량 최대의 ????배
            data['기준일거래량_'+str(dday)+'전의_많은수'] = arr_trade3 # d일전 기준일의 거래량보다 많은 거래량의 수 ????개
            data['기준일거래량_'+str(dnday)+'전의_많은수'] = arr_trade4 # d+n일전 기준일의 거래량보다 많은 거래량의 수 ????개
            data['기준일거래량_6개월전의_많은수'] = arr_trade5 # 6개월전 기준일의 거래량보다 많은 거래량의 수 ????개
            data['기준일거래량_1년전의_많은수'] = arr_trade6 # 1년전 기준일의 거래량보다 많은 거래량의 수 ????개
            data['기준일저가_'+str(dday)+'전최소값의_몇배'] = arr_min1 # 기준일 저가가 d일전 최소값의 ????배
            data[str(dday)+'전최소값_'+str(dnday)+'전최소값의_몇배'] = arr_min2 # d일전 최소값이 d+n일전 최소값의 ????배
            data['기준일종가_'+str(dday)+'전최소값의_몇배'] = arr_close1 # 기준일의 종가가 d일전 최소값의 ????배
            data['기준일종가_'+str(dnday)+'전최소값의_몇배'] = arr_close2 # 기준일의 종가가 d+n일 전 최소값의 ????배 
            data[str(dday)+'전_'+str(nbar)+'%이상의_봉수'] = arr_bar1 # d일 사이에 n% 이상의 봉이 ????개 
            data[str(dnday)+'전_'+str(nbar)+'%이상의_봉수'] = arr_bar2 # d+n일 사이에 n% 이상의 봉이 ????개
            data['6개월전_'+str(nbar)+'%이상의_봉수'] = arr_bar3 # 6개월 사이에 n% 이상의 봉이 ????개
            data['1년전_'+str(nbar)+'%이상의_봉수'] = arr_bar4 # 1년 사이에 n% 이상의 봉이 ????개
            data[str(dday)+'전_'+str(nbar)+'%이하의_봉수'] = arr_mibar1 # d일 사이에 -n% 이하의 봉이 ????개
            data[str(dnday)+'전_'+str(nbar)+'%이하의_봉수'] = arr_mibar2 # d+n일 사이에 -n% 이하의 봉이 ????개
            data['6개월전_'+str(nbar)+'%이하의_봉수'] = arr_mibar3 # 6개월 사이에 -n% 이하의 봉이 ????개
            data['1년전_'+str(nbar)+'%이하의_봉수'] = arr_mibar4 # 1년 사이에 -n% 이하의 봉이 ????개
            data['기준일고가보다_높았던봉수(1년)'] = arr_fmlow # 1년전(240봉)의 최소값 일자부터 기준일의 고가보다 높았던 가격의 봉 수 = ????
            data['1년전최대값_기준일고가의_몇배'] = arr_maxclmi1 # 1년전의 최대값이 기준일 고가의 ????배
            data['기준일저가_1년전최소값의_몇배'] = arr_maxclmi2 # 기준일 저가가 1년전의 최소값의 ????배
            data['1년전최대최소의중간값_기준일종가의_몇배'] = arr_maxclmi3 # 1년전 최대값과 1년전 최소값의 중간값이 기준일 종가의 ????배
            data['1년전최대값_1년전최소값의_몇%증가'] = arr_maxmin1 # 1년전의 최대값이 1년전의 최소값의 몇%증가     
            
            #csv로 저장
            #data.to_csv('F:/JusikData/analysis_csv/step/step3/'+name+'_추가_'+str(num)+'.csv', encoding='cp949', index = False)
            
            # 형식 읽기
            inde_form = pd.read_excel('F:/JusikData/analysis_csv/step/step3/증가감소비교_Form.xlsx', engine='openpyxl')
            inde_form2 = pd.read_excel('F:/JusikData/analysis_csv/step/step3/증가내부비교_Form.xlsx', engine='openpyxl')
            
            # 엑셀로 저장
            if not os.path.exists('F:/JusikData/analysis_csv/step/step3/증가감소(추가)_'+str(num)+'.xlsx'):
                with pd.ExcelWriter('F:/JusikData/analysis_csv/step/step3/증가감소(추가)_'+str(num)+'.xlsx', mode='w', engine='openpyxl') as writer:
                    data.to_excel(writer, sheet_name=name, encoding='cp949', index=False)
                    writer.save()
            else:
                with pd.ExcelWriter('F:/JusikData/analysis_csv/step/step3/증가감소(추가)_'+str(num)+'.xlsx', mode='a', engine='openpyxl') as writer:
                    data.to_excel(writer, sheet_name=name, encoding='cp949', index=False)
                    inde_form.to_excel(writer, sheet_name='증가감소비교분석', encoding='cp949', header=False, index=False)
                    inde_form2.to_excel(writer, sheet_name='증가내부비교분석', encoding='cp949', header=False, index=False)
                    writer.save()
                    
                
#conn = step3_cls()
#conn.make_step3(1)
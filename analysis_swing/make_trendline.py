import pandas as pd
import numpy as np
import math
import time
import os
import mpl_finance
import matplotlib.pyplot as plt
from cmath import nan

class trendline_cls:
    def exe_trendline(self, name, edate):
        # 저장 경로
        path = 'F:/JusikData/API/data/'+name+'_'+edate+'.xlsx'

        # 시작일 설정(매수시점 일에서 2년전)
        #start = int(edate) - 20000
        #print(start)
        
        if os.path.isfile(path) :
            # 저장한 엑셀 데이터 가져오기
            data_excel =  pd.read_excel('F:/JusikData/API/data/'+name+'_'+edate+'.xlsx', engine='openpyxl')
            #data_excel = data_excel[data_excel['일자'] >= start]
            #data_excel = data_excel.reset_index(drop=True)
            
            
            
            ##-----------------------------------------------------------------------------------------------##
            ## 고점구하기
            # for문 전 변수 지정
            bf_max_column = []
            af_max_column = []
            sum_max_column = []
            count_bf_max = 0
            count_af_max = 0
            
            # for문 돌리기
            for i in data_excel.index:
                for j in range(i) : 
                    if i == 0:
                        break
                    
                    if data_excel.iloc[i]['고가'] <= data_excel.iloc[i-j-1]['고가']:
                        break
                    elif data_excel.iloc[i]['고가'] > data_excel.iloc[i-j-1]['고가']: # 현재 가격 이전 기준으로! 낮은 가격의 개수구하기 | 큰봉이 없었는지 열 만들기
                        count_bf_max += 1
                
                for k in range(i,len(data_excel)):
                    if i == len(data_excel)-1:
                        break
                    
                    if i == k :
                        continue
                    
                    if data_excel.iloc[i]['고가'] <= data_excel.iloc[k]['고가']:
                        break
                    elif data_excel.iloc[i]['고가'] > data_excel.iloc[k]['고가']: # 현재 가격 이후 기준으로! 낮은 가격의 개수구하기 | 큰봉이 없었는지 열 만들기
                        count_af_max += 1
                        
                bf_max_column.append(count_bf_max)
                af_max_column.append(count_af_max)
                sum_max_column.append(count_bf_max+count_af_max) # 다른 방법 : sum_max_column = [bf_max_column[i] + af_max_column[i] for i in range(len(bf_max_column))]
                count_bf_max = 0
                count_af_max = 0
            
            # 결과
            data = pd.DataFrame({'전작은값수' : bf_max_column, '후작은값수' : af_max_column, '작은값수합' : sum_max_column})
            
            # 오름차순 정렬
            data = data.sort_values('작은값수합', ascending=False)
            
            # 전작은값수나 후작은값수가 20미만 인 것들은 필터
            # 적어도 전,후 한달동안은 최고를 유지
            #data = data.loc[:, (data != 0).any(axis=0)]
            data = data[data['전작은값수'] >= 20]
            data = data[data['후작은값수'] >= 20]
            #print(data)
            
            # 필터된 데이터의 인덱스 가져오기
            result_date_arr = []
            result_index_arr = []
            result_max_arr = []
            
            for i in range(len(data)) : 
                idx = data.index[i]
                
                # 해당 인덱스의 일자 가져오기
                date = data_excel.loc[idx]['일자']
                
                # 해당 인덱스의 고가 가져오기
                max = data_excel.loc[idx]['고가']
                
                # 결과 리스트에 인덱스 넣기
                result_index_arr.append(idx)
                # 결과 리스트에 일자 넣기
                result_date_arr.append(date)
                # 결과 리스트에 고가 넣기
                result_max_arr.append(max)
            
            # 결과 데이터프레임 만들기
            data_result = pd.DataFrame({'일자' : result_date_arr, 'x값' : result_index_arr, 'y값' : result_max_arr})
            
            # 내림차순 정리
            data_result = data_result.sort_values('일자', ascending=False)
            #print(data_result)
            
            # 최신값 두개를 가져와서 직선만들기 : x는 인덱스값, y는 고가
            # 첫 번째 값의 좌표
            x1 = data_result.iloc[0]['x값']
            y1 = data_result.iloc[0]['y값']
            
            # 두 번째 값의 좌표
            x2 = data_result.iloc[1]['x값']
            y2 = data_result.iloc[1]['y값']
            
            # 세 번째 값의 좌표
            x3 = data_result.iloc[2]['x값']
            y3 = data_result.iloc[2]['y값']
            
            # 네 번째 값의 좌표
            #x4 = data_result.iloc[3]['x값']
            #y4 = data_result.iloc[3]['y값']
            
            # 기울기와 y절편 구하기
            inclination = round((y1 - y2) / (x1 - x2),0) # 기울기
            angle_incl1 = np.arctan(inclination)
            print('기울기(상) : '+str(inclination),
                  '기울기(상) 각도 : '+str(angle_incl1 * 180 / math.pi))
            
            inclination2 = round((y2 - y3) / (x2 - x3),0) # 기울기
            #inclination3 = round((y3 - y4) / (x3 - x4),0) # 기울기
            
            st_grape_arr = []
            for i in data_excel.index:
                if i >= x2 :
                    # 그래프그리기시작
                    st_y = inclination * (i-x1) + y1
                    st_grape_arr.append(st_y)
                elif i >= x3 :
                    # 그래프그리기시작
                    st_y = inclination2 * (i-x2) + y2
                    st_grape_arr.append(st_y)
                #elif i >= x4 :
                    # 그래프그리기시작
                    #st_y = inclination3 * (i-x3) + y3
                    #st_grape_arr.append(st_y)   
                else : 
                    # 그래프안그리는 곳 
                    st_grape_arr.append(y3)
            
            # 결과를 전체 데이터에 넣기
            data_excel['st_grape'] = st_grape_arr
            
            
            
            ##-----------------------------------------------------------------------------------------------##
            ## 저점구하기
            # for문 전 변수 지정
            bf_min_column = []
            af_min_column = []
            sum_min_column = []
            count_bf_min = 0
            count_af_min = 0
            
            # for문 돌리기
            for i in data_excel.index:
                for j in range(i) : 
                    if i == 0:
                        break
                    
                    if data_excel.iloc[i]['저가'] >= data_excel.iloc[i-j-1]['저가']:
                        break
                    elif data_excel.iloc[i]['저가'] < data_excel.iloc[i-j-1]['저가']: # 현재 가격 이전 기준으로! 높은 가격의 개수구하기
                        count_bf_min += 1
                
                for k in range(i,len(data_excel)):
                    if i == len(data_excel)-1:
                        break
                    
                    if i == k :
                        continue
                    
                    if data_excel.iloc[i]['저가'] >= data_excel.iloc[k]['저가']:
                        break
                    elif data_excel.iloc[i]['저가'] < data_excel.iloc[k]['저가']: # 현재 가격 이후 기준으로 ! 높은 가격의 개수구하기
                        count_af_min += 1
                        
                bf_min_column.append(count_bf_min)
                af_min_column.append(count_af_min)
                sum_min_column.append(count_bf_min+count_af_min) # 다른 방법 : sum_max_column = [bf_max_column[i] + af_max_column[i] for i in range(len(bf_max_column))]
                count_bf_min = 0
                count_af_min = 0
            
            # 결과
            data2 = pd.DataFrame({'전큰값수' : bf_min_column, '후큰값수' : af_min_column, '큰값수합' : sum_min_column})
            
            # 오름차순 정렬
            data2 = data2.sort_values('큰값수합', ascending=False)
            
            # 전작은값수나 후작은값수가 20미만 인 것들은 필터
            # 적어도 전,후 한달동안은 최고를 유지
            #data = data.loc[:, (data != 0).any(axis=0)]
            data2 = data2[data2['전큰값수'] >= 20]
            data2 = data2[data2['후큰값수'] >= 20]
            #print(data2)
            
            # 필터된 데이터의 인덱스 가져오기
            result_date2_arr = []
            result_index2_arr = []
            result_min_arr = []
            
            for i in range(len(data2)) : 
                idx2 = data2.index[i]
                
                # 해당 인덱스의 일자 가져오기
                date2 = data_excel.loc[idx2]['일자']
                
                # 해당 인덱스의 고가 가져오기
                min = data_excel.loc[idx2]['저가']
                
                # 결과 리스트에 인덱스 넣기
                result_index2_arr.append(idx2)
                # 결과 리스트에 일자 넣기
                result_date2_arr.append(date2)
                # 결과 리스트에 고가 넣기
                result_min_arr.append(min)
            
            # 결과 데이터프레임 만들기
            data_result2 = pd.DataFrame({'일자' : result_date2_arr, 'x값' : result_index2_arr, 'y값' : result_min_arr})
            
            # 내림차순 정리
            data_result2 = data_result2.sort_values('일자', ascending=False)
            #print(data_result2)
            
            # 최신값 두개를 가져와서 직선만들기 : x는 인덱스값, y는 고가
            # 첫 번째 값의 좌표
            x1 = data_result2.iloc[0]['x값']
            y1 = data_result2.iloc[0]['y값']
            
            # 두 번째 값의 좌표
            x2 = data_result2.iloc[1]['x값']
            y2 = data_result2.iloc[1]['y값']
            
            # 세 번째 값의 좌표
            x3 = data_result2.iloc[2]['x값']
            y3 = data_result2.iloc[2]['y값']
            
            # 네 번째 값의 좌표
            #x4 = data_result2.iloc[3]['x값']
            #y4 = data_result2.iloc[3]['y값']
            
            # 기울기와 y절편 구하기
            inclination = round((y1 - y2) / (x1 - x2),0) # 기울기
            angle_incl2 = np.arctan(inclination)
            print('기울기(하) : '+str(inclination),
                  '기울기(하) 각도 : '+str(angle_incl2 * 180 / math.pi))
            
            inclination2 = round((y2 - y3) / (x2 - x3),0) # 기울기
            #inclination3 = round((y3 - y4) / (x3 - x4),0) # 기울기
            
            st_grape_arr2 = []
            for i in data_excel.index:
                if i >= x2 :
                    # 그래프그리기시작
                    st_y = inclination * (i-x1) + y1
                    st_grape_arr2.append(st_y)
                elif i >= x3 :
                    # 그래프그리기시작
                    st_y = inclination2 * (i-x2) + y2
                    st_grape_arr2.append(st_y)
                #elif i >= x4 :
                    # 그래프그리기시작
                    #st_y = inclination3 * (i-x3) + y3
                    #st_grape_arr.append(st_y)   
                else : 
                    # 그래프안그리는 곳 
                    st_grape_arr2.append(y3)
            
            # 결과를 전체 데이터에 넣기
            data_excel['st_grape2'] = st_grape_arr2
            
            
            
            ##-----------------------------------------------------------------------------------------------##
            ## 매물대구하기
            # 고점 값들(매물대들) 가져오기
            # data_result = 일자, 인덱스값, 고가로 구성
            #print(data_result)
            
            # 개별 종목 데이터 가져오기
            path1 = "F:/JusikData/oneday_csv/onedaydata/"+name+'/'+name+'.csv'
            data_jusiksu = pd.read_csv(path1, encoding='cp949')
            
            arr_dd = []
            arr_jusik = []
            arr_trade = []
            arr_high = []
            arr_per = []
            arr_idx = []
            #print(data_result)
            for i in data_result.index:
                # 해당일자를 리스트에 담기
                arr_dd.append(data_result.iloc[i]['일자'])
                
                # 해당일자의 유통주식수 구하기
                jusik = data_jusiksu[data_jusiksu['일자'] == data_result.iloc[i]['일자']]['상장주식수'].values[0]
                arr_jusik.append(jusik)
            
                # 해당일자 + 전 + 후의 거래량 평균구하기
                idx_dd = data_result.iloc[i]['x값'] # 해당일자의 인덱스
                #dmo_tr = data_excel.iloc[idx_dd-1]['거래량']
                dd_tr = data_excel.iloc[idx_dd]['거래량']
                #dpo_tr = data_excel.iloc[idx_dd+1]['거래량']
                #avg_tr = round((dmo_tr + dd_tr + dpo_tr) / 3,0)
                avg_tr = dd_tr
                arr_trade.append(avg_tr)
                
                # 해당일자 + 전 + 후의 고가 평균구하기
                #dmo_hi = data_excel.iloc[idx_dd-1]['고가']
                dd_hi = data_excel.iloc[idx_dd]['고가']
                #dpo_hi = data_excel.iloc[idx_dd+1]['고가']
                #avg_hi = round((dmo_hi + dd_hi + dpo_hi) / 3,0)
                avg_hi = dd_hi
                arr_high.append(avg_hi)
                
                # 유통주식수 대비 거래량의 %
                jusik_tr = round(avg_tr / jusik * 100,0)
                arr_per.append(jusik_tr)
                
                # 인덱스 넣기
                arr_idx.append(idx_dd)
                
            # 결과 데이터프레임 만들기
            data_result3 = pd.DataFrame({'일자' : arr_dd ,'매물대' : arr_high, '비율' : arr_per, 
                                         '인덱스' : arr_idx, '거래량' : arr_trade, '유통주식수' : arr_jusik})
            
            
            
            ##-----------------------------------------------------------------------------------------------##
            # 매물대 해소 판단
            #vprint(data_result3) # 이후에 매물대 터치봉 확인하기
            
            release_arr = []
            result_num = 0
            for i in data_result3.index:
                idx_result3 = int(data_result3.iloc[i]['인덱스']) # 해당일자의 인덱스
                
                for j in range(idx_result3+1,len(data_excel)-1):
                    if data_excel.iloc[j]['고가'] >= data_result3.iloc[i]['매물대']:
                        result_num += 1
                    
                # 이후에 매물대보다 고가가 있었다면 매물대 해소로 판단하여 '1'을 넣음    
                if result_num != 0:
                    release_arr.append(result_num)
                else:
                    release_arr.append(0)
                      
                # num 초기화
                result_num = 0
                
            #print(release_arr)
            data_result3['release'] = release_arr
            
            
            
            ##-----------------------------------------------------------------------------------------------##
            # 그래프 그리기
            # 표시할 데이터 개수 정하기
            data_excel = data_excel[-240:]
            data_excel = data_excel.reset_index(drop=True)
            
            # 캔버스 설정(크기, 배경 설정 등)
            fig = plt.figure(figsize=(25,15)) ## 캔버스 생성
            fig.set_facecolor('white') ## 캔버스 색상 설정
            
            # 그림 뼈대(프레임) 생성 
            #차트1 : 지수-종목그래프 and 추세선
            ax1 = fig.add_subplot(211)
            ax1.plot(data_excel['st_grape'], color='red', label='Choo_max')
            ax1.plot(data_excel['st_grape2'], color='blue', label='Choo_min')            
            mpl_finance.candlestick2_ohlc(ax1, data_excel['시가'], data_excel['고가'], data_excel['저가'], data_excel['종가'], width=0.5, colorup='r', colordown='b')
            plt.xticks(visible=False) # 축값없애기
            #plt.legend() # 범례만들기
            
            # 차트2 : 거래량차트
            # 거래량 바 차트
            ax2 = fig.add_subplot(212)
            plt.bar(range(len(data_excel)), data_excel['거래량'])
            
            # 수평선 긋기
            for i in data_result3.index:
                
                
                if data_result3.iloc[i]['release'] >= 1:
                    color = 'black'
                    ax1.axhline(data_result3.iloc[i]['매물대'], color=color, linestyle='--') 
                    
                    print("일자 : "+str(data_result3.iloc[i]['일자']),
                          "매물대_"+str(i)+" = ",
                          "가격 : "+str(data_result3.iloc[i]['매물대'])
                          ,"유통주식수 : "+str(data_result3.iloc[i]['유통주식수'])
                          ,'거래량 : '+str(data_result3.iloc[i]['거래량'])
                          ,"색깔 : "+color
                          ,'매물대해소 : '+str(data_result3.iloc[i]['release']))
                    
                else:
                    if data_result3.iloc[i]['비율'] >= 20:
                        color = 'red'
                    elif data_result3.iloc[i]['비율'] >= 10:
                        color = 'blue'
                    elif data_result3.iloc[i]['비율'] >= 5:
                        color = 'green'
                    else:
                        color = 'yellow'
                
                    ax1.axhline(data_result3.iloc[i]['매물대'], color=color)
                    
                    print("일자 : "+str(data_result3.iloc[i]['일자']),
                          "매물대_"+str(i)+" = ",
                          "가격 : "+str(data_result3.iloc[i]['매물대'])
                          ,"유통주식수 : "+str(data_result3.iloc[i]['유통주식수'])
                          ,'거래량 : '+str(data_result3.iloc[i]['거래량'])
                          ,"색깔 : "+color
                          ,'매물대해소 : '+str(data_result3.iloc[i]['release']))
                    
            # 그래프 보기
            #plt.show()
            
            # 저장
            plt.savefig('F:/JusikData/API/analy_1/'+name+'_'+str(edate)+'.png')
            
            # 메모리 제거
            plt.close()
            
            
            
            ##-----------------------------------------------------------------------------------------------##
            # 해소 못한 매물대 이후의 수급 확인하기 위해 데이터 리턴하기
            
            
        else:
            print(name+'_'+edate+'.xlsx', ' : 자료가 없습니다.')
            
            
            
            
            
            
#conn = trendline_cls()
#conn.exe_trendline("오공", "20210101")
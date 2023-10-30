import pandas as pd
import os
import numpy as np
import csv
import datetime

class Increase_cls:
    def Make_Increase(self):
        # 경로에 있는 csv 파일명을 가져와서 배열로 저장
        csv_files_collect = []
        for path, dirs, files in os.walk("F:/JusikData/oneday_csv/onedaydata"):
            csv_files_collect.append(''.join(files))

        # 배열의 첫번째는 값이 없으므로 제거
        del csv_files_collect[0]
        
        # 확인
        #print(csv_files_collect)
        
        # .csv를 빼서 종목명만 집어넣기
        JongMok = []
        for i in csv_files_collect:
            aa = i.replace('.csv','')
            if aa == 'JYP Ent.JYP Ent':
                JongMok.append('JYP Ent')
            else :
                JongMok.append(aa)
                
        # 확인
        #print(JongMok)

        ################################################################################        
        ####  #### 
        # 기준일로부터 n일 동안 증가율이 n% 이상일때의 기간 및 값 구하기
        # 구하고 이차원 배열로 저장
        dname = []
        ddate = []
        n_day = []
        max_val_arr = []
        closing_price = []
        trading_volume = []
        move_five = []
        move_ten = []
        move_to = []
        move_so = []
        move_otz = []
        move_f_t = []
        move_t_s = []
        move_t_ot = []
        move_s_ot = []
        bar_to = []
        bar_so = []
        bar_ot = []
        trade_ago_one = []
        trade_avg_five = [] 
        trade_avg_ten = []
        trade_avg_to = []
        var_avg_five = [] 
        var_avg_ten = []
        var_avg_to = []
        max_five = [] 
        max_ten = []
        max_to = []
        min_five = [] 
        min_ten = []
        min_to = []
        group_arr = []
        
        for name in JongMok:
            # 중단 필요시
            #if name == 'AJ네트웍스':
                #break
            
            # 경로를 만들고 해당경로의 csv 파일 가져오기
            path = "F:/JusikData/oneday_csv/onedaydata/"+name+'/'+name+'.csv'
            data = pd.read_csv(path, encoding='cp949')
            
            # 인덱스 0부터 시작
            data_index = 0
            # 인덱스 마지막 번호는
            max_index = len(data)
            
            #@ 데이터 추가 @#
            # 이동평균선 위치
            data['5이평'] = data['종가'].rolling(window=5).mean()
            data['10이평'] = data['종가'].rolling(window=10).mean()
            data['20이평'] = data['종가'].rolling(window=20).mean()
            data['60이평'] = data['종가'].rolling(window=60).mean()
            data['120이평'] = data['종가'].rolling(window=120).mean()
            
            # 이동평균선 차이(거리)
            data['5일-20일'] = data['5이평'] - data['20이평']
            data['20일-60일'] = data['20이평'] - data['60이평']
            data['20일-120일'] = data['20이평'] - data['120이평']
            data['60일-120일'] = data['60이평'] - data['120이평']
            
            # 이동평균선과 주가 차이(거리)
            data['종가-20'] = data['종가'] - data['20이평']
            data['종가-60'] = data['종가'] - data['60이평']
            data['종가-120'] = data['종가'] - data['120이평']
            
            # 거래량 n일 전 평균
            trade_1ago = []
            trade_5ago = []
            trade_10ago = []
            trade_20ago = []
            for i in data.index:
                if i >=1 :
                    trade_1ago.append(data.iloc[i-1]['거래량'])
                else : 
                    trade_1ago.append('false')
                
                if i >=5 :
                    trade_5ago.append(data[i-5:i-1]['거래량'].mean())
                else : 
                    trade_5ago.append('false')
                
                if i >= 10 :
                    trade_10ago.append(data[i-10:i-1]['거래량'].mean())
                else :
                    trade_10ago.append('false')
                    
                if i >= 20 :
                    trade_20ago.append(data[i-20:i-1]['거래량'].mean())
                else :
                    trade_20ago.append('false')
            
            data['거래량_1일전'] = trade_1ago
            data['거래량_5일전평균'] = trade_5ago
            data['거래량_10일전평균'] = trade_10ago
            data['거래량_20일전평균'] = trade_20ago
            
            # 분산
            var_5ago = []
            var_10ago = []
            var_20ago = []
            for i in data.index:
                if i >=5 :
                    var_5ago.append(data[i-5:i-1]['종가'].var())
                else : 
                    var_5ago.append('false')
                
                if i >= 10 :
                    var_10ago.append(data[i-10:i-1]['종가'].var())
                else :
                    var_10ago.append('false')
                    
                if i >= 20 :
                    var_20ago.append(data[i-20:i-1]['종가'].var())
                else :
                    var_20ago.append('false')
                    
            data['분산_5일전평균'] = var_5ago
            data['분산_10일전평균'] = var_10ago
            data['분산_20일전평균'] = var_20ago
            
            # n일전 최소값, 최대값
            min_5ago = []
            min_10ago = []
            min_20ago = []
            max_5ago = []
            max_10ago = []
            max_20ago = []
            for i in data.index:
                if i >=5 :
                    min_5ago.append(data[i-5:i-1]['종가'].min())
                    max_5ago.append(data[i-5:i-1]['종가'].max())
                else : 
                    min_5ago.append('false')
                    max_5ago.append('false')
                
                if i >= 10 :
                    min_10ago.append(data[i-10:i-1]['종가'].min())
                    max_10ago.append(data[i-10:i-1]['종가'].max())
                else :
                    min_10ago.append('false')
                    max_10ago.append('false')
                    
                if i >= 20 :
                    min_20ago.append(data[i-20:i-1]['종가'].min())
                    max_20ago.append(data[i-20:i-1]['종가'].max())
                else :
                    min_20ago.append('false')
                    max_20ago.append('false')
                    
            data['최소값_5일전'] = min_5ago
            data['최소값_10일전'] = min_10ago
            data['최소값_20일전'] = min_20ago       
            data['최대값_5일전'] = max_5ago
            data['최대값_10일전'] = max_10ago
            data['최대값_20일전'] = max_20ago
            
            #print(data.columns)
            #print(data)
            
            group_num = 1
            
            ## n% 증가한 기준일 구하기 ##            
            while True:
                # 기준일로부터 n일 동안의 최고가, 최저가 구하기
                during_day = [20]
                for i in during_day:
                    data2 = data.loc[data_index:data_index+i,:]
                    max_val = data2['종가'].max()
                    now_val = data['종가'][data_index]
                    min_val = data2['종가'].min()
                    #print(max_val, now_val, min_val)
                    #print(max_val, min_val)
                
                    # 현재주가부터 최고가가 얼마나 올랐는지 확인
                    roi = round((max_val - now_val) / now_val * 100, 1)
                    #print(roi) # 최저가로부터 몇 % 올랐는지
                    
                    if roi >= 50 :
                        #print('최대값의 인덱스 : ', data2.index[data2['고가'] == max_val].tolist())
                        print(name, data['일자'][data_index])
                        dname.append(name) # 종목명
                        ddate.append(data['일자'][data_index]) # 일자
                        n_day.append(i)
                        max_val_arr.append(max_val)
                        closing_price.append(data['종가'][data_index])
                        trading_volume.append(data['거래량'][data_index])
                        move_five.append(data['5이평'][data_index])
                        move_ten.append(data['10이평'][data_index])
                        move_to.append(data['20이평'][data_index])
                        move_so.append(data['60이평'][data_index])
                        move_otz.append(data['120이평'][data_index])
                        move_f_t.append(data['5일-20일'][data_index])
                        move_t_s.append(data['20일-60일'][data_index])
                        move_t_ot.append(data['20일-120일'][data_index])
                        move_s_ot.append(data['60일-120일'][data_index])
                        bar_to.append(data['종가-20'][data_index])
                        bar_so.append(data['종가-60'][data_index])
                        bar_ot.append(data['종가-120'][data_index])
                        trade_ago_one.append(data['거래량_1일전'][data_index])
                        trade_avg_five.append(data['거래량_5일전평균'][data_index])
                        trade_avg_ten.append(data['거래량_10일전평균'][data_index])
                        trade_avg_to.append(data['거래량_20일전평균'][data_index])
                        var_avg_five.append(data['분산_5일전평균'][data_index]) 
                        var_avg_ten.append(data['분산_10일전평균'][data_index])
                        var_avg_to.append(data['분산_20일전평균'][data_index])
                        min_five.append(data['최소값_5일전'][data_index])
                        min_ten.append(data['최소값_10일전'][data_index])
                        min_to.append(data['최소값_20일전'][data_index])
                        max_five.append(data['최대값_5일전'][data_index])
                        max_ten.append(data['최대값_10일전'][data_index])
                        max_to.append(data['최대값_20일전'][data_index])
                        group_arr.append(group_num)
                
                if data_index / 20 >= 1:
                    if (data_index / 20) - int(data_index / 20) == 0:
                        group_num += 1
                            
                data_index += 1
                
                if data_index >= max_index - during_day[0] - 1:
                    break
        ##########
        
        ####  ####
        # 이차원 배열을 데이터프레임 형태로 바꾼다음 엑셀로 저장하기
        dataset = pd.DataFrame({'종목명': dname, '기준일': ddate, 'n일': n_day, '최대값': max_val_arr, '종가': closing_price, '거래량': trading_volume, '거래량_1일전':  trade_ago_one,
                                '5이평': move_five, '10이평': move_ten, '20이평': move_to, '60이평': move_so, '120이평': move_otz,
                                '5일-20일': move_f_t, '20일-60일': move_t_s, '20일-120일': move_t_ot, '60일-120일': move_s_ot, '종가-20': bar_to, '종가-60': bar_so, '종가-120': bar_ot,
                                '거래량_5일전평균': trade_avg_five, '거래량_10일전평균': trade_avg_ten, '거래량_20일전평균': trade_avg_to,
                                '분산_5일전평균': var_avg_five, '분산_10일전평균': var_avg_ten, '분산_20일전평균': var_avg_to,
                                '최소값_5일전': min_five, '최소값_10일전': min_ten, '최소값_20일전': min_to,
                                '최대값_5일전': max_five, '최대값_10일전': max_ten, '최대값_20일전': max_to, '그룹번호': group_arr })
        dataset = dataset.drop_duplicates(['종목명', '최대값'])
        dataset.to_csv('F:/JusikData/analysis_csv/increase/분석_증가데이터2.csv', encoding='cp949', index = False)
        ##########
            
# 테스트
conn = Increase_cls()
conn.Make_Increase()
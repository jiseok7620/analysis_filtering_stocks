import pandas as pd
from pandas.core.dtypes.missing import isnull


class goodone_analy_cls:
    def make_analy(self):
        data = pd.read_csv('F:/JusikData/analysis_csv/increase/조건(2).csv', encoding='cp949')

        arr_max = [] # 기준일 이후 60봉중 최고가(60봉 == 3달)
        arr_index = [] # 최고가의 위치가 몇봉째인지
        arr_20per = [] # 기준일 이후 20% 이상 오른 봉이 몇번째인지
        test = []
        test2 = []
        for i in data.index:
            # 자료가져오기
            data_ori = pd.read_csv("F:/JusikData/oneday_csv/onedaydata/"+data.iloc[i]['종목명']+'/'+data.iloc[i]['종목명']+'.csv', encoding='cp949')

            ##### ##### #####
            # 해당 기준일의 인덱스 구하기
            index_num = data_ori[data_ori['일자'] == data.iloc[i]['기준일']].index.tolist()
            # 기준일 시점 종가
            close_now = data_ori.iloc[index_num[0]]['종가']
            # 60봉 후 중 최고가
            max_after_60 = data_ori[index_num[0]+1:index_num[0]+60]['고가'].max()
            print(max_after_60)
            
            # 다음날이 없는 종목들이있음
            if not isnull(max_after_60) :
                # 60봉 후 몇% 올랐는지
                per_close_to_max = ((max_after_60 - close_now) / max_after_60)* 100
                # 배열로 저장
                arr_max.append(per_close_to_max)
                
                ##### ##### #####
                # 최고가의 인덱스구하기
                data_max = data_ori[index_num[0]+1:index_num[0]+60]
                index_num_max = data_max[data_max['고가'] == max_after_60].index.tolist()
                # 최고가의 위치(몇봉후인지) 배열로 저장
                arr_index.append(index_num_max[0] - index_num[0])
                
                ##### ##### #####
                # 20% 이상 오른 봉이 몇봉 후 인지 구하기
                index_num_20per = data_max[data_max['고가'] >= close_now * 1.2].index.tolist()
                try:
                    # 배열로 저장
                    arr_20per.append(index_num_20per[0] - index_num[0])
                except:
                    # 배열로 저장
                    arr_20per.append('없음')
                    
                ##### ##### #####
                # 테스트
                # 
                try:
                    gojong = data_ori.iloc[index_num[0]+1]['고가'] - data_ori.iloc[index_num[0]]['종가']
                    test.append(gojong)
                    gojong2 = data_ori.iloc[index_num[0]+2]['고가'] - data_ori.iloc[index_num[0]+1]['고가']
                    test2.append(gojong2)
                except:
                    test2.append('nan')
                
            else :
                # 배열로 저장
                arr_max.append('nan')
            
                # 최고가의 위치(몇봉후인지) 배열로 저장
                arr_index.append('nan')
                
                # 20%도 nan
                arr_20per.append('nan')
            
                # 테스트도 nan
                test.append('nan')
                test2.append('nan')
            
        
        data['등락률'] = arr_max
        data['몇봉째'] = arr_index
        data['20%이상'] = arr_20per
        data['고-종'] = test
        data['고-고2'] = test2
        data.to_csv('F:/JusikData/analysis_csv/analy/첫번째3.csv', encoding='cp949', index = False)
        
# 테스트
conn = goodone_analy_cls()
conn.make_analy()
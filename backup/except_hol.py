import datetime

class except_hol_cls:
    def exe_except(self, dd):
        # 휴일정보 넣기
        holli = [20160101
                ,20160208
                ,20160209
                ,20160210
                ,20160301
                ,20160413
                ,20160505
                ,20160506
                ,20160606
                ,20160815
                ,20160914
                ,20160915
                ,20160916
                ,20161003
                ,20161230
                ,20170127
                ,20170130
                ,20170301
                ,20170501
                ,20170503
                ,20170505
                ,20170509
                ,20170606
                ,20170815
                ,20171002
                ,20171003
                ,20171004
                ,20171005
                ,20171006
                ,20171009
                ,20171225
                ,20180101
                ,20180215
                ,20180216
                ,20180301
                ,20180501
                ,20180507
                ,20180522
                ,20180606
                ,20180613
                ,20180815
                ,20180924
                ,20180925
                ,20180926
                ,20181003
                ,20181009
                ,20181225
                ,20190101
                ,20190204
                ,20190205
                ,20190206
                ,20190301
                ,20190501
                ,20190506
                ,20190606
                ,20190815
                ,20190912
                ,20190913
                ,20191003
                ,20191009
                ,20191225
                ,20191231
                ,20200101
                ,20200124
                ,20200127
                ,20200415
                ,20200430
                ,20200501
                ,20200505
                ,20200817
                ,20200930
                ,20201001
                ,20201002
                ,20201009
                ,20201225
                ,20201231
                ,20210101
                ,20210211
                ,20210212
                ,20210301
                ,20210505
                ,20210519
                ,20210816
                ,20210920
                ,20210921
                ,20210922
                ,20211004
                ,20211011
                ,20211231]
        
        # 들어온 날짜데이터 정제
        dd_full = dd
        dd_y = int(str(dd_full)[0:4])
        dd_m = int(str(dd_full)[4:6])
        dd_d = int(str(dd_full)[6:8])
        dd_week = datetime.date(dd_y, dd_m, dd_d).weekday()
        
        # 요일이 토요일이나 일요일이면 이렇게 하기
        if dd_week == 5:
            if dd_d == 1:
                try: 
                    datetime.date(dd_y, dd_m - 1, 31).weekday()
                    if len(str(dd_m - 1)) == 1:
                        dd_full = str(dd_y)[0:4] + "0" + str(dd_m - 1) + str(31)                        
                    else :    
                        dd_full = str(dd_y)[0:4] + str(dd_m - 1) + str(31)
                except:
                    try:
                        datetime.date(dd_y, dd_m - 1, 30).weekday()
                        if len(str(dd_m - 1)) == 1:
                            dd_full = str(dd_y)[0:4] + "0" + str(dd_m - 1) + str(30)                        
                        else :    
                            dd_full = str(dd_y)[0:4] + str(dd_m - 1) + str(30)
                    except:
                        if len(str(dd_m - 1)) == 1:
                            dd_full = str(dd_y)[0:4] + "0" + str(dd_m - 1) + str(29)                        
                        else :    
                            dd_full = str(dd_y)[0:4] + str(dd_m - 1) + str(29)
            else :
                dd_full = str(int(dd_full) - 1)
        elif dd_week == 6:
            if dd_d == 1:
                try: 
                    if datetime.date(dd_y, dd_m - 1, 30).weekday() != 5:
                        if len(str(dd_m - 1)) == 1:
                            dd_full = str(dd_y)[0:4] + "0" + str(dd_m - 1) + str(30)                        
                        else :    
                            dd_full = str(dd_y)[0:4] + str(dd_m - 1) + str(30)
                    else :
                        if len(str(dd_m - 1)) == 1:
                            dd_full = str(dd_y)[0:4] + "0" + str(dd_m - 1) + str(29)                        
                        else :    
                            dd_full = str(dd_y)[0:4] + str(dd_m - 1) + str(29)
                except:
                    if len(str(dd_m - 1)) == 1:
                        dd_full = str(dd_y)[0:4] + "0" + str(dd_m - 1) + str(29)                        
                    else :    
                        dd_full = str(dd_y)[0:4] + str(dd_m - 1) + str(29)
            elif dd_d == 2:
                try: 
                    datetime.date(dd_y, dd_m - 1, 31).weekday()
                    if len(str(dd_m - 1)) == 1:
                        dd_full = str(dd_y)[0:4] + "0" + str(dd_m - 1) + str(31)                        
                    else :    
                        dd_full = str(dd_y)[0:4] + str(dd_m - 1) + str(31)
                except:
                    try:
                        datetime.date(dd_y, dd_m - 1, 30).weekday()
                        if len(str(dd_m - 1)) == 1:
                            dd_full = str(dd_y)[0:4] + "0" + str(dd_m - 1) + str(30)                        
                        else :    
                            dd_full = str(dd_y)[0:4] + str(dd_m - 1) + str(30)
                    except:
                        if len(str(dd_m - 1)) == 1:
                            dd_full = str(dd_y)[0:4] + "0" + str(dd_m - 1) + str(29)                        
                        else :    
                            dd_full = str(dd_y)[0:4] + str(dd_m - 1) + str(29)
            else:
                dd_full = str(int(dd_full) - 2)
                
        # 정제 후 배열에 해당 값이 있으면 또 -1해주기
        while int(dd_full) in holli :
            dd_y = int(str(dd_full)[0:4])
            dd_m = int(str(dd_full)[4:6])
            dd_d = int(str(dd_full)[6:8])
            if dd_d == 1:
                try: 
                    datetime.date(dd_y, dd_m - 1, 31).weekday()
                    if len(str(dd_m - 1)) == 1:
                        dd_full = str(dd_y)[0:4] + "0" + str(dd_m - 1) + str(31)                        
                    else :    
                        dd_full = str(dd_y)[0:4] + str(dd_m - 1) + str(31)
                except:
                    try:
                        datetime.date(dd_y, dd_m - 1, 30).weekday()
                        if len(str(dd_m - 1)) == 1:
                            dd_full = str(dd_y)[0:4] + "0" + str(dd_m - 1) + str(30)                        
                        else :    
                            dd_full = str(dd_y)[0:4] + str(dd_m - 1) + str(30)
                    except:
                        if len(str(dd_m - 1)) == 1:
                            dd_full = str(dd_y)[0:4] + "0" + str(dd_m - 1) + str(29)                        
                        else :    
                            dd_full = str(dd_y)[0:4] + str(dd_m - 1) + str(29)
            else :
                dd_full = str(int(dd_full) - 1)
            
        print(dd_full)
        return dd_full
    
    
#conn = except_hol_cls()
#conn.exe_except('20171001')

            
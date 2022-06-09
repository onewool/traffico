from pandas import DataFrame, read_csv, concat
import pandas as pd

df=read_csv('data/AcDay/Ac_Day_20210103.csv', encoding='euc-kr', keep_default_na=False, names=['Date','accID','startDate','endDate','type','eventType','message','coordX', 'coordY',1,2,3,4,5], header=None)
df1=read_csv('data/AcDay/Ac_Day_20210102.csv', encoding='euc-kr', keep_default_na=False, names=['Date','accID','startDate','endDate','type','eventType','message','coordX', 'coordY',1,2,3,4,5], header=None)
df2=read_csv('data/AcDay/Ac_Day_20210102.csv', encoding='euc-kr', keep_default_na=False, names=['Date','accID','startDate','endDate','type','eventType','message','coordX', 'coordY',1,2,3,4,5], header=None)
df= concat([df,df1,df2]) 
for i in range(0,len(df.index)):   
    if df.iloc[i,-1] != '':
        df.iloc[i,7] = df.iloc[i,-2]
        df.iloc[i,8] = df.iloc[i,-1]
    elif df.iloc[i,-2] != '':
        df.iloc[i,7] = df.iloc[i,-3]
        df.iloc[i,8] = df.iloc[i,-2]
    elif df.iloc[i,-3] != '':
        df.iloc[i,7] = df.iloc[i,-4]
        df.iloc[i,8] = df.iloc[i,-3]
    elif df.iloc[i,-4] != '':
        df.iloc[i,7] = df.iloc[i,-5]
        df.iloc[i,8] = df.iloc[i,-4]
    elif df.iloc[i,-5] != '':
        df.iloc[i,7] = df.iloc[i,-6]
        df.iloc[i,8] = df.iloc[i,-5]

######## 쓸모없는 열 제거 #########
df = df.drop(df.columns[1:5], axis=1).drop(df.columns[6], axis=1).drop(df.columns[9:], axis=1)
#print(df)

######### 위도 경도 소숫점 2 자리수까지 반올림 #########
print(df['coordX'].dtype)
print(df['coordY'].dtype)
df['coordX'] = df['coordX'].astype(float, errors = 'raise')
df['coordY'] = df['coordY'].astype(float, errors = 'raise')
print(df['coordX'].dtype)
print(df['coordY'].dtype)
df['coordX'] = df['coordX'].round(2)
df['coordY'] = df['coordY'].round(2)
print(df)
df.to_csv('./2101_test.csv', encoding='euc-kr', header=False, index=False)
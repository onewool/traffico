from pandas import DataFrame, read_excel
import pandas as pd

######### 콘솔창에 행열 많이 보이게 #########
pd.set_option('display.max_row', 500)
pd.set_option('display.max_columns', 100)

######### 데이터 불러오기 #########

df = read_excel('data/행정안전부_상습 결빙구간_20200921.xlsx', sheet_name=0)

df = df.rename(index=df['구간명']).drop('구간명', axis=1).filter(['구간길이','센터X좌표','센터Y좌표'])

print(df)
df.to_csv('./frost.csv', encoding='euc-kr', header=False, index=True)
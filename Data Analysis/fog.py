from pandas import DataFrame, read_excel
import pandas as pd
import matplotlib.pyplot as plt
import folium

######### 데이터 불러오기 #########
df1 = read_excel('data/fog.xlsx', keep_default_na=False)
#print(df1)

######### 폰트 및 그래프 사이즈 설정 #########
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['font.size'] =12
plt.rcParams['figure.figsize']= (6,4)

######### 필요한 열만 추출 #########
df1 = df1.filter(['구간명','구간길이','센터X좌표','센터Y좌표'])
#print(df1)

######### 열 이름 변경 #########
df1 = df1.rename(columns={'센터X좌표':'latitude','센터Y좌표':'longitude','구간길이':'properLength'})
#print(df1)

df1 = df1.drop(df1.index[0])
#print(df1)
df1['properLength'] = df1['properLength'].astype(float)

m = folium.Map(location=[36.423463, 127.938300], zoom_start=8)

for i in df1.index :
    marker = folium.CircleMarker([df1.loc[i,'latitude'],df1.loc[i,'longitude']], radius=df1['properLength'][i]*1.5, popup=df1['구간명'][i], icon = folium.Icon(color = 'blue', icon = 'info-sign'))
    marker.add_to(m)
m.save('Korea_fog.html')

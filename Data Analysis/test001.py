

#================================================================================
#=================================구역나누는 코드=================================
#================================================================================

import requests
import json
from pandas import read_csv

df = read_csv('frost.csv', keep_default_na=False, encoding ='cp949')
#서울지역 json 파일
kr_distinct_geojson = 'https://raw.githubusercontent.com/onewool/traffico/main/Data%20Analysis/data/geojson/hangjeongdong_%EA%B0%95%EC%9B%90%EB%8F%84.geojson'

response = requests.get(kr_distinct_geojson)
dictres = response.json()
c = response.content
jsonData = json.loads(c)

#json파일 dictionary로 바꿈
geo_dict = {}
for dict_row in dictres['features'] :
    geo_name = dict_row['properties']['sggnm'];
    geo_value = dict_row['geometry']['coordinates'][0][0];
    geo_dict[geo_name] = geo_value
print(geo_dict)

#
from shapely.geometry import Point, Polygon
def get_GeoName(longi,lati):
    for geo_name, geo_poly in geo_dict.items():
        poly_obj = Polygon(geo_poly)
        point_obj = Point(longi,lati)
        if point_obj.within(poly_obj):
            return geo_name
    return None

#구역 이름 새로운 column으로 붙이기
df['geo_name'] = df.apply(lambda x : get_GeoName(x['CENTER_MAP_X_CRDNT'], x['CENTER_MAP_Y_CRDNT']), axis=1)

print(df['geo_name'])

#df['geo_name']이 null값인, 서울지역이 아닌 갯수 세기
print(df.isnull().sum())
#df['geo_name']이 null값인 행 날리기
df = df.dropna(axis=0)
#출력
print(df)

import folium
#시도 center정하기
center = [37.33961877777525,128.84582136150203]
m = folium.Map(location = center,zoom_start = 8)
folium.GeoJson(kr_distinct_geojson).add_to(m)
folium.Choropleth(geo_data=jsonData,
                  data=df,
                  columns=['geo_name','SCTN_LT'],
                  key_on='feature.properties.sggnm',
                  fill_color="BuPu",
                  fill_opacity=0.6,
                  line_opacity=0.2,
                  legend_name="Seoul"
                  ).add_to(m)
m.save('./2019 강원도 결빙_heatmap.html')
print('html 저장완료')
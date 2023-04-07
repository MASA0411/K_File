import pandas as pd
import streamlit as st
import pydeck as pdk
import plotly.express as px
from itertools import product

import warnings
warnings.simplefilter('ignore')

################################################################################
# 開店のヒートマップ
################################################################################
st.title('東京23区の開店閉店状況')

df_23ku_lat_lon = pd.read_csv('23ku_lat_lon.csv')
df_23ku_lat_lon.drop('NO', axis=1, inplace=True)
df_open_ku_map = pd.read_csv('df_open_ku_map.csv')
df_close_ku_map = pd.read_csv('df_close_ku_map.csv')

################################################################################
# 開店のヒートマップ
################################################################################

st.header('開店のヒートマップ')
view = pdk.ViewState(
    longitude=139.691648,
    latitude=35.689185,
    zoom=10,
    pitch=40.5,
)

layer_open = pdk.Layer(
    "HeatmapLayer",
    data=df_open_ku_map,
    opacity=0.4,
    get_position=["lon", "lat"],
    threshold=0.3,
    get_weight = '件数（相対値）'
)
layer_open_map = pdk.Deck(
    layers=layer_open,
    initial_view_state=view,
)

st.pydeck_chart(layer_open_map)

show_df = st.checkbox('Show DataFrame')
if show_df == True:
    st.write(df_open_ku_map)

################################################################################
# 閉店のヒートマップ
################################################################################
st.header('閉店のヒートマップ')
view = pdk.ViewState(
    longitude=139.691648,
    latitude=35.689185,
    zoom=10,
    pitch=40.5,
)

layer_close = pdk.Layer(
    "HeatmapLayer",
    data=df_close_ku_map,
    opacity=0.4,
    get_position=["lon", "lat"],
    threshold=0.3,
    get_weight = '件数（相対値）'
)
layer_close_map = pdk.Deck(
    layers=layer_close,
    initial_view_state=view,
)

st.pydeck_chart(layer_close_map)


show_close_df = st.checkbox('Show DataFrame2')
if show_close_df == True:
    st.write(df_close_ku_map)

################################################################################
#23区の開店閉店状況の折れ線グラフ
################################################################################

st.header('23区の開店閉店状況の推移')



# df_tokyo = pd.read_csv('df_tokyo_new2.csv')

# lst_ku = df_tokyo['address_ku'].unique()
# lst_year = range(df_tokyo['year'].min(), df_tokyo['year'].max())

# # もしdf_tokyo['status'] に '休業'があれば、'閉店'に変換する
# df_tokyo['status'] = df_tokyo['status'].replace('休業', '閉店')
# lst_status = df_tokyo['status'].unique()

# # 年毎、区ごとに開店閉店の推移を集計する
# df_template = pd.DataFrame(list(product(lst_year, lst_ku, lst_status)), columns=['year', 'address_ku', 'status'])

# # テンプレートとマージ
# df_template = df_template.merge(df_tokyo.groupby([df_tokyo['year'], 'address_ku', 'status']).size().reset_index(name='count'),
#                            on=['year', 'address_ku', 'status'], how='left').fillna(0)

# df_open_trend = df_template.loc[df_template['status'] == '開店']
# df_close_trend = df_template.loc[df_template['status'] == '閉店']

# df_open_trend = df_open_trend.rename(columns = {'count':'open_count'})
# df_close_trend = df_close_trend.rename(columns = {'count':'close_count'})

# df_open_trend = df_open_trend.set_index('year')
# df_close_trend = df_close_trend.set_index('year')

# df_open_close_trend = df_open_trend.copy()
# df_open_close_trend = df_open_close_trend.drop(['status'], axis=1)

# df_open_close_trend['close_count'] = df_close_trend['close_count']
# df_option = df_open_close_trend.copy()
# df_option = df_option.reset_index()

# print('df_option')
# print(df_option)
# option_ku = st.selectbox(
#     '区名',
#     (lst_ku))
# df_option = df_option[df_option['address_ku'] == option_ku]
# # print("df_option")
# # print(df_option)

# # df_open_close_trend = df_open_close_trend.drop(['address_ku'], axis=1)
# df_open_close_trend = df_open_close_trend.rename(columns = {'open_count':'開店の推移'})
# df_open_close_trend = df_open_close_trend.rename(columns = {'close_count':'閉店の推移'})

# # df_open_close_trend.drop(['address_ku'], inplace=True)
# # df_mean_line = df_mean_line[['year', 'status', 'count']]
# df_open_close_trend = df_option.set_index('year')
# df_open_close_trend = df_open_close_trend.drop(['address_ku'], axis=1)
# st.line_chart(df_open_close_trend)
# # print("df_open_close_trend")
# # print(df_open_close_trend)





df_tokyo = pd.read_csv('df_tokyo_new2.csv')

lst_ku = df_tokyo['address_ku'].unique()
lst_year = range(df_tokyo['year'].min(), df_tokyo['year'].max())

# もしdf_tokyo['status'] に '休業'があれば、'閉店'に変換する
df_tokyo['status'] = df_tokyo['status'].replace('休業', '閉店')
lst_status = df_tokyo['status'].unique()

# 年毎、区ごとに開店閉店の推移を集計する
df_template = pd.DataFrame(list(product(lst_year, lst_ku, lst_status)), columns=['year', 'address_ku', 'status'])

# テンプレートとマージ
df_template = df_template.merge(df_tokyo.groupby([df_tokyo['year'], 'address_ku', 'status']).size().reset_index(name='count'),
                           on=['year', 'address_ku', 'status'], how='left').fillna(0)

df_open_trend = df_template.loc[df_template['status'] == '開店']
df_close_trend = df_template.loc[df_template['status'] == '閉店']

df_open_trend = df_open_trend.rename(columns = {'count':'open_count'})
df_close_trend = df_close_trend.rename(columns = {'count':'close_count'})

df = pd.DataFrame()
df["open_mean"] = df_open_trend.groupby(["year"])["open_count"].mean()
df["close_mean"] = df_close_trend.groupby(["year"])["close_count"].mean()
# print("df")
# print(df)

df_open_trend = df_open_trend.set_index('year')
df_close_trend = df_close_trend.set_index('year')

df_open_close_trend = df_open_trend.copy()
df_open_close_trend = df_open_close_trend.drop(['status'], axis=1)

df_open_close_trend['close_count'] = df_close_trend['close_count']
df_option = df_open_close_trend.copy()
df_option = df_option.reset_index()
# print("df_option")
# print(df_option)

option_ku = st.selectbox(
    '区名',
    (lst_ku))
df_option = df_option[df_option['address_ku'] == option_ku]
# print("df_option")
# print(df_option)

# df_open_close_trend = df_open_close_trend.drop(['address_ku'], axis=1)
df_open_close_trend = df_open_close_trend.rename(columns = {'open_count':'開店の推移'})
df_open_close_trend = df_open_close_trend.rename(columns = {'close_count':'閉店の推移'})

# df_open_close_trend.drop(['address_ku'], inplace=True)
# df_mean_line = df_mean_line[['year', 'status', 'count']]
df_open_close_trend = df_option.set_index('year')
df_open_close_trend = df_open_close_trend.drop(['address_ku'], axis=1)
df_open_close_trend = pd.merge(df, df_open_close_trend, left_index=True, right_index=True)
# st.line_chart(df_open_close_trend)
st.line_chart(df_open_close_trend)
# print("df_open_close_trend")
# print(df_open_close_trend)
# df_open_close_trend.to_csv('df_open_close_trend.csv')
# print("df_open_close_trend")
# print(df_open_close_trend)
################################################################################


###############################################################################




# st.header('■年齢階級別の全国一人あたり平均賃金（万円）')

# df_mean_bubble = df_jp_ind[df_jp_ind['年齢'] != '年齢計']

# fig = px.scatter(df_mean_bubble,
#                 x="一人当たり賃金（万円）",
#                 y="年間賞与その他特別給与額（万円）",
#                 range_x=[150,700],
#                 range_y=[0,150],
#                 size="所定内給与額（万円）",
# 	            size_max = 38,
#                 color="年齢",
#                 animation_frame="集計年",
#                 animation_group="年齢")

# st.plotly_chart(fig)



# st.header('■産業別の賃金推移')

# year_list = df_jp_category["集計年"].unique()
# option_year = st.selectbox(
#     '集計年',
#     (year_list))

# wage_list = ['一人当たり賃金（万円）', '所定内給与額（万円）', '年間賞与その他特別給与額（万円）']
# option_wage = st.selectbox(
#     '賃金の種類',
#     (wage_list))

# df_mean_categ = df_jp_category[(df_jp_category["集計年"] == option_year)]

# max_x = df_mean_categ[option_wage].max() + 50

# fig = px.bar(df_mean_categ,
#             x=option_wage,
#             y="産業大分類名",
#             color="産業大分類名",
#             animation_frame="年齢",
#             range_x=[0,max_x],
#             orientation='h',
#             width=800,
#             height=500)
# st.plotly_chart(fig)


# st.text('出典：RESAS（地域経済分析システム）')
# st.text('本結果はRESAS（地域経済分析システム）を加工して作成')

import streamlit as st
from typing import List
import matplotlib.pyplot as plt
from dataclasses import dataclass
from itertools import product
import json;
from PIL import Image
import requests
import pandas as pd
import numpy as np
import csv


url = "https://api-mainnet.magiceden.dev/v2/ord/btc/stat?collectionSymbol=bitcoin-frogs"
bearer_token = '35d17fa0-06be-434f-8357-9d17dd537d13'
headers = {'Authorization': 'Bearer ' + bearer_token}
response = requests.get(url, headers=headers)
json_data = json.loads(response.text)
floor_price = float(json_data['floorPrice'])*0.00000001
rounded_floor_price = round(floor_price, 4)
owners = int(json_data["owners"])
totalListed =int(json_data["totalListed"])
totalVolume = float(json_data['totalVolume'])*0.00000001
rounded_totalVolume = round(totalVolume, 4)
pending = int(json_data["pendingTransactions"])

with open('bitcoin_frogs_items.json') as f:
    data = json.load(f)

filtered_frogs = []

# 设置页面的宽度
st.set_page_config(layout="wide")




def main():
    
    #st.markdown("<hr/>", unsafe_allow_html = True)
    #st.write("Floor Price : ",rounded_floor_price," Owners : ",owners," Total Listed : ",totalListed," Total Volume : ",rounded_totalVolume)
    col1, col2, col3 ,col4 ,col5 = st.columns(5)

    col1.metric("Floor Price", rounded_floor_price,"N/A") 
    col2.metric("Owners", owners,"N/A") 
    col3.metric("Total Listed", totalListed,"N/A") 
    col4.metric("Pending Transactions", pending,"N/A") 
    col5.metric("Total Volume", rounded_totalVolume,"N/A") 
    
    st.markdown("<hr/>", unsafe_allow_html = True)

    
    fpcsv = pd.read_csv("https://raw.githubusercontent.com/raymondwang0225/BitcoinFrogsData/main/data.csv", parse_dates=['timestamp'])
    # 定义 CSV 文件列表
    csv_files = [
        'https://raw.githubusercontent.com/raymondwang0225/BitcoinFrogsData/main/level_01.csv',
        'https://raw.githubusercontent.com/raymondwang0225/BitcoinFrogsData/main/level_02.csv',
        'https://raw.githubusercontent.com/raymondwang0225/BitcoinFrogsData/main/level_03.csv',
        'https://raw.githubusercontent.com/raymondwang0225/BitcoinFrogsData/main/level_04.csv',
        'https://raw.githubusercontent.com/raymondwang0225/BitcoinFrogsData/main/level_05.csv',
    ]

    # 定义价格区间
    price_ranges = ['0.05 and below', '0.05 to 0.1', '0.1 to 0.15', '0.15 to 0.2', '0.2 and above']

    # 创建一个空的字典来存储数据透视表结果
    pivot_tables = {}

    # 计算每个 CSV 文件的总量
    for file in csv_files:
        df = pd.read_csv(file)
        pivot_table = pd.pivot_table(df, values='Total', index='Price Range', aggfunc='sum')
        pivot_table = pivot_table.reindex(price_ranges)  # 重新索引以匹配价格区间
        pivot_tables[file] = pivot_table

    # 创建一个图形对象
    fig, ax = plt.subplots()

    # 绘制每个 CSV 文件的条形图
    for file, pivot_table in pivot_tables.items():
        ax.bar(pivot_table.index, pivot_table['Total'], label=file)

    # 设置图形标题和轴标签
    ax.set_title('Total Quantity by Price Range')
    ax.set_xlabel('Price Range')
    ax.set_ylabel('Total Quantity')

    # 添加图例
    ax.legend()

    

    
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Floor Price", "Owners","Total Listed","Total Volume","List Price Level"])
    with tab1:
        st.line_chart(fpcsv[["timestamp", "floor_price"]], x = 'timestamp')
    with tab2:
        st.line_chart(fpcsv[["timestamp", "owners"]], x = 'timestamp')
    with tab3:
        st.line_chart(fpcsv[["timestamp", "total_listed"]], x = 'timestamp')
    with tab4:
        st.line_chart(fpcsv[["timestamp", "total_volume"]], x = 'timestamp')
    with tab5:
        # 显示图形
        st.pyplot(fig)
    
    
    st.sidebar.image("https://cdn.discordapp.com/attachments/1117712065293987840/1124212987243278356/rpbp.png", use_column_width=True)
    #st.sidebar.title("Bitcoin Frogs")
    st.sidebar.title("Bitcoin Frogs Filters")
    
    # 属性选项
    backgrounds = ["Brown", "Red", "Olive", "Grey", "Pink", "Dark Blue", "Orange", "Blue", "Green", "Light Blue", "Bitcoin Orange", "Black", "Yellow"]
    clothing = ["Prison Jumpsuit", "Green Hoodie", "Businessman", "Bling", "Wizard Robe", "None", "Leather Jacket", "Leather Dust Coat", "Red Hoodie", "Elvis", "Jersey", "Orange Checkered", "Blue Jacket", "Fur Coat", "23 TShirt", "Black Vest", "Karate Outfit", "Black Hoodie", "Purple Checkered", "Kings Robes", "Vest and Shirt", "Ninja", "Clown", "Priest", "Red Overalls", "Grey Suit", "Blue Hoodie", "Hawaiian", "Hitman", "Yellow Hoodie", "Bowtie", "Bitcoin Shirt", "Gentlemans Suit", "Spartan"]
    bodies = ["Spotted", "Electro", "Dark Red", "Green", "Tron"]
    mouths = ["Bitcoin Pizza", "None", "Magicians Moustache", "Bubblegum", "Dictators Moustache", "Cigar", "Tongue Out", "Clown Nose", "Big Moustache", "Pipe"]
    eyes = ["Dank Shades", "Happy", "Visor", "Monocle", "none", "Frown", "Powerful", "Golden Sunglasses", "Nakamoto Glasses", "Angry", "3D Glasses", "Purple Cosmic Eyes"]

    # 用户选择过滤条件
    desired_backgrounds = st.sidebar.multiselect("Background", backgrounds)
    desired_clothing = st.sidebar.multiselect("Clothing", clothing)
    desired_bodies = st.sidebar.multiselect("Body", bodies)
    desired_mouths = st.sidebar.multiselect("Mouth", mouths)
    desired_eyes = st.sidebar.multiselect("Eyes", eyes)
    #desired_backgrounds = st.sidebar.multiselect("Select desired backgrounds", backgrounds)
    #desired_clothing = st.sidebar.multiselect("Select desired clothing", clothing)
    #desired_bodies = st.sidebar.multiselect("Select desired bodies", bodies)
    #desired_mouths = st.sidebar.multiselect("Select desired mouths", mouths)
    #desired_eyes = st.sidebar.multiselect("Select desired eyes", eyes)

    # 创建一个滑动条
    column_value = st.sidebar.slider("Column display quantity", min_value=1, max_value=11, value=10, step=1)
    
    # "Apply Filter" 按钮
    apply_filter = st.sidebar.button("Apply Filter")

    #sidebar_empty = st.sidebar.empty()
    #sidebar_empty.markdown("Powered by Ribbit Plus")
    
    
    # 应用过滤器并获取最终结果
    if apply_filter:
        
        # 根据条件过滤人物
        filtered_frogs = [frog for frog in data if
                           (not desired_backgrounds or frog["background"]  in desired_backgrounds) and
                           (not desired_bodies or frog["body"] in desired_bodies) and
                           (not desired_clothing or frog["clothing"] in desired_clothing) and  
                           (not desired_mouths or frog["mouth"] in desired_mouths) and
                           (not desired_eyes or frog["eyes"] in desired_eyes)]

        # 显示符合条件的人物
        #st.write("Filtered Bitcoin Frogs  :   [ " + str(len(filtered_frogs)) + " ] Frogs")
        st.write("Result  :   [ " + str(len(filtered_frogs)) + " ] Frogs")
        for frog in filtered_frogs:
            frog["image_url"] = 'https://ordiscan.com/content/'+str(frog["inscription_id"])
            frog["me_link"] = "https://magiceden.io/ordinals/item-details/" + str(frog["inscription_id"])
            #st.write(frog)
            #st.image('https://ordiscan.com/content/'+str(frog["inscription_id"]), caption=frog["item_name"],width=576/2)

       
        
        # 定义每列的宽度
        col_width = column_value
        
        # 间距的像素值
        #spacing = 200  

        # 创建网格布局
        cols = st.columns(col_width)
        # 显示图片
        for i, frog in enumerate(filtered_frogs):
            with cols[i % col_width]:
                link_url = frog["me_link"]
                link_name = frog["item_name"] 
                caption = f"[{link_name}]({link_url})"
                
                #st.image(frog["image_url"],width=576/4)
                image = st.image(frog["image_url"],use_column_width = True)
                st.markdown(caption, unsafe_allow_html=True)
                
                
            #st.write("&nbsp;" * spacing, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

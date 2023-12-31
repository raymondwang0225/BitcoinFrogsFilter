import streamlit as st
from typing import List
from dataclasses import dataclass
from itertools import product
import json;
from PIL import Image
import requests
import pandas as pd
import numpy as np
import csv
import plost
import matplotlib.pyplot as plt
import altair as alt



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
    frog_data = json.load(f)

filtered_frogs = []

# 设置页面的宽度
st.set_page_config(layout="wide")


@st.cache
def load_level_data(nrows):
    data = pd.read_csv('level_data.csv',nrows=nrows)
    return data

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
    #level_data = load_level_data(10)
    level_data=pd.read_csv('level_data.csv')
    whale_data=pd.read_csv('whale.csv')
    wallet_all_data =pd.read_csv('https://raw.githubusercontent.com/raymondwang0225/CheckFrogWallet/main/wallet_all.csv')
    
    total_len =[]
    
    # 遍歷每個 CSV 文件
    for i in range(1, 6):
        csv_file_name = f"https://raw.githubusercontent.com/raymondwang0225/BitcoinFrogsData/main/level_{i:02d}.csv"
    
        # 讀取 CSV 文件
        df = pd.read_csv(csv_file_name)
    
        # 計算總量並存儲到 data 字典中
        total = len(df)
        total_len.append(total)
   
    # 存儲每個 CSV 文件的總量和價格區間
    data = {
        'Price Range': ['0.05 and below', '0.05 to 0.1', '0.1 to 0.15', '0.15 to 0.2', '0.2 and above'],
        'Total': [total_len[0], total_len[1], total_len[2], total_len[3], total_len[4]]
    }

    
    # 創建資料框
    chart_data = pd.DataFrame(data)
    
    # 將 'Price Range' 設定為索引欄位
    chart_data.set_index('Price Range', inplace=True)
    
    

    tab0,tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Top15 Whales","Floor Price", "Owners","Total Listed","Total Volume","Listed Price Composition","Links Overview","Useful Links"])
    with tab0:
        st.markdown('### Top15 Whales')
        plost.donut_chart(
            data= whale_data,
            theta='amount',
            color='abridge',
            legend='bottom')
        st.markdown('### All Holders')
        st.table(wallet_all_data)
    with tab1:
        st.markdown('### Floor Price')
        st.line_chart(fpcsv[["timestamp", "floor_price"]],x='timestamp')
    with tab2:
        st.markdown('### Owners')
        st.line_chart(fpcsv[["timestamp", "owners"]],x='timestamp')
    with tab3:
        st.markdown('### Total Listed')
        st.line_chart(fpcsv[["timestamp", "total_listed"]],x='timestamp')
    with tab4:
        st.markdown('### Total Volume')
        st.line_chart(fpcsv[["timestamp", "total_volume"]],x='timestamp')
    with tab5:
        st.markdown('### Listed Price Composition')
        plost.donut_chart(
            data=level_data,
            theta='amount',
            color='range',
            legend='bottom', 
            use_container_width=True)
        st.table(level_data)

    # 读取数据
        url = 'https://raw.githubusercontent.com/raymondwang0225/CheckFrogWallet/main/wallet_distribution.csv'
        ddf = pd.read_csv(url)

        # 绘制条形图
        chart = alt.Chart(ddf).mark_bar(color='#4BAAFF').encode(
            x='WALLETS',
            y='OWNED'
        ).properties(
            width=500,
            height=400
        )
        
        # 显示图表
        st.altair_chart(chart, use_container_width=True)

    
    with tab6:
        st.markdown('### Links Overview')
        st.write("Website  [https://bitcoinfrogs.com/](https://bitcoinfrogs.com/) ")
        st.write("Follow our Twitter  [https://twitter.com/BitcoinFrogs](https://twitter.com/BitcoinFrogs) ")
        st.write("Join our Discord  [https://discord.gg/bitcoinfrogs](https://discord.gg/bitcoinfrogs) ")
        st.write("Buy and Sell at Magic Eden  [https://magiceden.io/ordinals/marketplace/bitcoin-frogs](https://magiceden.io/ordinals/marketplace/bitcoin-frogs) ")
        st.write("Buy and Sell at Ordinals Wallet  [https://ordinalswallet.com/collection/bitcoin-frogs](https://ordinalswallet.com/collection/bitcoin-frogs) ")
        st.write("Buy and Sell at Gamma Marketplace  [https://gamma.io/ordinals/collections/bitcoin-frogs](https://gamma.io/ordinals/collections/bitcoin-frogs) ")
        st.write("Buy and Sell at Binance  [https://www.binance.com/en/nft/collection/bitcoin-frogs-715939293550313472?ref=NFTTW](https://www.binance.com/en/nft/collection/bitcoin-frogs-715939293550313472?ref=NFTTW) ")
        st.write("Buy and Sell at OrdSwap  [https://ordswap.io/collections/bitcoin-frogs](https://ordswap.io/collections/bitcoin-frogs) ")
        st.write("Buy and Sell at Ordynals  [https://gamma.io/ordinals/collections/bitcoin-frogs](https://gamma.io/ordinals/collections/bitcoin-frogs) ")
        st.write("Buy and Sell at Gamma Marketplace  [https://ordynals.com/collection/bitcoin-frogs](https://ordynals.com/collection/bitcoin-frogs) ")
    with tab7:
        st.markdown('### Useful Links')
        st.write("BRC-20 Marketplace  [https://unisat.io/market](https://unisat.io/market) ")
        st.write("Track Sat Rarities  [https://www.ord.io/]( https://www.ord.io/) ")
        st.write("Track your transaction  [https://mempool.space/]( https://mempool.space/) ")
        st.write("Track the floor from all markets  [https://bestinslot.xyz/ordinals/collection/bitcoin-frogs](https://bestinslot.xyz/ordinals/collection/bitcoin-frogs) ")
        st.write("Track the number of holders  [https://ordinalswallet.com/collection/bitcoin-frogs](https://ordinalswallet.com/collection/bitcoin-frogs) ")
        st.write("Get a Wallet to store your Ordinals  [https://twitter.com/xverseApp](https://twitter.com/xverseApp) ")
    
    
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
        filtered_frogs = [frog for frog in frog_data if
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

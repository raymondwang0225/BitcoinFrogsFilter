
import streamlit as st
import time
from typing import List
from dataclasses import dataclass
from itertools import product
import json;
from PIL import Image
import requests
import random
import pandas as pd



url = "https://api-mainnet.magiceden.dev/v2/ord/btc/stat?collectionSymbol=bitcoin-frogs"
bearer_token = '35d17fa0-06be-434f-8357-9d17dd537d13'
headers = {'Authorization': 'Bearer ' + bearer_token}
response = requests.get(url, headers=headers)
json_data = json.loads(response.text)
_floor_price = float(json_data['floorPrice'])*0.00000001
_rounded_floor_price = round(_floor_price, 4)
_owners = int(json_data["owners"])
_totalListed =int(json_data["totalListed"])
_totalVolume = float(json_data['totalVolume'])*0.00000001
_rounded_totalVolume = round(_totalVolume, 4)
_pending = int(json_data["pendingTransactions"])

with open('bitcoin_frogs_items.json') as f:
    data = json.load(f)

filtered_frogs = []

# 设置页面的宽度
st.set_page_config(layout="wide")




@st.cache(allow_output_mutation=True)
def load_data(json_file):
    # 读取 JSON 数据
    with open(json_file, 'r') as file:
        data = json.load(file)

    # 转换为 Pandas DataFrame
    df = pd.DataFrame(data)

    # 将 timestamp 列转换为日期时间类型，并设置为索引
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    return df

def create_historical_chart(json_file):
    df = load_data(json_file)

    # 提取数据
    timestamps = []
    floor_prices = []
    owners = []
    total_listed = []
    total_volumes = []

    for entry in data:
        timestamp = pd.to_datetime(entry['timestamp'])
        floor_price = entry['floor_price']
        owner = entry['owners']
        total_listed = entry['total_listed']
        total_volume = entry['total_volume']

        timestamps.append(timestamp)
        floor_prices.append(floor_price)
        owners.append(owner)
        total_listed.append(total_listed)
        total_volumes.append(total_volume)

    # 创建DataFrame
    df = pd.DataFrame({
        'Timestamp': timestamps,
        'Floor Price': floor_prices,
        'Owners': owners,
        'Total Listed': total_listed,
        'Total Volume': total_volumes
    })

    # 设置Timestamp列为索引，并按小时重采样
    df.set_index('Timestamp', inplace=True)
    df_hourly = df.resample('H').last().ffill()

    # 计算每小时成交量差异
    df_hourly['Hourly Volume Diff'] = df_hourly['Total Volume'].diff()

    

    tab1, tab2, tab3, tab4 ,tab5 = st.tabs(['Floor Price', 'Owners', 'Total Listed', 'Total Volume', 'Hourly Volume Diff'])
    with tab1:
        st.line_chart(df['Floor Price'])
    with tab2:
        st.line_chart(df['Floor Price'])
    with tab3:
        st.line_chart(df['Floor Price'])
    with tab4:
        st.line_chart(df_hourly['Total Volume'])
    with tab5:
        st.line_chart(df_hourly['Hourly Volume Diff'])
   



# 定义爬虫函数
def crawl_floor_price():
    # 在这里编写你的爬虫逻辑，从网站获取 floor price 数据
    _response = requests.get(url, headers=headers)
    print(_response.text)
    json_data = json.loads(response.text)
    fp = float(json_data['floorPrice'])*0.00000001
    rounded_fp = round(fp, 4)
    floor_price = rounded_fp
    owners=int(json_data['owners'])
    total_listed=int(json_data['totalListed'])
    tv= float(json_data['totalVolume'])*0.00000001
    total_volume = round(tv, 4)
     
    # 将获取的数据保存到 JSON 文件中
    
  # 执行爬虫获取 floor price 数据
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {"timestamp": timestamp, "floor_price": floor_price, "owners": owners ,"total_listed": total_listed,"total_volume": total_volume}
    
    if not os.path.exists("History_data.json"):
        with open("History_data.json", "w") as f:
            json.dump([], f)
    
    # 读取之前的历史数据
    with open("History_data.json", "r") as f:
        history_data = json.load(f)
    
    # 将当前数据追加到历史数据列表中
    history_data.append(data)
    
    # 写入更新后的历史数据
    with open("History_data.json", "w") as f:
        json.dump(history_data, f)



    
        
    #st.markdown("<hr/>", unsafe_allow_html = True)
    #st.write("Floor Price : ",rounded_floor_price," Owners : ",owners," Total Listed : ",totalListed," Total Volume : ",rounded_totalVolume)
    col1, col2, col3 ,col4 ,col5 = st.columns(5)

    col1.metric("Floor Price", _rounded_floor_price,"N/A") 
    col2.metric("Owners", _owners,"N/A") 
    col3.metric("Total Listed", _totalListed,"N/A") 
    col4.metric("Pending Transactions", _pending,"N/A") 
    col5.metric("Total Volume", _rounded_totalVolume,"N/A") 
    while True:
        # 调用 create_historical_chart 函数
        create_historical_chart('History_data.json')

        # 暂停 5 分钟
        time.sleep(300)
    st.markdown("<hr/>", unsafe_allow_html = True)
    
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

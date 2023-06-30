import streamlit as st
from typing import List
from dataclasses import dataclass
from itertools import product
import json;
from PIL import Image
import requests

url = "https://api-mainnet.magiceden.dev/v2/ord/btc/stat?collectionSymbol=bitcoin-frogs"
bearer_token = '35d17fa0-06be-434f-8357-9d17dd537d13'
headers = {'Authorization': 'Bearer ' + bearer_token}
response = requests.get(url, headers=headers)
json_data = json.loads(response.text)
floor_price = float(json_data['floorPrice'])*0.00000001
rounded_floor_price = round(floor_price, 3)
owners = int(json_data["owners"])
totalListed =int(json_data["totalListed"])

with open('bitcoin_frogs_items.json') as f:
    data = json.load(f)

filtered_frogs = []

def main():    
    st.write("Main Info - ","Floor Price (ME) : ",rounded_floor_price," Owners : ",owners," Total Listed : ",totalListed)
    #st.write("<p style='margin-top: 20px; margin-bottom: 20px'></p>", unsafe_allow_html=True)
   
    st.sidebar.image("https://cdn.discordapp.com/attachments/1117712065293987840/1124212987243278356/rpbp.png", use_column_width=True)
    #st.sidebar.title("Bitcoin Frogs")
    st.sidebar.title("Bitcoin Frogs Traits Filter")
    
    # 属性选项
    backgrounds = ["Brown", "Red", "Olive", "Grey", "Pink", "Dark Blue", "Orange", "Blue", "Green", "Light Blue", "Bitcoin Orange", "Black", "Yellow"]
    clothing = ["Prison Jumpsuit", "Green Hoodie", "Businessman", "Bling", "Wizard Robe", "None", "Leather Jacket", "Leather Dust Coat", "Red Hoodie", "Elvis", "Jersey", "Orange Checkered", "Blue Jacket", "Fur Coat", "23 TShirt", "Black Vest", "Karate Outfit", "Black Hoodie", "Purple Checkered", "Kings Robes", "Vest and Shirt", "Ninja", "Clown", "Priest", "Red Overalls", "Grey Suit", "Blue Hoodie", "Hawaiian", "Hitman", "Yellow Hoodie", "Bowtie", "Bitcoin Shirt", "Gentlemans Suit", "Spartan"]
    bodies = ["Spotted", "Electro", "Dark Red", "Green", "Tron"]
    mouths = ["Bitcoin Pizza", "None", "Magicians Moustache", "Bubblegum", "Dictators Moustache", "Cigar", "Tongue Out", "Clown Nose", "Big Moustache", "Pipe"]
    eyes = ["Dank Shades", "Happy", "Visor", "Monocle", "none", "Frown", "Powerful", "Golden Sunglasses", "Nakamoto Glasses", "Angry", "3D Glasses", "Purple Cosmic Eyes"]

    # 用户选择过滤条件
    desired_backgrounds = st.sidebar.multiselect("Select desired backgrounds", backgrounds)
    desired_clothing = st.sidebar.multiselect("Select desired clothing", clothing)
    desired_bodies = st.sidebar.multiselect("Select desired bodies", bodies)
    desired_mouths = st.sidebar.multiselect("Select desired mouths", mouths)
    desired_eyes = st.sidebar.multiselect("Select desired eyes", eyes)

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
        st.write("Filtered Bitcoin Frogs:   [ " + str(len(filtered_frogs)) + " ] Frogs")
        for frog in filtered_frogs:
            frog["image_url"] = 'https://ordiscan.com/content/'+str(frog["inscription_id"])
            #st.write(frog)
            #st.image('https://ordiscan.com/content/'+str(frog["inscription_id"]), caption=frog["item_name"],width=576/2)
        
        # 定义每列的宽度
        col_width = 5
        
        # 间距的像素值
        #spacing = 200  

        # 创建网格布局
        cols = st.columns(col_width)
        # 显示图片
        for i, frog in enumerate(filtered_frogs):
            with cols[i % col_width]:
                st.image(frog["image_url"], caption=frog["item_name"],width=576/4)
            #st.write("&nbsp;" * spacing, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

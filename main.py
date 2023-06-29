import streamlit as st
from typing import List
from dataclasses import dataclass
from itertools import product
import json;
from PIL import Image



with open('bitcoin_frogs_items.json') as f:
    data = json.load(f)

filtered_frogs = []

def main():
    st.sidebar.title("Frog Filter")
    
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
        st.write("Filtered Frogs:")
        for frog in filtered_frogs:
            #st.write(frog)
            
            print(frog["item_name"])
            st.image('https://ordiscan.com/content/'+str(frog["inscription_id"]), caption=frog["item_name"],width=160,use_column_width =True)

if __name__ == "__main__":
    main()

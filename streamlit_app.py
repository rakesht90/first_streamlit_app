import streamlit as st
import pandas


st.title('My parents new healthy dinner')

st.header('Breakfast Menu')
st.text('🥣Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
st.dataframe(fruits_to_show)

st.header("Fruityvice Fruit Advice!")
import requests

fruit_choice = st.text_input('What fruit would you like information about?','Kiwi')
st.write('The user entered ', fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
fruityvice_normalized= pandas.json_normalize(fruityvice_response.json())
st.dataframe(fruityvice_normalized)
import snowflake.connector

st.header("Fruit load list contains:")
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from FRUIT_LOAD_LIST")
my_data_all = my_cur.fetchall()
fruit= pandas.DataFrame(my_data_all)
st.dataframe(fruit)
fruit_entered = st.text_input('What fruit would you like to add?')
st.write('Thanks for adding', fruit_entered)
my_cur.execute("inser into FRUIT_LOAD_LIST values(fruit_entered)")
my_cur.execute("select * from FRUIT_LOAD_LIST")


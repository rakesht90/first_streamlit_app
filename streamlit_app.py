import streamlit as st
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


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

#import requests
#create the repeatable code block (called function)
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ this_fruit_choice)
    fruityvice_normalized= pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
# new section to display fruityvice api response
st.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = st.text_input('What fruit would you like information about?')
    if not fruit_choice:
           st.error("Please select a fruit to get information.")
    else:
         back_from_function = get_fruityvice_data(fruit_choice)
         st.dataframe(back_from_function)
except URLError as e:
     st.error()
     st.stop()
#import snowflake.connector


st.header("Fruit load list contains:")
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from FRUIT_LOAD_LIST")
my_data_all = my_cur.fetchall()
fruit= pandas.DataFrame(my_data_all)
st.dataframe(fruit)
fruit_entered = st.text_input('What fruit would you like to add?')
st.write('Thanks for adding', fruit_entered)
my_cur = my_cnx.cursor()
my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values('from st')")
my_cur.execute("select * from FRUIT_LOAD_LIST")
my_data_all = my_cur.fetchall()
fruit = pandas.DataFrame(my_data_all)
st.dataframe(fruit)

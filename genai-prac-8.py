

from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
import streamlit as st
import os
os.environ['GOOGLE_API_KEY']='AIzaSyAyaZeWICvZBmJZmnJmchQIK9nXfQvfieM'
llm=init_chat_model("google_genai:gemini-2.5-flash-lite")
def generate_restaurant_name_and_item(cuisine):
    prompt_template_name = PromptTemplate(
    input_variables = ["cuisine"],
    template =("I want to open a restaurant for {cuisine} food. Suggest one fancy restaurant name. Output only the name. No postamble.")
    )
    name_chain=prompt_template_name|llm
    name={"restaurant_name":name_chain.invoke({"cuisine":cuisine}).content}
    prompt_template_items = PromptTemplate(
        input_variables=["restaurant_name"],
        template=("Suggest some menu items for {restaurant_name}. Return only comma-seperated values. No preamble. No postamble.")
    )
    food_item_chain = prompt_template_items|llm
    food_item=food_item_chain.invoke(name).content
    return food_item.split(','), name
if __name__=="__main__":
    st.title("Restaurant name generated & name")
    cuisine=st.sidebar.selectbox("Pick a continent",("Select a continent",
    "Indian","Mexican","Italian","Arabic","American"),)
    if cuisine!="Select a continent":
        food_item_name, res_name=generate_restaurant_name_and_item(cuisine)
        st.header(res_name["restaurant_name"].strip())
        st.write("**Menu Items**")
        for item in food_item_name:
            st.write("-",item)

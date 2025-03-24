import streamlit as st
from scrape import scrape_website
from operations import find_ques

st.title("AI Web Scraper")
number = st.text_input("Leetcode question number:")

if st.button("Enter"):
    st.write("Entering into database")
    result = find_ques(int(number))

    st.write(f"https://leetcode.com/problems/{result[0]}/description/")
    st.write(f"{result[1]}")
    st.write(f"{result[2]}")
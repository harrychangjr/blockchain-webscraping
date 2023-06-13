import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Blockchain Analysis - News Scraper", page_icon = "🖥️", layout = "centered", initial_sidebar_state = "auto")


url = "https://decrypt.co/"
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

articles = soup.find_all("div", class_="article")

st.write(articles)

for article in articles:
    title_element = article.find("h2", class_="title")
    title = title_element.text.strip()
    st.write(title)


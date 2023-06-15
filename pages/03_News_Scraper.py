import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.set_page_config(page_title="Blockchain Analysis - News Scraper", page_icon = "🖥️", layout = "centered", initial_sidebar_state = "auto")


url = "https://blockchain.news"
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

articles = soup.find_all("div", class_="blog-content")

st.write(articles)

# Create a list to store the scraped data
data = []

for article in articles:
    title_element = article.find("a", class_="post-title") or article.find("h1", class_="post-title")
    title = title_element.text.strip() if title_element else None
    
    # Extract the link
    link_element = article.find('a')
    link = link_element['href'] if link_element else None
    link = url + link if link_element else None

    # Add the data to the list
    data.append({'Title': title, 'Link': link})

# Convert the list of dictionaries into a Pandas DataFrame
df = pd.DataFrame(data)

# Remove rows with None values for both title and link
df = df.dropna(subset=['Title', 'Link'], how='all')

# Print the DataFrame
st.write(df)


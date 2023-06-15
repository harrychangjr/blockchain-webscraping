import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from st_aggrid import AgGrid

st.set_page_config(page_title="Blockchain Analysis - News Scraper", page_icon = "🖥️", layout = "centered", initial_sidebar_state = "auto")


url = "https://blockchain.news"
response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

articles = soup.find_all("div", class_="blog-content")

st.write(articles)

# Create a list to store the scraped data
data = []

for article in articles:
    # Extract the title
    title_element = article.find("a", class_="post-title") or article.find("h1", class_="post-title")
    title = title_element.text.strip() if title_element else None
    
    # Extract the link
    link_element = article.find('a')
    link = link_element['href'] if link_element else None
    link = url + link if link_element else None

    # Extract the date
    #date_element = article.find('time')
    #date = date_element['datetime'] if date_element else None

    if link:
        # Send an HTTP GET request to the article link
        article_response = requests.get(link)
        
        if article_response.ok:
            article_soup = BeautifulSoup(article_response.content, 'html.parser')
            
            # Find the element containing the article content
            author = article_soup.find('span', id="author")
            author_clean = author.text.strip() if author else None

            # Extract author URL
            author_cleaned = author_clean.replace(" ", "-") if author_clean else None
            author_url = url + "/Profile/" + author_cleaned if author_cleaned else None

            # Extract the date
            date_element = article.find('time')
            date = date_element['datetime'] if date_element else None

            # Extract the text content of the time tag (date and time)
            time = date_element.text.strip() if date_element else None

            # Extract the body content of the article
            content = article_soup.find("div", class_="textbody")
            content = content.get_text() if content else None

            if author_url:
                # Send an HTTP GET request to the article link
                profile_response = requests.get(author_url)

                if profile_response.ok:
                    profile_soup = BeautifulSoup(profile_response.content, 'html.parser')

                    # Find the element containing the author profile
                    profile = profile_soup.find("div", class_="profile-user-desc")
                    profile = profile.get_text() if profile else None

                    # Add the data to the list
                    data.append({'Title': title, 'Link': link, 'Date': date, 'Time': time, 
                    'Author': author_clean, 'Author URL': author_url, 'Author Profile': profile,
                    'Content': content})


    # Add the data to the list
   #data.append({'Title': title, 'Link': link, 'Date': date, 'Time': time, 'Content': article_content})

# Convert the list of dictionaries into a Pandas DataFrame
df = pd.DataFrame(data)

# Remove rows with None values for both title and link
df = df.dropna(subset=['Title', 'Link'], how='all')

# Print the DataFrame
AgGrid(df)

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(df)
# adding a download button to download csv file
st.download_button( 
    label="Download data as CSV",
    data=csv,
    file_name='BlockchainNews.csv',
    mime='text/csv',
)


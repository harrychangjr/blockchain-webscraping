import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from st_aggrid import AgGrid
import re

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def remove_substring(string):
    pattern = r"/\w+/"  # Regex pattern to match '/<word>/'
    result = re.sub(pattern, "/", string)
    return result

st.set_page_config(page_title="Blockchain Analysis - News Scraper", page_icon = "🖥️", layout = "centered", initial_sidebar_state = "auto")

st.header("News Scraper")

tab1, tab2 = st.tabs(["blockchain.news - Main Page", "blockchain.news - Sub-Pages"])

with tab1:

    st.subheader("https://blockchain.news")


    ### MAIN PAGE SCRAPER
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
                content = content.text.strip() if content else None

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


 
    # Convert the list of dictionaries into a Pandas DataFrame
    df = pd.DataFrame(data)

    # Remove rows with None values for both title and link
    df = df.dropna(subset=['Title', 'Link'], how='all')

    # Print the DataFrame
    AgGrid(df)



    csv = convert_df(df)
    # adding a download button to download csv file
    st.download_button( 
        label="Download data as CSV",
        data=csv,
        file_name='BlockchainNews.csv',
        mime='text/csv',
    )

# other pages to scrape
# /tag/Cryptocurrency/0 to xxx
# /tag/Bitcoin/0 to xxx
# /tag/Bitcoin-price/0 to xxx
# /tag/Ethereum/0 to xxx
# /tag/Cardano/0 to xxx
# /tag/Ripple/0 to xxx
# /tag/Stablecoin/0 to xxx
# /tag/CBDC/0 to xxx
# /tag/DeFi/0 to xxx
# /NFT/0 to xxx
# /tag/regulation/0 to xxx
# /tag/legal/0 to xxx
# /tag/regulation/0 to xxx
# /tag/legal/0 to xxx
# /tag/cybercrime/0 to xxx
# /tag/industry/0 to xxx
# /tag/exchanges/0 to xxx
# /tag/mining/0 to xxx
# /tag/Data-Service/0 to xxx
# /tag/technology/0 to xxx
# /tag/Enterprise/0 to xxx
# /tag/exchanges/0 to xxx
# /tag/Blockchain-Application/0 to xxx
# analysis, interview, wiki, price, learn, press%20release, opinion, prnewswire



with tab2:
    st.subheader("blockchain.news - Sub-Pages")
    def scrape_data(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.find_all("div", class_="col-xl-8half col-xl-8 col-7")
        st.write(articles)

        data = []

        for article in articles:
            # Extract the title
            title_element = article.find("strong")
            title = title_element.text.strip() if title_element else None

            # Extract the link
            link_element = article.find('a')
            link = link_element['href'] if link_element else None
            link = remove_substring(link)
            link = url + link if link_element else None

            # Extract the date
            date_element = article.find('font', class_="post-desc")
            date = date_element.text.strip() if date_element else None
            #time = date_element.text.strip() if date_element else None

            # Extract the time
            
            # Extract the author name
            author_element = article.find("div", class_="col-6 align-left").find("a")
            author_name = author_element.text.strip() if author_element else None

            # Extract the author link
            author_url = author_element["href"] if author_element else None
            author_url = "https://blockchain.news" + author_url

            # Extract the author profile and article content
            #if author_url:
                #profile_response = requests.get(author_url)
                #if profile_response.ok and article_response.ok:
                    #profile_soup = BeautifulSoup(profile_response.content, 'html.parser')

                    #profile = profile_soup.find("div", class_="profile-user-desc")
                    #profile = profile.get_text() if profile else None

            # Extract the content from the article link
            if link:
                article_response = requests.get(link)
                if article_response.ok:
                    article_soup = BeautifulSoup(article_response.content, 'html.parser')
                    content_element = article_soup.find("div", class_="textbody")
                    content = content_element.get_text() if content_element else None
                
                    # Extract the author profile from the author link
                    if author_url:
                        author_response = requests.get(author_url)
                        if author_response.ok:
                            author_soup = BeautifulSoup(author_response.content, 'html.parser')
                            profile_element = author_soup.find("div", class_="profile-user-desc")
                            profile = profile_element.get_text() if profile_element else None
                        else:
                            profile = None
                    else:
                        profile = None
                else:
                    content = None
                    profile = None
            else:
                content = None
                profile = None

            data.append({
                'Title': title,
                'Link': link,
                'Date': date,
                'Author': author_name,
                'Author URL': author_url,
                'Content': content,
                'Author Profile': profile
            })

        return data
    
    subpage_data = scrape_data("https://blockchain.news/analysis")

    st.write(subpage_data)

    # Convert the list of dictionaries into a Pandas DataFrame
    df = pd.DataFrame(subpage_data)

    # Remove rows with None values for both title and link
    # df = df.dropna(subset=['Title', 'Link'], how='all')

    # Print the DataFrame
    AgGrid(df)  
    #st.write(df) 


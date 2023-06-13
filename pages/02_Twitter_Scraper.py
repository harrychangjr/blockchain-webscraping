import streamlit as st
import snscrape.modules.twitter as sntwitter
import pandas as pd

st.set_page_config(page_title="Blockchain Analysis - Twitter Scraper", page_icon = "🖥️", layout = "centered", initial_sidebar_state = "auto")

def scrape(usernames, path):

    tweets = []

    for i, name in enumerate(usernames):
        for j,tweet in enumerate(sntwitter.TwitterSearchScraper('from:{}'.format(usernames[i])).get_items()):
            if j>10:
                break
            tweets.append([tweet.date, tweet.id, tweet.rawContent, tweet.url,\
                            tweet.user.username, tweet.user.followersCount,tweet.replyCount,\
                            tweet.retweetCount, tweet.likeCount, tweet.quoteCount, tweet.lang,\
                            # tweet.source, tweet.sourceUrl, tweet.sourceLabel,\
                            tweet.links, tweet.media, tweet.retweetedTweet, tweet.quotedTweet,\
                            tweet.inReplyToTweetId, tweet.inReplyToUser, tweet.mentionedUsers,\
                            tweet.coordinates, tweet.place, tweet.hashtags, tweet.cashtags, tweet.card])
            
    columns = ['date', 'id', 'rawContent', 'url',\
        'username', 'followerCount', 'replyCount',\
        'retweetCount', 'likeCount', 'quoteCount', 'langugage',\
        # 'source', 'sourceURL', 'sourceLabel',\
        'links', 'media', 'retweetedTweet', 'quotedTweet',\
        'inReplyToTweetId', 'inReplyToUser', 'mentionedUsers',
        'coordinates', 'place', 'hashtags', 'cashtags', 'card']
    
    df = pd.DataFrame(tweets, columns=columns)
    df.to_csv(path)

    return df

def scrape1(usernames, path): #chatgpt
    tweets = []

    for username in usernames:
        for j, tweet in enumerate(sntwitter.TwitterSearchScraper('from:{}'.format(username)).get_items()):
            tweets.append([
                tweet.date, tweet.id, tweet.content, tweet.url, tweet.user.username,
                tweet.user.followersCount, tweet.replyCount, tweet.retweetCount,
                tweet.likeCount, tweet.quoteCount, tweet.lang,
                tweet.links, tweet.media, getattr(tweet, 'retweetedTweet', None),
                getattr(tweet, 'quotedTweet', None), tweet.inReplyToTweetId,
                tweet.inReplyToUser, tweet.mentionedUsers, getattr(tweet, 'coordinates', None),
                getattr(tweet, 'place', None), tweet.hashtags, tweet.cashtags,
                getattr(tweet, 'card', None)
            ])

    columns = [
        'date', 'id', 'rawContent', 'url', 'username', 'followersCount', 'replyCount',
        'retweetCount', 'likeCount', 'quoteCount', 'language', 'links', 'media',
        'retweetedTweet', 'quotedTweet', 'inReplyToTweetId', 'inReplyToUser',
        'mentionedUsers', 'coordinates', 'place', 'hashtags', 'cashtags', 'card'
    ]

    df = pd.DataFrame(tweets, columns=columns)
    df.to_csv(path, index=False)

    return df

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

tab1, tab2 = st.tabs(["CoinGecko", "CoinMarketCap"])

with tab1:
    st.subheader("CoinGecko")

    cg10 = pd.read_csv('original_files/coinGeckoAggregateFlat.csv')['links_twitter_screen_name'].dropna()[:10]
    st.write("**Top 10 Coins - CoinGecko**")
    st.write(cg10)

    if st.button('Scrape Data from CoinGecko'):
        scrape1(list(cg10), 'coinGeckoTweets_scraped.csv')
        coinGeckoTweets_scraped = pd.read_csv('coinGeckoTweets_scraped.csv')
        st.write(coinGeckoTweets_scraped)
        #converting the sample dataframe
        csv = convert_df(coinGeckoTweets_scraped)
        #adding a download button to download csv file
        st.download_button( 
        label="Download data as CSV",
        data=csv,
        file_name='coinGeckoTweets_scraped.csv',
        mime='text/csv',
    )

with tab2:
    st.subheader("CoinMarketCap")

    cmc10 = pd.read_csv('original_files/coinMarketCapAggregateFlat.csv')['data_twitter_username'].dropna()[:10]
    st.write("**Top 10 Coins - CoinMarketCap**")
    st.write(cmc10)

    if st.button('Scrape Data from CoinMarketCap'):
        scrape1(list(cmc10), 'coinMarketCapTweets_scraped.csv')
        coinMarketCapTweets_scraped = pd.read_csv('coinMarketCapTweets_scraped.csv')
        st.write(coinMarketCapTweets_scraped)
        #converting the sample dataframe
        csv = convert_df(coinMarketCapTweets_scraped)
        #adding a download button to download csv file
        st.download_button( 
        label="Download data as CSV",
        data=csv,
        file_name='coinMarketCapTweets_scraped.csv',
        mime='text/csv',
    )

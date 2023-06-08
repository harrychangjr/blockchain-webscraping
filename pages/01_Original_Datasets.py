import streamlit as st
import pandas as pd

coinGeckoAggregateFlat = pd.read_csv("original_files/coinGeckoAggregateFlat.csv") #given
coinGeckoTweets = pd.read_csv("original_files/coinGeckoTweets.csv") #scraped
coinMarketCapAggregateFlat = pd.read_csv("original_files/coinGeckoTweets.csv") #given
coinMarketCapTweets = pd.read_csv("original_files/coinGeckoTweets.csv") #scraped

st.subheader("Source: https://coingecko.com")

st.write("Given dataset: coinGeckoAggregateFlat.csv")
st.write(coinGeckoAggregateFlat)

st.write("Scraped dataset: coinGeckoTweets.csv")
st.write(coinGeckoTweets)

st.subheader("Source: https://coinmarketcap.com")

st.write("Given dataset: coinGeckoAggregateFlat.csv")
st.write(coinMarketCapAggregateFlat)

st.write("Scraped dataset: coinMarketCapTweets.csv")
st.write(coinMarketCapTweets)
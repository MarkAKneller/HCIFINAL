import streamlit as st
import pandas as pd
import requests
import json

# Set up the page
st.title('Cryptocurrency Analysis App')
st.write('This app uses the Alpha Vantage API to fetch cryptocurrency data.')

# Alpha Vantage API Key (replace with your own key)
API_KEY = 'YOUR_ALPHA_VANTAGE_API_KEY'

# Function to fetch cryptocurrency data
def get_crypto_data(symbol):
    url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={symbol}&to_currency=USD&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data

# User input for the cryptocurrency symbol
symbol = st.text_input('Enter a cryptocurrency symbol (e.g., BTC, ETH):')

# Button to fetch data
if st.button('Get Data'):
    data = get_crypto_data(symbol)
    if 'Realtime Currency Exchange Rate' in data:
        st.write(data['Realtime Currency Exchange Rate'])
    else:
        st.error('Error fetching data. Please check the symbol and try again.')

# Run the app: streamlit run app.py
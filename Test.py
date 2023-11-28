import streamlit as st
import pandas as pd
import requests
import plotly.graph_objs as go

# Initialize session state
if 'df' not in st.session_state:
    st.session_state['df'] = pd.DataFrame()
if 'data' not in st.session_state:
    st.session_state['data'] = {}

# Alpha Vantage API Key and Base URL
url = "https://alpha-vantage.p.rapidapi.com/query"
headers = {
    "X-RapidAPI-Key": "7300c21118mshb9b8940b597a52cp1d3136jsnd9f0c95239bd",
    "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
}

# Function to fetch cryptocurrency data
def get_crypto_data(symbol, market):
    querystring = {
        'market': market,
        'function': 'DIGITAL_CURRENCY_DAILY',
        "symbol": symbol
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    return data

# Set up the page
st.title('Cryptocurrency Analysis Dashboard')
st.write("Explore the dynamic world of cryptocurrencies. Analyze daily trends, prices, and volumes at a glance.")

# Sidebar for user input
st.sidebar.header('Customize Your Analysis')
symbol = st.sidebar.selectbox('Cryptocurrency Symbol', ['BTC', 'SOL', 'ETC'], help='Enter a cryptocurrency symbol (e.g., BTC, ETH)')
market = st.sidebar.selectbox('Market Currency', ['USD', 'EUR', 'JPY'], help='Select the currency for market comparison')
resolution = st.sidebar.slider('Select Graph Resolution (Hours)', 1, 24, 1, help='Choose the resolution of the candlestick chart (hours)')

# Fetch data button
if st.sidebar.button('Analyze'):
    with st.spinner('Fetching data...'):
        st.session_state['data'] = get_crypto_data(symbol, market)
        if 'Time Series (Digital Currency Daily)' in st.session_state['data']:
            st.success(f'Data for {symbol} successfully retrieved!')
            st.session_state['df'] = pd.DataFrame.from_dict(
                st.session_state['data']['Time Series (Digital Currency Daily)'], orient='index')
            st.session_state['df'] = st.session_state['df'].apply(pd.to_numeric)
            st.subheader(f'Daily Data for {symbol} in {market}')
            st.dataframe(st.session_state['df'].head())
        else:
            st.error('Error fetching data. Please check the symbol and try again.')

# Check if DataFrame is not empty before plotting
if not st.session_state['df'].empty:
    # Calculate daily price variance
    st.session_state['df']['Price Variance'] = st.session_state['df']['2. high'].sub(st.session_state['df']['3. low'])

    # Filter data based on resolution
    st.session_state['df'] = st.session_state['df'].resample(f'{resolution}H').agg({
        '1b. open (USD)': 'first',
        '2. high': 'max',
        '3. low': 'min',
        '5. volume': 'sum',
        '4a. close (USD)': 'last',
        'Price Variance': 'mean'
    })

    # Create a candlestick chart
    trace = go.Candlestick(x=st.session_state['df'].index,
                           open=st.session_state['df']['1b. open (USD)'],
                           high=st.session_state['df']['2. high'],
                           low=st.session_state['df']['3. low'],
                           close=st.session_state['df']['4a. close (USD)'])
    layout = go.Layout(title=f'{symbol} Candlestick Chart ({resolution}H Resolution)',
                       xaxis=dict(title='Date'),
                       yaxis=dict(title=f'Price in {market}'))
    fig = go.Figure(data=[trace], layout=layout)
    st.plotly_chart(fig)
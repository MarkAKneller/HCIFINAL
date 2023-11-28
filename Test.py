import streamlit as st
import pandas as pd
import requests
import plotly.graph_objs as go
from datetime import datetime

# Alpha Vantage API Key and Base URL
url = "https://alpha-vantage.p.rapidapi.com/query"
headers = {
    "X-RapidAPI-Key": "7300c21118mshb9b8940b597a52cp1d3136jsnd9f0c95239bd",
    "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
}

# Initialize session state for storing data and selected columns
if 'data' not in st.session_state:
    st.session_state['data'] = None
if 'selected_columns' not in st.session_state:
    st.session_state['selected_columns'] = []

# Function to fetch cryptocurrency data
def get_crypto_data(symbol, market):
    querystring = {
        'market': market,
        'function': 'DIGITAL_CURRENCY_DAILY',
        "symbol": symbol
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

# Set up the page
st.title('Cryptocurrency Analysis Dashboard')
st.write("Explore the dynamic world of cryptocurrencies. Analyze daily trends, prices, and volumes at a glance.")

# Sidebar for user input
st.sidebar.header('Customize Your Analysis')
symbol = st.sidebar.selectbox('Cryptocurrency Symbol', ['BTC', 'ETH', 'XRP'], help='Enter a cryptocurrency symbol (e.g., BTC, ETH)')
market = st.sidebar.selectbox('Market Currency', ['USD', 'EUR', 'JPY'], help='Select the currency for market comparison')
start_date, end_date = st.sidebar.date_input("Select Date Range", [datetime.now().date(), datetime.now().date()], help='Select start and end dates for the data')

# Validate date range
if start_date > end_date:
    st.sidebar.error("End date must be after start date.")

# Fetch data button
if st.sidebar.button('Fetch Data'):
    if start_date <= end_date:
        with st.spinner('Fetching data...'):
            st.session_state['data'] = get_crypto_data(symbol, market)
            st.session_state['selected_columns'] = []  # Reset column selection
            if 'Time Series (Digital Currency Daily)' in st.session_state['data']:
                st.success(f'Data for {symbol} successfully retrieved!')
            else:
                st.error('Error fetching data. Please check the symbol and try again.')
    else:
        st.error('Invalid date range. Please select a valid range.')

# Display checkboxes for column selection if data is available
if st.session_state['data']:
    df = pd.DataFrame.from_dict(st.session_state['data']['Time Series (Digital Currency Daily)'], orient='index')
    df = df.apply(pd.to_numeric)
    df.index = pd.to_datetime(df.index)
    df_filtered = df[(df.index.date >= start_date) & (df.index.date <= end_date)]

    st.sidebar.header('Select Data Columns to Display')
    for col in df_filtered.columns:
        if st.sidebar.checkbox(col, col in st.session_state['selected_columns']):
            if col not in st.session_state['selected_columns']:
                st.session_state['selected_columns'].append(col)
        elif col in st.session_state['selected_columns']:
            st.session_state['selected_columns'].remove(col)

    # Filter DataFrame based on selected columns
    if st.session_state['selected_columns']:
        df_display = df_filtered[st.session_state['selected_columns']]
        st.subheader(f'Daily Data for {symbol} in {market}')
        st.dataframe(df_display)  # Displaying the filtered data with selected columns

    # Candlestick Chart
    required_columns_candlestick = ['1a. open (USD)', '2a. high (USD)', '3a. low (USD)', '4a. close (USD)']
    if all(col in df_filtered.columns for col in required_columns_candlestick):
        fig_candlestick = go.Figure(data=[go.Candlestick(x=df_filtered.index,
                                                         open=df_filtered['1a. open (USD)'],
                                                         high=df_filtered['2a. high (USD)'],
                                                         low=df_filtered['3a. low (USD)'],
                                                         close=df_filtered['4a. close (USD)'])])
        fig_candlestick.update_layout(title=f'{symbol} Candlestick Chart',
                                      xaxis=dict(title='Date'),
                                      yaxis=dict(title=f'Price in {market}'))
        st.plotly_chart(fig_candlestick)
    else:
        st.warning('Required columns for the candlestick chart are not available.')
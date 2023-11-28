import streamlit as st
import pandas as pd
import requests

# Alpha Vantage API Key and Base URL
API_KEY = 'IBR8NA5DH28CVSUP'
BASE_URL = "https://www.alphavantage.co/query"

# Function to fetch cryptocurrency data
def get_crypto_data(symbol, market):
    params = {
        'function': 'DIGITAL_CURRENCY_DAILY',
        'symbol': symbol,
        'market': market,
        'apikey': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    return data

# Set up the page
st.title('Cryptocurrency Analysis Dashboard')
st.write("Explore the dynamic world of cryptocurrencies. Analyze daily trends, prices, and volumes at a glance.")

# Sidebar for user input
st.sidebar.header('Customize Your Analysis')
symbol = st.sidebar.text_input('Cryptocurrency Symbol', 'BTC', help='Enter a cryptocurrency symbol (e.g., BTC, ETH)')
market = st.sidebar.selectbox('Market Currency', ['USD', 'EUR', 'JPY'], help='Select the currency for market comparison')

# Fetch data button
if st.sidebar.button('Analyze'):
    with st.spinner('Fetching data...'):
        data = get_crypto_data(symbol, market)
        if 'Time Series (Digital Currency Daily)' in data:
            st.success(f'Data for {symbol} successfully retrieved!')
            df = pd.DataFrame.from_dict(data['Time Series (Digital Currency Daily)'], orient='index')
            df = df.apply(pd.to_numeric)
            st.subheader(f'Daily Data for {symbol} in {market}')
            st.dataframe(df.head())

            # Plotting charts with Streamlit's native functions
            st.subheader('Price Trend')
            st.line_chart(df['4a. close (USD)'].head(30))

            st.subheader('Trading Volume')
            st.bar_chart(df['5. volume'].head(30))
        else:
            st.error('Error fetching data. Please check the symbol and try again.')

# Additional interactive elements
if st.sidebar.checkbox('Show Raw Data', False):
    st.subheader('Raw JSON Data')
    st.json(data)

# Example map (static for demonstration)
if st.sidebar.checkbox('Show Example Map', False):
    st.subheader('Global Market Overview')
    map_data = pd.DataFrame({'lat': [37.76, 40.71], 'lon': [-122.4, -74.0]})
    st.map(map_data)

# Feedback and messages
if st.sidebar.button('Show Success Message'):
    st.success('Success! Your analysis is ready.')
if st.sidebar.button('Show Info Message'):
    st.info('Did you know? Cryptocurrency markets are highly volatile.')
if st.sidebar.button('Show Warning Message'):
    st.warning('Warning: Cryptocurrency investments are subject to market risks.')

# Additional Widgets
st.sidebar.subheader('Additional Settings')
time_frame = st.sidebar.slider('Select Time Frame (Days)', 1, 60, 30)
st.sidebar.write(f'Analyzing the last {time_frame} days')

# Radio button for chart type
chart_type = st.sidebar.radio('Choose Chart Type', ['Line Chart', 'Bar Chart'])
if chart_type == 'Line Chart':
    st.line_chart(df['4a. close (USD)'].tail(time_frame))
elif chart_type == 'Bar Chart':
    st.bar_chart(df['5. volume'].tail(time_frame))

# Number input for custom analysis
custom_value = st.sidebar.number_input('Enter a custom value', min_value=0, max_value=10000, value=5000)
st.sidebar.write('Your custom value is:', custom_value)

# Run the app: streamlit run HCI.py

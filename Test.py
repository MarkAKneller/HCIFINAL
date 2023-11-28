import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

# Initialize session state
if 'df' not in st.session_state:
    st.session_state['df'] = pd.DataFrame()

# Alpha Vantage API Key and Base URL
API_KEY = 'IBR8NA5DH28CVSUP'  # Replace with your actual API key
BASE_URL = "http://apilayer.net/api/"

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
symbol = st.sidebar.selectbox('Cryptocurrency Symbol', ['BTC', 'ETH', 'SOL'], help='Enter a cryptocurrency symbol (e.g., BTC, ETH)')
market = st.sidebar.selectbox('Market Currency', ['USD', 'EUR', 'JPY'], help='Select the currency for market comparison')

# Fetch data button
if st.sidebar.button('Analyze'):
    with st.spinner('Fetching data...'):
        data = get_crypto_data(symbol, market)
        if 'Time Series (Digital Currency Daily)' in data:
            st.success(f'Data for {symbol} successfully retrieved!')
            df = pd.DataFrame.from_dict(data['Time Series (Digital Currency Daily)'], orient='index')
            df = df.apply(pd.to_numeric)
            df.index = pd.to_datetime(df.index)
            st.session_state['df'] = df
            st.subheader(f'Daily Data for {symbol} in {market}')
            st.dataframe(df.head())
        else:
            st.error('Error fetching data. Please check the symbol and try again.')

# Check if DataFrame is not empty before plotting
if not st.session_state['df'].empty:
    # Date range selector
    st.sidebar.subheader('Select Date Range')
    start_date = st.sidebar.date_input('Start date', st.session_state['df'].index.min())
    end_date = st.sidebar.date_input('End date', st.session_state['df'].index.max())

    # Filter data based on selection
    filtered_df = st.session_state['df'].loc[start_date:end_date]

    # Calculate daily price change
    closing_price_column = f'4a. close ({market})'  # Adjust column name based on market currency
    filtered_df['Price Change'] = filtered_df[closing_price_column].diff()

    # Plotting the closing price with color based on price change
    if not filtered_df.empty:
        fig, ax = plt.subplots()
        for i in range(1, len(filtered_df)):
            # Determine color (green for increase, red for decrease)
            color = 'green' if filtered_df['Price Change'].iloc[i] >= 0 else 'red'
            ax.plot(filtered_df.index[i-1:i+1], filtered_df[closing_price_column].iloc[i-1:i+1], color=color)

        ax.set_xlabel('Date')
        ax.set_ylabel(f'Closing Price ({market})')
        ax.set_title(f'{symbol} Closing Price in {market}')
        st.pyplot(fig)

# Run the app: streamlit run your_script_name.py


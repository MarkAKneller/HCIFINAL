import geopandas as gpd
import streamlit as st
import pandas as pd
import requests
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import folium
from streamlit_folium import folium_static

# Initialize session state
if 'df' not in st.session_state:
    st.session_state['df'] = pd.DataFrame()
if 'data' not in st.session_state:
    st.session_state['data'] = {}
if 'selected_columns' not in st.session_state:
    st.session_state['selected_columns'] = []
# Alpha Vantage API Key and Base URL

url = "https://alpha-vantage.p.rapidapi.com/query"
headers = {
	"X-RapidAPI-Key": "834bbc8170mshd02e51e16a32289p1476e8jsn1a211a6524a1",
	"X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
}
api_key = "834bbc8170mshd02e51e16a32289p1476e8jsn1a211a6524a1"

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

def get_monthly_crypto_data(symbol, market, api_key):
    url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_MONTHLY&symbol={symbol}&market={market}&apikey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Sidebar for page selection
page = st.sidebar.selectbox(
    "Select a Page",
    ["Homepage", "Comparison", "Candles","Ban Map","Calculator"]
)

if page == "Homepage":
    st.markdown("<h1 style='text-align: center;'>Welcome to the Crypto Analysis Web App</h1>", unsafe_allow_html=True)

    st.markdown(
        """
        Cryptocurrency Analysis made simple! Explore various features to understand 
        crypto trends, prices, and more.
        """
    )

    st.markdown("<h2 style='text-align: center; text-decoration: underline;'>Features</h2>", unsafe_allow_html=True)

    # First row with two columns
    col1, col2 = st.columns(2)

    # Feature 1: Currency Converter Calculator
    with col1:
        st.markdown("<h3 style='text-align: center;'>Currency Converter Calculator</h3>", unsafe_allow_html=True)
        st.write(
            "Convert any selected currency into USD using our handy calculator."
        )
        st.image("https://raw.githubusercontent.com/MarkAKneller/HCIFINAL/main/images/calculator.png",
                 width=300)  # Adjust the width as needed

    # Feature 2: Crypto Comparison Chart
    with col2:
        st.markdown("<h3 style='text-align: center;'>Crypto Comparison Chart</h3>", unsafe_allow_html=True)
        st.write(
            "Select two cryptocurrencies and compare their prices over the last year with our interactive chart."
        )
        st.image("https://raw.githubusercontent.com/MarkAKneller/HCIFINAL/main/images/comparison.png",
                 width=300)  # Adjust the width as needed

    # Second row with two columns
    col3, col4 = st.columns(2)

    # Feature 3: Crypto Ban Map
    with col3:
        st.markdown("<h3 style='text-align: center;'>Crypto Ban Map</h3>", unsafe_allow_html=True)
        st.write(
            "Explore the global map to see countries where crypto is banned."
        )
        st.image("https://raw.githubusercontent.com/MarkAKneller/HCIFINAL/main/images/ban_map.png",
                 width=300)  # Adjust the width as needed

    # Feature 4: Candlestick Data Selection
    with col4:
        st.markdown("<h3 style='text-align: center;'>Candlestick Data</h3>", unsafe_allow_html=True)
        st.write(
            "Select a timeframe and visualize candlestick data for a specific cryptocurrency."
        )
        st.image("https://raw.githubusercontent.com/MarkAKneller/HCIFINAL/main/images/candlestick.jpeg",
                 width=300)  # Adjust the width as needed

    st.markdown("---")

    st.subheader("Get Started")
    st.write(
        "Explore these features in the sidebar and start analyzing cryptocurrencies today!"
    )
    st.warning(
        "⚠️ Cryptocurrency markets are known for their high volatility, which can lead to significant price swings. "
        "Investors should be aware of the risks involved, including the possibility of losing their entire investment. "
        "Volatility is influenced by factors like regulatory news, market manipulation, and the relatively small size of the market compared to traditional securities."

    )

elif page == "Comparison":
    st.title('Select Cryptocurrencies for Comparison')
    selected_crypto_1 = st.selectbox("Select first cryptocurrency", ["", "BTC", "XRP", "ETH", "SOL", "LTC", "BNB", "ADA"])
    selected_crypto_2 = st.selectbox("Select second cryptocurrency", ["", "BTC", "XRP", "ETH", "SOL", "LTC", "BNB", "ADA"])

    if selected_crypto_1 == selected_crypto_2 and selected_crypto_1 != "":
        st.error("Please select two different cryptocurrencies.")
    else:
        crypto_data = None
        try:
            if selected_crypto_1 and selected_crypto_2:
                last_year = datetime.now() - timedelta(days=365)  # Defining last_year

                crypto_data_1 = get_monthly_crypto_data(selected_crypto_1, 'CNY', api_key)
                crypto_data_2 = get_monthly_crypto_data(selected_crypto_2, 'CNY', api_key)

                if crypto_data_1 and 'Time Series (Digital Currency Monthly)' in crypto_data_1 and crypto_data_2 and 'Time Series (Digital Currency Monthly)' in crypto_data_2:
                    # Convert JSON response to DataFrame for plotting - Crypto 1
                    monthly_data_1 = crypto_data_1['Time Series (Digital Currency Monthly)']
                    crypto_df_1 = pd.DataFrame(monthly_data_1).T
                    crypto_df_1.index = pd.to_datetime(crypto_df_1.index)
                    crypto_df_1_last_year = crypto_df_1[crypto_df_1.index >= last_year]

                    # Convert JSON response to DataFrame for plotting - Crypto 2
                    monthly_data_2 = crypto_data_2['Time Series (Digital Currency Monthly)']
                    crypto_df_2 = pd.DataFrame(monthly_data_2).T
                    crypto_df_2.index = pd.to_datetime(crypto_df_2.index)
                    crypto_df_2_last_year = crypto_df_2[crypto_df_2.index >= last_year]

                    fig, ax = plt.subplots(figsize=(10, 6))

                    # Change the plot style
                    plt.style.use('ggplot')  # You can replace 'ggplot' with other styles like 'seaborn', 'fivethirtyeight', etc.

                    # Plotting Crypto 1
                    line_color_1 = st.color_picker(f"Choose line color for {selected_crypto_1}", "#1f77b4")  # Default color is steelblue
                    ax.plot(crypto_df_1_last_year.index, crypto_df_1_last_year['4b. close (USD)'].astype(float),
                            label=selected_crypto_1, color=line_color_1)

                    # Plotting Crypto 2
                    line_color_2 = st.color_picker(f"Choose line color for {selected_crypto_2}", "#ff7f0e")  # Default color is orange
                    ax.plot(crypto_df_2_last_year.index, crypto_df_2_last_year['4b. close (USD)'].astype(float),
                            label=selected_crypto_2, color=line_color_2)

                    ax.legend()

                    # Format y-axis ticks to display USD with a dollar sign
                    def dollar_formatter(y, pos):
                        return f"${y:.2f}"

                    ax.yaxis.set_major_formatter(plt.FuncFormatter(dollar_formatter))

                    # Customize x-axis date format
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))  # Displaying month and year

                    st.pyplot(fig)

                    col1, col2 = st.columns(2)  # Split the layout into two columns

                    with col1:
                        # Calculate high and low values and their dates - Crypto 1
                        high_value_1 = crypto_df_1_last_year['4b. close (USD)'].astype(float).max()
                        low_value_1 = crypto_df_1_last_year['4b. close (USD)'].astype(float).min()
                        high_date_1 = crypto_df_1_last_year[crypto_df_1_last_year['4b. close (USD)'].astype(float) == high_value_1].index[0]
                        low_date_1 = crypto_df_1_last_year[crypto_df_1_last_year['4b. close (USD)'].astype(float) == low_value_1].index[0]

                        # Display info boxes - Crypto 1
                        st.info(f"{selected_crypto_1} - Highest value: ${high_value_1:.2f} on {high_date_1.strftime('%b %d, %Y')}")
                        st.info(f"{selected_crypto_1} - Lowest value: ${low_value_1:.2f} on {low_date_1.strftime('%b %d, %Y')}")

                    with col2:
                        # Calculate high and low values and their dates - Crypto 2
                        high_value_2 = crypto_df_2_last_year['4b. close (USD)'].astype(float).max()
                        low_value_2 = crypto_df_2_last_year['4b. close (USD)'].astype(float).min()
                        high_date_2 = crypto_df_2_last_year[crypto_df_2_last_year['4b. close (USD)'].astype(float) == high_value_2].index[0]
                        low_date_2 = crypto_df_2_last_year[crypto_df_2_last_year['4b. close (USD)'].astype(float) == low_value_2].index[0]

                        # Display info boxes - Crypto 2
                        st.info(f"{selected_crypto_2} - Highest value: ${high_value_2:.2f} on {high_date_2.strftime('%b %d, %Y')}")
                        st.info(f"{selected_crypto_2} - Lowest value: ${low_value_2:.2f} on {low_date_2.strftime('%b %d, %Y')}")

        except Exception as e:
            st.error(f"Error: {str(e)}")


elif page == "Candles":
    st.title('Cryptocurrency Analysis Dashboard')
    st.write("Explore the dynamic world of cryptocurrencies. Analyze daily trends, prices, and volumes at a glance.")

    # Sidebar for user input
    st.sidebar.header('Customize Your Analysis')
    symbol = st.sidebar.selectbox('Cryptocurrency Symbol', ["BTC", "XRP", "ETH", "SOL", "LTC", "BNB", "ADA"],
                                  help='Enter a cryptocurrency symbol (e.g., BTC, ETH)')
    market = st.sidebar.selectbox('Market Currency', ['USD'], help='Select the currency for market comparison')
    start_date, end_date = st.sidebar.date_input("Select Date Range", [datetime.now().date(), datetime.now().date()],
                                                 help='Select start and end dates for the data')

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

        # Remove duplicate columns
        df_filtered = df_filtered.T.drop_duplicates().T

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

elif page == "Ban Map":
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    m = folium.Map(location=[0, 0], zoom_start=2)

    banned_countries = ['Cameroon', 'Aveiro', 'Central African Republic', 'Gabon',
                        'Guyana', 'Lesotho', 'Libya', 'Zimbabwe', 'Qatar', 'Saudi Arabia', 'China']

    folium.GeoJson(
        data=world[['geometry', 'name']],
        style_function=lambda x: {
            'fillColor': 'red'
            if x['properties']['name'] in banned_countries
            else 'green',
            'fillOpacity': .5
            if x['properties']['name'] in banned_countries
            else 0.1,
            'weight': 0.1
        },
    ).add_to(m)

    # Step 4: Streamlit App
    st.title("Countries Crypto is banned")

   

    # Display the Folium Map
    folium_static(m)
    st.info("In some countries, cryptocurrencies are banned due to concerns over financial security, regulatory control, and potential use in illegal activities. "
        "Each country's stance on cryptocurrencies can vary greatly based on its economic policies, financial market stability, and governmental regulations.")
elif page == "Calculator":
    st.title("Currency Converter")

    # Sidebar for user input
    usd_amount = st.number_input('Enter the amount in USD', value=100.0, min_value=0.0)
    coin_symbol = st.selectbox('Select a cryptocurrency', ['BTC', 'ETH', 'XRP', 'SOL', 'BNB', 'LTC', 'ADA'], help='Select a cryptocurrency symbol')

    # Function call to retrieve cryptocurrency data
    data = get_crypto_data(coin_symbol, 'USD')

    if 'Time Series (Digital Currency Daily)' in data:
        time_series_data = data['Time Series (Digital Currency Daily)']
        latest_date = max(time_series_data.keys())  # Get the latest date available

        latest_price = float(time_series_data[latest_date]['4a. close (USD)'])
        coin_amount = usd_amount / latest_price
        st.success(f"The current price of {coin_symbol} is$ {latest_price}")
        st.success(f"${usd_amount} USD can buy you approximately {coin_amount:.8f} {coin_symbol}")
    else:
        st.error('Error fetching data. Please try again.')
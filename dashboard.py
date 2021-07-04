import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go
from PIL import Image
import cufflinks




st.set_page_config(page_title='Cryptocurrency Dashboard',page_icon="chart_with_upwards_trend",initial_sidebar_state="auto")

st.markdown("<h1 style='text-align: center; color: White;'>Cryptocurrency Dashboard</h1>", unsafe_allow_html=True)
st.text("")
st.text("")
st.text("")
# st.text("")
# st.text("")


image1 = Image.open("C:/Users/sourav/btcimg1.jpg")
image2 = Image.open("C:/Users/sourav/ethimg.jpg")
image3 = Image.open("C:/Users/sourav/xrpimg.jpg")


def get_crypto_img(symbol):
    symbol = symbol.upper()

    if symbol == "BTC":
        return  st.image(image1, use_column_width=True)
    elif symbol == "ETH":
        return st.image(image2, use_column_width=True)
    elif symbol == "XRP":
        return st.image(image3, use_column_width=True)
    else:
        return "None"

st.text("")
st.text("")
st.sidebar.markdown("<h1 style='text-align: left; color: White;'>User Input</h1>", unsafe_allow_html=True)


st.text("")
st.text("")
def get_input():
    start_date = st.sidebar.text_input("Start Date","29-04-2013")
    end_date = st.sidebar.text_input("End Date", "07-02-2020")
    crypto_symbol = st.sidebar.selectbox("Crypto Symbol", ("BTC","ETH", "XRP"))

    return start_date, end_date, crypto_symbol



def get_crypto_name(symbol):
    symbol = symbol.upper()

    if symbol == "BTC":
        return "Bitcoin"
    elif symbol == "ETH":
        return "Ethereum"
    elif symbol == "XRP":
        return "Ripple"
    else:
        return "None"



def get_data(symbol,start, end):
    symbol = symbol.upper()

    if symbol == "BTC":
        df = pd.read_csv("C:/Users/sourav/Cleaned coin_Bitcoin.csv")
    elif symbol == "ETH":
        df = pd.read_csv("C:/Users/sourav/Cleaned ETH.csv")
    elif symbol == "XRP":
        df = pd.read_csv("C:/Users/sourav/Cleaned XRP.csv")
    else:
        df = pd.DataFrame(columns=['Date', 'High', 'Low', 'Open', 'Close'])

    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

    df = df.set_index(pd.DatetimeIndex(df['Date'].values))

    return df.loc[start:end]


def get_crypto_pred(symbol,start,end):
    symbol = symbol.upper()

    if symbol == "BTC":
        p_df = pd.read_csv("C:/Users/sourav/rbtc.csv")
    elif symbol == "ETH":
        p_df = pd.read_csv("C:/Users/sourav/xeth.csv")
    elif symbol == "XRP":
        p_df = pd.read_csv("C:/Users/sourav/rxrp.csv")
    else:
        p_df = pd.DataFrame(columns=['Date', 'Close', 'Prediction'])

    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

    p_df = p_df.set_index(pd.DatetimeIndex(p_df['Date'].values))

    return p_df.loc[start:end]



start,end,symbol = get_input()
df = get_data(symbol,start,end)
crypto_name = get_crypto_name(symbol)
get_crypto_img(symbol)
p_df = get_crypto_pred(symbol,start,end)



st.header(crypto_name + "Data")
st.write(df.drop(['Unnamed: 0','Date'],axis=1))

st.header(crypto_name + " High vs Low vs Open vs Close Data")
fig1 = go.Figure(
    data = [go.Candlestick(
        x = df.index,
        open = df['Open'],
        high = df['High'],
        low = df['Low'],
        close = df['Close'],

        increasing_line_color = 'green',
        decreasing_line_color = 'red'
    )
  ]
)
fig1.layout.update(xaxis_rangeslider_visible=True,width=800, height=600)
st.plotly_chart(fig1)


st.header(crypto_name + " Data Statistics")
st.write((df.drop(['Unnamed: 0'],axis=1).describe()))

st.header(crypto_name + " Close Price")
st.write(df['Close'])

st.header(crypto_name + " Open vs Close Data")
def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Open'], name='Stock_open'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name='Stock_Close'))
    fig.layout.update(xaxis_rangeslider_visible=True,width=900, height=600)
    st.plotly_chart(fig)
plot_raw_data()


st.header(crypto_name + " Volume")
st.write(df['Volume'])

st.header(crypto_name + " Prediction")
st.write(p_df.drop(['Date'],axis=1))

st.header(crypto_name + " Close_Data vs Prediction_Data")
# def plot_raw_data():
#     fig2 = go.Figure()
#     fig2.add_trace(go.Scatter(x=p_df['Date'], y=p_df['Close'], name='Close Data'))
#     fig2.add_trace(go.Scatter(x=p_df['Date'], y=p_df['Prediction'], name='Predicted Data'))
#     fig2.layout.update(xaxis_rangeslider_visible=True,width=900, height=600)
#     st.plotly_chart(fig2)
# plot_raw_data()
p_df=p_df.drop(['Date'], axis=1)
fig5 = p_df.iplot(asFigure=True, xTitle="Close Data",yTitle="Prediction Data")
st.plotly_chart(fig5)

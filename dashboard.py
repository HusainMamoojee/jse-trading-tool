import streamlit as st
import yfinance
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go

from datetime import datetime, timedelta

end_date = datetime.today()
start_date = end_date - timedelta(days=365)



st.title("JSE Trading Dashboard")

stocks = {
    "Absa Group (ABG)": "ABG.JO",
    "Anglo American (AGL)": "AGL.JO",
    "Amplats (AMS)": "AMS.JO",
    "AngloGold Ashanti (ANG)": "ANG.JO",
    "AB InBev (ANH)": "ANH.JO",
    "Aspen Pharmacare (APN)": "APN.JO",
    "BHP Group (BHG)": "BHG.JO",
    "Bid Corporation (BID)": "BID.JO",
    "Bidvest (BVT)": "BVT.JO",
    "Richemont (CFR)": "CFR.JO",
    "Clicks (CLS)": "CLS.JO",
    "Capitec (CPI)": "CPI.JO",
    "Discovery (DSY)": "DSY.JO",
    "Exxaro (EXX)": "EXX.JO",
    "FirstRand (FSR)": "FSR.JO",
    "Gold Fields (GFI)": "GFI.JO",
    "Glencore (GLN)": "GLN.JO",
    "Growthpoint (GRT)": "GRT.JO",
    "Harmony Gold (HAR)": "HAR.JO",
    "Implats (IMP)": "IMP.JO",
    "Investec Ltd (INL)": "INL.JO",
    "Investec Plc (INP)": "INP.JO",
    "Italtile (ITU)": "ITU.JO",
    "Mediclinic (MEI)": "MEI.JO",
    "Mondi (MNP)": "MNP.JO",
    "Mr Price (MRP)": "MRP.JO",
    "MTN Group (MTN)": "MTN.JO",
    "Murray & Roberts (MUR)": "MUR.JO",
    "Nedbank (NED)": "NED.JO",
    "Northam Platinum (NPH)": "NPH.JO",
    "Naspers (NPN)": "NPN.JO",
    "Redefine (NRP)": "NRP.JO",
    "Old Mutual (OMU)": "OMU.JO",
    "Prosus (PRX)": "PRX.JO",
    "Remgro (REM)": "REM.JO",
    "Reinet (RNI)": "RNI.JO",
    "Standard Bank (SBK)": "SBK.JO",
    "Shoprite (SHP)": "SHP.JO",
    "Sanlam (SLM)": "SLM.JO",
    "Sasol (SOL)": "SOL.JO",
    "Shoprite (SPP)": "SPP.JO",
    "Sibanye Stillwater (SSW)": "SSW.JO",
    "Truworths (TGA)": "TGA.JO",
    "The Foschini Group (TRU)": "TRU.JO",
    "Vodacom (VOD)": "VOD.JO",
    "Woolworths (WHL)": "WHL.JO",
}

selected = st.selectbox("Select stock", list(stocks.keys()))
ticker = stocks[selected]


st.subheader(f"{ticker} — RSI Strategy")





# data fetching
data = yfinance.Ticker(ticker)
historical_data = data.history(start=start_date, end=end_date)
close_price = historical_data["Close"]


if historical_data.empty:
    st.error("No data found for this ticker. Try another stock.")
    st.stop()


# indicator calculation
rsi = ta.rsi(close_price)


# moving average
ma50 = historical_data["Close"].rolling(window=50).mean()

# support and resistance
support = historical_data["Low"].rolling(window=20).min().iloc[-1]
resistance = historical_data["High"].rolling(window=20).max().iloc[-1]

# current price
current_price = historical_data["Close"].iloc[-1]
current_rsi = rsi.iloc[-1]

# trend direction
trend = "Bullish" if current_price > ma50.iloc[-1] else "Bearish"

# signal generation
historical_data["Signal"] = "Hold"
historical_data.loc[(rsi.shift(1) > 30) & (rsi < 30), "Signal"] = "Buy"
historical_data.loc[(rsi.shift(1) < 70) & (rsi > 70), "Signal"] = "Sell"



col1, col2, col3 = st.columns(3)
col1.metric("Current Price", f"R{current_price/100:.2f}")
col2.metric("RSI (14)", f"{current_rsi:.1f}")
col3.metric("Trend", trend)



# candlestick chart
st.subheader(f"{ticker} Price Chart")

fig = go.Figure(data=[go.Candlestick(
    x=historical_data.index,
    open=historical_data["Open"],
    high=historical_data["High"],
    low=historical_data["Low"],
    close=historical_data["Close"]
)])

fig.update_layout(
    xaxis_rangeslider_visible=False,
    plot_bgcolor="white",
    height=500
)

st.plotly_chart(fig, use_container_width=True)



# trade idea
st.subheader("Trade Idea")

# calculate entry, stop loss, target
entry = current_price
stop_loss = support * 0.98  # 2% below support
target = resistance * 0.98  # just below resistance
risk = entry - stop_loss
reward = target - entry
rr_ratio = reward / risk if risk > 0 else 0

# generate recommendation
if current_rsi < 30 and trend == "Bullish":
    recommendation = "Strong Buy"
    reasoning = f"RSI is oversold at {current_rsi:.1f} with a bullish trend. High probability bounce."
elif current_rsi < 30:
    recommendation = "Buy"
    reasoning = f"RSI is oversold at {current_rsi:.1f}. Watch for trend confirmation."
elif current_rsi > 70 and trend == "Bearish":
    recommendation = "Strong Sell"
    reasoning = f"RSI is overbought at {current_rsi:.1f} with a bearish trend. High probability reversal."
elif current_rsi > 70:
    recommendation = "Sell"
    reasoning = f"RSI is overbought at {current_rsi:.1f}. Watch for trend confirmation."
else:
    recommendation = "Hold"
    reasoning = f"RSI is neutral at {current_rsi:.1f}. No clear signal. Wait for a better entry."

# display
st.markdown(f"### Recommendation: {recommendation}")
st.write(reasoning)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Entry", f"R{entry/100:.2f}")
col2.metric("Stop Loss", f"R{stop_loss/100:.2f}")
col3.metric("Target", f"R{target/100:.2f}")
col4.metric("Risk/Reward", f"{rr_ratio:.1f}x")
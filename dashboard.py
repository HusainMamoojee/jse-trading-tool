import streamlit as st
import yfinance
import pandas as pd
import pandas_ta as ta



st.title("JSE Trading Dashboard")

ticker = st.selectbox("Select stock", ["SOL.JO", "NPN.JO", "BHG.JO", "SBK.JO", "AGL.JO"])

st.subheader(f"{ticker} — RSI Strategy")





# data fetching
data = yfinance.Ticker(ticker)
historical_data = data.history(start="2024-01-01", end="2024-12-31")
close_price = historical_data["Close"]


if historical_data.empty:
    st.error("No data found for this ticker. Try another stock.")
    st.stop()


# indicator calculation
rsi = ta.rsi(close_price)

# signal generation
historical_data["Signal"] = "Hold"
historical_data.loc[(rsi.shift(1) > 30) & (rsi < 30), "Signal"] = "Buy"
historical_data.loc[(rsi.shift(1) < 70) & (rsi > 70), "Signal"] = "Sell"

# backtester
position = False
buy_price = 0
profit = 0
trades = []

for date, row in historical_data.iterrows():
    if row["Signal"] == "Buy" and position == False:
        buy_date = date
        buy_price = row["Close"]
        position = True
    if row["Signal"] == "Sell" and position == True:
        position = False
        profit += row["Close"] - buy_price
        trades.append({
            "Buy Date": buy_date,
            "Sell Date": date,
            "Buy Price": buy_price,
            "Sell Price": row["Close"],
            "Profit": row["Close"] - buy_price
        })

if position == True:
    last_price = historical_data["Close"].iloc[-1]
    profit += last_price - buy_price
    position = False

realised = sum(t['Profit'] for t in trades)
unrealised = historical_data["Close"].iloc[-1] - buy_price
trades_df = pd.DataFrame(trades)

# dashboard
col1, col2, col3 = st.columns(3)
col1.metric("Realised Profit", f"R{realised/100:.2f}")
col2.metric("Unrealised P&L", f"R{unrealised/100:.2f}")
col3.metric("Total Profit", f"R{profit/100:.2f}")

st.subheader("Trade History")
st.dataframe(trades_df)

st.subheader(f"{ticker} Price 2024")
st.line_chart(close_price)
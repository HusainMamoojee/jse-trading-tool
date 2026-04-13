import yfinance
import pandas as pd
import pandas_ta as ta
from datetime import datetime, timedelta

end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# data fetching
data = yfinance.Ticker("SOL.JO")
historical_data = data.history(start=start_date, end=end_date)
close_price = historical_data["Close"]

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

trades_df = pd.DataFrame(trades)
print(trades_df)
print(f"\nOpen Position: Bought on {buy_date} at {buy_price}")
print(f"Last Price: {historical_data['Close'].iloc[-1]}")
print(f"Unrealised P&L: {historical_data['Close'].iloc[-1] - buy_price:.2f} cents")
print(f"\nRealised Profit: {sum(t['Profit'] for t in trades):.2f} cents")
print(f"Total Profit (incl. open): {profit:.2f} cents = R{profit/100:.2f}")
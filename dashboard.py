import streamlit as st
import yfinance
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

end_date = datetime.today()
start_date = end_date - timedelta(days=365)

st.set_page_config(page_title="JSE Trading Dashboard", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif;
    }

    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    h1 {
        font-family: 'IBM Plex Mono', monospace !important;
        color: #58a6ff !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.15em !important;
        text-transform: uppercase !important;
        border-bottom: 1px solid #21262d !important;
        padding-bottom: 0.75rem !important;
        margin-bottom: 1.5rem !important;
    }

    h2, h3 {
        font-family: 'IBM Plex Mono', monospace !important;
        color: #58a6ff !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.12em !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Metric cards */
    [data-testid="metric-container"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 6px !important;
        padding: 1rem 1.25rem !important;
    }

    [data-testid="metric-container"] label {
        font-family: 'IBM Plex Mono', monospace !important;
        color: #8b949e !important;
        font-size: 0.65rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
    }

    [data-testid="stMetricValue"] {
        font-family: 'IBM Plex Mono', monospace !important;
        color: #e6edf3 !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricDelta"] {
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 0.8rem !important;
    }

    /* Selectbox */
    .stSelectbox label {
        font-family: 'IBM Plex Mono', monospace !important;
        color: #8b949e !important;
        font-size: 0.7rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
    }

    .stSelectbox > div > div {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        color: #e6edf3 !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
        border-radius: 6px !important;
    }

    /* Divider */
    hr {
        border-color: #21262d !important;
    }

    /* Recommendation box */
    .rec-box {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 1rem 1.25rem;
        margin: 0.5rem 0 1rem 0;
    }

    .rec-strong-buy  { border-left: 4px solid #3fb950; }
    .rec-buy         { border-left: 4px solid #56d364; }
    .rec-hold        { border-left: 4px solid #d29922; }
    .rec-sell        { border-left: 4px solid #f85149; }
    .rec-strong-sell { border-left: 4px solid #da3633; }

    .rec-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #8b949e;
        margin-bottom: 0.25rem;
    }

    .rec-value {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .rec-strong-buy  .rec-value { color: #3fb950; }
    .rec-buy         .rec-value { color: #56d364; }
    .rec-hold        .rec-value { color: #d29922; }
    .rec-sell        .rec-value { color: #f85149; }
    .rec-strong-sell .rec-value { color: #da3633; }

    .rec-reasoning {
        font-size: 0.85rem;
        color: #8b949e;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

st.title("⬛ JSE Trading Dashboard")

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
    "Pick n Pay (SPP)": "SPP.JO",
    "Sibanye Stillwater (SSW)": "SSW.JO",
    "Truworths (TGA)": "TGA.JO",
    "The Foschini Group (TRU)": "TRU.JO",
    "Vodacom (VOD)": "VOD.JO",
    "Woolworths (WHL)": "WHL.JO",
}

selected = st.selectbox("Select stock", list(stocks.keys()))
ticker = stocks[selected]

# data fetching
data = yfinance.Ticker(ticker)
historical_data = data.history(start=start_date, end=end_date, auto_adjust=True)
close_price = historical_data["Close"]

if historical_data.empty:
    st.error("No data found for this ticker. Try another stock.")
    st.stop()

# indicator calculation
rsi = ta.rsi(close_price)

if rsi is None or rsi.dropna().empty:
    st.error("Not enough data to calculate indicators for this ticker.")
    st.stop()

macd_df = ta.macd(close_price)
if macd_df is None:
    st.error("Not enough data to calculate MACD for this ticker.")
    st.stop()

macd_line = macd_df["MACD_12_26_9"]
signal_line = macd_df["MACDs_12_26_9"]
histogram = macd_df["MACDh_12_26_9"]

ma50 = historical_data["Close"].rolling(window=50).mean()
support = historical_data["Low"].rolling(window=20).min().iloc[-1]
resistance = historical_data["High"].rolling(window=20).max().iloc[-1]

current_price = historical_data["Close"].dropna().iloc[-1]
current_rsi = rsi.iloc[-1]
current_macd = macd_line.iloc[-1]
current_signal_val = signal_line.iloc[-1]

if pd.isna(current_price) or pd.isna(current_rsi):
    st.error("Price data unavailable for this ticker. Try another stock.")
    st.stop()

trend = "Bullish" if current_price > ma50.iloc[-1] else "Bearish"
macd_is_bullish = current_macd > current_signal_val
macd_is_bearish = current_macd < current_signal_val

# signal generation
macd_bullish_cross = (macd_line.shift(1) < signal_line.shift(1)) & (macd_line > signal_line)
macd_bearish_cross = (macd_line.shift(1) > signal_line.shift(1)) & (macd_line < signal_line)
rsi_oversold = (rsi.shift(1) > 30) & (rsi < 30)
rsi_overbought = (rsi.shift(1) < 70) & (rsi > 70)

historical_data["Signal"] = "Hold"
historical_data.loc[rsi_oversold | macd_bullish_cross, "Signal"] = "Buy"
historical_data.loc[rsi_oversold & macd_bullish_cross, "Signal"] = "Strong Buy"
historical_data.loc[rsi_overbought | macd_bearish_cross, "Signal"] = "Sell"
historical_data.loc[rsi_overbought & macd_bearish_cross, "Signal"] = "Strong Sell"

# metrics row
st.subheader(f"{ticker} — Live Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Current Price", f"R{current_price / 100:.2f}")
col2.metric("RSI (14)", f"{current_rsi:.1f}",
            delta="Oversold" if current_rsi < 30 else ("Overbought" if current_rsi > 70 else "Neutral"))
col3.metric("Trend (MA50)", trend)
col4.metric("MACD Bias", "Bullish" if macd_is_bullish else "Bearish")

# chart
st.subheader(f"{ticker} — Price Chart")

fig = make_subplots(
    rows=4, cols=1,
    shared_xaxes=True,
    row_heights=[0.5, 0.17, 0.17, 0.16],
    vertical_spacing=0.03,
    subplot_titles=("", "Volume", "RSI (14)", "MACD")
)

fig.add_trace(go.Candlestick(
    x=historical_data.index,
    open=historical_data["Open"],
    high=historical_data["High"],
    low=historical_data["Low"],
    close=historical_data["Close"],
    name="Price",
    increasing_line_color="#3fb950",
    decreasing_line_color="#f85149"
), row=1, col=1)

fig.add_trace(go.Scatter(
    x=historical_data.index,
    y=ma50,
    name="MA50",
    line=dict(color="#58a6ff", width=1, dash="dot")
), row=1, col=1)

fig.add_trace(go.Bar(
    x=historical_data.index,
    y=historical_data["Volume"],
    name="Volume",
    marker_color="rgba(88, 166, 255, 0.3)"
), row=2, col=1)

fig.add_trace(go.Scatter(
    x=historical_data.index,
    y=rsi,
    name="RSI",
    line=dict(color="#d29922", width=1.5)
), row=3, col=1)

fig.add_hline(y=70, line_dash="dash", line_color="#f85149", line_width=1, row=3, col=1)
fig.add_hline(y=30, line_dash="dash", line_color="#3fb950", line_width=1, row=3, col=1)

fig.add_trace(go.Scatter(
    x=historical_data.index,
    y=macd_line,
    name="MACD",
    line=dict(color="#58a6ff", width=1.5)
), row=4, col=1)

fig.add_trace(go.Scatter(
    x=historical_data.index,
    y=signal_line,
    name="Signal",
    line=dict(color="#d29922", width=1.5)
), row=4, col=1)

fig.add_trace(go.Bar(
    x=historical_data.index,
    y=histogram,
    name="Histogram",
    marker_color=["#3fb950" if v >= 0 else "#f85149" for v in histogram]
), row=4, col=1)

fig.update_layout(
    xaxis_rangeslider_visible=False,
    height=750,
    plot_bgcolor="#0d1117",
    paper_bgcolor="#0d1117",
    font=dict(color="#8b949e", family="IBM Plex Mono"),
    showlegend=False,
    margin=dict(l=0, r=0, t=20, b=0),
)

for i in range(1, 5):
    fig.update_xaxes(gridcolor="#21262d", showgrid=True, row=i, col=1)
    fig.update_yaxes(gridcolor="#21262d", showgrid=True, row=i, col=1)

st.plotly_chart(fig, use_container_width=True)

# trade idea
st.subheader("Trade Idea")

entry = current_price
stop_loss = support * 0.98
target = resistance * 0.98
risk = entry - stop_loss
reward = target - entry
rr_ratio = reward / risk if risk > 0 else 0

if current_rsi < 30 and macd_is_bullish:
    recommendation = "Strong Buy"
    reasoning = f"RSI oversold at {current_rsi:.1f} AND MACD bullish. Strong confluence — high probability bounce."
    css_class = "rec-strong-buy"
elif current_rsi < 30:
    recommendation = "Buy"
    reasoning = f"RSI oversold at {current_rsi:.1f}. MACD not yet confirming — wait for crossover before entering."
    css_class = "rec-buy"
elif current_rsi > 70 and macd_is_bearish:
    recommendation = "Strong Sell"
    reasoning = f"RSI overbought at {current_rsi:.1f} AND MACD bearish. Strong confluence — high probability reversal."
    css_class = "rec-strong-sell"
elif current_rsi > 70:
    recommendation = "Sell"
    reasoning = f"RSI overbought at {current_rsi:.1f}. MACD not yet confirming — watch for bearish crossover."
    css_class = "rec-sell"
else:
    recommendation = "Hold"
    reasoning = f"RSI neutral at {current_rsi:.1f}. No clear confluence signal. Wait for a better entry point."
    css_class = "rec-hold"

st.markdown(f"""
<div class="rec-box {css_class}">
    <div class="rec-label">Recommendation</div>
    <div class="rec-value">{recommendation}</div>
    <div class="rec-reasoning">{reasoning}</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Entry", f"R{entry / 100:.2f}")
col2.metric("Stop Loss", f"R{stop_loss / 100:.2f}")
col3.metric("Target", f"R{target / 100:.2f}")
col4.metric("Risk/Reward", f"{rr_ratio:.1f}x")
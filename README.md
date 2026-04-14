# JSE Trading Dashboard

A data-driven trading analysis tool built for the JSE Investment Challenge. Uses Python to fetch live Johannesburg Stock Exchange data, calculate technical indicators, generate buy/sell signals, and display everything in an interactive web dashboard.

---

## Features

- **Live JSE Data** — fetches real-time and historical price data for JSE Top 40 stocks via Yahoo Finance
- **RSI + MACD Signal Engine** — calculates RSI and MACD indicators and detects crossover signals with confluence logic
- **Interactive Charts** — candlestick chart with volume, RSI, and MACD subplots powered by Plotly
- **Trade Ideas** — automatically generates entry price, stop loss, target, and risk/reward ratio for each stock
- **Multi-Stock Scanner** — scans all JSE Top 40 stocks simultaneously and ranks them by signal strength
- **Bloomberg-style Dark Theme** — professional terminal aesthetic built with custom CSS

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| yfinance | JSE stock data fetching |
| pandas | Data manipulation |
| pandas-ta | Technical indicators (RSI, MACD) |
| Streamlit | Web dashboard framework |
| Plotly | Interactive charting |

---

## Screenshots

### Analysis Tab
<img width="1115" height="784" alt="Screenshot 2026-04-14 at 02 52 45" src="https://github.com/user-attachments/assets/74d43aeb-6b3e-4905-8b64-cd5c3939f494" />


### Scanner Tab
<img width="1023" height="225" alt="Screenshot 2026-04-14 at 02 53 19" src="https://github.com/user-attachments/assets/3da85a8b-daf6-460f-bcc5-7f4bf3434b63" />
<img width="1071" height="503" alt="Screenshot 2026-04-14 at 02 53 03" src="https://github.com/user-attachments/assets/a960e2c9-4d19-480f-acfa-c81a07865aef" />


---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/jse-trading-system.git
cd jse-trading-system
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the dashboard

```bash
streamlit run dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`

---

## How It Works

### Signal Logic

The system generates signals based on RSI and MACD confluence:

| Condition | Signal |
|---|---|
| RSI crosses below 30 AND MACD bullish crossover | Strong Buy |
| RSI crosses below 30 OR MACD bullish crossover | Buy |
| RSI neutral, no crossover | Hold |
| RSI crosses above 70 OR MACD bearish crossover | Sell |
| RSI crosses above 70 AND MACD bearish crossover | Strong Sell |

### Trade Idea Calculation

- **Entry** — current closing price
- **Stop Loss** — 2% below the 20-day support level
- **Target** — just below the 20-day resistance level
- **Risk/Reward** — calculated automatically as `reward / risk`

---

## Project Structure

```
jse-trading-system/
├── main.py          # Core signal engine and backtester
├── dashboard.py     # Streamlit web dashboard
├── requirements.txt # Python dependencies
└── README.md        # Project documentation
```

---

## Built By

Husain — Software Engineering Student at Eduvos  
Built as a project to help me and my team analyse and understand the market so we can take better trades in the jse trading challenge

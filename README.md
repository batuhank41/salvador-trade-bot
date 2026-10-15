# ⚡ AlgoTrader-Engine (Automated Crypto & Stock Trading Bot)

An algorithmic, event-driven quantitative trading bot designed for crypto exchanges and equity markets. It combines technical indicators (RSI, MACD, Volume Profile), Price Action patterns (Liquidity Sweeps, Market Structure Shifts), and automated risk management (trailing stops, bracket orders, strict risk/reward ratios).

---

## 📌 Features

- **Multi-Strategy Architecture:**
  - **Price Action Engine:** Detects Liquidity Sweeps, pinbars, fair value gaps (FVG), and Market Structure Shifts (MSS).
  - **Momentum & Oscillators:** Dynamic RSI breakout, MACD divergence, and Stochastic oversold/overbought crosses.
  - **Volume & Derivatives Analysis:** Analyzes Open Interest (OI) spikes, Funding Rates (short squeeze detection), and Volume Profile (POC/VAH/VAL).
- **Automated Execution & Smart Order Routing:**
  - Automated Stop-Loss (SL) and Take-Profit (TP) bracket orders.
  - Native support for Limit, Market, and Trigger-based conditional stop orders.
  - Trailing Stop-Loss to secure unrealized profits during strong momentum runs.
- **Risk Management Engine:**
  - Fixed-fractional position sizing (default: max 1-2% account equity risk per trade).
  - Real-time Risk/Reward (R:R) validator before firing execution orders.
  - Daily Drawdown circuit breaker (halts trading if daily loss limit is hit).
- **Notifications & Logging:**
  - Real-time alerts via Telegram Bot, Discord Webhooks, and structured JSON logs.
  - Backtesting and paper trading simulation modes with detailed metrics.



## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- Active API keys from your supported exchange (e.g., Binance, Bybit, OKX, or local broker APIs).

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/algotrader-engine.git](https://github.com/yourusername/algotrader-engine.git)
   cd algotrader-engine
Create and activate a virtual environment:Bashpython3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:Bashpip install -r requirements.txt
Configure environment variables:Bashcp .env.example .env
Open .env and fill in your credentials:Kod snippet'iEXCHANGE_ID=binance
API_KEY=your_api_key_here
API_SECRET=your_api_secret_here
PAPER_TRADING=true
MAX_RISK_PER_TRADE=0.01
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
⚙️ ConfigurationStrategy parameters can be tuned in config/strategy_config.yaml:YAMLtrading:
  symbols:
    - "BTC/USDT"
    - "ETH/USDT"
    - "SOL/USDT"
  timeframe: "15m"
  leverage: 1

indicators:
  rsi:
    period: 14
    oversold: 30
    overbought: 70
  macd:
    fast_period: 12
    slow_period: 26
    signal_period: 9

risk:
  risk_reward_ratio: 2.0     # Minimum 1:2 R:R
  stop_loss_pct: 0.015       # 1.5% fixed SL
  take_profit_pct: 0.035     # 3.5% target TP
  max_open_positions: 3
  daily_max_drawdown_pct: 0.05
🖥️ UsageRun Paper Trading (Dry Run)Test strategies in a live sandbox environment without risking actual capital:Bashpython main.py --mode paper --symbol BTC/USDT --timeframe 15m
Run Live TradingExecute live orders with dynamic bracket protection:Bashpython main.py --mode live --config config/strategy_config.yaml
Run BacktesterEvaluate historical performance on stored OHLCV data:Bashpython backtest.py --symbol ETH/USDT --start 2026-01-01 --end 2026-08-01
🛡️ Risk & Order Execution LogicThe bot handles orders using a dual-state bracket flow to prevent liquidation or slippage:Signal Generation: When technical indicators align with a confirmed structural shift, the strategy triggers a buy signal.Order Placement: Executes a limit entry inside the specified fair value spread.Contingent Stop-Loss: An automated stop-trigger (STOP_LOSS_LIMIT or STOP_MARKET) is placed concurrently on the exchange order book.Take-Profit Target: A limit take-profit order is submitted; if hit, the trailing engine cancels outstanding stop triggers (OCO / One-Cancels-the-Other).📊 Backtest Metrics (Sample)MetricValueTotal Trades214Win Rate61.2%Profit Factor1.84Max Drawdown-6.4%Sharpe Ratio1.92⚠️ DisclaimerThis software is for educational, research, and algorithmic testing purposes only. Cryptocurrency and equity trading involve substantial financial risk. Past performance does not guarantee future results. Never trade with capital you cannot afford to lose.📄 LicenseDistributed under the MIT License. See LICENSE for more information.

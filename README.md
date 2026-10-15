# 🦅 Salvador Quant & AI Trade Bot
### *Autonomous Algorithmic Trading & Intelligence Platform Powered by a Custom-Trained Financial AI*

[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Model](https://img.shields.io/badge/Custom_AI-Salvador_Quant_8B_(LoRA%20Fine--Tuned)-orange?logo=openai&logoColor=white)](#-1-custom-trained-ai-architecture-custom-quant-llm)
[![Engine](https://img.shields.io/badge/Local_Inference-Ollama_%26_GGUF-purple?logo=ollama&logoColor=white)](#-local-inference-and-gguf-quantization)
[![Markets](https://img.shields.io/badge/Markets-BIST_%7C_NASDAQ_%7C_Crypto-brightgreen)](#-2-supported-markets-and-data-pipeline)
[![Brokers](https://img.shields.io/badge/Execution-Alpaca_Markets_%7C_Binance-red)](#-6-autonomous-execution-and-risk-engine-order_enginepy)
[![Interface](https://img.shields.io/badge/Control_Center-Telegram_Bot_V2.0-blue?logo=telegram&logoColor=white)](#-5-telegram-command-center-livepy)

---

## 📌 Project Overview

**Salvador Trade Bot** is a next-generation **Quantitative & Algorithmic Trading Platform** designed from the ground up to filter out market noise and produce **actionable, mathematical, and institutionally grounded decisions** instead of vague, speculative commentary.

Unlike standard trading bots that rely on generic external APIs, Salvador features its own **custom-trained, fine-tuned local Large Language Model (Salvador Quant LLM)**, specialized specifically in financial terminology, technical indicators, chart patterns, and quantitative risk management rules.

The platform simultaneously scans **Borsa Istanbul (BIST)**, **US Equities (NASDAQ & NYSE)**, and the **Crypto Market (Binance)**, analyzes **Coinglass** futures derivatives data, and synthesizes **Wall Street and BIST brokerage price targets** with technical indicators—all orchestrated fully autonomously via Telegram.

---

## 🧠 1. Custom-Trained AI Architecture (Custom Quant LLM)

At the core of Salvador lies a **custom fine-tuned artificial intelligence engine**, engineered to enforce strict financial discipline and decisive, jargon-free execution that off-the-shelf models fail to deliver.

```
                    ┌───────────────────────────────────────────────┐
                    │    Raw Financial Dataset & Strategy Pool      │
                    │ (master_dataset.json, hisse_analiz_rehberi)   │
                    └───────────────────────┬───────────────────────┘
                                            │
                                            ▼
                    ┌───────────────────────────────────────────────┐
                    │   Unsloth 4-Bit LoRA Fine-Tuning Pipeline     │
                    │   (q_proj, k_proj, v_proj, o_proj, MLP)       │
                    └───────────────────────┬───────────────────────┘
                                            │
                                            ▼
                    ┌───────────────────────────────────────────────┐
                    │       FP16 Model Export & GGUF Conversion     │
                    │              (convert_to_gguf.py)             │
                    └───────────────────────┬───────────────────────┘
                                            │
                                            ▼
                    ┌───────────────────────────────────────────────┐
                    │  Q4_K_M Quantization & Local Ollama Engine    │
                    │      (Modelfile -> salvador-quant / Qwen)     │
                    └───────────────────────┬───────────────────────┘
                                            │
                   ┌────────────────────────┴────────────────────────┐
                   ▼                                                 ▼
        ┌──────────────────────┐                          ┌──────────────────────┐
        │ Natural Language/AI  │                          │ Time Series & ML     │
        │ (Autonomous Decision)│                          │ (LSTM Hybrid Model)  │
        └──────────────────────┘                          └──────────────────────┘
```

### 🔬 Model Fine-Tuning Specifications
* **Base Models:** `unsloth/llama-3-8b-Instruct-bnb-4bit` and `Qwen2.5-7B` architectures.
* **Training Framework:** `Unsloth FastLanguageModel` + `HuggingFace TRL (SFTTrainer)`, delivering a 5x faster pipeline with an 80% reduction in VRAM overhead.
* **LoRA Hyperparameters:**
  * `r = 16`, `lora_alpha = 16`, `lora_dropout = 0`
  * **Target Modules:** `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`
  * **Optimizer:** `adamw_8bit` (with Gradient Checkpointing and Bfloat16/FP16 native support).
* **Proprietary Financial Dataset:**
  * `master_dataset.json`, `salvador_trader_dataset.json`, `salvador_trader_dataset_v2.json`
  * Thousands of curated real-world market scenarios, RSI divergences, support/resistance breaks, whale volume movements, balance sheet evaluations, and Turkish/US equities question-answering pairs.
* **Embedded Financial Policy:** The model strictly enforces guidelines from `hisse_analiz_rehberi.txt`. Rather than providing ambiguous statements such as *"It might go up"*, it issues **firm decisions (🟢 BUY / 🟡 HOLD / ⚠️ DANGER)**, a **projected price target range**, and an unambiguous **Salvador Confidence Score (0 to 100)**.

### ⚡ Local Inference and GGUF Quantization
* Fine-tuned LoRA weights were merged with the base model, exported into **FP16 GGUF** format (`convert_to_gguf.py`), and quantized to **Q4_K_M**.
* The model is served directly through a local **Ollama** runtime using a custom `Modelfile`.
* **Key Advantages:**
  * Zero external API usage costs.
  * Absolute data privacy (all trading logic and portfolio balances stay strictly local).
  * Sub-second latency for real-time market decision making.

### 📈 Hybrid Deep Learning: LSTM Time-Series Engine
Alongside LLM-driven natural language analysis, the system incorporates **`lstm_trade_bot.h5`**, a recurrent neural network that processes historical OHLCV price series to perform regression-based price forecasting and directional trend verification.

---

## 🌐 2. Supported Markets and Data Pipeline

Salvador is not confined to a single asset class; it unifies three major financial ecosystems into one operational terminal:

| Market | Asset Universe | Primary Data Source | Core Capabilities |
|---|---|---|---|
| 🇹🇷 **Borsa Istanbul (BIST)** | 500+ BIST Equities (`.IS`) | Yahoo Finance, Is Yatirim, KAP, Google News RSS | Fresh IPO tracking (down to 17-19 trading days), circuit breaker monitoring, Turkish brokerage consensus. |
| 🇺🇸 **Wall Street (NASDAQ & NYSE)** | 3,300+ US Stocks | Alpaca Market Data, Yahoo Pre/Post-Market, SEC | Wall Street institutional price targets, pre-market/after-hours quotes, direct order execution. |
| 🪙 **Cryptocurrency (Crypto)** | 900+ USDT Pairs | CCXT (Binance Spot & Futures), Coinglass API | Volume breakout (Pump/Dump) alarms, whale flow detection, Long/Short ratios, Open Interest (OI), Liquidation maps. |

---

## 🏛️ 3. Institutional Analyst & Consensus Intelligence

Salvador synthesizes technical setups with **Institutional Smart Money positioning**:

* **12-Month Target Prices:** Aggregates Wall Street and BIST consensus targets (Low, Mean, High) and computes upside/downside potential (%).
* **Consensus Breakdown:** Tracks exact recommendation distributions (`95% BUY │ 2 HOLD │ 1 SELL`).
* **Featured Institutional Research:**
  * **NASDAQ:** *Goldman Sachs, Morgan Stanley, JP Morgan, Raymond James, Jefferies, BMO Capital, Cantor Fitzgerald*, etc.
  * **BIST:** *Is Yatirim, Garanti BBVA, Vakif Yatirim, Ak Yatirim, Yapi Kredi, Deniz Yatirim, Unlu & Co, HSBC*, etc.
* **Autotrade Scoring Bonus:** When a stock exhibits **>= 20% upside potential** backed by **>= 70% BUY consensus**, the scanner algorithm automatically awards a **+10 Point Bonus**.

---

## 📊 4. Multi-Timeframe Performance Engine

Instead of relying solely on immediate price action, Salvador analyzes multi-horizon momentum:
* **1-Day (1D)**, **1-Week (1W)**, **1-Month (1M)**, **3-Month (3M)**, **1-Year (1Y)**, and **5-Year (5Y)** percentage returns.
* **IPO Lifecycle Intelligence:** For recently listed equities with fewer than 250 days of trading history (e.g., `METEN`, `KARCL`, `PLTUR`), the system prevents misleading 0.00% outputs by reporting **Return Since IPO** alongside the exact count of **Active Trading Days**.

---

## 📱 5. Telegram Command Center (`live.py`)

A reactive, keyboard-driven Telegram interface offering instant access to quantitative metrics and conversational AI analysis:

```text
📊 SALVADOR PRO ANALYSIS: NVDA (DAILY)
───────────────────────
💰 Current Price: $213.05
📈 Session Change: %+2.19
🕯️ Last Candle: GREEN CANDLE 📈 Bullish — RSI: 52.4
🎯 Salvador Decision: 🟢 BUY (85% Confidence)
───────────────────────
📊 Historical Performance:
   • 1D: %+2.19 | 1W: %-3.04 | 1M: %+8.42
   • 3M: %-0.73 | 1Y: %+19.86 | 5Y: %+868.76
───────────────────────
🏛️ INSTITUTIONAL ANALYST & EXPERT CONSENSUS:
   • 🎯 12M Mean Target: $304.73 (+%43.0 Upside Potential)
   • 📊 Consensus (62 Firms): 95% BUY │ 2 HOLD │ 1 SELL
   *Recent Firm Ratings:*
   • 🟢 Raymond James: Strong Buy
   • 🟢 Keybanc: Overweight
   • 🟢 Cantor Fitzgerald: Overweight
   • 🟢 BMO Capital: Outperform
───────────────────────
🤖 SALVADOR QUANT & AI SUMMARY:
Technical indicators hold firmly above the 200 EMA with expanding accumulation volume. 
Institutional target consensus provides a +43% margin of safety. 
Risk/Reward profile is optimal. Salvador Confidence Score: 92/100.
```

### 🎮 Primary Telegram Commands:
* `/analiz <SYMBOL>`: Live technical indicators, multi-timeframe performance, institutional targets, and custom AI verdict.
* `/derin <SYMBOL>`: Deep market matrix, whale footprint, and granular analyst research breakdown.
* `/radar`: Highest-ranking breakout and momentum signals across BIST & NASDAQ.
* `/alarm <SYMBOL> <PRICE>`: Low-latency alert triggered as soon as the target level is crossed.
* `/sohbet <QUERY>`: Free-form conversational market dialogue with the local Salvador Quant LLM.

---

## 🛡️ 6. Autonomous Execution and Risk Engine (`order_engine.py`)

To safeguard capital and ensure institutional discipline, all operations adhere to strict automated constraints:

* **Alpaca REST API Integration:** Direct market access for US equities executing in New York trading sessions.
* **Zero-Debt & No-Leverage Policy:** Even on accounts with margin capabilities, borrowing and leverage are strictly prohibited.
* **Hard Capital Allocation Cap:** Total portfolio expenditure is restricted by a hard ceiling of `$40,000.00`, preventing overexposure.
* **Market-Open Liquidation Watcher (`pozisyon_sifirlanma_gozcusu`):** Automatically clears overnight exposure when requested, restoring liquidity prior to executing clean strategic batches.

---

## ⚙️ 7. Modular Architecture & 5-Terminal Operations

The platform operates through a multithreaded, decoupled architecture distributed across 5 isolated terminal services:

```
[ Terminal 1: live.py ] ──────────► Telegram Bot, Local Qwen LLM Chat, Commands & Position Watcher
[ Terminal 2: bist_nasdaq_scanner ]► 3,300+ Stock Scanner, Institutional Scoring & $40k Autotrade
[ Terminal 3: run_scanner.py ] ───► 900+ Crypto Pair Breakout & Whale Volume Detector
[ Terminal 4: crypto_trader.py ] ─► 20-Second High-Frequency Crypto Volatility & Price Alarms
[ Terminal 5: batch_scanner.py ] ─► Coinglass Derivatives Depth, Open Interest & Long/Short Analytics
[ Background: Ollama Serve ] ────► Salvador Quant LLM Local Inference Engine (GGUF)
```

---

## 🚀 8. Installation and Setup

### 1. Clone the Repository and Initialize Virtual Environment
```bash
git clone https://github.com/yourusername/ai-trade-bot.git
cd ai-trade-bot

python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables (`.env`)
Create a `.env` file in the root directory and configure your credentials:
```env
TELEGRAM_TOKEN=your_telegram_bot_token
ADMIN_CHAT_ID=your_telegram_chat_id
ALPACA_API_KEY=your_alpaca_key
ALPACA_SECRET_KEY=your_alpaca_secret
ALPACA_BASE_URL=https://paper-api.alpaca.markets
BINANCE_API_KEY=your_binance_key
BINANCE_SECRET=your_binance_secret
```

### 4. Build the Local AI Model (Ollama)
```bash
# Ensure Ollama is running in the background:
ollama create salvador-quant -f Modelfile
```

### 5. Launch the Platform
Start each subsystem in its designated terminal:
```bash
# Terminal 1: Primary Telegram Bot & Command Center
python live.py

# Terminal 2: BIST & NASDAQ Multi-Layer Scanner
python bist_nasdaq_scanner.py --loop

# Terminal 3: Crypto Volume Breakout Scanner
python run_scanner.py

# Terminal 4: High-Frequency Crypto Alert Service
python crypto_trader.py

# Terminal 5: Coinglass Derivatives Depth Scanner
python batch_scanner.py --loop
```

---

## 📁 9. Directory Structure

```
ai-trade-bot/
├── train_trader.py             # Unsloth LoRA Fine-Tuning training script
├── convert_to_gguf.py          # Script for exporting trained models to GGUF format
├── Modelfile                   # Ollama local model service configuration
├── master_dataset.json         # Custom financial and quant training dataset
├── hisse_analiz_rehberi.txt    # LLM decision-making guidelines & analysis reference
├── live.py                     # Primary execution manager & Telegram bot entry point
├── telegram_bot.py             # Telegram UI, inline buttons, and command dispatchers
├── ai_service.py               # Local LLM inference and prompt synthesis engine
├── bist_nasdaq_scanner.py      # Multithreaded BIST & NASDAQ scanner and scoring engine
├── market_data.py              # Financial data ingestion (BIST, US, Analyst Consensus)
├── indicators.py               # Quantitative indicators (RSI, MACD, BB, ATR, Patterns)
├── order_engine.py             # Alpaca order execution & $40k risk governor
├── crypto_trader.py            # High-frequency crypto price & volatility tracker
├── run_scanner.py              # Binance crypto volume pump detector
├── batch_scanner.py            # Coinglass derivatives & order book depth engine
└── config.py                   # Global constants, symbol resolution, and logging
```

---

## ⚖️ Legal Disclaimer

*This software is designed solely for educational, research, and algorithmic strategy development purposes. None of the analyses, predictions, or metrics produced by this system constitute **Financial or Investment Advice**. Trading financial markets involves substantial risk of loss. Users bear full and sole responsibility for any profits or losses resulting from the use of automated strategies.*

---

**Developed by:** Salvador Quant & AI Trading Labs  
**License:** MIT License 🦅

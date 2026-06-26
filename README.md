# QuantSphere Alpha Station 

QuantSphere Alpha Station is an advanced quantitative finance and algorithmic trading backtesting engine built in Python. It provides institutional-grade risk analytics and strategy execution modeling using dynamic market data extraction via the Yahoo Finance API.

## Core Features & Architecture
- **Automated Data Pipeline**: Real-time multi-variate time-series extraction utilizing `yfinance`.
- **Institutional Risk Analytics Module**:
  - **Annualized Sharpe Ratio**: Measures risk-adjusted performance return.
  - **Historical Value-at-Risk (VaR)**: Quantifies the maximum potential portfolio loss at a 95% confidence interval using non-parametric historical simulation.
  - **Maximum Drawdown (MDD)**: Evaluates peak-to-trough capital preservation metrics.
- **Algorithmic Backtester**: Implements a systematic **Moving Average Crossover (20/50 Day)** trend-following strategy, simulating dynamic position shifting and evaluating cumulative returns against a passive Buy & Hold benchmark.

## Technical Requirements
To build and run this quantitative terminal locally, install the core data science dependencies:
```bash
pip install numpy pandas yfinance

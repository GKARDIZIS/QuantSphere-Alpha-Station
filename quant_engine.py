import numpy as np
import pandas as pd
import yfinance as yf

class QuantEngine:
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.data = None

    def fetch_data(self):
        """Fetch historical market data from Yahoo Finance API"""
        print(f"[*] Extracting high-frequency daily data for {self.ticker}...")
        df = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        if df.empty:
            raise ValueError("No data fetched. Check ticker symbol or internet connection.")
        
        # Keep only necessary columns and calculate daily returns
        self.data = df[['Close']].copy()
        # Flatten MultiIndex columns if necessary (common in newer yfinance versions)
        if isinstance(self.data.columns, pd.MultiIndex):
            self.data.columns = self.data.columns.get_level_values(0)
            
        self.data['Daily_Return'] = self.data['Close'].pct_change()
        return self.data

    def calculate_risk_analytics(self, confidence_level=0.95):
        """Calculate advanced institutional risk metrics"""
        if self.data is None or 'Daily_Return' not in self.data.columns:
            self.fetch_data()
            
        returns = self.data['Daily_Return'].dropna()
        
        # 1. Sharpe Ratio (assuming Risk-Free Rate = 0 for simplicity)
        trading_days = 252
        sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(trading_days)
        
        # 2. Value-at-Risk (VaR) using Historical Simulation method
        var_historical = np.percentile(returns, (1 - confidence_level) * 100)
        
        # 3. Maximum Drawdown (Peak to Trough decline)
        cumulative_returns = (1 + returns).cumprod()
        running_max = cumulative_returns.cummax()
        drawdown = (cumulative_returns - running_max) / running_max
        max_drawdown = drawdown.min()
        
        return {
            "Annualized_Sharpe_Ratio": round(float(sharpe_ratio), 4),
            "Historical_VaR_95%": round(float(var_historical), 4),
            "Maximum_Drawdown": round(float(max_drawdown), 4)
        }

    def run_backtest(self, short_window=20, long_window=50):
        """Execute a Moving Average Crossover Algorithmic Trading Strategy"""
        if self.data is None:
            self.fetch_data()
            
        df = self.data.copy()
        
        # Generate Technical Indicators
        df['Signal_Short_MA'] = df['Close'].rolling(window=short_window).mean()
        df['Signal_Long_MA'] = df['Close'].rolling(window=long_window).mean()
        
        # Generate Trading Signals (1 = Buy, 0 = Sell/Hold)
        df['Position'] = np.where(df['Signal_Short_MA'] > df['Signal_Long_MA'], 1.0, 0.0)
        df['Strategy_Signal'] = df['Position'].shift(1) # Trade executed on the next day's open
        
        # Calculate Strategy Returns vs Buy & Hold
        df['Strategy_Return'] = df['Daily_Return'] * df['Strategy_Signal']
        
        cum_buy_hold = (1 + df['Daily_Return'].dropna()).cumprod().iloc[-1] - 1
        cum_strategy = (1 + df['Strategy_Return'].dropna()).cumprod().iloc[-1] - 1
        
        return {
            "Benchmark_Buy_Hold_Return": round(float(cum_buy_hold), 4),
            "Algorithmic_Strategy_Return": round(float(cum_strategy), 4)
        }

if __name__ == "__main__":
    print("=== QUANTSPHERE ALPHA ENGINE INITIALIZED ===")
    
    # Analyze Apple Inc. (AAPL) as a case study
    engine = QuantEngine(ticker="AAPL", start_date="2023-01-01", end_date="2026-01-01")
    
    # 1. Risk Metrics
    risk_metrics = engine.calculate_risk_analytics()
    print("\n[+] Institutional Risk Portfolio Analytics:")
    for metric, value in risk_metrics.items():
        print(f"   >> {metric}: {value}")
        
    # 2. Backtesting Strategy
    backtest_results = engine.run_backtest()
    print("\n[+] Algorithmic Backtesting Performance Results:")
    for strategy, performance in backtest_results.items():
        print(f"   >> {strategy}: {performance:.2%}")

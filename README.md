# XAUUSD Trading System Backtester

A Python-based backtesting framework for testing a Previous Day High/Low (PDH/PDL) sweep trading strategy on historical XAU/USD (Gold) price data.

## Overview

This trading system implements a liquidity sweep strategy that:
- Identifies the previous day's high (PDH) and low (PDL)
- Determines daily market bias (bullish/bearish)
- Enters trades when price sweeps PDH/PDL and reverses
- Exits at the sweep point for profit

The backtester has achieved **~70% win rate** across multiple timeframes (1m, 5m, 15m, 30m, 1h, 4h).

## Strategy Logic

### Entry Conditions

**For Bullish Bias** (previous day closed higher than open):
1. Price must sweep below the Previous Day Low (PDL)
2. Price must then reverse and move back above the sweep point
3. Enter long position on the reversal

**For Bearish Bias** (previous day closed lower than open):
1. Price must sweep above the Previous Day High (PDH)
2. Price must then reverse and move back below the sweep point
3. Enter short position on the reversal

### Exit Conditions

- **Take Profit**: Price returns to the initial sweep point
- **Stop Loss**: End of trading day if target not reached
- **Break Even**: Price exactly reaches sweep point

## Project Structure

```
.
├── ExtractTrades.py       # Data parser and daily metrics calculator
├── TradeSimulation.py     # Core backtesting engine
├── main.ipynb            # Test runner and results aggregator
```

## Installation

### Prerequisites

- Python 3.11+
- Jupyter Notebook (for running `main.ipynb`)

### Required Dependencies

```bash
pip install kagglehub
```

### Setup

1. Clone the repository:
```bash
git clone https://github.com/ikeawesom/xauusd-backtest.git
cd xauusd-backtest
```

2. Download the dataset:
The notebook automatically downloads the XAUUSD historical data from Kaggle:
```python
import kagglehub
path = kagglehub.dataset_download("novandraanugrah/xauusd-gold-price-historical-data-2004-2024")
```

## Usage

### Running the Backtest

1. **Open the Jupyter notebook:**
```bash
jupyter notebook main.ipynb
```

2. **Run all cells** to execute the backtest across all timeframes

3. **View results** displayed in the output

### Using Individual Classes

#### ExtractTrades Class

Parses CSV data and calculates daily metrics:

```python
from ExtractTrades import ExtractTrades

# Load data
data = ExtractTrades("./data/XAU_15m_data.csv")

# Get daily bias
is_bullish = data.isBullishDailyBias("2024-01-15")

# Get previous day high/low
pdh = data.getPDH("2024-01-15")
pdl = data.getPDL("2024-01-15")

# Display all data
data.displayData()
```

#### TradeSimulation Class

Runs the backtest simulation:

```python
from TradeSimulation import TradeSimulation

# Initialize simulation
sim = TradeSimulation("./data/XAU_15m_data.csv")

# Enable detailed logging (optional)
sim.enableLog()

# Run the simulation
sim.start()

# View results
sim.displayResults(full=True)

# Get statistics
results = sim.calculateResults()
print(f"Win Rate: {results['winrate']}%")
print(f"Trades Taken: {results['trades_taken']}")
print(f"Wins: {results['wins']}")
```

## Backtest Results

Results from testing across multiple timeframes (2004-2024 data):

| Timeframe | Total Trades | Wins | Win Rate |
|-----------|-------------|------|----------|
| 1m        | 7,181       | 4,977| 69.31%   |
| 5m        | 5,619       | 3,981| 70.85%   |
| **15m**   | **4,547**   | **3,236**| **71.17%** |
| 30m       | 3,704       | 2,614| 70.57%   |
| 1h        | 2,761       | 1,911| 69.21%   |
| 4h        | 1,097       | 674  | 61.44%   |
| 1d        | 0           | 0    | N/A      |
| 1w        | 0           | 0    | N/A      |
| 1M        | 0           | 0    | N/A      |

**Best Performance:** 15-minute timeframe with 71.17% win rate

## Data Format

The CSV files should follow this structure:

```
Date;Open;High;Low;Close;Volume
2024-01-15 09:00:00;2045.50;2046.20;2044.80;2045.90;1250
```

Fields:
- **Date**: Timestamp (YYYY-MM-DD HH:MM:SS)
- **Open**: Opening price
- **High**: Highest price in period
- **Low**: Lowest price in period
- **Close**: Closing price
- **Volume**: Trading volume

## Key Features

- ✅ Multiple timeframe support (1m to 1 month)
- ✅ Automatic daily bias detection
- ✅ PDH/PDL calculation for each trading day
- ✅ Detailed trade logging (optional)
- ✅ Comprehensive statistics tracking
- ✅ Multi-trade per day support
- ✅ Break-even trade detection

## Classes Overview

### ExtractTrades

Responsible for:
- Loading and parsing CSV data
- Grouping price data by date
- Calculating daily bias (bullish/bearish)
- Computing Previous Day High (PDH) and Previous Day Low (PDL)

**Key Methods:**
- `isBullishDailyBias(date)`: Returns True if bullish, False if bearish
- `getPDH(date)`: Returns the previous day's highest price
- `getPDL(date)`: Returns the previous day's lowest price
- `getDf()`: Returns the complete dataframe

### TradeSimulation

Responsible for:
- Running the backtest simulation
- Managing trade entries and exits
- Tracking win/loss statistics
- Generating detailed trade logs

**Key Methods:**
- `start()`: Executes the backtest
- `calculateResults()`: Returns statistics dictionary
- `displayResults(full=False)`: Prints results to console
- `enableLog()` / `disableLog()`: Toggle detailed logging

## Limitations & Considerations

1. **No spread/commission**: Results don't account for trading costs
2. **Perfect execution**: Assumes all orders fill at exact prices
3. **No slippage**: Doesn't simulate market slippage
4. **Historical bias**: Past performance doesn't guarantee future results
5. **Daily timeframe**: No trades on 1d, 1w, 1M timeframes (strategy requires intraday PDH/PDL)

## License

This project is provided as-is for educational and research purposes.

## Data Source

Historical XAUUSD data sourced from Kaggle:
[XAUUSD Gold Price Historical Data (2004-2024)](https://www.kaggle.com/datasets/novandraanugrah/xauusd-gold-price-historical-data-2004-2024)

## Disclaimer

This backtesting tool is for educational purposes only. Trading financial instruments carries risk. Past performance is not indicative of future results. Always conduct thorough testing and risk management before live trading.

---

**Built with Python** | Backtesting XAUUSD PDH/PDL Sweep Strategy

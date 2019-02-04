from backtesting import Backtest, Strategy
from backtesting.lib import resample_apply
import pandas as pd

def SMA(array, n):
    """Simple moving average"""
    return pd.Series(array).rolling(n).mean()


def RSI(array, n):
    """Relative strength index"""
    # Approximate; good enough
    gain = pd.Series(array).diff()
    loss = gain.copy()
    gain[gain < 0] = 0
    loss[loss > 0] = 0
    rs = gain.ewm(n).mean() / loss.abs().ewm(n).mean()
    return 100 - 100 / (1 + rs)
	
class System(Strategy):
    d_rsi = 30  # Daily RSI lookback periods
    level_low = 10
    level_high = 15
    
    def init(self):
        # Compute moving averages the strategy demands
        self.ma10 = self.I(SMA, self.data.Close, 10)

        
        # Compute daily RSI(30)
        self.daily_rsi = self.I(RSI, self.data.Close, self.d_rsi)
        
                
    def next(self):
        price = self.data.Close[-1]
        
        # If we don't already have a position, and
        # if all conditions are satisfied, enter long.
        if (not self.position and
		    self.daily_rsi[-1] > self.level_low and
            self.daily_rsi[-1] < self.level_high):
            
            # Buy at market price on next open, but do
            # set 8% fixed stop loss.
            self.buy(sl=.95 * price)
        
        # If the price closes 2% or more below 10-day MA
        # close the position, if any.
        elif price < .99 * self.ma10[-1]:
            self.position.close()
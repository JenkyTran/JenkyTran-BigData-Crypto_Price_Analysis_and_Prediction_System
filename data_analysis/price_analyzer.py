import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class PriceAnalyzer:
    def __init__(self):
        self.price_data = pd.DataFrame()
        self.technical_indicators = {}
        
    def add_price_data(self, data: List[Dict[str, Any]]):
        """
        Add new price data to the analyzer
        
        Args:
            data (List[Dict]): List of price data points
        """
        try:
            new_data = pd.DataFrame(data)
            new_data['timestamp'] = pd.to_datetime(new_data['timestamp'])
            self.price_data = pd.concat([self.price_data, new_data], ignore_index=True)
            logger.info(f"Added {len(data)} new price data points")
        except Exception as e:
            logger.error(f"Error adding price data: {str(e)}")
            raise
            
    def calculate_technical_indicators(self):
        """
        Calculate technical indicators for price analysis
        """
        try:
            if self.price_data.empty:
                raise ValueError("No price data available")
                
            # Sort by timestamp
            df = self.price_data.sort_values('timestamp')
            
            # Calculate moving averages
            df['MA_7'] = df['price'].rolling(window=7).mean()
            df['MA_25'] = df['price'].rolling(window=25).mean()
            df['MA_50'] = df['price'].rolling(window=50).mean()
            
            # Calculate RSI
            delta = df['price'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            
            # Calculate Bollinger Bands
            df['BB_middle'] = df['price'].rolling(window=20).mean()
            df['BB_std'] = df['price'].rolling(window=20).std()
            df['BB_upper'] = df['BB_middle'] + (df['BB_std'] * 2)
            df['BB_lower'] = df['BB_middle'] - (df['BB_std'] * 2)
            
            # Calculate MACD
            exp1 = df['price'].ewm(span=12, adjust=False).mean()
            exp2 = df['price'].ewm(span=26, adjust=False).mean()
            df['MACD'] = exp1 - exp2
            df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
            
            self.technical_indicators = df
            logger.info("Successfully calculated technical indicators")
            
        except Exception as e:
            logger.error(f"Error calculating technical indicators: {str(e)}")
            raise
            
    def detect_trend(self, window: int = 7) -> str:
        """
        Detect the current trend based on moving averages
        
        Args:
            window (int): Window size for trend detection
            
        Returns:
            str: Trend direction ('up', 'down', or 'sideways')
        """
        try:
            if self.technical_indicators.empty:
                self.calculate_technical_indicators()
                
            df = self.technical_indicators
            recent_data = df.tail(window)
            
            # Calculate price change
            price_change = (recent_data['price'].iloc[-1] - recent_data['price'].iloc[0]) / recent_data['price'].iloc[0]
            
            # Determine trend
            if price_change > 0.02:  # 2% increase
                return 'up'
            elif price_change < -0.02:  # 2% decrease
                return 'down'
            else:
                return 'sideways'
                
        except Exception as e:
            logger.error(f"Error detecting trend: {str(e)}")
            raise
            
    def detect_volatility(self, window: int = 7) -> float:
        """
        Calculate price volatility
        
        Args:
            window (int): Window size for volatility calculation
            
        Returns:
            float: Volatility percentage
        """
        try:
            if self.price_data.empty:
                raise ValueError("No price data available")
                
            df = self.price_data
            recent_data = df.tail(window)
            
            # Calculate daily returns
            returns = recent_data['price'].pct_change()
            
            # Calculate volatility (standard deviation of returns)
            volatility = returns.std() * np.sqrt(252)  # Annualized volatility
            
            return volatility
            
        except Exception as e:
            logger.error(f"Error calculating volatility: {str(e)}")
            raise
            
    def get_support_resistance_levels(self, window: int = 30) -> Dict[str, float]:
        """
        Identify support and resistance levels
        
        Args:
            window (int): Window size for level detection
            
        Returns:
            Dict: Support and resistance levels
        """
        try:
            if self.price_data.empty:
                raise ValueError("No price data available")
                
            df = self.price_data
            recent_data = df.tail(window)
            
            # Calculate local minima and maxima
            local_min = recent_data['price'].rolling(window=5, center=True).min()
            local_max = recent_data['price'].rolling(window=5, center=True).max()
            
            # Identify support and resistance levels
            support_levels = local_min[local_min == recent_data['price']].tolist()
            resistance_levels = local_max[local_max == recent_data['price']].tolist()
            
            return {
                'support_levels': support_levels,
                'resistance_levels': resistance_levels
            }
            
        except Exception as e:
            logger.error(f"Error identifying support/resistance levels: {str(e)}")
            raise 
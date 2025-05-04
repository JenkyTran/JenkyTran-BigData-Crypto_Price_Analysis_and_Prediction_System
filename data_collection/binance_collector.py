import os
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class BinanceCollector:
    def __init__(self):
        self.api_key = os.getenv('BINANCE_API_KEY')
        self.api_secret = os.getenv('BINANCE_API_SECRET')
        self.client = Client(self.api_key, self.api_secret)
        
    def get_historical_klines(self, symbol, interval, start_time, end_time=None):
        """
        Get historical klines (candlestick data) from Binance
        
        Args:
            symbol (str): Trading pair symbol (e.g., 'BTCUSDT')
            interval (str): Kline interval (e.g., '1h', '4h', '1d')
            start_time (str): Start time in ISO format
            end_time (str): End time in ISO format (optional)
            
        Returns:
            list: List of kline data
        """
        try:
            klines = self.client.get_historical_klines(
                symbol=symbol,
                interval=interval,
                start_str=start_time,
                end_str=end_time
            )
            return klines
        except BinanceAPIException as e:
            logger.error(f"Error fetching historical klines: {str(e)}")
            raise
            
    def get_current_price(self, symbol):
        """
        Get current price for a trading pair
        
        Args:
            symbol (str): Trading pair symbol (e.g., 'BTCUSDT')
            
        Returns:
            float: Current price
        """
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            return float(ticker['price'])
        except BinanceAPIException as e:
            logger.error(f"Error fetching current price: {str(e)}")
            raise
            
    def get_24h_stats(self, symbol):
        """
        Get 24-hour statistics for a trading pair
        
        Args:
            symbol (str): Trading pair symbol (e.g., 'BTCUSDT')
            
        Returns:
            dict: 24-hour statistics
        """
        try:
            stats = self.client.get_ticker(symbol=symbol)
            return stats
        except BinanceAPIException as e:
            logger.error(f"Error fetching 24h stats: {str(e)}")
            raise
            
    def get_order_book(self, symbol, limit=100):
        """
        Get order book for a trading pair
        
        Args:
            symbol (str): Trading pair symbol (e.g., 'BTCUSDT')
            limit (int): Number of orders to return
            
        Returns:
            dict: Order book data
        """
        try:
            order_book = self.client.get_order_book(symbol=symbol, limit=limit)
            return order_book
        except BinanceAPIException as e:
            logger.error(f"Error fetching order book: {str(e)}")
            raise 
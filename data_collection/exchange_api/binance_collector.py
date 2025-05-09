import os
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

"""
BinanceCollector - Thu thập dữ liệu từ Binance Exchange

Input:
    - symbol: Mã giao dịch (ví dụ: 'BTCUSDT')
    - interval: Chu kỳ nến (ví dụ: '1h', '4h', '1d')
    - start_time, end_time: Thời gian bắt đầu/kết thúc (ISO format)
    - handle_message: Hàm callback xử lý dữ liệu streaming (WebSocket)

Output:
    - Dữ liệu trả về là Python dict hoặc list (có thể chuyển thành JSON)
    - Cấu trúc dữ liệu ví dụ:

    1. get_current_price(symbol):
        float (giá hiện tại)
        Ví dụ: 65000.12

    2. get_historical_klines(symbol, interval, start_time, end_time):
        list[list]:
        [
            [
                1499040000000,      # Open time (timestamp, milliseconds)
                "0.01634790",      # Open price
                "0.80000000",      # High price
                "0.01575800",      # Low price
                "0.01577100",      # Close price
                "148976.11427815", # Volume
                1499644799999,      # Close time (timestamp, milliseconds)
                "2434.19055334",   # Quote asset volume
                308,                # Number of trades
                "1756.87402397",   # Taker buy base asset volume
                "28.46694368",     # Taker buy quote asset volume
                "17928899.62484339"# Ignore (không sử dụng)
            ],
            ...
        ]
        # Mỗi phần tử là 1 cây nến (candlestick) cho 1 khoảng thời gian

    3. get_24h_stats(symbol):
        dict:
        {
            'symbol': 'BTCUSDT',
            'priceChange': '100.00',           # Thay đổi giá 24h
            'priceChangePercent': '1.5',       # % thay đổi giá 24h
            'weightedAvgPrice': '65000.00',    # Giá trung bình 24h
            'prevClosePrice': '64900.00',      # Giá đóng cửa trước đó
            'lastPrice': '65000.00',           # Giá hiện tại
            'lastQty': '0.00129000',           # Khối lượng giao dịch cuối cùng
            'bidPrice': '65000.00',            # Giá mua tốt nhất
            'bidQty': '2.00000000',            # Khối lượng mua tốt nhất
            'askPrice': '65010.00',            # Giá bán tốt nhất
            'askQty': '1.50000000',            # Khối lượng bán tốt nhất
            'openPrice': '64000.00',           # Giá mở cửa 24h
            'highPrice': '65500.00',           # Giá cao nhất 24h
            'lowPrice': '63900.00',            # Giá thấp nhất 24h
            'volume': '39326.84006000',        # Tổng khối lượng giao dịch 24h
            'quoteVolume': '4022859313.72070470', # Tổng giá trị giao dịch 24h
            ...
        }

    4. get_order_book(symbol, limit):
        dict:
        {
            'lastUpdateId': 1027024,
            'bids': [
                ['65000.00', '1.20000000'],    # [giá, khối lượng]
                ...
            ],
            'asks': [
                ['65010.00', '0.80000000'],    # [giá, khối lượng]
                ...
            ]
        }
        # bids: Danh sách lệnh mua, asks: Danh sách lệnh bán

    5. stream_symbol_ticker(symbol, handle_message):
        - Streaming dữ liệu realtime qua WebSocket.
        - Callback nhận dict dạng:
        {
            'e': '24hrTicker',                 # Event type
            'E': 1672515782136,                # Event time (timestamp)
            's': 'BTCUSDT',                    # Symbol
            'p': '100.00',                     # Price change
            'P': '1.5',                        # Price change percent
            'w': '65000.00',                   # Weighted avg price
            'c': '65000.00',                   # Last price
            'Q': '0.001',                      # Last quantity
            'b': '64999.00',                   # Best bid price
            'B': '2.000',                      # Best bid qty
            'a': '65010.00',                   # Best ask price
            'A': '1.500',                      # Best ask qty
            'o': '64000.00',                   # Open price
            'h': '65500.00',                   # High price
            'l': '63900.00',                   # Low price
            'v': '39326.84',                   # Total traded base asset volume
            'q': '4022859313.72',              # Total traded quote asset volume
            ...
        }

"""

class BinanceCollector:
    def __init__(self):
        self.api_key = os.getenv('BINANCE_API_KEY')
        self.api_secret = os.getenv('BINANCE_API_SECRET')
        
        if not self.api_key or not self.api_secret:
            raise ValueError("Binance API credentials not found in .env file")
            
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

    def stream_symbol_ticker(self, symbol, handle_message, duration=10):
        """
        Streaming realtime ticker data cho một symbol sử dụng WebSocket.
        Args:
            symbol (str): Trading pair symbol (e.g., 'BTCUSDT')
            handle_message (function): Hàm callback xử lý dữ liệu nhận được
            duration (int): Số giây muốn stream (mặc định 10)
        """
        from binance import ThreadedWebsocketManager
        twm = ThreadedWebsocketManager(api_key=self.api_key, api_secret=self.api_secret)
        twm.start()
        twm.start_symbol_ticker_socket(callback=handle_message, symbol=symbol)
        import time
        time.sleep(duration)
        twm.stop()  
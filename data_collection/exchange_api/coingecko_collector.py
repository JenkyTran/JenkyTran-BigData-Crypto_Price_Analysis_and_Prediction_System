import os
import logging
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class CoinGeckoCollector:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Add API key if available
        api_key = os.getenv('COINGECKO_API_KEY')
        if api_key:
            self.headers['X-CG-API-KEY'] = api_key
        
    def get_coin_list(self) -> List[Dict[str, Any]]:
        """
        Get list of all coins with their IDs
        
        Returns:
            List[Dict]: List of coins with their details
        """
        try:
            response = requests.get(f"{self.base_url}/coins/list", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting coin list: {str(e)}")
            raise
            
    def get_coin_market_data(self, coin_id: str) -> Dict[str, Any]:
        """
        Get market data for a specific coin
        
        Args:
            coin_id (str): Coin ID (e.g., 'bitcoin', 'ethereum')
            
        Returns:
            Dict: Market data for the coin
        """
        try:
            response = requests.get(
                f"{self.base_url}/coins/{coin_id}",
                params={
                    'localization': 'false',
                    'tickers': 'false',
                    'market_data': 'true',
                    'community_data': 'true',
                    'developer_data': 'true'
                },
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting market data for {coin_id}: {str(e)}")
            raise
            
    def get_historical_data(self, coin_id: str, days: int = 30) -> Dict[str, Any]:
        """
        Get historical data for a coin
        
        Args:
            coin_id (str): Coin ID (e.g., 'bitcoin', 'ethereum')
            days (int): Number of days of historical data
            
        Returns:
            Dict: Historical data for the coin
        """
        try:
            response = requests.get(
                f"{self.base_url}/coins/{coin_id}/market_chart",
                params={
                    'vs_currency': 'usd',
                    'days': days,
                    'interval': 'daily'
                },
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting historical data for {coin_id}: {str(e)}")
            raise
            
    def get_global_data(self) -> Dict[str, Any]:
        """
        Get global cryptocurrency market data
        
        Returns:
            Dict: Global market data
        """
        try:
            response = requests.get(f"{self.base_url}/global", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting global data: {str(e)}")
            raise
            
    def get_trending_coins(self) -> List[Dict[str, Any]]:
        """
        Get trending coins
        
        Returns:
            List[Dict]: List of trending coins
        """
        try:
            response = requests.get(f"{self.base_url}/search/trending", headers=self.headers)
            response.raise_for_status()
            return response.json()['coins']
        except Exception as e:
            logger.error(f"Error getting trending coins: {str(e)}")
            raise 
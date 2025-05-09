import os
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class NewsCollector:
    def __init__(self):
        # List of crypto news websites
        self.news_sources = [
            'https://cointelegraph.com',
            'https://www.coindesk.com',
            'https://cryptonews.com',
            'https://www.newsbtc.com'
        ]
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def scrape_crypto_news(self) -> List[Dict[str, Any]]:
        """
        Scrape crypto news from various sources
        
        Returns:
            List[Dict]: List of news articles
        """
        try:
            articles = []
            headers = self.headers
            for source in self.news_sources:
                try:
                    response = requests.get(source, headers=headers)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Cointelegraph: lấy các bài viết bằng selector mới
                    if 'cointelegraph.com' in source:
                        for a in soup.select('a.post-card-inline__title-link'):
                            title = a.text.strip()
                            link = a['href']
                            if link.startswith('/'):
                                link = f'https://cointelegraph.com{link}'
                            article_data = {
                                'platform': 'news',
                                'source': source,
                                'title': title,
                                'url': link,
                                'timestamp': None
                            }
                            articles.append(article_data)
                    # TODO: Thêm selector cho các trang khác nếu cần
                except Exception as e:
                    logger.error(f"Error scraping {source}: {str(e)}")
                    continue
            logger.info(f"Collected {len(articles)} news articles")
            return articles
        except Exception as e:
            logger.error(f"Error scraping crypto news: {str(e)}")
            raise
            
    def scrape_coin_news(self, coin: str) -> List[Dict[str, Any]]:
        """
        Scrape news specifically about a cryptocurrency
        
        Args:
            coin (str): Cryptocurrency name (e.g., 'bitcoin', 'ethereum')
            
        Returns:
            List[Dict]: List of news articles about the coin
        """
        try:
            articles = []
            
            for source in self.news_sources:
                try:
                    # Construct search URL for the specific coin
                    search_url = f"{source}/search?q={coin}"
                    response = requests.get(search_url, headers=self.headers)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extract articles
                    for article in soup.find_all('article')[:10]:
                        title = article.find('h2').text.strip() if article.find('h2') else ''
                        link = article.find('a')['href'] if article.find('a') else ''
                        date = article.find('time')['datetime'] if article.find('time') else datetime.now().isoformat()
                        
                        if title and link:
                            article_data = {
                                'platform': 'news',
                                'source': source,
                                'coin': coin,
                                'title': title,
                                'url': link,
                                'timestamp': date
                            }
                            articles.append(article_data)
                            
                except Exception as e:
                    logger.error(f"Error scraping {source} for {coin}: {str(e)}")
                    continue
                    
            logger.info(f"Collected {len(articles)} news articles about {coin}")
            return articles
            
        except Exception as e:
            logger.error(f"Error scraping news for {coin}: {str(e)}")
            raise 
import os
import logging
import tweepy
import praw
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Dict, Any
from data_processing.kafka_producer import KafkaProducer

logger = logging.getLogger(__name__)

class SocialMediaScraper:
    def __init__(self):
        # Initialize Kafka producer
        self.kafka_producer = KafkaProducer()
        
        # Initialize Twitter API
        self.twitter_auth = tweepy.OAuthHandler(
            os.getenv('TWITTER_API_KEY'),
            os.getenv('TWITTER_API_SECRET')
        )
        self.twitter_auth.set_access_token(
            os.getenv('TWITTER_ACCESS_TOKEN'),
            os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        )
        self.twitter_api = tweepy.API(self.twitter_auth)
        
        # Initialize Reddit API
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent='CryptoAnalysisBot'
        )
        
        # List of crypto news websites
        self.news_sources = [
            'https://cointelegraph.com',
            'https://www.coindesk.com',
            'https://cryptonews.com',
            'https://www.newsbtc.com'
        ]
        
    def get_twitter_sentiment(self, query: str, count: int = 100) -> List[Dict[str, Any]]:
        """
        Collect tweets about crypto and analyze sentiment
        
        Args:
            query (str): Search query
            count (int): Number of tweets to collect
            
        Returns:
            List[Dict]: List of tweets with sentiment
        """
        try:
            tweets = []
            for tweet in tweepy.Cursor(
                self.twitter_api.search_tweets,
                q=query,
                lang='en',
                tweet_mode='extended'
            ).items(count):
                tweet_data = {
                    'platform': 'twitter',
                    'text': tweet.full_text,
                    'timestamp': tweet.created_at.isoformat(),
                    'user': tweet.user.screen_name,
                    'retweets': tweet.retweet_count,
                    'favorites': tweet.favorite_count
                }
                tweets.append(tweet_data)
                
            # Send to Kafka
            for tweet in tweets:
                self.kafka_producer.send_social_media_data('twitter', tweet)
                
            logger.info(f"Collected {len(tweets)} tweets about {query}")
            return tweets
            
        except Exception as e:
            logger.error(f"Error collecting tweets: {str(e)}")
            raise
            
    def get_reddit_sentiment(self, subreddit: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Collect Reddit posts and comments about crypto
        
        Args:
            subreddit (str): Subreddit name
            limit (int): Number of posts to collect
            
        Returns:
            List[Dict]: List of Reddit posts and comments
        """
        try:
            posts = []
            subreddit = self.reddit.subreddit(subreddit)
            
            for post in subreddit.hot(limit=limit):
                post_data = {
                    'platform': 'reddit',
                    'type': 'post',
                    'title': post.title,
                    'text': post.selftext,
                    'timestamp': datetime.fromtimestamp(post.created_utc).isoformat(),
                    'author': post.author.name if post.author else 'deleted',
                    'score': post.score,
                    'num_comments': post.num_comments
                }
                posts.append(post_data)
                
                # Get top comments
                post.comments.replace_more(limit=0)
                for comment in post.comments.list()[:10]:  # Top 10 comments
                    comment_data = {
                        'platform': 'reddit',
                        'type': 'comment',
                        'text': comment.body,
                        'timestamp': datetime.fromtimestamp(comment.created_utc).isoformat(),
                        'author': comment.author.name if comment.author else 'deleted',
                        'score': comment.score
                    }
                    posts.append(comment_data)
                    
            # Send to Kafka
            for post in posts:
                self.kafka_producer.send_social_media_data('reddit', post)
                
            logger.info(f"Collected {len(posts)} Reddit posts and comments from r/{subreddit}")
            return posts
            
        except Exception as e:
            logger.error(f"Error collecting Reddit data: {str(e)}")
            raise
            
    def scrape_crypto_news(self) -> List[Dict[str, Any]]:
        """
        Scrape crypto news from various sources
        
        Returns:
            List[Dict]: List of news articles
        """
        try:
            articles = []
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            for source in self.news_sources:
                try:
                    response = requests.get(source, headers=headers)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extract articles (adjust selectors based on each website)
                    for article in soup.find_all('article')[:10]:  # Get latest 10 articles
                        title = article.find('h2').text.strip() if article.find('h2') else ''
                        link = article.find('a')['href'] if article.find('a') else ''
                        date = article.find('time')['datetime'] if article.find('time') else datetime.now().isoformat()
                        
                        if title and link:
                            article_data = {
                                'platform': 'news',
                                'source': source,
                                'title': title,
                                'url': link,
                                'timestamp': date
                            }
                            articles.append(article_data)
                            
                except Exception as e:
                    logger.error(f"Error scraping {source}: {str(e)}")
                    continue
                    
            # Send to Kafka
            for article in articles:
                self.kafka_producer.send_social_media_data('news', article)
                
            logger.info(f"Collected {len(articles)} news articles")
            return articles
            
        except Exception as e:
            logger.error(f"Error scraping crypto news: {str(e)}")
            raise
            
    def collect_all_sources(self, query: str = "bitcoin OR ethereum OR crypto") -> Dict[str, List[Dict[str, Any]]]:
        """
        Collect data from all sources
        
        Args:
            query (str): Search query for Twitter
            
        Returns:
            Dict: Data from all sources
        """
        try:
            data = {
                'twitter': self.get_twitter_sentiment(query),
                'reddit': self.get_reddit_sentiment('CryptoCurrency'),
                'news': self.scrape_crypto_news()
            }
            
            logger.info("Successfully collected data from all sources")
            return data
            
        except Exception as e:
            logger.error(f"Error collecting data from all sources: {str(e)}")
            raise
            
    def close(self):
        """Close connections"""
        try:
            self.kafka_producer.close()
            logger.info("Closed all connections")
        except Exception as e:
            logger.error(f"Error closing connections: {str(e)}")
            raise 
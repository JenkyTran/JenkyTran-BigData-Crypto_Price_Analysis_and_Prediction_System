import os
import logging
import tweepy
from datetime import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class TwitterCollector:
    def __init__(self):
        # Get API credentials from environment variables
        api_key = os.getenv('TWITTER_API_KEY')
        api_secret = os.getenv('TWITTER_API_SECRET')
        access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        
        if not all([api_key, api_secret, access_token, access_token_secret]):
            raise ValueError("Twitter API credentials not found in .env file")
            
        # Initialize Twitter API
        self.twitter_auth = tweepy.OAuthHandler(api_key, api_secret)
        self.twitter_auth.set_access_token(access_token, access_token_secret)
        self.twitter_api = tweepy.API(self.twitter_auth)
        
    def get_tweets(self, query: str, count: int = 100) -> List[Dict[str, Any]]:
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
                
            logger.info(f"Collected {len(tweets)} tweets about {query}")
            return tweets
            
        except Exception as e:
            logger.error(f"Error collecting tweets: {str(e)}")
            raise
            
    def get_user_tweets(self, username: str, count: int = 100) -> List[Dict[str, Any]]:
        """
        Get tweets from a specific user
        
        Args:
            username (str): Twitter username
            count (int): Number of tweets to collect
            
        Returns:
            List[Dict]: List of user's tweets
        """
        try:
            tweets = []
            for tweet in tweepy.Cursor(
                self.twitter_api.user_timeline,
                screen_name=username,
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
                
            logger.info(f"Collected {len(tweets)} tweets from @{username}")
            return tweets
            
        except Exception as e:
            logger.error(f"Error collecting user tweets: {str(e)}")
            raise 
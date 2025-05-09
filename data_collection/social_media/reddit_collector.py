import os
import logging
import praw
from datetime import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class RedditCollector:
    def __init__(self):
        # Get API credentials from environment variables
        client_id = os.getenv('REDDIT_CLIENT_ID')
        client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        
        if not client_id or not client_secret:
            raise ValueError("Reddit API credentials not found in .env file")
            
        # Initialize Reddit API
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent='CryptoAnalysisBot'
        )
        
    def get_subreddit_posts(self, subreddit: str, limit: int = 100) -> List[Dict[str, Any]]:
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
                    
            logger.info(f"Collected {len(posts)} Reddit posts and comments from r/{subreddit}")
            return posts
            
        except Exception as e:
            logger.error(f"Error collecting Reddit data: {str(e)}")
            raise
            
    def get_user_posts(self, username: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get posts from a specific Reddit user
        
        Args:
            username (str): Reddit username
            limit (int): Number of posts to collect
            
        Returns:
            List[Dict]: List of user's posts
        """
        try:
            posts = []
            user = self.reddit.redditor(username)
            
            for post in user.submissions.new(limit=limit):
                post_data = {
                    'platform': 'reddit',
                    'type': 'post',
                    'title': post.title,
                    'text': post.selftext,
                    'timestamp': datetime.fromtimestamp(post.created_utc).isoformat(),
                    'subreddit': post.subreddit.display_name,
                    'score': post.score,
                    'num_comments': post.num_comments
                }
                posts.append(post_data)
                
            logger.info(f"Collected {len(posts)} posts from u/{username}")
            return posts
            
        except Exception as e:
            logger.error(f"Error collecting user posts: {str(e)}")
            raise 
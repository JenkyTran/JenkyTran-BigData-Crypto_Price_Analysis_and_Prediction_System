import os
import json
import logging
from kafka import KafkaProducer
from datetime import datetime

logger = logging.getLogger(__name__)

class KafkaProducer:
    def __init__(self):
        self.bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda v: v.encode('utf-8') if v else None
        )
        
    def send_crypto_price(self, symbol, price_data):
        """
        Send cryptocurrency price data to Kafka
        
        Args:
            symbol (str): Trading pair symbol (e.g., 'BTCUSDT')
            price_data (dict): Price data to send
        """
        try:
            # Add timestamp to data
            price_data['timestamp'] = datetime.utcnow().isoformat()
            
            # Send to crypto_prices topic
            self.producer.send(
                topic=os.getenv('KAFKA_TOPIC_CRYPTO_PRICES', 'crypto_prices'),
                key=symbol,
                value=price_data
            )
            self.producer.flush()
            
            logger.info(f"Sent price data for {symbol} to Kafka")
        except Exception as e:
            logger.error(f"Error sending price data to Kafka: {str(e)}")
            raise
            
    def send_social_media_data(self, platform, data):
        """
        Send social media data to Kafka
        
        Args:
            platform (str): Social media platform (e.g., 'twitter', 'reddit')
            data (dict): Social media data to send
        """
        try:
            # Add timestamp and platform to data
            data['timestamp'] = datetime.utcnow().isoformat()
            data['platform'] = platform
            
            # Send to social_media topic
            self.producer.send(
                topic=os.getenv('KAFKA_TOPIC_SOCIAL_MEDIA', 'social_media'),
                key=platform,
                value=data
            )
            self.producer.flush()
            
            logger.info(f"Sent {platform} data to Kafka")
        except Exception as e:
            logger.error(f"Error sending social media data to Kafka: {str(e)}")
            raise
            
    def close(self):
        """Close the Kafka producer connection"""
        try:
            self.producer.close()
            logger.info("Kafka producer closed successfully")
        except Exception as e:
            logger.error(f"Error closing Kafka producer: {str(e)}")
            raise 
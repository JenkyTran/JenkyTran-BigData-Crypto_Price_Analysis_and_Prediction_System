import os
import logging
from dotenv import load_dotenv
from data_collection.binance_collector import BinanceCollector
# from data_collection.coingecko_collector import CoinGeckoCollector
from data_collection.social_media_scraper import SocialMediaScraper
from data_processing.kafka_producer import KafkaProducer
from data_processing.spark_processor import SparkProcessor
from data_analysis.dashboard import Dashboard
# from ml_models.model_manager import ModelManager

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=os.getenv('LOG_FILE', './logs/crypto_analysis.log')
)
logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("Starting Crypto Analysis System...")
        
        # Initialize data collectors
        binance_collector = BinanceCollector()
        # coingecko_collector = CoinGeckoCollector()
        social_media_scraper = SocialMediaScraper()
        
        # Initialize data processors
        kafka_producer = KafkaProducer()
        spark_processor = SparkProcessor()
        
        # Initialize ML models
        # model_manager = ModelManager()
        
        # Initialize dashboard
        dashboard = Dashboard()
        
        logger.info("System initialized successfully")
        
        # Start data collection and processing
        data = social_media_scraper.collect_all_sources()
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main()

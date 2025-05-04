import os
import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, to_timestamp
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

logger = logging.getLogger(__name__)

class SparkProcessor:
    def __init__(self):
        self.spark = SparkSession.builder \
            .appName(os.getenv('SPARK_APP_NAME', 'CryptoAnalysis')) \
            .master(os.getenv('SPARK_MASTER', 'local[*]')) \
            .getOrCreate()
            
        # Define schemas for different data types
        self.price_schema = StructType([
            StructField("symbol", StringType(), True),
            StructField("price", DoubleType(), True),
            StructField("volume", DoubleType(), True),
            StructField("timestamp", TimestampType(), True)
        ])
        
        self.social_media_schema = StructType([
            StructField("platform", StringType(), True),
            StructField("text", StringType(), True),
            StructField("sentiment", DoubleType(), True),
            StructField("timestamp", TimestampType(), True)
        ])
        
    def process_crypto_prices(self, kafka_topic):
        """
        Process cryptocurrency price data from Kafka
        
        Args:
            kafka_topic (str): Kafka topic name for crypto prices
            
        Returns:
            DataFrame: Processed price data
        """
        try:
            # Read from Kafka
            df = self.spark.readStream \
                .format("kafka") \
                .option("kafka.bootstrap.servers", os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')) \
                .option("subscribe", kafka_topic) \
                .load()
                
            # Parse JSON data
            df = df.select(
                from_json(col("value").cast("string"), self.price_schema).alias("data")
            ).select("data.*")
            
            # Add processing time
            df = df.withColumn("processing_time", to_timestamp(col("timestamp")))
            
            logger.info("Successfully processed crypto price data")
            return df
            
        except Exception as e:
            logger.error(f"Error processing crypto prices: {str(e)}")
            raise
            
    def process_social_media(self, kafka_topic):
        """
        Process social media data from Kafka
        
        Args:
            kafka_topic (str): Kafka topic name for social media data
            
        Returns:
            DataFrame: Processed social media data
        """
        try:
            # Read from Kafka
            df = self.spark.readStream \
                .format("kafka") \
                .option("kafka.bootstrap.servers", os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')) \
                .option("subscribe", kafka_topic) \
                .load()
                
            # Parse JSON data
            df = df.select(
                from_json(col("value").cast("string"), self.social_media_schema).alias("data")
            ).select("data.*")
            
            # Add processing time
            df = df.withColumn("processing_time", to_timestamp(col("timestamp")))
            
            logger.info("Successfully processed social media data")
            return df
            
        except Exception as e:
            logger.error(f"Error processing social media data: {str(e)}")
            raise
            
    def aggregate_data(self, df, window_duration, slide_duration):
        """
        Aggregate data over a time window
        
        Args:
            df (DataFrame): Input DataFrame
            window_duration (str): Window duration (e.g., '5 minutes')
            slide_duration (str): Slide duration (e.g., '1 minute')
            
        Returns:
            DataFrame: Aggregated data
        """
        try:
            # Group by time window and calculate statistics
            aggregated_df = df.groupBy(
                window(col("timestamp"), window_duration, slide_duration)
            ).agg(
                {"price": "avg", "volume": "sum"}
            )
            
            logger.info("Successfully aggregated data")
            return aggregated_df
            
        except Exception as e:
            logger.error(f"Error aggregating data: {str(e)}")
            raise
            
    def stop(self):
        """Stop the Spark session"""
        try:
            self.spark.stop()
            logger.info("Spark session stopped successfully")
        except Exception as e:
            logger.error(f"Error stopping Spark session: {str(e)}")
            raise 
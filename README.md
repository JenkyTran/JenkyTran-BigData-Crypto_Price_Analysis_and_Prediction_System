# Crypto Price Analysis and Prediction System

A Big Data system for analyzing and predicting cryptocurrency prices using real-time data from exchanges, social media, and news sources.

## Project Structure

```
crypto-analysis/
├── data_collection/          # Data collection modules
│   ├── exchange_api/         # Binance, CoinGecko API integration
│   ├── social_media/         # Twitter, Reddit data collection
│   └── news_scraper/         # News scraping modules
├── data_processing/          # Data processing pipeline
│   ├── kafka/               # Kafka streaming setup
│   ├── spark/               # Spark processing jobs
│   └── storage/             # MongoDB, Elasticsearch integration
├── analytics/               # Data analysis and visualization
│   ├── dashboard/           # Streamlit/Dash dashboard
│   ├── visualization/       # Data visualization scripts
│   └── reports/             # Analysis reports
├── ml_models/               # Machine learning models
│   ├── arima/              # ARIMA model implementation
│   ├── lstm/               # LSTM model implementation
│   └── prophet/            # Prophet model implementation
├── config/                  # Configuration files
├── tests/                   # Test files
└── docs/                    # Documentation
```

## Technology Stack

- **Data Collection**: 
  - Binance API, CoinGecko API
  - BeautifulSoup, Selenium for web scraping
- **Data Processing**:
  - Apache Kafka for streaming
  - Apache Spark for processing
  - MongoDB, Elasticsearch for storage
- **Analytics & Visualization**:
  - Kibana, Power BI
  - Matplotlib, Seaborn
  - Streamlit/Dash
- **Machine Learning**:
  - ARIMA, LSTM, Prophet models
  - TensorFlow/PyTorch

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configurations
```

3. Start the system:
```bash
python main.py
```

## Project Timeline

- Week 1: Data Collection & Integration
- Week 2: Data Processing Pipeline
- Week 3: Data Visualization
- Week 4: Data Analysis
- Week 5: Machine Learning Models
- Week 6: Final Integration & Documentation

## Team Members

- Trần Văn Lực (20210555) - Backend Developer
- Nguyễn Quang Huy (20225009) - Data Engineer
- Cao Nam Cường (20215323) - Data Analyst/Visualization Developer
- Trần Mạnh Hoàng - Machine Learning Engineer

## License

MIT License
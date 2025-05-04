import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from pymongo import MongoClient
from dotenv import load_dotenv
import os

class Dashboard:
    def __init__(self):
        load_dotenv()
        self.mongo_client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.mongo_client[os.getenv('MONGODB_DB_NAME')]
        
    def setup_page(self):
        st.set_page_config(
            page_title="Crypto Analysis Dashboard",
            page_icon="📊",
            layout="wide"
        )
        st.title("Phân tích và Dự đoán giá tiền điện tử")
        
    def display_price_chart(self, symbol='BTCUSDT', days=30):
        # Lấy dữ liệu từ MongoDB
        collection = self.db['crypto_prices']
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        data = list(collection.find({
            'symbol': symbol,
            'timestamp': {'$gte': start_date, '$lte': end_date}
        }).sort('timestamp', 1))
        
        if not data:
            st.warning(f"Không tìm thấy dữ liệu cho {symbol}")
            return
            
        df = pd.DataFrame(data)
        
        # Tạo biểu đồ giá
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=df['timestamp'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='Giá'
        ))
        
        fig.update_layout(
            title=f'Biểu đồ giá {symbol}',
            xaxis_title='Thời gian',
            yaxis_title='Giá (USDT)',
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    def display_sentiment_analysis(self, symbol='BTC'):
        # Lấy dữ liệu sentiment từ MongoDB
        collection = self.db['social_media']
        data = list(collection.find({
            'symbol': symbol,
            'timestamp': {'$gte': datetime.now() - timedelta(days=7)}
        }).sort('timestamp', 1))
        
        if not data:
            st.warning(f"Không tìm thấy dữ liệu sentiment cho {symbol}")
            return
            
        df = pd.DataFrame(data)
        
        # Tính toán sentiment trung bình theo ngày
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        sentiment_by_day = df.groupby('date')['sentiment'].mean().reset_index()
        
        # Tạo biểu đồ sentiment
        fig = px.line(sentiment_by_day, x='date', y='sentiment',
                     title=f'Phân tích tâm lý thị trường {symbol}')
        fig.update_layout(
            xaxis_title='Ngày',
            yaxis_title='Sentiment Score',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    def display_prediction(self, symbol='BTCUSDT'):
        # Lấy dữ liệu dự đoán từ MongoDB
        collection = self.db['predictions']
        prediction = collection.find_one({
            'symbol': symbol,
            'timestamp': {'$gte': datetime.now() - timedelta(hours=1)}
        })
        
        if not prediction:
            st.warning(f"Không tìm thấy dự đoán mới nhất cho {symbol}")
            return
            
        # Hiển thị dự đoán
        st.subheader(f"Dự đoán giá {symbol}")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Giá hiện tại", f"${prediction['current_price']:.2f}")
        with col2:
            st.metric("Dự đoán ngắn hạn", f"${prediction['short_term_prediction']:.2f}")
        with col3:
            st.metric("Dự đoán dài hạn", f"${prediction['long_term_prediction']:.2f}")
            
        # Hiển thị biểu đồ dự đoán
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=prediction['timestamps'],
            y=prediction['predicted_prices'],
            name='Dự đoán',
            line=dict(color='red')
        ))
        fig.add_trace(go.Scatter(
            x=prediction['timestamps'],
            y=prediction['actual_prices'],
            name='Thực tế',
            line=dict(color='blue')
        ))
        
        fig.update_layout(
            title=f'Dự đoán giá {symbol}',
            xaxis_title='Thời gian',
            yaxis_title='Giá (USDT)',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    def run(self):
        self.setup_page()
        
        # Sidebar controls
        st.sidebar.header("Cài đặt")
        symbol = st.sidebar.selectbox(
            "Chọn đồng tiền",
            ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']
        )
        days = st.sidebar.slider(
            "Số ngày hiển thị",
            min_value=1,
            max_value=90,
            value=30
        )
        
        # Main content
        tab1, tab2, tab3 = st.tabs(["Biểu đồ giá", "Phân tích tâm lý", "Dự đoán"])
        
        with tab1:
            self.display_price_chart(symbol, days)
            
        with tab2:
            self.display_sentiment_analysis(symbol.replace('USDT', ''))
            
        with tab3:
            self.display_prediction(symbol)
            
if __name__ == "__main__":
    dashboard = Dashboard()
    dashboard.run() 
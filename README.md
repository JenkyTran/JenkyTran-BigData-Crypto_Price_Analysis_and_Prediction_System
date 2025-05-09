# Hệ Thống Phân Tích và Dự Đoán Giá Tiền Điện Tử (Crypto Price Analysis and Prediction System)

## Giới Thiệu

Dự án này nhằm xây dựng một hệ thống Big Data toàn diện để thu thập, xử lý, phân tích và dự đoán giá của các loại tiền điện tử. Hệ thống tận dụng dữ liệu từ nhiều nguồn đa dạng bao gồm các sàn giao dịch lớn, mạng xã hội và các trang tin tức tài chính để cung cấp cái nhìn sâu sắc về thị trường và đưa ra các dự báo có giá trị.

Mục tiêu cốt lõi là áp dụng các công nghệ và kiến trúc Big Data (như Lambda hoặc Kappa) để xử lý hiệu quả các đặc tính 3V (Volume, Velocity, Variety) của dữ liệu crypto, từ đó xây dựng các mô hình học máy tiên tiến cho việc dự đoán xu hướng giá.

## Mục Lục

- [Tổng Quan](#tổng-quan)
- [Kiến Trúc Hệ Thống](#kiến-trúc-hệ-thống)
- [Công Nghệ Sử Dụng](#công-nghệ-sử-dụng)
- [Cấu Trúc Dự Án](#cấu-trúc-dự-án)
- [Luồng Dữ Liệu Chính](#luồng-dữ-liệu-chính)
- [Quy Trình Phát Triển & Phân Chia Công Việc](#quy-trình-phát-triển--phân-chia-công-việc)
  - [Thành Viên Nhóm](#thành-viên-nhóm)
  - [Kế Hoạch Chi Tiết Theo Tuần](#kế-hoạch-chi-tiết-theo-tuần)
- [Tính Năng Chính](#tính-năng-chính)
- [Hướng Dẫn Cài Đặt và Chạy Dự Án](#hướng-dẫn-cài-đặt-và-chạy-dự-án)
- [Tài Liệu Kỹ Thuật Chi Tiết](#tài-liệu-kỹ-thuật-chi-tiết)
- [Hướng Phát Triển Tương Lai](#hướng-phát-triển-tương-lai)

## Tổng Quan

Thị trường tiền điện tử nổi tiếng với sự biến động cao và phức tạp. Việc phân tích và dự đoán giá đòi hỏi khả năng xử lý lượng lớn dữ liệu thay đổi nhanh chóng từ nhiều nguồn khác nhau. Dự án này giải quyết thách thức đó bằng cách:

1.  **Thu thập dữ liệu đa dạng:** Từ giá giao dịch real-time, khối lượng, đến các tin tức thị trường và tâm lý cộng đồng trên mạng xã hội.
2.  **Xử lý dữ liệu lớn:** Sử dụng Apache Kafka cho streaming và Apache Spark cho cả xử lý batch và stream.
3.  **Lưu trữ hiệu quả:** Kết hợp Data Lake (HDFS/Cloud Storage) cho dữ liệu thô và NoSQL (MongoDB, Elasticsearch) cho dữ liệu đã xử lý và phục vụ truy vấn nhanh.
4.  **Phân tích sâu và trực quan hóa:** Cung cấp dashboard tương tác (Kibana, PowerBI, Streamlit/Dash) để theo dõi các chỉ số quan trọng.
5.  **Dự đoán thông minh:** Áp dụng các mô hình Machine Learning (ARIMA, Prophet, LSTM) để dự báo xu hướng giá.

## Kiến Trúc Hệ Thống

Hệ thống được thiết kế dựa trên kiến trúc **Lambda** (hoặc **Kappa** tùy theo ưu tiên triển khai), bao gồm các tầng chính:

*   **Tầng Thu Thập Dữ Liệu (Ingestion Layer):** Thu thập dữ liệu từ các API sàn giao dịch (Binance, CoinGecko), web scraping tin tức và dữ liệu từ mạng xã hội (Twitter, Reddit).
*   **Tầng Truyền Tải Dữ Liệu (Streaming Layer):** Apache Kafka được sử dụng để tiếp nhận và truyền tải dữ liệu real-time dưới dạng các luồng (streams).
*   **Tầng Xử Lý Dữ Liệu (Processing Layer):**
    *   **Batch Processing (Spark):** Xử lý dữ liệu lịch sử lớn, thực hiện các tác vụ làm sạch, biến đổi phức tạp, trích xuất đặc trưng cho mô hình ML, và phân tích sentiment.
    *   **Stream Processing (Spark Structured Streaming):** Xử lý dữ liệu real-time từ Kafka, tính toán các chỉ số nhanh, và cập nhật dữ liệu cho dashboard.
*   **Tầng Lưu Trữ (Storage Layer):**
    *   **Data Lake (HDFS, Google Cloud Storage, AWS S3):** Lưu trữ dữ liệu thô và dữ liệu trung gian đã được xử lý theo batch.
    *   **MongoDB:** Lưu trữ dữ liệu phi cấu trúc hoặc bán cấu trúc như bài viết từ mạng xã hội, tin tức.
    *   **Elasticsearch:** Lưu trữ dữ liệu đã được tối ưu hóa cho việc tìm kiếm, phân tích và trực quan hóa trên Kibana.
*   **Tầng Phục Vụ và Phân Tích (Serving & Analytics Layer):**
    *   **Kibana/PowerBI/Streamlit/Dash:** Cung cấp giao diện trực quan để theo dõi thị trường, xem kết quả phân tích và dự đoán.
    *   **API (Tùy chọn):** Cung cấp API để các ứng dụng khác có thể truy cập kết quả dự đoán.
*   **Tầng Học Máy (Machine Learning Layer):** Huấn luyện, đánh giá và triển khai các mô hình dự đoán giá.

*(Nên có một sơ đồ kiến trúc ở đây)*

## Công Nghệ Sử Dụng

*   **Thu Thập Dữ Liệu:**
    *   Python (`requests`, `tweepy`, `praw`, `BeautifulSoup`, `Scrapy`, `Selenium`)
    *   API: Binance, CoinGecko
    *   (Tùy chọn) Apache NiFi
*   **Truyền Tải Dữ Liệu:**
    *   Apache Kafka
*   **Lưu Trữ Dữ Liệu:**
    *   HDFS / Google Cloud Storage / AWS S3
    *   MongoDB
    *   Elasticsearch
*   **Xử Lý Dữ Liệu:**
    *   Apache Spark (Core, SQL, Structured Streaming)
    *   Ngôn ngữ: PySpark, Scala (nếu có)
*   **Học Máy & Phân Tích Sentiment:**
    *   Spark MLlib, Scikit-learn
    *   TensorFlow / Keras / PyTorch (cho LSTM)
    *   `statsmodels` (cho ARIMA), `fbprophet` (cho Prophet)
    *   Thư viện NLP: `nltk`, `spaCy`, `underthesea`, `transformers`
*   **Trực Quan Hóa Dữ Liệu:**
    *   Kibana
    *   Power BI / Tableau
    *   Streamlit / Dash (Plotly)
*   **Triển Khai & Vận Hành:**
    *   Docker, Docker Compose
    *   (Tùy chọn) Apache Airflow, Cron
*   **Quản Lý Phiên Bản:** Git

## Cấu Trúc Dự Án

```
crypto-analysis/
├── data_collection/                 # Thu thập dữ liệu
│   ├── exchange_api/               # API từ các sàn giao dịch
│   │   ├── binance_collector.py    # Thu thập dữ liệu từ Binance
│   │   └── coingecko_collector.py  # Thu thập dữ liệu từ CoinGecko
│   │
│   ├── social_media/              # Dữ liệu từ mạng xã hội
│   │   ├── twitter_collector.py   # Thu thập tweets
│   │   └── reddit_collector.py    # Thu thập posts từ Reddit
│   │
│   └── news_scraper/             # Thu thập tin tức
│       ├── news_collector.py     # Scrape tin tức từ các trang
│       └── rss_collector.py      # Thu thập từ RSS feeds
│
├── data_processing/              # Xử lý dữ liệu
│   ├── kafka_producers/         # Đẩy dữ liệu vào Kafka
│   │   ├── price_producer.py    # Producer cho dữ liệu giá
│   │   └── social_producer.py   # Producer cho dữ liệu mạng xã hội
│   │
│   ├── spark_jobs/             # Xử lý dữ liệu với Spark
│   │   ├── batch/             # Xử lý batch
│   │   │   └── price_processor.py
│   │   └── streaming/         # Xử lý streaming
│   │       └── realtime_processor.py
│   │
│   └── nlp_sentiment/         # Phân tích sentiment
│       ├── text_processor.py
│       └── sentiment_analyzer.py
│
├── data_storage/              # Lưu trữ dữ liệu
│   ├── mongodb/              # Cấu hình MongoDB
│   │   ├── schemas/         # Định nghĩa schema
│   │   └── indexes/         # Cấu hình indexes
│   │
│   └── elasticsearch/       # Cấu hình Elasticsearch
│       ├── mappings/        # Định nghĩa mappings
│       └── templates/       # Index templates
│
├── analytics/               # Phân tích và trực quan hóa
│   ├── dashboards/         # Cấu hình dashboard
│   │   ├── kibana/        # Dashboards Kibana
│   │   └── streamlit/     # Ứng dụng Streamlit
│   │
│   └── visualizations/     # Scripts tạo biểu đồ
│       ├── price_charts.py
│       └── sentiment_charts.py
│
├── ml_models/              # Mô hình Machine Learning
│   ├── notebooks/         # Jupyter notebooks
│   │   ├── eda/          # Phân tích dữ liệu
│   │   └── experiments/  # Thử nghiệm mô hình
│   │
│   ├── training/         # Scripts huấn luyện
│   │   ├── arima/
│   │   ├── lstm/
│   │   └── prophet/
│   │
│   └── models/           # Mô hình đã huấn luyện
│
├── deployment/           # Triển khai hệ thống
│   ├── docker/          # Cấu hình Docker
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   │
│   └── kubernetes/      # Cấu hình Kubernetes (nếu cần)
│
├── config/              # Cấu hình hệ thống
│   ├── .env.example    # Mẫu file cấu hình
│   └── config.yaml     # Cấu hình chung
│
├── tests/              # Kiểm thử
│   ├── unit/          # Unit tests
│   └── integration/   # Integration tests
│
└── docs/              # Tài liệu
    ├── api/          # Tài liệu API
    ├── setup/        # Hướng dẫn cài đặt
    └── architecture/ # Tài liệu kiến trúc
```

## Luồng Dữ Liệu Chính

1.  **Thu thập:** Các script Python định kỳ hoặc liên tục lấy dữ liệu giá từ API Binance/CoinGecko, scrape tin tức từ các trang báo, và thu thập bài viết/bình luận từ Twitter/Reddit.
2.  **Đẩy vào Kafka:** Dữ liệu thô từ các nguồn được chuẩn hóa sơ bộ và đẩy vào các Kafka topics tương ứng (`crypto_price_raw`, `social_media_raw`, `news_raw`).
3.  **Xử lý Batch (Hàng ngày/định kỳ):**
    *   Spark đọc dữ liệu thô (đặc biệt là dữ liệu lịch sử lớn) từ Data Lake hoặc Kafka (nếu replay).
    *   Thực hiện làm sạch, biến đổi, tính toán các chỉ số kỹ thuật, phân tích sentiment cho tin tức/mạng xã hội.
    *   Dữ liệu đã xử lý được lưu lại vào Data Lake (Parquet/Avro) và/hoặc Elasticsearch/MongoDB cho truy vấn.
    *   Huấn luyện lại các mô hình ML với dữ liệu mới.
4.  **Xử lý Stream (Real-time/Near Real-time):**
    *   Spark Structured Streaming đọc dữ liệu mới từ Kafka topics.
    *   Thực hiện các phép tính toán nhanh (ví dụ: giá trung bình động, cảnh báo biến động bất thường), phân tích sentiment sơ bộ.
    *   Ghi kết quả đã xử lý vào Elasticsearch để cập nhật dashboard gần như ngay lập tức.
5.  **Lưu trữ:**
    *   Dữ liệu thô và dữ liệu batch đã xử lý: HDFS/Cloud Storage.
    *   Dữ liệu tin tức, mạng xã hội (dạng document): MongoDB.
    *   Dữ liệu cho dashboard và truy vấn nhanh: Elasticsearch.
6.  **Phân tích và Trực quan hóa:**
    *   Kibana đọc dữ liệu từ Elasticsearch để hiển thị các biểu đồ, đồ thị về giá, khối lượng, sentiment, kết quả dự đoán.
    *   (Tùy chọn) Streamlit/Dash app cung cấp giao diện tùy chỉnh.
7.  **Dự đoán:**
    *   Mô hình ML (ARIMA, Prophet, LSTM) được huấn luyện trên dữ liệu lịch sử và các feature đã trích xuất.
    *   Kết quả dự đoán được lưu trữ và hiển thị trên dashboard.

## Quy Trình Phát Triển & Phân Chia Công Việc

### Thành Viên Nhóm

| MSSV     | Tên                 | Vai trò                                   |
| :------- | :------------------ | :--------------------------------------- |
| 20210555 | Trần Văn Lực        | Backend Developer                        |
| 20225009 | Nguyễn Quang Huy    | Data Engineer                            |
| 20215323 | Cao Nam Cường       | Machine Learning Engineer                |
|          | Trần Mạnh Hoàng     | Data Analyst / Visualization Developer |

### Kế Hoạch Chi Tiết Theo Tuần

*(Tóm tắt các nhiệm vụ chính từ kế hoạch chi tiết của bạn)*

**Tuần 1: Tìm hiểu & Nghiên cứu – Thu thập, xử lý và tích hợp dữ liệu**

*   **Cả nhóm:** Nghiên cứu nguồn dữ liệu, API.
*   **Backend Developer (Lực):** Xây dựng scripts thu thập dữ liệu giá (API Binance, CoinGecko) và crawler cơ bản cho tin tức/mạng xã hội.
*   **Data Engineer (Huy):** Thiết kế pipeline Kafka, module xử lý sơ bộ bằng Spark, tích hợp lưu trữ vào MongoDB/Elasticsearch.
*   **Lực & Huy:** Tích hợp module thu thập và pipeline xử lý, kiểm thử.
*   **Cả nhóm:** Họp tổng kết, thống nhất chuẩn đầu ra.

**Tuần 2: Phát triển & Triển khai – Trực quan hóa, dự báo và tích hợp hệ thống**

*   **Data Analyst (Hoàng):** Thiết kế và xây dựng dashboard (Kibana/PowerBI/Streamlit) trực quan hóa giá, khối lượng, sentiment.
*   **ML Engineer (Cường):** Phát triển và thử nghiệm các mô hình dự báo giá (ARIMA, LSTM, Prophet), đánh giá độ chính xác.
*   **Cả nhóm (phối hợp):** Tích hợp dashboard với backend và mô hình ML, kiểm thử end-to-end.
*   **Cả nhóm:** Tổng kết, chuẩn bị báo cáo và slide thuyết trình.

**Quy Trình Làm Việc Chung:**

*   **Giao tiếp & Theo dõi:** Sử dụng Trello/Asana.
*   **Đầu ra minh bạch:** Lưu trữ code, báo cáo, tài liệu kỹ thuật.
*   **Backup & Versioning:** Sử dụng Git.

## Tính Năng Chính

*   Thu thập dữ liệu giá crypto real-time và lịch sử từ nhiều sàn.
*   Thu thập tin tức tài chính và dữ liệu từ mạng xã hội liên quan đến crypto.
*   Xử lý và làm sạch dữ liệu bằng Apache Spark.
*   Phân tích sentiment từ tin tức và mạng xã hội.
*   Lưu trữ dữ liệu hiệu quả với HDFS, MongoDB và Elasticsearch.
*   Trực quan hóa dữ liệu thị trường, sentiment và kết quả dự đoán qua dashboard tương tác.
*   Dự đoán xu hướng giá crypto sử dụng các mô hình ARIMA, LSTM, Prophet.
*   Hệ thống được đóng gói bằng Docker để dễ dàng triển khai.

## Hướng Dẫn Cài Đặt và Chạy Dự Án

*(Phần này sẽ được chi tiết hóa khi dự án hoàn thiện)*

1.  **Yêu cầu tiên quyết:**
    *   Docker & Docker Compose
    *   Python 3.x, Pip
    *   Java (cho Hadoop, Spark, Kafka, Elasticsearch)
    *   Truy cập Internet để tải dependencies và dữ liệu
    *   API Keys (Binance, Twitter, etc. - lưu trong file `.env`)
2.  **Clone repository:**
    ```bash
    git clone <repository_url>
    cd crypto-analysis
    ```
3.  **Cấu hình môi trường:**
    ```bash
    cp config/.env.example config/.env
    # Sửa đổi file config/.env với API keys và các cấu hình cần thiết
    ```
4.  **Cài đặt dependencies (nếu chạy service ngoài Docker):**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Khởi chạy hệ thống (sử dụng Docker Compose):**
    ```bash
    docker-compose up -d --build
    ```
6.  **Truy cập các thành phần:**
    *   Kibana: `http://localhost:5601`
    *   Spark Master UI: `http://localhost:8080`
    *   (Các UI khác nếu có)
7.  **Chạy các tác vụ cụ thể (ví dụ: Spark job):**
    ```bash
    # Ví dụ chạy một Spark batch job
    docker-compose exec spark-master spark-submit \
        --master spark://spark-master:7077 \
        /opt/spark_jobs/batch/example_batch_job.py
    ```
8.  **Dừng hệ thống:**
    ```bash
    docker-compose down
    ```

## Tài Liệu Kỹ Thuật Chi Tiết

Để hiểu rõ hơn về thiết kế và triển khai của từng thành phần trong hệ thống, vui lòng tham khảo **[Tài Liệu Kỹ Thuật Chi Tiết](./docs/technical_documentation.md)**. *(Link đến file tài liệu kỹ thuật bạn đã tạo)*

Tài liệu này bao gồm các thông tin về:
*   Kiến trúc hệ thống chi tiết.
*   Mô tả nguồn dữ liệu và quy trình thu thập.
*   Cấu hình Kafka, Spark, Elasticsearch, MongoDB.
*   Luồng xử lý dữ liệu batch và stream.
*   Chi tiết về các mô hình Machine Learning và phân tích sentiment.
*   Thiết kế dashboard và trực quan hóa.
*   Hướng dẫn triển khai và vận hành.

## Hướng Phát Triển Tương Lai

*   Mở rộng nguồn dữ liệu: Thêm nhiều sàn giao dịch, nguồn tin tức, và nền tảng mạng xã hội.
*   Cải thiện mô hình dự đoán: Sử dụng các kỹ thuật ensemble, deep learning phức tạp hơn, tích hợp thêm nhiều features (ví dụ: phân tích kỹ thuật, dữ liệu on-chain).
*   Xây dựng hệ thống cảnh báo real-time cho các biến động bất thường hoặc cơ hội giao dịch.
*   Phát triển API công khai để chia sẻ kết quả phân tích và dự đoán.
*   Tối ưu hóa hiệu năng hệ thống và khả năng mở rộng.
*   Tích hợp phân tích dữ liệu on-chain (ví dụ: số lượng ví hoạt động, dòng tiền vào/ra sàn).

---

## License

MIT License
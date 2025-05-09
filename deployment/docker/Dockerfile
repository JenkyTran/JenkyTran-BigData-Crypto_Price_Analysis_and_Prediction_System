FROM python:3.10-slim

WORKDIR /app

# Cài đặt các dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn vào container
COPY . .

# Biến môi trường (nếu cần)
ENV PYTHONUNBUFFERED=1


CMD ["python", "main.py"] 
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
ARG BUILD_NUMBER=0
ENV APP_VERSION=${BUILD_NUMBER}
EXPOSE 5000
CMD ["python", "app.py"]

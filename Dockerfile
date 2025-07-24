FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
COPY .env ./
RUN pip install --no-cache-dir -r requirements.txt

ADD ./src .

EXPOSE 8080
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8080}"]

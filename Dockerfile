FROM python:3.10-slim

WORKDIR /lemmatizer

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt && \
    python -m spacy download en_core_web_sm && \
    python -m spacy download es_core_news_sm

COPY . /lemmatizer

CMD ["sh", "-c", "cd app; uvicorn main:server --host 0.0.0.0 --port 4355 --workers 1"]
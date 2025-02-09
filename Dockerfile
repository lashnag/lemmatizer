FROM python:3.10-slim

WORKDIR /lemmatizer

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /lemmatizer

CMD ["sh", "-c", "cd app; uvicorn main:server --host 0.0.0.0 --port 4355 --workers 4"]
FROM python:3.12-slim

LABEL maintainer="contact@annette-lasar.de"
LABEL version="1.0"
LABEL description="Python 3.12 Slim Debian-based image for Join backend"

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        bash \
        postgresql-client && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x backend.entrypoint.dev.sh backend.entrypoint.prod.sh

EXPOSE 8000
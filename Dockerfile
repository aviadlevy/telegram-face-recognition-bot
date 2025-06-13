FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        libglib2.0-0 \
        libsm6 \
        libxrender1 \
        libxext6 \
        git \
        libjpeg-dev \
        zlib1g-dev \
        libpng-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel

COPY requirements.lock.txt .
RUN pip install -r requirements.lock.txt

COPY . .

# Generate embeddings at build time
RUN python save_embedding.py

CMD ["python", "-u", "bot.py"]

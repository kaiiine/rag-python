# Utilise l'image PyTorch officielle (déjà optimisée)
FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

LABEL maintainer="qtdufour@gmail.com"
LABEL description="RAG (Retrieval Augmented Generation) Application with Python"
LABEL version="1.0"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/app

# PyTorch est déjà installé ! Pas besoin de le réinstaller


RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libpoppler-cpp-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser


WORKDIR $APP_HOME

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p data pdfs embedding_models chrome_langchain_db storage \
    && chown -R appuser:appuser $APP_HOME

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

USER appuser

EXPOSE 4200

CMD ["/app/start.sh"]


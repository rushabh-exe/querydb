FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -U flask-cors

EXPOSE 8000
EXPOSE 5431
EXPOSE 5173
EXPOSE 11434
COPY .env.example .
CMD ["python", "run.py"]
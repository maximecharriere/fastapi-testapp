# Étape 1 : Build (image légère avec Python)
FROM python:3.11 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Étape 2 : Exécution avec image minimale
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local /usr/local
COPY app.py .
EXPOSE 8000
CMD ["fastapi", "run", "app.py"]
FROM python:3.11-slim

# Install Ollama
RUN apt-get update && apt-get install -y curl zstd && \
    curl -fsSL https://ollama.com/install.sh | sh

# Install Python deps
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Start script
COPY start.sh .
RUN chmod +x start.sh

EXPOSE 8501
CMD ["./start.sh"]

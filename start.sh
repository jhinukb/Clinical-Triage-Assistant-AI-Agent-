#!/bin/bash

# Start Ollama in background
ollama serve &

# Wait until Ollama is actually ready (not just started)
echo "Waiting for Ollama to start..."
until curl -s http://localhost:11434/api/tags > /dev/null 2>&1; do
    sleep 2
    echo "Still waiting..."
done

echo "Ollama is ready!"

# Pull the model
ollama pull llama3.2

echo "Model ready! Starting Streamlit..."

# Start Streamlit
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

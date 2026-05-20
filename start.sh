#!/bin/bash
# Start Ollama in background
ollama serve &

# Wait for Ollama to be ready
sleep 5

# Pull the model
ollama pull llama3.2

# Start Streamlit
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
#!/bin/bash
# Startup script to clean corrupted ChromaDB database

echo "Starting ERFDoc application..."
echo "Cleaning up any corrupted ChromaDB data..."

# Remove chroma_db directory if it exists
if [ -d "/app/data/chroma_db" ]; then
    echo "Removing corrupted ChromaDB directory..."
    rm -rf /app/data/chroma_db
    mkdir -p /app/data/chroma_db
    echo "ChromaDB directory cleaned"
fi

# Ensure all required directories exist
mkdir -p /app/data/raw
mkdir -p /app/data/processed
mkdir -p /app/data/chat_history
mkdir -p /app/data/chroma_db

echo "Directories ready. Starting Streamlit..."

# Run the Streamlit app
exec streamlit run app/erfdoc_app.py --server.port=8501 --server.address=0.0.0.0

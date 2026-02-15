# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies with retry logic
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    espeak \
    ffmpeg \
    libespeak1 \
    && rm -rf /var/lib/apt/lists/* || (apt-get update && apt-get install -y --no-install-recommends curl espeak ffmpeg libespeak1 && rm -rf /var/lib/apt/lists/*)

# Install uv - fast Python package installer
RUN pip install --no-cache-dir uv

# Copy requirements first for better caching
COPY requirements.prod.txt requirements.txt ./

# Set UV timeout to 20 minutes for large packages
ENV UV_HTTP_TIMEOUT=1200

# Install PyTorch CPU version first to reduce image size and avoid timeout
RUN uv pip install --system torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu

# Install remaining Python packages using uv
RUN uv pip install --system -r requirements.prod.txt

# Copy configuration files
COPY config.py .

# Create necessary directories
RUN mkdir -p data/raw data/processed data/chroma_db data/chat_history

# Copy application code
COPY app/ ./app/
COPY .streamlit/ ./.streamlit/
COPY ingestion/ ./ingestion/
COPY graph/ ./graph/
COPY utils/ ./utils/
COPY tests/ ./tests/
COPY notebooks/ ./notebooks/
COPY document_intelligence/ ./document_intelligence/
COPY ingest_all.py .
COPY test_part1.py .

# Expose Streamlit default port
EXPOSE 8501

# Set environment variables for Streamlit
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV ANONYMIZED_TELEMETRY=False

# Copy test scripts
COPY test_part1.py .
COPY test_part2.py .
COPY test_part3.py .
COPY test_part4.py .
COPY test_part5.py .
COPY test_part6.py .
COPY test_part7.py .
COPY test_integration.py .
COPY test_cache.py .
COPY demo_cache.py .

# Copy startup script
COPY startup.py .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run startup cleanup and then the application
CMD ["bash", "-c", "python startup.py && streamlit run app/erfdoc_app.py --server.port=8501 --server.address=0.0.0.0"]

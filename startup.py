#!/usr/bin/env python3
"""
Startup script to ensure all required directories exist
ChromaDB data is now persistent - only reset if explicitly requested
"""

from pathlib import Path
import os

def setup_directories():
    """Setup all required directories - DO NOT delete existing data"""
    
    print("=" * 60)
    print("ERFDoc Startup - Directory Setup")
    print("=" * 60)
    
    # Ensure all directories exist (creates if missing, preserves if existing)
    required_dirs = [
        "/app/data/raw",
        "/app/data/processed", 
        "/app/data/chat_history",
        "/app/data/chroma_db",
        "/app/outputs/cache",
        "/app/outputs/chunks",
        "/app/outputs/summaries",
        "/app/outputs/extraction",
        "/app/outputs/evaluation",
        "/app/outputs/reports"
    ]
    
    for dir_path in required_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✓ Directory ready: {dir_path}")
    
    print("✓ All directories configured")
    print("=" * 60)
    print("Starting Streamlit application...\n")

if __name__ == "__main__":
    setup_directories()

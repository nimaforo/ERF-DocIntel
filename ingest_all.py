import os
import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from config import RAW_DATA_DIR, CHROMA_DB_DIR
from ingestion.index import DocumentProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting bulk ingestion...")
    
    # Initialize processor
    processor = DocumentProcessor(
        persist_directory=str(CHROMA_DB_DIR),
        embedding_model="sentence-transformers/all-MiniLM-L6-v2",
        use_openai_embeddings=False
    )
    
    # Get all files
    if not RAW_DATA_DIR.exists():
        logger.error(f"Raw data directory not found: {RAW_DATA_DIR}")
        return

    files = [f for f in RAW_DATA_DIR.iterdir() if f.is_file() and f.name != "README_SAMPLE_DOCS.md"]
    
    logger.info(f"Found {len(files)} files to process")
    
    for i, file_path in enumerate(files, 1):
        try:
            logger.info(f"Processing [{i}/{len(files)}]: {file_path.name}")
            stats = processor.process_single_document(str(file_path))
            logger.info(f"Result: {stats}")
        except Exception as e:
            logger.error(f"Failed to process {file_path.name}: {e}")
            
    logger.info("Ingestion complete!")

if __name__ == "__main__":
    main()

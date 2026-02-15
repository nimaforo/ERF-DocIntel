#!/usr/bin/env python
"""
Simple test to verify system initialization without Streamlit.
This helps diagnose what's failing in the app startup.
"""

import sys
import logging
import traceback
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test all critical imports."""
    logger.info("=" * 60)
    logger.info("Testing Critical Imports")
    logger.info("=" * 60)
    
    try:
        logger.info("Importing ingestion.index...")
        from ingestion.index import DocumentProcessor
        logger.info("  ✓ DocumentProcessor imported")
        
        logger.info("Importing graph.workflow...")
        from graph.workflow import ConversationalAgent
        logger.info("  ✓ ConversationalAgent imported")
        
        logger.info("Importing utils...")
        from utils.translation_service import TranslationService
        logger.info("  ✓ TranslationService imported")
        
        from utils.chat_history import ChatHistoryManager
        logger.info("  ✓ ChatHistoryManager imported")
        
        logger.info("Importing config...")
        from config import DATA_DIR, RAW_DATA_DIR, CHROMA_DB_DIR
        logger.info("  ✓ Config imported")
        
        return True
    except Exception as e:
        logger.error(f"Import failed: {e}", exc_info=True)
        return False


def test_document_processor():
    """Test DocumentProcessor initialization."""
    logger.info("=" * 60)
    logger.info("Testing DocumentProcessor")
    logger.info("=" * 60)
    
    try:
        from config import CHROMA_DB_DIR
        from ingestion.index import DocumentProcessor
        
        logger.info(f"Initializing DocumentProcessor with persist_directory: {CHROMA_DB_DIR}")
        processor = DocumentProcessor(
            persist_directory=str(CHROMA_DB_DIR),
            embedding_model="sentence-transformers/all-MiniLM-L6-v2",
            use_openai_embeddings=False,
        )
        logger.info("  ✓ DocumentProcessor initialized successfully")
        
        logger.info("Getting vector store...")
        vs = processor.get_vector_store()
        logger.info(f"  ✓ Vector store retrieved: {type(vs)}")
        
        return True, processor
    except Exception as e:
        logger.error(f"DocumentProcessor test failed: {e}", exc_info=True)
        return False, None


def test_conversational_agent(processor):
    """Test ConversationalAgent initialization."""
    logger.info("=" * 60)
    logger.info("Testing ConversationalAgent")
    logger.info("=" * 60)
    
    try:
        from graph.workflow import ConversationalAgent
        
        logger.info("Creating ConversationalAgent...")
        agent = ConversationalAgent(processor.get_vector_store(), llm_provider="ollama")
        logger.info("  ✓ ConversationalAgent initialized successfully")
        
        return True
    except Exception as e:
        logger.error(f"ConversationalAgent test failed: {e}", exc_info=True)
        return False


def main():
    """Run all tests."""
    logger.info("Starting initialization tests...")
    
    # Test imports
    if not test_imports():
        logger.error("Import test failed - cannot continue")
        return False
    
    # Test DocumentProcessor
    success, processor = test_document_processor()
    if not success or processor is None:
        logger.error("DocumentProcessor test failed")
        return False
    
    # Test ConversationalAgent
    if not test_conversational_agent(processor):
        logger.error("ConversationalAgent test failed")
        return False
    
    logger.info("=" * 60)
    logger.info("✓ All initialization tests passed!")
    logger.info("=" * 60)
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

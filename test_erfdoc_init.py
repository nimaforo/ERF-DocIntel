#!/usr/bin/env python3
"""Test erfdoc_app initialization without running full Streamlit app."""

import logging
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_erfdoc_initialization():
    """Test erfdoc_app initialization."""
    logger.info("=" * 60)
    logger.info("Testing erfdoc_app Initialization")
    logger.info("=" * 60)
    
    try:
        logger.info("Importing erfdoc_app components...")
        from app.erfdoc_app import initialize_system
        logger.info("✓ erfdoc_app imported successfully")
        
        logger.info("\nTesting system initialization...")
        processor, agent, translation_service, llm_provider, chat_history_manager, smart_translation_handler = initialize_system()
        
        # Check if initialization actually worked
        if processor is None:
            logger.error("✗ FAILED: System initialization returned None values")
            logger.error("This means there was an error during initialization (likely ChromaDB deprecated config)")
            return False
        
        logger.info("✓ System initialized successfully!")
        logger.info(f"  - DocumentProcessor: {type(processor).__name__}")
        logger.info(f"  - ConversationalAgent: {type(agent).__name__}")
        logger.info(f"  - TranslationService: {type(translation_service).__name__}")
        logger.info(f"  - ChatHistoryManager: {type(chat_history_manager).__name__}")
        return True
        
    except Exception as e:
        logger.error(f"✗ Import error: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    logger.info("\n" + "=" * 60)
    logger.info("ERFDOC APP INITIALIZATION TEST")
    logger.info("=" * 60 + "\n")
    
    success = test_erfdoc_initialization()
    
    logger.info("\n" + "=" * 60)
    if success:
        logger.info("✓ ERFDOC APP INITIALIZATION SUCCESSFUL!")
        logger.info("=" * 60)
        sys.exit(0)
    else:
        logger.error("✗ ERFDOC APP INITIALIZATION FAILED")
        logger.error("=" * 60)
        sys.exit(1)

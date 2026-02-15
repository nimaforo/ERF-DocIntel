#!/usr/bin/env python3
"""Test script to verify SimpleEnsembleRetriever.invoke() and get_stats() fixes."""

import logging
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_simple_ensemble_retriever():
    """Test that SimpleEnsembleRetriever has invoke() method."""
    logger.info("=" * 60)
    logger.info("Testing SimpleEnsembleRetriever.invoke() method...")
    logger.info("=" * 60)
    
    try:
        from utils.hybrid_retriever import SimpleEnsembleRetriever
        from langchain_community.retrievers import BM25Retriever
        from langchain_core.documents import Document
        
        # Create test documents
        docs = [
            Document(page_content='Test document about anticheat'),
            Document(page_content='Machine learning concepts'),
            Document(page_content='Software security methods'),
        ]
        
        # Create BM25 retriever
        bm25 = BM25Retriever.from_documents(docs, k=2)
        
        # Create ensemble retriever
        ensemble = SimpleEnsembleRetriever([bm25], [1.0])
        
        # Test invoke() method exists
        if not hasattr(ensemble, 'invoke'):
            logger.error("✗ SimpleEnsembleRetriever.invoke() method NOT FOUND")
            return False
        
        # Test invoke() works
        results = ensemble.invoke('anticheat')
        logger.info(f"✓ SimpleEnsembleRetriever.invoke() works: {len(results)} results")
        
        # Test get_relevant_documents still works
        results2 = ensemble.get_relevant_documents('anticheat')
        logger.info(f"✓ SimpleEnsembleRetriever.get_relevant_documents() works: {len(results2)} results")
        
        logger.info("✓ SimpleEnsembleRetriever tests PASSED")
        return True
        
    except Exception as e:
        logger.error(f"✗ SimpleEnsembleRetriever test FAILED: {e}", exc_info=True)
        return False


def test_get_stats():
    """Test that get_stats() handles ChromaDB errors gracefully."""
    logger.info("=" * 60)
    logger.info("Testing DocumentProcessor.get_stats() error handling...")
    logger.info("=" * 60)
    
    try:
        from ingestion.index import DocumentProcessor
        from config import CHROMA_DB_DIR
        
        # Initialize processor
        processor = DocumentProcessor(persist_directory=str(CHROMA_DB_DIR))
        logger.info("✓ DocumentProcessor initialized")
        
        # Test get_stats() doesn't crash on empty DB
        stats = processor.get_stats()
        logger.info(f"✓ get_stats() returned: {stats}")
        
        # Verify it returns expected keys
        expected_keys = {'total_chunks', 'persist_directory', 'embedding_model'}
        if not all(key in stats for key in expected_keys):
            logger.warning(f"Warning: Missing keys in stats. Got: {stats.keys()}")
        
        # Should not have raised "no such table: collections" error
        if 'error' in stats and 'no such table' in str(stats.get('error', '')):
            logger.error(f"✗ ChromaDB table error still present: {stats['error']}")
            return False
        
        logger.info("✓ get_stats() error handling tests PASSED")
        return True
        
    except Exception as e:
        logger.error(f"✗ get_stats() test FAILED: {e}", exc_info=True)
        return False


def test_hybrid_retriever_integration():
    """Test full HybridRetriever with invoke()."""
    logger.info("=" * 60)
    logger.info("Testing HybridRetriever integration...")
    logger.info("=" * 60)
    
    try:
        from ingestion.index import DocumentProcessor
        from utils.hybrid_retriever import HybridRetriever
        from config import CHROMA_DB_DIR
        
        # Initialize processor
        processor = DocumentProcessor(persist_directory=str(CHROMA_DB_DIR))
        logger.info("✓ DocumentProcessor initialized")
        
        # Create HybridRetriever
        retriever = HybridRetriever(processor.vector_store)
        logger.info("✓ HybridRetriever initialized")
        
        # Test retrieve() which uses invoke()
        results = retriever.retrieve("test query")
        logger.info(f"✓ HybridRetriever.retrieve() works: {len(results)} results")
        
        logger.info("✓ HybridRetriever integration tests PASSED")
        return True
        
    except Exception as e:
        logger.error(f"✗ HybridRetriever integration test FAILED: {e}", exc_info=True)
        return False


def main():
    """Run all tests."""
    logger.info("\n" + "=" * 60)
    logger.info("RUNNING COMPREHENSIVE FIX VERIFICATION TESTS")
    logger.info("=" * 60 + "\n")
    
    results = {
        "SimpleEnsembleRetriever.invoke()": test_simple_ensemble_retriever(),
        "get_stats() error handling": test_get_stats(),
        "HybridRetriever integration": test_hybrid_retriever_integration(),
    }
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("TEST SUMMARY")
    logger.info("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_flag in results.items():
        status = "✓ PASS" if passed_flag else "✗ FAIL"
        logger.info(f"{status}: {test_name}")
    
    logger.info("=" * 60)
    logger.info(f"Results: {passed}/{total} tests passed")
    logger.info("=" * 60 + "\n")
    
    if passed == total:
        logger.info("✓ ALL FIXES VERIFIED SUCCESSFULLY!")
        return 0
    else:
        logger.error(f"✗ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

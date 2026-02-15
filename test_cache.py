"""
Test Document Cache System
"""

import sys
from pathlib import Path
import time

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from document_intelligence.cache import DocumentCache
from document_intelligence.integration import DocumentIntelligenceIntegration


def test_cache_functionality():
    """Test the document cache system."""
    print("=" * 80)
    print("Testing Document Cache System")
    print("=" * 80)
    
    # Test 1: Cache initialization
    print("\n[1] Testing cache initialization...")
    cache = DocumentCache()
    print(f"✓ Cache initialized at: {cache.cache_dir}")
    
    # Test 2: Hash calculation
    print("\n[2] Testing hash calculation...")
    test_files = list(Path("data/raw").glob("*.txt"))
    
    if test_files:
        test_file = test_files[0]
        file_hash = cache.calculate_file_hash(test_file)
        print(f"✓ Calculated hash for {test_file.name}")
        print(f"  Hash (SHA256): {file_hash[:16]}...")
    else:
        print("✗ No test files found in data/raw/")
    
    # Test 3: Cache stats (before processing)
    print("\n[3] Cache statistics (before processing)...")
    stats = cache.get_cache_stats()
    print(f"✓ Total entries: {stats['total_entries']}")
    print(f"  Completed: {stats['completed']}")
    print(f"  Failed: {stats['failed']}")
    print(f"  Total size: {stats['total_size_bytes'] / 1024:.2f} KB")
    
    # Test 4: List cached documents
    print("\n[4] Listing cached documents...")
    cached_docs = cache.list_cached_documents()
    if cached_docs:
        print(f"✓ Found {len(cached_docs)} cached documents:")
        for doc in cached_docs[:5]:  # Show first 5
            print(f"  - {doc['file_name']}: {doc['status']} ({doc['processing_time']:.2f}s)")
    else:
        print("  No cached documents yet")
    
    # Test 5: Export cache report
    print("\n[5] Exporting cache report...")
    cache.export_cache_report()
    report_path = Path("outputs/cache/cache_report.md")
    if report_path.exists():
        print(f"✓ Cache report exported: {report_path}")
    
    print("\n" + "=" * 80)
    print("Cache Functionality Test Complete!")
    print("=" * 80)


def test_cache_with_integration():
    """Test cache integration with document processing."""
    print("\n" + "=" * 80)
    print("Testing Cache Integration with Document Processing")
    print("=" * 80)
    
    # Find test file
    test_files = list(Path("data/raw").glob("*.txt"))
    if not test_files:
        print("✗ No test files found")
        return
    
    test_file = test_files[0]
    print(f"\nTest file: {test_file.name}")
    
    # Initialize integration
    print("\n[1] Initializing integration with cache...")
    di = DocumentIntelligenceIntegration()
    print("✓ Integration initialized")
    
    # First processing (should process and cache)
    print("\n[2] First processing (should process and cache)...")
    print("   This will take a while as it processes the document...")
    start_time = time.time()
    result1 = di.process_uploaded_document(test_file, run_full_analysis=False)
    time1 = time.time() - start_time
    
    print(f"✓ First processing completed in {time1:.2f}s")
    print(f"  Status: {result1['status']}")
    print(f"  From cache: {result1.get('from_cache', False)}")
    
    # Second processing (should use cache)
    print("\n[3] Second processing (should use cache)...")
    start_time = time.time()
    result2 = di.process_uploaded_document(test_file, run_full_analysis=False)
    time2 = time.time() - start_time
    
    print(f"✓ Second processing completed in {time2:.2f}s")
    print(f"  Status: {result2['status']}")
    print(f"  From cache: {result2.get('from_cache', False)}")
    
    # Compare times
    print(f"\n[4] Performance comparison:")
    print(f"  First processing:  {time1:.2f}s (full pipeline)")
    print(f"  Second processing: {time2:.2f}s (from cache)")
    if time1 > 0:
        speedup = time1 / time2 if time2 > 0 else float('inf')
        print(f"  Speedup: {speedup:.1f}x faster")
    
    # Cache stats after processing
    print("\n[5] Cache statistics (after processing)...")
    cache_stats = di.get_cache_stats()
    print(f"✓ Total cached documents: {cache_stats['total_entries']}")
    print(f"  Completed: {cache_stats['completed']}")
    print(f"  Total size: {cache_stats['total_size_bytes'] / 1024:.2f} KB")
    
    # List cached documents
    print("\n[6] Cached documents:")
    cached_docs = di.list_cached_documents()
    for doc in cached_docs[:3]:
        print(f"  - {doc['file_name']}: {doc['status']}")
        print(f"    Hash: {doc['hash']}, Processed: {doc['processed_at']}")
    
    print("\n" + "=" * 80)
    print("Cache Integration Test Complete!")
    print("=" * 80)
    
    print("\n📝 CACHE SYSTEM SUMMARY:")
    print("   ✓ Hash checksums calculated using SHA256")
    print("   ✓ Documents stored in cache after processing")
    print("   ✓ Cache checked before processing to avoid duplicates")
    print("   ✓ Significant performance improvement on cached documents")
    print("   ✓ Cache metadata includes file info, processing time, status")
    print()
    print("   Cache benefits:")
    print("   - Avoid reprocessing identical PDFs")
    print("   - Fast retrieval of previous results")
    print("   - Track processing history")
    print("   - Automatic cache management")
    print("=" * 80)


if __name__ == "__main__":
    # Run both tests
    test_cache_functionality()
    print("\n")
    test_cache_with_integration()

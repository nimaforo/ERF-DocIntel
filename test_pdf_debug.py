#!/usr/bin/env python3
"""
Debug script for testing PDF file loading and processing.
"""

import logging
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from config import RAW_DATA_DIR, PROCESSED_DATA_DIR
from ingestion.index import DocumentProcessor

def test_pdf_loading():
    """Test loading a PDF file."""
    print("=" * 60)
    print("PDF Loading Debug Test")
    print("=" * 60)
    
    # Initialize processor
    processor = DocumentProcessor()
    
    # Find PDF files
    pdf_files = list(RAW_DATA_DIR.glob('*.pdf'))
    
    if not pdf_files:
        print(f"❌ No PDF files found in {RAW_DATA_DIR}")
        return
    
    print(f"\n✓ Found {len(pdf_files)} PDF file(s)")
    
    for pdf_file in pdf_files:
        print(f"\n{'=' * 60}")
        print(f"Testing: {pdf_file.name}")
        print(f"File size: {pdf_file.stat().st_size / 1024:.2f} KB")
        print(f"Full path: {pdf_file}")
        print(f"{'=' * 60}")
        
        try:
            # Try to load the PDF
            print(f"\n1. Loading document...")
            documents = processor.load_document(str(pdf_file))
            print(f"   ✓ Success! Loaded {len(documents)} pages")
            
            if documents:
                print(f"\n2. Content preview:")
                for i, doc in enumerate(documents[:2]):  # Show first 2 pages
                    content_preview = doc.page_content[:200].replace('\n', ' ')
                    print(f"   Page {i+1}: {content_preview}...")
                
                print(f"\n3. Processing document...")
                result = processor.process_single_document(str(pdf_file))
                print(f"   ✓ Processing results:")
                print(f"     - Successful: {result.get('successful')}")
                print(f"     - Failed: {result.get('failed')}")
                print(f"     - Total chunks: {result.get('total_chunks')}")
                
                if result.get('failed_files'):
                    print(f"     - Errors: {result['failed_files']}")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_pdf_loading()

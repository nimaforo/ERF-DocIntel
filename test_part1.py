"""
Test script for Document Intelligence Pipeline - Part 1
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from document_intelligence.pipeline import DocumentIntelligencePipeline
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_part1():
    """Test Part 1: Ingestion & Cleaning"""
    
    print("\n" + "="*70)
    print("TESTING PART 1: DATA INGESTION & CLEANING")
    print("="*70)
    
    # Initialize pipeline
    pipeline = DocumentIntelligencePipeline(output_dir=Path("outputs"))
    
    # Find documents in data/raw/
    data_dir = Path("data/raw")
    
    if not data_dir.exists():
        print(f"\n⚠ Warning: Directory not found: {data_dir}")
        print("Please ensure you have documents in data/raw/")
        return
    
    # Get PDF and DOCX files
    pdf_files = list(data_dir.glob("*.pdf"))
    docx_files = list(data_dir.glob("*.docx"))
    input_files = pdf_files + docx_files
    
    if not input_files:
        print("\n⚠ Warning: No PDF or DOCX files found in data/raw/")
        print("Please add some documents to test the pipeline")
        return
    
    print(f"\nFound {len(input_files)} documents:")
    print(f"  - PDF files: {len(pdf_files)}")
    print(f"  - DOCX files: {len(docx_files)}")
    
    # Limit to first 3 documents for testing
    test_files = input_files[:3]
    print(f"\nProcessing first {len(test_files)} documents for testing...")
    
    for f in test_files:
        print(f"  - {f.name}")
    
    # Run Part 1
    try:
        results = pipeline.run_part1_ingestion(test_files)
        
        print("\n" + "="*70)
        print("RESULTS SUMMARY")
        print("="*70)
        print(f"Total files: {results['total_files']}")
        print(f"Successful: {results['successful']}")
        print(f"Failed: {results['failed']}")
        print(f"Required OCR: {results['required_ocr']}")
        
        print("\n📂 Output Files Generated:")
        output_dir = Path("outputs")
        
        reports = list((output_dir / "reports").glob("*.md"))
        print(f"\n  Reports ({len(reports)}):")
        for report in reports:
            print(f"    ✓ {report.name}")
        
        data_files = list(output_dir.glob("*.json"))
        print(f"\n  Data Files ({len(data_files)}):")
        for data_file in data_files:
            print(f"    ✓ {data_file.name}")
        
        print("\n" + "="*70)
        print("✅ PART 1 TEST COMPLETED SUCCESSFULLY")
        print("="*70)
        
        print("\n💡 Next Steps:")
        print("  1. Review the ingestion_report.md in outputs/reports/")
        print("  2. Check processed_documents.json for structured data")
        print("  3. Proceed to Part 2: Semantic Chunking")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_part1()

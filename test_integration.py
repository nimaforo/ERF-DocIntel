"""
Test the Document Intelligence Integration for ERFDoc
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from document_intelligence.integration import DocumentIntelligenceIntegration, process_pdf


def test_integration():
    """Test the integration layer."""
    print("=" * 80)
    print("Testing Document Intelligence Integration for ERFDoc")
    print("=" * 80)
    
    # Initialize
    print("\n[1] Initializing integration...")
    di = DocumentIntelligenceIntegration()
    print("✓ Integration initialized")
    
    # Check status
    print("\n[2] Checking processing status...")
    status = di.get_processing_status()
    print(f"✓ Pipeline ready: {status['pipeline_ready']}")
    
    print("\n[3] Available outputs:")
    for output_name, available in status['outputs_available'].items():
        symbol = "✓" if available else "✗"
        print(f"  {symbol} {output_name}")
    
    # Check if we have processed data
    if status['outputs_available']['chunks']:
        print("\n[4] Testing chunk retrieval...")
        chunks = di.get_document_chunks()
        print(f"✓ Retrieved {len(chunks)} chunks")
        
        if chunks:
            print(f"\nSample chunk:")
            sample = chunks[0]
            print(f"  Type: {sample.get('type')}")
            print(f"  Tokens: {sample.get('token_count')}")
            print(f"  Content preview: {sample.get('content', '')[:100]}...")
    
    if status['outputs_available']['summaries']:
        print("\n[5] Testing summary retrieval...")
        summary = di.get_document_summary("test_document")
        if summary:
            print(f"✓ Retrieved summary ({len(summary)} chars)")
            print(f"\nSummary preview:")
            print(summary[:200] + "...")
    
    if status['outputs_available']['extractions']:
        print("\n[6] Testing extraction retrieval...")
        for schema_type in ['legal_contract', 'technical_proposal', 'hr_compliance']:
            data = di.get_extracted_data(schema_type)
            if data:
                print(f"✓ Retrieved {schema_type} extraction")
                print(f"  Fields: {len(data.get('extracted_data', {}))}")
                print(f"  Valid: {data.get('validation', {}).get('is_valid', False)}")
    
    if status['outputs_available']['chunks']:
        print("\n[7] Testing chunk search...")
        results = di.search_in_chunks(
            query="resume",
            max_results=3
        )
        print(f"✓ Found {len(results)} matching chunks")
        for i, chunk in enumerate(results, 1):
            print(f"  {i}. Type: {chunk.get('type')}, Tokens: {chunk.get('token_count')}")
    
    print("\n" + "=" * 80)
    print("Integration Test Complete!")
    print("=" * 80)
    
    print("\n📚 INTEGRATION SUMMARY:")
    print("   The Document Intelligence System is now available as a")
    print("   sub-component for ERFDoc's PDF processing pipeline.")
    print()
    print("   Usage in ERFDoc:")
    print("   ------------------")
    print("   from document_intelligence.integration import DocumentIntelligenceIntegration")
    print()
    print("   di = DocumentIntelligenceIntegration()")
    print("   results = di.process_uploaded_document(pdf_path)")
    print("   summary = di.get_document_summary('document.pdf')")
    print("   chunks = di.get_document_chunks()")
    print("   data = di.get_extracted_data('legal_contract')")
    print()
    print("   See: document_intelligence/README.md for full documentation")
    print("=" * 80)


if __name__ == "__main__":
    test_integration()

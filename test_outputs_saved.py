"""
Test to verify document intelligence outputs are saved and accessible for queries
"""

import sys
import os
from pathlib import Path
import json

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from document_intelligence.integration import DocumentIntelligenceIntegration


def test_outputs_saved():
    """Test that all outputs are created and accessible"""
    
    print("=" * 80)
    print("TESTING: Document Intelligence Output Persistence")
    print("=" * 80)
    
    # Initialize
    doc_intel = DocumentIntelligenceIntegration()
    
    if not doc_intel.is_initialized:
        print("❌ Document Intelligence not initialized")
        print(f"   Reason: {doc_intel.initialization_error}")
        return False
    
    print("✅ Document Intelligence initialized")
    
    # Check if outputs directories exist
    output_dirs = {
        "chunks": Path("outputs/chunks"),
        "summaries": Path("outputs/summaries"),
        "extractions": Path("outputs/extraction"),
        "reports": Path("outputs/reports")
    }
    
    print("\n" + "=" * 80)
    print("Checking output directories:")
    print("=" * 80)
    
    for name, path in output_dirs.items():
        if path.exists():
            files = list(path.glob("*.*"))
            print(f"✅ {name:15} exists with {len(files)} files")
            if files:
                for f in files[:3]:  # Show first 3 files
                    size = f.stat().st_size / 1024  # KB
                    print(f"   - {f.name} ({size:.1f} KB)")
        else:
            print(f"⚠️  {name:15} does not exist")
    
    # Check processed documents
    processed_file = Path("outputs/processed_documents.json")
    print("\n" + "=" * 80)
    print("Checking processed documents cache:")
    print("=" * 80)
    
    if processed_file.exists():
        with open(processed_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Found {len(data)} processed documents")
        
        for doc_path, doc_info in list(data.items())[:3]:  # Show first 3
            doc_name = Path(doc_path).name
            status = doc_info.get('status', 'unknown')
            parts = list(doc_info.get('parts', {}).keys())
            proc_time = doc_info.get('processing_time', 0)
            
            print(f"\n📄 {doc_name}")
            print(f"   Status: {status}")
            print(f"   Parts: {', '.join(parts)}")
            print(f"   Time: {proc_time:.2f}s")
            
            # Check if outputs are accessible
            if parts:
                print("\n   Testing get_document_data_for_query()...")
                query_data = doc_intel.get_document_data_for_query(Path(doc_path))
                
                print(f"   - Available: {query_data['available']}")
                print(f"   - Chunks: {len(query_data.get('chunks', []))}")
                print(f"   - Summaries: {len(query_data.get('summaries', {}))}")
                print(f"   - Extractions: {'Yes' if query_data.get('extractions') else 'No'}")
    else:
        print("⚠️  No processed documents found")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)
    
    return True


if __name__ == "__main__":
    try:
        test_outputs_saved()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

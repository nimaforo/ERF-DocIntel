"""
Quick test to verify Document Intelligence integration works correctly
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

def test_integration():
    """Test the document intelligence integration initialization"""
    print("Testing Document Intelligence Integration...")
    
    try:
        from document_intelligence.integration import DocumentIntelligenceIntegration
        print("✓ Import successful")
        
        # Try to initialize
        print("\nInitializing integration...")
        integration = DocumentIntelligenceIntegration()
        print(f"✓ Initialization successful")
        print(f"  - Pipeline initialized: {integration.pipeline is not None}")
        print(f"  - Cache initialized: {integration.cache is not None}")
        print(f"  - Is initialized: {integration.is_initialized}")
        
        # Test cache methods
        print("\nTesting cache methods...")
        cache_stats = integration.get_cache_stats()
        print(f"✓ Cache stats retrieved: {cache_stats}")
        
        # Test status check
        print("\nTesting status check...")
        status = integration.get_processing_status()
        print(f"✓ Status retrieved: {status['pipeline_ready']}")
        
        print("\n✅ All integration tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_integration()
    sys.exit(0 if success else 1)

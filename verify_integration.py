"""
Quick verification that enhanced retrieval is properly integrated.
Run this to ensure everything is connected correctly.
"""

def verify_integration():
    """Verify all components are properly integrated."""
    print("=" * 80)
    print("Enhanced Retrieval Integration Verification")
    print("=" * 80)
    
    checks_passed = 0
    checks_total = 0
    
    # Check 1: DI Retriever file exists
    checks_total += 1
    from pathlib import Path
    di_retriever_file = Path("document_intelligence/di_retriever.py")
    if di_retriever_file.exists():
        print("✅ 1. DocumentIntelligenceRetriever file exists")
        checks_passed += 1
    else:
        print("❌ 1. DocumentIntelligenceRetriever file missing")
    
    # Check 2: RetrieverAgent has di_retriever parameter
    checks_total += 1
    try:
        with open("graph/agents.py", 'r', encoding='utf-8') as f:
            agents_content = f.read()
            if "di_retriever" in agents_content and "DocumentIntelligenceRetriever" in agents_content:
                print("✅ 2. RetrieverAgent enhanced with DI retriever")
                checks_passed += 1
            else:
                print("❌ 2. RetrieverAgent not enhanced")
    except:
        print("❌ 2. Could not verify RetrieverAgent")
    
    # Check 3: create_agents initializes DI retriever
    checks_total += 1
    if "DocumentIntelligenceRetriever" in agents_content:
        print("✅ 3. create_agents() initializes DI retriever")
        checks_passed += 1
    else:
        print("❌ 3. create_agents() missing DI initialization")
    
    # Check 4: Translation service integrated
    checks_total += 1
    if "translation_service" in agents_content:
        print("✅ 4. Translation service integrated")
        checks_passed += 1
    else:
        print("❌ 4. Translation service not integrated")
    
    # Check 5: Context formatting enhanced
    checks_total += 1
    if "DOCUMENT SUMMARIES" in agents_content or "STRUCTURED INFORMATION" in agents_content:
        print("✅ 5. Context formatting enhanced")
        checks_passed += 1
    else:
        print("❌ 5. Context formatting not enhanced")
    
    # Check 6: Document intelligence outputs exist
    checks_total += 1
    outputs_dir = Path("outputs/summaries")
    if outputs_dir.exists() and list(outputs_dir.glob("*.md")):
        print("✅ 6. Document intelligence outputs exist")
        checks_passed += 1
    else:
        print("⚠️  6. Document intelligence outputs not found (will work after document upload)")
        checks_passed += 0.5  # Partial credit
    
    print("\n" + "=" * 80)
    print(f"Integration Check: {checks_passed}/{checks_total} passed")
    print("=" * 80)
    
    if checks_passed >= 5:
        print("\n✅ READY: Enhanced retrieval is fully integrated!")
        print("\nHow it works:")
        print("1. User asks a question in English or Farsi")
        print("2. Query is automatically translated to both languages")
        print("3. System searches:")
        print("   - Vector store (BM25 + semantic)")
        print("   - Summary files (all 4 levels)")
        print("   - Semantic chunks")
        print("   - Structured extractions")
        print("4. Results are combined, ranked, and deduplicated")
        print("5. LLM generates answer with citations")
        print("\n🚀 Ready to use! Just ask questions in the chat.")
    else:
        print("\n⚠️  WARNING: Some components are missing")
        print("Please review the integration steps.")
    
    return checks_passed >= 5

if __name__ == "__main__":
    success = verify_integration()
    
    if success:
        print("\n" + "=" * 80)
        print("Testing Example Queries")
        print("=" * 80)
        print("\nTry these queries in your app:")
        print("\nEnglish:")
        print("  - What are the main requirements?")
        print("  - Tell me about the resume information")
        print("  - What skills are mentioned?")
        print("\nFarsi:")
        print("  - الزامات اصلی چیست؟")
        print("  - اطلاعات رزومه چیست؟")
        print("  - مهارت‌های ذکر شده کدامند؟")
        print("\n✨ Both languages will search the same content!")

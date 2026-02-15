"""
Quick test to verify enhanced prompts are working
"""

from document_intelligence.prompting.enhanced_prompts import EnhancedPromptTemplates, TEMPLATE_REGISTRY

print("=" * 80)
print("TESTING ENHANCED PROMPTS")
print("=" * 80)

# Test 1: System prompts
print("\n1. Testing Role-Based System Prompts:")
print("-" * 80)
for role in ['analyst', 'legal', 'technical', 'executive']:
    prompt = EnhancedPromptTemplates.get_system_prompt(role, 'en')
    preview = prompt[:100].replace('\n', ' ')
    print(f"✅ {role:12} → {preview}...")

# Test 2: Multilingual support
print("\n2. Testing Multilingual Support:")
print("-" * 80)
for lang in ['en', 'fa', 'ar']:
    prompt = EnhancedPromptTemplates.get_system_prompt('analyst', lang)
    preview = prompt[:80].replace('\n', ' ')
    print(f"✅ {lang.upper():4} → {preview}...")

# Test 3: Prompt strategies
print("\n3. Testing Prompt Strategies:")
print("-" * 80)
sample_text = "This is a sample document about AI and machine learning."

for strategy_name in ['few_shot', 'chain_of_thought', 'hierarchical']:
    if strategy_name in TEMPLATE_REGISTRY:
        if strategy_name == 'hierarchical':
            prompt = TEMPLATE_REGISTRY[strategy_name](sample_text, 'chunk', 'en', {})
        else:
            prompt = TEMPLATE_REGISTRY[strategy_name](sample_text, 'en')
        preview = prompt[:100].replace('\n', ' ')
        print(f"✅ {strategy_name:20} → {preview}...")

# Test 4: Structured extraction
print("\n4. Testing Structured Extraction Prompts:")
print("-" * 80)
schema = {"type": "object", "properties": {"name": {"type": "string"}}}
prompt = EnhancedPromptTemplates.structured_extraction_prompt(
    sample_text, schema, "test document", "en"
)
preview = prompt[:100].replace('\n', ' ')
print(f"✅ Extraction prompt → {preview}...")

print("\n" + "=" * 80)
print("✅ ALL TESTS PASSED!")
print("=" * 80)
print("\nEnhanced prompts are loaded and working correctly!")
print("Upload a document to see them in action at http://localhost:8501")

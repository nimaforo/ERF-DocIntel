#!/usr/bin/env python
"""
Comprehensive test to verify the network error fix and agent initialization.
Tests all components of the application to ensure proper setup.
"""

import logging
import os
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def test_environment_variables():
    """Test that all required environment variables are set correctly."""
    logger.info("=" * 60)
    logger.info("Testing Environment Variables")
    logger.info("=" * 60)
    
    from dotenv import load_dotenv
    load_dotenv()
    
    config = {
        "MODEL_PROVIDER": os.getenv("MODEL_PROVIDER", "local"),
        "OLLAMA_BASE_URL": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        "LOCAL_MODEL_NAME": os.getenv("LOCAL_MODEL_NAME", "qwen2.5:7b"),
        "OPENAI_API_KEY": "***" if os.getenv("OPENAI_API_KEY") else "NOT SET",
    }
    
    for key, value in config.items():
        status = "✓" if value != "NOT SET" else "✗"
        logger.info(f"{status} {key}: {value}")
    
    # Validate configuration
    model_provider = config["MODEL_PROVIDER"]
    if model_provider not in ["local", "openai", "anthropic"]:
        logger.error(f"Invalid MODEL_PROVIDER: {model_provider}")
        return False
    
    logger.info("✓ Environment variables validated successfully\n")
    return True


def test_ollama_connectivity():
    """Test connection to Ollama service."""
    logger.info("=" * 60)
    logger.info("Testing Ollama Connectivity")
    logger.info("=" * 60)
    
    import socket
    import time
    
    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    logger.info(f"Testing Ollama at: {ollama_url}")
    
    # Parse URL
    from urllib.parse import urlparse
    parsed = urlparse(ollama_url)
    host = parsed.hostname or "localhost"
    port = parsed.port or 11434
    
    # Test connectivity with retries
    max_retries = 3
    for attempt in range(max_retries):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                logger.info(f"✓ Ollama is accessible at {host}:{port}")
                break
            else:
                logger.warning(f"✗ Connection failed (attempt {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    time.sleep(2)
                else:
                    logger.error(f"✗ Cannot connect to Ollama after {max_retries} attempts")
                    return False
        except Exception as e:
            logger.error(f"✗ Connection error: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                return False
    
    # Test API
    try:
        import requests
        response = requests.get(f"{ollama_url}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            logger.info(f"✓ Ollama API responding with {len(models)} model(s)")
            for model in models:
                logger.info(f"  - {model['name']}")
            return True
        else:
            logger.error(f"✗ Ollama API returned status {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"✗ Failed to query Ollama API: {e}")
        return False


def test_agent_initialization():
    """Test that agents can be initialized properly."""
    logger.info("=" * 60)
    logger.info("Testing Agent Initialization")
    logger.info("=" * 60)
    
    try:
        from ingestion.index import DocumentProcessor
        from graph.agents import create_agents
        from config import get_llm_provider
        
        # Get configured provider
        from dotenv import load_dotenv
        load_dotenv()
        llm_provider = get_llm_provider()
        logger.info(f"Using LLM provider: {llm_provider}")
        
        # Initialize document processor
        logger.info("Initializing DocumentProcessor...")
        processor = DocumentProcessor(persist_directory="./data/chroma_db")
        vector_store = processor.get_vector_store()
        logger.info("✓ DocumentProcessor initialized")
        
        # Initialize agents
        logger.info("Initializing agents...")
        agents = create_agents(vector_store, llm_provider=llm_provider)
        logger.info(f"✓ Agents initialized successfully")
        
        # Verify all agents exist
        required_agents = ["supervisor", "retriever", "reasoning", "utility"]
        for agent_name in required_agents:
            if agent_name in agents:
                logger.info(f"  ✓ {agent_name} agent initialized")
            else:
                logger.error(f"  ✗ {agent_name} agent NOT initialized")
                return False
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Failed to initialize agents: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_workflow_creation():
    """Test that the workflow can be created and invoked."""
    logger.info("=" * 60)
    logger.info("Testing Workflow Creation")
    logger.info("=" * 60)
    
    try:
        from ingestion.index import DocumentProcessor
        from graph.workflow import ConversationalAgent
        from config import get_llm_provider
        from dotenv import load_dotenv
        
        load_dotenv()
        llm_provider = get_llm_provider()
        logger.info(f"Using LLM provider: {llm_provider}")
        
        # Initialize processor
        logger.info("Initializing DocumentProcessor...")
        processor = DocumentProcessor(persist_directory="./data/chroma_db")
        logger.info("✓ DocumentProcessor initialized")
        
        # Create conversational agent
        logger.info("Creating ConversationalAgent...")
        agent = ConversationalAgent(processor.get_vector_store(), llm_provider=llm_provider)
        logger.info("✓ ConversationalAgent created")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Failed to create workflow: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_simple_query():
    """Test a simple query through the workflow."""
    logger.info("=" * 60)
    logger.info("Testing Simple Query")
    logger.info("=" * 60)
    
    try:
        from ingestion.index import DocumentProcessor
        from graph.workflow import ConversationalAgent
        from config import get_llm_provider
        from dotenv import load_dotenv
        
        load_dotenv()
        llm_provider = get_llm_provider()
        logger.info(f"Using LLM provider: {llm_provider}")
        
        # Initialize
        logger.info("Initializing system...")
        processor = DocumentProcessor(persist_directory="./data/chroma_db")
        agent = ConversationalAgent(processor.get_vector_store(), llm_provider=llm_provider)
        
        # Test query
        test_query = "What documents are available?"
        logger.info(f"Sending test query: '{test_query}'")
        
        response = agent.chat(test_query, session_id="test")
        
        if response.get("answer"):
            logger.info("✓ Query processed successfully")
            logger.info(f"Response length: {len(response['answer'])} characters")
            logger.info(f"Query type: {response.get('query_type', 'unknown')}")
            if response.get("error"):
                logger.warning(f"Warning: {response['error']}")
            return True
        else:
            logger.error("✗ No response received")
            if response.get("error"):
                logger.error(f"Error: {response['error']}")
            return False
    
    except Exception as e:
        logger.error(f"✗ Query test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    logger.info("\n" + "=" * 60)
    logger.info("NETWORK ERROR FIX VERIFICATION")
    logger.info("=" * 60 + "\n")
    
    os.chdir(Path(__file__).parent)
    
    tests = [
        ("Environment Variables", test_environment_variables),
        ("Ollama Connectivity", test_ollama_connectivity),
        ("Agent Initialization", test_agent_initialization),
        ("Workflow Creation", test_workflow_creation),
        ("Simple Query", test_simple_query),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            logger.error(f"Test '{test_name}' crashed: {e}")
            results[test_name] = False
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("TEST SUMMARY")
    logger.info("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✓ PASS" if passed_test else "✗ FAIL"
        logger.info(f"{status}: {test_name}")
    
    logger.info(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("\n✓ All tests passed! Your application is configured correctly.")
        return 0
    else:
        logger.error(f"\n✗ {total - passed} test(s) failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

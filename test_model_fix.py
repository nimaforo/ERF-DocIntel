#!/usr/bin/env python
"""Quick test to verify the model name fix works."""

import logging
import os
from pathlib import Path
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

os.chdir(Path(__file__).parent)
load_dotenv()

logger.info("Testing with corrected model name...")
logger.info(f"Configured model: {os.getenv('LOCAL_MODEL_NAME')}")

from ingestion.index import DocumentProcessor
from graph.workflow import ConversationalAgent
from config import get_llm_provider

llm_provider = get_llm_provider()
logger.info(f"Using LLM provider: {llm_provider}")

# Initialize
processor = DocumentProcessor(persist_directory="./data/chroma_db")
agent = ConversationalAgent(processor.get_vector_store(), llm_provider=llm_provider)

# Test query
query = "What are the main topics in the documents?"
logger.info(f"\nTesting query: '{query}'")

response = agent.chat(query, session_id="quick_test")

logger.info(f"\n✓ Response received")
logger.info(f"Answer (first 200 chars): {response['answer'][:200]}...")
logger.info(f"Query type: {response.get('query_type', 'unknown')}")

if response.get("error"):
    logger.error(f"Error: {response['error']}")
else:
    logger.info("✓ Query processed successfully without errors!")

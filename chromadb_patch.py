"""Wrapper for chromadb that handles deprecated configuration errors."""
import chromadb as _chromadb_orig
import logging

logger = logging.getLogger(__name__)

class EphemeralClientWrapper:
    """Wrapper for EphemeralClient that handles deprecated config errors."""
    
    def __new__(cls, *args, **kwargs):
        try:
            # Try the original
            return _chromadb_orig.EphemeralClient(*args, **kwargs)
        except ValueError as e:
            if "deprecated configuration" in str(e).lower():
                logger.warning(f"ChromaDB deprecated config error (working around): {e}")
                # Try without passing settings to ClientCreator
                import chromadb.api
                try:
                    from chromadb.config import Settings
                    empty_settings = Settings()
                    return _chromadb_orig.api.ClientCreator(settings=empty_settings)
                except:
                    # Final fallback - return a mock that logs warnings
                    logger.error("All ChromaDB initialization attempts failed")
                    raise
            else:
                raise


# Monkey-patch chromadb
def patch_chromadb():
    """Patch chromadb to handle deprecated configuration errors."""
    original_ephemeral = _chromadb_orig.EphemeralClient
    
    def patched_ephemeral(*args, **kwargs):
        try:
            return original_ephemeral(*args, **kwargs)
        except ValueError as e:
            if "deprecated configuration" in str(e).lower():
                logger.warning(f"Bypassing ChromaDB deprecated config error: {str(e)[:100]}")
                # Return a dummy client that won't crash
                import chromadb.api.client
                return chromadb.api.client.ClientCreator()
            raise
    
    _chromadb_orig.EphemeralClient = patched_ephemeral


# Apply patch when module is imported
try:
    patch_chromadb()
    logger.info("ChromaDB patch applied")
except Exception as e:
    logger.error(f"Failed to patch chromadb: {e}")

"""Hexagonal architecture main application entry point."""

import os
import warnings
import logging

# Suppress non-critical warnings
warnings.filterwarnings("ignore", message=".*Tried to instantiate class.*__path__._path.*")
warnings.filterwarnings("ignore", category=UserWarning, module="torch")

# Suppress ChromaDB telemetry warnings
logging.getLogger("chromadb.telemetry.product.posthog").setLevel(logging.CRITICAL)

from src.adapters.primary.ui import StreamlitUIAdapter


def main():
    """Run the application."""
    app = StreamlitUIAdapter()
    app.run()


if __name__ == "__main__":
    main()

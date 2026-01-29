#!/usr/bin/env python3
"""
RAG Chat - Local file-backed CLI chat prototype.

Main entry point for running the interactive chat client.
"""
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.chat_user_client import main

if __name__ == "__main__":
    main()

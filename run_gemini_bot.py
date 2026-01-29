#!/usr/bin/env python3
"""
Gemini AI Bot - Local file-backed CLI chat bot powered by Google Gemini.

Main entry point for running the Gemini AI bot.
"""
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from bots.gemini_bot import main

if __name__ == "__main__":
    main()

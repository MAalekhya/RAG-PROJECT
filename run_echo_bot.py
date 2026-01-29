#!/usr/bin/env python3
"""
Echo Bot - Local file-backed CLI chat bot.

Example bot that responds to !echo commands.
Main entry point for running the echo bot.
"""
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from bots.echo_bot import main

if __name__ == "__main__":
    main()

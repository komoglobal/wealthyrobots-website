#!/usr/bin/env python3
"""
Get the complete AGI response with actionable choices
"""

def main():
    print("🚀 Starting AGI Live Chat...")
    print("=" * 80)
    print("Type your question when prompted, then press Enter")
    print("After getting the response, type 'quit' to exit")
    print("=" * 80)
    
    # Import and run the AGI Live Chat
    from agi_live_chat import main as agi_main
    agi_main()

if __name__ == "__main__":
    main()

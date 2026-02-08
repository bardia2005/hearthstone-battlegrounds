import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server.game_server import main

if __name__ == "__main__":
    print("=" * 60)
    print("       HEARTHSTONE - DEDICATED SERVER")
    print("=" * 60)
    print("\nStarting server on 0.0.0.0:8765")
    print("Players can connect using 'localhost:8765'")
    print("Press Ctrl+C to stop\n")
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nServer stopped gracefully")
        sys.exit(0)

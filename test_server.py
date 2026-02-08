import asyncio
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_server():
    """Test server startup"""
    print("Testing server startup...")
    
    try:
        from server.game_server import GameServer
        print("✅ Server module imported successfully")
        
        # Create server instance
        server = GameServer(host="localhost", port=8765)
        print("✅ Server instance created")
        
        print("\n🎉 Server is ready to use!")
        print("\nTo start the server:")
        print("  python start_server.py")
        print("\nOr from the game menu:")
        print("  python main.py → Select 'Start Server'")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\n📦 Please install dependencies:")
        print("  pip install websockets")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_server())
    sys.exit(0 if result else 1)

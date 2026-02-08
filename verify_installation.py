#!/usr/bin/env python3
"""
Comprehensive installation verification script
"""

import sys
import os

def check_python_version():
    """Check Python version"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"  ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  ❌ Python {version.major}.{version.minor}.{version.micro} (need 3.7+)")
        return False

def check_module(module_name, required=True):
    """Check if a module is installed"""
    try:
        __import__(module_name)
        print(f"  ✅ {module_name}")
        return True
    except ImportError:
        if required:
            print(f"  ❌ {module_name} (required)")
        else:
            print(f"  ⚠️  {module_name} (optional - needed for online play)")
        return False

def check_game_files():
    """Check if game files exist"""
    print("\nChecking game files...")
    files = [
        "main.py",
        "hearthstone/game.py",
        "hearthstone/player.py",
        "hearthstone/gui/game_gui.py",
        "server/game_server.py",
        "client/network_client.py"
    ]
    
    all_exist = True
    for file in files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (missing)")
            all_exist = False
    
    return all_exist

def main():
    """Run all checks"""
    print("="*60)
    print("  HEARTHSTONE - INSTALLATION VERIFICATION")
    print("="*60)
    print()
    
    results = []
    
    # Check Python version
    results.append(check_python_version())
    
    # Check required modules
    print("\nChecking required modules...")
    results.append(check_module("pygame", required=True))
    
    # Check optional modules
    print("\nChecking optional modules...")
    websockets_ok = check_module("websockets", required=False)
    
    # Check game files
    results.append(check_game_files())
    
    # Summary
    print("\n" + "="*60)
    print("  SUMMARY")
    print("="*60)
    
    if all(results):
        print("\n✅ All required components are installed!")
        print("\n🎮 You can now:")
        print("  • Play Tutorial: python main.py → Tutorial")
        print("  • Play Local: python main.py → Local Game")
        
        if websockets_ok:
            print("  • Play Online: python main.py → Play Online")
            print("  • Host Server: python start_server.py")
        else:
            print("\n⚠️  Online play disabled (websockets not installed)")
            print("   To enable: pip install websockets")
        
        print("\n📚 Read QUICK_REFERENCE.md for controls")
        print()
        return 0
    else:
        print("\n❌ Some components are missing!")
        print("\n📦 To fix:")
        print("  pip install -r requirements.txt")
        print("\n📚 Read INSTALLATION.md for detailed instructions")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())

# Installation Guide

## Quick Install

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- `pygame` - Game engine
- `websockets` - Online multiplayer support

### Step 2: Verify Installation
```bash
python test_server.py
```

You should see:
```
✅ Server module imported successfully
✅ Server instance created
🎉 Server is ready to use!
```

### Step 3: Start Playing!
```bash
python main.py
```

## Detailed Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Check Python Version
```bash
python --version
```

Should show Python 3.7 or higher.

### Install Dependencies

#### Option 1: Install All (Recommended)
```bash
pip install -r requirements.txt
```

#### Option 2: Install Individually
```bash
pip install pygame
pip install websockets
```

#### Option 3: Local Play Only (No Online)
If you only want to play locally/tutorial mode:
```bash
pip install pygame
```

Online multiplayer will be disabled but local play works fine.

## Troubleshooting

### "pip: command not found"
Try:
```bash
python -m pip install -r requirements.txt
```

### "Permission denied"
Try:
```bash
pip install --user -r requirements.txt
```

Or on Linux/Mac:
```bash
sudo pip install -r requirements.txt
```

### "No module named 'pygame'"
Install pygame:
```bash
pip install pygame
```

### "No module named 'websockets'"
Install websockets:
```bash
pip install websockets
```

### Import Errors
Make sure you're in the Game directory:
```bash
cd Game
python main.py
```

## Platform-Specific Instructions

### Windows

1. **Install Python**
   - Download from python.org
   - Check "Add Python to PATH" during installation

2. **Open Command Prompt**
   - Press Win+R, type `cmd`, press Enter

3. **Navigate to Game folder**
   ```cmd
   cd path\to\Game
   ```

4. **Install dependencies**
   ```cmd
   pip install -r requirements.txt
   ```

5. **Run game**
   ```cmd
   python main.py
   ```

### Mac

1. **Install Python** (if not installed)
   ```bash
   brew install python3
   ```

2. **Open Terminal**
   - Press Cmd+Space, type "Terminal"

3. **Navigate to Game folder**
   ```bash
   cd path/to/Game
   ```

4. **Install dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

5. **Run game**
   ```bash
   python3 main.py
   ```

### Linux

1. **Install Python** (usually pre-installed)
   ```bash
   sudo apt-get install python3 python3-pip
   ```

2. **Navigate to Game folder**
   ```bash
   cd path/to/Game
   ```

3. **Install dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Run game**
   ```bash
   python3 main.py
   ```

## Verification

### Test Local Play
```bash
python main.py
```
- Select "Tutorial" or "Local Game"
- Should work without errors

### Test Server
```bash
python test_server.py
```
- Should show success messages

### Test Online Play
```bash
# Terminal 1: Start server
python start_server.py

# Terminal 2: Connect player
python main.py
# Select "Play Online" → localhost:8765
```

## Common Issues

### Issue: "ModuleNotFoundError: No module named 'websockets'"
**Solution:**
```bash
pip install websockets
```

### Issue: "pygame.error: No available video device"
**Solution:** You're running on a system without a display (like SSH). Use a system with a GUI.

### Issue: "Address already in use"
**Solution:** Port 8765 is in use. Either:
1. Stop the other program using port 8765
2. Change port in `server/game_server.py`

### Issue: Game window doesn't appear
**Solution:**
1. Check if pygame is installed: `pip show pygame`
2. Update pygame: `pip install --upgrade pygame`
3. Check display settings

### Issue: Can't connect to server
**Solution:**
1. Verify server is running
2. Check firewall settings
3. Try `localhost:8765` first
4. Verify websockets is installed

## Updating

### Update All Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Update Specific Package
```bash
pip install --upgrade pygame
pip install --upgrade websockets
```

## Uninstalling

### Remove Dependencies
```bash
pip uninstall pygame websockets
```

### Remove Game
Just delete the Game folder.

## Next Steps

After installation:
1. Read `QUICK_REFERENCE.md` for controls
2. Try Tutorial mode to learn the game
3. Read `ONLINE_MULTIPLAYER_GUIDE.md` for online play
4. Read `SERVER_GUIDE.md` for hosting servers

## Getting Help

If you encounter issues:
1. Check this guide
2. Run `python test_server.py` to diagnose
3. Check Python version: `python --version`
4. Check installed packages: `pip list`
5. Verify you're in the Game directory

## System Requirements

### Minimum
- Python 3.7+
- 512MB RAM
- 100MB disk space
- Display with 1024x768 resolution

### Recommended
- Python 3.9+
- 1GB RAM
- 200MB disk space
- Display with 1920x1080 resolution
- Stable internet connection (for online play)

## Success!

If you see the game menu, you're all set! 🎉

Start with Tutorial mode to learn how to play.

Enjoy! 🎮

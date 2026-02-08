# Quick Reference Card

## 🚀 Quick Start Commands

### Start Server
```bash
python start_server.py
```
Or double-click `start_server.bat` (Windows)

### Start Game
```bash
python main.py
```

## 🎮 Game Modes

| Mode | Description | Command |
|------|-------------|---------|
| Tutorial | Learn to play | Select "Tutorial" in menu |
| Local | Play vs AI | Select "Local Game" in menu |
| Online | Play vs Player | Select "Play Online" in menu |
| Server | Host matches | Select "Start Server" in menu |

## 🌐 Connection Settings

### Local Play
- Host: `localhost`
- Port: `8765`

### Network Play
- Host: `<server-ip>` (e.g., `192.168.1.100`)
- Port: `8765`

## ⌨️ Controls

| Action | Control |
|--------|---------|
| Play Card | Click & Drag to board |
| Attack | Click minion → Click target |
| Hero Power | Click HP button |
| End Turn | Click button or SPACE |
| Cancel | Right Click |
| Toggle Log | TAB |
| Exit | ESC |

## 📋 Server Commands

### Check Server Status
Look for these in server terminal:
- `New connection: <id>` - Player connected
- `Registered player: <name>` - Player registered
- `Match created: <p1> vs <p2>` - Match started
- `Turn ended in match <id>` - Turn changed

### Stop Server
- Press `Ctrl+C` in terminal
- Or close server window

## 🔧 Troubleshooting

### Can't Connect
1. Check server is running
2. Verify IP address and port
3. Try `localhost:8765` first
4. Check firewall settings

### Game Lag
1. Use wired connection
2. Close other applications
3. Play on local network
4. Restart server

### Actions Not Working
1. Check if it's your turn
2. Verify enough mana
3. Ensure valid target
4. Wait for server response

## 📁 Important Files

| File | Purpose |
|------|---------|
| `main.py` | Start game |
| `start_server.py` | Start server |
| `requirements.txt` | Dependencies |
| `SERVER_GUIDE.md` | Server docs |
| `ONLINE_MULTIPLAYER_GUIDE.md` | Player guide |

## 🆘 Getting Help

1. Check `ONLINE_MULTIPLAYER_GUIDE.md`
2. Check `SERVER_GUIDE.md`
3. Look at server logs
4. Verify dependencies installed

## 📦 Installation

```bash
pip install -r requirements.txt
```

## 🎯 Quick Test

```bash
# Terminal 1
python start_server.py

# Terminal 2
python main.py
# → Play Online → localhost:8765

# Terminal 3
python main.py
# → Play Online → localhost:8765

# Match starts automatically!
```

## 📊 System Requirements

- Python 3.7+
- pygame 2.5.0+
- websockets 12.0+
- 512MB RAM
- Stable network connection

## 🔐 Firewall Setup

### Windows
1. Windows Defender Firewall
2. Allow an app
3. Add Python
4. Allow port 8765

### Mac
1. System Preferences
2. Security & Privacy
3. Firewall Options
4. Allow Python

### Linux
```bash
sudo ufw allow 8765
```

## 📞 Support

Check documentation:
- `ONLINE_MULTIPLAYER_GUIDE.md` - Detailed player guide
- `SERVER_GUIDE.md` - Server setup and management
- `MULTIPLAYER_SUMMARY.md` - Technical overview

---

**Happy Gaming! 🎮**

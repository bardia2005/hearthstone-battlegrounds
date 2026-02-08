# Online Multiplayer Guide

## Quick Start

### Playing Online (3 Easy Steps)

1. **Start the Server**
   ```bash
   python start_server.py
   ```
   Or on Windows, double-click `start_server.bat`

2. **Connect Player 1**
   - Run `python main.py`
   - Select "Play Online"
   - Enter username (e.g., "Alice")
   - Enter server: `localhost:8765`
   - Click "Connect"

3. **Connect Player 2**
   - Open another terminal/command prompt
   - Run `python main.py`
   - Select "Play Online"
   - Enter username (e.g., "Bob")
   - Enter server: `localhost:8765`
   - Click "Connect"

**Match starts automatically when 2 players are connected!**

## Detailed Setup

### Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify Installation**
   ```bash
   python -c "import pygame, websockets; print('All dependencies installed!')"
   ```

### Server Setup

#### Option 1: In-Game Server
1. Run `python main.py`
2. Select "Start Server" from menu
3. Server window appears showing status
4. Leave this window open while playing

#### Option 2: Dedicated Server
```bash
python start_server.py
```

The server runs in the terminal and shows:
- Player connections
- Match creation
- Game events
- Errors (if any)

### Network Configuration

#### Playing on Same Computer
- Host: `localhost`
- Port: `8765`
- No additional setup needed

#### Playing on Local Network (LAN)
1. **Find Server IP Address**
   - Windows: Open CMD, type `ipconfig`
   - Mac: Open Terminal, type `ifconfig`
   - Linux: Open Terminal, type `ip addr`
   - Look for IPv4 address (e.g., `192.168.1.100`)

2. **Configure Firewall**
   - Allow incoming connections on port 8765
   - Windows: Windows Defender Firewall → Allow an app
   - Mac: System Preferences → Security & Privacy → Firewall
   - Linux: `sudo ufw allow 8765`

3. **Connect**
   - Server player uses: `localhost:8765`
   - Other players use: `<server-ip>:8765` (e.g., `192.168.1.100:8765`)

#### Playing Over Internet
⚠️ **Advanced Setup Required**
1. Port forward port 8765 on your router
2. Find your public IP address (whatismyip.com)
3. Share public IP with other players
4. They connect to: `<your-public-ip>:8765`

**Security Warning**: Only play with trusted friends. Consider using a VPN service like Hamachi or ZeroTier for safer internet play.

## How to Play Online

### Matchmaking
1. Connect to server
2. Automatically enters matchmaking queue
3. Wait for opponent (usually instant if someone else is waiting)
4. Match starts when 2 players are ready

### During the Match

#### Your Turn
- **Green border** around cards you can play
- **Play cards**: Click and drag to board
- **Attack**: Click your minion, then click target
- **Hero Power**: Click HP button next to your hero
- **End Turn**: Click "End Turn" button or press SPACE

#### Opponent's Turn
- Wait for opponent to finish
- Watch their actions in real-time
- Check game log for details

#### Game Controls
- **Right Click**: Cancel selection
- **SPACE**: End turn
- **ESC**: Exit game (counts as concede)
- **TAB**: Toggle game log

### Winning/Losing
- Reduce opponent's hero to 0 health = Victory
- Your hero reaches 0 health = Defeat
- Opponent disconnects = Victory (after 30 seconds)
- You disconnect = Defeat (after 30 seconds)

## Features

### Real-Time Synchronization
- All actions happen instantly
- Both players see the same game state
- Server validates all moves (no cheating!)

### Disconnection Handling
- 30-second grace period to reconnect
- Opponent notified of disconnection
- Automatic win for remaining player

### Game Log
- All actions recorded
- Visible to both players
- Press TAB to show/hide

## Troubleshooting

### "Failed to connect to server"
**Causes:**
- Server not running
- Wrong IP address or port
- Firewall blocking connection

**Solutions:**
1. Verify server is running (check server window/terminal)
2. Double-check IP address and port
3. Try `localhost:8765` first
4. Disable firewall temporarily to test
5. Check server logs for errors

### "Connection lost during game"
**Causes:**
- Network interruption
- Server crashed
- Firewall blocked connection

**Solutions:**
1. Check network connection
2. Restart server if it crashed
3. Reconnect within 30 seconds
4. If timeout, opponent wins automatically

### "Actions not working"
**Causes:**
- Not your turn
- Not enough mana
- Invalid target
- Server lag

**Solutions:**
1. Check if it's your turn (green indicator)
2. Verify you have enough mana
3. Ensure target is valid (e.g., can't attack stealthed minions)
4. Wait a moment for server response
5. Check server logs for errors

### "Match not starting"
**Causes:**
- Only 1 player connected
- Server error
- Client not in matchmaking

**Solutions:**
1. Ensure 2 players are connected
2. Check server logs
3. Restart both clients
4. Restart server

### "Lag or delay"
**Causes:**
- Slow network connection
- Server overloaded
- High latency

**Solutions:**
1. Use wired connection instead of WiFi
2. Close other network-heavy applications
3. Play on local network instead of internet
4. Restart server

## Advanced Features

### Multiple Matches
- Server supports multiple simultaneous matches
- Each match is independent
- Matchmaking pairs players automatically

### Spectating (Future Feature)
- Not yet implemented
- Planned for future release

### Custom Game Modes (Future Feature)
- Not yet implemented
- Planned for future release

## Technical Details

### Network Protocol
- WebSocket-based communication
- JSON message format
- Server-authoritative architecture

### Message Flow
```
Client → Server: play_card
Server validates action
Server updates game state
Server → Both Clients: game_state update
```

### Security
- Server validates all actions
- Clients cannot cheat
- Game logic runs on server
- Clients only display state

### Performance
- Low bandwidth usage (~10KB/s per match)
- Minimal latency (<50ms on LAN)
- Supports 100+ concurrent players

## Best Practices

### For Smooth Gameplay
1. Use wired internet connection
2. Close unnecessary applications
3. Play on local network when possible
4. Keep server running on stable computer

### For Hosting
1. Use dedicated server mode
2. Keep server terminal visible for monitoring
3. Check logs regularly
4. Restart server if issues occur

### For Playing
1. Test connection with localhost first
2. Communicate with opponent (voice chat, etc.)
3. Be patient with network delays
4. Report bugs or issues

## FAQ

**Q: Can I play with friends over the internet?**
A: Yes, but requires port forwarding or VPN. Local network is easier.

**Q: How many players can connect?**
A: Server supports 100+ players, but matches are 1v1.

**Q: Can I save and resume games?**
A: Not currently. Games must be completed in one session.

**Q: What happens if I disconnect?**
A: You have 30 seconds to reconnect, otherwise you lose.

**Q: Can I spectate matches?**
A: Not yet, planned for future release.

**Q: Is there ranked matchmaking?**
A: Not yet, currently first-come first-served.

**Q: Can I use custom decks?**
A: Currently uses starter decks. Custom decks planned for future.

**Q: Is there a chat system?**
A: Not yet, use external voice/text chat for now.

**Q: Can I play against AI online?**
A: No, online mode is player vs player only.

**Q: What if server crashes during game?**
A: Game ends, both players disconnected. Restart server and reconnect.

## Getting Help

### Check Logs
- Server logs show all events
- Client shows connection status
- Look for error messages

### Common Error Codes
- `INVALID_JSON`: Corrupted message, restart client
- `NOT_YOUR_TURN`: Wait for your turn
- `ALREADY_IN_MATCH`: Already in a game
- `ACTION_FAILED`: Invalid action, check requirements

### Reporting Issues
When reporting issues, include:
1. What you were trying to do
2. What happened instead
3. Error messages (if any)
4. Server logs
5. Steps to reproduce

## Next Steps

1. **Try Local Play First**
   - Test with localhost
   - Learn the controls
   - Practice gameplay

2. **Play on LAN**
   - Set up local network play
   - Invite friends on same network
   - Test stability

3. **Advanced Setup**
   - Configure port forwarding
   - Set up VPN for internet play
   - Host tournaments

Enjoy playing Hearthstone online! 🎮

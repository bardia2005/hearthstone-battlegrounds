# Hearthstone Server Guide

## Overview
The Hearthstone server enables online multiplayer matches between players. It handles matchmaking, game state synchronization, and turn management.

## Installation

### Requirements
```bash
pip install -r requirements.txt
```

This will install:
- `pygame` - For the game client
- `websockets` - For server/client communication

## Starting the Server

### Method 1: From the Game Menu
1. Run `python main.py`
2. Select "Start Server" from the main menu
3. The server will start on `0.0.0.0:8765`
4. A server status window will appear

### Method 2: Standalone Server
```bash
python server/game_server.py
```

The server will start on `0.0.0.0:8765` by default.

## Connecting to the Server

### Local Connection (Same Computer)
- Host: `localhost`
- Port: `8765`

### Network Connection (Different Computers)
1. Find the server's IP address:
   - Windows: `ipconfig` (look for IPv4 Address)
   - Mac/Linux: `ifconfig` or `ip addr`
2. Use that IP address as the host
3. Port: `8765`
4. Make sure firewall allows port 8765

### From the Game Menu
1. Run `python main.py`
2. Select "Play Online"
3. Enter your username
4. Enter server address (e.g., `localhost:8765` or `192.168.1.100:8765`)
5. Click "Connect"

## Server Features

### Matchmaking
- Automatic matchmaking when 2+ players are in queue
- First-come, first-served matching
- Players can cancel matchmaking before match starts

### Game State Synchronization
- Real-time game state updates
- Server-authoritative game logic
- Prevents cheating by validating all actions

### Turn Management
- Enforces turn order
- Validates actions (only current player can act)
- Automatic turn switching

### Disconnection Handling
- 30-second grace period for reconnection
- Opponent notified of disconnection
- Automatic win for remaining player after timeout

## Server Architecture

### Components

1. **GameServer** (`server/game_server.py`)
   - Main server class
   - Handles WebSocket connections
   - Manages matchmaking queue
   - Coordinates matches

2. **Match**
   - Represents an active game between two players
   - Contains the actual Game instance
   - Manages game state serialization

3. **Player**
   - Represents a connected player
   - Tracks connection status
   - Links to WebSocket connection

### Message Types

#### Client → Server
- `register` - Register username
- `find_match` - Join matchmaking queue
- `cancel_matchmaking` - Leave matchmaking queue
- `play_card` - Play a card from hand
- `attack` - Attack with a minion
- `hero_power` - Use hero power
- `end_turn` - End current turn
- `concede` - Concede the game
- `ping` - Keep-alive ping

#### Server → Client
- `connected` - Connection confirmation
- `registered` - Registration confirmation
- `matchmaking` - Matchmaking status update
- `match_found` - Match has been found
- `game_state` - Current game state
- `your_turn` - It's your turn notification
- `action_success` - Action was successful
- `game_over` - Game has ended
- `opponent_disconnected` - Opponent disconnected
- `error` - Error message

### Game State Format

```json
{
  "turn": 5,
  "your_turn": true,
  "player": {
    "name": "Player1",
    "health": 25,
    "armor": 0,
    "mana": 5,
    "max_mana": 5,
    "deck_size": 20,
    "hand": [
      {
        "name": "Fireball",
        "mana_cost": 4,
        "type": "spell",
        "description": "Deal 6 damage"
      }
    ],
    "board": [
      {
        "name": "Chillwind Yeti",
        "attack": 4,
        "health": 5,
        "can_attack": true,
        "taunt": false
      }
    ],
    "hero_power_used": false
  },
  "opponent": {
    "name": "Player2",
    "health": 30,
    "armor": 0,
    "mana": 5,
    "max_mana": 5,
    "deck_size": 22,
    "hand_size": 6,
    "board": [],
    "hero_power_used": false
  },
  "game_log": [
    "Player1 plays Chillwind Yeti",
    "Player2 ends turn"
  ]
}
```

## Troubleshooting

### Server won't start
- Check if port 8765 is already in use
- Try a different port by modifying `game_server.py`
- Check firewall settings

### Can't connect to server
- Verify server is running
- Check IP address and port
- Ensure firewall allows connections on port 8765
- Try `localhost` first for local testing

### Connection drops during game
- Check network stability
- Server has 30-second grace period for reconnection
- If disconnected, opponent wins automatically

### Actions not working
- Ensure it's your turn
- Check if you have enough mana
- Verify target is valid
- Check server logs for errors

## Server Logs

The server logs important events:
- Player connections/disconnections
- Match creation
- Turn changes
- Errors

Check console output for debugging.

## Performance

### Recommended Specs
- CPU: Any modern processor
- RAM: 512MB minimum
- Network: Stable internet connection
- Bandwidth: ~10KB/s per active match

### Capacity
- Tested with up to 100 concurrent players
- Each match uses minimal resources
- Can run on modest hardware

## Security Notes

- Server validates all game actions
- Client cannot cheat by modifying local state
- All game logic runs on server
- WebSocket connections are not encrypted by default
  - For production, use WSS (WebSocket Secure)

## Development

### Adding New Features

1. **New Action Type**
   - Add handler in `GameServer.handle_message()`
   - Implement action logic
   - Update game state
   - Broadcast to clients

2. **New Message Type**
   - Define message format
   - Add to server/client protocol
   - Update documentation

### Testing

```bash
# Start server
python server/game_server.py

# In another terminal, start client 1
python main.py
# Select "Play Online", connect to localhost:8765

# In another terminal, start client 2
python main.py
# Select "Play Online", connect to localhost:8765

# Match should start automatically
```

## Future Enhancements

- [ ] Ranked matchmaking
- [ ] Friend system
- [ ] Spectator mode
- [ ] Replay system
- [ ] Chat system
- [ ] Tournament mode
- [ ] Custom game modes
- [ ] Deck builder integration
- [ ] Statistics tracking
- [ ] Leaderboards

## Support

For issues or questions:
1. Check this guide
2. Review server logs
3. Test with local connection first
4. Verify all dependencies are installed

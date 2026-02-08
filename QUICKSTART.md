# Quick Start Guide

## Installation

1. **Install Python 3.8+** (if not already installed)

2. **Install dependencies:**
```bash
pip install pygame websockets numpy
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

## Running the Game

Simply run:
```bash
python main.py
```

## Main Menu

When you start the game, you'll see a beautiful main menu with four options:

### 🎮 Play Local
- Click "Play Local"
- Enter names for Player 1 and Player 2
- Click "Start Game"
- Play hot-seat multiplayer on the same computer
- Take turns playing cards and attacking

### 🌐 Play Online
- First, someone needs to host a server (see "Host Server" below)
- Click "Play Online"
- Enter your username
- Enter server address (e.g., "localhost:8765" or "192.168.1.100:8765")
- Click "Connect"
- Wait for matchmaking to find an opponent
- Play against a real player over the network!

### 🖥️ Host Server
- Click "Host Server"
- Server starts on port 8765
- Share your IP address with friends
- They can connect using "your-ip:8765"
- A server status window will appear
- Close the window to stop the server

### ❌ Quit
- Exit the game

## Sound Effects

The game includes procedurally generated sound effects:
- **Button Hover** - Soft tick when hovering over buttons
- **Button Click** - Beep when clicking buttons
- **Card Play** - Whoosh sound when playing cards
- **Card Draw** - Swish sound when drawing cards
- **Attack** - Impact sound when minions attack
- **End Turn** - Pleasant chime when ending turn
- **Victory** - Ascending fanfare when you win
- **Defeat** - Descending tones when you lose
- **Error** - Buzz sound for invalid actions

## Game Controls

### Mouse Controls
- **Left-click card** - Select card from hand
- **Drag card to board** - Play minion card
- **Drag card to target** - Play spell with target
- **Click minion** - Select for attack
- **Click target** - Attack with selected minion
- **Right-click** - Cancel selection
- **Click "End Turn"** - End your turn
- **Click "HP"** - Use hero power (costs 2 mana)

### Keyboard Shortcuts
- **ESC** - Cancel action / Return to menu
- **Space** - End turn
- **Tab** - Toggle game log

## Tips for New Players

1. **Mana Management** - You gain 1 mana crystal each turn (max 10)
2. **Card Advantage** - Drawing cards is important
3. **Board Control** - Control the board with minions
4. **Taunt** - Taunt minions must be attacked first
5. **Divine Shield** - Blocks one instance of damage
6. **Charge** - Can attack immediately when played
7. **Hero Power** - Use it every turn if you can afford it

## Troubleshooting

### No Sound
- Make sure your system volume is up
- Check that pygame.mixer initialized correctly
- Sound is generated procedurally, no external files needed

### Connection Failed (Online Mode)
- Make sure the server is running first
- Check the server address is correct
- Ensure port 8765 is not blocked by firewall
- Try "localhost:8765" if playing on same computer

### Game Crashes
- Make sure all dependencies are installed
- Check Python version is 3.8 or higher
- Try reinstalling pygame: `pip install --upgrade pygame`

## Playing Over Network

### Host (Server)
1. Run the game and click "Host Server"
2. Find your IP address:
   - Windows: `ipconfig` in Command Prompt
   - Mac/Linux: `ifconfig` or `ip addr`
3. Share your IP with friends (e.g., "192.168.1.100")

### Client (Player)
1. Run the game and click "Play Online"
2. Enter your username
3. Enter host's IP address with port (e.g., "192.168.1.100:8765")
4. Click "Connect"
5. Wait for matchmaking

## Have Fun!

Enjoy playing Hearthstone - Python Edition! 🎮✨

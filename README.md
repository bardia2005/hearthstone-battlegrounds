# Hearthstone - Python Edition

A fully-featured Hearthstone card game implementation in Python with both local and online multiplayer support.

## Features

### Core Gameplay
- ✅ Complete card game mechanics (minions, spells, weapons)
- ✅ Mana system (1-10 crystals per turn)
- ✅ 30-card decks with shuffling
- ✅ Hand management (max 10 cards)
- ✅ Board with up to 7 minions per side
- ✅ Hero health, armor, and weapons
- ✅ Hero powers (2 mana cost)

### Card Mechanics
- ✅ **Taunt** - Must be attacked first
- ✅ **Charge** - Can attack immediately
- ✅ **Divine Shield** - Absorbs one hit
- ✅ **Windfury** - Can attack twice per turn
- ✅ **Stealth** - Cannot be targeted
- ✅ **Poisonous** - Destroys any minion it damages
- ✅ **Lifesteal** - Heals hero for damage dealt
- ✅ **Battlecry** - Effect when played
- ✅ **Deathrattle** - Effect when dies
- ✅ **Silence** - Remove all card text

### Card Collection
- 50+ unique cards including:
  - Basic minions (Wisp, Yeti, Ogre, etc.)
  - Special ability minions (Charge, Taunt, Divine Shield)
  - Legendary minions (Ragnaros, Sylvanas, Tirion, etc.)
  - Spells (Fireball, Polymorph, Flamestrike, etc.)
  - Weapons (Fiery War Axe, Truesilver Champion, etc.)

### Multiplayer
- ✅ **Local Play** - Hot-seat multiplayer on same computer
- ✅ **Online Play** - WebSocket-based multiplayer
- ✅ **Matchmaking** - Automatic player pairing
- ✅ **Dedicated Server** - Host your own game server

### Graphics & UI
- ✅ Beautiful card rendering with stats
- ✅ Drag-and-drop card playing
- ✅ Visual targeting system
- ✅ Animated combat
- ✅ Game log panel
- ✅ Turn indicators
- ✅ Mana crystal display
- ✅ Hero portraits with health/armor

## Installation

1. Install Python 3.8 or higher
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Game

Simply run:
```bash
python main.py
```

This will open the main menu where you can:
- **Play Local** - Start a local game (hot-seat multiplayer)
- **Play Online** - Connect to a server for online multiplayer
- **Host Server** - Start a dedicated server for others to join
- **Quit** - Exit the game

### Main Menu Options

#### Play Local
1. Click "Play Local"
2. Enter names for Player 1 and Player 2
3. Click "Start Game"
4. Play on the same computer, taking turns

#### Play Online
1. Click "Play Online"
2. Enter your username
3. Enter server address (default: localhost:8765)
4. Click "Connect"
5. Wait for matchmaking to find an opponent
6. Play against a real player over the network

#### Host Server
1. Click "Host Server"
2. Server starts on port 8765
3. Share your IP address with friends
4. They can connect using "your-ip:8765"
5. Close the server window to stop

### No Terminal Required!
Everything is done through the graphical interface - no command-line arguments needed.

## Controls

### Mouse Controls
- **Left-click card** - Select card from hand
- **Drag card to board** - Play minion card
- **Drag card to target** - Play spell with target
- **Click minion** - Select for attack
- **Click target** - Attack with selected minion
- **Right-click** - Cancel selection
- **Click "End Turn"** - End your turn
- **Click "HP"** - Use hero power

### Keyboard Shortcuts
- **ESC** - Cancel action
- **Space** - End turn
- **Tab** - Toggle game log

## Game Rules

### Turn Structure
1. Draw a card
2. Gain 1 mana crystal (max 10)
3. Play cards and attack
4. End turn

### Card Costs
- **Minions**: 3 gold to buy from shop
- **Hero Power**: 2 mana
- **Refresh Shop**: 1 gold
- **Upgrade Tavern**: 5-7 gold

### Combat
- Minions can attack once per turn (twice with Windfury)
- Newly played minions have summoning sickness (except Charge)
- Taunt minions must be attacked first
- Divine Shield blocks one instance of damage
- Poisonous minions destroy any minion they damage

### Win Conditions
- Reduce opponent's health to 0
- Opponent runs out of cards (fatigue damage)
- Opponent concedes

## Architecture

### Project Structure
```
Game/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── README.md              # This file
├── hearthstone/           # Core game logic
│   ├── card.py           # Card classes
│   ├── minion.py         # Minion on board
│   ├── spell.py          # Spell cards
│   ├── player.py         # Player state
│   ├── game.py           # Game logic
│   ├── cards_collection.py  # All cards
│   └── gui/              # Graphics
│       ├── game_gui.py   # Main GUI
│       ├── card_renderer.py  # Card rendering
│       └── colors.py     # Color palette
├── server/               # Multiplayer server
│   └── game_server.py    # WebSocket server
├── client/               # Network client
│   └── network_client.py # WebSocket client
└── data/                 # Mock data for testing
    └── *.json           # Test scenarios
```

### Network Protocol
The game uses WebSocket for real-time communication:

**Client → Server:**
- `register` - Register username
- `find_match` - Join matchmaking queue
- `game_action` - Play card, attack, etc.
- `end_turn` - End current turn
- `concede` - Forfeit game

**Server → Client:**
- `connected` - Connection established
- `match_found` - Match created
- `game_state` - Current game state
- `your_turn` - Turn notification
- `game_over` - Game ended

## Development

### Adding New Cards
Edit `hearthstone/cards_collection.py`:

```python
def my_battlecry(owner, game, target):
    # Your effect here
    game.add_log("Effect triggered!")

new_card = MinionCard(
    "My Minion", 
    mana_cost=3, 
    attack=3, 
    health=4,
    battlecry=my_battlecry
)
```

### Testing Offline
Use mock JSON files in `data/` directory for testing without a server.

## Credits

Inspired by Blizzard Entertainment's Hearthstone.
This is a fan-made educational project.

## License

MIT License - See LICENSE file for details

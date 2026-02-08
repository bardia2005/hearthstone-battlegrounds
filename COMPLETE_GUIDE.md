# Hearthstone - Python Edition: Complete Guide

## 🎮 Getting Started

### Installation (3 Simple Steps)

1. **Install Python 3.8+**
   - Download from [python.org](https://python.org)
   - Make sure to check "Add Python to PATH"

2. **Install Dependencies**
   ```bash
   pip install pygame websockets numpy
   ```

3. **Run the Game**
   ```bash
   python main.py
   ```

## 📋 Main Menu Options

When you launch the game, you'll see 5 options:

### 1. 🎓 Tutorial (RECOMMENDED FOR NEW PLAYERS)
- **What:** Interactive 17-step tutorial
- **Duration:** 5-10 minutes
- **Learn:** All game mechanics with hands-on practice
- **Perfect for:** First-time players
- **Features:**
  - Highlighted UI elements
  - Animated arrows pointing to actions
  - Auto-advance when you complete tasks
  - Skip anytime with ESC

### 2. 🎮 Play Local
- **What:** Hot-seat multiplayer on same computer
- **Players:** 2 (taking turns)
- **Setup:**
  1. Click "Play Local"
  2. Enter Player 1 name
  3. Enter Player 2 name
  4. Click "Start Game"
- **Perfect for:** Playing with friends/family

### 3. 🌐 Play Online
- **What:** Multiplayer over internet
- **Players:** 2 (real-time)
- **Requirements:** Server must be running
- **Setup:**
  1. Someone hosts a server (see option 4)
  2. Click "Play Online"
  3. Enter your username
  4. Enter server address (e.g., "192.168.1.100:8765")
  5. Click "Connect"
  6. Wait for matchmaking
- **Perfect for:** Playing with friends online

### 4. 🖥️ Host Server
- **What:** Dedicated game server
- **Purpose:** Let others connect to you
- **Setup:**
  1. Click "Host Server"
  2. Server starts on port 8765
  3. Find your IP address:
     - Windows: `ipconfig` in CMD
     - Mac/Linux: `ifconfig` or `ip addr`
  4. Share IP with friends (e.g., "192.168.1.100:8765")
- **Perfect for:** Hosting games for friends

### 5. ❌ Quit
- Exit the game

## 🎯 Game Objective

**WIN:** Reduce your opponent's hero to 0 health
**LOSE:** Your hero reaches 0 health

## 🎴 Game Basics

### The Board Layout

```
┌─────────────────────────────────────────┐
│         OPPONENT'S HERO (30 HP)         │
│              [Game Log]                 │
├─────────────────────────────────────────┤
│      OPPONENT'S BOARD (7 minions)       │
├─────────────────────────────────────────┤
│         ═══ CENTER LINE ═══             │
├─────────────────────────────────────────┤
│       YOUR BOARD (7 minions)            │
├─────────────────────────────────────────┤
│          YOUR HERO (30 HP)              │
│         [Hero Power] [End Turn]         │
├─────────────────────────────────────────┤
│         YOUR HAND (10 cards)            │
│         [Mana Crystals: ●●●○○]          │
└─────────────────────────────────────────┘
```

### Turn Structure

Each turn follows this sequence:

1. **Start of Turn**
   - Gain 1 mana crystal (max 10)
   - Refresh all mana
   - Draw 1 card
   - Minions wake up (can attack)

2. **Main Phase** (Your Actions)
   - Play cards from hand
   - Attack with minions
   - Use hero power (once per turn)
   - Use weapon (if equipped)

3. **End Turn**
   - Click "End Turn" button
   - Opponent's turn begins

## 💎 Mana System

- **Start:** 0 mana crystals
- **Each Turn:** +1 crystal (max 10)
- **Usage:** Spend to play cards
- **Refresh:** Full mana at turn start
- **Display:** Blue = available, Gray = used

**Example:**
- Turn 1: 1 mana (play 1-cost cards)
- Turn 5: 5 mana (play 5-cost card or multiple small cards)
- Turn 10+: 10 mana (maximum)

## 🃏 Card Types

### 1. Minion Cards
- **Stay on board** after played
- **Attack** and **Health** stats
- **Can attack** enemy minions or hero
- **Max 7** on board at once

**Example:** Chillwind Yeti (4 mana, 4/5)
- Costs 4 mana
- 4 attack, 5 health
- Stays on board until killed

### 2. Spell Cards
- **One-time effect** when played
- **Removed** after use
- **Various effects:** damage, draw, buff, etc.

**Example:** Fireball (4 mana)
- Costs 4 mana
- Deal 6 damage to any target
- Card is discarded after use

### 3. Weapon Cards
- **Equips** to your hero
- **Hero can attack** with it
- **Durability:** loses 1 per attack
- **Breaks** at 0 durability

**Example:** Fiery War Axe (3 mana, 3/2)
- Costs 3 mana
- 3 attack, 2 durability
- Hero attacks twice before breaking

## ⚔️ Combat System

### Attacking with Minions

1. **Click** your minion
2. **Click** target (enemy minion or hero)
3. **Both** take damage simultaneously
4. **Dead** minions are removed

**Example Combat:**
- Your 4/3 minion attacks enemy 2/5 minion
- Enemy takes 4 damage (becomes 2/1)
- Your minion takes 2 damage (becomes 4/1)
- Both survive

### Attacking with Hero

1. **Equip** a weapon
2. **Click** your hero
3. **Click** target
4. **Hero** takes damage back from minions
5. **Weapon** loses 1 durability

### Summoning Sickness

- **New minions** can't attack (shown with "Z")
- **Exception:** Charge minions attack immediately
- **Wakes up:** Next turn

## 🌟 Special Abilities

### Taunt
- **Symbol:** Gray border glow
- **Effect:** Must be attacked before other minions
- **Strategy:** Protects your hero and other minions

### Charge
- **Symbol:** Lightning bolt
- **Effect:** Can attack immediately when played
- **Strategy:** Surprise attacks, finishing blows

### Divine Shield
- **Symbol:** "DS" badge
- **Effect:** Blocks first instance of damage
- **Strategy:** Protects valuable minions

### Windfury
- **Symbol:** "W" badge
- **Effect:** Can attack twice per turn
- **Strategy:** Double damage output

### Stealth
- **Symbol:** "S" badge
- **Effect:** Cannot be targeted by spells/attacks
- **Breaks:** When minion attacks
- **Strategy:** Safe setup for combos

### Poisonous
- **Symbol:** "P" badge
- **Effect:** Destroys any minion it damages
- **Strategy:** Kill large minions with small ones

### Lifesteal
- **Effect:** Heals your hero for damage dealt
- **Strategy:** Sustain and survival

### Battlecry
- **Trigger:** When played from hand
- **Effect:** Varies by card
- **Examples:** Deal damage, draw cards, buff minions

### Deathrattle
- **Trigger:** When minion dies
- **Effect:** Varies by card
- **Examples:** Summon minions, draw cards, damage

### Silence
- **Effect:** Removes all card text and buffs
- **Removes:** All abilities, buffs, debuffs
- **Keeps:** Base attack/health

## 🎮 Controls

### Mouse Controls
| Action | Control |
|--------|---------|
| Select card | Left-click card in hand |
| Play minion | Drag card to board |
| Play spell | Drag card to target |
| Select minion | Left-click your minion |
| Attack | Click target after selecting |
| Cancel | Right-click |
| End turn | Click "End Turn" button |
| Hero power | Click "HP" button |

### Keyboard Shortcuts
| Key | Action |
|-----|--------|
| Space | End turn |
| Tab | Toggle game log |
| ESC | Cancel action / Exit |

## 📊 Game Interface

### Top Section
- **Opponent's Hero:** Health, armor, hero power status
- **Opponent's Board:** Their minions
- **Game Log:** All actions recorded (right side)

### Middle Section
- **Center Line:** Divides the battlefield
- **Your Board:** Your minions

### Bottom Section
- **Your Hero:** Health, armor, hero power
- **Your Hand:** Cards you can play
- **Mana Crystals:** Available resources
- **End Turn Button:** Pass your turn

## 🎯 Strategy Tips

### Beginner Tips

1. **Mana Efficiency**
   - Use all your mana each turn
   - Don't waste resources
   - Plan ahead for expensive cards

2. **Board Control**
   - Keep minions alive
   - Remove enemy threats
   - Control the battlefield

3. **Card Advantage**
   - More cards = more options
   - Draw cards when possible
   - Don't overextend

4. **Health Management**
   - Health is a resource
   - Trading health for advantage is OK
   - Win at 1 HP or 30 HP

5. **Tempo**
   - Play on curve (use all mana)
   - Pressure opponent
   - Don't fall behind

### Intermediate Tips

1. **Trading**
   - Favorable trades (kill big with small)
   - Protect valuable minions
   - Use Taunt effectively

2. **Spell Timing**
   - Save removal for threats
   - Don't waste spells
   - Combo potential

3. **Hero Power**
   - Use it every turn if possible
   - 2 mana for value
   - Don't forget it!

4. **Positioning**
   - Taunt minions protect others
   - Spread damage
   - Plan attacks

### Advanced Tips

1. **Lethal Calculation**
   - Count damage for win
   - Plan multiple turns ahead
   - Don't miss lethal!

2. **Resource Management**
   - Cards in hand
   - Cards in deck
   - Health total

3. **Opponent's Options**
   - What can they do?
   - Play around threats
   - Bait removal

4. **Win Conditions**
   - How will you win?
   - Adapt strategy
   - Multiple paths to victory

## 🔊 Sound Effects

The game features procedurally generated sounds:

| Sound | When |
|-------|------|
| Button Hover | Mouse over buttons |
| Button Click | Click buttons |
| Card Play | Play a card |
| Card Draw | Draw a card |
| Attack | Minion attacks |
| Error | Invalid action |
| End Turn | Turn ends |
| Chime | Hero power, special events |
| Victory | You win! |
| Defeat | You lose |

**Volume Control:** Sounds are at 50% by default

## 🐛 Troubleshooting

### Game Won't Start
- Check Python version: `python --version` (need 3.8+)
- Install dependencies: `pip install -r requirements.txt`
- Try: `python3 main.py` instead of `python main.py`

### No Sound
- Check system volume
- Pygame mixer should auto-initialize
- Sounds are generated, no files needed

### Connection Failed (Online)
- Server must be running first
- Check server address is correct
- Port 8765 must be open
- Try "localhost:8765" for same computer

### Game Crashes
- Update pygame: `pip install --upgrade pygame`
- Check all dependencies installed
- Report bugs with error message

### Performance Issues
- Close other programs
- Lower screen resolution (edit WIDTH/HEIGHT in code)
- Disable animations (future feature)

## 📚 Additional Resources

- **README.md** - Complete documentation
- **QUICKSTART.md** - Quick reference
- **TUTORIAL.md** - Tutorial guide
- **FEATURES.md** - Feature list

## 🎉 Have Fun!

Remember:
- ✅ Start with the tutorial
- ✅ Practice with local games
- ✅ Learn from mistakes
- ✅ Try different strategies
- ✅ Most importantly: HAVE FUN! 🎮✨

---

**Questions?** Check the documentation files or experiment in-game!

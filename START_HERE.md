# 🎮 START HERE - Hearthstone Python Edition

## ⚡ Quick Start (3 Steps)

### 1. Install Dependencies
```bash
pip install pygame websockets numpy
```

### 2. Run the Game
```bash
python main.py
```

### 3. Click "Tutorial" on the Menu
The interactive tutorial will teach you everything!

---

## 📖 Documentation Guide

Choose what you need:

### 🆕 New Players
1. **START HERE** (you are here!)
2. **[TUTORIAL.md](TUTORIAL.md)** - Learn how the tutorial works
3. **[COMPLETE_GUIDE.md](COMPLETE_GUIDE.md)** - Full game guide
4. **Play the in-game tutorial** - Best way to learn!

### ⚡ Quick Reference
- **[QUICKSTART.md](QUICKSTART.md)** - Installation and basic usage
- **[FEATURES.md](FEATURES.md)** - Complete feature list
- **[README.md](README.md)** - Technical documentation

### 🎯 What to Read First

**If you're completely new:**
1. This file (START_HERE.md) ← You are here
2. Run `python main.py`
3. Click "Tutorial" button
4. Follow the 17-step interactive guide
5. Start playing!

**If you want to understand the game:**
1. [COMPLETE_GUIDE.md](COMPLETE_GUIDE.md) - Everything explained

**If you want quick answers:**
1. [QUICKSTART.md](QUICKSTART.md) - Fast reference

**If you want technical details:**
1. [README.md](README.md) - Full documentation
2. [FEATURES.md](FEATURES.md) - Feature list

---

## 🎓 The Tutorial

### What It Teaches (17 Steps)

1. ✅ Welcome & Introduction
2. ✅ Your Hero (30 HP, your life)
3. ✅ Mana Crystals (resources to play cards)
4. ✅ Your Hand (cards you can play)
5. ✅ **Playing Cards** (drag & drop - YOU DO THIS!)
6. ✅ The Board (where minions fight)
7. ✅ Minion Stats (attack/health)
8. ✅ Summoning Sickness (can't attack first turn)
9. ✅ End Turn Button (pass to opponent)
10. ✅ Hero Power (special ability, 2 mana)
11. ✅ Opponent's Hero (your target)
12. ✅ Attacking (click minion, click target)
13. ✅ Game Log (see all actions)
14. ✅ Card Types (minions, spells, weapons)
15. ✅ Special Abilities (taunt, charge, etc.)
16. ✅ Strategy Tips (how to win)
17. ✅ Tutorial Complete! 🎉

### Tutorial Features

- 🎯 **Interactive** - You actually play!
- 💡 **Highlighted Areas** - Shows exactly where to look
- ➡️ **Animated Arrows** - Points to what you need to click
- ⏭️ **Auto-Advance** - Moves forward when you complete actions
- ⏸️ **Skip Anytime** - Press ESC if you want to skip
- 🔊 **Sound Effects** - Hear the game as you learn
- 📊 **Progress Tracker** - See which step you're on

### How Long?
**5-10 minutes** if you read everything carefully

---

## 🎮 Game Modes

### 1. Tutorial (Recommended First!)
- Learn all mechanics
- Hands-on practice
- 17 interactive steps
- Skip anytime

### 2. Play Local
- Same computer, 2 players
- Take turns
- Perfect for learning
- Play with friends/family

### 3. Play Online
- Internet multiplayer
- Real-time matches
- Requires server
- Play with anyone

### 4. Host Server
- Let others connect
- Share your IP
- Port 8765
- Be the host!

---

## 🎯 Core Concepts (Quick Version)

### Goal
**Reduce opponent's hero to 0 health**

### Resources
- **Mana:** Play cards (gain 1 per turn, max 10)
- **Cards:** Actions you can take (max 10 in hand)
- **Health:** Your life (start at 30)

### Card Types
1. **Minions** - Stay on board, attack
2. **Spells** - One-time effects
3. **Weapons** - Hero can attack

### Turn Structure
1. Draw card
2. Gain mana
3. Play cards & attack
4. End turn

### Combat
- Click minion → Click target
- Both take damage
- 0 health = dies

---

## 🌟 Special Abilities (Quick Reference)

| Ability | Effect |
|---------|--------|
| **Taunt** | Must attack first |
| **Charge** | Attack immediately |
| **Divine Shield** | Block 1 hit |
| **Windfury** | Attack twice |
| **Stealth** | Can't be targeted |
| **Poisonous** | Kills any minion |
| **Lifesteal** | Heals your hero |
| **Battlecry** | Effect when played |
| **Deathrattle** | Effect when dies |

---

## 🎮 Controls (Quick Reference)

### Mouse
- **Drag card** → Play it
- **Click minion** → Select for attack
- **Click target** → Attack
- **Right-click** → Cancel
- **Click "End Turn"** → Pass turn

### Keyboard
- **Space** → End turn
- **Tab** → Toggle log
- **ESC** → Cancel/Exit

---

## ❓ Common Questions

### Q: Do I need to read all the documentation?
**A:** No! Just run the game and click "Tutorial". It teaches you everything interactively.

### Q: What if I get stuck?
**A:** 
1. Press ESC to skip tutorial
2. Check [COMPLETE_GUIDE.md](COMPLETE_GUIDE.md)
3. Try again - practice makes perfect!

### Q: Can I play alone?
**A:** Yes! Play Local mode and control both players, or wait for AI (future feature).

### Q: Do I need internet?
**A:** No for local play. Yes for online multiplayer.

### Q: Is it hard to learn?
**A:** No! The tutorial makes it easy. 5-10 minutes and you're ready!

---

## 🚀 Your Learning Path

```
1. Install (pip install pygame websockets numpy)
   ↓
2. Run (python main.py)
   ↓
3. Click "Tutorial"
   ↓
4. Follow 17 steps (5-10 min)
   ↓
5. Play Local games (practice)
   ↓
6. Try Online multiplayer
   ↓
7. Master the game! 🏆
```

---

## 📁 File Structure (What's What)

```
Game/
├── main.py                    ← RUN THIS!
├── START_HERE.md             ← YOU ARE HERE
├── TUTORIAL.md               ← Tutorial guide
├── COMPLETE_GUIDE.md         ← Full game guide
├── QUICKSTART.md             ← Quick reference
├── README.md                 ← Technical docs
├── FEATURES.md               ← Feature list
├── requirements.txt          ← Dependencies
├── launch.bat / launch.sh    ← Easy launchers
└── hearthstone/              ← Game code
    ├── gui/                  ← Graphics
    │   ├── menu.py          ← Main menu
    │   ├── game_gui.py      ← Game interface
    │   ├── tutorial.py      ← Tutorial system
    │   └── sound_manager.py ← Sounds
    ├── game.py              ← Game logic
    ├── player.py            ← Player state
    ├── card.py              ← Card system
    └── cards_collection.py  ← All 50+ cards
```

---

## 🎉 Ready to Play?

### Right Now:
```bash
python main.py
```

### Then:
1. Click **"Tutorial"**
2. Follow the guide
3. Have fun! 🎮✨

---

## 💡 Pro Tips

1. **Don't skip the tutorial** - It's interactive and fun!
2. **Use all your mana** - Don't waste resources
3. **Control the board** - Keep minions alive
4. **Read the cards** - Understand what they do
5. **Practice** - Play local games to improve
6. **Have fun** - It's a game, enjoy it!

---

## 🆘 Need Help?

1. **In-game tutorial** - Best way to learn
2. **[COMPLETE_GUIDE.md](COMPLETE_GUIDE.md)** - Detailed explanations
3. **[QUICKSTART.md](QUICKSTART.md)** - Quick answers
4. **Experiment** - Try things and learn!

---

## 🎊 Welcome to Hearthstone!

You're about to have a great time. The tutorial will teach you everything you need to know in just a few minutes.

**Ready? Let's go!**

```bash
python main.py
```

**Click "Tutorial" and start your journey! 🚀**

---

*Made with ❤️ in Python. Have fun playing!*

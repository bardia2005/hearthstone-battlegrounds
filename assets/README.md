# Assets Folder

This folder contains game assets like card artwork, music, sounds, and other media files.

## Folder Structure

```
assets/
├── card_art/          # Card artwork images
│   ├── [CardName].png
│   ├── [CardName].jpg
│   └── ...
├── music/             # Background music tracks
│   ├── menu_*.mp3     # Menu/tavern music
│   ├── game_*.mp3     # Gameplay/battle music
│   └── CREDITS.txt    # Music attribution
└── sounds/            # Sound effects (future)
```

## Adding Card Artwork

1. Create images for your cards (PNG, JPG, or JPEG format)
2. Name them exactly as the card name (e.g., "Bloodfen Raptor.png")
3. Place them in the `card_art/` folder
4. The game will automatically load them!

See `CARD_ART_GUIDE.md` in the main Game folder for detailed instructions.

## Adding Music

1. Get royalty-free fantasy music (MP3, OGG, or WAV format)
2. Name files with "menu" or "game" prefix:
   - `menu_tavern_theme.mp3` - For main menu
   - `game_battle_epic.mp3` - For gameplay
3. Place them in the `music/` folder
4. The game will automatically play them!

See `MUSIC_GUIDE.md` in the main Game folder for detailed instructions.

### Music Recommendations

**Menu Music** (Calm, tavern-like):
- Peaceful medieval themes
- Acoustic instruments (lute, harp)
- Slow tempo (60-90 BPM)

**Game Music** (Epic, battle-like):
- Dramatic orchestral themes
- Heroic and intense
- Faster tempo (100-140 BPM)

### Free Music Sources
- Incompetech (incompetech.com) - Kevin MacLeod
- Bensound (bensound.com)
- OpenGameArt (opengameart.org)
- YouTube Audio Library

## Legal Notice

**Do not add copyrighted material** from Blizzard Entertainment or other companies. Only use:
- Royalty-free music and artwork
- Creative Commons licensed work (with proper attribution)
- Your own original creations
- AI-generated content you created

## Recommended Specs

### Card Art
- **Format**: PNG (best quality) or JPG (smaller files)
- **Size**: 256x256 to 512x512 pixels
- **Aspect Ratio**: Square or near-square

### Music
- **Format**: MP3 (most compatible) or OGG (better quality)
- **Bitrate**: 128-192 kbps
- **Length**: 2-5 minutes (will loop)
- **Sample Rate**: 44.1 kHz

## Example Files

### Card Art
- Bloodfen Raptor.png
- River Crocolisk.jpg
- Chillwind Yeti.png
- Fireball.png

### Music
- menu_tavern_theme.mp3
- menu_peaceful_inn.ogg
- game_epic_battle.mp3
- game_heroic_combat.ogg

The game will automatically generate procedural art for cards without images and play appropriate music when available!

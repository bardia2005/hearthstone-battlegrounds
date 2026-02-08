# Music Guide - Fantasy Themed Background Music

## Overview

The game now includes a music system that plays fantasy-themed background music for both the menu and gameplay. You can add your own custom music tracks!

## Quick Start

### Adding Music Files

1. **Create the music folder** (if it doesn't exist):
   ```
   Game/assets/music/
   ```

2. **Add your music files**:
   - Supported formats: MP3, OGG, WAV
   - Name them appropriately for auto-detection

3. **File naming conventions**:
   - **Menu music**: Include "menu" or "tavern" in filename
     - Examples: `menu_theme.mp3`, `tavern_ambience.ogg`
   - **Game music**: Include "game" or "battle" in filename
     - Examples: `battle_theme.mp3`, `game_music.ogg`

4. **Run the game** - Music plays automatically!

## Music Categories

### Menu Music (Tavern Theme)
**Mood**: Calm, welcoming, peaceful, cozy

**Characteristics**:
- Slower tempo (60-90 BPM)
- Acoustic instruments (lute, harp, flute)
- Warm, inviting atmosphere
- Medieval tavern ambience
- Light percussion
- Occasional crowd sounds

**Suggested Themes**:
- Tavern ambience
- Peaceful village
- Cozy inn
- Friendly gathering
- Medieval marketplace

### Game Music (Battle Theme)
**Mood**: Epic, dramatic, intense, heroic

**Characteristics**:
- Faster tempo (100-140 BPM)
- Orchestral instruments
- Dramatic strings and brass
- Epic percussion
- Building intensity
- Heroic melodies

**Suggested Themes**:
- Epic battle
- Heroic adventure
- Dramatic confrontation
- Strategic warfare
- Fantasy combat

## Finding Fantasy Music

### Legal Sources

#### 1. Royalty-Free Music Sites
- **Incompetech** (incompetech.com) - Kevin MacLeod's music
- **Free Music Archive** (freemusicarchive.org)
- **Bensound** (bensound.com)
- **Purple Planet** (purple-planet.com)
- **Silverman Sound** (silvermansound.com)

#### 2. Creative Commons Music
- **ccMixter** (ccmixter.org)
- **Jamendo** (jamendo.com)
- **SoundCloud** (CC-licensed tracks)

#### 3. Game Music Resources
- **OpenGameArt** (opengameart.org)
- **GameSounds.xyz**
- **Freesound** (freesound.org)

#### 4. YouTube Audio Library
- Free music for creators
- Filter by genre: "Cinematic", "Ambient"
- Download and use freely

### Recommended Search Terms

**For Menu Music**:
- "medieval tavern music"
- "fantasy inn ambience"
- "peaceful lute music"
- "medieval marketplace"
- "cozy tavern theme"
- "fantasy village music"

**For Game Music**:
- "epic fantasy battle music"
- "heroic orchestral theme"
- "dramatic fantasy combat"
- "epic adventure music"
- "fantasy war theme"
- "heroic battle soundtrack"

## Specific Recommendations

### Menu Music Examples

1. **"Tavern Loop" by Kevin MacLeod**
   - Perfect tavern atmosphere
   - Available on Incompetech
   - Free with attribution

2. **"Medieval Feast" by Bensound**
   - Upbeat medieval theme
   - Great for menu screens
   - Royalty-free

3. **"Peaceful Village" (various artists)**
   - Search on OpenGameArt
   - Multiple free options
   - Fantasy RPG style

### Game Music Examples

1. **"Heroic Adventure" by Kevin MacLeod**
   - Epic orchestral theme
   - Perfect for battles
   - Free with attribution

2. **"Epic Battle" by Bensound**
   - Dramatic and intense
   - Great for gameplay
   - Royalty-free

3. **"Fantasy Battle Theme" (various)**
   - Search on OpenGameArt
   - Many free options
   - Epic fantasy style

## File Organization

### Recommended Structure
```
assets/music/
├── menu_tavern_theme.mp3      # Main menu music
├── menu_peaceful_inn.ogg      # Alternative menu
├── game_epic_battle.mp3       # Main game music
├── game_heroic_combat.ogg     # Alternative game
└── README.txt                 # Attribution info
```

### File Naming Best Practices
- Use descriptive names
- Include category (menu/game)
- Add mood descriptor
- Keep names simple
- Use underscores, not spaces

## Technical Specifications

### Audio Format Recommendations

**MP3**:
- Most compatible
- Good compression
- Recommended: 128-192 kbps
- Smaller file sizes

**OGG**:
- Better quality at same bitrate
- Open source format
- Recommended: 128-192 kbps
- Good for looping

**WAV**:
- Highest quality
- No compression
- Larger file sizes
- Use for short tracks only

### Audio Settings
- **Sample Rate**: 44.1 kHz (CD quality)
- **Bit Depth**: 16-bit
- **Channels**: Stereo (2 channels)
- **Bitrate**: 128-192 kbps (for compressed formats)

### File Size Guidelines
- Menu music: 2-5 MB (2-3 minutes)
- Game music: 3-8 MB (3-5 minutes)
- Keep total under 20 MB for all tracks

## Music Features

### Automatic Playback
- Menu music starts when game launches
- Game music starts when match begins
- Smooth crossfade between tracks
- Loops continuously

### Volume Control
- Default volume: 30%
- Adjustable in code
- Doesn't interfere with sound effects

### Crossfading
- 1.5 second fade between menu and game
- Smooth transitions
- No abrupt cuts

## Creating Your Own Music

### Using Free Tools

#### 1. LMMS (Linux MultiMedia Studio)
- Free, open-source DAW
- Great for game music
- Built-in instruments
- Export to MP3/OGG

#### 2. Audacity
- Free audio editor
- Mix multiple tracks
- Add effects
- Export to any format

#### 3. MuseScore
- Free music notation
- Create orchestral scores
- Export to audio
- Great for epic themes

### AI Music Generation

#### 1. Suno AI
- Generate custom music
- Describe the mood
- Download and use

#### 2. AIVA
- AI music composer
- Fantasy/epic themes
- Free tier available

#### 3. Soundraw
- Customize AI music
- Adjust mood and tempo
- Download tracks

### Tips for Creating Fantasy Music

**Menu Music**:
1. Start with acoustic instruments
2. Use major keys (C, G, D)
3. Slow, steady tempo
4. Add ambient sounds
5. Keep it simple and warm

**Game Music**:
1. Use orchestral instruments
2. Minor keys for drama (Am, Dm, Em)
3. Build intensity gradually
4. Add percussion for energy
5. Create memorable melodies

## Attribution

### If Using Creative Commons Music

Create a file: `assets/music/CREDITS.txt`

```
Music Credits:

Menu Music:
- "Tavern Loop" by Kevin MacLeod (incompetech.com)
  Licensed under Creative Commons: By Attribution 4.0
  http://creativecommons.org/licenses/by/4.0/

Game Music:
- "Epic Battle" by Bensound (bensound.com)
  Licensed under Creative Commons: By Attribution 4.0
  http://creativecommons.org/licenses/by/4.0/
```

## Troubleshooting

### Music Not Playing
- Check file format (MP3, OGG, or WAV)
- Verify file is in `assets/music/` folder
- Check filename includes "menu" or "game"
- Look for error messages in console
- Test file in media player first

### Music Too Loud/Quiet
- Adjust volume in code:
  ```python
  music_manager.set_volume(0.3)  # 30%
  ```
- Or normalize audio in Audacity

### Music Stuttering
- Reduce file size
- Lower bitrate (128 kbps)
- Use MP3 instead of WAV
- Close other programs

### No Crossfade
- Ensure both tracks exist
- Check console for errors
- Verify pygame.mixer initialized

## Advanced Features

### Multiple Tracks
The system randomly selects from available tracks:
- Add multiple menu tracks for variety
- Add multiple game tracks for variety
- System picks randomly each time

### Custom Playlists
Edit `music_manager.py` to:
- Create custom playlists
- Add shuffle functionality
- Implement track progression
- Add fade effects

### Dynamic Music
Future enhancements could include:
- Music changes based on game state
- Intensity increases with action
- Victory/defeat music
- Special event themes

## Example Workflow

### Using Incompetech (Kevin MacLeod)

1. **Visit** incompetech.com
2. **Browse** by genre: "Medieval" or "Cinematic"
3. **Preview** tracks
4. **Download** MP3 files
5. **Rename**:
   - `Tavern Loop.mp3` → `menu_tavern_loop.mp3`
   - `Heroic Adventure.mp3` → `game_heroic_adventure.mp3`
6. **Place** in `assets/music/`
7. **Create** CREDITS.txt with attribution
8. **Run** game and enjoy!

### Using AI Generation (Suno)

1. **Visit** suno.ai
2. **Describe** music:
   - "Peaceful medieval tavern music with lute and flute"
   - "Epic fantasy battle music with orchestra"
3. **Generate** tracks
4. **Download** MP3 files
5. **Rename** appropriately
6. **Place** in `assets/music/`
7. **Run** game!

## Legal Compliance

**Important Reminders**:
- ❌ Do NOT use copyrighted music without permission
- ❌ Do NOT rip music from games or movies
- ❌ Do NOT use music from streaming services
- ✅ DO use royalty-free music
- ✅ DO use Creative Commons (with attribution)
- ✅ DO create your own music
- ✅ DO respect licensing terms

## Resources

### Music Sites
- **Incompetech**: incompetech.com
- **Bensound**: bensound.com
- **Purple Planet**: purple-planet.com
- **OpenGameArt**: opengameart.org

### Music Tools
- **LMMS**: lmms.io
- **Audacity**: audacityteam.org
- **MuseScore**: musescore.org

### AI Music
- **Suno**: suno.ai
- **AIVA**: aiva.ai
- **Soundraw**: soundraw.io

## Support

For music-related issues:
1. Check this guide
2. Verify file formats and names
3. Test files in media player
4. Check console for errors
5. Ensure pygame.mixer is working

Enjoy your fantasy-themed Hearthstone experience with epic music! 🎵

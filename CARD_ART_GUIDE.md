# Card Artwork Guide

## Overview

The game now includes a professional card art system that supports custom artwork. You can add your own card images to make the game look exactly how you want!

## How to Add Custom Card Art

### 1. Prepare Your Images

**Image Requirements:**
- Format: PNG, JPG, or JPEG
- Recommended size: 256x256 pixels or larger
- Aspect ratio: Any (will be scaled to fit)
- Quality: Higher resolution = better quality

**Image Guidelines:**
- Use clear, recognizable artwork
- Ensure good contrast for visibility
- Avoid overly dark or light images
- Consider the fantasy/medieval theme

### 2. Name Your Files

Name your image files **exactly** as the card name (case-insensitive):

```
Bloodfen Raptor.png
Chillwind Yeti.jpg
Fireball.png
Boulderfist Ogre.jpeg
```

### 3. Place Files in the Assets Folder

Put your images in: `Game/assets/card_art/`

The folder structure will be created automatically when you run the game.

```
Game/
├── assets/
│   └── card_art/
│       ├── Bloodfen Raptor.png
│       ├── Chillwind Yeti.png
│       ├── Fireball.png
│       └── ...
```

### 4. Run the Game

The game will automatically:
- Load your custom artwork
- Scale it to fit the card
- Cache it for better performance
- Fall back to procedural art if no image exists

## Procedural Art System

If you don't provide custom artwork, the game generates professional-looking procedural art based on:

### Spell Cards
- **Fire Spells**: Red/orange flames with fire symbols
- **Frost Spells**: Blue/cyan ice with snowflake symbols
- **Arcane Spells**: Purple/pink magic with sparkle symbols
- **Shadow Spells**: Dark purple with skull symbols
- **Holy Spells**: Bright yellow/white with divine symbols
- **Nature Spells**: Green with leaf symbols

### Minion Cards
- **Dragons**: Red with dragon symbols
- **Demons**: Purple with demon symbols
- **Beasts**: Brown with animal symbols
- **Murlocs**: Blue with fish symbols
- **Mechs**: Gray with robot symbols
- **Undead**: Gray-blue with skull symbols
- **Warriors**: Gold with sword symbols
- **Mages**: Blue with wizard symbols

## Finding Card Artwork

### Legal Sources for Card Art

**IMPORTANT**: Do not use copyrighted Hearthstone card art from Blizzard. Instead, use:

1. **Public Domain Art**:
   - Wikimedia Commons (public domain section)
   - Pixabay
   - Unsplash
   - Pexels

2. **Creative Commons (with attribution)**:
   - DeviantArt (CC-licensed works)
   - ArtStation (with permission)
   - Flickr (CC-licensed)

3. **AI-Generated Art**:
   - Midjourney
   - DALL-E
   - Stable Diffusion
   - Leonardo.ai

4. **Commission Custom Art**:
   - Hire artists on Fiverr
   - Commission on DeviantArt
   - Use ArtStation for professional artists

5. **Create Your Own**:
   - Digital painting (Photoshop, Krita, GIMP)
   - 3D rendering (Blender)
   - Photo manipulation

### Recommended Search Terms

For finding appropriate artwork:
- "fantasy creature"
- "medieval warrior"
- "magic spell effect"
- "dragon illustration"
- "fantasy character portrait"
- "creature concept art"

## Example Workflow

### Using AI Art Generation

1. **Generate with Midjourney/DALL-E**:
   ```
   Prompt: "fantasy card game art, bloodfen raptor, 
   dinosaur creature, medieval style, portrait view"
   ```

2. **Save the image**:
   - Download as PNG
   - Name it "Bloodfen Raptor.png"

3. **Place in folder**:
   - Copy to `Game/assets/card_art/`

4. **Test in game**:
   - Run the game
   - The card will now show your custom art!

### Using Public Domain Art

1. **Search Wikimedia Commons**:
   - Go to commons.wikimedia.org
   - Search for "dragon medieval"
   - Filter by "Public Domain"

2. **Download and edit**:
   - Download high-res version
   - Crop to square aspect ratio
   - Adjust brightness/contrast if needed

3. **Save and use**:
   - Save as "Dragon.png"
   - Place in assets folder

## Card List

Here are the default cards you can create artwork for:

### Basic Minions
- Bloodfen Raptor (2 mana, 3/2)
- River Crocolisk (2 mana, 2/3)
- Chillwind Yeti (4 mana, 4/5)
- Boulderfist Ogre (6 mana, 6/7)
- War Golem (7 mana, 7/7)

### Spells
- Fireball (4 mana, deal 6 damage)
- Frostbolt (2 mana, deal 3 damage and freeze)
- Arcane Missiles (1 mana, deal 3 damage randomly)

### Special Minions
- Taunt minions (add shield artwork)
- Charge minions (add speed lines)
- Divine Shield minions (add glow effect)

## Advanced Customization

### Creating Themed Decks

You can create themed artwork sets:

**Cyberpunk Theme**:
- Replace medieval creatures with robots
- Use neon colors
- Futuristic spell effects

**Horror Theme**:
- Dark, gothic artwork
- Undead creatures
- Blood and shadow effects

**Cute/Chibi Theme**:
- Cartoon-style characters
- Bright, cheerful colors
- Simplified designs

### Batch Processing

If you have many images to prepare:

1. Use image editing software (GIMP, Photoshop)
2. Create an action/script to:
   - Resize to 256x256
   - Adjust brightness/contrast
   - Add border/frame
   - Export as PNG

3. Batch process all your artwork

## Performance Tips

- **Optimal size**: 256x256 to 512x512 pixels
- **File format**: PNG for quality, JPG for smaller files
- **Compression**: Use moderate compression for JPG
- **Caching**: Images are cached after first load

## Troubleshooting

### Image Not Showing
- Check filename matches card name exactly
- Verify file is in `assets/card_art/` folder
- Ensure file extension is .png, .jpg, or .jpeg
- Check file isn't corrupted

### Image Looks Stretched
- Use square or near-square aspect ratios
- Pre-crop images before adding

### Performance Issues
- Reduce image file sizes
- Use JPG instead of PNG for photos
- Limit image resolution to 512x512

## Legal Notice

**Important**: This game is a fan project for educational purposes. Do not use copyrighted artwork from Blizzard Entertainment or other companies without permission. Always respect intellectual property rights and use only:
- Public domain artwork
- Creative Commons licensed work (with attribution)
- Your own original artwork
- Commissioned artwork you have rights to use
- AI-generated artwork you created

## Resources

### Free Art Resources
- **Wikimedia Commons**: commons.wikimedia.org
- **Pixabay**: pixabay.com
- **Unsplash**: unsplash.com
- **OpenGameArt**: opengameart.org

### AI Art Tools
- **Midjourney**: midjourney.com
- **DALL-E**: openai.com/dall-e
- **Stable Diffusion**: stability.ai
- **Leonardo.ai**: leonardo.ai

### Art Communities
- **DeviantArt**: deviantart.com
- **ArtStation**: artstation.com
- **Behance**: behance.net

## Support

If you need help with card artwork:
1. Check this guide first
2. Verify your file names and locations
3. Test with a single card first
4. Check the console for error messages

Enjoy creating your custom Hearthstone experience!

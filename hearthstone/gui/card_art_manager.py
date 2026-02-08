"""
Card Art Manager - Handles loading and rendering card artwork
Supports both image files and procedurally generated art
"""

import pygame
import os
import re
from typing import Dict, Optional
from .colors import *


class CardArtManager:
    """Manages card artwork - loads images or generates procedural art"""
    
    def __init__(self, progress_callback=None):
        self.art_cache: Dict[str, pygame.Surface] = {}
        self.art_directory = "Cards"  # Main Cards folder with 300+ PNGs
        self.heroes_directory = "Heroes"  # Hero cards folder at Game/Heroes
        self.fallback_directory = "assets/card_art"  # Custom art folder
        self.progress_callback = progress_callback  # Callback for loading progress
        
        # Create directories if they don't exist
        os.makedirs(self.fallback_directory, exist_ok=True)
        
        # Card name mapping: game name -> PNG filename
        self.name_mapping: Dict[str, str] = {}
        
        # List of all available card images (for random assignment)
        self.available_images: list = []
        
        # Hero images specifically
        self.hero_images: list = []
        
        # Assigned cards: game card name -> assigned image
        self.assigned_cards: Dict[str, pygame.Surface] = {}
        
        # Track used hero indices to ensure heroes are NEVER the same
        self.used_hero_indices: set = set()
        
        # Load hero cards from Heroes folder FIRST
        self._load_hero_cards()
        
        # Preload card art from Cards folder
        self._load_card_art_from_cards_folder()
        
        # Also load any custom art
        self._load_existing_art()
        
        # Build list of available images
        self._build_available_images_list()
    
    
    def _load_hero_cards(self):
        """Load hero cards from the Heroes folder"""
        if not os.path.exists(self.heroes_directory):
            print(f"Heroes folder not found at {self.heroes_directory}")
            print(f"Expected path: {os.path.abspath(self.heroes_directory)}")
            return
        
        files = sorted([f for f in os.listdir(self.heroes_directory) if f.endswith(('.png', '.jpg', '.jpeg'))])
        
        if not files:
            print(f"WARNING: No hero images found in {self.heroes_directory} folder!")
            print(f"Full path: {os.path.abspath(self.heroes_directory)}")
            print("Please add hero card images to the Heroes folder")
            return
        
        print(f"Loading {len(files)} hero cards from {self.heroes_directory} folder...")
        
        for filename in files:
            filepath = os.path.join(self.heroes_directory, filename)
            try:
                image = pygame.image.load(filepath)
                self.hero_images.append(image)
                print(f"✓ Loaded hero card: {filename} ({image.get_width()}x{image.get_height()})")
            except Exception as e:
                print(f"✗ Failed to load hero {filename}: {e}")
        
        print(f"Successfully loaded {len(self.hero_images)} hero cards total")
    
    def _crop_white_borders(self, surface: pygame.Surface) -> pygame.Surface:
        """Crop white/light borders from card PNG to get just the card art"""
        width, height = surface.get_size()
        
        # Convert to pixel array for analysis
        pixels = pygame.surfarray.array3d(surface)
        
        # Find bounds of non-white content (threshold for "white" is 240+ on all channels)
        WHITE_THRESHOLD = 240
        
        # Find top boundary
        top = 0
        for y in range(height):
            row = pixels[:, y, :]
            if not (row >= WHITE_THRESHOLD).all():
                top = y
                break
        
        # Find bottom boundary
        bottom = height - 1
        for y in range(height - 1, -1, -1):
            row = pixels[:, y, :]
            if not (row >= WHITE_THRESHOLD).all():
                bottom = y
                break
        
        # Find left boundary
        left = 0
        for x in range(width):
            col = pixels[x, :, :]
            if not (col >= WHITE_THRESHOLD).all():
                left = x
                break
        
        # Find right boundary
        right = width - 1
        for x in range(width - 1, -1, -1):
            col = pixels[x, :, :]
            if not (col >= WHITE_THRESHOLD).all():
                right = x
                break
        
        # Crop the surface
        if right > left and bottom > top:
            crop_rect = pygame.Rect(left, top, right - left + 1, bottom - top + 1)
            cropped = surface.subsurface(crop_rect).copy()
            return cropped
        
        # If no cropping needed, return original
        return surface
    
    def _load_card_art_from_cards_folder(self):
        """Load card art from the Cards folder with 300+ PNG files"""
        if not os.path.exists(self.art_directory):
            return
        
        files = [f for f in os.listdir(self.art_directory) if f.endswith('.png')]
        total_files = len(files)
        
        for i, filename in enumerate(files):
            # Report progress
            if self.progress_callback:
                progress = (i + 1) / total_files
                self.progress_callback(progress, f"Loading card art... ({i+1}/{total_files})")
            
            # EXCLUDE hero portrait cards (they have arch/frame style)
            # These typically have "HERO" or specific hero names in filename
            filename_lower = filename.lower()
            if any(keyword in filename_lower for keyword in ['hero', 'portrait', 'rexxar', 'jaina', 'uther', 
                                                              'garrosh', 'malfurion', 'anduin', 'valeera', 
                                                              'thrall', 'guldан', 'medivh']):
                continue  # Skip hero portrait cards
            
            # Extract readable card name from filename
            card_name = self._extract_card_name_from_filename(filename)
            
            if card_name:
                filepath = os.path.join(self.art_directory, filename)
                try:
                    image = pygame.image.load(filepath)
                    # CROP WHITE BORDERS to get just the card art
                    cropped_image = self._crop_white_borders(image)
                    
                    # Store with both the extracted name and variations
                    self.art_cache[card_name.lower()] = cropped_image
                    self.name_mapping[card_name.lower()] = filename
                    
                    # Also store without spaces for easier matching
                    no_space_name = card_name.replace(" ", "").lower()
                    self.art_cache[no_space_name] = cropped_image
                    self.name_mapping[no_space_name] = filename
                except Exception as e:
                    print(f"Failed to load {filename}: {e}")
    
    def _extract_card_name_from_filename(self, filename: str) -> Optional[str]:
        """Extract readable card name from PNG filename"""
        # Remove extension
        name = filename.replace('.png', '')
        
        # Split by underscore to get parts
        parts = name.split('_')
        
        # Find the part after 'enUS' which contains the card name
        for i, part in enumerate(parts):
            if part == 'enUS' and i + 1 < len(parts):
                # Get the card name part (before the ID number)
                card_part = parts[i + 1]
                # Remove the ID number (everything after the last dash)
                if '-' in card_part:
                    card_name = card_part.rsplit('-', 1)[0]
                    # Convert CamelCase to spaces
                    # e.g., "Semi-StablePortal" -> "Semi Stable Portal"
                    card_name = re.sub(r'([a-z])([A-Z])', r'\1 \2', card_name)
                    # Replace remaining dashes with spaces
                    card_name = card_name.replace('-', ' ')
                    return card_name
        
        return None
    
    def _load_existing_art(self):
        """Load any existing custom card art from the fallback directory"""
        if not os.path.exists(self.fallback_directory):
            return
        
        for filename in os.listdir(self.fallback_directory):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                card_name = os.path.splitext(filename)[0]
                filepath = os.path.join(self.fallback_directory, filename)
                try:
                    image = pygame.image.load(filepath)
                    # Only add if not already loaded from Cards folder
                    if card_name.lower() not in self.art_cache:
                        self.art_cache[card_name.lower()] = image
                except:
                    pass
    
    def _build_available_images_list(self):
        """Build a list of all available card images for random assignment"""
        self.available_images = []
        for key, image in self.art_cache.items():
            # Skip cached scaled versions (they have dimensions in the key)
            if isinstance(key, str) and '_' not in key:
                self.available_images.append(image)
        
        print(f"CardArtManager: Loaded {len(self.available_images)} unique card images")
    
    def get_card_art(self, card_name: str, width: int, height: int, is_spell: bool = False, is_hero: bool = False) -> pygame.Surface:
        """Get card art - loads from file or assigns from available images"""
        cache_key = f"{card_name.lower()}_{width}_{height}"
        
        # Check cache first
        if cache_key in self.art_cache:
            return self.art_cache[cache_key]
        
        # For heroes, use hero images from Heroes folder
        if is_hero and self.hero_images:
            art_surface = self._assign_hero_image(card_name, width, height)
            self.art_cache[cache_key] = art_surface
            return art_surface
        
        # Try to load from file (exact match)
        art_surface = self._load_art_from_file(card_name, width, height)
        
        # If no exact match, assign a card image from available images
        if art_surface is None:
            art_surface = self._assign_card_image(card_name, width, height, is_spell)
        
        # Cache and return
        self.art_cache[cache_key] = art_surface
        return art_surface
    
    def _assign_hero_image(self, card_name: str, width: int, height: int) -> pygame.Surface:
        """Assign a RANDOM hero image from Heroes folder - scale to fit slot perfectly"""
        # ONLY use images from Heroes folder - no fallback
        if not self.hero_images:
            print("WARNING: No hero images loaded from Heroes folder!")
            # Create a placeholder with text
            surface = pygame.Surface((width, height))
            surface.fill((100, 100, 150))  # Purple placeholder
            font = pygame.font.Font(None, 24)
            text = font.render("NO HERO", True, (255, 255, 255))
            text_rect = text.get_rect(center=(width//2, height//2))
            surface.blit(text, text_rect)
            return surface
        
        # Check if we already assigned an image to this hero
        # Use card_name directly (which is the player ID from render_hero)
        hero_key = card_name.lower()
        if hero_key in self.assigned_cards:
            original = self.assigned_cards[hero_key]
            # Scale to EXACT dimensions to fit slot perfectly
            return pygame.transform.smoothscale(original, (width, height))
        
        # RANDOMLY select a hero image (truly random each time a new hero is created)
        import random
        index = random.randint(0, len(self.hero_images) - 1)
        
        assigned_image = self.hero_images[index]
        self.assigned_cards[hero_key] = assigned_image
        
        print(f"✓ Randomly assigned hero image {index+1}.png to hero {card_name}")
        
        # Scale to EXACT dimensions to fit slot perfectly
        return pygame.transform.smoothscale(assigned_image, (width, height))
    
    def _assign_card_image(self, card_name: str, width: int, height: int, is_spell: bool) -> pygame.Surface:
        """Assign a card image from available images to this card - scale to EXACT size"""
        # Check if we already assigned an image to this card
        if card_name.lower() in self.assigned_cards:
            original = self.assigned_cards[card_name.lower()]
            # Scale to EXACT dimensions
            return pygame.transform.smoothscale(original, (width, height))
        
        # If we have available images, assign one
        if self.available_images:
            # Use hash of card name to consistently assign the same image
            import hashlib
            hash_val = int(hashlib.md5(card_name.lower().encode()).hexdigest(), 16)
            index = hash_val % len(self.available_images)
            
            assigned_image = self.available_images[index]
            self.assigned_cards[card_name.lower()] = assigned_image
            
            # Scale to EXACT dimensions (no aspect ratio preservation)
            return pygame.transform.smoothscale(assigned_image, (width, height))
        
        # Fallback to procedural art if no images available
        return self._generate_procedural_art(card_name, width, height, is_spell)
    
    def _load_art_from_file(self, card_name: str, width: int, height: int) -> Optional[pygame.Surface]:
        """Try to load card art from file - scale to EXACT size"""
        # Try exact match first
        if card_name.lower() in self.art_cache:
            original = self.art_cache[card_name.lower()]
            # Scale to EXACT dimensions
            return pygame.transform.smoothscale(original, (width, height))
        
        # Try without spaces
        no_space_name = card_name.replace(" ", "").lower()
        if no_space_name in self.art_cache:
            original = self.art_cache[no_space_name]
            # Scale to EXACT dimensions
            return pygame.transform.smoothscale(original, (width, height))
        
        # Try partial matching (for similar names)
        card_lower = card_name.lower()
        for cached_name, cached_image in self.art_cache.items():
            if isinstance(cached_name, str) and not cached_name.endswith(f"_{width}_{height}"):
                # Check if card name is contained in cached name or vice versa
                if card_lower in cached_name or cached_name in card_lower:
                    # Scale to EXACT dimensions
                    return pygame.transform.smoothscale(cached_image, (width, height))
        
        # Try loading from fallback directory
        for ext in ['.png', '.jpg', '.jpeg']:
            filepath = os.path.join(self.fallback_directory, f"{card_name}{ext}")
            if os.path.exists(filepath):
                try:
                    image = pygame.image.load(filepath)
                    # Scale to EXACT dimensions
                    scaled = pygame.transform.smoothscale(image, (width, height))
                    self.art_cache[card_name.lower()] = image
                    return scaled
                except:
                    pass
        
        return None
    
    def _generate_procedural_art(self, card_name: str, width: int, height: int, is_spell: bool) -> pygame.Surface:
        """Generate professional-looking procedural card art"""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        if is_spell:
            self._draw_spell_art(surface, card_name, width, height)
        else:
            self._draw_minion_art(surface, card_name, width, height)
        
        return surface
    
    def _draw_spell_art(self, surface: pygame.Surface, card_name: str, width: int, height: int):
        """Draw procedural spell art with magical effects"""
        name_lower = card_name.lower()
        
        # Determine spell school colors
        if any(word in name_lower for word in ['fire', 'flame', 'burn', 'pyro']):
            colors = [(255, 100, 0), (255, 150, 0), (255, 200, 50), (255, 80, 0)]
            symbol = '🔥'
        elif any(word in name_lower for word in ['frost', 'ice', 'freeze', 'cold']):
            colors = [(100, 200, 255), (150, 220, 255), (200, 240, 255), (80, 180, 255)]
            symbol = '❄️'
        elif any(word in name_lower for word in ['arcane', 'magic', 'mystic']):
            colors = [(200, 100, 255), (220, 150, 255), (240, 200, 255), (180, 80, 255)]
            symbol = '✨'
        elif any(word in name_lower for word in ['shadow', 'dark', 'void', 'death']):
            colors = [(100, 50, 150), (120, 70, 170), (80, 40, 130), (60, 30, 100)]
            symbol = '💀'
        elif any(word in name_lower for word in ['holy', 'light', 'divine', 'heal']):
            colors = [(255, 255, 200), (255, 255, 150), (255, 250, 100), (255, 240, 80)]
            symbol = '✝️'
        elif any(word in name_lower for word in ['nature', 'wild', 'growth']):
            colors = [(100, 200, 100), (120, 220, 120), (80, 180, 80), (60, 160, 60)]
            symbol = '🌿'
        else:
            colors = [(150, 100, 255), (170, 120, 255), (130, 80, 255), (110, 60, 235)]
            symbol = '⚡'
        
        # Draw magical gradient background
        for i in range(height):
            color_idx = int((i / height) * (len(colors) - 1))
            next_idx = min(color_idx + 1, len(colors) - 1)
            factor = (i / height) * (len(colors) - 1) - color_idx
            
            color = tuple(int(colors[color_idx][j] + (colors[next_idx][j] - colors[color_idx][j]) * factor) for j in range(3))
            pygame.draw.line(surface, color, (0, i), (width, i))
        
        # Draw magical circles/runes
        center_x, center_y = width // 2, height // 2
        
        # Outer circle
        pygame.draw.circle(surface, (255, 255, 255, 100), (center_x, center_y), min(width, height) // 3, 2)
        
        # Inner circle
        pygame.draw.circle(surface, (255, 255, 255, 150), (center_x, center_y), min(width, height) // 5, 1)
        
        # Draw symbol
        try:
            font = pygame.font.Font(None, min(width, height) // 2)
            text = font.render(symbol, True, (255, 255, 255))
            text_rect = text.get_rect(center=(center_x, center_y))
            
            # Glow effect
            glow_font = pygame.font.Font(None, min(width, height) // 2 + 4)
            glow = glow_font.render(symbol, True, colors[0])
            glow_rect = glow.get_rect(center=(center_x, center_y))
            surface.blit(glow, glow_rect)
            
            surface.blit(text, text_rect)
        except:
            # Fallback to geometric shape
            pygame.draw.circle(surface, (255, 255, 255), (center_x, center_y), min(width, height) // 6)
    
    def _draw_minion_art(self, surface: pygame.Surface, card_name: str, width: int, height: int):
        """Draw procedural minion art with creature silhouette"""
        name_lower = card_name.lower()
        
        # Determine creature type and colors
        if any(word in name_lower for word in ['dragon', 'drake', 'wyrm']):
            colors = [(180, 50, 50), (200, 70, 70), (220, 90, 90)]
            symbol = '🐉'
            bg_color = (80, 20, 20)
        elif any(word in name_lower for word in ['demon', 'devil', 'imp']):
            colors = [(150, 50, 150), (170, 70, 170), (190, 90, 190)]
            symbol = '👹'
            bg_color = (60, 20, 60)
        elif any(word in name_lower for word in ['beast', 'wolf', 'bear', 'lion', 'tiger']):
            colors = [(150, 120, 80), (170, 140, 100), (190, 160, 120)]
            symbol = '🐺'
            bg_color = (60, 50, 30)
        elif any(word in name_lower for word in ['murloc', 'fish']):
            colors = [(80, 150, 180), (100, 170, 200), (120, 190, 220)]
            symbol = '🐸'
            bg_color = (30, 60, 80)
        elif any(word in name_lower for word in ['mech', 'robot', 'golem']):
            colors = [(150, 150, 150), (170, 170, 170), (190, 190, 190)]
            symbol = '🤖'
            bg_color = (60, 60, 60)
        elif any(word in name_lower for word in ['undead', 'skeleton', 'zombie']):
            colors = [(120, 120, 140), (140, 140, 160), (160, 160, 180)]
            symbol = '💀'
            bg_color = (40, 40, 50)
        elif any(word in name_lower for word in ['knight', 'warrior', 'soldier']):
            colors = [(180, 150, 100), (200, 170, 120), (220, 190, 140)]
            symbol = '⚔️'
            bg_color = (70, 60, 40)
        elif any(word in name_lower for word in ['mage', 'wizard', 'sorcerer']):
            colors = [(100, 100, 200), (120, 120, 220), (140, 140, 240)]
            symbol = '🧙'
            bg_color = (40, 40, 80)
        else:
            colors = [(150, 130, 100), (170, 150, 120), (190, 170, 140)]
            symbol = '⚔️'
            bg_color = (60, 50, 40)
        
        # Draw gradient background
        for i in range(height):
            factor = i / height
            color = tuple(int(bg_color[j] + (colors[1][j] - bg_color[j]) * factor) for j in range(3))
            pygame.draw.line(surface, color, (0, i), (width, i))
        
        # Draw creature silhouette/shape
        center_x, center_y = width // 2, height // 2
        
        # Draw atmospheric circles (depth effect)
        for i in range(3):
            radius = min(width, height) // 3 + i * 5
            alpha = 50 - i * 15
            circle_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(circle_surface, (*colors[i], alpha), (radius, radius), radius)
            surface.blit(circle_surface, (center_x - radius, center_y - radius))
        
        # Draw creature symbol
        try:
            font = pygame.font.Font(None, min(width, height) // 2)
            text = font.render(symbol, True, (255, 255, 255))
            text_rect = text.get_rect(center=(center_x, center_y))
            
            # Shadow
            shadow = font.render(symbol, True, (0, 0, 0))
            shadow_rect = shadow.get_rect(center=(center_x + 2, center_y + 2))
            surface.blit(shadow, shadow_rect)
            
            surface.blit(text, text_rect)
        except:
            # Fallback to geometric shape
            pygame.draw.ellipse(surface, colors[2], (width // 4, height // 4, width // 2, height // 2))


# Global instance
_art_manager = None

def get_art_manager(progress_callback=None) -> CardArtManager:
    """Get the global card art manager instance"""
    global _art_manager
    if _art_manager is None:
        _art_manager = CardArtManager(progress_callback)
    return _art_manager

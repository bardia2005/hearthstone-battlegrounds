import pygame
import math
from .colors import *
from .card_art_manager import get_art_manager


class CardRenderer:
    CARD_WIDTH = 247  # 0.9x of 274 (274 * 0.9 = 246.6 ≈ 247)
    CARD_HEIGHT = 261  # 0.9x of 290 (290 * 0.9 = 261)
    MINION_WIDTH = 247  # Board minions same as hand cards
    MINION_HEIGHT = 261  # Board minions same as hand cards
    
    def __init__(self):
        pygame.font.init()
        # Try to use a more fantasy-style font, fallback to default
        try:
            self.name_font = pygame.font.SysFont('georgia', 16, bold=True)
            self.stat_font = pygame.font.SysFont('georgia', 28, bold=True)
            self.mana_font = pygame.font.SysFont('georgia', 32, bold=True)
            self.desc_font = pygame.font.SysFont('georgia', 12)
        except:
            self.name_font = pygame.font.Font(None, 18)
            self.stat_font = pygame.font.Font(None, 28)
            self.mana_font = pygame.font.Font(None, 32)
            self.desc_font = pygame.font.Font(None, 14)
        
        # Get art manager
        self.art_manager = get_art_manager()
    
    def render_card(self, card, playable=False, selected=False, hover=False):
        """Render a card in hand - ONLY the image, no borders, no mana crystal - FULL IMAGE VISIBLE"""
        surface = pygame.Surface((self.CARD_WIDTH, self.CARD_HEIGHT), pygame.SRCALPHA)
        
        # Glow effect for playable/selected cards
        if selected or playable or hover:
            glow_surface = pygame.Surface((self.CARD_WIDTH + 10, self.CARD_HEIGHT + 10), pygame.SRCALPHA)
            glow_color = GLOW_YELLOW if selected else (GLOW_GREEN if playable else CARD_HOVER_GLOW)
            for i in range(5):
                alpha = 50 - i * 10
                pygame.draw.rect(glow_surface, (*glow_color[:3], alpha), 
                               (5-i, 5-i, self.CARD_WIDTH + i*2, self.CARD_HEIGHT + i*2), 
                               border_radius=12)
            temp_surface = pygame.Surface((self.CARD_WIDTH + 10, self.CARD_HEIGHT + 10), pygame.SRCALPHA)
            temp_surface.blit(glow_surface, (0, 0))
            temp_surface.blit(surface, (5, 5))
            surface = temp_surface
            offset = 5
        else:
            offset = 0
        
        # NO FRAME - just the image fills entire card - FULL IMAGE, NO CROPPING
        frame_width = self.CARD_WIDTH
        frame_height = self.CARD_HEIGHT
        
        # Image is EXACT size - no zoom, show full card art
        art_width = frame_width
        art_height = frame_height
        
        # Position at top-left
        art_x = offset
        art_y = offset
        art_rect = pygame.Rect(art_x, art_y, art_width, art_height)
        
        # Get and draw card art - EXACT size (no zoom, full image visible)
        is_spell_card = not (hasattr(card, 'attack') and hasattr(card, 'health'))
        art_surface = self.art_manager.get_card_art(card.name, art_rect.width, art_rect.height, is_spell_card)
        
        # Draw full image - no clipping
        surface.blit(art_surface, art_rect.topleft)
        
        # NO mana crystal - removed completely
        
        # NO attack/health gems - they're visible in the card art itself
        
        return surface
    
    def _draw_mana_crystal(self, surface, x, y, value, size):
        """Draw an authentic Hearthstone mana crystal"""
        # Outer dark border
        pygame.draw.circle(surface, MANA_CRYSTAL_BORDER, (x, y), size + 2)
        
        # Main crystal
        pygame.draw.circle(surface, MANA_CRYSTAL_FULL, (x, y), size)
        
        # Highlight shine
        shine_offset = int(size * 0.35)
        pygame.draw.circle(surface, MANA_CRYSTAL_HIGHLIGHT, (x - shine_offset, y - shine_offset), int(size * 0.45))
        
        # Value text with shadow (use smaller font for mana cost)
        cost_font = pygame.font.Font(None, int(size * 1.8))
        value_text = cost_font.render(str(value), True, TEXT_WHITE)
        value_shadow = cost_font.render(str(value), True, BLACK)
        value_rect = value_text.get_rect(center=(x, y + 1))
        surface.blit(value_shadow, (value_rect.x + 1, value_rect.y + 1))
        surface.blit(value_text, value_rect)
    
    def _draw_stat_gem(self, surface, x, y, value, stat_type, size):
        """Draw attack or health gem with authentic styling"""
        if stat_type == 'attack':
            main_color = ATTACK_YELLOW
            border_color = ATTACK_BORDER
            text_color = TEXT_BLACK
        else:
            main_color = HEALTH_RED
            border_color = HEALTH_BORDER
            text_color = TEXT_WHITE
        
        # Outer border
        pygame.draw.circle(surface, border_color, (x, y), size + 1)
        
        # Main gem
        pygame.draw.circle(surface, main_color, (x, y), size)
        
        # Shine effect
        shine_offset = int(size * 0.25)
        pygame.draw.circle(surface, STAT_SHINE, (x - shine_offset, y - shine_offset), int(size * 0.35))
        
        # Value with shadow - use appropriate font size
        if size <= 12:
            # Hand cards
            stat_font = pygame.font.Font(None, 20)
        elif size >= 15:
            # Board minions (0.8x or larger)
            stat_font = pygame.font.Font(None, 22)
        else:
            # Medium size
            stat_font = pygame.font.Font(None, 18)
        
        value_text = stat_font.render(str(value), True, text_color)
        value_shadow = stat_font.render(str(value), True, BLACK if stat_type == 'attack' else (80, 0, 0))
        value_rect = value_text.get_rect(center=(x, y + 1))
        surface.blit(value_shadow, (value_rect.x + 1, value_rect.y + 1))
        surface.blit(value_text, value_rect)
    
    def _draw_taunt_shield(self, surface, rect):
        """Draw taunt shield icon"""
        # Shield shape - scaled based on rect size
        center_x = rect.centerx
        center_y = rect.centery
        scale = rect.width / 20  # Scale based on width
        
        points = [
            (center_x, center_y - int(10 * scale)),
            (center_x + int(8 * scale), center_y - int(6 * scale)),
            (center_x + int(8 * scale), center_y + int(4 * scale)),
            (center_x, center_y + int(10 * scale)),
            (center_x - int(8 * scale), center_y + int(4 * scale)),
            (center_x - int(8 * scale), center_y - int(6 * scale))
        ]
        pygame.draw.polygon(surface, TAUNT_SHIELD_GOLD, points)
        pygame.draw.polygon(surface, TAUNT_SHIELD_DARK, points, max(2, int(2 * scale)))
    
    def render_minion(self, minion, can_attack=False, selected=False, is_target=False):
        """Render a minion on the board - same style as hand cards"""
        base_width = self.MINION_WIDTH
        base_height = self.MINION_HEIGHT
        
        # Create surface
        surface = pygame.Surface((base_width + 8, base_height + 8), pygame.SRCALPHA)
        offset = 4
        
        # Taunt glow effect
        if minion.taunt:
            for i in range(6):
                alpha = 80 - i * 12
                glow_rect = pygame.Rect(offset-i*2, offset-i*2, base_width + i*4, base_height + i*4)
                pygame.draw.rect(surface, (*TAUNT_SHIELD_GOLD[:3], alpha), glow_rect, border_radius=12)
        
        # Glow for states
        if selected or can_attack or is_target:
            glow_color = GLOW_YELLOW if selected else (GLOW_GREEN if can_attack else GLOW_RED)
            for i in range(4):
                alpha = 60 - i * 15
                glow_rect = pygame.Rect(offset-i*2, offset-i*2, base_width + i*4, base_height + i*4)
                pygame.draw.rect(surface, (*glow_color[:3], alpha), glow_rect, border_radius=10)
        
        # NO FRAME - just the image fills entire card (same as hand cards)
        frame_width = base_width
        frame_height = base_height
        
        # Image is EXACT size - no zoom, show full card art
        art_width = frame_width
        art_height = frame_height
        
        # Position at top-left
        art_x = offset
        art_y = offset
        art_rect = pygame.Rect(art_x, art_y, art_width, art_height)
        
        # Get and draw minion art - EXACT size (no zoom, full image visible)
        art_surface = self.art_manager.get_card_art(minion.name, art_rect.width, art_rect.height, False)
        
        # Draw full image - no clipping
        surface.blit(art_surface, art_rect.topleft)
        
        # Attack gem (bottom left) - on top of image
        attack_x = offset + 18
        attack_y = offset + base_height - 18
        self._draw_stat_gem(surface, attack_x, attack_y, minion.attack, 'attack', 15)
        
        # Health gem (bottom right) - on top of image
        health_x = offset + base_width - 18
        health_y = offset + base_height - 18
        is_damaged = minion.health < minion.max_health
        
        if is_damaged:
            # Draw damaged health (brighter red)
            pygame.draw.circle(surface, HEALTH_BORDER, (health_x, health_y), 17)
            pygame.draw.circle(surface, HEALTH_DAMAGED, (health_x, health_y), 15)
            pygame.draw.circle(surface, STAT_SHINE, (health_x - 4, health_y - 4), 5)
            
            # Use appropriate font
            health_font = pygame.font.Font(None, 26)
            health_text = health_font.render(str(minion.health), True, TEXT_WHITE)
            health_shadow = health_font.render(str(minion.health), True, (80, 0, 0))
            health_rect = health_text.get_rect(center=(health_x, health_y + 1))
            surface.blit(health_shadow, (health_rect.x + 1, health_rect.y + 1))
            surface.blit(health_text, health_rect)
        else:
            self._draw_stat_gem(surface, health_x, health_y, minion.health, 'health', 15)
        
        # Sleeping indicator (zzz)
        if not minion.can_attack:
            sleep_bg = pygame.Rect(offset + base_width - 35, offset + 4, 32, 26)
            pygame.draw.ellipse(surface, (40, 40, 60, 200), sleep_bg)
            sleep_font = pygame.font.Font(None, 18)
            sleep_text = sleep_font.render("zzz", True, (200, 200, 220))
            surface.blit(sleep_text, (offset + base_width - 33, offset + 7))
        
        # Taunt shield icon
        if minion.taunt:
            shield_rect = pygame.Rect(offset + base_width//2 - 12, offset + 2, 24, 24)
            self._draw_taunt_shield(surface, shield_rect)
        
        return surface
    
    def render_hero(self, player, is_current=False, is_target=False, width=None, height=None):
        """Render a hero portrait - FULL CARD from Heroes folder"""
        # Use FULL card dimensions (not scaled down)
        if width is None:
            width = 247
        if height is None:
            height = 261
            
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # NO GLOW - heroes are completely static, never move or change
        offset = 0
        
        # NO FRAME - just the image fills entire card - FULL IMAGE, NO CROPPING
        frame_width = width
        frame_height = height
        
        # Image is EXACT size - no zoom, show full card art
        art_width = frame_width
        art_height = frame_height
        
        # Position at top-left
        art_x = offset
        art_y = offset
        art_rect = pygame.Rect(art_x, art_y, art_width, art_height)
        
        # Get hero card art using PLAYER ID (not name) so it doesn't swap on turn change
        # Use a unique identifier that doesn't change
        hero_id = f"HERO_{id(player)}"  # Use Python object ID for consistency
        hero_art = self.art_manager.get_card_art(hero_id, art_rect.width, art_rect.height, False, is_hero=True)
        
        # Draw full image - no clipping
        surface.blit(hero_art, art_rect.topleft)
        
        # NO name plate - just pure card art like playable cards
        # NO health display - removed
        # NO armor display - removed
        
        return surface

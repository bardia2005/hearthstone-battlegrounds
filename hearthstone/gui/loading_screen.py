"""
Loading Screen - Shows progress while loading card art and game assets
"""

import pygame
from .colors import *


class LoadingScreen:
    """Displays a loading screen with progress bar"""
    
    def __init__(self, screen_width=1920, screen_height=1080):  # Bigger window
        self.width = screen_width
        self.height = screen_height
        self.screen = None
        self.font_large = None
        self.font_small = None
        
    def initialize(self):
        """Initialize pygame and create screen"""
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Hearthstone - Loading...")
        self.font_large = pygame.font.Font(None, 72)
        self.font_small = pygame.font.Font(None, 36)
        
    def draw(self, progress: float, message: str = "Loading..."):
        """Draw loading screen with progress bar
        
        Args:
            progress: Progress value between 0.0 and 1.0
            message: Status message to display (default: "Loading...")
        """
        if not self.screen:
            return
        
        # Load and draw Loading Screen background image
        try:
            bg_image = pygame.image.load("Designs/Loading_Screen_Background.jpg")
            # Scale to fit screen
            bg_image = pygame.transform.scale(bg_image, (self.width, self.height))
            self.screen.blit(bg_image, (0, 0))
        except:
            # Fallback to gradient background if image not found
            for y in range(self.height):
                color_factor = y / self.height
                color = (
                    int(BOARD_BG_TOP[0] + (BOARD_BG_BOTTOM[0] - BOARD_BG_TOP[0]) * color_factor),
                    int(BOARD_BG_TOP[1] + (BOARD_BG_BOTTOM[1] - BOARD_BG_TOP[1]) * color_factor),
                    int(BOARD_BG_TOP[2] + (BOARD_BG_BOTTOM[2] - BOARD_BG_TOP[2]) * color_factor)
                )
                pygame.draw.line(self.screen, color, (0, y), (self.width, y))
        
        # Title
        title_text = "HEARTHSTONE"
        title_surface = self.font_large.render(title_text, True, TEXT_GOLD)
        title_shadow = self.font_large.render(title_text, True, BLACK)
        title_rect = title_surface.get_rect(center=(self.width // 2, self.height // 2 - 100))
        self.screen.blit(title_shadow, (title_rect.x + 3, title_rect.y + 3))
        self.screen.blit(title_surface, title_rect)
        
        # Progress bar background
        bar_width = 600
        bar_height = 40
        bar_x = (self.width - bar_width) // 2
        bar_y = self.height // 2 + 20
        
        # Outer frame
        outer_rect = pygame.Rect(bar_x - 5, bar_y - 5, bar_width + 10, bar_height + 10)
        pygame.draw.rect(self.screen, CARD_BORDER_GOLD, outer_rect, border_radius=8)
        
        # Background
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(self.screen, BOARD_WOOD_DARK, bg_rect, border_radius=6)
        
        # Progress fill (dark purple)
        if progress > 0:
            fill_width = int(bar_width * min(progress, 1.0))
            fill_rect = pygame.Rect(bar_x, bar_y, fill_width, bar_height)
            
            # Dark purple gradient fill
            for i in range(fill_rect.width):
                x = bar_x + i
                color_factor = i / bar_width
                color = (
                    int(80 + 40 * color_factor),   # R: 80-120
                    int(40 + 40 * color_factor),   # G: 40-80
                    int(120 + 60 * color_factor)   # B: 120-180 (purple)
                )
                pygame.draw.line(self.screen, color, (x, bar_y), (x, bar_y + bar_height))
            
            # Shine effect on progress bar
            shine_rect = pygame.Rect(bar_x, bar_y, fill_width, bar_height // 3)
            shine_surface = pygame.Surface((fill_width, bar_height // 3), pygame.SRCALPHA)
            for i in range(bar_height // 3):
                alpha = 100 - (i * 3)
                pygame.draw.line(shine_surface, (150, 120, 200, alpha), (0, i), (fill_width, i))
            self.screen.blit(shine_surface, shine_rect.topleft)
        
        # Status message - just "Loading..."
        msg_surface = self.font_small.render("Loading...", True, BUTTON_TEXT)
        msg_shadow = self.font_small.render("Loading...", True, BLACK)
        msg_rect = msg_surface.get_rect(center=(self.width // 2, bar_y + bar_height + 50))
        self.screen.blit(msg_shadow, (msg_rect.x + 1, msg_rect.y + 1))
        self.screen.blit(msg_surface, msg_rect)
        
        pygame.display.flip()
        
        # Process events to keep window responsive
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys
                sys.exit()


# Global loading screen instance
_loading_screen = None

def get_loading_screen():
    """Get the global loading screen instance"""
    global _loading_screen
    if _loading_screen is None:
        _loading_screen = LoadingScreen()
    return _loading_screen

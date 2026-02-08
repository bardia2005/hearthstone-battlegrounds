"""
Main menu system for Hearthstone
"""

import pygame
import sys
from typing import Optional, Callable
from .colors import *
from .sound_manager import get_sound_manager
from .music_manager import get_music_manager


class Button:
    def __init__(self, x, y, width, height, text, callback, font_size=36):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.font = pygame.font.Font(None, font_size)
        self.hovered = False
        self.enabled = True
        self.was_hovered = False
        self.sound_manager = get_sound_manager()
    
    def draw(self, surface):
        # Button background with ornate styling
        if not self.enabled:
            color = MANA_CRYSTAL_EMPTY
            text_color = GRAY
            border_color = BOARD_WOOD_DARK
        elif self.hovered:
            color = BUTTON_HOVER
            text_color = TEXT_GOLD
            border_color = CARD_BORDER_GOLD
        else:
            color = BUTTON_BG
            text_color = BUTTON_TEXT
            border_color = BOARD_WOOD_LIGHT
        
        # Glow effect when hovering
        if self.hovered and self.enabled:
            for i in range(4):
                alpha = 60 - i * 15
                glow_rect = self.rect.inflate(i*4, i*4)
                pygame.draw.rect(surface, (*GLOW_YELLOW[:3], alpha), glow_rect, border_radius=12)
        
        # Main button
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        
        # Ornate border
        pygame.draw.rect(surface, border_color, self.rect, 4, border_radius=12)
        pygame.draw.rect(surface, BOARD_WOOD_DARK, self.rect.inflate(-8, -8), 2, border_radius=10)
        
        # Button text with shadow
        text_surface = self.font.render(self.text, True, text_color)
        text_shadow = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_shadow, (text_rect.x + 2, text_rect.y + 2))
        surface.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if not self.enabled:
            return False
        
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
            # Play hover sound when entering button
            if self.hovered and not self.was_hovered:
                self.sound_manager.play('button_hover')
            self.was_hovered = self.hovered
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.sound_manager.play('button_click')
                self.callback()
                return True
        return False


class TextInput:
    def __init__(self, x, y, width, height, placeholder="", max_length=20):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.placeholder = placeholder
        self.max_length = max_length
        self.font = pygame.font.Font(None, 32)
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0
    
    def draw(self, surface):
        # Background with ornate styling
        color = MANA_CRYSTAL_FULL if self.active else BUTTON_BG
        border_color = CARD_BORDER_GOLD if self.active else BOARD_WOOD_LIGHT
        
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, border_color, self.rect, 3, border_radius=10)
        
        # Inner border
        pygame.draw.rect(surface, BOARD_WOOD_DARK, self.rect.inflate(-6, -6), 1, border_radius=8)
        
        # Text
        display_text = self.text if self.text else self.placeholder
        text_color = TEXT_WHITE if self.text else GRAY
        text_surface = self.font.render(display_text, True, text_color)
        text_shadow = self.font.render(display_text, True, BLACK)
        text_rect = text_surface.get_rect(midleft=(self.rect.x + 15, self.rect.centery))
        surface.blit(text_shadow, (text_rect.x + 1, text_rect.y + 1))
        surface.blit(text_surface, text_rect)
        
        # Cursor
        if self.active:
            self.cursor_timer += 1
            if self.cursor_timer > 30:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0
            
            if self.cursor_visible:
                cursor_x = text_rect.right + 3
                pygame.draw.line(surface, TEXT_GOLD, 
                               (cursor_x, self.rect.y + 12),
                               (cursor_x, self.rect.bottom - 12), 3)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False
            elif len(self.text) < self.max_length:
                if event.unicode.isprintable():
                    self.text += event.unicode


class MainMenu:
    WIDTH = 1920  # Bigger window (was 1400)
    HEIGHT = 1080  # Bigger window (was 900)
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Hearthstone")
        self.clock = pygame.time.Clock()
        
        # Sound manager
        self.sound_manager = get_sound_manager()
        
        # Music manager
        self.music_manager = get_music_manager()
        
        # Fonts
        self.title_font = pygame.font.Font(None, 120)
        self.subtitle_font = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 36)
        
        # Current screen
        self.current_screen = "main"  # main, local_setup, online_setup, connecting
        
        # Game start flag
        self.should_start_game = False
        self.game_mode = None
        self.game_params = {}
        
        # Text inputs - LARGE spacing to prevent overlaps
        self.player1_input = TextInput(self.WIDTH // 2 - 200, 280, 400, 50, "Player 1")
        self.player2_input = TextInput(self.WIDTH // 2 - 200, 380, 400, 50, "Player 2")
        self.username_input = TextInput(self.WIDTH // 2 - 200, 280, 400, 50, "Your Username")
        self.server_input = TextInput(self.WIDTH // 2 - 200, 430, 400, 50, "localhost:8765")
        
        # Connection status
        self.connection_message = ""
        self.connection_status = "idle"  # idle, connecting, connected, error
        
        self.setup_buttons()
        
        # Play menu music - DISABLED
        # self.music_manager.play_menu_music()
        self.sound_manager.play('menu_open')
    
    def setup_buttons(self):
        center_x = self.WIDTH // 2
        
        # Main menu buttons - MASSIVE spacing to prevent ANY overlap with title or version
        button_start_y = 230
        button_spacing = 100
        
        self.main_buttons = [
            Button(center_x - 200, button_start_y, 400, 70, "Tutorial", self.start_tutorial),
            Button(center_x - 200, button_start_y + button_spacing, 400, 70, "Play Local", self.show_local_setup),
            Button(center_x - 200, button_start_y + button_spacing * 2, 400, 70, "Play Online", self.show_online_setup),
            Button(center_x - 200, button_start_y + button_spacing * 3, 400, 70, "Host Server", self.start_server),
            Button(center_x - 200, button_start_y + button_spacing * 4, 400, 70, "Quit", self.quit_game)
        ]
        
        # Local setup buttons - LARGE spacing
        self.local_buttons = [
            Button(center_x - 150, 500, 300, 60, "Start Game", self.start_local),
            Button(center_x - 150, 590, 300, 60, "Back", self.show_main)
        ]
        
        # Online setup buttons - LARGE spacing
        self.online_buttons = [
            Button(center_x - 150, 520, 300, 60, "Connect", self.start_online),
            Button(center_x - 150, 610, 300, 60, "Back", self.show_main)
        ]
    
    def show_main(self):
        self.current_screen = "main"
    
    def show_local_setup(self):
        self.current_screen = "local_setup"
        self.player1_input.text = "Player 1"
        self.player2_input.text = "Player 2"
    
    def show_online_setup(self):
        self.current_screen = "online_setup"
        self.username_input.text = ""
        self.server_input.text = "localhost:8765"
    
    def start_tutorial(self):
        self.should_start_game = True
        self.game_mode = "tutorial"
        self.game_params = {}
        self.sound_manager.play('menu_close')
    
    def start_local(self):
        player1_name = self.player1_input.text or "Player 1"
        player2_name = self.player2_input.text or "Player 2"
        
        self.should_start_game = True
        self.game_mode = "local"
        self.game_params = {"player1": player1_name, "player2": player2_name}
        self.sound_manager.play('menu_close')
    
    def start_online(self):
        username = self.username_input.text or "Player"
        server = self.server_input.text or "localhost:8765"
        
        # Parse server address
        if ":" in server:
            host, port = server.split(":")
            port = int(port)
        else:
            host = server
            port = 8765
        
        self.should_start_game = True
        self.game_mode = "online"
        self.game_params = {"username": username, "host": host, "port": port}
        self.sound_manager.play('menu_close')
    
    def start_server(self):
        self.should_start_game = True
        self.game_mode = "server"
        self.game_params = {}
        self.sound_manager.play('menu_close')
    
    def quit_game(self):
        pygame.quit()
        sys.exit()
    
    def set_connection_status(self, status: str, message: str = ""):
        self.connection_status = status
        self.connection_message = message
    
    def run(self) -> dict:
        """Run the menu and return the selected options"""
        running = True
        
        while running and not self.should_start_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                
                # Handle text inputs
                if self.current_screen == "local_setup":
                    self.player1_input.handle_event(event)
                    self.player2_input.handle_event(event)
                elif self.current_screen == "online_setup":
                    self.username_input.handle_event(event)
                    self.server_input.handle_event(event)
                
                # Handle buttons
                if self.current_screen == "main":
                    for button in self.main_buttons:
                        button.handle_event(event)
                elif self.current_screen == "local_setup":
                    for button in self.local_buttons:
                        button.handle_event(event)
                elif self.current_screen == "online_setup":
                    for button in self.online_buttons:
                        button.handle_event(event)
                elif self.current_screen == "connecting":
                    # Back button during connection
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.show_main()
            
            self.draw()
            self.clock.tick(60)
        
        return {"mode": self.game_mode, "params": self.game_params}
    
    def draw(self):
        # Load and draw Main Menu background image
        try:
            bg_image = pygame.image.load("Designs/Main_Menu_Background.webp")
            # Scale to fit screen
            bg_image = pygame.transform.scale(bg_image, (self.WIDTH, self.HEIGHT))
            self.screen.blit(bg_image, (0, 0))
        except:
            # Fallback to gradient background if image not found
            for y in range(self.HEIGHT):
                color_factor = y / self.HEIGHT
                color = (
                    int(BOARD_BG_TOP[0] + (BOARD_BG_BOTTOM[0] - BOARD_BG_TOP[0]) * color_factor),
                    int(BOARD_BG_TOP[1] + (BOARD_BG_BOTTOM[1] - BOARD_BG_TOP[1]) * color_factor),
                    int(BOARD_BG_TOP[2] + (BOARD_BG_BOTTOM[2] - BOARD_BG_TOP[2]) * color_factor)
                )
                pygame.draw.line(self.screen, color, (0, y), (self.WIDTH, y))
        
        if self.current_screen == "main":
            self.draw_main_menu()
        elif self.current_screen == "local_setup":
            self.draw_local_setup()
        elif self.current_screen == "online_setup":
            self.draw_online_setup()
        elif self.current_screen == "connecting":
            self.draw_connecting()
        
        pygame.display.flip()
    
    def draw_main_menu(self):
        # Enhanced title with better styling
        title_text = "HEARTHSTONE"
        
        # Large outer glow for depth
        for i in range(5, 0, -1):
            glow_size = 120 + (i * 3)
            glow_font = pygame.font.Font(None, glow_size)
            alpha = 40 - (i * 5)
            glow_color = (255, 200, 50, alpha)
            glow = glow_font.render(title_text, True, glow_color[:3])
            glow_rect = glow.get_rect(center=(self.WIDTH // 2, 100))
            glow_surface = pygame.Surface(glow.get_size(), pygame.SRCALPHA)
            glow_surface.blit(glow, (0, 0))
            glow_surface.set_alpha(alpha)
            self.screen.blit(glow_surface, glow_rect)
        
        # Dark outline for contrast
        outline_font = pygame.font.Font(None, 124)
        for offset_x, offset_y in [(-3, -3), (3, -3), (-3, 3), (3, 3), (-4, 0), (4, 0), (0, -4), (0, 4)]:
            outline = outline_font.render(title_text, True, (20, 15, 10))
            outline_rect = outline.get_rect(center=(self.WIDTH // 2 + offset_x, 100 + offset_y))
            self.screen.blit(outline, outline_rect)
        
        # Main title - bright gold with gradient effect
        title = self.title_font.render(title_text, True, (255, 223, 0))
        title_rect = title.get_rect(center=(self.WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Top highlight for 3D effect
        highlight_font = pygame.font.Font(None, 120)
        highlight = highlight_font.render(title_text, True, (255, 245, 150))
        highlight_rect = highlight.get_rect(center=(self.WIDTH // 2, 97))
        highlight_surface = pygame.Surface(highlight.get_size(), pygame.SRCALPHA)
        highlight_surface.blit(highlight, (0, 0))
        highlight_surface.set_alpha(120)
        self.screen.blit(highlight_surface, highlight_rect)
        
        # Buttons
        for button in self.main_buttons:
            button.draw(self.screen)
        
        # Version info with ornate styling
        version_bg = pygame.Rect(10, self.HEIGHT - 50, 100, 40)
        pygame.draw.rect(self.screen, BOARD_WOOD_DARK, version_bg, border_radius=6)
        pygame.draw.rect(self.screen, BOARD_WOOD_LIGHT, version_bg, 1, border_radius=6)
        
        version = self.font.render("v1.0.0", True, TEXT_GOLD)
        version_shadow = self.font.render("v1.0.0", True, BLACK)
        version_rect = version.get_rect(center=version_bg.center)
        self.screen.blit(version_shadow, (version_rect.x + 1, version_rect.y + 1))
        self.screen.blit(version, version_rect)
    
    def draw_local_setup(self):
        # Title
        title = self.subtitle_font.render("Local Game Setup", True, (255, 215, 0))
        title_shadow = self.subtitle_font.render("Local Game Setup", True, BLACK)
        title_rect = title.get_rect(center=(self.WIDTH // 2, 80))
        self.screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
        self.screen.blit(title, title_rect)
        
        # Instructions - LARGE gap from title
        inst = self.font.render("Enter player names:", True, BUTTON_TEXT)
        inst_shadow = self.font.render("Enter player names:", True, BLACK)
        inst_rect = inst.get_rect(center=(self.WIDTH // 2, 200))
        self.screen.blit(inst_shadow, (inst_rect.x + 1, inst_rect.y + 1))
        self.screen.blit(inst, inst_rect)
        
        # Text inputs - LARGE spacing
        self.player1_input.rect.y = 280
        self.player2_input.rect.y = 380
        
        self.player1_input.draw(self.screen)
        self.player2_input.draw(self.screen)
        
        # Buttons
        for button in self.local_buttons:
            button.draw(self.screen)
    
    def draw_online_setup(self):
        # Title
        title = self.subtitle_font.render("Online Multiplayer", True, (255, 215, 0))
        title_shadow = self.subtitle_font.render("Online Multiplayer", True, BLACK)
        title_rect = title.get_rect(center=(self.WIDTH // 2, 80))
        self.screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
        self.screen.blit(title, title_rect)
        
        # Username instruction - LARGE gap from title
        inst1 = self.font.render("Enter your username:", True, BUTTON_TEXT)
        inst1_shadow = self.font.render("Enter your username:", True, BLACK)
        inst1_rect = inst1.get_rect(center=(self.WIDTH // 2, 200))
        self.screen.blit(inst1_shadow, (inst1_rect.x + 1, inst1_rect.y + 1))
        self.screen.blit(inst1, inst1_rect)
        
        # Username input - LARGE spacing
        self.username_input.rect.y = 280
        self.username_input.draw(self.screen)
        
        # Server instruction - LARGE gap
        inst2 = self.font.render("Server address:", True, BUTTON_TEXT)
        inst2_shadow = self.font.render("Server address:", True, BLACK)
        inst2_rect = inst2.get_rect(center=(self.WIDTH // 2, 370))
        self.screen.blit(inst2_shadow, (inst2_rect.x + 1, inst2_rect.y + 1))
        self.screen.blit(inst2, inst2_rect)
        
        # Server input - LARGE spacing
        self.server_input.rect.y = 430
        self.server_input.draw(self.screen)
        
        # Buttons - LARGE gap from inputs
        for button in self.online_buttons:
            button.draw(self.screen)
        
        # Info banner - LARGE gap below buttons
        info = self.font.render("Make sure the server is running first!", True, (255, 215, 0))
        info_shadow = self.font.render("Make sure the server is running first!", True, BLACK)
        info_rect = info.get_rect(center=(self.WIDTH // 2, 720))
        self.screen.blit(info_shadow, (info_rect.x + 1, info_rect.y + 1))
        self.screen.blit(info, info_rect)
    
    def draw_connecting(self):
        # Ornate connecting banner
        banner_rect = pygame.Rect(self.WIDTH // 2 - 300, 280, 600, 200)
        
        # Background with gradient
        banner_surface = pygame.Surface((600, 200), pygame.SRCALPHA)
        for i in range(200):
            alpha = 240 - (abs(i - 100))
            color = (*BOARD_WOOD_DARK[:3], alpha)
            pygame.draw.line(banner_surface, color, (0, i), (600, i))
        
        self.screen.blit(banner_surface, banner_rect.topleft)
        
        # Ornate border
        pygame.draw.rect(self.screen, CARD_BORDER_GOLD, banner_rect, 4, border_radius=15)
        pygame.draw.rect(self.screen, BOARD_WOOD_LIGHT, banner_rect.inflate(-8, -8), 2, border_radius=13)
        
        # Title with glow
        title = self.subtitle_font.render("Connecting...", True, TEXT_GOLD)
        title_shadow = self.subtitle_font.render("Connecting...", True, BLACK)
        title_rect = title.get_rect(center=(self.WIDTH // 2, 330))
        self.screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
        self.screen.blit(title, title_rect)
        
        # Status message
        msg = self.font.render(self.connection_message, True, BUTTON_TEXT)
        msg_shadow = self.font.render(self.connection_message, True, BLACK)
        msg_rect = msg.get_rect(center=(self.WIDTH // 2, 390))
        self.screen.blit(msg_shadow, (msg_rect.x + 1, msg_rect.y + 1))
        self.screen.blit(msg, msg_rect)
        
        # Animated dots
        dots = "." * ((pygame.time.get_ticks() // 500) % 4)
        dots_text = self.subtitle_font.render(dots, True, TEXT_GOLD)
        dots_rect = dots_text.get_rect(center=(self.WIDTH // 2, 430))
        self.screen.blit(dots_text, dots_rect)
        
        # Cancel instruction
        cancel = self.font.render("Press ESC to cancel", True, GRAY)
        cancel_shadow = self.font.render("Press ESC to cancel", True, BLACK)
        cancel_rect = cancel.get_rect(center=(self.WIDTH // 2, 540))
        self.screen.blit(cancel_shadow, (cancel_rect.x + 1, cancel_rect.y + 1))
        self.screen.blit(cancel, cancel_rect)

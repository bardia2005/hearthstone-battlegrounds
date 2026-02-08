"""
Online multiplayer GUI for Hearthstone
Integrates with network client for real-time multiplayer
"""

import pygame
import asyncio
from typing import Optional, Dict, Any
from .game_gui import GameGUI
from .colors import *
from client.network_client import NetworkClient


class OnlineGameGUI(GameGUI):
    def __init__(self, client: NetworkClient, player_id: str):
        # Don't call super().__init__ yet - we need to wait for game state
        self.client = client
        self.player_id = player_id
        self.game_state: Optional[Dict] = None
        self.waiting_for_state = True
        self.match_found = False
        self.opponent_name = "Waiting..."
        
        # Initialize pygame
        pygame.init()
        self.WIDTH = 1400
        self.HEIGHT = 900
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Hearthstone - Online Match")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 48)
        
        # Register callbacks
        self.client.on("game_state", self.on_game_state)
        self.client.on("match_found", self.on_match_found)
        self.client.on("your_turn", self.on_your_turn)
        self.client.on("game_over", self.on_game_over)
        self.client.on("opponent_disconnected", self.on_opponent_disconnected)
        self.client.on("error", self.on_error)
        self.client.on("action_success", self.on_action_success)
        
        # Game state
        self.selected_card_index = None
        self.selected_minion_index = None
        self.dragging = False
        self.drag_pos = (0, 0)
        self.hover_card_index = None
        self.targeting_mode = False
        self.message = ""
        self.message_timer = 0
        self.game_over_state = None
        
        # Layout positions
        self.hand_y = self.HEIGHT - 200
        self.player_board_y = self.HEIGHT // 2 + 60
        self.opponent_board_y = self.HEIGHT // 2 - 160
        self.player_hero_y = self.HEIGHT - 220
        self.opponent_hero_y = 40
    
    def on_game_state(self, data: Dict):
        """Handle game state update from server"""
        self.game_state = data.get("state")
        self.waiting_for_state = False
    
    def on_match_found(self, data: Dict):
        """Handle match found"""
        self.match_found = True
        self.opponent_name = data.get("opponent", "Opponent")
        self.show_message(f"Match found! vs {self.opponent_name}")
    
    def on_your_turn(self, data: Dict):
        """Handle your turn notification"""
        self.show_message("Your turn!")
    
    def on_game_over(self, data: Dict):
        """Handle game over"""
        self.game_over_state = data
        result = data.get("result")
        reason = data.get("reason")
        
        if result == "victory":
            self.show_message("Victory!")
        else:
            self.show_message("Defeat!")
    
    def on_opponent_disconnected(self, data: Dict):
        """Handle opponent disconnection"""
        self.show_message("Opponent disconnected!")
    
    def on_error(self, data: Dict):
        """Handle error from server"""
        message = data.get("message", "An error occurred")
        self.show_message(f"Error: {message}")
    
    def on_action_success(self, data: Dict):
        """Handle action success confirmation"""
        pass  # State will be updated via game_state message
    
    def show_message(self, msg: str):
        """Show a message to the player"""
        self.message = msg
        self.message_timer = 120
    
    async def run_async(self):
        """Async run loop"""
        running = True
        
        while running:
            # Handle pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.waiting_for_state:
                    await self.handle_click(event.pos, event.button)
                elif event.type == pygame.MOUSEBUTTONUP and not self.waiting_for_state:
                    await self.handle_release(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_motion(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.waiting_for_state:
                        await self.end_turn()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
            
            self.update()
            self.draw_online()
            self.clock.tick(60)
            
            # Allow other async tasks to run
            await asyncio.sleep(0)
        
        # Disconnect from server
        await self.client.disconnect()
    
    def update(self):
        """Update game state"""
        if self.message_timer > 0:
            self.message_timer -= 1
    
    def draw_online(self):
        """Draw the online game"""
        # Background
        for y in range(self.HEIGHT):
            color_factor = y / self.HEIGHT
            color = (
                int(BOARD_BG[0] + (BOARD_CENTER[0] - BOARD_BG[0]) * color_factor),
                int(BOARD_BG[1] + (BOARD_CENTER[1] - BOARD_BG[1]) * color_factor),
                int(BOARD_BG[2] + (BOARD_CENTER[2] - BOARD_BG[2]) * color_factor)
            )
            pygame.draw.line(self.screen, color, (0, y), (self.WIDTH, y))
        
        if self.waiting_for_state or not self.game_state:
            self.draw_waiting_screen()
        else:
            self.draw_game_state()
        
        # Draw message
        if self.message_timer > 0:
            self.draw_message()
        
        # Draw game over screen
        if self.game_over_state:
            self.draw_game_over_online()
        
        pygame.display.flip()
    
    def draw_waiting_screen(self):
        """Draw waiting for match screen"""
        text = self.large_font.render("Waiting for match...", True, WHITE)
        text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        self.screen.blit(text, text_rect)
        
        if self.match_found:
            opponent_text = self.font.render(f"Opponent: {self.opponent_name}", True, CARD_SELECTED)
            opponent_rect = opponent_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 60))
            self.screen.blit(opponent_text, opponent_rect)
    
    def draw_game_state(self):
        """Draw the current game state"""
        if not self.game_state:
            return
        
        player_state = self.game_state.get("player", {})
        opponent_state = self.game_state.get("opponent", {})
        
        # Draw board center
        center_rect = pygame.Rect(100, 250, self.WIDTH - 200, 400)
        pygame.draw.rect(self.screen, BOARD_CENTER, center_rect, border_radius=20)
        pygame.draw.rect(self.screen, CARD_BORDER, center_rect, 3, border_radius=20)
        
        # Draw center line
        pygame.draw.line(self.screen, DARK_GRAY, 
                        (150, self.HEIGHT // 2), 
                        (self.WIDTH - 150, self.HEIGHT // 2), 3)
        
        # Draw heroes
        self.draw_heroes_online(player_state, opponent_state)
        
        # Draw boards
        self.draw_board_online(opponent_state.get("board", []), self.opponent_board_y, False)
        self.draw_board_online(player_state.get("board", []), self.player_board_y, True)
        
        # Draw hand
        self.draw_hand_online(player_state.get("hand", []))
        
        # Draw mana
        self.draw_mana_online(player_state)
        
        # Draw deck info
        self.draw_deck_info_online(player_state, opponent_state)
        
        # Draw turn indicator
        self.draw_turn_indicator_online()
        
        # Draw end turn button
        self.draw_end_turn_button()
        
        # Draw dragged card
        if self.dragging and self.selected_card_index is not None:
            # Would need card renderer - simplified for now
            pass
        
        # Draw targeting arrow
        if self.targeting_mode and self.selected_minion_index is not None:
            self.draw_targeting_arrow()
    
    def draw_heroes_online(self, player_state: Dict, opponent_state: Dict):
        """Draw heroes"""
        # Opponent hero
        hero_x = self.WIDTH // 2 - 60
        pygame.draw.rect(self.screen, CARD_BG, (hero_x, self.opponent_hero_y, 120, 100), border_radius=10)
        pygame.draw.rect(self.screen, CARD_BORDER, (hero_x, self.opponent_hero_y, 120, 100), 2, border_radius=10)
        
        name_text = self.small_font.render(opponent_state.get("name", "Opponent"), True, WHITE)
        self.screen.blit(name_text, (hero_x + 10, self.opponent_hero_y + 10))
        
        health_text = self.font.render(f"{opponent_state.get('health', 30)}", True, HEALTH_RED)
        self.screen.blit(health_text, (hero_x + 45, self.opponent_hero_y + 50))
        
        # Player hero
        pygame.draw.rect(self.screen, CARD_BG, (hero_x, self.player_hero_y, 120, 100), border_radius=10)
        pygame.draw.rect(self.screen, CARD_BORDER, (hero_x, self.player_hero_y, 120, 100), 2, border_radius=10)
        
        name_text = self.small_font.render(player_state.get("name", "You"), True, WHITE)
        self.screen.blit(name_text, (hero_x + 10, self.player_hero_y + 10))
        
        health_text = self.font.render(f"{player_state.get('health', 30)}", True, HEALTH_RED)
        self.screen.blit(health_text, (hero_x + 45, self.player_hero_y + 50))
    
    def draw_board_online(self, board: list, y: int, is_player: bool):
        """Draw minions on board"""
        if not board:
            return
        
        total_width = len(board) * 100
        start_x = (self.WIDTH - total_width) // 2
        
        for i, minion in enumerate(board):
            x = start_x + i * 100
            
            # Draw minion card
            pygame.draw.rect(self.screen, CARD_BG, (x, y, 90, 110), border_radius=8)
            pygame.draw.rect(self.screen, CARD_BORDER, (x, y, 90, 110), 2, border_radius=8)
            
            # Name
            name_text = self.small_font.render(minion.get("name", "")[:8], True, WHITE)
            self.screen.blit(name_text, (x + 5, y + 5))
            
            # Attack/Health
            stats_text = self.font.render(f"{minion.get('attack')}/{minion.get('health')}", True, WHITE)
            self.screen.blit(stats_text, (x + 20, y + 60))
    
    def draw_hand_online(self, hand: list):
        """Draw player's hand"""
        if not hand:
            return
        
        hand_bg = pygame.Rect(0, self.hand_y - 10, self.WIDTH, 190)
        pygame.draw.rect(self.screen, HAND_BG, hand_bg)
        
        total_width = len(hand) * 85
        start_x = (self.WIDTH - total_width) // 2
        
        for i, card in enumerate(hand):
            if self.dragging and i == self.selected_card_index:
                continue
            
            x = start_x + i * 85
            y = self.hand_y
            
            if i == self.hover_card_index:
                y -= 20
            
            # Draw card
            pygame.draw.rect(self.screen, CARD_BG, (x, y, 100, 140), border_radius=8)
            pygame.draw.rect(self.screen, CARD_BORDER, (x, y, 100, 140), 2, border_radius=8)
            
            # Mana cost
            pygame.draw.circle(self.screen, MANA_BLUE, (x + 15, y + 15), 12)
            cost_text = self.small_font.render(str(card.get("mana_cost", 0)), True, WHITE)
            self.screen.blit(cost_text, (x + 10, y + 8))
            
            # Name
            name_text = self.small_font.render(card.get("name", "")[:10], True, WHITE)
            self.screen.blit(name_text, (x + 5, y + 40))
            
            # Stats if minion
            if card.get("type") == "minion":
                stats_text = self.font.render(f"{card.get('attack')}/{card.get('health')}", True, WHITE)
                self.screen.blit(stats_text, (x + 25, y + 100))
    
    def draw_mana_online(self, player_state: Dict):
        """Draw mana display"""
        mana_x = 30
        mana_y = self.HEIGHT - 60
        
        mana_text = f"{player_state.get('mana', 0)}/{player_state.get('max_mana', 0)}"
        text_surface = self.large_font.render(mana_text, True, MANA_BLUE)
        text_rect = text_surface.get_rect(center=(mana_x + 60, mana_y))
        
        pygame.draw.circle(self.screen, (0, 0, 0, 180), (mana_x + 60, mana_y), 45)
        pygame.draw.circle(self.screen, MANA_BLUE, (mana_x + 60, mana_y), 45, 3)
        
        self.screen.blit(text_surface, text_rect)
    
    def draw_deck_info_online(self, player_state: Dict, opponent_state: Dict):
        """Draw deck information"""
        deck_x = self.WIDTH - 120
        
        # Opponent
        deck_y = 80
        info_bg = pygame.Rect(deck_x - 10, deck_y - 10, 110, 70)
        pygame.draw.rect(self.screen, (0, 0, 0, 150), info_bg, border_radius=8)
        
        deck_text = self.small_font.render(f"Deck: {opponent_state.get('deck_size', 0)}", True, WHITE)
        self.screen.blit(deck_text, (deck_x, deck_y))
        hand_text = self.small_font.render(f"Hand: {opponent_state.get('hand_size', 0)}", True, WHITE)
        self.screen.blit(hand_text, (deck_x, deck_y + 30))
        
        # Player
        player_deck_y = self.HEIGHT - 180
        player_info_bg = pygame.Rect(deck_x - 10, player_deck_y - 10, 110, 50)
        pygame.draw.rect(self.screen, (0, 0, 0, 150), player_info_bg, border_radius=8)
        
        deck_text = self.small_font.render(f"Deck: {player_state.get('deck_size', 0)}", True, WHITE)
        self.screen.blit(deck_text, (deck_x, player_deck_y))
    
    def draw_turn_indicator_online(self):
        """Draw turn indicator"""
        if not self.game_state:
            return
        
        turn = self.game_state.get("turn", 1)
        your_turn = self.game_state.get("your_turn", False)
        
        turn_text = f"Turn {turn}"
        if your_turn:
            turn_text += " - YOUR TURN"
        
        text_surface = self.large_font.render(turn_text, True, CARD_SELECTED if your_turn else WHITE)
        text_rect = text_surface.get_rect(center=(self.WIDTH // 2, 30))
        
        bg_rect = text_rect.inflate(40, 20)
        pygame.draw.rect(self.screen, (0, 0, 0, 180), bg_rect, border_radius=10)
        
        self.screen.blit(text_surface, text_rect)
    
    def draw_message(self):
        """Draw message overlay"""
        msg_surface = pygame.Surface((400, 60), pygame.SRCALPHA)
        msg_surface.fill((0, 0, 0, 180))
        
        text = self.font.render(self.message, True, WHITE)
        text_rect = text.get_rect(center=(200, 30))
        msg_surface.blit(text, text_rect)
        
        self.screen.blit(msg_surface, (self.WIDTH // 2 - 200, self.HEIGHT // 2 - 30))
    
    def draw_game_over_online(self):
        """Draw game over screen"""
        overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        result = self.game_over_state.get("result", "")
        color = CARD_SELECTED if result == "victory" else HEALTH_RED
        
        text = self.large_font.render(result.upper(), True, color)
        text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        self.screen.blit(text, text_rect)
        
        inst_text = self.font.render("Close window to exit", True, WHITE)
        inst_rect = inst_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 50))
        self.screen.blit(inst_text, inst_rect)
    
    async def handle_click(self, pos, button):
        """Handle mouse click"""
        if not self.game_state or not self.game_state.get("your_turn"):
            return
        
        if button == 3:  # Right click
            self.selected_card_index = None
            self.selected_minion_index = None
            self.targeting_mode = False
            return
        
        # Check end turn button
        if self.is_end_turn_clicked(pos):
            await self.end_turn()
            return
        
        # Check hand cards
        card_index = self.get_hand_card_at_pos(pos)
        if card_index is not None:
            self.selected_card_index = card_index
            self.dragging = True
            self.drag_pos = pos
            return
        
        # Check player minions for attack
        minion_index = self.get_player_minion_at_pos(pos)
        if minion_index is not None:
            self.selected_minion_index = minion_index
            self.targeting_mode = True
            return
    
    async def handle_release(self, pos):
        """Handle mouse release"""
        if self.dragging and self.selected_card_index is not None:
            # Play card
            await self.client.play_card(self.selected_card_index, None)
        
        self.dragging = False
        self.selected_card_index = None
    
    def handle_motion(self, pos):
        """Handle mouse motion"""
        self.drag_pos = pos
        self.hover_card_index = self.get_hand_card_at_pos(pos)
    
    async def end_turn(self):
        """End turn"""
        await self.client.end_turn()
        self.selected_card_index = None
        self.selected_minion_index = None
        self.targeting_mode = False
    
    def get_hand_card_at_pos(self, pos):
        """Get card index at position"""
        if not self.game_state:
            return None
        
        hand = self.game_state.get("player", {}).get("hand", [])
        if not hand:
            return None
        
        total_width = len(hand) * 85
        start_x = (self.WIDTH - total_width) // 2
        
        for i in range(len(hand)):
            x = start_x + i * 85
            rect = pygame.Rect(x, self.hand_y - 30, 100, 180)
            if rect.collidepoint(pos):
                return i
        return None
    
    def get_player_minion_at_pos(self, pos):
        """Get player minion index at position"""
        if not self.game_state:
            return None
        
        board = self.game_state.get("player", {}).get("board", [])
        if not board:
            return None
        
        total_width = len(board) * 100
        start_x = (self.WIDTH - total_width) // 2
        
        for i in range(len(board)):
            x = start_x + i * 100
            rect = pygame.Rect(x, self.player_board_y, 90, 110)
            if rect.collidepoint(pos):
                return i
        return None
    
    def is_end_turn_clicked(self, pos):
        """Check if end turn button was clicked"""
        button_width = 140
        button_height = 70
        button_x = self.WIDTH - button_width - 30
        button_y = self.HEIGHT // 2 - button_height // 2
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        return button_rect.collidepoint(pos)
    
    def draw_targeting_arrow(self):
        """Draw targeting arrow"""
        if not self.game_state or self.selected_minion_index is None:
            return
        
        board = self.game_state.get("player", {}).get("board", [])
        total_width = len(board) * 100
        start_x = (self.WIDTH - total_width) // 2
        minion_x = start_x + self.selected_minion_index * 100 + 45
        minion_y = self.player_board_y + 55
        
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.line(self.screen, CARD_SELECTED, (minion_x, minion_y), mouse_pos, 4)
        pygame.draw.circle(self.screen, HEALTH_RED, mouse_pos, 10)

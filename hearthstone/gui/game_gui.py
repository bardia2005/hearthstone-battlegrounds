import pygame
from .colors import *
from .card_renderer import CardRenderer
from .sound_manager import get_sound_manager
from .music_manager import get_music_manager
from .tutorial import TutorialOverlay, create_tutorial_steps


class GameGUI:
    WIDTH = 1920  # Bigger window (was 1600)
    HEIGHT = 1080  # Bigger window (was 900)
    
    def __init__(self, game, online_mode=False, tutorial_mode=False):
        self.game = game
        self.online_mode = online_mode
        self.tutorial_mode = tutorial_mode
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Hearthstone")
        
        self.clock = pygame.time.Clock()
        self.renderer = CardRenderer()
        self.sound_manager = get_sound_manager()
        self.music_manager = get_music_manager()
        
        # Store player IDs at game start to prevent hero card swapping
        self.player1_id = id(game.player1)
        self.player2_id = id(game.player2)
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 22)
        self.tiny_font = pygame.font.Font(None, 18)
        self.large_font = pygame.font.Font(None, 48)
        
        # Game state
        self.selected_card_index = None
        self.selected_minion_index = None
        self.dragging = False
        self.drag_pos = (0, 0)
        self.hover_card_index = None
        self.targeting_mode = False
        self.message = ""
        self.message_timer = 0
        
        # Layout positions - COMPLETELY FIXED to prevent ALL overlaps
        # Right side reserved for game log (280px from right edge)
        self.log_width = 280
        self.log_x = self.WIDTH - self.log_width - 10
        self.game_area_width = self.log_x - 10
        
        # Vertical layout - Will be updated after table is cached
        self.opponent_hero_y = 30
        # These will be set after table caching
        self.opponent_board_y = 0
        self.center_y = self.HEIGHT // 2  # Exact center: 540
        self.player_board_y = 0
        self.player_hero_y = 0
        self.hand_y = 0
        
        # Horizontal positions - SPREAD OUT to prevent overlaps
        self.left_margin = 15
        self.hero_x = 200  # Hero MUCH further right, away from deck info
        
        # Calculate the vertical gold line position (right edge of game area)
        # The gold line is at board_right which is game_area_width - 50
        vertical_line_x = self.game_area_width - 50 - 10  # Moved 10px to the left
        
        # All three elements vertically stacked and centered on the same vertical line
        button_width = 120  # Wider, more square
        button_height = 120  # Shorter, more square
        
        # End turn button - MOVED HIGHER (closer to center line)
        # Position button so its CENTER is on the vertical line
        self.end_turn_x = vertical_line_x - (button_width // 2)
        # Align button CENTER slightly ABOVE the horizontal center line
        self.end_turn_y = self.center_y - (button_height // 2) - 40  # Moved 40px higher
        
        # Calculate exact center x (should be on vertical line)
        center_x = vertical_line_x
        
        # Hero power button - ABOVE end turn, SAME CENTER LINE, SLIGHTLY LOWER
        hero_power_size = 85
        self.hero_power_x = center_x - (hero_power_size // 2)  # Center aligned
        self.hero_power_y = self.end_turn_y - hero_power_size - 12  # 12px gap above end turn (was 15px)
        
        # Mana crystals - BELOW end turn button, SAME CENTER LINE, MOVED LOWER
        self.mana_x = center_x  # Exact center alignment
        # Position mana below the end turn button with larger gap
        self.mana_y = self.end_turn_y + button_height + 60  # 60px below end turn button (was 40px)
        
        # Deck info - TOP RIGHT corner (moved from left side)
        self.deck_info_x = self.log_x - 120  # Left of the log panel
        self.deck_info_y_opponent = 15  # Top right
        self.deck_info_y_player = 80  # Below opponent deck info
        
        # Tutorial system (must be after layout positions are defined)
        self.tutorial = TutorialOverlay(self.WIDTH, self.HEIGHT)
        # Enable tutorial in tutorial mode
        if tutorial_mode:
            self.tutorial.steps = create_tutorial_steps(self)
            self.tutorial.start()
        
        # Animation state
        self.animations = []
        self.card_hover_offset = 0
        self.card_hover_target = 0
        
        # Game log panel
        self.show_log = True
        self.log_scroll = 0
        
        # CACHE BACKGROUND IMAGE - load once, not every frame
        self.cached_background = None
        try:
            bg_image = pygame.image.load("Designs/Game_Background.webp")
            # Scale to fit screen ONCE
            self.cached_background = pygame.transform.scale(bg_image, (self.WIDTH, self.HEIGHT))
        except Exception as e:
            print(f"Failed to load Game_Background.webp: {e}")
            # Will use gradient fallback
        
        # CACHE TABLE IMAGE - load once, not every frame
        # Calculate table dimensions
        board_left = 50
        board_right = self.game_area_width - 50
        board_width = board_right - board_left
        table_height = 630
        table_start_y = (self.HEIGHT - table_height) // 2 - 45
        
        # Stretch table wider and TALLER (1.3x height instead of 1.035x)
        stretched_width = int(board_width * 1.2 * 0.9)
        stretched_height = int(table_height * 1.3)
        
        # Center the stretched table
        table_x = board_left - (stretched_width - board_width) // 2
        table_y = table_start_y - (stretched_height - table_height) // 2
        
        # Load and cache table image
        self.cached_table = None
        self.cached_table_pos = (table_x, table_y)
        self.table_actual_width = stretched_width
        self.table_actual_height = stretched_height
        self.table_actual_left = table_x
        self.table_actual_right = table_x + stretched_width
        self.table_actual_top = table_y
        self.table_actual_bottom = table_y + stretched_height
        try:
            table_image = pygame.image.load("Designs/TableMain.png")
            # Scale to stretched dimensions
            self.cached_table = pygame.transform.smoothscale(table_image, (stretched_width, stretched_height))
        except Exception as e:
            print(f"Failed to load TableMain.png: {e}")
            # No cached table - will use fallback drawing
        
        # NOW update board positions based on stretched table
        # Hero cards from Heroes folder - sized to fit PERFECTLY in arch slots
        hero_height = 260  # Fit arch height
        hero_width = 220   # Fit arch width
        
        # Calculate exact positions based on the table image
        # SWAPPED: Player 1 (bottom) hero - in the BOTTOM ARCH SLOT (CORRECT - checkmark)
        self.opponent_hero_y = self.table_actual_bottom - hero_height - 45  # Perfect fit
        # SWAPPED: Player 1 minions - above player 1 hero (BLUE AREA at bottom)
        self.opponent_board_y = self.opponent_hero_y - 260 - 70
        
        # SWAPPED: Player 2 (top) hero - in the TOP ARCH SLOT (needs to be LOWER - was X)
        self.player_hero_y = self.table_actual_top + 55  # Moved DOWN significantly to fit arch
        # SWAPPED: Player 2 minions - below player 2 hero (RED AREA at top)
        self.player_board_y = self.player_hero_y + hero_height + 70
        
        # Calculate hand position below stretched table
        table_bottom = self.table_actual_bottom
        available_space = self.HEIGHT - table_bottom
        card_height = 261
        self.hand_y = (self.HEIGHT + table_bottom - card_height) // 2 - 10
        
        # Start first turn
        if not online_mode:
            self.game.play_turn()
        
        # Start game music - DISABLED
        # self.music_manager.crossfade_to_game()
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Tutorial handles events first
                if self.tutorial.active and self.tutorial.handle_event(event):
                    continue
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos, event.button)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.handle_release(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_motion(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not self.tutorial.active:
                            self.end_turn()
                    elif event.key == pygame.K_TAB:
                        self.show_log = not self.show_log
                    elif event.key == pygame.K_ESCAPE:
                        if not self.tutorial.active:
                            running = False
            
            self.update()
            self.draw()
            self.clock.tick(60)
    
    def handle_click(self, pos, button):
        if self.game.game_over:
            return
        
        if button == 3:  # Right click to cancel
            self.sound_manager.play('button_click')
            self.selected_card_index = None
            self.selected_minion_index = None
            self.targeting_mode = False
            return
        
        # Check end turn button
        if self.is_end_turn_clicked(pos):
            self.end_turn()
            return
        
        # If in targeting mode, check for target selection
        if self.targeting_mode:
            target = self.get_target_at_pos(pos)
            if target:
                self.execute_action(target)
            return
        
        # Check hand cards
        card_index = self.get_hand_card_at_pos(pos)
        if card_index is not None:
            card = self.game.current_player.hand[card_index]
            if card.can_play(self.game.current_player):
                self.selected_card_index = card_index
                self.dragging = True
                self.drag_pos = pos
                self.sound_manager.play('button_hover')
            else:
                self.show_message("Not enough mana!")
                self.sound_manager.play('error')
            return
        
        # Check player's minions for attack
        minion_index = self.get_player_minion_at_pos(pos)
        if minion_index is not None:
            minion = self.game.current_player.board[minion_index]
            if minion.can_attack and minion.attack > 0:
                self.selected_minion_index = minion_index
                self.targeting_mode = True
                self.sound_manager.play('button_hover')
            elif not minion.can_attack:
                self.show_message("This minion can't attack yet!")
                self.sound_manager.play('error')
            return
    
    def handle_release(self, pos):
        if self.dragging and self.selected_card_index is not None:
            # Check if dropped on board area (play the card)
            if self.is_on_player_board(pos):
                self.play_selected_card(pos)
            elif self.is_on_target(pos):
                target = self.get_target_at_pos(pos)
                self.play_selected_card(pos, target)
        
        self.dragging = False
        self.selected_card_index = None
    
    def handle_motion(self, pos):
        self.drag_pos = pos
        
        # Update hover state
        self.hover_card_index = self.get_hand_card_at_pos(pos)
    
    def play_selected_card(self, pos, target=None):
        if self.selected_card_index is None:
            return
        
        card = self.game.current_player.hand[self.selected_card_index]
        
        # Check if spell needs target
        if hasattr(card, 'requires_target') and card.requires_target and target is None:
            self.show_message("This spell needs a target!")
            self.sound_manager.play('error')
            return
        
        # Check board space for minions
        if hasattr(card, 'attack') and len(self.game.current_player.board) >= 7:
            self.show_message("Board is full!")
            self.sound_manager.play('error')
            return
        
        if self.game.play_card(self.selected_card_index, target):
            self.sound_manager.play('card_play')
            self.check_game_over()
        else:
            self.sound_manager.play('error')
        
        self.selected_card_index = None
    
    def execute_action(self, target):
        if self.selected_minion_index is not None:
            # Attack with minion
            opponent = self.game.get_opponent(self.game.current_player)
            
            # Check taunt
            if opponent.has_taunt():
                if hasattr(target, 'taunt') and not target.taunt:
                    self.show_message("Must attack a Taunt minion!")
                    self.sound_manager.play('error')
                    self.targeting_mode = False
                    self.selected_minion_index = None
                    return
                if target == opponent:
                    self.show_message("Must attack a Taunt minion!")
                    self.sound_manager.play('error')
                    self.targeting_mode = False
                    self.selected_minion_index = None
                    return
            
            if self.game.attack_with_minion(self.selected_minion_index, target):
                self.sound_manager.play('attack')
            else:
                self.sound_manager.play('error')
            self.check_game_over()
        
        self.targeting_mode = False
        self.selected_minion_index = None
        self.selected_card_index = None
    
    def end_turn(self):
        self.sound_manager.play('end_turn')
        self.game.end_turn()
        if not self.game.game_over:
            self.game.play_turn()
            self.sound_manager.play('card_draw')
        self.selected_card_index = None
        self.selected_minion_index = None
        self.targeting_mode = False
        self.check_game_over()
    
    def check_game_over(self):
        if self.game.game_over:
            if self.game.winner == self.game.current_player:
                self.sound_manager.play('victory')
            else:
                self.sound_manager.play('defeat')
            self.show_message(f"{self.game.winner.name} wins!")
    
    def show_message(self, msg):
        self.message = msg
        self.message_timer = 120  # 2 seconds at 60fps
    
    def update(self):
        if self.message_timer > 0:
            self.message_timer -= 1
        
        # Smooth card hover animation
        if self.card_hover_offset < self.card_hover_target:
            self.card_hover_offset += 2
        elif self.card_hover_offset > self.card_hover_target:
            self.card_hover_offset -= 2
        
        # Update tutorial
        if self.tutorial.active:
            self.tutorial.update()
    
    def draw(self):
        # Draw cached background image (loaded once in __init__, not every frame)
        if self.cached_background:
            self.screen.blit(self.cached_background, (0, 0))
        else:
            # Fallback to gradient background if image not found
            for y in range(self.HEIGHT):
                color_factor = y / self.HEIGHT
                color = (
                    int(BOARD_BG_TOP[0] + (BOARD_BG_BOTTOM[0] - BOARD_BG_TOP[0]) * color_factor),
                    int(BOARD_BG_TOP[1] + (BOARD_BG_BOTTOM[1] - BOARD_BG_TOP[1]) * color_factor),
                    int(BOARD_BG_TOP[2] + (BOARD_BG_BOTTOM[2] - BOARD_BG_TOP[2]) * color_factor)
                )
                pygame.draw.line(self.screen, color, (0, y), (self.WIDTH, y))
        
        # Draw cached table image (loaded once in __init__, not every frame)
        if self.cached_table:
            # Simply blit the cached, pre-scaled table
            self.screen.blit(self.cached_table, self.cached_table_pos)
        else:
            # Fallback to drawn table if image failed to load
            board_left = 50
            board_right = self.game_area_width - 50
            board_width = board_right - board_left
            table_height = 630
            table_start_y = (self.HEIGHT - table_height) // 2 - 45
            board_top = table_start_y
            board_bottom = table_start_y + table_height
            
            center_rect = pygame.Rect(board_left, board_top, board_width, table_height)
            pygame.draw.rect(self.screen, BOARD_CENTER, center_rect, border_radius=25)
            pygame.draw.rect(self.screen, BOARD_WOOD_DARK, center_rect, 8, border_radius=25)
            pygame.draw.rect(self.screen, CARD_BORDER_GOLD, center_rect.inflate(-8, -8), 3, border_radius=23)
            pygame.draw.rect(self.screen, BOARD_WOOD_LIGHT, center_rect.inflate(-14, -14), 2, border_radius=21)
            center_y = (board_top + board_bottom) // 2
            pygame.draw.line(self.screen, BOARD_WOOD_DARK, (board_left + 40, center_y), (board_right - 40, center_y), 5)
            pygame.draw.line(self.screen, CARD_BORDER_GOLD, (board_left + 40, center_y - 2), (board_right - 40, center_y - 2), 2)
            pygame.draw.line(self.screen, CARD_BORDER_GOLD, (board_left + 40, center_y + 2), (board_right - 40, center_y + 2), 2)
        
        # Draw game log panel (right side) - always visible
        if self.show_log:
            self.draw_game_log()
        
        # Draw turn indicator FIRST (so it doesn't overlap log)
        self.draw_turn_indicator()
        
        # Draw deck counts
        self.draw_deck_info()
        
        # Draw heroes
        self.draw_heroes()
        
        # Draw boards
        self.draw_board(self.game.get_opponent(self.game.current_player), self.opponent_board_y, False)
        self.draw_board(self.game.current_player, self.player_board_y, True)
        
        # Draw mana crystals BEFORE hand (so hand doesn't cover it)
        self.draw_mana()
        
        # Draw hero power button
        self.draw_hero_power_button()
        
        # Draw end turn button
        self.draw_end_turn_button()
        
        # Draw hand LAST (on top of everything, no black area)
        self.draw_hand()
        
        # Draw dragged card
        if self.dragging and self.selected_card_index is not None:
            card = self.game.current_player.hand[self.selected_card_index]
            card_surface = self.renderer.render_card(card, True, True)
            rect = card_surface.get_rect(center=self.drag_pos)
            self.screen.blit(card_surface, rect)
        
        # Draw targeting arrow
        if self.targeting_mode and self.selected_minion_index is not None:
            self.draw_targeting_arrow()
        
        # Draw message
        if self.message_timer > 0:
            self.draw_message()
        
        # Draw game over screen
        if self.game.game_over:
            self.draw_game_over()
        
        # Draw tutorial overlay (always on top)
        if self.tutorial.active:
            self.tutorial.draw(self.screen)
        
        pygame.display.flip()
    
    def draw_heroes(self):
        # Draw BOTH heroes using FULL CARDS from Heroes folder (1.png-5.png)
        # Hero cards positioned EXACTLY in the arch frames

        # Hero cards sized to fit arch frames PERFECTLY
        hero_width = 260   # Narrower to fit arch width
        hero_height = 300  # Shorter to fit arch height

        # Calculate hero slot positions - CENTERED in the arch
        table_center_x = self.table_actual_left + self.table_actual_width // 2
        hero_slot_x = table_center_x - hero_width // 2  # Perfectly centered

        # SWAPPED: PLAYER 1 (bottom hero) - CORRECT position (checkmark)
        player1_hero_y = self.opponent_hero_y
        player1_is_current = (self.game.current_player == self.game.player1)
        hero1_surface = self.renderer.render_hero(self.game.player1, player1_is_current, False, hero_width, hero_height)
        self.screen.blit(hero1_surface, (hero_slot_x, player1_hero_y))
        
        # SWAPPED: PLAYER 2 (top hero) - FIXED position (was X, now correct)
        player2_hero_y = self.player_hero_y
        player2_is_current = (self.game.current_player == self.game.player2)
        player2_is_target = self.targeting_mode and player2_is_current
        hero2_surface = self.renderer.render_hero(self.game.player2, player2_is_current, player2_is_target, hero_width, hero_height)
        self.screen.blit(hero2_surface, (hero_slot_x, player2_hero_y))

    
    def draw_game_log(self):
        """Draw enhanced game log panel - FIXED position"""
        log_width = self.log_width
        log_height = self.HEIGHT - 40
        log_x = self.log_x
        log_y = 20
        
        # Main log panel
        log_rect = pygame.Rect(log_x, log_y, log_width, log_height)
        
        # Background with subtle gradient
        log_surface = pygame.Surface((log_width, log_height), pygame.SRCALPHA)
        for i in range(log_height):
            alpha = 240
            color = (*BOARD_WOOD_DARK[:3], alpha)
            pygame.draw.line(log_surface, color, (0, i), (log_width, i))
        
        self.screen.blit(log_surface, log_rect.topleft)
        
        # Ornate border
        pygame.draw.rect(self.screen, CARD_BORDER_GOLD, log_rect, 3, border_radius=12)
        pygame.draw.rect(self.screen, BOARD_WOOD_LIGHT, log_rect.inflate(-6, -6), 2, border_radius=10)
        
        # Title section
        title_banner = pygame.Rect(log_x + 15, log_y + 15, log_width - 30, 35)
        pygame.draw.rect(self.screen, HERO_PORTRAIT_BG, title_banner, border_radius=8)
        pygame.draw.rect(self.screen, CARD_BORDER_GOLD, title_banner, 2, border_radius=8)
        
        title = self.font.render("Battle Log", True, TEXT_GOLD)
        title_shadow = self.font.render("Battle Log", True, BLACK)
        title_rect = title.get_rect(center=title_banner.center)
        self.screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
        self.screen.blit(title, title_rect)
        
        # Separator line
        separator_y = log_y + 60
        pygame.draw.line(self.screen, CARD_BORDER_GOLD, 
                        (log_x + 20, separator_y), 
                        (log_x + log_width - 20, separator_y), 2)
        
        # Log entries with better formatting
        recent_logs = self.game.get_recent_log(25)
        y_offset = 75
        max_y = log_height - 20
        
        for i, log_entry in enumerate(reversed(recent_logs)):
            if y_offset > max_y:
                break
            
            # Color code different types of actions
            color = BUTTON_TEXT
            if "played" in log_entry.lower():
                color = GLOW_GREEN
            elif "attack" in log_entry.lower() or "damage" in log_entry.lower():
                color = HEALTH_RED
            elif "died" in log_entry.lower() or "destroyed" in log_entry.lower():
                color = GRAY
            elif "drew" in log_entry.lower():
                color = MANA_CRYSTAL_FULL
            elif "turn" in log_entry.lower():
                color = TEXT_GOLD
            
            # Word wrap for long entries
            words = log_entry.split()
            lines = []
            current_line = []
            current_width = 0
            max_width = log_width - 50
            
            for word in words:
                word_surface = self.tiny_font.render(word + " ", True, color)
                word_width = word_surface.get_width()
                
                if current_width + word_width > max_width:
                    if current_line:
                        lines.append(" ".join(current_line))
                        current_line = [word]
                        current_width = word_width
                else:
                    current_line.append(word)
                    current_width += word_width
            
            if current_line:
                lines.append(" ".join(current_line))
            
            # Draw each line
            for line in lines:
                if y_offset > max_y:
                    break
                
                # Bullet point
                bullet = self.tiny_font.render("•", True, CARD_BORDER_GOLD)
                self.screen.blit(bullet, (log_x + 20, y_offset + 2))
                
                # Entry text with shadow
                text = self.tiny_font.render(line, True, color)
                text_shadow = self.tiny_font.render(line, True, BLACK)
                self.screen.blit(text_shadow, (log_x + 36, y_offset + 1))
                self.screen.blit(text, (log_x + 35, y_offset))
                
                y_offset += 18
            
            # Small gap between entries
            y_offset += 2
    
    def draw_turn_indicator(self):
        """Draw turn number - positioned to NOT overlap with log"""
        turn_text = f"Turn {self.game.turn_count + 1}"
        text_surface = self.font.render(turn_text, True, TEXT_GOLD)
        text_shadow = self.font.render(turn_text, True, BLACK)
        
        # Position at top center of game area, WELL CLEAR of log
        center_x = self.game_area_width // 2
        text_rect = text_surface.get_rect(center=(center_x, 25))
        
        # Ornate background banner
        bg_rect = text_rect.inflate(50, 25)
        
        # Banner with gradient
        banner_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        for i in range(bg_rect.height):
            alpha = 220 - (abs(i - bg_rect.height//2) * 3)
            color = (*BOARD_WOOD_DARK[:3], alpha)
            pygame.draw.line(banner_surface, color, (0, i), (bg_rect.width, i))
        
        self.screen.blit(banner_surface, bg_rect.topleft)
        
        # Gold border
        pygame.draw.rect(self.screen, CARD_BORDER_GOLD, bg_rect, 3, border_radius=10)
        pygame.draw.rect(self.screen, BOARD_WOOD_LIGHT, bg_rect.inflate(-6, -6), 1, border_radius=8)
        
        # Text with shadow
        self.screen.blit(text_shadow, (text_rect.x + 2, text_rect.y + 2))
        self.screen.blit(text_surface, text_rect)
    
    def draw_hero_power_button(self):
        """Draw hero power button next to hero with authentic styling"""
        player = self.game.current_player
        
        button_size = 85
        button_x = self.hero_power_x
        button_y = self.hero_power_y
        button_rect = pygame.Rect(button_x, button_y, button_size, button_size)
        
        mouse_pos = pygame.mouse.get_pos()
        hover = button_rect.collidepoint(mouse_pos)
        
        # Determine if usable
        can_use = not player.hero_power_used and player.mana >= 2
        
        # Glow effect
        if can_use and hover:
            for i in range(4):
                alpha = 50 - i * 12
                glow_rect = button_rect.inflate(i*4, i*4)
                pygame.draw.ellipse(self.screen, (*GLOW_GREEN[:3], alpha), glow_rect)
        
        # Button background (circular gem)
        if can_use:
            color = MANA_CRYSTAL_FULL if not hover else MANA_CRYSTAL_HIGHLIGHT
            border_color = MANA_CRYSTAL_BORDER
        else:
            color = MANA_CRYSTAL_EMPTY
            border_color = (40, 40, 50)
        
        pygame.draw.ellipse(self.screen, border_color, button_rect.inflate(6, 6))
        pygame.draw.ellipse(self.screen, color, button_rect)
        
        # Shine effect
        if can_use:
            shine_rect = pygame.Rect(button_x + 15, button_y + 15, 30, 30)
            pygame.draw.ellipse(self.screen, MANA_CRYSTAL_HIGHLIGHT, shine_rect)
        
        # Hero power icon (simplified - could be class-specific)
        icon_text = self.large_font.render("⚡", True, TEXT_WHITE if can_use else GRAY)
        icon_rect = icon_text.get_rect(center=button_rect.center)
        self.screen.blit(icon_text, icon_rect)
        
        # Cost indicator - SMALL BADGE on bottom right corner
        cost_size = 28
        cost_bg = pygame.Rect(button_x + button_size - cost_size + 5, 
                             button_y + button_size - cost_size + 5, 
                             cost_size, cost_size)
        pygame.draw.ellipse(self.screen, MANA_CRYSTAL_BORDER, cost_bg)
        pygame.draw.ellipse(self.screen, MANA_CRYSTAL_FULL if can_use else MANA_CRYSTAL_EMPTY, 
                          cost_bg.inflate(-4, -4))
        
        cost_text = self.small_font.render("2", True, TEXT_WHITE)
        cost_rect = cost_text.get_rect(center=cost_bg.center)
        self.screen.blit(cost_text, cost_rect)
    
    def draw_board(self, player, y, is_current_player):
        minions = player.board
        
        # NO HERO DRAWING HERE - heroes are drawn separately in draw_heroes()
        # This prevents the swapping issue
        
        if not minions:
            return
        
        # Calculate minion positions - CENTER-ALIGNED across full table width
        card_width = 247  # Same as hand cards
        card_spacing = 15
        
        # Use stretched table dimensions - minions can use full width
        table_left = self.table_actual_left
        table_right = self.table_actual_right
        
        # Calculate total width of all minions
        total_minions_width = len(minions) * card_width + (len(minions) - 1) * card_spacing
        
        # Center minions across the full table width
        available_width = table_right - table_left - 100  # Full table width with margins
        minions_start_x = table_left + 50 + (available_width - total_minions_width) // 2
        
        # Draw all minions in a row, centered
        for i, minion in enumerate(minions):
            can_attack = is_current_player and minion.can_attack and minion.attack > 0
            selected = is_current_player and i == self.selected_minion_index
            is_target = self.targeting_mode and not is_current_player
            
            minion_surface = self.renderer.render_minion(minion, can_attack, selected, is_target)
            x = minions_start_x + i * (card_width + card_spacing)
            self.screen.blit(minion_surface, (x, y))
    
    def draw_hand(self):
        hand = self.game.current_player.hand
        if not hand:
            return
        
        # Calculate card positions - 0.9x cards (247x261)
        total_cards = len(hand)
        card_width = 262  # 247 + 15 spacing
        card_spacing = 15
        total_width = (total_cards * card_width)
        
        # Ensure cards stay within game area (left of log panel)
        max_width = self.game_area_width - 250
        if total_width > max_width:
            card_spacing = max(8, (max_width - (total_cards * 247)) // (total_cards - 1))
            card_width = 247 + card_spacing
            total_width = total_cards * card_width
        
        # Center in game area
        start_x = (self.game_area_width - total_width) // 2
        
        for i, card in enumerate(hand):
            if self.dragging and i == self.selected_card_index:
                continue
            
            playable = card.can_play(self.game.current_player)
            hover = i == self.hover_card_index
            
            card_surface = self.renderer.render_card(card, playable, False, hover)
            x = start_x + (i * card_width)
            y = self.hand_y
            
            # Account for glow offset (5px added by render_card when playable/hover)
            if playable or hover:
                x -= 5  # Shift left to compensate for glow
                y -= 5  # Shift up to compensate for glow
            
            if hover:
                y -= 30  # Hover offset for double-size cards
            
            self.screen.blit(card_surface, (x, y))
    
    def draw_mana(self):
        player = self.game.current_player
        
        # Position mana display - LARGER crystal
        mana_x = self.mana_x
        mana_y = self.mana_y
        
        # LARGER mana crystal display (0.8x size instead of 0.6x)
        crystal_size = 45  # Was 30, now bigger
        
        # Outer glow
        for i in range(3):
            alpha = 30 - i * 10
            pygame.draw.circle(self.screen, (*MANA_CRYSTAL_HIGHLIGHT[:3], alpha), 
                             (mana_x, mana_y), crystal_size + 5 - i*2)
        
        # Main crystal border
        pygame.draw.circle(self.screen, MANA_CRYSTAL_BORDER, (mana_x, mana_y), crystal_size + 2)
        
        # Crystal fill
        pygame.draw.circle(self.screen, MANA_CRYSTAL_FULL, (mana_x, mana_y), crystal_size)
        
        # Highlight shine
        shine_offset = int(crystal_size * 0.3)
        pygame.draw.circle(self.screen, MANA_CRYSTAL_HIGHLIGHT, 
                         (mana_x - shine_offset, mana_y - shine_offset), 
                         int(crystal_size * 0.35))
        
        # Mana text with shadow - LARGER font
        mana_text = f"{player.mana}/{player.max_mana}"
        text_surface = self.large_font.render(mana_text, True, TEXT_WHITE)  # Larger font
        text_shadow = self.large_font.render(mana_text, True, BLACK)
        text_rect = text_surface.get_rect(center=(mana_x, mana_y))
        self.screen.blit(text_shadow, (text_rect.x + 2, text_rect.y + 2))
        self.screen.blit(text_surface, text_rect)
        
        # Mana crystals visualization below - smaller
        crystal_start_x = self.mana_x - 35  # Center the row of crystals
        crystal_y = mana_y + 55  # Further below
        crystal_spacing = 8  # Spacing
        
        for i in range(10):
            x = crystal_start_x + i * crystal_spacing
            if i < player.max_mana:
                # Available or used crystal
                if i < player.mana:
                    color = MANA_CRYSTAL_FULL
                    border = MANA_CRYSTAL_HIGHLIGHT
                else:
                    color = MANA_CRYSTAL_EMPTY
                    border = MANA_CRYSTAL_BORDER
                
                pygame.draw.circle(self.screen, border, (x, crystal_y), 4)
                pygame.draw.circle(self.screen, color, (x, crystal_y), 3)
            else:
                # Not yet unlocked
                pygame.draw.circle(self.screen, (30, 30, 40), (x, crystal_y), 3)
                pygame.draw.circle(self.screen, (50, 50, 60), (x, crystal_y), 3, 1)
    
    def draw_end_turn_button(self):
        # End turn button (positioned to not overlap with log)
        button_width = 120  # Updated width
        button_height = 120  # Updated height
        button_x = self.end_turn_x
        button_y = self.end_turn_y
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        
        mouse_pos = pygame.mouse.get_pos()
        hover = button_rect.collidepoint(mouse_pos)
        
        # Glow effect when hovering
        if hover:
            for i in range(5):
                alpha = 50 - i * 10
                glow_rect = button_rect.inflate(i*4, i*4)
                pygame.draw.rect(self.screen, (*GLOW_YELLOW[:3], alpha), glow_rect, border_radius=15)
        
        # Button background (red stone)
        color = BUTTON_END_TURN if not hover else (220, 70, 70)
        pygame.draw.rect(self.screen, color, button_rect, border_radius=15)
        
        # Ornate gold border
        pygame.draw.rect(self.screen, BUTTON_BORDER_GOLD, button_rect, 4, border_radius=15)
        pygame.draw.rect(self.screen, BOARD_WOOD_DARK, button_rect.inflate(-8, -8), 2, border_radius=12)
        
        # Text with shadow - centered
        text = self.font.render("END", True, TEXT_GOLD)
        text_shadow = self.font.render("END", True, BLACK)
        text_rect = text.get_rect(center=(button_rect.centerx, button_rect.centery - 12))
        self.screen.blit(text_shadow, (text_rect.x + 2, text_rect.y + 2))
        self.screen.blit(text, text_rect)
        
        text2 = self.font.render("TURN", True, TEXT_GOLD)
        text2_shadow = self.font.render("TURN", True, BLACK)
        text2_rect = text2.get_rect(center=(button_rect.centerx, button_rect.centery + 12))
        self.screen.blit(text2_shadow, (text2_rect.x + 2, text2_rect.y + 2))
        self.screen.blit(text2, text2_rect)
    
    def draw_deck_info(self):
        # Opponent deck (top right corner, left of log panel)
        opponent = self.game.get_opponent(self.game.current_player)
        
        deck_x = self.deck_info_x
        deck_y = self.deck_info_y_opponent
        
        # Simple panel - top right
        info_bg = pygame.Rect(deck_x, deck_y, 100, 65)
        pygame.draw.rect(self.screen, BOARD_WOOD_DARK, info_bg, border_radius=8)
        pygame.draw.rect(self.screen, CARD_BORDER_GOLD, info_bg, 2, border_radius=8)
        
        # Text
        deck_text = self.small_font.render(f"Deck: {len(opponent.deck)}", True, TEXT_GOLD)
        self.screen.blit(deck_text, (deck_x + 8, deck_y + 10))
        
        hand_text = self.small_font.render(f"Hand: {len(opponent.hand)}", True, TEXT_GOLD)
        self.screen.blit(hand_text, (deck_x + 8, deck_y + 38))
        
        # Player deck (BELOW opponent deck in top right)
        player_deck_y = self.deck_info_y_player
        
        player_info_bg = pygame.Rect(deck_x, player_deck_y, 100, 45)
        pygame.draw.rect(self.screen, BOARD_WOOD_DARK, player_info_bg, border_radius=8)
        pygame.draw.rect(self.screen, CARD_BORDER_GOLD, player_info_bg, 2, border_radius=8)
        
        deck_text = self.small_font.render(f"Deck: {len(self.game.current_player.deck)}", True, TEXT_GOLD)
        self.screen.blit(deck_text, (deck_x + 8, player_deck_y + 15))
    
    def draw_targeting_arrow(self):
        if self.selected_minion_index is None:
            return
        
        # Get minion position - centered layout with 0.9x cards
        minions = self.game.current_player.board
        card_width = 247
        card_spacing = 15
        # Heroes now on RIGHT side of table
        board_right = self.game_area_width - 50
        hero_slot_x = board_right - 247 - 20  # Right side position
        hero_width = 247  # Same as playing cards
        
        # Calculate centered position
        hero_end_x = hero_slot_x + hero_width + 30
        available_width = self.game_area_width - hero_end_x - 50
        total_minions_width = len(minions) * card_width + (len(minions) - 1) * card_spacing
        minions_start_x = hero_end_x + (available_width - total_minions_width) // 2
        
        minion_x = minions_start_x + self.selected_minion_index * (card_width + card_spacing) + 123
        minion_y = self.player_board_y + 130
        
        # Draw glowing arrow to mouse
        mouse_pos = pygame.mouse.get_pos()
        
        # Glow effect
        for i in range(5):
            alpha = 100 - i * 20
            width = 8 - i
            pygame.draw.line(self.screen, (*GLOW_RED[:3], alpha), 
                           (minion_x, minion_y), mouse_pos, width)
        
        # Main arrow
        pygame.draw.line(self.screen, GLOW_RED, (minion_x, minion_y), mouse_pos, 5)
        
        # Arrow head with glow
        pygame.draw.circle(self.screen, HEALTH_BORDER, mouse_pos, 14)
        pygame.draw.circle(self.screen, HEALTH_RED, mouse_pos, 12)
        pygame.draw.circle(self.screen, STAT_SHINE, 
                         (mouse_pos[0] - 4, mouse_pos[1] - 4), 5)
    
    def draw_message(self):
        # Ornate message banner
        msg_width = 500
        msg_height = 80
        msg_x = self.WIDTH // 2 - msg_width // 2
        msg_y = self.HEIGHT // 2 - msg_height // 2
        
        msg_rect = pygame.Rect(msg_x, msg_y, msg_width, msg_height)
        
        # Background with gradient
        msg_surface = pygame.Surface((msg_width, msg_height), pygame.SRCALPHA)
        for i in range(msg_height):
            alpha = 240 - (abs(i - msg_height//2) * 2)
            color = (*BOARD_WOOD_DARK[:3], alpha)
            pygame.draw.line(msg_surface, color, (0, i), (msg_width, i))
        
        self.screen.blit(msg_surface, msg_rect.topleft)
        
        # Ornate border
        pygame.draw.rect(self.screen, CARD_BORDER_GOLD, msg_rect, 4, border_radius=15)
        pygame.draw.rect(self.screen, BOARD_WOOD_LIGHT, msg_rect.inflate(-8, -8), 2, border_radius=12)
        
        # Message text with shadow
        text = self.font.render(self.message, True, TEXT_GOLD)
        text_shadow = self.font.render(self.message, True, BLACK)
        text_rect = text.get_rect(center=msg_rect.center)
        self.screen.blit(text_shadow, (text_rect.x + 2, text_rect.y + 2))
        self.screen.blit(text, text_rect)
    
    def draw_game_over(self):
        # Dramatic overlay
        overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        # Ornate victory/defeat banner
        banner_width = 700
        banner_height = 250
        banner_x = self.WIDTH // 2 - banner_width // 2
        banner_y = self.HEIGHT // 2 - banner_height // 2
        banner_rect = pygame.Rect(banner_x, banner_y, banner_width, banner_height)
        
        # Banner background with gradient
        banner_surface = pygame.Surface((banner_width, banner_height), pygame.SRCALPHA)
        for i in range(banner_height):
            alpha = 250 - (abs(i - banner_height//2))
            color = (*BOARD_WOOD_DARK[:3], alpha)
            pygame.draw.line(banner_surface, color, (0, i), (banner_width, i))
        
        self.screen.blit(banner_surface, banner_rect.topleft)
        
        # Ornate gold border
        pygame.draw.rect(self.screen, CARD_BORDER_GOLD, banner_rect, 6, border_radius=20)
        pygame.draw.rect(self.screen, BOARD_WOOD_LIGHT, banner_rect.inflate(-12, -12), 3, border_radius=18)
        
        # Winner text with glow
        winner_text = f"{self.game.winner.name} Wins!"
        
        # Glow effect
        for i in range(5):
            alpha = 100 - i * 20
            glow_font = pygame.font.Font(None, 72 + i*4)
            glow_text = glow_font.render(winner_text, True, (*TEXT_GOLD[:3], alpha))
            glow_rect = glow_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 30))
            self.screen.blit(glow_text, glow_rect)
        
        # Main text with shadow
        winner_surface = self.large_font.render(winner_text, True, TEXT_GOLD)
        winner_shadow = self.large_font.render(winner_text, True, BLACK)
        text_rect = winner_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 30))
        self.screen.blit(winner_shadow, (text_rect.x + 3, text_rect.y + 3))
        self.screen.blit(winner_surface, text_rect)
        
        # Instruction with shadow
        inst_text = self.font.render("Close window to exit", True, TEXT_WHITE)
        inst_shadow = self.font.render("Close window to exit", True, BLACK)
        inst_rect = inst_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 60))
        self.screen.blit(inst_shadow, (inst_rect.x + 2, inst_rect.y + 2))
        self.screen.blit(inst_text, inst_rect)
    
    # Helper methods for hit detection
    def get_hand_card_at_pos(self, pos):
        hand = self.game.current_player.hand
        if not hand:
            return None
        
        # Updated for 0.9x cards: 247x261 - TIGHT hitboxes
        total_cards = len(hand)
        card_width = 262  # 247 + 15 spacing
        card_spacing = 15
        total_width = (total_cards * card_width)
        
        # Ensure cards stay within game area (left of log panel)
        max_width = self.game_area_width - 250
        if total_width > max_width:
            card_spacing = max(8, (max_width - (total_cards * 247)) // (total_cards - 1))
            card_width = 247 + card_spacing
            total_width = total_cards * card_width
        
        # Center in game area
        start_x = (self.game_area_width - total_width) // 2
        
        for i in range(len(hand)):
            x = start_x + (i * card_width)
            # TIGHT hitbox - just slightly bigger than card (247x261)
            rect = pygame.Rect(x - 5, self.hand_y - 10, 257, 281)
            if rect.collidepoint(pos):
                return i
        return None
    
    def get_player_minion_at_pos(self, pos):
        minions = self.game.current_player.board
        if not minions:
            return None
        
        # Updated for centered layout with 0.9x cards - TIGHT hitboxes
        card_width = 247
        card_spacing = 15
        hero_slot_x = 100  # Both heroes aligned at x=100
        hero_width = 153  # 1.3x hero width
        
        # Calculate centered position
        hero_end_x = hero_slot_x + hero_width + 30
        available_width = self.game_area_width - hero_end_x - 50
        total_minions_width = len(minions) * card_width + (len(minions) - 1) * card_spacing
        minions_start_x = hero_end_x + (available_width - total_minions_width) // 2
        
        for i in range(len(minions)):
            x = minions_start_x + i * (card_width + card_spacing)
            # TIGHT hitbox - just slightly bigger than card (247x261)
            rect = pygame.Rect(x - 5, self.player_board_y - 5, 257, 271)
            if rect.collidepoint(pos):
                return i
        
        return None
    
    def get_target_at_pos(self, pos):
        opponent = self.game.get_opponent(self.game.current_player)
        
        # Check opponent hero - heroes sized to fit arch frames EXACTLY
        hero_width = 220   # Match draw_heroes
        hero_height = 260  # Match draw_heroes
        table_center_x = self.table_actual_left + self.table_actual_width // 2
        hero_slot_x = table_center_x - hero_width // 2  # Match draw_heroes positioning
        hero_rect = pygame.Rect(hero_slot_x, self.opponent_hero_y, hero_width, hero_height)
        if hero_rect.collidepoint(pos):
            return opponent
        
        # Check opponent minions - centered layout with TIGHT hitboxes
        minions = opponent.board
        if minions:
            card_width = 247
            card_spacing = 15
            
            # Use stretched table dimensions - minions use full width
            table_left = self.table_actual_left
            table_right = self.table_actual_right
            
            # Calculate centered position
            total_minions_width = len(minions) * card_width + (len(minions) - 1) * card_spacing
            available_width = table_right - table_left - 100
            minions_start_x = table_left + 50 + (available_width - total_minions_width) // 2
            
            for i in range(len(minions)):
                x = minions_start_x + i * (card_width + card_spacing)
                # TIGHT hitbox - just slightly bigger than card (247x261)
                rect = pygame.Rect(x - 5, self.opponent_board_y - 5, 257, 271)
                if rect.collidepoint(pos):
                    return minions[i]
        
        return None
    
    def is_on_player_board(self, pos):
        # RED AREA - where current player minions are played
        # SWAPPED: Now the top tan section for player 2
        board_rect = pygame.Rect(
            self.table_actual_left + 80,  # Left edge with margin
            self.player_board_y - 20,  # Start slightly above board
            self.table_actual_width - 160,  # Width with margins
            260 + 40  # Height to cover the red area (adjusted for hero size)
        )
        return board_rect.collidepoint(pos)

    
    def is_on_target(self, pos):
        return self.get_target_at_pos(pos) is not None
    
    def is_end_turn_clicked(self, pos):
        button_width = 120  # Updated width
        button_height = 120  # Updated height
        button_rect = pygame.Rect(self.end_turn_x, self.end_turn_y, button_width, button_height)
        return button_rect.collidepoint(pos)

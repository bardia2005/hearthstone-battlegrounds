"""
Interactive tutorial system for Hearthstone
Teaches players the game mechanics step by step
"""

import pygame
from typing import List, Optional, Callable, Dict, Any
from .colors import *
from .sound_manager import get_sound_manager


class TutorialStep:
    def __init__(self, title: str, message: str, highlight_area: Optional[pygame.Rect] = None,
                 arrow_to: Optional[tuple] = None, condition: Optional[Callable] = None,
                 auto_advance: bool = False):
        self.title = title
        self.message = message
        self.highlight_area = highlight_area
        self.arrow_to = arrow_to  # (x, y) position to point arrow
        self.condition = condition  # Function that returns True when step is complete
        self.auto_advance = auto_advance
        self.completed = False


class TutorialOverlay:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 32)
        self.title_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)
        self.sound_manager = get_sound_manager()
        
        self.current_step = 0
        self.steps: List[TutorialStep] = []
        self.active = False
        self.completed = False
        
        # Animation
        self.arrow_bounce = 0
        self.arrow_direction = 1
        
        # Skip button
        self.skip_button = pygame.Rect(screen_width - 150, 20, 130, 50)
        self.skip_hovered = False
    
    def start(self):
        """Start the tutorial"""
        self.active = True
        self.current_step = 0
        self.completed = False
        self.sound_manager.play('chime')
    
    def add_step(self, step: TutorialStep):
        """Add a tutorial step"""
        self.steps.append(step)
    
    def next_step(self):
        """Advance to next step"""
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.sound_manager.play('button_click')
            return True
        else:
            self.complete()
            return False
    
    def complete(self):
        """Complete the tutorial"""
        self.active = False
        self.completed = True
        self.sound_manager.play('victory')
    
    def skip(self):
        """Skip the tutorial"""
        self.active = False
        self.completed = True
        self.sound_manager.play('menu_close')
    
    def check_condition(self) -> bool:
        """Check if current step's condition is met"""
        if self.current_step >= len(self.steps):
            return False
        
        step = self.steps[self.current_step]
        if step.condition and step.condition():
            if step.auto_advance:
                self.next_step()
            return True
        return False
    
    def handle_event(self, event) -> bool:
        """Handle input events, returns True if event was consumed"""
        if not self.active:
            return False
        
        if event.type == pygame.MOUSEMOTION:
            self.skip_hovered = self.skip_button.collidepoint(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Skip button
            if self.skip_button.collidepoint(event.pos):
                self.skip()
                return True
            
            # Click anywhere to advance (if no condition)
            step = self.steps[self.current_step]
            if not step.condition:
                self.next_step()
                return True
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.skip()
                return True
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                step = self.steps[self.current_step]
                if not step.condition:
                    self.next_step()
                    return True
        
        return False
    
    def update(self):
        """Update animation"""
        if not self.active:
            return
        
        # Animate arrow bounce
        self.arrow_bounce += 0.5 * self.arrow_direction
        if self.arrow_bounce > 10:
            self.arrow_direction = -1
        elif self.arrow_bounce < 0:
            self.arrow_direction = 1
        
        # Check step condition
        self.check_condition()
    
    def draw(self, surface: pygame.Surface):
        """Draw tutorial overlay with authentic Hearthstone styling"""
        if not self.active or self.current_step >= len(self.steps):
            return
        
        step = self.steps[self.current_step]
        
        # Darken screen with overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        
        # Highlight area (cut out from overlay)
        if step.highlight_area:
            # Draw everything except highlight area
            # Top
            pygame.draw.rect(overlay, (0, 0, 0, 200), 
                           (0, 0, self.screen_width, step.highlight_area.top))
            # Bottom
            pygame.draw.rect(overlay, (0, 0, 0, 200),
                           (0, step.highlight_area.bottom, self.screen_width, 
                            self.screen_height - step.highlight_area.bottom))
            # Left
            pygame.draw.rect(overlay, (0, 0, 0, 200),
                           (0, step.highlight_area.top, step.highlight_area.left,
                            step.highlight_area.height))
            # Right
            pygame.draw.rect(overlay, (0, 0, 0, 200),
                           (step.highlight_area.right, step.highlight_area.top,
                            self.screen_width - step.highlight_area.right,
                            step.highlight_area.height))
            
            # Glowing highlight border
            for i in range(4):
                alpha = 150 - i * 35
                glow_rect = step.highlight_area.inflate(i*4, i*4)
                pygame.draw.rect(surface, (*GLOW_YELLOW[:3], alpha), glow_rect, 3)
        else:
            surface.blit(overlay, (0, 0))
        
        # Draw arrow pointing to area
        if step.arrow_to:
            self.draw_arrow(surface, step.arrow_to)
        
        # Tutorial box with ornate styling
        box_width = 650
        box_height = 280
        box_x = (self.screen_width - box_width) // 2
        box_y = self.screen_height - box_height - 60
        
        # Adjust position if highlighting bottom area
        if step.highlight_area and step.highlight_area.bottom > self.screen_height - 350:
            box_y = 60
        
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        
        # Box background with gradient
        box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        for i in range(box_height):
            alpha = 245 - (abs(i - box_height//2) * 0.5)
            color = (*BOARD_WOOD_DARK[:3], int(alpha))
            pygame.draw.line(box_surface, color, (0, i), (box_width, i))
        
        surface.blit(box_surface, box_rect.topleft)
        
        # Ornate border
        pygame.draw.rect(surface, CARD_BORDER_GOLD, box_rect, 5, border_radius=18)
        pygame.draw.rect(surface, BOARD_WOOD_LIGHT, box_rect.inflate(-10, -10), 3, border_radius=16)
        
        # Title banner
        title_banner = pygame.Rect(box_x + 20, box_y + 20, box_width - 40, 45)
        pygame.draw.rect(surface, HERO_PORTRAIT_BG, title_banner, border_radius=8)
        pygame.draw.rect(surface, CARD_BORDER_GOLD, title_banner, 2, border_radius=8)
        
        title_text = self.title_font.render(step.title, True, TEXT_GOLD)
        title_shadow = self.title_font.render(step.title, True, BLACK)
        title_rect = title_text.get_rect(center=title_banner.center)
        surface.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
        surface.blit(title_text, title_rect)
        
        # Message (word wrap)
        self.draw_wrapped_text(surface, step.message, box_rect, box_y + 85)
        
        # Progress indicator
        progress_text = f"Step {self.current_step + 1} of {len(self.steps)}"
        progress_surface = self.small_font.render(progress_text, True, BUTTON_TEXT)
        progress_shadow = self.small_font.render(progress_text, True, BLACK)
        surface.blit(progress_shadow, (box_x + 26, box_y + box_height - 41))
        surface.blit(progress_surface, (box_x + 25, box_y + box_height - 40))
        
        # Continue hint
        if not step.condition:
            hint_text = "Click or press SPACE to continue"
            hint_surface = self.small_font.render(hint_text, True, TEXT_GOLD)
            hint_shadow = self.small_font.render(hint_text, True, BLACK)
            hint_rect = hint_surface.get_rect(centerx=box_rect.centerx, 
                                             bottom=box_y + box_height - 18)
            surface.blit(hint_shadow, (hint_rect.x + 1, hint_rect.y + 1))
            surface.blit(hint_surface, hint_rect)
        else:
            hint_text = "Complete the action to continue"
            hint_surface = self.small_font.render(hint_text, True, GLOW_GREEN)
            hint_shadow = self.small_font.render(hint_text, True, BLACK)
            hint_rect = hint_surface.get_rect(centerx=box_rect.centerx,
                                             bottom=box_y + box_height - 18)
            surface.blit(hint_shadow, (hint_rect.x + 1, hint_rect.y + 1))
            surface.blit(hint_surface, hint_rect)
        
        # Skip button with ornate styling
        skip_color = BUTTON_HOVER if self.skip_hovered else BUTTON_BG
        
        # Glow effect when hovering
        if self.skip_hovered:
            for i in range(3):
                alpha = 60 - i * 20
                glow_rect = self.skip_button.inflate(i*3, i*3)
                pygame.draw.rect(surface, (*GLOW_YELLOW[:3], alpha), glow_rect, border_radius=10)
        
        pygame.draw.rect(surface, skip_color, self.skip_button, border_radius=10)
        pygame.draw.rect(surface, CARD_BORDER_GOLD, self.skip_button, 3, border_radius=10)
        pygame.draw.rect(surface, BOARD_WOOD_DARK, self.skip_button.inflate(-6, -6), 1, border_radius=8)
        
        skip_text = self.font.render("Skip", True, TEXT_GOLD if self.skip_hovered else BUTTON_TEXT)
        skip_shadow = self.font.render("Skip", True, BLACK)
        skip_rect = skip_text.get_rect(center=self.skip_button.center)
        surface.blit(skip_shadow, (skip_rect.x + 2, skip_rect.y + 2))
        surface.blit(skip_text, skip_rect)
    
    def draw_arrow(self, surface: pygame.Surface, target_pos: tuple):
        """Draw an animated glowing arrow pointing to target"""
        x, y = target_pos
        y += self.arrow_bounce
        
        # Arrow color with glow
        color = TEXT_GOLD
        
        # Glow effect
        for i in range(4):
            alpha = 100 - i * 25
            glow_y = y - 50 - i*2
            pygame.draw.line(surface, (*color[:3], alpha), (x, glow_y), (x, y), 7 - i)
        
        # Arrow shaft
        pygame.draw.line(surface, color, (x, y - 50), (x, y), 6)
        
        # Arrow head (triangle)
        points = [
            (x, y),
            (x - 18, y - 25),
            (x + 18, y - 25)
        ]
        pygame.draw.polygon(surface, color, points)
        
        # Glow on arrow head
        pygame.draw.circle(surface, GLOW_YELLOW, (x, y), 8)
    
    def draw_wrapped_text(self, surface: pygame.Surface, text: str, 
                         box_rect: pygame.Rect, start_y: int):
        """Draw text with word wrapping and shadows"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        max_width = box_rect.width - 60
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surface = self.font.render(test_line, True, TEXT_WHITE)
            
            if test_surface.get_width() <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw lines with shadows
        y = start_y
        for line in lines:
            line_surface = self.font.render(line, True, TEXT_WHITE)
            line_shadow = self.font.render(line, True, BLACK)
            line_rect = line_surface.get_rect(centerx=box_rect.centerx, top=y)
            surface.blit(line_shadow, (line_rect.x + 1, line_rect.y + 1))
            surface.blit(line_surface, line_rect)
            y += 38


def create_tutorial_steps(gui) -> List[TutorialStep]:
    """Create all tutorial steps for the game"""
    steps = []
    
    # Step 1: Welcome
    steps.append(TutorialStep(
        "Welcome to Hearthstone!",
        "This tutorial will teach you how to play. Let's start with the basics of the game board.",
        auto_advance=False
    ))
    
    # Step 2: Hero - FIXED for left-aligned hero slot
    hero_slot_x = 100
    hero_rect = pygame.Rect(hero_slot_x - 10, gui.player_board_y - 10, 138, 165)
    steps.append(TutorialStep(
        "Your Hero",
        "This is your hero. Your goal is to reduce your opponent's hero to 0 health while keeping yours alive. You start with 30 health.",
        highlight_area=hero_rect,
        arrow_to=(hero_slot_x + 59, gui.player_board_y + 72)
    ))
    
    # Step 3: Mana Crystals - FIXED positioning
    mana_rect = pygame.Rect(gui.mana_x - 10, gui.mana_y - 30, 150, 80)
    steps.append(TutorialStep(
        "Mana Crystals",
        "Mana is used to play cards. You gain 1 mana crystal each turn (max 10). Blue crystals are available, gray ones are used.",
        highlight_area=mana_rect,
        arrow_to=(gui.mana_x + 50, gui.mana_y)
    ))
    
    # Step 4: Hand - FIXED positioning for WIDER cards (190x202) with proper margins
    hand_rect = pygame.Rect(200, gui.hand_y - 40, gui.game_area_width - 400, 260)
    steps.append(TutorialStep(
        "Your Hand",
        "These are your cards. You can hold up to 10 cards. The number in the blue crystal is the mana cost. Green border means you can play it.",
        highlight_area=hand_rect,
        arrow_to=(gui.game_area_width // 2, gui.hand_y + 100)
    ))
    
    # Step 5: Play a card - use same hand rect
    steps.append(TutorialStep(
        "Playing Cards",
        "Try it! Click and drag a card with a green border onto the board area (the middle of the screen).",
        highlight_area=hand_rect,
        condition=lambda: len(gui.game.current_player.board) > 0,
        auto_advance=True
    ))
    
    # Step 6: Board - FIXED positioning for 0.8x SMALLER minions (171x210)
    board_rect = pygame.Rect(100, gui.player_board_y - 30, gui.game_area_width - 200, 260)
    steps.append(TutorialStep(
        "The Board",
        "Great! Your minions appear here. The yellow number is attack, red is health. You can have up to 7 minions on the board.",
        highlight_area=board_rect,
        arrow_to=(gui.game_area_width // 2, gui.player_board_y + 105)
    ))
    
    # Step 7: Minion Stats - use same board rect
    steps.append(TutorialStep(
        "Minion Stats",
        "Minions have Attack (yellow) and Health (red). When a minion attacks, both deal damage to each other. If health reaches 0, the minion dies.",
        highlight_area=board_rect
    ))
    
    # Step 8: Summoning Sickness - use same board rect
    steps.append(TutorialStep(
        "Summoning Sickness",
        "Minions can't attack the turn they're played (unless they have Charge). The 'Z' symbol means the minion is sleeping.",
        highlight_area=board_rect
    ))
    
    # Step 9: End Turn - FIXED positioning
    end_turn_rect = pygame.Rect(gui.end_turn_x - 10, gui.end_turn_y - 10, 120, 160)
    steps.append(TutorialStep(
        "End Turn Button",
        "When you're done playing cards and attacking, click this button to end your turn. Your opponent will then take their turn.",
        highlight_area=end_turn_rect,
        arrow_to=(gui.end_turn_x + 50, gui.end_turn_y + 70)
    ))
    
    # Step 10: Hero Power - FIXED positioning
    hp_rect = pygame.Rect(gui.hero_power_x - 20, gui.hero_power_y - 20, 100, 100)
    steps.append(TutorialStep(
        "Hero Power",
        "Each hero has a special power that costs 2 mana. You can use it once per turn. Click the HP button to activate it.",
        highlight_area=hp_rect,
        arrow_to=(gui.hero_power_x + 40, gui.hero_power_y + 40)
    ))
    
    # Step 11: Opponent - FIXED for left-aligned opponent hero slot
    opp_hero_slot_x = 100
    opp_rect = pygame.Rect(opp_hero_slot_x - 10, gui.opponent_board_y - 10, 138, 165)
    steps.append(TutorialStep(
        "Opponent's Hero",
        "This is your opponent's hero. Attack it with your minions to win! But watch out for their minions blocking the way.",
        highlight_area=opp_rect,
        arrow_to=(opp_hero_slot_x + 59, gui.opponent_board_y + 72)
    ))
    
    # Step 12: Attacking - use board rect
    steps.append(TutorialStep(
        "Attacking",
        "To attack: Click one of your minions, then click an enemy minion or the enemy hero. Minions with Taunt (gray border) must be attacked first!",
        highlight_area=board_rect
    ))
    
    # Step 13: Game Log - FIXED positioning
    log_rect = pygame.Rect(gui.log_x - 10, 40, gui.log_width + 20, gui.HEIGHT - 120)
    steps.append(TutorialStep(
        "Game Log",
        "All game actions are recorded here. You can see what cards were played, attacks made, and other important events.",
        highlight_area=log_rect,
        arrow_to=(gui.log_x + gui.log_width // 2, 100)
    ))
    
    # Step 14: Card Types
    steps.append(TutorialStep(
        "Card Types",
        "There are 3 types of cards: Minions (stay on board), Spells (one-time effects), and Weapons (let your hero attack).",
        auto_advance=False
    ))
    
    # Step 15: Special Abilities
    steps.append(TutorialStep(
        "Special Abilities",
        "Cards can have special abilities: Taunt (must attack first), Charge (attack immediately), Divine Shield (block 1 hit), and more!",
        auto_advance=False
    ))
    
    # Step 16: Strategy Tips
    steps.append(TutorialStep(
        "Strategy Tips",
        "Control the board with minions. Use spells to remove threats. Save powerful cards for the right moment. Most importantly: have fun!",
        auto_advance=False
    ))
    
    # Step 17: Complete
    steps.append(TutorialStep(
        "Tutorial Complete!",
        "You're ready to play! Remember: reduce your opponent to 0 health to win. Good luck and have fun playing Hearthstone!",
        auto_advance=False
    ))
    
    return steps

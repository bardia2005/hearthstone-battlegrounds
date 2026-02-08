from typing import Optional, List, Callable
from .player import Player
from .minion import Minion


class Game:
    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.turn_count = 0
        self.game_over = False
        self.winner = None
        self.game_log: List[str] = []
        self.max_log_entries = 100

    def add_log(self, message: str):
        """Add a message to the game log"""
        self.game_log.append(message)
        if len(self.game_log) > self.max_log_entries:
            self.game_log.pop(0)

    def get_recent_log(self, count: int = 10) -> List[str]:
        """Get the most recent log entries"""
        return self.game_log[-count:]

    def get_opponent(self, player: Player) -> Player:
        return self.player2 if player == self.player1 else self.player1

    def start_game(self):
        self.add_log("=== Game Started ===")
        
        # Initial draw
        for _ in range(3):
            if self.player1.deck:
                card = self.player1.deck.pop()
                self.player1.hand.append(card)
        
        for _ in range(4):
            if self.player2.deck:
                card = self.player2.deck.pop()
                self.player2.hand.append(card)
        
        self.add_log(f"{self.player1.name} draws 3 cards")
        self.add_log(f"{self.player2.name} draws 4 cards")
        
        # Give coin to second player
        from .spell import SpellCard
        from .cards_collection import coin_effect
        coin = SpellCard("The Coin", 0, coin_effect, "Gain 1 mana crystal this turn")
        self.player2.hand.append(coin)
        self.add_log(f"{self.player2.name} receives The Coin!")

    def play_turn(self):
        self.current_player.start_turn(self)

    def end_turn(self):
        # Clean up dead minions
        self.player1.remove_dead_minions(self)
        self.player2.remove_dead_minions(self)
        
        # Check for game over
        self.check_game_over()
        
        if not self.game_over:
            # Switch players
            self.current_player = self.get_opponent(self.current_player)
            self.turn_count += 1
            self.add_log(f"Turn {self.turn_count + 1}")

    def check_game_over(self):
        if self.player1.is_dead() and self.player2.is_dead():
            self.game_over = True
            self.winner = None  # Draw
            self.add_log("=== DRAW! Both heroes died! ===")
        elif self.player1.is_dead():
            self.game_over = True
            self.winner = self.player2
            self.add_log(f"=== {self.player2.name} WINS! ===")
        elif self.player2.is_dead():
            self.game_over = True
            self.winner = self.player1
            self.add_log(f"=== {self.player1.name} WINS! ===")

    def play_card(self, card_index: int, target=None) -> bool:
        if card_index < 0 or card_index >= len(self.current_player.hand):
            self.add_log("Invalid card!")
            return False
        
        card = self.current_player.hand[card_index]
        
        if not card.can_play(self.current_player):
            self.add_log(f"Not enough mana! Need {card.mana_cost}, have {self.current_player.mana}")
            return False
        
        if card.play(self.current_player, self, target):
            self.current_player.hand.pop(card_index)
            self.player1.remove_dead_minions(self)
            self.player2.remove_dead_minions(self)
            self.check_game_over()
            return True
        return False

    def attack_with_minion(self, attacker_index: int, target) -> bool:
        if attacker_index < 0 or attacker_index >= len(self.current_player.board):
            self.add_log("Invalid minion!")
            return False
        
        attacker = self.current_player.board[attacker_index]
        opponent = self.get_opponent(self.current_player)
        
        # Check for taunt
        if opponent.has_taunt():
            if isinstance(target, Player):
                self.add_log("Must attack a Taunt minion first!")
                return False
            if isinstance(target, Minion) and not target.taunt:
                self.add_log("Must attack a Taunt minion first!")
                return False
        
        # Check for stealth
        if isinstance(target, Minion) and target.stealth:
            self.add_log("Cannot attack a stealthed minion!")
            return False
        
        result = attacker.attack_target(target, self.current_player, self)
        
        # Clean up
        self.player1.remove_dead_minions(self)
        self.player2.remove_dead_minions(self)
        self.check_game_over()
        
        return result

    def hero_attack(self, target) -> bool:
        opponent = self.get_opponent(self.current_player)
        
        # Check for taunt
        if opponent.has_taunt():
            if isinstance(target, Player):
                self.add_log("Must attack a Taunt minion first!")
                return False
            if isinstance(target, Minion) and not target.taunt:
                self.add_log("Must attack a Taunt minion first!")
                return False
        
        # Check for stealth
        if isinstance(target, Minion) and target.stealth:
            self.add_log("Cannot attack a stealthed minion!")
            return False
        
        result = self.current_player.hero_attack(target, self)
        
        self.player1.remove_dead_minions(self)
        self.player2.remove_dead_minions(self)
        self.check_game_over()
        
        return result

    def use_hero_power(self, target=None) -> bool:
        return self.current_player.use_hero_power(self, target)

    def get_valid_targets(self, for_spell=False, target_type: str = "any") -> list:
        """Get all valid targets for spells or battlecries"""
        targets = []
        opponent = self.get_opponent(self.current_player)
        
        if target_type in ["any", "hero", "enemy"]:
            targets.append(opponent)
        if target_type in ["any", "hero", "friendly"]:
            targets.append(self.current_player)
        
        if target_type in ["any", "minion", "enemy", "enemy_minion"]:
            for m in opponent.board:
                if not m.stealth or target_type == "friendly":
                    targets.append(m)
        
        if target_type in ["any", "minion", "friendly", "friendly_minion"]:
            targets.extend(self.current_player.board)
        
        return targets

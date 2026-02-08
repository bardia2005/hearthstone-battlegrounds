import random
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .card import Card
    from .minion import Minion
    from .spell import Weapon
    from .game import Game


class Player:
    def __init__(self, name: str, deck: List['Card'], hero_power=None):
        self.name = name
        self.deck = deck.copy()
        random.shuffle(self.deck)
        self.hand: List['Card'] = []
        self.board: List['Minion'] = []
        self.health = 30
        self.max_health = 30
        self.mana = 0
        self.max_mana = 0
        self.armor = 0
        self.fatigue_damage = 0
        self.weapon: Optional['Weapon'] = None
        self.hero_power = hero_power
        self.hero_power_used = False
        self.can_attack_hero = False
        self.hero_attacks_this_turn = 0

    def draw_card(self, game: 'Game', count: int = 1):
        for _ in range(count):
            if len(self.hand) >= 10:
                if self.deck:
                    burned = self.deck.pop()
                    game.add_log(f"{self.name}'s hand is full! {burned.name} burned.")
                continue
                
            if self.deck:
                card = self.deck.pop()
                self.hand.append(card)
                game.add_log(f"{self.name} draws {card.name}")
            else:
                self.fatigue_damage += 1
                self.take_damage(self.fatigue_damage, game)
                game.add_log(f"{self.name} takes {self.fatigue_damage} fatigue damage!")

    def start_turn(self, game: 'Game'):
        self.max_mana = min(self.max_mana + 1, 10)
        self.mana = self.max_mana
        self.hero_power_used = False
        self.hero_attacks_this_turn = 0
        
        # Refresh minion attacks
        for minion in self.board:
            minion.refresh_attack()
        
        self.draw_card(game)
        game.add_log(f"--- {self.name}'s turn (Mana: {self.mana}/{self.max_mana}) ---")

    def take_damage(self, amount: int, game: 'Game' = None) -> int:
        """Returns actual damage taken after armor"""
        if self.armor > 0:
            absorbed = min(self.armor, amount)
            self.armor -= absorbed
            amount -= absorbed
            if game and absorbed > 0:
                game.add_log(f"{self.name}'s armor absorbs {absorbed} damage")
        self.health -= amount
        return amount

    def heal(self, amount: int) -> int:
        old_health = self.health
        self.health = min(self.health + amount, self.max_health)
        return self.health - old_health

    def gain_armor(self, amount: int, game: 'Game' = None):
        self.armor += amount
        if game:
            game.add_log(f"{self.name} gains {amount} armor")

    def is_dead(self) -> bool:
        return self.health <= 0

    def has_taunt(self) -> bool:
        return any(m.taunt and not m.stealth for m in self.board)

    def get_taunt_minions(self) -> List['Minion']:
        return [m for m in self.board if m.taunt and not m.stealth]

    def remove_dead_minions(self, game: 'Game'):
        dead = [m for m in self.board if m.is_dead()]
        for minion in dead:
            if minion.deathrattle and not minion.silenced:
                minion.deathrattle(self, game)
            self.board.remove(minion)
            game.add_log(f"{minion.name} dies!")

    def get_attack_power(self) -> int:
        """Get hero's attack power (from weapon)"""
        if self.weapon:
            return self.weapon.attack
        return 0

    def can_hero_attack(self) -> bool:
        return self.weapon is not None and self.hero_attacks_this_turn == 0

    def hero_attack(self, target, game: 'Game') -> bool:
        if not self.can_hero_attack():
            return False
        
        damage = self.weapon.attack
        target_name = target.name if hasattr(target, 'name') else "enemy hero"
        game.add_log(f"{self.name} attacks {target_name} for {damage} damage")
        
        target.take_damage(damage, game)
        
        # Take damage back from minions
        if hasattr(target, 'attack'):
            self.take_damage(target.attack, game)
        
        # Use weapon durability
        if self.weapon.use():
            game.add_log(f"{self.weapon.name} breaks!")
            if self.weapon.deathrattle:
                self.weapon.deathrattle(self, game)
            self.weapon = None
        
        self.hero_attacks_this_turn += 1
        return True

    def use_hero_power(self, game: 'Game', target=None) -> bool:
        if self.hero_power_used:
            game.add_log("Hero power already used this turn!")
            return False
        if self.mana < 2:
            game.add_log("Not enough mana for hero power!")
            return False
        
        self.mana -= 2
        self.hero_power_used = True
        
        if self.hero_power:
            self.hero_power(self, game, target)
        
        return True

    def __repr__(self):
        return f"{self.name} - HP: {self.health} | Armor: {self.armor} | Mana: {self.mana}/{self.max_mana}"

from typing import TYPE_CHECKING, Optional, Callable

if TYPE_CHECKING:
    from .player import Player
    from .game import Game


class Minion:
    def __init__(self, name: str, attack: int, health: int, 
                 taunt: bool = False, charge: bool = False, divine_shield: bool = False,
                 windfury: bool = False, stealth: bool = False, poisonous: bool = False,
                 lifesteal: bool = False, deathrattle: Optional[Callable] = None):
        self.name = name
        self.attack = attack
        self.base_attack = attack
        self.health = health
        self.max_health = health
        self.taunt = taunt
        self.charge = charge
        self.divine_shield = divine_shield
        self.windfury = windfury
        self.stealth = stealth
        self.poisonous = poisonous
        self.lifesteal = lifesteal
        self.deathrattle = deathrattle
        
        # Attack state
        self.can_attack = charge
        self.attacks_this_turn = 0
        self.max_attacks = 2 if windfury else 1
        
        # Buffs tracking
        self.frozen = False
        self.silenced = False

    def take_damage(self, amount: int, game: 'Game' = None) -> bool:
        """Returns True if minion dies"""
        if self.divine_shield and amount > 0:
            self.divine_shield = False
            if game:
                game.add_log(f"{self.name}'s Divine Shield absorbs the damage!")
            return False
        
        self.health -= amount
        return self.health <= 0

    def heal(self, amount: int):
        old_health = self.health
        self.health = min(self.health + amount, self.max_health)
        return self.health - old_health

    def is_dead(self) -> bool:
        return self.health <= 0

    def can_attack_now(self) -> bool:
        if self.frozen:
            return False
        if not self.can_attack:
            return False
        if self.attacks_this_turn >= self.max_attacks:
            return False
        if self.attack <= 0:
            return False
        return True

    def attack_target(self, target, owner: 'Player', game: 'Game') -> bool:
        """Attack another minion or hero"""
        if not self.can_attack_now():
            return False

        # Stealth breaks when attacking
        if self.stealth:
            self.stealth = False
            game.add_log(f"{self.name} breaks stealth!")

        target_name = target.name if hasattr(target, 'name') else "enemy hero"
        game.add_log(f"{self.name} attacks {target_name} for {self.attack} damage")

        # Deal damage to target
        target.take_damage(self.attack, game)
        
        # Lifesteal
        if self.lifesteal:
            owner.heal(self.attack)
            game.add_log(f"{self.name} heals {owner.name} for {self.attack}")
        
        # Poisonous kills minions instantly
        if self.poisonous and isinstance(target, Minion) and not target.is_dead():
            target.health = 0
            game.add_log(f"{self.name}'s poison destroys {target.name}!")
        
        # Take damage back from minions
        if isinstance(target, Minion):
            self.take_damage(target.attack, game)
            if target.poisonous and not self.is_dead():
                self.health = 0
                game.add_log(f"{target.name}'s poison destroys {self.name}!")
            if target.lifesteal:
                enemy = game.get_opponent(owner)
                enemy.heal(target.attack)
        
        self.attacks_this_turn += 1
        return True

    def refresh_attack(self):
        """Called at start of turn"""
        self.can_attack = True
        self.attacks_this_turn = 0
        self.frozen = False

    def silence(self, game: 'Game'):
        """Remove all card text and enchantments"""
        self.taunt = False
        self.divine_shield = False
        self.windfury = False
        self.stealth = False
        self.poisonous = False
        self.lifesteal = False
        self.deathrattle = None
        self.silenced = True
        self.max_attacks = 1
        game.add_log(f"{self.name} is silenced!")

    def buff(self, attack_buff: int, health_buff: int, game: 'Game' = None):
        """Apply a buff to the minion"""
        self.attack += attack_buff
        self.health += health_buff
        self.max_health += health_buff
        if game:
            game.add_log(f"{self.name} gains +{attack_buff}/+{health_buff}")

    def __repr__(self):
        attrs = []
        if self.taunt: attrs.append("T")
        if self.divine_shield: attrs.append("DS")
        if self.windfury: attrs.append("W")
        if self.stealth: attrs.append("S")
        if self.poisonous: attrs.append("P")
        if self.frozen: attrs.append("F")
        attr_str = f" [{','.join(attrs)}]" if attrs else ""
        return f"{self.name} ({self.attack}/{self.health}){attr_str}"

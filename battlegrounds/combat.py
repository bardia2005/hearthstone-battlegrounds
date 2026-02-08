import random
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from .minion import BGMinion
from .player import BGPlayer


@dataclass
class CombatEvent:
    event_uuid: str
    step: int
    payload: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "combat_event",
            "event_uuid": self.event_uuid,
            "step": self.step,
            "payload": self.payload
        }


class CombatSimulator:
    """Simulates Battlegrounds combat between two boards"""
    
    def __init__(self, seed: Optional[int] = None):
        self.seed = seed or random.randint(0, 999999)
        random.seed(self.seed)
        self.events: List[CombatEvent] = []
        self.step = 0
        self.player_board: List[BGMinion] = []
        self.opponent_board: List[BGMinion] = []
        self.attacker_side = "player"
        self.player_attack_index = 0
        self.opponent_attack_index = 0
    
    def setup(self, player_minions: List[BGMinion], opponent_minions: List[BGMinion], first_attacker: str = ""):
        """Setup combat boards"""
        self.player_board = [m.copy() for m in player_minions]
        self.opponent_board = [m.copy() for m in opponent_minions]
        
        # Assign slots
        for i, m in enumerate(self.player_board):
            m.slot = i
            m.attacks_this_combat = 0
        for i, m in enumerate(self.opponent_board):
            m.slot = i
            m.attacks_this_combat = 0
        
        # Determine first attacker
        if first_attacker:
            self.attacker_side = first_attacker
        elif len(self.player_board) > len(self.opponent_board):
            self.attacker_side = "player"
        elif len(self.opponent_board) > len(self.player_board):
            self.attacker_side = "opponent"
        else:
            self.attacker_side = random.choice(["player", "opponent"])
        
        self._add_event("combat_start", {
            "first_attacker": self.attacker_side,
            "player_board_size": len(self.player_board),
            "opponent_board_size": len(self.opponent_board)
        })
    
    def _add_event(self, kind: str, data: Dict[str, Any]):
        self.step += 1
        event = CombatEvent(
            event_uuid=f"evt-{self.step:03d}",
            step=self.step,
            payload={"kind": kind, **data}
        )
        self.events.append(event)
    
    def _get_attacker_board(self) -> List[BGMinion]:
        return self.player_board if self.attacker_side == "player" else self.opponent_board
    
    def _get_defender_board(self) -> List[BGMinion]:
        return self.opponent_board if self.attacker_side == "player" else self.player_board
    
    def _get_next_attacker(self) -> Optional[BGMinion]:
        board = self._get_attacker_board()
        alive = [m for m in board if not m.is_dead() and m.can_attack()]
        if not alive:
            return None
        
        idx = self.player_attack_index if self.attacker_side == "player" else self.opponent_attack_index
        idx = idx % len(alive) if alive else 0
        return alive[idx] if alive else None
    
    def _get_defender(self, attacker: BGMinion) -> Optional[BGMinion]:
        board = self._get_defender_board()
        alive = [m for m in board if not m.is_dead()]
        if not alive:
            return None
        
        # Taunt check
        taunts = [m for m in alive if m.has_taunt]
        if taunts:
            return random.choice(taunts)
        
        return random.choice(alive)
